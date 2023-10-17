import logging
import rdflib
import pandas as pd
from typing import Any, List, Optional
from urllib import parse
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.processor import SPARQLResult
from spendpoint import service
from fastapi import APIRouter, Query, Request, Response
from fastapi.responses import JSONResponse
from rdflib import ConjunctiveGraph, Literal, URIRef
from rdflib.plugins.sparql.evaluate import evalPart
from rdflib.plugins.sparql.evalutils import _eval
from rdflib.plugins.sparql.parserutils import CompValue
from rdflib.plugins.sparql.sparql import QueryContext, SPARQLError
from rdflib.namespace import CSVW, DC, DCAT, DCTERMS, DOAP, FOAF, ODRL2, ORG, OWL, PROF, PROV, RDF, RDFS, SDO, SH, SKOS, SOSA, SSN, TIME, VOID, XMLNS, XSD


CONTENT_TYPE_TO_RDFLIB_FORMAT = {
    # https://www.w3.org/TR/sparql11-results-json/
    "application/sparql-results+json": "json",
    "application/json": "json",
    "text/json": "json",
    # https://www.w3.org/TR/rdf-sparql-XMLres/
    "application/sparql-results+xml": "xml",
    "application/xml": "xml",  # for compatibility
    "application/rdf+xml": "xml",  # for compatibility
    "text/xml": "xml",  # not standard
    # https://www.w3.org/TR/sparql11-results-csv-tsv/
    "application/sparql-results+csv": "csv",
    "text/csv": "csv",  # for compatibility
    # Extras
    "text/turtle": "ttl",
}
DEFAULT_CONTENT_TYPE = "application/json"


def parse_accept_header(accept: str) -> List[str]:
    """
    Given an accept header string, return a list of media types in order of preference.

    :param accept: Accept header value
    :return: Ordered list of media type preferences
    """

    def _parse_preference(qpref: str) -> float:
        qparts = qpref.split("=")
        try:
            return float(qparts[1].strip())
        except ValueError:
            pass
        except IndexError:
            pass
        return 1.0

    preferences = []
    types = accept.split(",")
    dpref = 2.0
    for mtype in types:
        parts = mtype.split(";")
        parts = [part.strip() for part in parts]
        pref = dpref
        try:
            for part in parts[1:]:
                if part.startswith("q="):
                    pref = _parse_preference(part)
                    break
        except IndexError:
            pass
        # preserve order of appearance in the list
        dpref = dpref - 0.01
        preferences.append((parts[0], pref))
    preferences.sort(key=lambda x: -x[1])
    return [pref[0] for pref in preferences]


def add_cell_to_graph(graph: ConjunctiveGraph, iri: str, row: int, column: int, cell_value: Any, verbose: bool) -> None:
    """Adds a Cell as known in the SDO2L ontology to the graph."""
    tabular_prefix = "http://ua.be/sdo2l/vocabulary/formalism/tabular"
    cell = URIRef(f"{iri}-cell-{row}-{column}")
    # Store the triples in a temporary graph. This allows us to use the rdflib query engine for the sub-query instead of finding the matching pairs manually.
    graph.add((cell, URIRef(f"{tabular_prefix}#holdsContent"), Literal(cell_value)))
    graph.add((cell, URIRef(f"{tabular_prefix}#hasRowPosition"), Literal(int(row))))
    graph.add((cell, URIRef(f"{tabular_prefix}#hasColumnPosition"), Literal(int(column))))

    if verbose:
        graph.add((cell, URIRef(f"{tabular_prefix}#isCellOfTabularData"), URIRef(f"{iri}")))
        graph.add((cell, URIRef(f"{tabular_prefix}#isInCollection"), URIRef(f"{iri}-column-{int(column)}")))
        graph.add((cell, URIRef(f"{tabular_prefix}#isInCollection"), URIRef(f"{iri}-row-{int(row)}")))

        graph.add((cell, RDF.type, OWL.Thing))
        graph.add((cell, RDF.type, URIRef("http://ua.be/sdo2l/vocabulary/formalism/tabular#Cell")))
        graph.add((cell, RDF.type, URIRef("http://ua.be/sdo2l/vocabulary/formalism/file#Data")))
        graph.add((cell, OWL.sameAs, URIRef(f"{iri}-cell-{int(row)}-{int(column)}")))


class SparqlRouter(APIRouter):
    """Class to deploy a SPARQL endpoint using a RDFLib Graph."""

    def __init__(self, *args: Any, title: str, description: str, version: str, configuration, **kwargs: Any):
        self.title = title
        self.description = description
        self.version = version
        self.configuration = configuration
        super().__init__(*args, **kwargs)
        rdflib.plugins.sparql.CUSTOM_EVALS["evalCustomFunctions"] = self.eval_custom_functions

        async def encode_graph_query_results(request, query_results):
            """"""
            mime_types = parse_accept_header(request.headers.get("accept", DEFAULT_CONTENT_TYPE))
            output_mime_type = DEFAULT_CONTENT_TYPE
            for mime_type in mime_types:
                if mime_type in CONTENT_TYPE_TO_RDFLIB_FORMAT:
                    output_mime_type = mime_type
                    break
            logging.debug(f"Returning {output_mime_type}.")
            try:
                rdflib_format = CONTENT_TYPE_TO_RDFLIB_FORMAT[output_mime_type]
                response = Response(query_results.serialize(format=rdflib_format), media_type=output_mime_type)
            except Exception as e:
                logging.error(f"Error serializing the SPARQL query results with RDFLib: {e}")
                return JSONResponse(status_code=422, content={"message": "Error serializing the SPARQL query results."})
            else:
                return response

        @self.get("/")
        async def sparql_endpoint_get(request: Request, query: Optional[str] = Query(None)) -> Response:
            """Returns an empty result."""
            # The graph is empty, so you would expect this to never return any pairs.
            # But we inject pairs in the custom functions!
            logging.debug("Received GET request.")
            if not query:
                logging.warning("No query provided in GET request!")
                return JSONResponse({"message": "No query provided."})

            graph = ConjunctiveGraph()
            try:
                query_results = graph.query(query)
            except Exception as e:
                logging.error("Error executing the SPARQL query on the RDFLib Graph: " + str(e))
                return JSONResponse(status_code=400, content={"message": "Error executing the SPARQL query on the RDFLib Graph."})

            return await encode_graph_query_results(request, query_results)

        @self.post("/")
        async def sparql_endpoint_post(request: Request, query: Optional[str] = Query(None)) -> Response:
            """Returns an empty result."""
            logging.debug("Received POST request.")
            if not query:
                query_body = await request.body()
                body = query_body.decode("utf-8")
                parsed_query = parse.parse_qsl(body)
                for params in parsed_query:
                    if params[0] == "query":
                        query = parse.unquote(params[1])
            return await sparql_endpoint_get(request, query)

        @self.get("/cell/")
        async def sparql_cell_endpoint_get(request: Request, iri, file_name, row, column, verbose: bool = True, query: Optional[str] = Query(None)) -> Response:
            """
            SELECT ?s ?p ?o WHERE {
              BIND(ENCODE_FOR_URI("http://ua.be/sdo2l/description/artifacts/artifacts#random-artefact") as ?e)
              BIND(uri(concat("http://localhost:8000/cell/?iri=", ?e ,"&row=2&column=2&file_name=example.csv")) as ?c)
              SERVICE ?c {?s ?p ?o}
            }
            """
            logging.debug(f"Received cell GET request [{iri}:{file_name}->{row}:{column}].")
            graph = ConjunctiveGraph()
            graph_ns = dict(graph.namespaces())
            # graph_ns["tabular"] = "http://ua.be/sdo2l/vocabulary/formalisms/tabular#"
            df = pd.read_csv(f"data/{file_name}", index_col=None, header=None)
            cell_value = df.iat[int(row), int(column)]
            add_cell_to_graph(graph, iri, int(row), int(column),cell_value, verbose)
            logging.debug(f"{cell_value=}")

            try:
                query_results = graph.query(query, initNs=graph_ns)
            except Exception as e:
                logging.error("Error executing the SPARQL query on the RDFLib Graph: " + str(e))
                return JSONResponse(status_code=400, content={"message": "Error executing the SPARQL query on the RDFLib Graph."})
            return await encode_graph_query_results(request, query_results)

        @self.get("/cell/{iri}/{file_name}/")
        async def sparql_sheet_endpoint_get(request: Request, iri, file_name, query: Optional[str] = Query(None), verbose: bool = True) -> Response:
            """Return all cell in SDO2L notation for a file."""
            logging.debug(f"Received sheet GET request [{file_name}].")
            graph = ConjunctiveGraph()
            graph_ns = dict(graph.namespaces())
            # graph_ns["tabular"] = "http://ua.be/sdo2l/vocabulary/formalisms/tabular#"
            df = pd.read_csv(f"data/{file_name}", index_col=None, header=None)
            df.reset_index()

            # Please forgive me pandas gods
            for row in range(df.shape[0]):
                for column in range(df.shape[1]):
                    cell_value = df.at[row, column]
                    add_cell_to_graph(graph, iri, int(row), int(column), cell_value, verbose)

            try:
                query_results = graph.query(query, initNs=graph_ns)
            except Exception as e:
                logging.error("Error executing the SPARQL query on the RDFLib Graph: " + str(e))
                return JSONResponse(status_code=400, content={"message": "Error executing the SPARQL query on the RDFLib Graph."})
            return await encode_graph_query_results(request, query_results)

        @self.get("/cell/{iri}/{file_name}/{row}/{column}/")
        async def sparql_cell_endpoint_get(request: Request, iri, file_name, row, column, query: Optional[str] = Query(None), verbose: bool = True) -> Response:
            """
            Create an ephemeral graph store based on the call parameters and perform the requested query.
            SELECT ?s ?p ?o WHERE {
              bind(str('http://localhost:8000') as ?base)
              bind(str('iri') as ?iri)
              bind(str('cell') as ?operation)
              bind(str('example.csv') as ?file)
              bind(str(2) as ?row)
              bind(str(2) as ?column)
              bind(iri(concat(?base, "/", ?operation, "/", ?file, "/", ?row, "/", ?column, "/")) as ?call)
              SERVICE ?call {?s ?p ?o}
            }
            """
            logging.debug(f"Received cell GET request [{file_name}->{row}:{column}].")
            graph = ConjunctiveGraph()
            graph_ns = dict(graph.namespaces())
            # graph_ns["tabular"] = "http://ua.be/sdo2l/vocabulary/formalisms/tabular#"
            df = pd.read_csv(f"data/{file_name}", index_col=None, header=None)
            cell_value = df.iat[int(row), int(column)]
            add_cell_to_graph(graph, iri, int(row), int(column), cell_value, verbose)
            logging.debug(f"{cell_value=}")

            try:
                query_results = graph.query(query, initNs=graph_ns)
            except Exception as e:
                logging.error("Error executing the SPARQL query on the RDFLib Graph: " + str(e))
                return JSONResponse(status_code=400, content={"message": "Error executing the SPARQL query on the RDFLib Graph."})
            return await encode_graph_query_results(request, query_results)


    def eval_custom_functions(self, ctx: QueryContext, part: CompValue) -> List[SPARQLResult]:
        if part.name != "Extend":
            raise NotImplementedError()

        query_results = []
        logging.debug("Custom evaluation.")
        for eval_part in evalPart(ctx, part.p):
            # Checks if the function is a URI (custom function)
            if hasattr(part.expr, "iri"):
                for conf_service in self.configuration.services:
                    # Check if URI correspond to a registered custom function
                    if part.expr.iri == URIRef(conf_service.namespace):
                        query_results, ctx, part, eval_part = getattr(service, conf_service.call)(query_results, ctx, part, eval_part, conf_service)
            else:
                # For built-in SPARQL functions (that are not URIs)
                evaluation: List[Any] = [_eval(part.expr, eval_part.forget(ctx, _except=part._vars))]
                if isinstance(evaluation[0], SPARQLError):
                    raise evaluation[0]
                # Append results for built-in SPARQL functions
                for result in evaluation:
                    query_results.append(eval_part.merge({part.var: Literal(result)}))
        return query_results

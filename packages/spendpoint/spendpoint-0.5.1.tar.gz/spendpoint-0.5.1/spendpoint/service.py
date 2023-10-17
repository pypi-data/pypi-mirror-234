import logging
from pathlib import Path

import arklog
import rdflib
import pandas as pd
from rdflib import Literal, XSD
from rdflib.plugins.sparql.evalutils import _eval
from dataclasses import dataclass
from timeit import default_timer as timer
from spendpoint.bridge import fetch_outliers
arklog.set_config_logging()


@dataclass(init=True, repr=True, order=False, frozen=True)
class Outlier:
    iri: str
    value: str

def outlier_service(query_results, ctx, part, eval_part, service_configuration):
    """
    Example query:
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dtf:  <https://ontology.rys.app/dt/function/>
    PREFIX owl:  <http://www.w3.org/2002/07/owl#>

    SELECT ?outlier ?outlier_relation ?outlier_value WHERE {
      SERVICE <http://127.0.0.1:8000/> {
        SELECT ?outlier ?outlier_relation ?outlier_value WHERE {
          BIND(dtf:outlier("rotation.csv", "2", "<http://ua.be/drivetrain/description/artifacts/artifacts#drivetrain-sensor-data-v1>") AS ?outlier)
        }
      }
    }

    :param query_results:
    :param ctx:
    :param part:
    :param eval_part:
    :param service_configuration:
    :return:
    """
    logging.debug(f"Outlier service '{service_configuration.namespace}'.")
    file_name = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))
    column = str(_eval(part.expr.expr[1], eval_part.forget(ctx, _except=part.expr._vars)))
    iri = str(_eval(part.expr.expr[2], eval_part.forget(ctx, _except=part.expr._vars)))
    logging.info(f"Looking for outlier in '{file_name}' at column '{column}' for '{iri}'.")
    outlier_graph = fetch_outliers(file_name, column, iri, service_configuration.endpoint, service_configuration.timeout)
    for stmt in outlier_graph:
        query_results.append(eval_part.merge({
            part.var: stmt[0],
            rdflib.term.Variable(part.var + "_relation") : stmt[1],
            rdflib.term.Variable(part.var + "_value") : stmt[2],
        }))
    logging.debug(f"{query_results=}")
    return query_results, ctx, part, eval_part


def conversion_service(query_results, ctx, part, eval_part, service_configuration):
    """"""
    logging.debug(f"Conversion service '{service_configuration.namespace}'.")
    input_file_name = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))
    output_file_name = str(_eval(part.expr.expr[1], eval_part.forget(ctx, _except=part.expr._vars)))
    data_dir = Path(__file__).resolve().parent.parent / Path("data")
    input_file_path = data_dir / Path(input_file_name)
    output_file_path = data_dir / Path(output_file_name)
    success = False
    start_time = timer()
    if input_file_path.suffix.endswith("csv") and output_file_path.suffix.endswith("parquet"):
        df = pd.read_csv(input_file_path)
        df.to_parquet(output_file_path)
        success = True
    end_time = timer()
    query_results.append(eval_part.merge({
        part.var: Literal(""),
        rdflib.term.Variable(part.var + "_input") : Literal(input_file_name),
        rdflib.term.Variable(part.var + "_output") : Literal(output_file_name),
        rdflib.term.Variable(part.var + "_duration") : Literal(end_time - start_time, datatype=XSD.duration),
        rdflib.term.Variable(part.var + "_success") : Literal(success),
    }))
    return query_results, ctx, part, eval_part


def example_service(query_results, ctx, part, eval_part, service_configuration):
    """"""
    logging.debug(f"{query_results=}")
    logging.debug(f"{ctx=}")
    logging.debug(f"{part=}")
    logging.debug(f"{eval_part=}")

    file_name = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))
    column = str(_eval(part.expr.expr[1], eval_part.forget(ctx, _except=part.expr._vars)))
    logging.info(f"Looking for outlier in '{file_name}' at column '{column}'.")

    outliers = [
        Outlier(iri="example_0",value="2.0"),
        Outlier(iri="example_1",value="2.5"),
        Outlier(iri="example_2",value="3.0"),
    ]

    for outlier in outliers:
        query_results.append(eval_part.merge({part.var: Literal(outlier.iri), rdflib.term.Variable(part.var + "_value"): Literal(outlier.value)}))
    return query_results, ctx, part, eval_part


# TODO maybe return a 'cell' type
def cell_service(query_results, ctx, part, eval_part, service_configuration):
    """"""
    logging.debug(f"{query_results=}")
    logging.debug(f"{ctx=}")
    logging.debug(f"{part=}")
    logging.debug(f"{eval_part=}")

    file_name = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))
    row = str(_eval(part.expr.expr[1], eval_part.forget(ctx, _except=part.expr._vars)))
    column = str(_eval(part.expr.expr[2], eval_part.forget(ctx, _except=part.expr._vars)))

    # TODO Should probably grab some setting from the KG, like header etc, maybe do that in query
    logging.info(f"Looking for cell {row}:{column} in '{file_name}'.")
    try:
        df = pd.read_csv(file_name, index_col=None, header=None)
        cell_value = df.iat[int(row), int(column)]
        query_results.append(eval_part.merge({
            part.var: Literal(cell_value),
            rdflib.term.Variable(part.var + "_value"): Literal(cell_value)
        }))
        logging.debug(f"{cell_value=}")
    except:
        # TODO Expand error info
        logging.error(f"Error.")

    return query_results, ctx, part, eval_part

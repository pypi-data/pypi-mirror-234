import logging
from urllib.error import URLError
import arklog
from SPARQLWrapper import SPARQLWrapper, JSON

arklog.set_config_logging()

prefixes = "\n".join((
    "PREFIX dtf:  <https://ontology.rys.app/dt/function/>",
    "PREFIX owl:  <http://www.w3.org/2002/07/owl#>",
    "PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
    "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>",
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
))


# TODO Convert to test
def query_0():
    """"""
    sparql = SPARQLWrapper("http://localhost:8000")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(
        prefixes +
        """
        SELECT ?outlier ?outlier_value WHERE {
            BIND(dtf:outlier("data.csv", "2") AS ?outlier)
        }
        """
    )
    try:
        ret = sparql.query().convert()
    except URLError as e:
        logging.error(e)
        return
    if not ret:
        logging.info("No outliers!")
    for r in ret["results"]["bindings"]:
        logging.info(r)


# TODO Convert to test
def query_1():
    """"""
    sparql = SPARQLWrapper("http://localhost:8000")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(
        prefixes +
        """
        SELECT ?outlier WHERE {
            SERVICE <http://localhost:8000/> {
                SELECT ?outlier ?outlier_value WHERE {
                    BIND(dtf:outlier("data2.csv", "1") AS ?outlier)
                }
            }
        }
        """
    )
    try:
        ret = sparql.query().convert()
    except URLError as e:
        logging.error(e)
        return
    if not ret:
        logging.info("No outliers!")
    for r in ret["results"]["bindings"]:
        logging.info(r)


# TODO Convert to test
def query_2():
    """"""
    sparql = SPARQLWrapper("http://localhost:8000")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(
        prefixes +
        """
        SELECT ?outlier ?outlier_relation ?outlier_value WHERE {
            SERVICE <http://127.0.0.1:8000/> {
                SELECT ?outlier ?outlier_relation ?outlier_value WHERE {
                    BIND(dtf:outlier("rotation.csv", "2", "<http://ua.be/drivetrain/description/artifacts/artifacts#drivetrain-sensor-data-v1>") AS ?outlier)
                }
            }
        }
        """
    )
    try:
        ret = sparql.query().convert()
    except URLError as e:
        logging.error(e)
        return
    if not ret:
        logging.info("No outliers!")
    for r in ret["results"]["bindings"]:
        logging.info(r)


if __name__ == "__main__":
    query_0()
    query_1()
    query_2()

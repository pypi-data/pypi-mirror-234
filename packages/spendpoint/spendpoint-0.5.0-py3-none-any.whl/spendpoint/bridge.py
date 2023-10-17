import logging
import arklog
import requests
from rdflib import Graph
from typing import Union

arklog.set_config_logging()


def fetch_outliers(file_name: str, column: Union[str, int], iri: str, outlier_service_url: str, timeout: int) -> Graph:
    """"""
    try:
        column = column if isinstance(column, int) else int(column)
    except ValueError as e:
        logging.error(f"Column '{column}' is not parseable to an integer.")
        raise
    parameters = {"iri": iri, "column" : column, "file" : file_name}
    try:
        outliers_result = requests.post(outlier_service_url, json=parameters, timeout=timeout)
        outliers_result.raise_for_status()
    except requests.exceptions.InvalidSchema as e:
        logging.error(f"Invalid schema for '{outlier_service_url}'.")
        raise
    except requests.exceptions.ConnectTimeout as e:
        logging.error(f"Request for '{outlier_service_url}' timed out.")
        raise
    except requests.exceptions.HTTPError as e:
        logging.error(f"Service at '{outlier_service_url}' returned an error.")
        raise
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Service at '{outlier_service_url}' is unreachable.")
        raise
    # logging.debug(outliers_result.content)
    # for stmt in outliers_result.content.decode().split("\n"):
    #     logging.debug(stmt)
    outlier_graph = Graph()
    outlier_graph.parse(data=outliers_result.content.decode(encoding="UTF-8"), format="n3")
    return outlier_graph

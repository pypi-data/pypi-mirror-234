import arklog

from spendpoint.configuration import Configuration
from spendpoint.endpoint import SparqlEndpoint
from spendpoint import __version__

def get_application(configuration: Configuration):
    arklog.set_config_logging()
    functions = [conf_service.namespace for conf_service in configuration.services]
    app = SparqlEndpoint(
        version = __version__,
        title = "SPARQL endpoint for storage and services",
        description = "\n".join((
            "SPARQL endpoint.",
            f"Supports {len(functions)} custom services:",
            *(f" - {service_uri}" for service_uri in functions))
        ),
        configuration=configuration
    )
    return app

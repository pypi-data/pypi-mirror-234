# Copied and modified from https://pypi.org/project/rdflib-endpoint/
# https://fastapi.tiangolo.com/

import logging
import arklog
import time
from typing import Any
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from spendpoint.router import SparqlRouter

arklog.set_config_logging()

class SparqlEndpoint(FastAPI):
    """SPARQL endpoint for services and storage of heterogeneous data."""

    def __init__(self, *args: Any, title: str, description: str, version: str, configuration, **kwargs: Any):
        """"""
        self.title = title
        self.description = description
        self.version = version
        self.configuration = configuration
        super().__init__(*args, title=title, description=description, version=version, **kwargs)
        logging.debug(self.description)
        sparql_router = SparqlRouter(title=title, description=description, version=version, configuration=configuration)
        self.include_router(sparql_router)
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.middleware("http")
        async def add_process_time_header(request: Request, call_next: Any) -> Response:
            start_time = time.time()
            response: Response = await call_next(request)
            duration = str(time.time() - start_time)
            response.headers["X-Process-Time"] = duration
            logging.debug(f"X-Process-Time = {duration}")
            return response

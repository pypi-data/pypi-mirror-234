##########
SpEndPoint
##########

Creates a SPARQL endpoint supporting custom services.
The default access point is at `http://127.0.0.1:8000`.
This endpoint can be configured in the `configuration.toml <data/configuration.toml>`_ file.
The docker image created uses uvicorn the host the application at `0.0.0.0:80`. Feel free to map this to any port of your liking.

Bound services
--------------

We currently support 4 bind services out of the box:

.. code-block::

   dtf:outlier
   dtf:example
   dtf:conversion
   dtf:cell

The outlier service relies on `another endpoint <https://msdl.uantwerpen.be/git/lucasalbertins/DTDesign/src/main/tools/typeOperations>`_ which needs to be set up and accessible.

.. code-block:: sparql

   PREFIX dtf: <https://ontology.rys.app/dt/function/>
   SELECT ?cell ?cell_value WHERE {
     SERVICE <http://localhost:8000/> {BIND(dtf:cell("data/example.csv", 0, 0) AS ?cell)}
   }

SPARQL query showing bind based cell service call.

URI based services
------------------

A second, more versatile, way to access a service is provided in the form of an URI.
It is possible to query cells by specifying an individual cell in the URI of the service call.

.. code-block:: sparql

   SELECT ?s ?p ?o WHERE {
     BIND(ENCODE_FOR_URI("http://ua.be/sdo2l/description/artifacts/artifacts#random-artefact") as ?e)
     BIND(uri(concat("http://localhost:8000/cell/?iri=", ?e ,"&row=2&column=2&file_name=example.csv")) as ?c)
     SERVICE ?c {?s ?p ?o}
   }

SPARQL query showing URI based cell service call.

Installation
------------

..
   .. code-block:: shell

      pip install spendpoint

   or

.. code-block:: shell

   pip install --index-url https://pip:glpat-m8mNfhxZAUnWvy7rLS1x@git.rys.one/api/v4/projects/262/packages/pypi/simple --no-deps spendpoint

Configuration
-------------

A configuration file at `configuration.toml <data/configuration.toml>`_ holds all user configurable data.
You can set the `host` and `port` the server will listen on.
A more advanced use is to import extra services.
These services need to be defined in the `service.py` file as well.

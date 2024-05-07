Server
======

The backend server is a `Flask <https://flask.palletsprojects.com/en/3.0.x/>` server. It is responsible for connecting the users and service providers to PKGs.

Run server
----------

Before starting the server, make sure that the `requirements <https://github.com/iai-group/pkg-api/blob/main/requirements.txt>` are installed and that CORS is disabled in your web browser.

To start the server, run the following command:

.. code-block:: bash

    flask --app pkg_api/server run --debug

Note the `--debug` flag is optional, but it is recommended to use it during development.

By default, the server will run locally on port 5000. In case you want to run the server on a different port, you can specify the port using the `--port` flag.

Routes
------

The server has four main routes that relate to the :doc:`features available <pkg_client>` in the PKG Client:

* `/auth`: Handles the authentication of users and service providers.
* `/nl`: Handles natural language instructions provided by users to manage the PKG.
* `/statements`: Manages the addition and deletion of statements via forms.
* `/explore`: Handles SPARQL queries for the visualization of the PKG.

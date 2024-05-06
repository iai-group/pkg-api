PKG Client
==========

PKG Client is a simple and user-friendly user interface, based on React, to manage a PKG. The management is done through requests sent to the server.

Run PKG Client
--------------

Node.js and npm are required to run PKG Client, more information on how to install them can be found `here <https://docs.npmjs.com/downloading-and-installing-node-js-and-npm>`.

To start PKG Client, run the following commands in the directory `pkg_client`:

.. code-block:: bash

    npm install
    npm start

Note that `npm install` only needs to be run once, unless the dependencies change. For more information on how to run the client, refer to the README in the `pkg_client` directory.

In case the server is not running on the default port (i.e., 5000), `PKG_API_BASE_URL` in `pkg_client/public/config.json` must be updated accordingly.

Features
--------

PKG Client provides the following features:

* **Login/Registration**: To access their PKG, users must be logged in. If they do not have an account, they can register.
* **Home**: The home page provides a text input field where users can enter their management instructions (i.e., add, remove, and retrieve statements) in natural language. After being processed by the server, the outcome of the instructions is displayed. The home page also provides a button to visualize the PKG.
* **Populate PKG**: Users can populate their PKG by adding or removing statements via a form. This feature assumes that the user is familiar with the `PKG vocabulary <https://iai-group.github.io/pkg-vocabulary/>`.
* **Explore PKG**: Users can visualize their PKG or a part of it as an RDF graph. The visualization is generated based on the results of a SPARQL query, hence, this feature is intended for advised users.
"""The server module contains the Flask app and the API resources.

Resources give access to HTTP methods related to a PKG API feature.
"""


from flask import Flask
from flask_restful import Api

from pkg_api.connector import DEFAULT_STORE_PATH
from pkg_api.server.auth import AuthResource
from pkg_api.server.facts_management import FactsManagementResource
from pkg_api.server.pkg_exploration import PKGExplorationResource
from pkg_api.server.preference_management import PreferenceManagementResource
from pkg_api.server.service_management import ServiceManagementResource


def create_app(testing: bool = False) -> Flask:
    """Creates the Flask app and add the API resources.

    Args:
        testing: Enable testing mode. Defaults to False.

    Returns:
        Flask app.
    """
    app = Flask(__name__)

    if testing:
        app.config["TESTING"] = True
        # Path to store all the PKGs
        app.config["STORE_PATH"] = "tests/data/RDFStore"
    else:
        app.config["STORE_PATH"] = DEFAULT_STORE_PATH

    api = Api(app)

    api.add_resource(AuthResource, "/auth")
    api.add_resource(ServiceManagementResource, "/service")
    api.add_resource(FactsManagementResource, "/facts")
    api.add_resource(PreferenceManagementResource, "/preference")
    api.add_resource(PKGExplorationResource, "/explore")

    return app

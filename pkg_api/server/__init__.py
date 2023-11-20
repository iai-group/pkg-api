"""The server module contains the Flask app and the API resources.

Resources give access to HTTP methods related to a PKG API feature.
"""

from flask import Flask
from flask_restful import Api

from pkg_api.server.auth import AuthResource
from pkg_api.server.facts_management import PersonalFactsResource
from pkg_api.server.pkg_exploration import PKGExplorationResource
from pkg_api.server.service_management import ServiceManagementResource


def create_app() -> Flask:
    """Create the Flask app and add the API resources.

    Returns:
        The Flask app.
    """
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(AuthResource, "/auth")
    api.add_resource(ServiceManagementResource, "/service")
    api.add_resource(PersonalFactsResource, "/facts")
    api.add_resource(PKGExplorationResource, "/explore")

    return app

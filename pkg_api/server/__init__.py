"""The server module contains the Flask app and the API resources.

Resources give access to HTTP methods related to a PKG API feature.
"""


from flask import Flask
from flask_restful import Api

from pkg_api.server.auth import AuthResource
from pkg_api.server.config import BaseConfig, TestingConfig
from pkg_api.server.models import db
from pkg_api.server.pkg_exploration import PKGExplorationResource
from pkg_api.server.service_management import ServiceManagementResource
from pkg_api.server.statements_management import StatementsManagementResource


def create_app(testing: bool = False) -> Flask:
    """Creates the Flask app and add the API resources.

    Args:
        testing: Enable testing mode. Defaults to False.

    Returns:
        Flask app.
    """
    app = Flask(__name__)

    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(BaseConfig)

    db.init_app(app)

    with app.app_context():
        # Create the database tables
        db.create_all()

    api = Api(app)

    api.add_resource(AuthResource, "/auth")
    api.add_resource(ServiceManagementResource, "/service")
    api.add_resource(StatementsManagementResource, "/statements")
    api.add_resource(PKGExplorationResource, "/explore")

    return app

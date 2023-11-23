"""The server module contains the Flask app and the API resources.

Resources give access to HTTP methods related to a PKG API feature.
"""

from flask import Flask
from flask_restful import Api

from pkg_api.server.auth import AuthResource
from pkg_api.server.models import db
from pkg_api.server.pkg_exploration import PKGExplorationResource
from pkg_api.server.pkg_population import PKGPopulationResource
from pkg_api.server.service_management import ServiceManagementResource


def create_app(testing: bool = False) -> Flask:
    """Create the Flask app and add the API resources.

    Args:
        testing: Enable testing mode. Defaults to False.

    Returns:
        The Flask app.
    """
    app = Flask(__name__)

    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)

    with app.app_context():
        # Create the database tables
        db.create_all()

    api = Api(app)

    api.add_resource(AuthResource, "/auth")
    api.add_resource(ServiceManagementResource, "/service")
    api.add_resource(PKGPopulationResource, "/population")
    api.add_resource(PKGExplorationResource, "/explore")

    return app

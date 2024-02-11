"""The server module contains the Flask app and the API resources.

Resources give access to HTTP methods related to a PKG API feature.
"""

from flask import Flask
from flask_restful import Api

from pkg_api.connector import DEFAULT_STORE_PATH
from pkg_api.pkg import DEFAULT_VISUALIZATION_PATH
from pkg_api.server.auth import AuthResource
from pkg_api.server.facts_management import PersonalFactsResource
from pkg_api.server.models import db
from pkg_api.server.nl_processing import NLResource
from pkg_api.server.pkg_exploration import PKGExplorationResource
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
        app.config["STORE_PATH"] = "tests/data/RDFStore"
        app.config["VISUALIZATION_PATH"] = "tests/data/pkg_visualizations"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
        app.config["STORE_PATH"] = DEFAULT_STORE_PATH
        app.config["VISUALIZATION_PATH"] = DEFAULT_VISUALIZATION_PATH

    db.init_app(app)

    with app.app_context():
        # Create the database tables
        db.create_all()

    api = Api(app)

    api.add_resource(AuthResource, "/auth")
    api.add_resource(ServiceManagementResource, "/service")
    api.add_resource(PersonalFactsResource, "/facts")
    api.add_resource(PKGExplorationResource, "/explore")
    api.add_resource(NLResource, "/nl")

    return app

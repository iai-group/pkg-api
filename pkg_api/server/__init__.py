"""The server module contains the Flask app and the API resources.

Resources give access to HTTP methods related to a PKG API feature.
"""

import os

from flask import Flask
from flask_restful import Api

from pkg_api.server.auth import AuthResource
from pkg_api.server.config import DevelopmentConfig, TestingConfig
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
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Create storage directories
    os.makedirs(app.config["STORE_PATH"], exist_ok=True)
    os.makedirs(app.config["VISUALIZATION_PATH"], exist_ok=True)

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

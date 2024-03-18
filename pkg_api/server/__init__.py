"""The server module contains the Flask app and the API resources.

Resources give access to HTTP methods related to a PKG API feature.
"""

import importlib
import os

from flask import Config, Flask
from flask_restful import Api

from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    ThreeStepStatementAnnotator,
)
from pkg_api.nl_to_pkg.nl_to_pkg import NLtoPKG
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
    api.add_resource(
        NLResource,
        "/nl",
        resource_class_kwargs={"nl_to_pkg": _init_nl_to_pkg(app.config)},
    )

    return app


def _init_nl_to_pkg(config: Config) -> NLtoPKG:
    """Initializes the NL to PKG module.

    Args:
        config: BaseConfig object.

    Returns:
        NLtoPKG object.
    """
    annotator = ThreeStepStatementAnnotator(
        prompt_paths=config["TS_ANNOTATOR_PROMPT_PATHS"],
        config_path=config["TS_ANNOTATOR_CONFIG_PATH"],
    )

    # Create entity linker from config
    entity_module, entity_class = config["ENTITY_LINKER_CONFIG"][
        "class_path"
    ].rsplit(".", maxsplit=1)
    entity_cls_module = importlib.import_module(entity_module)
    entity_cls = getattr(entity_cls_module, entity_class)
    entity_linker = entity_cls(**config["ENTITY_LINKER_CONFIG"]["kwargs"])

    return NLtoPKG(annotator, entity_linker)

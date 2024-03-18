"""Define server configuration."""

from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    _DEFAULT_CONFIG_PATH as DEFAULT_3_STEP_CONFIG_PATH,
)
from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    _DEFAULT_PROMPT_PATHS,
)
from pkg_api.nl_to_pkg.entity_linking.rel_entity_linking import (
    _DEFAULT_API_URL,
)
from pkg_api.pkg import DEFAULT_VISUALIZATION_PATH


class BaseConfig:
    """Base configuration for the server."""

    TESTING = False

    # Three step annotator configuration
    TS_ANNOTATOR_CONFIG_PATH = DEFAULT_3_STEP_CONFIG_PATH
    TS_ANNOTATOR_PROMPT_PATHS = _DEFAULT_PROMPT_PATHS

    # Entity linker configuration. Use REL by default.
    ENTITY_LINKER_CONFIG = {
        "class_path": "pkg_api.nl_to_pkg.entity_linking.rel_entity_linking."
        "RELEntityLinker",
        "kwargs": {"api_url": _DEFAULT_API_URL},
    }


class DevelopmentConfig(BaseConfig):
    """Development configuration for the server."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    STORE_PATH = "data"
    VISUALIZATION_PATH = DEFAULT_VISUALIZATION_PATH


class TestingConfig(BaseConfig):
    """Testing configuration for the server."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.sqlite"
    STORE_PATH = "tests/data/RDFStore"
    VISUALIZATION_PATH = "tests/data/pkg_visualizations"

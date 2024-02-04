"""Define server configuration."""


from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    _DEFAULT_CONFIG_PATH as DEFAULT_3_STEP_CONFIG_PATH,
)
from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    _DEFAULT_PROMPT_PATHS,
)
from pkg_api.nl_to_pkg.entity_linking.spotlight_entity_linker import (
    _DEFAULT_CONFIG_PATH as DEFAULT_SPOTLIGHT_CONFIG_PATH,
)


class BaseConfig:
    """Base configuration for the server."""

    TESTING = False

    # Three step annotator configuration
    TS_ANNOTATOR_CONFIG_PATH = DEFAULT_3_STEP_CONFIG_PATH
    TS_ANNOTATOR_RPOMPT_PATHS = _DEFAULT_PROMPT_PATHS

    # Entity linker configuration
    SPOTLIGHT_CONFIG_PATH = DEFAULT_SPOTLIGHT_CONFIG_PATH


class DevelopmentConfig(BaseConfig):
    """Development configuration for the server."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    STORE_PATH = "data"


class TestingConfig(BaseConfig):
    """Testing configuration for the server."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.sqlite"
    STORE_PATH = "tests/data/RDFStore"

"""Flask configuration classes."""

from pkg_api.connector import DEFAULT_STORE_PATH


class BaseConfig(object):
    """Base configuration class."""

    TESTING = False
    STORE_PATH = DEFAULT_STORE_PATH
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class TestingConfig(BaseConfig):
    """Testing configuration class."""

    TESTING = True
    STORE_PATH = "tests/data/RDFStore"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.sqlite"

"""Fixtures for the pkg_api.server package."""
import os

import pytest
from flask import Flask

from pkg_api.server import create_app


@pytest.fixture(scope="session")
def client() -> Flask:
    """Create the Flask test client and add the API resources.

    Yields:
        The Flask client.
    """
    app = create_app(testing=True)
    client = app.test_client()
    yield client
    # Delete the test database
    os.remove(f"{app.instance_path}/test.sqlite")

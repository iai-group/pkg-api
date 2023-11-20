"""Fixtures for the pkg_api.server package."""
import pytest
from flask import Flask

from pkg_api.server import create_app


@pytest.fixture
def client() -> Flask:
    """Create the Flask test client and add the API resources.

    Yields:
        The Flask client.
    """
    app = create_app()
    client = app.test_client()
    yield client

import pytest
from flask import Flask
from flask_restful import Api

from pkg_api.server.pkg_exploration import PKGExplorationResource


@pytest.fixture
def client():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(PKGExplorationResource, "/explore")
    client = app.test_client()
    yield client


def test_auth_endpoint(client):
    response = client.get("/explore")
    assert response.status_code == 200
    assert response.get_json() == {
        "message": "PKG Exploration"
    }

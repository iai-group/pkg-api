"""Tests for the NL resource endpoint."""
from flask import Flask


def test_nl_resource_post(client: Flask) -> None:
    """Tests POST /nl endpoint."""
    response = client.post("/nl")
    assert response.status_code == 400
    assert response.get_json() == {"message": "Not implemented."}

"""Tests for the pkg exploration endpoints."""

from flask import Flask

from pkg_api.pkg import DEFAULT_VISUALIZATION_PATH


def test_pkg_exploration_endpoint_errors(client: Flask) -> None:
    """Tests /explore endpoints with invalid data."""
    response = client.get(
        "/explore",
        json={
            "owner_username": "test",
        },
    )
    assert response.status_code == 400
    assert response.json["message"] == "Missing owner URI"

    response = client.post(
        "/explore",
        json={
            "owner_username": "test",
        },
    )
    assert response.status_code == 400
    assert response.json["message"] == "Missing owner URI"

    response = client.post(
        "/explore",
        json={
            "owner_uri": "http://example.com#test",
            "owner_username": "test",
            "sparql_query": (
                "INSERT DATA { <http://example.com#test> "
                "<http://example.com#likes> "
                "<http://example.com#icecream> . }"
            ),
        },
    )
    assert response.status_code == 400
    assert (
        response.json["message"]
        == "Operation is not supported. Provide SPARQL select query."
    )


def test_pkg_visualization(client: Flask) -> None:
    """Tests the GET /explore endpoint."""
    response = client.get(
        "/explore",
        json={
            "owner_uri": "http://example.com#test",
            "owner_username": "test",
        },
    )
    assert response.status_code == 200
    assert response.json["message"] == "PKG visualized successfully."
    assert response.json["img_path"] == DEFAULT_VISUALIZATION_PATH + "test.png"


def test_pkg_sparql_query(client: Flask) -> None:
    """Tests the POST /explore endpoint."""
    response = client.post(
        "/explore",
        json={
            "owner_uri": "http://example.com#test",
            "owner_username": "test",
            "sparql_query": (
                "SELECT ?statement WHERE { "
                "<http://example.com#test> "
                "<http://example.com#likes> ?statement . }"
            ),
        },
    )
    assert response.status_code == 200
    assert response.json["message"] == "SPARQL query executed successfully."

"""Tests for the pkg exploration endpoints."""

from flask import Flask


def test_pkg_exploration_endpoint_errors(client: Flask) -> None:
    """Test /explore endpoint with invalid data."""
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
            "owner_uri": "http://example.org/pkg/test",
            "owner_username": "test",
            "sparql_query": (
                "INSERT DATA { <http://example.org/pkg/test> "
                "<http://example.org/likes> "
                "<http://example.org/icecream> . }"
            ),
        },
    )
    assert response.status_code == 400
    assert (
        response.json["message"]
        == "Operation is not supported. Provide SPARQL select query."
    )


def test_pkg_visualization(client: Flask) -> None:
    """Test /explore endpoint."""
    response = client.get(
        "/explore",
        json={
            "owner_uri": "http://example.org/pkg/test",
            "owner_username": "test",
        },
    )
    assert response.status_code == 200
    assert response.json["message"] == "PKG visualized successfully."
    assert response.json["img_path"] == "pkg_api/pkg_visualizations/test.png"


def test_pkg_sparql_query(client: Flask) -> None:
    """Tests the POST /explore endpoint."""
    response = client.post(
        "/explore",
        json={
            "owner_uri": "http://example.org/pkg/test",
            "owner_username": "test",
            "sparql_query": (
                "SELECT ?object WHERE { "
                "<http://example.org/pkg/test> "
                "<http://example.org/likes> ?object . }"
            ),
        },
    )
    assert response.status_code == 200
    assert response.json["message"] == "SPARQL query executed successfully."

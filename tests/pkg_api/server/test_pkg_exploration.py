"""Tests for the pkg exploration endpoints."""

import os

from flask import Flask


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
            "owner_uri": "http://example.org/pkg#test",
            "owner_username": "test",
            "sparql_query": (
                "INSERT DATA { _:st a rdf:Statement ; "
                'rdf:predicate [ a skos:Concept ; dc:description "like" ] ;'
                "rdf:object"
                '[ a skos:Concept ; dc:description "icecream"] . '
                "<http://example.com#test> wi:preference ["
                "pav:derivedFrom _:st ;"
                'wi:topic [ a skos:Concept ; dc:description "icecream"] ;'
                "wo:weight"
                "[ wo:weight_value 1.0 ; wo:scale pkg:StandardScale]] . }"
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
    if not os.path.exists("tests/data/pkg_visualizations/"):
        os.makedirs("tests/data/pkg_visualizations/", exist_ok=True)
    if not os.path.exists("tests/data/RDFStore/"):
        os.makedirs("tests/data/RDFStore/", exist_ok=True)
    response = client.get(
        "/explore",
        json={
            "owner_uri": "http://example.org/pkg#test",
            "owner_username": "test",
        },
    )
    assert response.status_code == 200
    assert response.json["message"] == "PKG visualized successfully."
    assert response.json["img_path"] == "tests/data/pkg_visualizations/test.png"


def test_pkg_sparql_query(client: Flask) -> None:
    """Tests the POST /explore endpoint."""
    if not os.path.exists("tests/data/RDFStore/"):
        os.makedirs("tests/data/RDFStore/", exist_ok=True)
    response = client.post(
        "/explore",
        json={
            "owner_uri": "http://example.org/pkg#test",
            "owner_username": "test",
            "sparql_query": (
                "SELECT ?statement WHERE { "
                "?statement rdf:predicate "
                '[ a skos:Concept ; dc:description "like" ] . }'
            ),
        },
    )
    assert response.status_code == 200
    assert response.json["message"] == "SPARQL query executed successfully."

"""Tests for the pkg exploration endpoints."""

import os
from io import StringIO

import pytest
from flask import Flask

from pkg_api.connector import RDFStore
from pkg_api.core.annotation import PKGData, Triple, TripleElement
from pkg_api.core.pkg_types import URI
from pkg_api.pkg import PKG


@pytest.fixture
def user_pkg() -> PKG:
    """Returns a PKG instance."""
    return PKG(
        "http://example.com#test",
        RDFStore.MEMORY,
        "tests/data/RDFStore/test",
        "tests/data/pkg_visualizations",
    )


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


def test_pkg_visualization(client: Flask, user_pkg: PKG) -> None:
    """Tests the GET /explore endpoint."""
    if not os.path.exists("tests/data/pkg_visualizations/"):
        os.makedirs("tests/data/pkg_visualizations/", exist_ok=True)

    pkg_data = PKGData(
        id="f47ac10b-34fd-4372-a567-0e02b2c3d479",
        statement="I live in Stavanger.",
        triple=Triple(
            TripleElement("I", URI("http://example.com#test")),
            TripleElement("live", "live"),
            TripleElement(
                "Stavanger", URI("https://dbpedia.org/page/Stavanger")
            ),
        ),
        logging_data={"authoredBy": URI("http://example.com#test")},
    )

    user_pkg.add_statement(pkg_data)
    user_pkg._connector.save_graph()

    response = client.get(
        "/explore",
        query_string={
            "owner_uri": "http://example.com#test",
            "owner_username": "test",
        },
    )

    with open("tests/data/pkg_visualizations/test.png", "rb") as img:
        test_image = StringIO(img.read())
    test_image.seek(0)

    assert response.data == test_image.read()


def test_pkg_sparql_query(client: Flask) -> None:
    """Tests the POST /explore endpoint."""
    if not os.path.exists("tests/data/RDFStore/"):
        os.makedirs("tests/data/RDFStore/", exist_ok=True)
    response = client.post(
        "/explore",
        json={
            "owner_uri": "http://example.com#test",
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

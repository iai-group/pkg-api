"""Tests for the NL resource endpoint."""

import uuid
from unittest.mock import patch

from flask import Flask

from pkg_api.core.annotation import (
    Concept,
    PKGData,
    Preference,
    Triple,
    TripleElement,
)
from pkg_api.core.intents import Intent
from pkg_api.core.pkg_types import URI


def test_nl_resource_post_errors(client: Flask) -> None:
    """Tests POST with invalid data."""
    response = client.post("/nl", json={"owner_username": "test"})
    assert response.status_code == 400
    assert response.json == {"message": "Missing owner URI"}

    response = client.post(
        "/nl",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
        },
    )
    assert response.status_code == 400
    assert response.json == {"message": "Missing query"}


def test_nl_resource_post_add_statement(client: Flask) -> None:
    """Tests POST with a valid add statement."""
    statement = PKGData(
        id=uuid.UUID("{583b029c-c667-11ee-9601-a662d3a1cf88}"),
        statement="I like apples.",
        triple=Triple(
            TripleElement("I", URI("http://example.com/test")),
            TripleElement("like", Concept(description="like")),
            TripleElement("apples", Concept(description="apples")),
        ),
        preference=Preference(
            TripleElement("apples", Concept(description="apples")), 1.0
        ),
    )
    with patch("pkg_api.nl_to_pkg.nl_to_pkg.NLtoPKG.annotate") as mock_annotate:
        mock_annotate.return_value = Intent.ADD, statement
        response = client.post(
            "/nl",
            json={
                "owner_uri": "http://example.com/test",
                "owner_username": "test",
                "query": "I like apples.",
            },
        )
        assert response.status_code == 200
        assert response.json == {
            "message": "Statement added to your PKG.",
            "annotation": statement.as_dict(),
        }


def test_nl_resource_post_get_statement(client: Flask) -> None:
    """Tests POST with a valid get statement."""
    with patch("pkg_api.nl_to_pkg.nl_to_pkg.NLtoPKG.annotate") as mock_annotate:
        mock_annotate.return_value = Intent.GET, PKGData(
            id=uuid.UUID("{a0ba1070-c668-11ee-80c6-a662d3a1cf88}"),
            statement="What do I like?",
            triple=Triple(
                TripleElement("I", URI("http://example.com/test")),
                TripleElement("like", Concept(description="like")),
            ),
        )
        response = client.post(
            "/nl",
            json={
                "owner_uri": "http://example.com/test",
                "owner_username": "test",
                "query": "What do I like?",
            },
        )
        assert response.status_code == 200
        assert response.json["message"] == "Statements retrieved from your PKG"
        assert isinstance(response.json["data"], list)
        assert len(response.json["data"]) > 0
        assert isinstance(response.json["annotation"], dict)


def test_nl_resource_post_delete_statement(client: Flask) -> None:
    """Tests POST with a valid delete statement."""
    with patch("pkg_api.nl_to_pkg.nl_to_pkg.NLtoPKG.annotate") as mock_annotate:
        mock_annotate.return_value = Intent.DELETE, PKGData(
            id=uuid.UUID("{1b53c98e-c669-11ee-9c00-a662d3a1cf88}"),
            statement="Forget that I like apples.",
            triple=Triple(
                TripleElement("I", URI("http://example.com/test")),
                TripleElement("like", Concept(description="like")),
                TripleElement("apples", Concept(description="apples")),
            ),
        )
        response = client.post(
            "/nl",
            json={
                "owner_uri": "http://example.com/test",
                "owner_username": "test",
                "query": "Forget that I like apples.",
            },
        )
        assert response.status_code == 200
        assert response.json["message"] == "Statement was deleted if present"
        assert isinstance(response.json["annotation"], dict)

"""Tests for the population endpoint."""

from typing import Any, Dict

import pytest
from flask import Flask

from pkg_api.core.pkg_types import URI, PKGData, Triple, TripleElement
from pkg_api.server.utils import open_pkg


def test_statement_management_with_errors(client: Flask) -> None:
    """Tests /statements endpoint with errors."""
    response = client.post("/statements", json={})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Missing owner URI"}

    response = client.delete("/statements", json={})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Missing owner URI"}


@pytest.fixture
def request_data() -> Dict[str, Any]:
    """Returns request data."""
    return {
        "owner_uri": "http://example.org/pkg#test",
        "owner_username": "test",
        "description": "I like Tom Cruise",
        "subject": "http://example.org/pkg#test",
        "predicate": {"value": {"description": "like"}},
        "object": "https://en.wikipedia.org/wiki/Tom_Cruise",
    }


def test_statement_management_post(
    client: Flask, request_data: Dict[str, Any]
) -> None:
    """Tests POST /statements endpoint."""
    response = client.post("/statements", json=request_data)
    assert response.status_code == 200
    assert response.get_json() == {"message": "Statement added successfully"}

    with client.application.app_context():
        pkg = open_pkg(request_data)
        statements = pkg.get_statements(
            PKGData(
                id=None,
                statement="I like Tom Cruise",
                triple=Triple(
                    None,
                    None,
                    TripleElement(
                        "Tom Cruise",
                        URI("https://en.wikipedia.org/wiki/Tom_Cruise"),
                    ),
                ),
            )
        )
        assert "I like Tom Cruise" in [
            statement.statement for statement in statements
        ]
        pkg.close()


def test_statement_management_delete(
    client: Flask, request_data: Dict[str, Any]
) -> None:
    """Tests DELETE /statements endpoint."""
    response = client.delete("/statements", json=request_data)
    assert response.status_code == 200
    assert response.get_json() == {"message": "Statement removed successfully"}

    with client.application.app_context():
        pkg = open_pkg(request_data)
        statements = pkg.get_statements(
            PKGData(
                id=None,
                statement="I like Tom Cruise",
                triple=Triple(
                    None,
                    None,
                    TripleElement(
                        "Tom Cruise",
                        URI("https://en.wikipedia.org/wiki/Tom_Cruise"),
                    ),
                ),
            )
        )
        assert "I like Tom Cruise" not in [
            statement.statement for statement in statements
        ]
        pkg.close()

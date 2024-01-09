"""Tests for preference management endpoints."""

from flask import Flask


def test_preference_endpoints_erros(client: Flask) -> None:
    """Tests /preference endpoints with invalid data."""
    response = client.get(
        "/preference",
        json={
            "owner_username": "test",
            "subject_uri": "http://example.com/test",
            "entity_uri": "http://example.com/Stavanger",
        },
    )
    assert response.status_code == 400
    assert response.json == {"message": "Missing owner URI"}

    response = client.post(
        "/preference",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
            "entity_uri": "http://example.com/Stavanger",
        },
    )
    assert response.status_code == 400
    assert response.json == {"message": "Missing preference data"}


def test_add_preference(client: Flask) -> None:
    """Tests the POST /preference endpoint."""
    response = client.post(
        "/preference",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
            "subject_uri": "http://example.com/test",
            "entity_uri": "http://example.com/Stavanger",
            "preference": 1.0,
        },
    )
    assert response.status_code == 200
    assert response.json == {"message": "Preference added successfully"}


def test_get_preference(client: Flask) -> None:
    """Tests the GET /preference endpoint."""
    response = client.get(
        "/preference",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
            "subject_uri": "http://example.com/test",
            "entity_uri": "http://example.com/Stavanger",
        },
    )
    assert response.status_code == 200
    assert response.json == {
        "data": 1.0,
        "message": "Preference retrieved successfully",
    }

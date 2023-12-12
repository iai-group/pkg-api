"""Tests for the facts management endpoints."""


from flask import Flask


def test_fact_endpoint_errors(client: Flask) -> None:
    """Tests /facts endpoints with invalid data."""
    response = client.get(
        "/facts",
        json={
            "owner_username": "test",
            "subject_uri": "http://example.com/test",
            "predicate": "http://example.com/livesIn",
            "entity_uri": "http://example.com/Stavanger",
        },
    )
    assert response.status_code == 400
    assert response.json == {"message": "Missing owner URI"}

    response = client.post(
        "/facts",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
            "predicate": "http://example.com/livesIn",
            "entity_uri": "http://example.com/Stavanger",
        },
    )
    assert response.status_code == 400
    assert response.json == {"message": "Missing fact data"}


def test_add_fact(client: Flask) -> None:
    """Tests the POST /facts endpoint."""
    response = client.post(
        "/facts",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
            "subject_uri": "http://example.com/test",
            "predicate": "http://example.com/livesIn",
            "entity_uri": "http://example.com/Stavanger",
        },
    )
    assert response.status_code == 200
    assert response.json == {"message": "Fact added successfully"}


def test_get_fact(client: Flask) -> None:
    """Tests the GET /facts endpoint."""
    response = client.get(
        "/facts",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
            "subject_uri": "http://example.com/test",
            "predicate": "http://example.com/livesIn",
        },
    )
    assert response.status_code == 200
    assert response.json == {
        "data": ["http://example.com/Stavanger"],
        "message": "Fact retrieved successfully",
    }


def test_remove_fact(client: Flask) -> None:
    """Tests the DELETE /facts endpoint."""
    response = client.delete(
        "/facts",
        json={
            "owner_uri": "http://example.com/test",
            "owner_username": "test",
            "subject_uri": "http://example.com/test",
            "predicate": "http://example.com/livesIn",
            "entity_uri": "http://example.com/Stavanger",
        },
    )
    assert response.status_code == 200
    assert response.json == {"message": "Fact deleted successfully"}

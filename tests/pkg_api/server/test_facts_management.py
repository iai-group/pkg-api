"""Tests for the facts management endpoints."""


def test_facts_management_endpoint(client) -> None:
    """Test the facts endpoint."""
    response = client.get("/facts")
    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Personal Facts/Preferences Management"
    }

"""Tests for the auth endpoints."""


def test_auth_endpoint(client) -> None:
    """Test the auth endpoint."""
    response = client.get("/auth")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Prompt for login/signup"}

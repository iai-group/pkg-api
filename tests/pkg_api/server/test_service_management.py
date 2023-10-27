"""Tests for the service management endpoints."""


def test_service_management_endpoint(client) -> None:
    """Test the service management endpoint."""
    response = client.get("/service")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Service Management"}

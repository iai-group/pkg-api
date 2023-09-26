"""Tests for the pkg exploration endpoints."""


def test_pkg_exploration_endpoint(client) -> None:
    """Test the pkg exploration endpoint."""
    response = client.get("/explore")
    assert response.status_code == 200
    assert response.get_json() == {"message": "PKG Exploration"}

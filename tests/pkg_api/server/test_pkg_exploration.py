def test_auth_endpoint(client):
    response = client.get("/explore")
    assert response.status_code == 200
    assert response.get_json() == {"message": "PKG Exploration"}

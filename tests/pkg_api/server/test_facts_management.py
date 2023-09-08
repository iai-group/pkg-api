def test_auth_endpoint(client):
    response = client.get("/facts")
    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Personal Facts/Preferences Management"
    }

"""Tests for the auth endpoints."""


def test_auth_endpoint_error(client) -> None:
    """Test the auth endpoint."""
    response = client.post("/auth", json={})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Missing username or password"}


def test_auth_endpoint_register(client) -> None:
    """Tests user registration."""
    response = client.post(
        "/auth",
        json={
            "username": "user1",
            "password": "pass1",
            "isRegistration": True,
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "user": {"username": "user1", "uri": "http://example.com#user1"},
        "message": "Login successful",
    }


def test_auth_endpoint_register_existing_user(client) -> None:
    """Tests user registration with an existing user."""
    response = client.post(
        "/auth",
        json={
            "username": "user1",
            "password": "pass1",
            "isRegistration": True,
        },
    )
    assert response.status_code == 400
    assert response.get_json() == {"message": "This username already exists."}


def test_auth_endpoint_login(client) -> None:
    """Tests user login."""
    response = client.post(
        "/auth",
        json={
            "username": "user1",
            "password": "pass1",
            "isRegistration": False,
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "user": {"username": "user1", "uri": "http://example.com#user1"},
        "message": "Login successful",
    }


def test_auth_endpoint_login_wrong_password(client) -> None:
    """Tests user login with wrong password."""
    response = client.post(
        "/auth",
        json={
            "username": "user1",
            "password": "wrong_password",
            "isRegistration": False,
        },
    )
    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid username or password."}


def test_auth_endpoint_login_wrong_username(client) -> None:
    """Tests user login with wrong username."""
    response = client.post(
        "/auth",
        json={
            "username": "wrong_username",
            "password": "pass1",
            "isRegistration": False,
        },
    )
    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid username or password."}

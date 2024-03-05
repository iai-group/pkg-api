"""Authentication resource."""

from typing import Any, Dict, Tuple

from flask import request
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from pkg_api.server.models import User, db

# TODO: Retrieve namespace from the mapping class
# See issue: https://github.com/iai-group/pkg-api/issues/13
NS = "http://example.com#"


def create_user_uri(username: str) -> str:
    """Creates the user URI from the username."""
    return f"{NS}{username}"


class AuthResource(Resource):
    def post(self) -> Tuple[Dict[str, Any], int]:
        """Logs in or registers the user.

        Returns:
            A dictionary with the user data and a message and the status code.
        """
        authentication_data = request.json
        username = authentication_data.get("username", None)
        password = authentication_data.get("password", None)
        is_registration = authentication_data.get("isRegistration", False)

        if not username or not password:
            return {"message": "Missing username or password"}, 400

        # Retrieve the first user with the given username from the database.
        user = User.query.filter_by(username=username).first()

        if is_registration:
            if not user:
                user = User(
                    username=username,
                    uri=create_user_uri(username),
                    password=generate_password_hash(password),
                )
                db.session.add(user)
                db.session.commit()
            else:
                return {"message": "This username already exists."}, 400
        else:
            if not user or not check_password_hash(user.password, password):
                return {"message": "Invalid username or password."}, 401

        return {
            "user": {
                "username": user.username,
                "uri": user.uri,
            },
            "message": "Login successful",
        }, 200

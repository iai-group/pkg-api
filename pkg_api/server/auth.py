"""Authentication resource."""

from flask_restful import Resource


class AuthResource(Resource):
    def get(self):
        """Returns the authentication data."""
        return {"message": "Prompt for login/signup"}

"""Authentication resource."""

from typing import Dict

from flask_restful import Resource


class AuthResource(Resource):
    def get(self) -> Dict[str, str]:
        """Returns the authentication data.
        
        Returns:
            Dict[str, str]: The authentication data.
        """
        return {"message": "Prompt for login/signup"}

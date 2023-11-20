"""Service Management API."""
from typing import Dict

from flask_restful import Resource


class ServiceManagementResource(Resource):
    def get(self) -> Dict[str, str]:
        """Returns the service management data."""
        return {"message": "Service Management"}

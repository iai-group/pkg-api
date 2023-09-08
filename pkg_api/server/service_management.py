"""Service Management API."""
from flask_restful import Resource


class ServiceManagementResource(Resource):
    def get(self):
        """Returns the service management data."""
        return {"message": "Service Management"}

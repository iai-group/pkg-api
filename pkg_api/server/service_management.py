"""Service Management API."""
from typing import Any, Dict, Tuple

from flask import request
from flask_restful import Resource

from pkg_api.server.models import Service, ServiceAccess, db

# TODO: Retrieve namespace from the mapping class
# See issue: https://github.com/iai-group/pkg-api/issues/13
NS = "http://example.org/pkg/"

def create_service_uri(service_name: str) -> str:
    """Creates the service URI from the service name."""
    return f"{NS}{service_name}"

def create_fact_uri(fact_name: str) -> str:
    """Creates the service URI from the service name."""
    return f"{NS}{fact_name}"

class ServiceManagementResource(Resource):
    def get(self) -> Dict[str, str]:
        """Returns the service management data."""
        return {"message": "Service Management"}
    
    def post(self) -> Tuple[Dict[str, Any], int]:
        """Adds, changes or deletes the service access.

        Returns:
            A dictionary with the service/fact access data and a message and the status code.
        """
        authorization_data = request.json
        service_name = authorization_data.get("serviceName", None)
        fact_name = authorization_data.get("factName", None)
        write_access = authorization_data.get("isWrite", False)
        read_access = authorization_data.get("isRead", False)
        is_delete = authorization_data.get("isDelete", False)

        if is_delete:
            # TODO: Implement deletion of the service
            return {
                "service_access": {
                "service_name": service_name,
                "fact_name": fact_name,
                "read_access": write_access,
                "write_access": read_access
            },
            "message": "Service removal not yet implemented."},
        else:
            if not service_name or not fact_name:
                return {"message": "Missing service name or fact name"}, 400

            service_uri = create_service_uri(service_name)
            fact_uri = create_fact_uri(fact_name)
            service = Service.query.filter_by(service_uri=service_uri).first()
            service_access = ServiceAccess.query.filter_by(service_uri=service_uri, fact_uri=fact_name).first()

            if not service:
                # Service does not exist yet
                # Create service
                service = Service(
                    service_name=service_name,
                    service_uri=create_service_uri(service_name)
                )
                db.session.add(service)
                db.session.commit()

            if not service_access:
                # Create service access
                service_access = ServiceAccess(
                    service_uri=service_uri,
                    fact_uri=fact_uri,
                    access_read=read_access,
                    access_write=write_access
                )
                db.session.add(service_access)
            else:
                # Update access rights
                service_access.access_read = read_access
                service_access.access_write = write_access

            db.session.commit()

            return {
            "service_access": {
                "service_name": service.service_name,
                "service_uri": service.service_uri,
                "fact_name": fact_name,
                "fact_uri": fact_uri,
                "read_access": service_access.access_read,
                "write_access": service_access.access_write
            },
            "message": "Service access was added/changed successfully.",
    }, 200

"""Preference Management API resource."""
from typing import Any, Dict, Tuple

from flask import request
from flask_restful import Resource

from pkg_api.server.utils import open_pkg, parse_pouplation_request_data


class PreferenceManagementResource(Resource):
    def get(self) -> Tuple[Dict[str, Any], int]:
        """Retrieves a preference given constraints.

        Returns:
            A dictionary containing the preference and a message, and status
              code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

        subject_uri, _, entity_uri, _ = parse_pouplation_request_data(data)
        if subject_uri is None or entity_uri is None:
            return {"message": "Missing preference data"}, 400

        preference = pkg.get_preference(subject_uri, entity_uri)
        pkg.close()
        return {
            "data": preference,
            "message": "Preference retrieved successfully",
        }, 200

    def post(self) -> Tuple[Dict[str, str], int]:
        """Adds a preference to the PKG.

        Returns:
            A dictionary containing a message, and status code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

        subject_uri, _, entity_uri, preference = parse_pouplation_request_data(
            data
        )
        if subject_uri is None or entity_uri is None or preference is None:
            return {"message": "Missing preference data"}, 400

        pkg.set_preference(subject_uri, entity_uri, preference)
        pkg.close()
        return {"message": "Preference added successfully"}, 200

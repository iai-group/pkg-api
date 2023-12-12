"""Facts Management API Resource."""
from typing import Dict, Tuple

from flask import request
from flask_restful import Resource

from pkg_api.server.utils import open_pkg, parse_pouplation_request_data


class FactsManagementResource(Resource):
    def get(self) -> Tuple[Dict[str, str], int]:
        """Returns a fact given constraints.

        Returns:
            A dictionary containing the fact and a message, and the status code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

        subject_uri, predicate, _, _ = parse_pouplation_request_data(data)
        if subject_uri is None or predicate is None:
            return {"message": "Missing fact data"}, 400

        objects = pkg.get_objects_from_facts(subject_uri, predicate)
        pkg.close()
        return {"data": objects, "message": "Fact retrieved successfully"}, 200

    def post(self) -> Tuple[Dict[str, str], int]:
        """Adds a fact to the PKG.

        Returns:
            A dictionary containing a message, and the status code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

        subject_uri, predicate, entity_uri, _ = parse_pouplation_request_data(
            data
        )
        if subject_uri is None or predicate is None or entity_uri is None:
            return {"message": "Missing fact data"}, 400

        pkg.add_fact(subject_uri, predicate, entity_uri)
        pkg.close()
        return {"message": "Fact added successfully"}, 200

    def delete(self) -> Tuple[Dict[str, str], int]:
        """Deletes a fact from the PKG.

        Returns:
            A dictionary containing a message, and the status code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

        subject_uri, predicate, entity_uri, _ = parse_pouplation_request_data(
            data
        )
        if subject_uri is None or predicate is None or entity_uri is None:
            return {"message": "Missing fact data"}, 400

        pkg.remove_fact(subject_uri, predicate, entity_uri)
        pkg.close()
        return {"message": "Fact deleted successfully"}, 200

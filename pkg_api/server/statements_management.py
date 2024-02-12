"""Statements Management API Resource."""

from typing import Dict, Tuple

from flask import request
from flask_restful import Resource

from pkg_api.server.utils import (
    open_pkg,
    parse_query_statement_population_data,
)


class StatementsManagementResource(Resource):
    def post(self) -> Tuple[Dict[str, str], int]:
        """Adds a statement to the PKG.

        Returns:
            A dictionary containing a message, and the status code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

        try:
            pkg_data = parse_query_statement_population_data(data)
            pkg.add_statement(pkg_data)
            pkg.close()
        except Exception as e:
            return {"message": str(e)}, 400

        return {"message": "Statement added successfully"}, 200

    def delete(self) -> Tuple[Dict[str, str], int]:
        """Deletes a statement from the PKG.

        Returns:
            A dictionary containing a message, and the status code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

        try:
            pkg_data = parse_query_statement_population_data(data)
            # Uncomment when PR #93 is merged
            # pkg.remove_statement(pkg_data)
            pkg.close()
        except Exception as e:
            return {"message": str(e)}, 400

        return {"message": "Statement removed successfully"}, 200

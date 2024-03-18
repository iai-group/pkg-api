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

        Raises:
            KeyError: if there is missing information to open the user's PKG,
              or if the statement is missing.

        Returns:
            A dictionary containing a message and the status code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except KeyError as e:
            return {"message": e.args[0]}, 400

        try:
            pkg_data = parse_query_statement_population_data(data)
            pkg.add_statement(pkg_data)
            pkg.close()
        except KeyError as e:
            return {"message": e.args[0]}, 400

        return {"message": "Statement added successfully"}, 200

    def delete(self) -> Tuple[Dict[str, str], int]:
        """Deletes a statement from the PKG.

        Raises:
            KeyError: if there is missing information to open the user's PKG, or
              if the statement is missing.

        Returns:
            A dictionary containing a message and the status code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except KeyError as e:
            return {"message": e.args[0]}, 400

        try:
            pkg_data = parse_query_statement_population_data(data)
            pkg.remove_statement(pkg_data)
            pkg.close()
        except KeyError as e:
            return {"message": e.args[0]}, 400

        return {"message": "Statement removed successfully"}, 200

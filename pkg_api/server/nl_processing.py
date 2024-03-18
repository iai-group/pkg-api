"""API Resource receiving NL input."""

from typing import Any, Dict, Tuple

from flask import request
from flask_restful import Resource

from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.nl_to_pkg import NLtoPKG
from pkg_api.server.utils import open_pkg


class NLResource(Resource):
    def __init__(self, nl_to_pkg: NLtoPKG) -> None:
        """Initializes the NL resource.

        Args:
            nl_to_pkg: NLtoPKG object.
        """
        self.nl_to_pkg = nl_to_pkg

    def post(self) -> Tuple[Dict[str, Any], int]:
        """Processes the NL input to update the PKG.

        Note that the returned dictionary may contain additional fields based
        on the frontend's needs.

        Raises:
            KeyError: if there is missing information to open the user's PKG.

        Returns:
            A tuple with a dictionary containing a message, and the status code.
        """
        data = request.json

        try:
            pkg = open_pkg(data)
        except KeyError as e:
            return {"message": e.args[0]}, 400

        query = data.get("query", None)
        if not query:
            return {"message": "Missing query"}, 400

        intent, statement_data = self.nl_to_pkg.annotate(query)
        if intent == Intent.ADD:
            pkg.add_statement(statement_data)
            pkg.close()
            return {
                "message": "Statement added to your PKG.",
                "annotation": statement_data.as_dict(),
            }, 200
        elif intent == Intent.GET:
            statements = pkg.get_statements(
                statement_data, triple_conditioned=True
            )
            return {
                "message": "Statements retrieved from your PKG",
                "data": [s.as_dict() for s in statements],
                "annotation": statement_data.as_dict(),
            }, 200
        elif intent == Intent.DELETE:
            pkg.remove_statement(statement_data)
            pkg.close()
            return {
                "message": "Statement was deleted if present",
                "annotation": statement_data.as_dict(),
            }, 200

        return {
            "message": "The operation could not be performed. Please try to"
            " rephrase your query."
        }, 200

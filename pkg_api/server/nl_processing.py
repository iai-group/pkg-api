"""API Resource receiving NL input."""

from typing import Any, Dict, Tuple

from flask import current_app, request
from flask_restful import Resource

from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    ThreeStepStatementAnnotator,
)
from pkg_api.nl_to_pkg.entity_linking.rel_entity_linking import RELEntityLinker
from pkg_api.nl_to_pkg.nl_to_pkg import NLtoPKG
from pkg_api.server.utils import open_pkg


class NLResource(Resource):
    def __init__(self) -> None:
        """Initializes the NL resource."""
        self.annotator = ThreeStepStatementAnnotator(
            prompt_paths=current_app.config["TS_ANNOTATOR_RPOMPT_PATHS"],
            config_path=current_app.config["TS_ANNOTATOR_CONFIG_PATH"],
        )
        self.entity_linker = RELEntityLinker()
        self.nl_to_pkg = NLtoPKG(self.annotator, self.entity_linker)

    def post(self) -> Tuple[Dict[str, Any], int]:
        """Processes the NL input to update the PKG.

        Note that the returned dictionary may contain additional fields based
        on the frontend's needs.

        Returns:
            A tuple with a dictionary containing a message, and the status code.
        """
        data = request.json

        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

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

"""API Resource receiving NL input."""

from typing import Dict, Tuple

from flask import current_app, request
from flask_restful import Resource

from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    ThreeStepStatementAnnotator,
)
from pkg_api.nl_to_pkg.entity_linking.spotlight_entity_linker import (
    SpotlightEntityLinker,
)
from pkg_api.nl_to_pkg.nl_to_pkg import NLtoPKG
from pkg_api.server.utils import open_pkg


class NLResource(Resource):
    def __init__(self) -> None:
        """Initializes the NL resource."""
        self.annotator = ThreeStepStatementAnnotator(
            prompt_paths=current_app.config["TS_ANNOTATOR_RPOMPT_PATHS"],
            config_path=current_app.config["TS_ANNOTATOR_CONFIG_PATH"],
        )
        self.entity_linker = SpotlightEntityLinker(
            current_app.config["SPOTLIGHT_CONFIG_PATH"]
        )
        self.nl_to_pkg = NLtoPKG(self.annotator, self.entity_linker)

    def post(self) -> Tuple[Dict[str, str], int]:
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
            return {"message": "Statement added to your PKG."}, 200
        elif intent == Intent.GET:
            return {"message": "GET not implemented."}, 400
        elif intent == Intent.DELETE:
            return {"message": "DELETE not implemented."}, 400

        return {
            "message": "The operation could not be performed. Please try to"
            " rephrase your query."
        }, 200

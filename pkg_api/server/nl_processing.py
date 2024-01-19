"""API Resource receiving NL input."""

from typing import Dict, Tuple

from flask_restful import Resource


class NLResource(Resource):
    def post(self) -> Tuple[Dict[str, str], int]:
        """Processes the NL input to update the PKG.

        Note that the returned dictionary may contain additional fields based
        on the frontend's needs.

        Returns:
            A tuple with a dictionary containing a message, and the status code.
        """
        # TODO: Implement this method following the approved pipeline.
        # See issue: https://github.com/iai-group/pkg-api/issues/78
        return {"message": "Not implemented."}, 400

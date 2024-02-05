"""PKG Exploration Resource."""
from typing import Any, Dict, Tuple

import flask
from flask import Response, request
from flask_restful import Resource

from pkg_api.server.utils import open_pkg, parse_query_request_data


class PKGExplorationResource(Resource):
    def get(self) -> Response:
        """Returns the PKG visualization.

        Returns:
            A response containing the image of the PKG graph.
        """
        data = dict(request.args)
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

        graph_img_path = pkg.visualize_graph()
        pkg.close()

        return flask.send_file(graph_img_path, mimetype="image/png")

    def post(self) -> Tuple[Dict[str, Any], int]:
        """Executes the SPARQL query.

        Returns:
            A dictionary with the result of running SPARQL query and the status
            code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": str(e)}, 400

        sparql_query = parse_query_request_data(data)

        if "SELECT" in sparql_query:
            result = pkg.execute_sparql_query(sparql_query)
            # TODO: Update pkg.visualize_graph() to return partial graph based
            # on the query result
        else:
            return {
                "message": (
                    "Operation is not supported. Provide SPARQL select "
                    "query."
                )
            }, 400

        pkg.close()

        return {
            "message": "SPARQL query executed successfully.",
            "result": str(result.bindings),
        }, 200

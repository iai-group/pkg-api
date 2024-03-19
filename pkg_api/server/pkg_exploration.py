"""PKG Exploration Resource."""

from typing import Any, Dict, Tuple

from flask import request
from flask_restful import Resource

from pkg_api.server.utils import open_pkg, parse_query_request_data


class PKGExplorationResource(Resource):
    def get(self) -> Tuple[Dict[str, Any], int]:
        """Returns the PKG visualization.

        Returns:
            A dictionary with the path to PKG visualization and the status code.
        """
        data = request.json
        try:
            pkg = open_pkg(data)
        except Exception as e:
            return {"message": e.args[0]}, 400

        graph_img_path = pkg.visualize_graph()
        pkg.close()

        return {
            "message": "PKG visualized successfully.",
            "img_path": graph_img_path,
        }, 200

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
            return {"message": e.args[0]}, 400

        sparql_query = parse_query_request_data(data)

        if "SELECT" in sparql_query:
            result = str(pkg.execute_sparql_query(sparql_query))
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
            "data": result,
        }, 200

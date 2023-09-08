"""PKG Exploration Resource."""
from flask_restful import Resource


class PKGExplorationResource(Resource):
    def get(self):
        """Returns the data for PKG exploration."""
        return {"message": "PKG Exploration"}

"""PKG Exploration Resource."""
from typing import Dict

from flask_restful import Resource


class PKGExplorationResource(Resource):
    def get(self) -> Dict[str, str]:
        """Returns the data for PKG exploration.
        
        Returns:
            Dict[str, str]: The data for PKG exploration.
        """
        return {"message": "PKG Exploration"}

"""Facts Management API Resource."""
from typing import Dict

from flask_restful import Resource


class PersonalFactsResource(Resource):
    def get(self) -> Dict[str, str]:
        """Returns the personal facts/preferences management data."""
        return {"message": "Personal Facts/Preferences Management"}

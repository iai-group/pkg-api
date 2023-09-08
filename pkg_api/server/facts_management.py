"""Facts Management API Resource."""
from flask_restful import Resource


class PersonalFactsResource(Resource):
    def get(self):
        """Returns the personal facts/preferences management data."""
        return {"message": "Personal Facts/Preferences Management"}

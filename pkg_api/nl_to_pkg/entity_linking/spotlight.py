from pprint import pprint
from typing import Any, Dict

import requests

from pkg_api.core.annotations import Concept, PKGData, Triple
from pkg_api.nl_to_pkg.entity_linking.entity_linker import EntityLinker
from pkg_api.util.load_config import load_yaml_config

_DEFAULT_CONFIG_PATH = "config/entity_linking/dbpedia_spotlight.yaml"


class SpotlightEntityLinker(EntityLinker):
    def __init__(self):
        self._config = load_yaml_config(_DEFAULT_CONFIG_PATH)

    def link_annotation_entities(self, pkg_data: PKGData) -> PKGData:
        if pkg_data.triple is None or pkg_data.triple.object is None:
            return pkg_data

        linked_entities = self._link_statement_entities(
            pkg_data.triple.object.description
        )
        if linked_entities is None or "Resources" not in linked_entities:
            return pkg_data

        for entity in linked_entities["Resources"]:
            pkg_data.triple.object.related_entities.append(entity["@URI"])

        return pkg_data

    def _link_statement_entities(self, text: str) -> Dict[str, Any]:
        params = {**self._config["params"], "text": text}
        response = requests.get(
            self._config["url"], headers=self._config["headers"], params=params
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}


if __name__ == "__main__":
    pkg_data = PKGData(
        "I dislike all movies with the actor Tom Cruise.",
        Triple(
            "I",
            Concept("dislike"),
            Concept("all movies with the actor Tom Cruise"),
        ),
    )
    pkg_data = PKGData(
        "Bob likes Oppenheimer.",
        Triple(
            "Bob",
            Concept("likes"),
            Concept("Oppenheimer"),
        ),
    )
    linker = SpotlightEntityLinker()
    pprint(linker.link_annotation_entities(pkg_data))

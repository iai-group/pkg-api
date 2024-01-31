"""This module contains the DBpedia Spotlight entity linker."""

from typing import Any, Dict, Union

import requests

from pkg_api.core.annotation import Concept, PKGData, Triple, TripleElement
from pkg_api.nl_to_pkg.entity_linking.entity_linker import EntityLinker
from pkg_api.pkg_types import URI
from pkg_api.util.load_config import load_yaml_config

_DEFAULT_CONFIG_PATH = "config/entity_linking/dbpedia_spotlight.yaml"


class SpotlightEntityLinker(EntityLinker):
    def __init__(self):
        """Initializes the DBpedia Spotlight entity linker."""
        self._config = load_yaml_config(_DEFAULT_CONFIG_PATH)

    def link_annotation_entities(self, pkg_data: PKGData) -> PKGData:
        """Returns the PKG data with linked entities.

        Args:
            pkg_data: The PKG data to be annotated.

        Returns:
            The PKG data with linked entities.
        """
        if pkg_data.triple is None:
            return pkg_data

        for attr in ["predicate", "object"]:
            triple_element = getattr(pkg_data.triple, attr)
            if triple_element is not None:
                triple_element.reference = self._get_linked_text(
                    triple_element.value
                )

        return pkg_data

    def _get_linked_text(self, value: str) -> Union[URI, Concept, str]:
        """Returns the triple element with linked entities.

        Args:
            triple_element: The triple element to be annotated.

        Returns:
            The triple element with linked entities.
        """
        linked_entities = self._get_linker_response(value)
        if linked_entities is None or "Resources" not in linked_entities:
            return Concept(value)

        # If the entire value is a single entity, return the URI.
        if (
            len(linked_entities["Resources"]) == 1
            and linked_entities["Resources"][0]["@surfaceForm"] == value
        ):
            return linked_entities["Resources"][0]["@URI"]

        # Otherwise, return a concept with the linked entities.
        reference = Concept(value)
        for entity in linked_entities["Resources"]:
            reference.related_entities.append(entity["@URI"])

        return reference

    def _get_linker_response(self, text: str) -> Dict[str, Any]:
        """Returns the response from the DBpedia Spotlight API.

        Args:
            text: The text to be annotated.

        Returns:
            The response from the DBpedia Spotlight API.
        """
        params = {**self._config["params"], "text": text}
        response = requests.get(
            self._config["url"], headers=self._config["headers"], params=params
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}


if __name__ == "__main__":
    linker = SpotlightEntityLinker()

    pkg_data = PKGData(
        "I dislike all movies with the actor Tom Cruise.",
        Triple(
            TripleElement("I"),
            TripleElement("dislike"),
            TripleElement("all movies with the actor Tom Cruise"),
        ),
    )
    linker.link_annotation_entities(pkg_data)
    print(pkg_data)
    pkg_data = PKGData(
        "Bob likes Oppenheimer.",
        Triple(
            TripleElement("Bob"),
            TripleElement("likes"),
            TripleElement("Oppenheimer"),
        ),
    )
    linker.link_annotation_entities(pkg_data)
    print(pkg_data)

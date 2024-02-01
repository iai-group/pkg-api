"""This module contains the DBpedia Spotlight entity linker."""

from typing import Any, Dict, Union

import requests

from pkg_api.core.annotation import Concept, PKGData, TripleElement
from pkg_api.core.pkg_types import URI
from pkg_api.nl_to_pkg.entity_linking.entity_linker import EntityLinker
from pkg_api.util.load_config import load_yaml_config

_DEFAULT_CONFIG_PATH = "config/entity_linking/dbpedia_spotlight.yaml"


class SpotlightEntityLinker(EntityLinker):
    def __init__(self, path: str = _DEFAULT_CONFIG_PATH) -> None:
        """Initializes the DBpedia Spotlight entity linker.

        Args:
            path: The path to the config file. Defaults to _DEFAULT_CONFIG_PATH.
        """
        self._config = load_yaml_config(path)

    def link_annotation_entities(self, pkg_data: PKGData) -> PKGData:
        """Returns the PKG data with linked entities.

        Only the predicate and object of the triple are linked to a public KG,
        as the subject should be retrieved from the PKG.

        Args:
            pkg_data: The PKG data to be annotated.

        Returns:
            The PKG data with linked entities.
        """
        if pkg_data.triple is None:
            return pkg_data

        for attr in ["predicate", "object"]:
            triple_element: TripleElement = getattr(pkg_data.triple, attr)
            if triple_element is not None:
                triple_element.value = self._get_linked_text(
                    triple_element.reference
                )

        return pkg_data

    def _get_linked_text(self, reference: str) -> Union[URI, Concept, str]:
        """Returns the linked object as URI, Concept or literal.

        Args:
            reference: The reference text to be linked.

        Returns:
            The linked object.
        """
        # Return Concept as default as we cannot distinguish between Concept
        # and literal.
        linked_entities = self._get_linker_response(reference)
        if linked_entities is None or "Resources" not in linked_entities:
            return Concept(reference)

        # If the entire value is a single entity, return the URI.
        if (
            len(linked_entities["Resources"]) == 1
            and linked_entities["Resources"][0]["@surfaceForm"] == reference
        ):
            return URI(linked_entities["Resources"][0]["@URI"])

        # Otherwise, return a concept with the linked entities.
        value = Concept(reference)
        for entity in linked_entities["Resources"]:
            value.related_entities.append(entity["@URI"])

        return value

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

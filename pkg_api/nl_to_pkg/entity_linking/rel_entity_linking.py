"""REL entity linker."""

from typing import Any, List, Optional, Union

import requests

from pkg_api.core.annotation import Concept, PKGData, TripleElement
from pkg_api.core.pkg_types import URI
from pkg_api.nl_to_pkg.entity_linking.entity_linker import EntityLinker

_DEFAULT_API_URL = "https://rel.cs.ru.nl/api"


class RELEntityLinker(EntityLinker):
    def __init__(self, api_url: str = _DEFAULT_API_URL) -> None:
        """Initializes the REL entity linker.

        Args:
            api_url: The URL of the REL API. Defaults to _DEFAULT_API_URL.
        """
        self._api_url = api_url
        self._template_uri = "https://en.wikipedia.org/wiki/{entity_name}"

    def link_entities(self, pkg_data: PKGData) -> PKGData:
        """Returns the PKG data with linked entities.

        Only the predicate and object of the triple are linked to a public KG,
        as the subject should be retrieved from the PKG.

        Args:
            pkg_data: The PKG data to be linked.

        Returns:
            The PKG data with linked entities.
        """
        if pkg_data.triple is None:
            return pkg_data

        for attr in ["predicate", "object"]:
            triple_element: TripleElement = getattr(pkg_data.triple, attr)
            if triple_element is not None:
                triple_element.value = self._get_linked_entity(
                    triple_element.reference
                )

        return pkg_data

    def _get_linked_entity(self, reference: str) -> Union[URI, Concept, str]:
        """Returns the linked object as URI, Concept or literal.

        Args:
            reference: The reference text to be linked.

        Returns:
            The linked entity.
        """
        # Return Concept as default as we cannot distinguish between Concept
        # and literal.
        linked_entities = self._get_linker_response(reference)
        if linked_entities is None:
            return Concept(reference)

        if len(linked_entities) == 1 and linked_entities[0][2] == reference:
            return URI(
                self._template_uri.format(entity_name=linked_entities[0][3])
            )

        value = Concept(description=reference)
        for _, _, _, entity_name, _, _, _ in linked_entities:
            value.related_entities.append(
                URI(self._template_uri.format(entity_name=entity_name))
            )

        return value

    def _get_linker_response(self, reference: str) -> Optional[List[List[Any]]]:
        """Returns the response from the REL API.

        For each entity linked, the response contains the following information:
        start index, end index, surface form, entity name, ED confidence, MD
        confidence, and tag.

        Args:
            reference: The reference text to be linked.

        Returns:
            The response from the REL API.
        """
        el_response = requests.post(
            self._api_url, json={"text": reference, "spans": []}
        )
        if el_response.status_code != 200:
            return None
        return el_response.json()

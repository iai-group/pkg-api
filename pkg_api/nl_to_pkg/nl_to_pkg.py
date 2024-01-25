"""Class for annotating a statement with a linked triple and a preference."""

from typing import Tuple

from pkg_api.core.annotations import PKGData
from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg import EntityLinker, StatementAnnotator


class NLtoPKG:
    def __init__(
        self, annotator: StatementAnnotator, entity_linker: EntityLinker
    ) -> None:
        """Initializes the NLtoPKG class."""
        self._annotator = annotator
        self._entity_linker = entity_linker

    def annotate(self, statement: str) -> Tuple[Intent, PKGData]:
        """Returns a tuple of the intent and the annotated and linked statement.

        Args:
            statement: The statement to be annotated.

        Returns:
            A tuple of the intent and the annotated and linked statement.
        """
        intent, pkg_data = self._annotator.get_annotations(statement)

        if pkg_data.triple is None:
            return pkg_data

        linked_triple = self._entity_linker.link_annotation_entities(
            statement, pkg_data.triple
        )
        if pkg_data.preference and linked_triple.object:
            pkg_data.preference.topic = linked_triple.object
        pkg_data.triple = linked_triple

        return intent, pkg_data

"""Class for annotating a statement with a linked triple and a preference."""

from typing import Tuple

from pkg_api.core.annotation import PKGData
from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg import EntityLinker, StatementAnnotator


class NLtoPKG:
    def __init__(
        self, annotator: StatementAnnotator, entity_linker: EntityLinker
    ) -> None:
        """Initializes the NLtoPKG class.

        Args:
            annotator: The statement annotator to use.
            entity_linker: The entity linker to use.
        """
        self._annotator = annotator
        self._entity_linker = entity_linker

    def annotate(self, statement: str) -> Tuple[Intent, PKGData]:
        """Annotates the statement with intent, linked triple, and preference.

        Args:
            statement: The statement to be annotated.

        Returns:
            A tuple of the intent and the annotated and linked statement.
        """
        intent, pkg_data = self._annotator.get_annotations(statement)
        linked_pkg_data = self._entity_linker.link_annotation_entities(pkg_data)

        return intent, linked_pkg_data

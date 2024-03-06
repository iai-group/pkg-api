"""Class for annotating a natural language query.

The main purpose is to return the intent (ADD | GET | DELETE) and to
annotate the triple (subject, predicate, object) and the preference (1 |
-1) in the query.
"""

from abc import ABC, abstractmethod
from typing import Tuple

from pkg_api.core.intents import Intent
from pkg_api.core.pkg_types import PKGData
from pkg_api.nl_to_pkg.llm.prompt import Prompt


class StatementAnnotator(ABC):
    def __init__(self) -> None:
        """Initializes the statement annotator."""
        self._prompt = Prompt()

    @abstractmethod
    def get_annotations(self, statement: str) -> Tuple[Intent, PKGData]:
        """Returns a tuple of the intent and the annotated statement.

        Args:
            statement: The statement to be annotated.

        Raises:
            NotImplementedError: If the method is not implemented.

        Returns:
            A tuple of the intent and the annotated statement as PKGData.
        """
        raise NotImplementedError

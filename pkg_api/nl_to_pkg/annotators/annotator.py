"""Class for annotating a natural language query.

The main purpose is to return users intent (ADD | GET | DELETE) and to annotate
the triples (subject, predicate, object) and the preferences (1 | -1) in the
query.
"""


from abc import ABC, abstractmethod
from typing import Tuple

from pkg_api.core.annotations import PKGData
from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.annotators.prompt import Prompt


class StatementAnnotator(ABC):
    def __init__(self) -> None:
        """Initializes the NLtoAPI class.

        Args:
            path: Path to the file containing the prompt.
        """
        self._prompt = Prompt()

    @abstractmethod
    def get_annotations(self, statement: str) -> Tuple[Intent, PKGData]:
        """Returns a tuple of the intent and the annotated statement.

        Args:
            statement: The statement to be annotated.

        Raises:
            NotImplementedError: If the method is not implemented.

        Returns:
            A tuple of the intent and the annotated statement.
        """
        raise NotImplementedError

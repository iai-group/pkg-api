"""A three-step annotator for annotating a statement.

This module contains a three-step annotator for annotating a statement
with a triple and a preference using LLM.
"""


import re
from typing import Optional, Tuple

from pkg_api.core.annotation import PKGData, Preference, Triple, TripleElement
from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.annotators.annotator import StatementAnnotator
from pkg_api.nl_to_pkg.llm.llm_connector import LLMConnector
from pkg_api.nl_to_pkg.llm.prompt import Prompt

_DEFAULT_PROMPT_PATHS = {
    "intent": "data/llm_prompts/default/intent.txt",
    "triple": "data/llm_prompts/default/triple.txt",
    "preference": "data/llm_prompts/default/preference.txt",
}


def is_number(value: str) -> bool:
    """Returns True if a value is a number, False otherwise.

    Args:
        value: The value to be checked.

    Returns:
        True if the value is a number, False otherwise.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


class ThreeStepStatementAnnotator(StatementAnnotator):
    def __init__(self) -> None:
        """Initializes the three-step statement annotator."""
        self._prompt_paths = _DEFAULT_PROMPT_PATHS
        self._prompt = Prompt()
        self._valid_intents = {intent.name for intent in Intent}
        self._llm_connector = LLMConnector()

    def get_annotations(self, statement: str) -> Tuple[Intent, PKGData]:
        """Returns a tuple with annotations for a statement.

        Args:
            statement: The statement to be annotated.

        Returns:
            The intent and the annotations.
        """
        intent = self._get_intent(statement)
        triple = self._get_triple(statement)
        preference = (
            self._get_preference(statement, triple.object)
            if triple is not None and triple.object is not None
            else None
        )
        return intent, PKGData(statement, triple, preference)

    def _get_intent(self, statement: str) -> Intent:
        """Returns the intent for a statement.

        Args:
            statement: The statement to be annotated.

        Returns:
            The intent.
        """
        prompt = self._prompt.get_prompt(
            self._prompt_paths["intent"], statement=statement
        )
        response = self._llm_connector.get_response(prompt)
        response_terms = response.split()
        if len(self._valid_intents.intersection(response_terms)) == 1:
            return next(
                intent for intent in Intent if intent.name in response_terms
            )
        return Intent.UNKNOWN

    def _get_triple(self, statement: str) -> Optional[Triple]:
        """Returns the triple for a statement.

        Args:
            statement: The statement to be annotated.

        Returns:
            The triple comprised of subject, predicate, and object or None.
        """
        prompt = self._prompt.get_prompt(
            self._prompt_paths["triple"], statement=statement
        )
        response = self._llm_connector.get_response(prompt)
        response_terms = [
            None if term.strip() == "N/A" else term.strip()
            for term in response.split("|")
        ]
        if len(response_terms) == 3:
            subject, predicate, object = response_terms
            return Triple(
                TripleElement(subject) if subject else None,
                TripleElement(predicate) if predicate else None,
                TripleElement(object) if object else None,
            )
        return None

    def _get_preference(
        self, statement: str, triple_object: TripleElement
    ) -> Optional[Preference]:
        """Returns the preference for a statement.

        Args:
            statement: The statement to be annotated.
            triple_object: The object of the triple.

        Returns:
            The preference.
        """
        prompt = self._prompt.get_prompt(
            self._prompt_paths["preference"],
            statement=statement,
            object=triple_object.reference,
        )
        response = self._llm_connector.get_response(prompt)
        response_terms = [
            term.strip() for term in re.split(r"[ .,;]+", response)
        ]
        preference = next(
            (term for term in response_terms if is_number(term)),
            None,
        )
        if preference:
            return Preference(triple_object, float(preference))
        return None

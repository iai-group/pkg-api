"""A three-step annotator for annotating a statement with a triple and a
preference using LLM."""


import re
from abc import ABC
from typing import Optional, Tuple

from pkg_api.core.annotations import (
    PKGData,
    PreferenceAnnotation,
    TripleAnnotation,
)
from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.annotators.llm_connector import LLMConnector
from pkg_api.nl_to_pkg.annotators.prompt import Prompt

_DEFAULT_PROMPT_PATHS = {
    "intent": "data/llm_prompts/default/intent.txt",
    "triple": "data/llm_prompts/default/triple.txt",
    "preference": "data/llm_prompts/default/preference.txt",
}


class ThreeStepStatementAnnotator(ABC):
    """Annotator for annotating a statement with a triple and a preference
    using LLM."""

    def __init__(self) -> None:
        """Initializes the ThreeStepStatementAnnotator class."""
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
            if triple and triple.object
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

    def _get_triple(self, statement: str) -> Optional[TripleAnnotation]:
        """Returns the triple for a statement.

        Args:
            statement: The statement to be annotated.

        Returns:
            The triple.
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
            return TripleAnnotation(*response_terms)
        return None

    def _get_preference(
        self, statement: str, triple_object: str
    ) -> Optional[PreferenceAnnotation]:
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
            object=triple_object,
        )
        response = self._llm_connector.get_response(prompt)
        response_terms = [
            term.strip() for term in re.split(r"[.,\-; ]+", response)
        ]
        preference = next(
            (term for term in response_terms if term.isnumeric()),
            None,
        )
        if preference:
            return PreferenceAnnotation(triple_object, float(preference))
        return None


if __name__ == "__main__":
    annotator = ThreeStepStatementAnnotator()
    print(annotator.get_annotations("I like apples."))
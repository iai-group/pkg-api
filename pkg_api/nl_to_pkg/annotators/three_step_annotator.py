"""A three-step annotator for annotating a statement with a triple and a
preference using LLM.
"""


from abc import ABC
from typing import Optional, Tuple

from pkg_api.core.annotations import (
    PKGData,
    PreferenceAnnotation,
    TripleAnnotation,
)
from pkg_api.core.intents import Intent
from pkg_api.nl_to_pkg.annotators.prompt import Prompt, PromptPurpose


class ThreeStepStatementAnnotator(ABC):
    """Annotator for annotating a statement with a triple and a preference
    using LLM.
    """

    def __init__(self) -> None:
        """Initializes the ThreeStepStatementAnnotator class."""
        self._prompt = Prompt()
        self._valid_intents = {intent.name for intent in Intent}

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
        response = self._get_llm_response(statement, PromptPurpose.INTENT)
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
        response = self._get_llm_response(statement, PromptPurpose.TRIPLE)
        response_terms = response.split(",")
        if len(response_terms) == 3:
            return TripleAnnotation(*response_terms)
        return None

    def _get_preference(
        self, statement: str, object: str
    ) -> Optional[PreferenceAnnotation]:
        """Returns the preference for a statement.

        Args:
            statement: The statement to be annotated.
            object: The object of the triple.

        Returns:
            The preference.
        """
        response = self._get_llm_response(statement, PromptPurpose.PREFERENCE)
        preference = response[:2].strip()
        if preference.isnumeric():
            return PreferenceAnnotation(object, float(preference))
        return None

    def _get_llm_response(self, statement: str, purpose: PromptPurpose) -> str:
        """Returns the LLM response for a statement.

        Args:
            statement: The statement to be annotated.
            purpose: The purpose of the prompt.

        Returns:
            The LLM response.
        """
        prompt = self._prompt.get_prompt(statement, purpose=purpose)
        # TODO: Implement
        return prompt

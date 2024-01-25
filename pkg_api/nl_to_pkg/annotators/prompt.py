"""Module for loading and processing llm prompts."""

import os
from enum import Enum, auto
from typing import Dict

_DEFAULT_PROMPT_FOLDER = "data/llm_prompts/default"


def load_prompt(path: str) -> str:
    """Loads an LLM prompt from a file.

    Args:
        path: Path to the file containing the prompt.

    Returns:
        The prompt as a string.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File {path} not found.")

    with open(path, "r") as f:
        return f.read()


class PromptPurpose(Enum):
    INTENT = auto()
    TRIPLE = auto()
    PREFERENCE = auto()
    JOINT = auto()


class Prompt:
    """Class for loading and processing a prompt."""

    def __init__(self, folder_path: str = _DEFAULT_PROMPT_FOLDER) -> None:
        """Initializes the Prompt class.

        Args:
            folder_path: Path to the folder containing the prompt files.
        """
        self._folder_path = folder_path
        self._prompts: Dict[str, str] = {}

    def get_prompt(
        self, statement: str, purpose: PromptPurpose = PromptPurpose.JOINT
    ) -> str:
        """Returns the prompt.

        Args:
            statement: The statement to be annotated.
            purpose: The purpose of the prompt.

        Returns:
            The prompt.
        """
        purpose_name = purpose.name.lower()
        prompt = self._prompts.get(purpose_name)
        if not prompt:
            prompt = load_prompt(
                os.path.join(self._folder_path, f"{purpose_name}.txt")
            )
            self._prompts[purpose_name] = prompt
        return prompt.format(statement=statement)

"""Module for loading and processing llm prompts."""

import os
from typing import Dict


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


class Prompt:
    """Class for loading and processing a prompt."""

    def __init__(self) -> None:
        """Initializes the Prompt class.

        Args:
            folder_path: Path to the folder containing the prompt files.
        """
        self._prompts: Dict[str, str] = {}

    def get_prompt(self, path: str, **kwargs) -> str:
        """Returns the prompt.

        Args:
            statement: The statement to be annotated.
            purpose: The purpose of the prompt.

        Returns:
            The prompt.
        """
        if path not in self._prompts:
            self._prompts[path] = load_prompt(path)

        return self._prompts[path].format(**kwargs)

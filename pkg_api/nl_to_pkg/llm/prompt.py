"""Module for loading and processing LLM prompts."""

import os
from typing import Dict


def load_prompt(path: str) -> str:
    """Loads an LLM prompt from a file.

    Args:
        path: Path to the file containing the prompt.

    Raises:
        FileNotFoundError: If the file is not found.

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
        """Initializes the Prompt class."""
        self._prompts: Dict[str, str] = {}

    def get_prompt(self, path: str, **kwargs) -> str:
        """Returns the prompt.

        Args:
            path: Path to the file containing the prompt.
            kwargs: Keyword arguments to be used for formatting the prompt.

        Returns:
            The formatted prompt.
        """
        if path not in self._prompts:
            self._prompts[path] = load_prompt(path)

        return self._prompts[path].format(**kwargs)

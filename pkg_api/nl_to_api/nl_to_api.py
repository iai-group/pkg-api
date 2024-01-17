"""Class for converting natural language to API calls.
Example:

    >>> query = "I like cats"
    >>> from pkg_api.nl_to_api import NLtoAPI
    >>> nl_to_api = NLtoAPI("path/to/prompt.txt")
    >>> method_call = nl_to_api.get_method_call(query)
    >>> method_call
    (<function pkg_api.pkg.pkg.set_owner_preference()>, (cats, 1))
"""

from typing import Callable, Optional, Tuple

MethodCallWithParameters = Tuple[Callable, Tuple]


def load_prompt(path: str) -> str:
    """Loads a prompt from a file.

    Args:
        path: Path to the file containing the prompt.

    Returns:
        The prompt as a string.
    """
    # TODO: Implement
    return ""


class NLtoAPI:
    def __init__(self, path: str) -> None:
        """Initializes the NLtoAPI class.

        Args:
            path: Path to the file containing the prompt.
        """
        self._prompt = load_prompt(path)

    def get_method_call(
        self, query: str
    ) -> Optional[MethodCallWithParameters]:
        """Gets a method call.

        Args:
            query: The query as a string.

        Returns:
            The method call as a string.
        """
        metod_as_string = self._llm_to_api_as_string(query)
        method_with_parameters = self._convert_str_to_method_call(
            metod_as_string
        )
        return method_with_parameters

    def _llm_to_api_as_string(self, prompt: str) -> str:
        """Converts a natural language prompt to an API prompt.

        Args:
            prompt: The prompt as a string.

        Returns:
            The API prompt as a string.
        """
        # TODO: Implement
        return ""

    def _convert_str_to_method_call(
        self, string: str
    ) -> Optional[MethodCallWithParameters]:
        """Converts a string to a method call.

        Args:
            string: The string to convert.

        Returns:
            A tuple containing the method and its parameters.
        """
        # TODO: Implement
        return None

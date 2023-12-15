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
    def __init__(self, path: str):
        """Initializes the NLtoAPI class.

        Args:
            path: Path to the file containing the prompt.
        """
        self._prompt = load_prompt(path)

    def get_method_call(self, query: str) -> Optional[MethodCallWithParameters]:
        """Gets a method call.

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
            The prompt as a string.
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
            The method call as a string.
        """
        # TODO: Implement
        return None

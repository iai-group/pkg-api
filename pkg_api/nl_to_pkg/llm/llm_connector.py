"""Module for querying LLM."""

from typing import Any, Dict

from ollama import Client, Options

_DEFAULT_ENDPOINT = "http://badne4.ux.uis.no:11434"


class LLMConnector:
    def __init__(self, model: str = "llama2") -> None:
        """Initializes the LLMConnector class.

        Args:
            model: The LLM to use, defaults to "llama2".
        """
        self._model = model
        self._client = Client(host=_DEFAULT_ENDPOINT)

    def get_response(self, prompt: str) -> str:
        """Returns the response from LLM.

        Args:
            prompt: The prompt to be sent to LLM.

        Returns:
            The response from LLM.
        """
        return self._client.generate(
            self._model,
            prompt,
            options=self._get_llm_config(),
            stream=False,
        )

    def _get_headers(self) -> Dict[str, str]:
        """Returns the headers for the request."""
        return {"Content-Type": "application/json"}

    def _get_llm_config(self) -> Dict[str, Any]:
        """Returns the config for the request."""
        return Options(
            temperature=0.0,
            top_p=0.9,
            stop=["\n"],
        )

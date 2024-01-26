"""Module for querying LLM."""

import json
from typing import Any, Dict

import requests

_DEFAULT_ENDPOINT = "http://gustav1.ux.uis.no:8888/completion"


class LLMConnector:
    def __init__(self, endpoint: str = _DEFAULT_ENDPOINT) -> None:
        """Initializes the LLMConnector class.

        Args:
            endpoint: The endpoint for LLM. Defaults to _DEFAULT_ENDPOINT.
        """
        self._endpoint = endpoint

    def get_response(self, prompt: str) -> str:
        """Returns the response from LLM.

        Args:
            prompt: The prompt to be sent to LLM.

        Returns:
            The response from LLM.
        """
        response = requests.post(
            self._endpoint,
            headers=self._get_headers(),
            json={**self._get_llm_config(), "prompt": prompt},
        )
        return json.loads(response.text)["content"]

    def _get_headers(self) -> Dict[str, str]:
        """Returns the headers for the request."""
        return {"Content-Type": "application/json"}

    def _get_llm_config(self) -> Dict[str, Any]:
        """Returns the config for the request."""
        return {
            "max_tokens": 64,
            "temperature": 0.0,
            "top_p": 0.9,
            "n": 1,
            "stream": False,
            "logprobs": 10,
            "stop": ["\n"],
        }

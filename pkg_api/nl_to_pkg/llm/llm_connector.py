"""Module for querying LLM."""
import yaml

from typing import Any, Dict

from ollama import Client, Options
import os

_DEFAULT_ENDPOINT = "http://badne4.ux.uis.no:11434"


class LLMConnector:
    def __init__(
        self, config_path: str = "pkg_api/nl_to_pkg/llm/llm_config_llama2.yaml"
    ) -> None:
        """Initializes the LLMConnector class.

        Args:
            config_path: Path to the config file.
        """
        self._config = self._load_config(config_path)
        self._model = self._config.get("model", "llama2")
        self._stream = self._config.get("stream", True)
        self._llm_options = self._get_llm_config()
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

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads the config from the given path.

        Args:
            config_path: Path to the config file.

        Raises:
            FileNotFoundError: If the file is not found.

        Returns:
            A dictionary containing the config keys and values.
        """
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"File {config_path} not found.")
        with open(config_path, "r") as file:
            yaml_data = yaml.safe_load(file)
        return yaml_data

    def _get_llm_config(self) -> Dict[str, Any]:
        """Returns the config for the request."""
        return Options(self._config.get("options", {}))

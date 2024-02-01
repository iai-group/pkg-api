"""Module for querying LLM."""
import os
from typing import Any, Dict

import yaml
from ollama import Client, Options

_DEFAULT_CONFIG_PATH = "pkg_api/nl_to_pkg/llm/configs/llm_config_llama2.yaml"


class LLMConnector:
    def __init__(
        self,
        config_path: str = _DEFAULT_CONFIG_PATH,
    ) -> None:
        """Initializes the LLMConnector class.

        Args:
            config_path: Path to the config file.

        Raises:
            ValueError: If no model is specified in the config.
            ValueError: If no host is specified in the config.
            FileNotFoundError: If the config file is not found.
        """
        self._config_path = config_path
        self._config = self._load_config()
        if "model" not in self._config:
            raise ValueError(
                "No model specified in the config, e.g., 'llama2'."
            )
        if "host" not in self._config:
            raise ValueError("No host specified in the config.")
        self._client = Client(host=self._config.get("host"))
        self._model = self._config.get("model")
        self._stream = self._config.get("stream", False)
        self._llm_options = self._get_llm_config()

    def _generate(self, prompt: str) -> Dict[str, Any]:
        """Generates a response from LLM.

        Args:
            prompt: The prompt to be sent to LLM.

        Returns:
            The dict with response and metadata from LLM.
        """
        return self._client.generate(
            self._model, prompt, options=self._llm_options, stream=self._stream
        )

    def get_response(self, prompt: str) -> str:
        """Returns the response from LLM.

        Args:
            prompt: The prompt to be sent to LLM.

        Returns:
            The response from LLM, if it was successful.
        """
        # Ignoring type because the type hint by ollama is wrong.
        return self._generate(prompt).get("response", "")  # type: ignore

    def _load_config(self) -> Dict[str, Any]:
        """Loads the config from the given path.

        Raises:
            FileNotFoundError: If the file is not found.

        Returns:
            A dictionary containing the config keys and values.
        """
        if not os.path.isfile(self._config_path):
            raise FileNotFoundError(f"File {self._config_path} not found.")
        with open(self._config_path, "r") as file:
            yaml_data = yaml.safe_load(file)
        return yaml_data

    def _get_llm_config(self) -> Dict[str, Any]:
        """Returns the config for the request."""
        return Options(self._config.get("options", {}))

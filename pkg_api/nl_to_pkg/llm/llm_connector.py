"""Module for querying LLM."""
import yaml

from typing import Any, Dict

from ollama import Client, Options
import os

_DEFAULT_ENDPOINT = "http://badne4.ux.uis.no:11434"
_DEFAULT_CONFIG_PATH = "pkg_api/nl_to_pkg/llm/configs/llm_config_llama2.yaml"


class LLMConnector:
    def __init__(
        self,
        config_path: str = _DEFAULT_CONFIG_PATH,
    ) -> None:
        """Initializes the LLMConnector class.

        Args:
            config_path: Path to the config file.
        """
        self._config = self._load_config(config_path)
        self._model = self._config.get("model", "llama2")
        self._stream = self._config.get("stream", True)
        self._client = Client(host=self._config.get("host", _DEFAULT_ENDPOINT))
        self._llm_options = self._get_llm_config()

    def _generate(self, prompt: str) -> str:
        """Generates a response from LLM.

        Args:
            prompt: The prompt to be sent to LLM.

        Returns:
            The response with metadata from LLM.
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
        return self._generate(prompt).get("response", "")  # type: ignore

    @staticmethod
    def _load_config(config_path: str) -> Dict[str, Any]:
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

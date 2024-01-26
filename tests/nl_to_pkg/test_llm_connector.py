"""Tests for LLM connector."""

import pytest

from pkg_api.nl_to_pkg.llm.llm_connector import LLMConnector
from unittest.mock import mock_open


@pytest.fixture
def llm_connector_default() -> LLMConnector:
    """Returns an LLMConnector instance."""
    return LLMConnector()


@pytest.fixture
def llm_connector_llama2() -> LLMConnector:
    """Returns an LLMConnector instance."""
    return LLMConnector("pkg_api/nl_to_pkg/llm/configs/llm_config_llama2.yaml")


@pytest.fixture
def llm_connector_mistral() -> LLMConnector:
    """Returns an LLMConnector instance."""
    return LLMConnector("pkg_api/nl_to_pkg/llm/configs/llm_config_mistral.yaml")


def test_get_response_request_params_default(
    llm_connector_default: LLMConnector,
) -> None:
    """Tests that get_response sends the correct request to LLM."""
    response = llm_connector_default._generate("Test prompt")
    assert response
    assert response["model"] == "llama2"
    assert response["response"] == llm_connector_default.get_response(
        "Test prompt"
    )
    assert response


def test_get_response_request_params_llama(
    llm_connector_llama2: LLMConnector,
) -> None:
    """Tests that get_response sends the correct request to LLM."""
    response = llm_connector_llama2._generate("Test prompt")
    assert response["model"] == "llama2"
    assert response["response"] == llm_connector_llama2.get_response(
        "Test prompt"
    )
    assert response


def test_get_response_request_params_mistral(
    llm_connector_mistral: LLMConnector,
) -> None:
    """Tests that get_response sends the correct request to LLM."""
    response = llm_connector_mistral._generate("Test prompt")
    assert response["model"] == "mistral"
    assert response["response"] == llm_connector_mistral.get_response(
        "Test prompt"
    )
    assert response


def test_load_config_success(mocker):
    """Tests that _load_config returns the correct config.

    Args:
        mocker: Mocking object.
    """
    mocker.patch("builtins.open", mock_open(read_data="key: value"))
    mocker.patch("os.path.isfile", return_value=True)
    result = LLMConnector._load_config("fake_path")
    assert result == {"key": "value"}


def test_load_config_file_not_found(mocker):
    """Tests that _load_config raises FileNotFoundError.

    Args:
        mocker: Mocking object.
    """
    mocker.patch("os.path.isfile", return_value=False)
    with pytest.raises(FileNotFoundError):
        LLMConnector._load_config("fake_path")


def test_load_config_content(mocker):
    """Tests that _load_config returns the valid data.

    Args:
        mocker: Mocking object.
    """
    mocker.patch(
        "builtins.open", mock_open(read_data="key1: value1\nkey2: value2")
    )
    mocker.patch("os.path.isfile", return_value=True)
    result = LLMConnector._load_config("fake_path")
    assert result == {"key1": "value1", "key2": "value2"}

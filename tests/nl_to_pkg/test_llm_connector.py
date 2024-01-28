"""Tests for LLM connector."""

from unittest.mock import mock_open

import pytest
from pytest_mock import MockerFixture

from pkg_api.nl_to_pkg.llm.llm_connector import LLMConnector


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
    """Tests that get_response sends the correct request to LLM.

    Args:
        llm_connector_default: LLMConnector instance.
    """
    response = llm_connector_default._generate("Test prompt")
    assert response
    assert response["model"] == "llama2"
    assert response["response"] == llm_connector_default.get_response(
        "Test prompt"
    )


def test_get_response_request_params_llama(
    llm_connector_llama2: LLMConnector,
) -> None:
    """Tests that get_response sends the correct request to LLM.

    Args:
        llm_connector_llama2: LLMConnector instance with Llama2 instance.
    """
    response = llm_connector_llama2._generate("Test prompt")
    assert response["model"] == "llama2"
    assert response["response"] == llm_connector_llama2.get_response(
        "Test prompt"
    )
    assert response


def test_get_response_request_params_mistral(
    llm_connector_mistral: LLMConnector,
) -> None:
    """Tests that get_response sends the correct request to LLM.

    Args:
        llm_connector_mistral: LLMConnector instance for Mistral model config.
    """
    response = llm_connector_mistral._generate("Test prompt")
    assert response["model"] == "mistral"
    assert response["response"] == llm_connector_mistral.get_response(
        "Test prompt"
    )
    assert response


def test_load_config_file_not_found(mocker: MockerFixture) -> None:
    """Tests that _load_config raises FileNotFoundError.

    Args:
        mocker: Mocking object.
    """
    mocker.patch("os.path.isfile", return_value=False)
    with pytest.raises(FileNotFoundError):
        LLMConnector("fake_path")._load_config()


def test_load_config_content(mocker: MockerFixture) -> None:
    """Tests that _load_config returns the valid data.

    Args:
        mocker: Mocking object.
    """
    mocker.patch(
        "builtins.open", mock_open(read_data="model: value1\nhost: value2")
    )
    mocker.patch("os.path.isfile", return_value=True)
    result = LLMConnector(config_path="fake_path")._load_config()
    assert result == {"model": "value1", "host": "value2"}

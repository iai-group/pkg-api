"""Tests for LLM connector."""

from unittest.mock import MagicMock, mock_open

import pytest
from pytest_mock import MockerFixture

from pkg_api.nl_to_pkg.llm.llm_connector import LLMConnector


def test_generate_method() -> None:
    """Tests that the generate method is called with the correct arguments."""
    # Arrange
    mock_response = {"response": "test response", "other_data": "some value"}
    connector = LLMConnector()
    connector._client.generate = MagicMock(return_value=mock_response)

    # Act
    response = connector.get_response("test prompt")

    # Assert
    assert response == "test response"
    connector._client.generate.assert_called_once_with(
        connector._model,
        "test prompt",
        options=connector._llm_options,
        stream=connector._stream,
    )


def test_get_response_method() -> None:
    """Tests that the get_response method returns the correct response."""
    mock_response = {"response": "mocked response"}
    connector = LLMConnector()
    connector._generate = MagicMock(return_value=mock_response)

    response = connector.get_response("test prompt")

    assert response == "mocked response"
    connector._generate.assert_called_once_with("test prompt")


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

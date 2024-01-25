"""Tests for LLM connetor."""

import json
from unittest.mock import Mock, patch

import pytest

from pkg_api.nl_to_pkg.llm.llm_connector import LLMConnector


@pytest.fixture
def llm_connector() -> LLMConnector:
    """Returns an LLMConnector instance."""
    return LLMConnector()


@patch("requests.post")
def test_get_response_success(
    mock_post: Mock, llm_connector: LLMConnector
) -> None:
    """Tests that get_response returns the response from LLM."""
    mock_response = Mock()
    mock_response.text = json.dumps({"content": "Test LLM response"})
    mock_post.return_value = mock_response

    response = llm_connector.get_response("Test prompt")

    assert response == "Test LLM response"
    mock_post.assert_called_once()


@patch("requests.post")
def test_get_response_request_params(
    mock_post: Mock, llm_connector: LLMConnector
) -> None:
    """Tests that get_response sends the correct request to LLM."""
    mock_response = Mock()
    mock_response.text = json.dumps({"content": "Test LLM response"})
    mock_post.return_value = mock_response

    llm_connector.get_response("Test prompt")

    mock_post.assert_called_once_with(
        "http://gustav1.ux.uis.no:8888/completion",
        headers={"Content-Type": "application/json"},
        json={
            "max_tokens": 64,
            "temperature": 0.0,
            "top_p": 0.9,
            "n": 1,
            "stream": False,
            "logprobs": 10,
            "stop": ["\n"],
            "prompt": "Test prompt",
        },
    )

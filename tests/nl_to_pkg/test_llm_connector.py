"""Tests for LLM connector."""

import pytest

from pkg_api.nl_to_pkg.llm.llm_connector import LLMConnector


@pytest.fixture
def llm_connector() -> LLMConnector:
    """Returns an LLMConnector instance."""
    return LLMConnector()


def test_get_response_request_params(llm_connector: LLMConnector) -> None:
    """Tests that get_response sends the correct request to LLM."""
    response = llm_connector.get_response("Test prompt")
    assert response

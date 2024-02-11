"""Tests for prompts."""

from unittest.mock import Mock, patch

import pytest
from pytest_mock import MockerFixture

from pkg_api.nl_to_pkg.llm.prompt import Prompt, load_prompt


def test_load_prompt_success(mocker: MockerFixture) -> None:
    """Tests that load_prompt loads the prompt file correctly."""
    path = "dummy/path/to/prompt.txt"
    mock_content = "Test prompt content"

    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_content))

    content = load_prompt(path)
    assert content == mock_content


def test_load_prompt_file_not_found() -> None:
    """Tests that load_prompt raises FileNotFoundError if file is not found."""
    with pytest.raises(FileNotFoundError):
        load_prompt("nonexistent/path/to/prompt.txt")


@patch("pkg_api.nl_to_pkg.llm.prompt.load_prompt")
def test_get_prompt_caching(mock_load_prompt: Mock) -> None:
    """Tests that get_prompt caches the prompt."""
    mock_load_prompt.return_value = "Loaded prompt"
    prompt_processor = Prompt()

    # First call should load the prompt
    result1 = prompt_processor.get_prompt("path/to/prompt.txt")
    assert result1 == "Loaded prompt"
    mock_load_prompt.assert_called_once_with("path/to/prompt.txt")

    # Second call should use the cached version, not load again
    result2 = prompt_processor.get_prompt("path/to/prompt.txt")
    assert result2 == "Loaded prompt"
    mock_load_prompt.assert_called_once()


@patch(
    "pkg_api.nl_to_pkg.llm.prompt.load_prompt", return_value="Hello, {name}!"
)
def test_get_prompt_formatting(mock_load_prompt: Mock) -> None:
    """Tests that get_prompt formats the prompt correctly."""
    prompt_processor = Prompt()
    formatted_prompt = prompt_processor.get_prompt(
        "path/to/prompt.txt", name="World"
    )
    assert formatted_prompt == "Hello, World!"

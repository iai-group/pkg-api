"""Tests eval_nl_to_pkg.py file."""
from typing import List, Dict, Tuple
from unittest.mock import patch, MagicMock
from pkg_api.nl_to_pkg.eval_nl_to_pkg import eval_annotations, load_data
from pkg_api.nl_to_pkg.annotators.three_step_annotator import (
    ThreeStepStatementAnnotator,
)
from pkg_api.core.annotations import PKGData, Triple
from pkg_api.core.intents import Intent
import pytest


def test_load_data() -> None:
    """Tests load_data function.

    Args:
        mock_csv_data: Expected data from the mock csv file.
    """
    result = load_data("tests/nl_to_pkg/data/nl_to_pkg_mock_file.csv")
    assert len(result) == 3
    assert all(len(row) == 6 for row in result)
    assert result[0] == ["Sentence1.", "ADD", "S1", "P1", "O1", ""]


@pytest.fixture
def mock_data():
    """Fixture for mock the NL annotation data."""
    return [["Sentence1.", "ADD", "S1", "P1", "O1", ""]]


@pytest.fixture
def mock_prompt_paths():
    """Fixture for mock the prompt paths."""
    return {
        "intent": "some_value",
        "triple": "tiple_value",
        "preference": "preference_value",
    }


@pytest.fixture
def mock_config_path():
    """Fixture for mock the config path."""
    return "path/to/config"


@pytest.fixture
def mock_annotations():
    """Fixture for mock the NL annotations returned by the LLM."""
    mock_pkg_data1 = PKGData(
        statement="Sentence1.",
        triple=Triple(subject="S1", predicate="P1", object="O1"),
        preference=None,
    )
    return (Intent.ADD, mock_pkg_data1)


@patch("pkg_api.nl_to_pkg.annotators.three_step_annotator.LLMConnector")
@patch.object(ThreeStepStatementAnnotator, "get_annotations")
@patch(
    "pkg_api.nl_to_pkg.annotators.three_step_annotator.ThreeStepStatementAnnotator"  # noqa E501
)
def test_eval_annotations(
    MockAnnotator: MagicMock,
    mock_get_annotations: MagicMock,
    MockLLMConnector: MagicMock,
    mock_annotations: List[Tuple[Intent, PKGData]],
    mock_data: List[List[str]],
    mock_prompt_paths: Dict[str, str],
    mock_config_path: str,
) -> None:
    """Tests the eval_annotations function.

    Args:
        MockAnnotator: A mock of the ThreeStepStatementAnnotator class.
        mock_get_annotations: A mock of the get_annotations method.
        MockLLMConnector: A mock of the LLMConnector class.
        mock_annotations: A list of mock annotations.
        mock_data: A list of mock data.
        mock_prompt_paths: A dictionary of mock prompt paths.
        mock_config_path: A mock config path.
    """
    mock_get_annotations.return_value = mock_annotations
    result = eval_annotations(mock_data, mock_prompt_paths, mock_config_path)
    mock_get_annotations.assert_called_once_with("Sentence1.")
    assert result == {
        "Intent F1 (macro)": 1.0,
        "Intent F1 (micro)": 1.0,
        "Preference F1 (macro)": 1.0,
        "Preference F1 (micro)": 1.0,
        "Avg. Triple Correct": 3.0,
    }

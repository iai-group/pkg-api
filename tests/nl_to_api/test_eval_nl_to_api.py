"""Test eval_nl_to_api.py file."""
import pytest

from pkg_api.nl_annotations.eval_nl_to_kg import load_data


@pytest.fixture
def mock_csv_data():
    """Fixture for the mock csv data."""
    return [
        ["Sentence 1", "API1()"],
        ["Sentence 2", "API2()"],
        ["Sentence 3", "API3()"],
    ]


def test_load_data(mock_csv_data):
    """Test load_data function.

    Args:
        mock_csv_data: Expected data from the mock csv file.
    """
    result = load_data("tests/nl_to_api/data/nl_to_api_mock_file.csv")
    assert result == mock_csv_data

"""Test eval_nl_to_pkg.py file."""

from pkg_api.nl_to_pkg.eval_nl_to_pkg import load_data


def test_load_data():
    """Test load_data function.

    Args:
        mock_csv_data: Expected data from the mock csv file.
    """
    result = load_data("tests/nl_to_pkg/data/nl_to_pkg_mock_file.csv")
    assert len(result) == 3
    assert all(len(row) == 6 for row in result)
    assert result[0] == ["Sentence1.", "ADD", "S1", "P1", "O1", ""]

"""Test eval_nl_to_api.py file."""

from pkg_api.nl_annotations.eval_nl_to_kg import load_data


def test_load_data():
    """Test load_data function.

    Args:
        mock_csv_data: Expected data from the mock csv file.
    """
    result = load_data("tests/nl_annotations/data/nl_to_kg_mock_file.csv")
    assert len(result) == 3
    assert all(len(row) == 6 for row in result)
    assert result[0][0] == "Sentence1."
    assert result[0][1] == "ADD"
    assert result[0][2] == "S1"
    assert result[0][3] == "P1"
    assert result[0][4] == "O1"
    assert result[0][5] == ""

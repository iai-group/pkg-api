"""This script is used to evaluate the NL to API model."""
import csv


def load_data(path: str) -> list:
    """Loads a csv data file containing NL to API test.

    Args:
        path: Path to the file containing the data.

    Returns:
        The prompt as a string.
    """
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        data = list(reader)
    return data

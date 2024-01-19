"""Evaluates the NL to API model."""
import csv


def load_data(path: str) -> list:
    """Loads a csv data file containing NL to API test.

    Args:
        path: Path to the file containing the data.

    Returns:
        The prompt as a string.
    """
    with open(path, "r") as f:
        reader = csv.reader(f, skipinitialspace=True, delimiter=",")
        next(reader)  # Skip the header row
        data = list(reader)
    return data

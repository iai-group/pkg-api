"""Evaluates the NL to PKG models."""
import csv


def load_data(path: str) -> list:
    """Loads a csv data file containing NL to PKG test.

    Args:
        path: Path to the file containing the data.

    Returns:
        List of NL to PKG annotation data.
    """
    with open(path, "r") as f:
        reader = csv.reader(f, skipinitialspace=True, delimiter=",")
        next(reader)  # Skip the header row
        data = list(reader)
    return data

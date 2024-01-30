import os
from typing import Any, Dict

import yaml


def load_yaml_config(path: str) -> Dict[str, Any]:
    """
    Loads configuration from a YAML file at the given path.

    Args:
        path: The file path to the YAML configuration file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the path is not a file.

    Returns:
        A dictionary containing the configuration data.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at {path} does not exist.")

    if not os.path.isfile(path):
        raise ValueError(f"The path {path} is not a file.")

    with open(path, "r") as file:
        config = yaml.safe_load(file)

    return config

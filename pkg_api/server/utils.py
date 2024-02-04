"""Utility functions for the server."""
from typing import Dict

from flask import current_app

from pkg_api.connector import RDFStore
from pkg_api.core.pkg_types import URI
from pkg_api.pkg import PKG


def open_pkg(data: Dict[str, str]) -> PKG:
    """Opens a connection to the PKG.
    Args:
        data: Request data.
    Returns:
        A PKG instance.
    """
    owner_uri = data.get("owner_uri", None)
    owner_username = data.get("owner_username", None)
    if owner_uri is None:
        raise Exception("Missing owner URI")

    store_path = current_app.config["STORE_PATH"]

    return PKG(
        URI(owner_uri),
        RDFStore.MEMORY,
        f"{store_path}/{owner_username}",
    )

"""Utility functions for the server."""
from typing import Dict, Tuple

from pkg_api.connector import DEFAULT_STORE_PATH, RDFStore
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

    return PKG(
        owner_uri,
        RDFStore.MEMORY,
        f"{DEFAULT_STORE_PATH}/{owner_username}",
    )


def parse_pouplation_request_data(data: Dict[str, str]) -> Tuple[str, str, str]:
    """Parses the request data to retrieve query parameters.

    Args:
        data: Request data.

    Returns:
        A tuple containing subject, predicate, entity, and preference.
    """
    subject_uri = data.get("subject_uri", None)
    predicate = data.get("predicate", None)
    entity_uri = data.get("entity_uri", None)
    preference = data.get("preference", None)
    return subject_uri, predicate, entity_uri, preference

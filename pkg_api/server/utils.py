"""Utility functions for the server."""
from typing import Any, Dict, Tuple

from flask import current_app

from pkg_api.connector import RDFStore
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

    store_path = current_app.config["SQLALCHEMY_DATABASE_URI"]

    return PKG(
        owner_uri,
        RDFStore.MEMORY,
        f"{store_path}/{owner_username}",
    )


def parse_population_request_data(
    data: Dict[str, Any]
) -> Tuple[str, str, str, float]:
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


def parse_query_request_data(data: Dict[str, Any]) -> str:
    """Parses the request data to execute SPARQL query.

    Args:
        data: Request data.

    Returns:
        A string containing SPARQL query.
    """
    return data.get("sparql_query", None)

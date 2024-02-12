"""Utility functions for the server."""

import uuid
from datetime import datetime
from typing import Any, Dict, Union

from flask import current_app

from pkg_api.connector import RDFStore
from pkg_api.core.annotation import (
    Concept,
    PKGData,
    Preference,
    Triple,
    TripleElement,
)
from pkg_api.core.pkg_types import URI
from pkg_api.pkg import PKG


def open_pkg(data: Dict[str, str]) -> PKG:
    """Opens a connection to the PKG.

    Args:
        data: Request data.

    Raises:
        Exception: If the owner URI is missing.

    Returns:
        A PKG instance.
    """
    owner_uri = data.get("owner_uri", None)
    owner_username = data.get("owner_username", None)
    if owner_uri is None:
        raise Exception("Missing owner URI")

    store_path = current_app.config["STORE_PATH"]
    visualization_path = current_app.config["VISUALIZATION_PATH"]

    return PKG(
        URI(owner_uri),
        RDFStore.MEMORY,
        f"{store_path}/{owner_username}",
        visualization_path=visualization_path,
    )


def parse_query_request_data(data: Dict[str, Any]) -> str:
    """Parses the request data to execute SPARQL query.

    Args:
        data: Request data.

    Returns:
        A string containing SPARQL query.
    """
    return data.get("sparql_query", None)


def _parse_triple_element(
    element_data: Union[Dict[str, Any], str]
) -> TripleElement:
    """Parses a triple element received from HTTP request.

    Args:
        element_data: Data sent with HTTP request.

    Returns:
        Triple element.
    """
    if element_data is not None:
        value = (
            element_data
            if isinstance(element_data, str)
            else element_data.get("value")
        )
        if isinstance(value, dict):
            return TripleElement(value.get("description"), Concept(**value))
        elif isinstance(value, str):
            try:
                return TripleElement(value, URI(value))
            except Exception:
                return TripleElement(value, None)

    return None


def parse_query_statement_population_data(data: Dict[str, Any]) -> PKGData:
    """Parses the request data to execute SPARQL query.

    Args:
        data: Request data.

    Returns:
        Associated PKGData.
    """
    description = data.get("description", None)
    if description is None:
        raise Exception("Missing description")

    # Parse triple elements
    subject = _parse_triple_element(data.get("subject", None))
    predicate = _parse_triple_element(data.get("predicate", None))
    statement_object = _parse_triple_element(data.get("object", None))

    # Parse preference
    preference = data.get("preference", None)
    if -1.0 <= preference <= 1.0:
        preference = Preference(statement_object, preference)
    else:
        preference = None

    return PKGData(
        id=uuid.uuid1(),
        statement=description,
        triple=Triple(subject, predicate, statement_object),
        preference=preference,
        logging_data={
            "authoredOn": datetime.now().isoformat(),
            "authoredBy": data.get("owner_uri", None),
        },
    )

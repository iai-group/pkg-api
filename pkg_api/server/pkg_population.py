"""Facts Management API Resource."""
import re
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from flask import request
from flask_restful import Resource

from pkg_api.connector import DEFAULT_STORE_PATH, RDFStore
from pkg_api.pkg import PKG

_QUERY_FORMAT_ERROR = ValueError(
    "The query string should be in the following format:"
    " Type: [fact|preference] Subject: [me|owner|URI] Predicate: [URI]"
    " Object: [URI|Literal] Preference: [preference]."
    " Some fields are optional, but the order must be preserved."
)


def process_query(query: str) -> Tuple[str, str, str, str, float]:
    """Processes a query string.

    The query string should be in the following format:
    "Type: [fact|preference] Subject: [me|owner|URI] Predicate: [URI]
    Object: [URI|Literal] Preference: [preference]".
    Some fields are optional, but the order must be preserved. For example,
    when asking for a fact, the fields Object and Preference are not
    required.

    Args:
        query: The query string.

    Returns:
        The type, subject, predicate, and object of the query.
    """
    components = defaultdict(Any)

    pattern = r"(?P<field>\w+):\s*(?P<value>[^ ]+)"
    matches = re.finditer(pattern, query)

    for match in matches:
        field = match.group("field").strip()
        value = match.group("value").strip()
        components[field] = value

    query_type = components.get("Type", None)
    if query_type not in ["fact", "preference"]:
        raise _QUERY_FORMAT_ERROR

    return (
        query_type,
        components.get("Subject", None),
        components.get("Predicate", None),
        components.get("Object", None),
        components.get("Preference", None),
    )


def check_query_fields(fields: List[str]) -> None:
    """Checks if all the fields are filled in the query.

    Args:
        fields: The fields to check.

    Raises:
        ValueError: If any of the fields is None.
    """
    if None in fields:
        raise _QUERY_FORMAT_ERROR


class PKGPopulationResource(Resource):
    def _execute_query(
        self,
        owner_uri: str,
        owner_username: str,
        query: str,
        http_request: str,
    ) -> Tuple[Dict[str, str], int]:
        """Processes and executes a query.

        This method extracts the necessary information from the query and
        execute the appropriate method in the PKG.
        For now, it is a preliminary implementation.

        Args:
            owner_uri: URI of the owner.
            owner_username: Username of the owner.
            query: Query.
            http_request: HTTP request method.

        Returns:
            A message indicating the status of the operation and status code.
        """
        pkg = PKG(
            owner_uri,
            RDFStore.MEMORY,
            f"{DEFAULT_STORE_PATH}/{owner_username}",
        )

        try:
            (
                query_type,
                subject,
                predicate,
                object,
                preference,
            ) = process_query(query)

            if subject in ["me", "owner"]:
                subject = owner_uri

            if query_type == "fact":
                check_query_fields([subject, predicate, object])
                if http_request == "POST":
                    pkg.add_fact(subject, predicate, object)
                elif http_request == "DELETE":
                    pkg.remove_fact(subject, predicate, object)
            elif query_type == "preference" and http_request == "POST":
                check_query_fields([subject, object, preference])
                pkg.set_preference(subject, object, float(preference))
            else:
                raise Exception("Cannot find an appropriate method.")
        except Exception as e:
            return {"message": str(e)}, 500
        finally:
            pkg.close()
        return {"message": "Your PKG was modified."}, 200

    def get(self) -> Tuple[Dict[str, str], int]:
        """Retrieves a fact or a preference from PKG.

        Returns:
            Retrieved fact or preference and status code.
        """
        return {"message": "Not implemented yet."}, 501

    def post(self) -> Tuple[Dict[str, str], int]:
        """Adds a fact or a preference to PKG.

        Returns:
            A message indicating the status of the operation and status code.
        """
        data = request.get_json()
        owner_uri = data.get("owner_uri", None)
        owner_username = data.get("owner_username", None)
        query = data.get("query", None)

        if not owner_uri or not query:
            return {"message": "Invalid request body."}, 400

        return self._execute_query(owner_uri, owner_username, query, "POST")

    def delete(self) -> Tuple[Dict[str, str], int]:
        """Deletes a fact from PKG.

        Returns:
            A message indicating the status of the operation and status code.
        """
        data = request.get_json()
        owner_uri = data.get("owner_uri", None)
        owner_username = data.get("owner_username", None)
        query = data.get("query", None)

        if not owner_uri or not query:
            return {"message": "Invalid request body."}, 400

        return self._execute_query(owner_uri, owner_username, query, "DELETE")

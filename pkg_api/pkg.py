"""PKG API.

A statement is the main piece of information, it may be enriched with properties
such as subject, object, and predicate (for more details refer to the PKG
vocabulary and class PKGData). A statement may also be linked to a preference, 
the representation of a preference is described in the PKG vocabulary.
The PKG vocabulary and an example of a statement can be found here:
https://github.com/iai-group/pkg-vocabulary
"""

from typing import Dict, Optional

from rdflib.term import Variable

import pkg_api.utils as utils
from pkg_api.connector import Connector, RDFStore
from pkg_api.core.pkg_types import URI


class PKG:
    def __init__(self, owner: URI, rdf_store: RDFStore, rdf_path: str) -> None:
        """Initializes PKG of a given user.

        Args:
            owner: Owner URI.
            rdf_store: Type of RDF store.
            rdf_path: Path to the RDF store.
        """
        self._owner_uri = owner
        self._connector = Connector(owner, rdf_store, rdf_path)

    @property
    def owner_uri(self) -> URI:
        """Returns the URI of the owner of this PKG."""
        return self._owner_uri

    def close(self) -> None:
        """Closes the connection to the connector."""
        self._connector.close()

    def get_owner_preference(self, object: URI) -> float:
        """Gets preference for a given object.

        Args:
            object: Object of the preference.

        Returns:
            Preference value.
        """
        return self.get_preference(self._owner_uri, object)

    def get_owner_preferences(self, rdf_class: URI) -> Dict[URI, float]:
        """Gets preferences for a given class.

        Args:
            rdf_class: Class of the preference.

        Returns:
            Dictionary of preferences.
        """
        return self.get_preferences(self._owner_uri, rdf_class)

    def get_preference(self, who: URI, object: URI) -> Optional[float]:
        """Gets the preference for a given object.

        Bindings that are returned after executing a query in RDFLib are
        iterable. By design, we should have up to one binding returned when
        querying for preferences (there is a preference set or not). If more
        than one binding is returned, it means that something went wrong while
        setting the preferences and the exception is raised.

        Args:
            who: Subject of the preference.
            object: Object of the preference.

        Raises:
            Exception: If multiple bindings are returned after executing the
            query.

        Returns:
            Preference value. If no preference is found, returns None.
        """
        query = utils.get_query_for_get_preference(who, object)
        bindings = [
            binding
            for binding in self._connector.execute_sparql_query(query).bindings
        ]
        if len(bindings) > 1:
            raise Exception(
                f"Multiple bindings found for {who} and {object}: "
                f"{bindings}"
            )
        return (
            float(bindings[0].get(Variable("pref")))
            if len(bindings) == 1
            else None
        )

    def get_preferences(self, who: URI, rdf_class: URI) -> Dict[URI, float]:
        """Gets preferences for a given class.

        Args:
            who: Subject of the preference.
            rdf_class: Class of the preference.

        Returns:
            Dictionary of preferences.
        """
        pass

    def add_statement(self, pkg_data: utils.PKGData) -> None:
        """Adds a statement to the PKG.

        Args:
            pkg_data: PKG data associated to a statement.
        """
        query = utils.get_query_for_add_statement(pkg_data)
        self._connector.execute_sparql_query(query)

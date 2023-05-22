"""PKG API.

A fact is an atomic piece of information that can be represented as a triple:
subject, predicate, object. A fact can be about the owner in which case the
subject is the owner's URI or about another entity then the subject is the
entity's URI.
For example:
    - The owner (user1) likes ice cream is represented as follow:
    (http://example.org/user1, http://example.org/likes, http://example.org/icecream)   # noqa
    - Stavanger is in Norway is represented as follow:
    (http://example.org/stavanger, http://example.org/isIn, http://example.org/norway)  # noqa

A preference indicates how much a person (can be the owner or someone else)
likes an entity. In practice, the preference is represented with a blank node
that links the subject, the object and the preference value (a float between -1
and 1).
"""

from typing import List

import pkg_api.utils as utils
from pkg_api.connector import Connector
from pkg_api.types import URI


class PKG:
    def __init__(self, owner: URI) -> None:
        """Initializes PKG of a given user.

        Args:
            owner: Owner URI.
        """
        self._owner_uri = owner
        self._connector = Connector(owner)

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

    def get_owner_preferences(self, rdf_class: URI) -> dict[URI, float]:
        """Gets preferences for a given class.

        Args:
            rdf_class: Class of the preference.

        Returns:
            Dictionary of preferences.
        """
        return self.get_preferences(self._owner_uri, rdf_class)

    def get_preference(self, who: URI, object: URI) -> float:
        """Gets the preference for a given object.

        Args:
            who: Subject of the preference.
            object: Object of the preference.

        Returns:
            Preference value.
        """
        pass

    def get_owner_objects_from_facts(self, predicate: URI) -> List[URI]:
        """Gets objects given subject and predicate.

        Args:
            predicate: Predicate of the fact.

        Returns:
            List of objects.
        """
        return self.get_objects_from_facts(self._owner_uri, predicate)

    def get_preferences(self, who: URI, rdf_class: URI) -> dict[URI, float]:
        """Gets preferences for a given class.

        Args:
            who: Subject of the preference.
            rdf_class: Class of the preference.

        Returns:
            Dictionary of preferences.
        """
        pass

    def get_objects_from_facts(self, subject: URI, predicate: URI) -> List[URI]:
        """Gets objects given subject and predicate.

        Args:
            subject: Subject of the fact.
            predicate: Predicate of the fact.

        Returns:
            List of objects.
        """
        query = utils.get_query_get_objects_from_facts(subject, predicate)
        results = self._connector.execute_sparql_query(query)
        return results

    def set_owner_preference(self, entity: URI, preference: float) -> None:
        """Sets owner preference for a given entity.

        Args:
            entity: Entity.
            preference: Preference value.
        """
        self.set_preference(self._owner_uri, entity, preference)

    def set_preference(self, who: URI, entity: URI, preference: float) -> None:
        """Sets preference for a given entity.

        Args:
            who: Who is setting the preference.
            entity: URI of the entity.
            preference: Preference value.
        """
        # (Optional) Create RDF representation of the preference
        # Create SPARQL query
        # Execute SPARQL query
        pass

    def add_owner_fact(self, predicate: URI, entity: URI) -> None:
        """Adds a fact related to the PKG owner.

        Args:
            predicate: Predicate.
            entity: Entity.
        """
        self.add_fact(self._owner_uri, predicate, entity)

    def add_fact(self, subject: URI, predicate: URI, entity: URI) -> None:
        """Adds a fact.

        Args:
            subject: Subject.
            predicate: Predicate.
            entity: Entity.
        """
        # (Optional) Create RDF representation of the fact
        # Create SPARQL query
        # Execute SPARQL query
        query = utils.get_query_add_fact(subject, predicate, entity)
        self._connector.execute_sparql_update(query)


if __name__ == "__main__":
    pkg = PKG("http://example.org/user1")
    pkg.add_owner_fact(
        "http://example.org/likes", "http://example.org/icecream"
    )
    pkg.add_owner_fact("http://example.org/likes", "http://example.org/pizza")

    for item in pkg.get_owner_objects_from_facts("http://example.org/likes"):
        print(item[0])

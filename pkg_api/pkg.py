"""PKG API."""

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
        query = utils.get_query_get_preference(who, object)
        return pkg._connector.execute_sparql_query(query)

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

    def get_objects_from_facts(self, who: URI, predicate: URI) -> List[URI]:
        """Gets objects given subject and predicate.

        Args:
            who: Subject of the fact.
            predicate: Predicate of the fact.

        Returns:
            List of objects.
        """
        query = utils.get_query_get_objects_from_facts(who, predicate)
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
        entity_preference = None
        for user_preference in self.get_preference(who, entity):
            entity_preference = user_preference[0]
        print("set_pref", entity_preference)
        if entity_preference is None:
            query = utils.get_query_set_preference(who, entity, preference)
        else:
            query = utils.get_query_update_preference(who, entity, entity_preference, preference)

        # query = utils.get_query_set_preference(who, entity, preference)
        return self._connector.execute_sparql_update(query)

    def add_owner_fact(self, predicate: URI, entity: URI) -> None:
        """Adds a fact related to the PKG owner.

        Args:
            predicate: Predicate.
            entity: Entity.
        """
        self.add_fact(self._owner_uri, predicate, entity)

    def add_fact(self, who: URI, predicate: URI, entity: URI) -> None:
        """Adds a fact.

        Args:
            who: Who is adding the fact.
            predicate: Predicate.
            entity: Entity.
        """
        # (Optional) Create RDF representation of the fact
        # Create SPARQL query
        # Execute SPARQL query
        query = utils.get_query_add_fact(who, predicate, entity)
        self._connector.execute_sparql_update(query)


if __name__ == "__main__":
    pkg = PKG("http://example.org/user1")
    pkg.add_owner_fact(
        "http://example.org/likes", "http://example.org/icecream"
    )
    pkg.add_owner_fact("http://example.org/likes", "http://example.org/pizza")

    for item in pkg.get_owner_objects_from_facts("http://example.org/likes"):
        print(item[0])

    pkg.set_owner_preference("http://example.org/tea", 1)
    pkg.set_owner_preference("http://example.org/coffee", -1)

    for item in pkg.get_owner_preference("http://example.org/coffee"):
        print(item[0])

    # Update user preference
    pkg.set_owner_preference("http://example.org/coffee", 0.5)
    for item in pkg.get_owner_preference("http://example.org/coffee"):
        print(item[0])

    for item in pkg.get_owner_preference("http://example.org/tea"):
        print(item[0])

    # pkg.set_owner_preference("http://example.org/coffee", 2)
    # for item in pkg.get_owner_preference("http://example.org/coffee"):
    #     print(item[0])

    # print(list(pkg.get_owner_preference("http://example.org/tea")))
    # print(list(pkg.get_owner_preference("http://example.org/pizza")))

    # query = utils.get_query_update_preference("http://example.org/user1", "http://example.org/coffee", -1, 0.5)
    # pkg._connector.execute_sparql_update(query)

    # query = utils.get_query_set_preference("http://example.org/user1", "http://example.org/sample_entity", 1)
    # pkg._connector.execute_sparql_update(query)

    # query2 = utils.get_query_get_preference("http://example.org/user1", "http://example.org/sample_entity")
    # i = pkg._connector.execute_sparql_query(query2)
    # for i1 in i:
    #     print(i1[0])
    # # print(i)

    # query3 = utils.select("http://example.org/user1", "http://example.org/sample_entity")
    # i = pkg._connector.execute_sparql_query(query3)
    # for i1 in i:
    #     print(i1[0])
    # # print(i)


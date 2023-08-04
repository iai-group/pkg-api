"""PKG API.

A fact is an atomic piece of information that can be represented as a triple:
subject, predicate, object. A fact can be about the owner, in which case the
subject is the owner's URI, or about another entity, then the subject is the
entity's URI.

For example:
    - 'The owner (user1) likes ice cream' is represented as follow:
    (/../user1, /../likes, /../icecream)
    - 'Stavanger is in Norway' is represented as follow:
    (/../stavanger, /../isIn, /../norway)  # noqa

A preference indicates how much a person (can be the owner or someone else)
likes an entity. Representing a preference requires multiple triples; creating
this representation is left to the utils class.
"""

from typing import Dict, List, Optional

from rdflib.term import Variable

import pkg_api.utils as utils
from pkg_api.connector import Connector, RDFStore
from pkg_api.pkg_types import URI


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

    def get_owner_objects_from_facts(self, predicate: URI) -> List[URI]:
        """Gets objects given subject and predicate.

        Args:
            predicate: Predicate of the fact.

        Returns:
            List of objects for the given predicate.
        """
        return self.get_objects_from_facts(self._owner_uri, predicate)

    def get_preferences(self, who: URI, rdf_class: URI) -> Dict[URI, float]:
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
            List of objects for the given predicate.
        """
        query = utils.get_query_for_get_objects_from_facts(subject, predicate)
        return [
            str(binding.get(Variable("object")))
            for binding in self._connector.execute_sparql_query(query).bindings
        ]

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
        old_preference = self.get_preference(who, entity)

        if old_preference is None:
            query = utils.get_query_for_set_preference(who, entity, preference)
        else:
            query = utils.get_query_for_update_preference(
                who, entity, old_preference, preference
            )

        self._connector.execute_sparql_update(query)

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
        query = utils.get_query_for_add_fact(subject, predicate, entity)
        self._connector.execute_sparql_update(query)

    def remove_fact(self, subject: URI, predicate: URI, entity: URI) -> None:
        """Removes a fact.

        Args:
            subject: Subject of the fact being removed.
            predicate: Predicate of the fact being removed.
            entity: Entity to be removed.
        """
        query = utils.get_query_for_remove_fact(subject, predicate, entity)
        self._connector.execute_sparql_update(query)

    def remove_owner_fact(self, predicate: URI, entity: URI) -> None:
        """Removes a fact related to the PKG owner.

        Args:
            predicate: Predicate to be removed.
            entity: Entity to be removed.
        """
        self.remove_fact(self._owner_uri, predicate, entity)


if __name__ == "__main__":
    pkg = PKG("http://example.org/user1", RDFStore.MEMORY, "data/RDFStore")
    pkg.add_owner_fact(
        "http://example.org/likes", "http://example.org/icecream"
    )
    pkg.add_owner_fact("http://example.org/likes", "http://example.org/pizza")

    for item in pkg.get_owner_objects_from_facts("http://example.org/likes"):
        print(item)

    pkg.remove_owner_fact(
        "http://example.org/likes", "http://example.org/pizza"
    )
    for item in pkg.get_owner_objects_from_facts("http://example.org/likes"):
        print(item)

    pkg.set_owner_preference("http://example.org/tea", 1.0)
    pkg.set_owner_preference("http://example.org/coffee", -1.0)

    print(pkg.get_owner_preference("http://example.org/coffee"))

    # Update user preference
    pkg.set_owner_preference("http://example.org/coffee", 0.5)
    print(pkg.get_owner_preference("http://example.org/coffee"))

    print(pkg.get_owner_preference("http://example.org/tea"))

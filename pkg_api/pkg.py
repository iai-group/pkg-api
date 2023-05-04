"""PKG API."""

URI = str


class PKG:
    def __init__(self) -> None:
        self._owner_uri = "owner"

    @property
    def owner_uri(self) -> URI:
        """Returns the URI of the owner of this PKG."""
        return self._owner_uri

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
        pass

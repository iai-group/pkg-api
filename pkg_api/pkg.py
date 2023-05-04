"""PKG API."""

from typing import List

URI = str

class PKG:
    def __init__(self, user: URI) -> None:
        """Initialize PKG for a given user.

        Args:
            user: User URI.
        """
        self.user = user

    def get_preference(self, who: URI, object: URI) -> float:
        """Get preference for a given object.

        Args:
            who: Subject of the preference.
            object: Object of the preference.

        Returns:
            Preference value.
        """
        pass

    def get_preferences(self, who: URI, rdf_class: URI) -> dict[URI, float]:
        """Get preferences for a given class.
        
        Args:
            who: Subject of the preference.
            rdf_class: Class of the preference.

        Returns:
            Dictionary of preferences.
        """
        pass

    def get_objects_from_facts(self, who: URI, predicate: URI) -> List[URI]:
        """Get objects given subject and predicate.

        Args:
            who: Subject of the fact.
            predicate: Predicate of the fact.

        Returns:
            List of objects.
        """
        pass
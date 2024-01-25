"""Abstract class for entity linking."""


from abc import ABC, abstractmethod

from pkg_api.core.annotations import Triple


class EntityLinker(ABC):
    """Entity linker for linking entities to the PKG or available KGs."""

    @abstractmethod
    def link_annotation_entities(
        self, statement: str, triple: Triple
    ) -> Triple:
        """Resolves the annotation if possible.

        Args:
            statement: The statement to be annotated.
            triple: The triple annotation.

        Returns:
            The resolved triple annotation.
        """
        raise NotImplementedError

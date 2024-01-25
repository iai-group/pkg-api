"""Abstract class for entity linking."""


from abc import ABC, abstractmethod

from pkg_api.core.annotations import PKGData


class EntityLinker(ABC):
    """Entity linker for linking entities to the PKG or available KGs."""

    @abstractmethod
    def link_annotation_entities(self, pkg_data: PKGData) -> PKGData:
        """Resolves the pkg data annotations if possible.

        Args:
            pkg_data: The PKG data to be resolved.

        Returns:
            The resolved PKG data annotations.
        """
        raise NotImplementedError

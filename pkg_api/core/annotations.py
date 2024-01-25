"""Dataclasses for the annotations used in the PKG API."""

from dataclasses import dataclass
from typing import Optional, Union

from pkg_api.pkg_types import URI


@dataclass
class Concept:
    """Class representing a SKOS concept."""

    description: str
    related_entities: Optional[URI] = None
    broader_entities: Optional[URI] = None
    narrower_entities: Optional[URI] = None


@dataclass
class Triple:
    """Class representing a subject, predicate, object triple."""

    subject: Union[URI, str, None] = None
    predicate: Union[URI, str, None] = None
    object: Union[URI, Concept, str, None] = None


@dataclass
class Preference:
    """Class representing a preference."""

    topic: Union[URI, Concept, str]
    weight: float


@dataclass
class PKGData:
    """Represents a statement annotated with a triple and a preference."""

    statement: str
    triple: Optional[Triple] = None
    preference: Optional[Preference] = None

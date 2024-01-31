"""Dataclasses for the annotations used in the PKG API."""

from dataclasses import dataclass, field
from typing import List, Optional, Union

from pkg_api.pkg_types import URI


@dataclass
class Concept:
    """Class representing a SKOS concept."""

    description: str
    related_entities: List[URI] = field(default_factory=list)
    broader_entities: List[URI] = field(default_factory=list)
    narrower_entities: List[URI] = field(default_factory=list)


@dataclass
class TripleElement:
    """Class representing a subject, predicate or object element.

    Attributes:
        value: Raw string value of the element.
        reference: URI, Concept or literal reference of the element.
    """

    value: str
    reference: Union[URI, Concept, str, None] = None


@dataclass
class Triple:
    """Class representing a subject, predicate, object triple."""

    subject: Optional[TripleElement] = None
    predicate: Optional[TripleElement] = None
    object: Optional[TripleElement] = None


@dataclass
class Preference:
    """Class representing a preference.

    Note: In the current version of the PKG API, topic refers to the object of
    a triple.
    """

    topic: TripleElement
    weight: float


@dataclass
class PKGData:
    """Represents a statement annotated with a triple and a preference."""

    statement: str
    triple: Optional[Triple] = None
    preference: Optional[Preference] = None
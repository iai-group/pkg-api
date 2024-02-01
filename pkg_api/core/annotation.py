"""Dataclasses for the annotations used in the PKG API."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from pkg_api.core.pkg_types import URI


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
        reference: Raw string reference of the element.
        value: URI, Concept or literal value of the element.
    """

    reference: str
    value: Union[URI, Concept, str, None] = field(default=None)


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
    """Class representing an annotated statement.

    Annotations include a triple, a preference, and logging data.
    """

    statement: str
    triple: Optional[Triple] = None
    preference: Optional[Preference] = None
    logging_data: Dict[str, Any] = field(default_factory=dict)

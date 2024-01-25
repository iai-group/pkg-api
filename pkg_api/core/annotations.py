"""Dataclasses for the annotations used in the PKG API."""

from dataclasses import dataclass
from typing import Optional, Union

from pkg_api.pkg_types import URI


@dataclass
class TripleAnnotation:
    subject: Union[URI, str, None] = None
    predicate: Union[URI, str, None] = None
    object: Union[URI, str, None] = None


@dataclass
class PreferenceAnnotation:
    topic: Union[URI, str]
    weight: float


@dataclass
class PKGData:
    statement: str
    triple: Optional[TripleAnnotation] = None
    preference: Optional[PreferenceAnnotation] = None

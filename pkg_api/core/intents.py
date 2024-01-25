"""Intents for the API."""

from enum import Enum, auto


class Intent(Enum):
    """Enum for intents."""

    ADD = auto()
    GET = auto()
    DELETE = auto()
    UNKNOWN = auto()

"""PKG package types."""
from rfc3987 import match

SPARQLQuery = str


class URI(str):
    def __new__(cls, *args, **kwargs):
        assert match(args[0], rule="IRI"), f"Invalid URI: {args[0]}"
        return super().__new__(cls, *args, **kwargs)

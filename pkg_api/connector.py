"""Connector to triplestore."""
from enum import Enum

from rdflib import Graph
from rdflib.query import Result

from pkg_api.types import URI

# Method to create/load the RDF graph
# Method to execute the SPARQL query

DEFAULT_STORE_PATH = "data/RDFStore"


class RDFStore(Enum):
    """Enum for the different triplestores."""

    MEMORY = "Memory"
    BERKELEYDB = "BerkeleyDB"
    SPARQLUPDATESTORE = "SPARQLUpdateStore"


class Connector:
    def __init__(
        self,
        owner: URI,
        rdf_store: RDFStore = RDFStore.MEMORY,
        rdf_store_path: str = DEFAULT_STORE_PATH,
    ) -> None:
        """Initializes the connector to the triplestore.

        Args:
            owner: Owner URI.
            rdf_store: Type of RDF store to use.
            rdf_store_path: Path to the RDF store.
        """
        self._graph = Graph(rdf_store.value, identifier=owner)
        self._graph.open(rdf_store_path, create=True)

    def execute_sparql_query(self, query: str) -> Result:
        """Execute SPARQL query.

        Args:
            query: SPARQL query.
        """
        return self._graph.query(query)

    def execute_sparql_update(self, query: str) -> None:
        """Execute SPARQL update.

        Args:
            query: SPARQL update.
        """
        self._graph.update(query)

    def close(self) -> None:
        """Close the connection to the triplestore."""
        self._graph.close()

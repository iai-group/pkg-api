"""Connector to triplestore."""
import os
from enum import Enum

from rdflib import Graph
from rdflib.query import Result

from pkg_api.pkg_types import URI

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
        self._rdf_store_path = f"{rdf_store_path}.ttl"
        self._graph = Graph(rdf_store.value, identifier=owner)
        if os.path.exists(self._rdf_store_path):
            self._graph.parse(self._rdf_store_path, format="turtle")
        self._graph.open(rdf_store_path, create=True)

    def execute_sparql_query(self, query: str) -> Result:
        """Executes SPARQL query.

        Args:
            query: SPARQL query.
        """
        return self._graph.query(query)

    def execute_sparql_update(self, query: str) -> None:
        """Executes SPARQL update.

        Args:
            query: SPARQL update.
        """
        self._graph.update(query)

    def close(self) -> None:
        """Closes the connection to the triplestore."""
        self.save_graph()
        self._graph.close()

    def save_graph(self) -> None:
        """Saves the graph to a file."""
        if not os.path.exists(self._rdf_store_path):
            parent_dir = os.path.dirname(self._rdf_store_path)
            os.makedirs(parent_dir, exist_ok=True)
        self._graph.serialize(self._rdf_store_path, format="turtle")

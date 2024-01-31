"""PKG API.

A statement is the main piece of information, it may be enriched with
properties such as subject, object, and predicate (for more details
refer to the PKG vocabulary and class PKGData). A statement may also be
linked to a preference, the representation of a preference is described
in the PKG vocabulary. The PKG vocabulary and an example of a statement
can be found here: https://github.com/iai-group/pkg-vocabulary
"""

import logging
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple, Union

from rdflib import BNode, Literal, URIRef
from rdflib.namespace import NamespaceManager
from rdflib.term import Variable

import pkg_api.utils as utils
from pkg_api.connector import Connector, RDFStore
from pkg_api.core.annotations import Concept, PKGData, Preference, Triple
from pkg_api.core.pkg_types import URI
from pkg_api.mapping_vocab import MappingVocab


class PKG:
    def __init__(self, owner: URI, rdf_store: RDFStore, rdf_path: str) -> None:
        """Initializes PKG of a given user.

        Args:
            owner: Owner URI.
            rdf_store: Type of RDF store.
            rdf_path: Path to the RDF store.
        """
        self._owner_uri = owner
        self._connector = Connector(owner, rdf_store, rdf_path)

    @property
    def owner_uri(self) -> URI:
        """Returns the URI of the owner of this PKG."""
        return self._owner_uri

    def close(self) -> None:
        """Closes the connection to the connector."""
        self._connector.close()

    def get_owner_preference(self, object: URI) -> float:
        """Gets preference for a given object.

        Args:
            object: Object of the preference.

        Returns:
            Preference value.
        """
        return self.get_preference(self._owner_uri, object)

    def get_owner_preferences(self, rdf_class: URI) -> Dict[URI, float]:
        """Gets preferences for a given class.

        Args:
            rdf_class: Class of the preference.

        Returns:
            Dictionary of preferences.
        """
        return self.get_preferences(self._owner_uri, rdf_class)

    def get_preference(self, who: URI, object: URI) -> Optional[float]:
        """Gets the preference for a given object.

        Bindings that are returned after executing a query in RDFLib are
        iterable. By design, we should have up to one binding returned when
        querying for preferences (there is a preference set or not). If more
        than one binding is returned, it means that something went wrong while
        setting the preferences and the exception is raised.

        Args:
            who: Subject of the preference.
            object: Object of the preference.

        Raises:
            Exception: If multiple bindings are returned after executing the
            query.

        Returns:
            Preference value. If no preference is found, returns None.
        """
        query = utils.get_query_for_get_preference(who, object)
        bindings = [
            binding
            for binding in self._connector.execute_sparql_query(query).bindings
        ]
        if len(bindings) > 1:
            raise Exception(
                f"Multiple bindings found for {who} and {object}: "
                f"{bindings}"
            )
        return (
            float(bindings[0].get(Variable("pref")))
            if len(bindings) == 1
            else None
        )

    def get_preferences(self, who: URI, rdf_class: URI) -> Dict[URI, float]:
        """Gets preferences for a given class.

        Args:
            who: Subject of the preference.
            rdf_class: Class of the preference.

        Returns:
            Dictionary of preferences.
        """
        pass

    def add_statement(self, pkg_data: PKGData) -> None:
        """Adds a statement to the PKG.

        Note that if a preference is provided, it will be added with a separate
        query.

        Args:
            pkg_data: PKG data associated to a statement.
        """
        query = utils.get_query_for_add_statement(pkg_data)
        self._connector.execute_sparql_update(query)
        if pkg_data.preference:
            query = utils.get_query_for_add_preference(pkg_data)
            self._connector.execute_sparql_update(query)

    def get_statements(self, pkg_data: PKGData) -> List[PKGData]:
        """Gets statements from the PKG.

        Args:
            pkg_data: PKG data associated to wanted statements.

        Returns:
            PKG data associated to the statement.
        """
        statements = []
        query = utils.get_query_for_get_statement(pkg_data)
        results = self._connector.execute_sparql_query(query).bindings
        for row in results:
            statement_bnode = row.get(Variable("statement"))
            triples = list(
                self._connector._graph.triples((statement_bnode, None, None))
            )
            statement = self._parse_statement_node(
                triples, self._connector._graph.namespace_manager
            )
            statements.append(statement)
        return statements

    def _parse_statement_node(
        self,
        triples: List[Tuple[Any, Any, Any]],
        namespace_manager: NamespaceManager,
    ) -> Optional[PKGData]:
        """Parses a statement node.

        Args:
            triples: List of triples that form the statement.
            namespace_manager: Namespace manager of the graph.

        Returns:
            PKG data associated to the statement.
        """
        statement_dict = defaultdict(lambda: defaultdict())

        for _, p, o in triples:
            value = None
            property = p.n3(namespace_manager)
            pkg_data_field, field_property = MappingVocab.get_pkgdata_field(
                property
            )
            if pkg_data_field is None:
                logging.warning(
                    f"Statement parsing - Property {property} not supported."
                )
                continue
            value = self._parse_triple_object(o)
            if field_property is None:
                statement_dict[pkg_data_field] = value
            else:
                statement_dict[pkg_data_field][field_property] = value

        if not statement_dict.get("statement", None):
            logging.warning(
                "Statement parsing failed, not statement returned."
            )
            return None

        return PKGData(
            statement=statement_dict.get("statement"),
            triple=Triple(**statement_dict.get("triple"))
            if statement_dict.get("triple", None)
            else None,
            preference=Preference(**statement_dict.get("preference"))
            if statement_dict.get("preference", None)
            else None,
            logging_data=dict(statement_dict.get("logging_data", {})),
        )

    def _parse_triple_object(
        self, object: Any
    ) -> Optional[Union[URI, Concept, str]]:
        """Parses a triple object.

        Args:
            object: Triple object.

        Returns:
            Value of the triple object as URI, Concept, or str.
        """
        if isinstance(object, URIRef):
            return URI(str(object))
        elif isinstance(object, Literal):
            return str(object)
        elif isinstance(object, BNode):
            return self._retrieve_and_parse_concept(object)

        logging.warning(
            f"Object {object} of type {type(object)} not supported."
        )
        return None

    def _retrieve_and_parse_concept(
        self, concept_node_id: str
    ) -> Optional[Concept]:
        """Retrieves and parses a concept from the graph.

        Args:
            concept_node_id: Node ID of the concept.

        Returns:
            Concept.
        """
        concept_dict = defaultdict()
        namespace_manager = self._connector._graph.namespace_manager
        for _, p, o in self._connector._graph.triples(
            (concept_node_id, None, None)
        ):
            property = p.n3(namespace_manager)
            concept_field = MappingVocab.CONCEPT_MAPPING.get(property, None)
            if concept_field is None:
                logging.warning(
                    f"Concept parsing - Property {property} not supported."
                )
                continue

            if concept_field == "description":
                concept_dict[concept_field] = str(o)
            else:
                # Other fields of Concept are lists of URIs
                concept_dict.setdefault(concept_field, []).append(URI(str(o)))

        if not concept_dict.get("description", None):
            logging.warning("Concept parsing failed, not description found.")
            return None

        return Concept(**concept_dict)

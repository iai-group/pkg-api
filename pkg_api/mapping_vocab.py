"""Static class that maps labels to predicates in the PKG namespace.

These predicates are used to create SPARQL queries.
See example for a query to retrieve a preference for a given entity:
    SELECT ?preference
    {
    ?who Vocab.PREFERENCE_PROPERTY
    [ Vocab.ENTITY_PROPERTY ?entity ;
    Vocab.WEIGHT_PROPERTY ?preference ]
    }
Note: The naming convention is as follows: the name of the object followed by
its RDF type (i.e., NAME_RDFTYPE). For example, the class preference is named
PREFERENCE_CLASS.
"""


class MappingVocab:
    # Namespace for the RDF vocabulary terms related to the PKG.
    _NS = "http://example.org/pkg/"

    PREFERENCE_CLASS = f"{_NS}Preference"
    PREFERENCE_PROPERTY = f"{_NS}preference"
    WEIGHT_PROPERTY = f"{_NS}weight"
    ENTITY_PROPERTY = f"{_NS}entity"

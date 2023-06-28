"""Static class that maps labels to predicates in the PKG namespace.

These predicates are used to create SPARQL queries.

See example for a query to retrieve a preference for a given entity:
    SELECT ?preference
    {
    ?who Vocab.PREFERENCE
    [ Vocab.ENTITY ?entity ;
      Vocab.PREFERENCE_WEIGHT ?preference ]
    }
"""


class Vocab:
    # Namespace for the RDF vocabulary terms related to the PKG.
    _NS = "http://example.org/pkg/"

    PREFERENCE = f"{_NS}preference"
    PREFERENCE_WEIGHT = f"{_NS}weight"
    ENTITY = f"{_NS}entity"

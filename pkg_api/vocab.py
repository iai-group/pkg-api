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
    PREFERENCE = "pkg:preference"
    PREFERENCE_WEIGHT = "pkg:weight"
    ENTITY = "pkg:entity"

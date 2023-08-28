"""Static class that maps labels to predicates in the PKG namespace.

These predicates are used to create SPARQL queries.

See example for a query to retrieve a preference for a given entity:
    SELECT ?preference
    {
    ?who Vocab.PREFERENCE
    [ Vocab.ENTITY ?entity ;
      Vocab.PREFERENCE_WEIGHT ?preference ]
    }

Note: The naming convention in this file is different from the one used in the
rest of the code. Using upper case only can be a problem since IRIs are case
sensitive, i.e., introduce some confusions between similar IRIS (e.g.,
pkg:Weight and pkg:weight). The naming convention used in this file is to use
the same casing as the predicate label.
See comment: https://github.com/iai-group/pkg-api/pull/17#discussion_r1269803051
"""


class MappingVocab:
    # Namespace for the RDF vocabulary terms related to the PKG.
    _NS = "http://example.org/pkg/"

    Preference = f"{_NS}Preference"
    preference = f"{_NS}preference"
    weight = f"{_NS}weight"
    entity = f"{_NS}entity"

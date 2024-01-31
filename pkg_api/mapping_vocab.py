"""Static class that maps the PKG vocabulary properties to the associated
dataclass fields.

For example, the property description is mapped to the field statement of
PKGData, and the property subject is mapped to the field subject of Triple.
"""


from typing import Optional, Tuple


class MappingVocab:
    PKGDATA_MAPPING = {
        "statement": {"dc:description": None},
        "triple": {
            "rdf:subject": "subject",
            "rdf:predicate": "predicate",
            "rdf:object": "object",
        },
        "preference": {"wi:topic": "topic", "wo:weight_value": "weight"},
        "logging_data": {
            "pav:authoredOn": "authoredOn",
            "pav:authoredBy": "authoredBy",
            "pav:createdOn": "createdOn",
            "pav:createdBy": "createdBy",
        },
    }
    CONCEPT_MAPPING = {
        "dc:description": "description",
        "skos:related": "related_entities",
        "skos:broader": "broader_entities",
        "skos:narrower": "narrower_entities",
    }

    @staticmethod
    def get_pkgdata_field(property: str) -> Tuple[str, Optional[str]]:
        """Gets the field and optionally the nested field of a PKGData given
        a property.

        Args:
            property: Property to be mapped.

        Returns:
            Tuple of the field and optionally the nested field.
        """
        for field, mapping in MappingVocab.PKGDATA_MAPPING.items():
            if property in mapping.keys():
                return field, mapping.get(property, None)
        return None, None

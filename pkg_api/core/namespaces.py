"""Prefixes for namespaces used in the PKG vocabulary.

TODO: The list of prefixes should be automatically generated from the PKG
vocabulary.
See: https://github.com/iai-group/pkg-api/issues/86
"""

from enum import Enum


class PKGPrefixes(Enum):
    """Enum for the different prefixes in the PKG vocabulary."""

    DC = "http://purl.org/dc/terms/"
    DCAT = "http://www.w3.org/ns/dcat#"
    DOAP = "http://usefulinc.com/ns/doap#"
    EVENT = "http://purl.org/NET/c4dm/event.owl#"
    EX = "http://example.org/pkg#"
    FOAF = "http://xmlns.com/foaf/0.1/"
    GEO = "http://www.w3.org/2003/01/geo/wgs84_pos#"
    OWL = "http://www.w3.org/2002/07/owl#"
    PAV = "http://purl.org/pav/"
    RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    RDFS = "http://www.w3.org/2000/01/rdf-schema#"
    SH = "http://www.w3.org/ns/shacl#"
    SKOS = "http://www.w3.org/2004/02/skos/core#"
    VANN = "http://purl.org/vocab/vann/"
    VS = "http://www.w3.org/2003/06/sw-vocab-status/ns#"
    XSD = "http://www.w3.org/2001/XMLSchema#"
    WI = "http://purl.org/ontology/wi/core#"
    WO = "http://purl.org/ontology/wo/core#"
    PKG = "http://w3id.org/pkg/"

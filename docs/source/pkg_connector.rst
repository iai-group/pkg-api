PKG Connector
=============

This component is responsible for establishing a connection to the PKG and executing SPARQL queries against it.
The SPARQL queries are generated based on the user's annotated statements using utility functions.

Features
--------

The PKG Connector has the following features:

- Loading the PKG
- Binding the namespaces related to the PKG vocabulary (see complete list [here](https://iai-group.github.io/pkg-vocabulary/))
- Executing SPARQL queries against the PKG
- Saving the PKG

The PKG Connector uses the [RDFLib](https://github.com/RDFLib/rdflib) library to handle the PKG and execute the SPARQL queries. For this reason, we differentiate between two types of SPARQL queries: (1) queries to update the PKG, such as adding and removing statements, and (2) queries to retrieve information from the PKG.

SPARQL Queries
--------------

The SPARQL queries are automatically generated based on the user's annotated statements and templates. 

- **Insertion queries** for adding statements or preferences to the PKG, the templates are defined in :py:func:`pkg_api.utils.get_query_for_add_statement` and :py:func:`pkg_api.utils.get_query_for_add_preference` respectively.
- **Deletion queries** for removing statements or preferences from the PKG, the templates are defined in :py:func:`pkg_api.utils.get_query_for_remove_statement` and :py:func:`pkg_api.utils.get_query_for_remove_preference` respectively. Additionally, a query to remove dangling objects is provided.
- **Retrieval queries** for retrieving statements or preferences from the PKG, the templates are defined in :py:func:`pkg_api.utils.get_query_for_get_statements` and :py:func:`pkg_api.utils.get_query_for_get_preferences` respectively. For more flexibility, templates for retrieving statements and preferences based on specific criteria are also provided, see :py:func:`pkg_api.utils.get_query_for_conditional_get_statements` and :py:func:`pkg_api.utils.get_query_for_conditioned_get_preference`.

All templates are defined in the `pkg_api.utils` module.
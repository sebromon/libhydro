# -*- coding: utf-8 -*-
"""Module xml.to_xml.

Ce module contient des convertisseurs vers le format
Xml Hydrometrie (version 1.1 exclusivement).

Fonctions disponibles:
    (TODO)

Exemples d'utilisation:
    (TODO)

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from lxml import etree as _etree


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1a"""
__date__ = """2013-08-20"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


#-- todos ---------------------------------------------------------------------


#-- config --------------------------------------------------------------------
# mappings

# object = {attribute: xml tag, ...}

# FIXME - DO NOT WORK ORDER MATTERS !!!!
# use ordered dic ?

scenario = {
    'code': 'CodeScenario',
    'version': 'VersionScenario',
    'nom': 'NomScenario',
    'dtfichier': 'DateHeureCreationFichier'
}

destinataire = {
    'destinataire': 'CdIntervenant'
}

# check strict = TRUE -******************************

#-- functions ------------------------------------------------------------------
def to_xml(scenario, *args):
    """Fonction to_xml."""

    # FIXME
    # import ipdb; ipdb.set_trace()

    tree = _etree.Element('hydrometrie')

    # add scenario
    s = _etree.SubElement(tree, 'Scenario')
    for (k, v) in scenario.iteritems():
        child = _etree.SubElement(s, v)
        child.text = unicode(getattr(scenario, k))

    # add args

    # return
    print(
        _etree.tostring(
            tree, encoding='utf-8', xml_declaration=1,  pretty_print=1
        )
    )
    return tree

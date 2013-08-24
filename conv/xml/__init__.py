# -*- coding: utf-8 -*-
"""Module libhydro.conv.xml.

Ce module contient des convertisseurs de et vers les fichiers au format
Xml Hydrometrie (version 1.1 exclusivement).

Fonctions de lecture:
    (TODO)

Fonctions d'ecriture:
    (TODO)

Il contient egalement la classe:
    # Scenario

Exemples d'utilisation:
    (TODO)

"""
# import *
__all__ = [
    'Scenario',
    'parse',
    'to_xml'
]

# for the user, this package is like a module, sub-modules names are
# underscored to hide them
from _scenario import Scenario
from _from_xml import parse
from _to_xml import to_xml

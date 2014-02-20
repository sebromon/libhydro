# -*- coding: utf-8 -*-
"""Module libhydro.conv.xml.

Le module xml contient des convertisseurs de et vers les fichiers au format
Xml Hydrometrie (version 1.1 exclusivement), disponibles au travers la classe
Message.

Il contient les classes:
    # Message
    # Scenario

Exemples d'utilisation:
    (TODO)

"""
__all__ = ['Message', 'Scenario']
# for the user, this package is like a module, sub-modules names are
# underscored to hide them
from ._from_xml import Scenario
from ._xml import Message

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function
"""Module python nomenclature.

Contient les nomenclatures Sandre utilisées pour l'Hydrométrie.

Usage:

    NOMENCLATURES est la liste des nomenclatures (NOMENCLATURE.keys()).
        Les codes des nomenclatures sont toujours des entiers.

    NOMENCLATURE[i] est la nomenclature i, sous la forme d'un dictionnaire
        {code: mnémonique, ...}. Les codes des items d'une nomenclature sont
        des entiers ou des chaînes.

"""

#-- strings -------------------------------------------------------------------
__author__ = """philippe.gouin@developpement-durable.gouv.fr"""
__version__ = """version 0.1a"""
__date__ = """2013-07-12"""

#HISTORY
#V0.1 - 2013-07-12
#    first shot

#-- todos ---------------------------------------------------------------------
# TODO - all nomenclatures

# -- config -------------------------------------------------------------------
NOMENCLATURE = {

    #Syntaxe: "reférence : {code: mnémonique, ...}"

    # Grandeur observée de la série
    509: {'H': 'Hauteur', 'Q': 'Débit'},

    # Statut de la série
    510: {
        0: 'Sans validation', 4: 'Brute', 8: 'Corrigé',
        12: 'Pré-validé', 16: 'Validé'
    },

    # Type de site hydrométrique
    530: {
        'REEL': 'Site réel', 'FICTIF': 'Site fictif',
        'MAREGRAPHE': 'Marégraphe', 'PONCTUEL': 'Site de jaugeage ponctuel',
        'VIRTUEL': 'Site virtuel',
        'RECONSTITUE': 'Site à débit moyen mensuel reconstitué',
        'PLANDEAU': "Plan d'eau", 'SOURCE': 'Source'
    },

    # Type de station hydrométrique
    531: {
        'LIMNI': 'Limnimètre', 'DEB': 'Débitmètre', 'HC': 'Hauteur calculée',
        'LIMNIMERE': 'Limnimètre station mère',
        'LIMNIFILLE': 'Limnimètre station fille'
    }

}

NOMENCLATURES = NOMENCLATURE.keys()

# -*- coding: utf-8 -*-
"""Module python nomenclature.

Contient les nomenclatures Sandre utilisees pour l'Hydrometrie.

Usage:

    NOMENCLATURES est la liste des nomenclatures (NOMENCLATURE.keys()).
        Les codes des nomenclatures sont toujours des entiers.

    NOMENCLATURE[i] est la nomenclature i, sous la forme d'un dictionnaire
        {code: mnemonique, ...}. Les codes des items d'une nomenclature sont
        des entiers ou des chaînes.

"""
#-- imports -------------------------------------------------------------------
from __future__ import unicode_literals, absolute_import, division, print_function


#-- strings -------------------------------------------------------------------
__author__ = """philippe.gouin@developpement-durable.gouv.fr"""
__version__ = """version 0.1b"""
__date__ = """2013-08-05"""

#HISTORY
#V0.1 - 2013-07-12
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - all nomenclatures


# -- config -------------------------------------------------------------------
NOMENCLATURE = {

    #Syntaxe: "reference : {code: mnemonique, ...}"

    # Methode d'obtention du resultat de l'observation hydro
    507: {0: 'Mesure', 4: 'Reconstitution', 12: 'Interpolation'},

    # Grandeur observee de la serie
    509: {'H': 'Hauteur', 'Q': 'Debit'},

    # Statut de la serie
    510: {
        0: 'Sans validation', 4: 'Brute', 8: 'Corrige',
        12: 'Pre-valide', 16: 'Valide'
    },

    # Qualification de la donnees de l'observation hydrometrique
    515: {
        0: 'Neutre',
        4: 'Faible',
        8: 'Forte',
        12: 'Valeur incertaine',
        16: 'Valeur non qualifiee',
        20: 'Valeur bonne'
    },

    # Type de mesure du cpateur hydro
    520: {'H': 'Hauteur', 'Q': 'Debit'},

    # Type de site hydrometrique
    530: {
        'REEL': 'Site reel', 'FICTIF': 'Site fictif',
        'MAREGRAPHE': 'Maregraphe', 'PONCTUEL': 'Site de jaugeage ponctuel',
        'VIRTUEL': 'Site virtuel',
        'RECONSTITUE': 'Site a debit moyen mensuel reconstitue',
        'PLANDEAU': "Plan d'eau", 'SOURCE': 'Source'
    },

    # Type de station hydrometrique
    531: {
        'LIMNI': 'Limnimetre', 'DEB': 'Debitmetre', 'HC': 'Hauteur calculee',
        'LIMNIMERE': 'Limnimetre station mere',
        'LIMNIFILLE': 'Limnimetre station fille'
    }

}

NOMENCLATURES = NOMENCLATURE.keys()

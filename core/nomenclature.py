# -*- coding: utf-8 -*-
"""Module python nomenclature.

Contient les nomenclatures Sandre utilisees pour l'Hydrometrie.

Usage:

    NOMENCLATURES est la liste des nomenclatures (NOMENCLATURE.keys()).
        Les codes des nomenclatures sont toujours des entiers.

    NOMENCLATURE[i] est la nomenclature i, sous la forme d'un dictionnaire
        {code: mnemonique, ...}. Les codes des items d'une nomenclature sont
        des entiers ou des chaines.

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)


#-- strings -------------------------------------------------------------------
__author__ = """philippe.gouin@developpement-durable.gouv.fr"""
__version__ = """0.1d"""
__date__ = """2013-08-09"""

#HISTORY
#V0.1 - 2013-07-12
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - all nomenclatures
# TODO - write a decorator to check an attribute validity


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

    # Statut de la simulation
    516: {4: 'Brute', 16: 'Critiquee'},

    # Type de mesure du capteur hydro
    520: {'H': 'Hauteur', 'Q': 'Debit'},

    # Type du modele de prevision
    525: {
        0: 'Inconnu',
        1: "Prevision d'expert",
        2: 'Modele hydrologique empirique',
        3: 'Modele hydrologique a base physique',
        4: 'Modele hydraulique',
        5: 'Modele statistique',
        6: 'Enchainement de modeles',
        7: 'Modele a propagation empirique'
    },

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
    },

    # Civilité du contact
    538: {
        1: 'Monsieur', 2: 'Madame', 3: 'Mademoiselle'
    }
}

NOMENCLATURES = NOMENCLATURE.keys()

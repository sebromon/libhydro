# coding: utf-8
"""Module python nomenclature.

Contient les nomenclatures Sandre utilisees pour l'Hydrometrie.

Usage:

    NOMENCLATURES est la liste des nomenclatures (NOMENCLATURE.keys()).
        Les codes des nomenclatures sont toujours des entiers.

    NOMENCLATURE[i] est la nomenclature i, sous la forme d'un dictionnaire
        {code: mnemonique, ...}. Les codes des items d'une nomenclature sont
        des entiers ou des chaines.

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.6a"""
__date__ = """2014-07-15"""

# HISTORY
# V0.6 - 2014-07-15
#   add a bunch of nomenclatures
# V0.1 - 2013-07-12
#   first shot


# -- todos --------------------------------------------------------------------
# TODO - all nomenclatures
# TODO - write a decorator to check an attribute validity


# -- config -------------------------------------------------------------------
NOMENCLATURE = {

    # Syntaxe: "reference : {code: mnemonique, ...}"

    # Projection des coordonnees
    22: {
        0: 'Projection inconnue',
        1: 'Lambert I Nord',
        2: 'Lambert II Centre',
        3: 'Lambert III Sud',
        4: 'Lambert IV Corse',
        5: 'Lambert II Etendu',
        6: 'Lambert I Carto',
        7: 'Lambert II Carto',
        8: 'Lambert III Carto',
        9: 'Lambert IV Carto',
        10: 'ED50 UTM30',
        11: 'ED50 UTM31',
        12: 'ED50 UTM32',
        13: 'WGS72 UTM30',
        14: 'WGS72 UTM31',
        15: 'WGS72 UTM31',
        16: 'WGS84 UTM30',
        17: 'WGS84 UTM31',
        18: 'WGS84 UTM32',
        19: 'Reunion Gauss Laborde',
        20: 'Martinique Fort Desaix',
        21: 'Guadeloupe Saint-Anne',
        22: 'Guyane CSG67UTM21',
        23: 'Guyane CSG67UTM22',
        24: 'Mayotte Combani',
        25: 'Saint Pierre et Miquelon',
        26: 'RGF93 / Lambert 93',
        27: 'NTFG',
        28: 'NTFP',
        29: 'ED50G',
        30: 'WGS72G',
        31: 'WGS84G',
        32: 'Reunion geo. 1947',
        33: 'Guadeloupe St Anne geo',
        34: 'Guyane CSG67 geo.',
        35: 'Mayotte Combani geo.',
        36: 'St Pierre et Miquelon geo',
        37: 'ETRS89',
        38: 'RGR92 / UTM 40',
        39: 'RRAF 91 / UTM 20',
        40: 'RGFG95 / UTM 22',
        41: 'RGM04 / UTM 38',
        42: 'RGSPM06 / UTM 21',
        43: 'RGF93 / CC42 (CC Zone 1)',
        44: 'RGF93 / CC42 (CC Zone 2)',
        45: 'RGF93 / CC42 (CC Zone 3)',
        46: 'RGF93 / CC42 (CC Zone 4)',
        47: 'RGF93 / CC42 (CC Zone 5)',
        48: 'RGF93 / CC42 (CC Zone 6)',
        49: 'RGF93 / CC42 (CC Zone 7)',
        50: 'RGF93 / CC42 (CC Zone 8)',
        51: 'RGF93 / CC42 (CC Zone 9)',
        52: 'RGF93 geographiques (2D)',
        53: 'RRAF 1991 cartesiennes',
        54: 'RGFG95 geographiques (2D)',
        55: 'RGR92 geographiques (3D)',
        56: 'RGM04 cartesiennes',
        57: 'RGSPM06 cartesiennes',
        58: 'ETRS89 / LAEA',
        59: 'ETRS89 / LCC',
        60: 'ETRS89 / UTM Nord 30',
        61: 'ETRS89 / UTM Nord 31',
        62: 'ETRS89 / UTM Nord 32',
        63: 'WGS84 Web Mercator'
    },

    # Methode d'obtention du resultat de l'observation hydrometrique
    507: {0: 'Mesure', 4: 'Reconstitution', 12: 'Interpolation'},

    # Qualification de la donnees de l'observation meteorologique
    508: {
        0: 'Inconnu',
        12: 'Valeur incertaine',
        16: 'Valeur non qualifiee',
        20: 'Valeur bonne'
    },

    # Grandeur observee de la serie
    509: {'H': 'Hauteur', 'Q': 'Debit'},

    # Statut de la serie
    510: {
        0: 'Sans validation', 4: 'Brute', 8: 'Corrige',
        12: 'Pre-valide', 16: 'Valide'
    },

    # Statut de l'observation meteorologique
    511: {
        0: 'Sans validation', 4: 'Brute', 8: 'Corrige'
    },

    # Methode d'obtention du resultat de l'observation meteoroloqiue
    512: {
        0: 'Mesure', 4: 'Reconstitution', 8: 'Calcul',
        12: 'Interpolation', 16: 'Forcage'
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

    # Type de mesure du capteur hydrometrique
    520: {'H': 'Hauteur', 'Q': 'Debit'},

    # Grandeur meteorologique
    523: {
        'RR': "Cumul de precipitations",
        'TA': "Temperature de l'air",
        'PA': "Pression atmospherique",
        'HN': "Hauteur de neige",
        'EE': "Equivalent en eau",
        'VV': "Vitesse du vent",
        'DV': "Direction du vent",
        'EP': "Evapotranspiration potentielle",
        'ER': "Evapotranspiration reelle",
        'EM': "Evapotranspiration maximale",
        'RA': "Rayonnement",
        'HR': "Humidite relative",
        'HA': "Humidite absolue"
    },

    # Type du modele de prevision
    525: {
        0: "Inconnu",
        1: "Prevision d'expert",
        2: "Modele hydrologique empirique",
        3: "Modele hydrologique a base physique",
        4: "Modele hydraulique",
        5: "Modele statistique",
        6: "Enchainement de modeles",
        7: "Modele a propagation empirique"
    },

    # Type de seuil
    528: {1: 'Absolu', 2: 'Gradient'},

    # Nature du seuil
    529: {
        11: 'Seuil reglementaire valeur basse',
        12: 'Seuil reglementaire valeur forte',
        21: 'Seuil technique valeur basse',
        22: 'Seuil technique valeur forte',
        23: 'Seuil opérateur valeur basse',
        24: 'Seuil opérateur valeur haute',
        31: 'Seuil historique valeur basse',
        32: 'Seuil historique valeur forte',
        41: 'Seuil expertise valeur basse',
        42: 'Seuil expertise valeur forte',
        101: 'Seuil inferieur de valeur aberrante',
        102: 'Seuil superieur de valeur aberrante'
    },

    # Type de site hydrometrique
    530: {
        'REEL': "Site reel",
        'FICTIF': "Site fictif",
        'MAREGRAPHE': "Maregraphe",
        'PONCTUEL': "Site de jaugeage ponctuel",
        'VIRTUEL': "Site virtuel",
        'RECONSTITUE': "Site a debit moyen mensuel reconstitue",
        'PLANDEAU': "Plan d'eau",
        'SOURCE': "Source"
    },

    # Type de station hydrometrique
    531: {
        'LIMNI': 'Limnimetre',
        'DEB': 'Debitmetre',
        'HC': 'Hauteur calculee',
        'LIMNIMERE': 'Limnimetre station mere',
        'LIMNIFILLE': 'Limnimetre station fille'
    },

    # Type de publication de l'evenement
    534: {
        1: 'Fiches site et station',
        10: 'Vigicrues et tableau des dernieres valeurs',
        20: 'Vigicrues uniquement',
        25: 'Archive',
        30: 'Tableau des dernieres valeurs',
        100: 'Privé'
    },

    # Civilite du contact
    538: {
        1: 'Monsieur', 2: 'Madame', 3: 'Mademoiselle'
    }
}

NOMENCLATURES = NOMENCLATURE.keys()

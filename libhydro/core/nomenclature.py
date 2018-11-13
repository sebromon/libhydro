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
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)


# -- strings ------------------------------------------------------------------
__version__ = '0.6.4'
__date__ = '2015-09-29'

# HISTORY
# V0.6.4 - SR - 2015-09-23
# add nomenclature 923 (continuite obshydro)
# V0.6.3 - SR - 2015-09-23
# add nomenclature 519 (type du capteur)
# V0.6.2 - SR - 2015-06-09
# add nomenclature 76
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
        63: 'WGS84 Web Mercator'},

    # Système altimétrique
    76: {
        0: 'Système altimétrique inconnu',
        1: 'Bourdeloue 1857',
        2: 'NGF84',
        3: 'IGN 1969',
        4: 'NGC48',
        5: 'IGN 1978 (Corse)',
        6: 'IGN 1958 (Réunion)',
        7: 'IGN 1989 (Réunion)',
        8: 'IGN 1955 (Martinique)',
        9: 'IGN 1987 (Martinique)',
        10: 'IGN 1951 (Guadeloupe)',
        11: 'IGN 1988 (Guadeloupe)',
        12: 'IGN 1988 (Guadeloupe Les Saintes)',
        13: 'IGN 1988 (Guadeloupe Marie Galante)',
        14: 'IGN 1988 (Guadeloupe St Martin)',
        15: 'IGN 1988 (Guadeloupe St Barthelemy)',
        16: 'IGN 1942 (Guyane)',
        17: 'Niv. Général de la Guyane 1977',
        18: 'IGN 1950 (Mayotte)',
        19: 'Equipe 1979 (Mayotte)',
        20: 'Danger 1950 (St Pierre et Miquelon)',
        21: 'NGNC 1969 (Nelle Calédonie)',
        22: 'IGN 1984 (Wallis et Futuna)',
        23: 'SHOM 1953 (Mayotte)',
        24: 'Tahiti IGN 1966 (Polynésie)',
        25: 'SHOM 1981 (Iles Loyauté)',
        26: 'SHOM 1976 (Iles Loyauté)',
        27: 'SHOM 1970 (Iles Loyauté)',
        28: 'IGN 1962 (Iles Kerguelen)',
        29: 'EPF 1952 (Terre Adélie)',
        30: 'SHOM 1977 (Ile du canal du Mozambique)',
        31: 'TN'
    },

    # Influence générale hydro
    104: {
        0: 'Inconnue',
        1: 'Nulle',
        2: 'Etiage seulement',
        3: 'Forte',
        4: 'Hautes eaux seulement'
    },

    # Loi pour le module
    114: {
        0: 'Inconnue',
        1: 'Galton',
        2: 'Gauss',
        3: 'Gumbel'
    },

    # Statut hydrlogique du site hydro
    460: {1: 'Avec signification hydrologique',
          2: 'Sans signification hydrologique',
          3: 'Source captée'},

    # Type de courbe de tarage
    503: {0: 'Polyligne', 4: 'Fonction puissance'},

    # Etat de la courbe de tarage
    504: {0: 'Non utilisable', 4: 'Utilisable', 8: 'Utilisée', 12: 'Travail'},

    # Qualification du pivot de la courbe de tarage
    505: {12: 'Incertain', 16: 'Non qualifié', 20: 'Bon'},

    # Methode d'obtention du resultat de l'observation hydrometrique
    507: {0: 'Mesure', 4: 'Reconstitution', 12: 'Interpolation'},

    # Qualification de la donnees de l'observation meteorologique
    508: {
        0: 'Inconnu',
        12: 'Valeur incertaine',
        16: 'Valeur non qualifiee',
        20: 'Valeur bonne'},

    # Grandeur observee de la serie
    509: {'H': 'Hauteur', 'Q': 'Debit'},

    # Statut de la serie
    510: {
        0: 'Sans validation', 4: 'Brute', 8: 'Corrige',
        12: 'Pre-valide', 16: 'Valide'},

    # Statut de l'observation meteorologique
    511: {0: 'Sans validation', 4: 'Brute', 8: 'Corrige'},

    # Methode d'obtention du resultat de l'observation meteoroloqiue
    512: {
        0: 'Mesure', 4: 'Reconstitution', 8: 'Calcul',
        10: 'Expertisée', 14: 'Estimé',
        12: 'Interpolation', 16: 'Forcage'},

    # Type de grandeur de l'observation élaborée hydro
    513: {
        # 'QmJ': 'Débit moyen journalier',
        'QmM': 'Débit moyen mensuel',
        'QIXM': 'Débit instantanée maximal mensuel',
        'QINM': 'Débit instantanée minimal mensuel',
        'HIXM': 'Hauteur instantanée maximale mensuelle',
        'HINM': 'Hauteur instantanée minimale mensuelle',
        'dQmM': 'Delta du débit moyen mensuel pour la reconstitution du débit naturel',
        # 'QIXJ': 'Débit instantané maximal journalier',
        # 'QINJ': 'Débit instantané minimal journalier',
        # 'HIXJ': 'Hauteur instantanée maximale journalier',
        # 'HINJ': 'Hauteur instantanée minimal journalier'
        'Module': 'Débit moyen inter-annuel',
        'QIX': 'Débit instantané maximum',
        'QIN': 'Débit instantané minimum',
        'QmnJ': 'Débit moyen sur n jours',
        'QIXnJ': 'Débit instantané maximal n journalier',
        'QINnJ': 'Débit instantané minimal n journalier',
        'HIXnJ': 'Hauteur instantanée maximale n journalière',
        'HINnJ': 'Hauteur instantanée minimale n journalière',
        'QmnH': 'Débit moyen n horaire',
        'HmnH': 'Hauteur moyenne n horaire',
        'HmnJ': 'Hauteur moyenne n journalière',
        'HmM': 'Hauteur moyenne mensuelle'
    },

    # Qualification de la donnees de l'observation hydrometrique
    515: {
        0: 'Neutre',
        4: 'Faible',
        8: 'Forte',
        12: 'Valeur incertaine',
        16: 'Valeur non qualifiee',
        20: 'Valeur bonne'},

    # Statut de la simulation
    516: {4: 'Brute', 16: 'Critiquee'},
    # Type du capteur
    519: {
        0: 'Inconnu',
        1: 'Observateur',
        2: 'Bulle à bulle',
        3: 'Ultrasons (gele)',
        4: 'Radar',
        5: 'Pression',
        6: 'Codeur',
        7: 'Nilomètre',
        8: 'Ultrason immergé',
        9: 'Ultrason aérien',
        10: 'Ultrason débit',
        11: 'Vidéo',
        12: 'Limni'},
    # Type de mesure du capteur hydrometrique
    520: {'H': 'Hauteur', 'Q': 'Debit'},

    # Type de contexte loi statistique
    521: {
        1: 'Module',
        2: 'Crue',
        3: 'Etiage'
    },

    # Code de la finalité de la stationhydro
    522: {
        0: 'Inconnue',
        1: 'Suivi d\'étiage',
        2: 'Prévision des crues',
        3: 'Gestion des ouvrages',
        4: 'Police des eaux',
        5: 'Directive Cadre sur l\'Eau',
        6: 'Suivi qualitatif',
        7: 'Connaissance des flux',
        8: 'Zones humides'},

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
        'HA': "Humidite absolue"},

    # Type d'illustration de l'image
    524: {
        1: 'Localisation générale',
        2: 'Localisation précise',
        3: 'Photo'
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
        7: "Modele a propagation empirique"},

    # Code du régime hydrométrique
    526: {
        1: 'Basses eaux',
        2: 'Moyennes eaux',
        3: 'Hautes eaux'},

    # Rôle du contact hydrométrique
    527: {
        'ADM': 'Administrateur',
        'REF': 'Responsable référentiel',
        'RC': 'Responsable règles de calcul',
        'EXP':
            'Gestion des paramètres liés aux échanges de données temps réel',
        'DB': 'Responsable données brutes et concentrations',
        'DC': 'Responsable données corrigées',
        'DP': 'Responsable données pré validées',
        'DV': 'Responsable données validées',
        'MA': 'Responsable maintenance',
        'CT': 'Droit de consultation',
        'PRV': 'Prévisionniste'},

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
        102: 'Seuil superieur de valeur aberrante'},

    # Type de site hydrometrique
    530: {
        'REEL': "Site reel",
        'FICTIF': "Site fictif",
        'MAREGRAPHE': "Maregraphe",
        'PONCTUEL': "Site de jaugeage ponctuel",
        'VIRTUEL': "Site virtuel",
        'RECONSTITUE': "Site a debit moyen mensuel reconstitue",
        'PLANDEAU': "Plan d'eau",
        'SOURCE': "Source"},

    # Type de station hydrometrique
    531: {
        'LIMNI': 'Limnimetre',
        'DEB': 'Debitmetre',
        'HC': 'Hauteur calculee',
        'LIMNIMERE': 'Limnimetre station mere',
        'LIMNIFILLE': 'Limnimetre station fille'},

    # Droit de pubilcation de la station hydrometrique
    532: {
        10: 'Public',
        11: 'Public sans courbe de tarage ni courbe de correction',
        12: 'Hauteur publique',
        14: 'Débit public',
        20: 'Restreint',
        30: 'Privé'},

    # Qualification des données de la station hydrométrique
    533: {
        12: 'Incertaine',
        16: 'Non qualifiée',
        20: 'Bonne'},

    # Type de publication de l'evenement
    534: {
        1: 'Fiches site et station',
        10: 'Vigicrues et tableau des dernieres valeurs',
        20: 'Vigicrues uniquement',
        25: 'Archive',
        30: 'Tableau des dernieres valeurs',
        100: 'Privé'},

    # Civilite du contact
    538: {1: 'Monsieur', 2: 'Madame', 3: 'Mademoiselle'},

    # Droit de publication site hydrométrique
    871: {
        10: 'Public',
        20: 'Restreint',
        30: 'Privé'
    },

    # Contexte de production de l'observation météorologique
    872: {
        0: 'Contexte inconnu',
        1: 'Pluie',
        2: 'Neige',
        3: 'Début d\'un cumul',
        4: 'Fin d\'un cumul',
        8: 'Début d\'un cumul neige',
        9: 'Fin d\'un cumul neige'
        },

    # Mode de jaugeage du site hydrométrique
    873: {0: 'Inconnu',
          1: 'Saumon point par point',
          2: 'Saumon par integration',
          3: 'Perche point par point',
          4: 'Perche par integration',
          5: 'Dilution par integration',
          6: 'Dilution a debit constant',
          7: 'Flotteur',
          8: 'Debit mesure directement',
          9: 'Jaugeage par mesure de vitesse en surface',
          10: 'Mesure par ADCP',
          11: 'Autres'
          },

    # Type de publication évènements
    874: {
        0: 'Inconnu',
        10: 'Public hautes eaux',
        11: 'Public basses eaux',
        12: 'Public tous régimes',
        20: 'Privé hautes eaux',
        21: 'Privé basses eaux',
        22: 'Privé tous régimes',
        30: 'Protégé hautes eaux',
        31: 'Protégé basses eaux',
        32: 'Protégé tous régimes'
    },

    # Type de la série d'observations élaborées météorologiques
    876: {1: 'Observation pondérée',
          2: 'Indice de précipitations antérieures'},

    # Qualification du jeugeage
    877: {0: 'Inconnu',
          1: 'Douteux',
          2: 'Bon'},

    # Type d'événement hydrométrique ou météorologique
    891: {
        0: 'Inconnu',
        1: 'Recalage hauteur',
        2: 'Recalage temps',
        3: 'Déplacement',
        4: 'Dérangement',
        5: 'Hauteur influencée',
        6: 'Lecture échelle',
        7: 'Commentaire Vigicrues'
    },

    # Continuité de la donnée de l'observation hydro
    923: {
        0: 'Valeur continue',
        1: 'Valeur discontinue',
        4: 'Valeur discontinue faible',
        6: 'Valeur discontinue neutre',
        8: 'Valeur discontinue forte'
        }
}

NOMENCLATURES = list(NOMENCLATURE.keys())

MODEJAUGEAGEMNEMO = {
    0: 'Inconnu',
    1: 'SP',
    2: 'SI',
    3: 'PP',
    4: 'PI',
    5: 'DI',
    6: 'DC',
    7: 'FL',
    8: 'QD',
    9: 'AP',
    10: 'AU',
    11: 'VS'
    }

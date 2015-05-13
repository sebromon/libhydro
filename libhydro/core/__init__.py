# coding: utf-8
"""Package libhydro.core.

Ce package expose les classes modelisees par le Sandre dans les dictionnaires:
    # referentiel hydrometrique (V2.1)
    # processus d'acquisition des donnees hydrometriques (V1.1)

Il contient les modules:
    # evenement
    # intervenant
    # modeleprevision
    # nomenclature
    # obshydro
    # obsmeteo
    # seuil
    # simulation
    # sitehydro
    # sitemeteo

"""
__all__ = [
    'evenement',
    'intervenant',
    'modeleprevision',
    'nomenclature',
    'obshydro',
    'obsmeteo',
    'seuil',
    'simulation',
    'sitehydro',
    'sitemeteo',
]

from . import evenement, intervenant, modeleprevision, nomenclature, \
    obshydro, obsmeteo, seuil, simulation, sitehydro, sitemeteo

# alarm
# courbecorrection
# courbetarage
# gradienthydro
# jaugeage
# obselaboreehydro
# qualifannee

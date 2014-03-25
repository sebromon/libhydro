# -*- coding: utf-8 -*-
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
    # seuil
    # simulation
    # sitehydro

"""
__all__ = [
    'evenement',
    'intervenant',
    'modeleprevision',
    'nomenclature',
    'obshydro',
    'seuil',
    'simulation',
    'sitehydro'
]

from . import evenement, intervenant, modeleprevision, nomenclature, \
    obshydro, seuil, simulation, sitehydro

# alarm
# courbecorrection
# courbetarage
# gradienthydro
# jaugeage
# obselaboreehydro
# obsmeteo
# qualifannee
# sitemeteo

# -*- coding: utf-8 -*-
"""Module shom.

Ce module contient des convertisseurs de et vers les fichiers de predictions
de marees du SHOM:
    simulation_from_hsf()
    simulation_to_hsf()  -- TODO not implemented --

On peux aussi manipuler ces donnees comme des observations simplifiee a l'aide
des fonctions suivantes:
    serie_from_hsh()
    serie_to_hsf()  -- TODO not implemented --

Format des fichiers HSF:
    # fichier texte avec extension hfs
    # le nom du fichier est le nom du maregraphe ou du port en majuscule
    # une ligne par donnee au format "yyyy-mm-dd hh:mm:ss xx.xx"
    # pas de temps constant et heures TU
    # les hauteurs sont en metres. Se referer au descriptif du port fourni par
        le SHOM pour determiner la reference altimetrique

Exemple:
...
2013-01-23 00:00:00  3.46
2013-01-23 00:10:00  3.51
2013-01-23 00:20:00  3.55
...

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import os as _os
import pandas as _pandas
import numpy as _numpy

from ...core import (
    sitehydro as _sitehydro, modeleprevision as _modeleprevision,
    obshydro as _obshydro, simulation as _simulation
)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1b"""
__date__ = """2013-08-13"""

#HISTORY
#V0.1 - 2013-08-01
#    first shot


#-- todos ---------------------------------------------------------------------


#-- functions -----------------------------------------------------------------
def simulation_from_hsf(src, begin=None, end=None, entite=None, dtprod=None):
    """Retourne une simulation.Simulation a partir d'un fichier HSF.

    Arguments:
        src (str o ou file) = fichier source
        begin, end (isoformat string) = dates de debut/fin de la plage de
            valeurs a conserver, bornes incluses
        entite( Sitehydro, Stationhydro ou Capteur)
        dtprod (string ou datetime) = date de production

    """
    # use the Serie decoder
    serie = serie_from_hsf(src=src, begin=begin, end=end, entite=entite)
    prev = serie['res']  # TODO indice prob

    # make dtprod a date
    if isinstance(dtprod, (unicode, str)):
        dtprod = _numpy.datetime64(dtprod)

    # return Simulation
    return _simulation.Simulation(
        entite=serie.entite,
        modeleprevision=_modeleprevision.Modeleprevision(code='SCnMERshom'),
        grandeur='H',
        statut=16,
        qualite=100,
        public=False,
        commentaire='data SHOM',
        dtprod=dtprod,
        previsions=prev
    )


def simulation_to_hsf():
    """Not implemented."""
    # TODO
    raise NotImplementedError()


def serie_from_hsf(src, begin=None, end=None, entite=None):
    """Retourne une obshydro.Serie a partir d'un fichier HSF.

    La Serie est simplifiee et ne contient que la colonne res.

    Arguments:
        src (str o ou file) = fichier source
        begin, end (isoformat string) = dates de debut/fin de la plage de
            valeurs a conserver, bornes incluses
        entite( Sitehydro, Stationhydro ou Capteur)

    """
    # parse file
    df = _pandas.read_table(
        src,
        header=None,
        delim_whitespace=True,
        parse_dates=[[0, 1]],
        index_col=0,
        names=['date', 'heure', 'res']
    )
    # update the DataFrame
    df.index.name = 'dte'
    # if entite is None, get HSF file name
    if not entite:
        entite = _sitehydro.Sitehydro(
            typesite='MAREGRAPHE',
            libelle=_os.path.splitext(_os.path.split(src)[-1])[0]
        )
    # skip rows and return
    return _obshydro.Serie(
        entite=entite,
        grandeur='H',
        observations=df[begin:end]
    )


def serie_to_hsf(dst):
    """Not implemented."""
    # TODO
    raise NotImplementedError()

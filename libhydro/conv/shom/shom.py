# -*- coding: utf-8 -*-
"""Module shom.

Ce module contient des convertisseurs de et vers les fichiers de predictions
de marees du SHOM:
    simulation_from_hfs()
    simulation_to_hfs()  -- not implemented --

On peut aussi manipuler ces donnees comme des observations simplifiees a l'aide
des fonctions suivantes:
    serie_from_hfs()
    serie_to_hfs()  -- not implemented --

Format des fichiers HFS:
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
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2a"""
__date__ = """2014-09-25"""

#HISTORY
#V0.2 - 2014-09-25
#    fix conversion to mm
#V0.1 - 2013-08-01
#    first shot


#-- todos ---------------------------------------------------------------------
# FIXME - simulation_from_hfs is rather slow
#         15s to load a complete 4 years file in a simulation from DVD
#         (5s in a serie is quite good)
#         One could use use skiprows and nrows read_table options


#-- functions -----------------------------------------------------------------
def simulation_from_hfs(
    src, stationhydro=None, begin=None, end=None, dtprod=None, strict=True
):
    """Retourne une simulation.Simulation a partir d'un fichier HFS.

    Arguments:
        src (str o ou file) = fichier source
        stationhydro (Stationhydro) = par defaut utilise le nom du fichier src
        begin, end (isoformat string) = dates de debut/fin de la plage de
            valeurs a conserver, bornes incluses
        dtprod (string ou datetime) = date de production
        strict (bool, defaut True) = le mode permissif permet de lever le
            controle de validite de la stationhydro

    """
    # get a obshydro.Serie from the Serie decoder
    serie = serie_from_hfs(
        src=src, stationhydro=stationhydro, begin=begin, end=end, strict=strict
    )

    # make a multiindex with probability 50 for every value
    index = _pandas.MultiIndex.from_tuples(
        zip(
            serie.observations.index.tolist(),
            [50] * len(serie.observations)
        ),
        names=['dte', 'prb']
    )

    # make a pandas.Series
    prev = _pandas.Series(
        data=serie.observations['res'].values,
        index=index,
        name='res'
    )

    # make dtprod a datetime
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
        previsions=prev,
        strict=strict
    )


# def simulation_to_hfs():
#     """Not implemented."""
#     raise NotImplementedError()  # TODO


def serie_from_hfs(src, stationhydro=None, begin=None, end=None, strict=True):
    """Retourne une obshydro.Serie a partir d'un fichier HFS.

    La Serie est simplifiee et ne contient que la colonne res.

    Arguments:
        src (str o ou file) = fichier source
        stationhydro (Stationhydro) = par defaut utilise le nom du fichier src
        begin, end (isoformat string) = dates de debut/fin de la plage de
            valeurs a conserver, bornes incluses
        strict (bool, defaut True) = le mode permissif permet de lever le
            controle de validite de la stationhydro

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
    df.res *= 1000

    # if entite is None we use the HFS file name to build a station
    if stationhydro and strict:
        if not isinstance(stationhydro, _sitehydro.Stationhydro):
            raise TypeError('stationhydro is required')
    if not stationhydro:
        stationhydro = _sitehydro.Stationhydro(
            code=None,
            typestation='LIMNI',
            libelle=_os.path.splitext(_os.path.split(src)[-1])[0],
            strict=False
        )

    # skip rows
    df = df[begin:end]
    if df.empty:
        raise ValueError(
            'empty DataFrame, begin or end do not match any value'
        )

    # return
    return _obshydro.Serie(
        entite=stationhydro,
        grandeur='H',
        observations=df,
        strict=strict
    )


# def serie_to_hfs(dst):
#     """Not implemented."""
#     raise NotImplementedError()  # TODO

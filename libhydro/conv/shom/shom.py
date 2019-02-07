# coding: utf-8
"""Module shom.

Ce module contient des convertisseurs pour les fichiers de predictions
de marees du SHOM:
    simulation_from_hfs()
    simulation_from_h10()

On peut aussi manipuler ces donnees comme des observations simplifiees a
l'aide des fonctions suivantes:
    serie_from_hfs()
    serie_from_h10()

Format des fichiers HFS:
    # fichier texte, séparateur espace
    # horodatage TU, pas de temps constant
    # une ligne par donnée au format "yyyy-mm-dd hh:mm:ss xx.xx"
    # hauteurs en mètres. Se référer au descriptif du port fourni
        par le SHOM pour déterminer la réference altimétrique

Format des fichiers H10:
    # fichier texte, séparateur espace
    # horodatage TU+1, pas de temps constant
    # une ligne par jour, chaque ligne contenant 147 colonnes:
          année YYYY
          code station SHOM (numérique)
          jour de l'année de 1 à 365 (probablement 366)
          144 mesures de H en cm au pas de temps 10 min
    # hauteurs en centimètres. Se référer au descriptif du port fourni
        par le SHOM pour déterminer la réference altimétrique

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import os as _os
import datetime

import pandas as _pandas
import numpy as _numpy

from ...core import (
    sitehydro as _sitehydro, modeleprevision as _modeleprevision,
    obshydro as _obshydro, simulation as _simulation)

# -- strings ------------------------------------------------------------------
# version = 0.4.0
# date = 2018-12-11

# HISTORY
# V0.4 - 2018-12-07
#   ajout du décodeur h10
# V0.3 - 2017-05-17
#   les prévisions du SHOM sont considérées comme des prévisons de tendance
#   afin que le résultat se trouve dans la balise <ResMoyPrev>
# V0.2 - 2014-09-25
#   configure and update the code model
#   fix conversion to mm
# V0.1 - 2013-08-01
#   first shot


# -- functions ----------------------------------------------------------------
def simulation_from_hfs(src, codemodeleprevision, station=None, begin=None, end=None,
                        dtprod=None, strict=True):
    """Retourne une simulation.Simulation a partir d'un fichier HFS.

    Arguments:
        src (str ou file) = fichier source
        codemodeleprevision (str <= 10) = code du modèle de prévision
        station (Station) = par defaut utilise le nom du fichier src
        begin, end (isoformat string) = dates de debut/fin de la plage de
            valeurs a conserver, bornes incluses
        dtprod (string ou datetime) = date de production
        strict (bool, defaut True) = le mode permissif permet de lever le
            controle de validite de la station

    """
    # TODO - rather slow, 15s to load a complete 4 years file in a simulation
    #    from DVD (5s for the Serie, which is quite good). Could we use
    #    skiprows and nrows read_table options to be more efficient ?
    serie = serie_from_hfs(
        src=src, station=station, begin=begin, end=end, strict=strict)
    return _simulation_from_all(
        serie=serie, codemodeleprevision=codemodeleprevision, dtprod=dtprod,
        strict=strict)


def serie_from_hfs(src, station=None, begin=None, end=None, strict=True):
    """Retourne une obshydro.Serie a partir d'un fichier HFS.

    La Serie est simplifiee et ne contient que la colonne res.

    Arguments:
        src (str ou file) = fichier source
        station (Station) = par defaut utilise le nom du fichier src
        begin, end (isoformat string) = dates de debut/fin de la plage de
            valeurs a conserver, bornes incluses
        strict (bool, defaut True) = le mode permissif permet de lever le
            controle de validite de la station

    """
    # parse file
    dataframe = _pandas.read_table(
        src, header=None, delim_whitespace=True, parse_dates=[[0, 1]],
        engine='c', index_col=0, names=['date', 'heure', 'res'])

    # update the DataFrame
    dataframe.index.name = 'dte'
    dataframe.res *= 1000  # m to mm

    # return
    return _serie_from_all(
        src=src, station=station, begin=begin, end=end, strict=strict,
        observations=dataframe)


def simulation_from_h10(src, codemodeleprevision, station=None, begin=None, end=None,
                        dtprod=None, strict=True):
    """Retourne une simulation.Simulation a partir d'un fichier H10.

    Arguments:
        src (str ou file) = fichier source
        codemodeleprevision (str <= 10) = code du modèle de prévision
        station (Station) = par defaut utilise le nom du fichier src
        begin, end (isoformat string) = dates de debut/fin de la plage de
            valeurs a conserver, bornes incluses
        dtprod (string ou datetime) = date de production
        strict (bool, defaut True) = le mode permissif permet de lever le
            controle de validite de la station

    """
    serie = serie_from_h10(
        src=src, station=station, begin=begin, end=end, strict=strict)
    return _simulation_from_all(
        serie=serie, codemodeleprevision=codemodeleprevision, dtprod=dtprod,
        strict=strict)


def _simulation_from_all(serie, codemodeleprevision, dtprod, strict):
    """Factorisation."""
    # make a multiindex with probability 50 for every value
    index = _pandas.MultiIndex.from_tuples(
        list(zip(serie.observations.index.tolist(),
            ['moy'] * len(serie.observations))),
        names=['dte', 'tend'])

    # make a pandas.Series
    prev = _pandas.Series(
        data=serie.observations['res'].values, index=index, name='res')

    # make dtprod a datetime
    if isinstance(dtprod, str):
        dtprod = _numpy.datetime64(dtprod)

    # return Simulation
    return _simulation.Simulation(
        modeleprevision=_modeleprevision.Modeleprevision(
            code=codemodeleprevision),
        entite=serie.entite, grandeur='H', statut=16, qualite=100,
        public=False, commentaire='data SHOM', dtprod=dtprod,
        previsions_tend=prev, strict=strict)


def serie_from_h10(src, station=None, begin=None, end=None, strict=True):
    """Retourne une obshydro.Serie a partir d'un fichier H10.

    La Serie est simplifiee et ne contient que la colonne res.

    Arguments:
        src (str ou file) = fichier source
        station (Station) = par defaut utilise le nom du fichier src
        begin, end (isoformat string) = dates de debut/fin de la plage de
            valeurs a conserver, bornes incluses
        strict (bool, defaut True) = le mode permissif permet de lever le
            controle de validite de la station

    """
    # read a single column
    def readcol(col):
        dataframe = _pandas.read_csv(
            src, delim_whitespace=True, header=None,
            usecols=[0, 2, 3 + col], names=['year', 'day', 'res'],
            engine='c')
        dataframe['hour'], dataframe['minute'] = divmod(col * 10, 60)
        return dataframe

    # parse the file
    dataframe = _pandas.concat(
        [readcol(col=i) for i in range(144)], ignore_index=True)
    dataframe.index = _pandas.to_datetime(
        10000000 * dataframe.year + 10000 * dataframe.day
        + 100 * dataframe.hour + dataframe.minute,
        format='%Y%j%H%M')
    dataframe.index -= datetime.timedelta(hours=1)  # to TU
    dataframe = dataframe[['res']]

    # update the DataFrame
    dataframe.index.name = 'dte'
    dataframe = dataframe.sort_index()
    dataframe.res *= 10  # cm to mm

    # return
    return _serie_from_all(
        src=src, station=station, begin=begin, end=end, strict=strict,
        observations=dataframe)


def _serie_from_all(src, station, begin, end, strict, observations):
    """Factorisation."""
    # if entite is None we use the file name to build a station
    if station and strict:
        if not isinstance(station, _sitehydro.Station):
            raise TypeError('station is required')
    if not station:
        station = _sitehydro.Station(
            code=None, typestation='LIMNI',
            libelle=_os.path.splitext(_os.path.split(src)[-1])[0],
            strict=False)

    # skip rows
    observations = observations[begin:end]
    if observations.empty:
        raise ValueError(
            'observations is empty, begin or end does not match any value')

    # return
    return _obshydro.Serie(
        entite=station, grandeur='H', observations=observations, strict=strict)

# -*- coding: utf-8 -*-
"""Module shom.

Ce module contient des convertisseurs de et vers les fichiers de predictions
de marees du SHOM:
    simulation_from_hsf()  -- TODO not implemented --
    simulation_to_hsf()  -- TODO not implemented --

On peux aussi manipuler ces donnees comme des observations a l'aide des
fonctions suivantes:
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
from __future__ import unicode_literals, absolute_import, division, print_function

import pandas

try:
    import obshydro
except ImportError:
    from libhydro.core import obshydro


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1a"""
__date__ = """2013-08-01"""

#HISTORY
#V0.1 - 2013-08-01
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - nothing
# FIXME - nothing


#-- functions -----------------------------------------------------------------
def simulation_from_hsf():
    # TODO
    raise NotImplementedError()


def simulation_to_hsf():
    # TODO
    raise NotImplementedError()


def serie_from_hsf(src, begin=None, end=None, entite=None):
    """Retourne une obshydro.Serie a partir d'un fichier hsf.

    Arguments:
        src (str o ou file) = fichier source
        begin, end (datetime) = dates de debut/fin de la plage de valeurs a
            conserver
        entite( Sitehydro, Stationhydro ou Capteur)

    """
    # parse file and update the DataFrame
    df = pandas.read_table(
        src,
        header=None,
        delim_whitespace=True,
        parse_dates=[[0, 1]],
        index_col=0,
        names=['date', 'heure', 'res']
    )
    df.index.name = None
    # return serie
    return obshydro.Serie(
        entite=entite,
        grandeur='H',
        observations=df
    )


def serie_to_hsf(dst):
    # TODO
    raise NotImplementedError()

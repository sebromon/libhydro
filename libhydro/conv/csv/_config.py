# -*- coding: utf-8 -*-
"""Module libhydro.conv.csv._config.

Configuration par defaut du codec CSV.

Cette configuration est basee sur les regles de l"Echange de donnees
d'hydrometrie au format simplifie".

Elle peut etre surchargee pour definir ses propres regles.

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import csv as _csv


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1b"""
__date__ = """2014-12-17"""

#HISTORY¬
 #V0.1 - 2014-12-15¬
 #    first shot¬


#-- DIALECT config ------------------------------------------------------------
# FIXME - check Sandre rule to deal with semi columns in CSV
# CAREFUL, the csv.register_dialect deals only with strings :-( in Python2
DIALECT = {
    'delimiter': b';',
    'doublequote': False,
    'escapechar': b'\\',
    'lineterminator': b'\r\n',
    'quotechar': b'"',
    'quoting': _csv.QUOTE_NONE,
    'skipinitialspace': True,
    'strict': False
}

#-- MAPPING config ------------------------------------------------------------
# TODO - reverse the mapping
#    for python 2.7+ / 3+:
#        inv_map = {v: k for k, v in map.items()}
#    in python2.7+, using map.iteritems() would be more efficient

# SYNTAX: {object: {CSV_header: object_attribute, ...}, ...}
MAPPING = {
    'sitehydro': {
        '<CdSiteHydro>': 'code',  # mandatory
        '<LbSiteHydro>': 'libelle',
        '<TypSiteHydro>': 'typesite',
        '<AltitudeSiteHydro>': None,  # NotImplemented yet
        '<SysAltimetriqueSiteHydro>': None,  # NotImplemented yet
        '<BassinVersantSiteHydro>': None,  # NotImplemented yet
        '<FuseauHoraireSiteHydro>': None,  # NotImplemented yet
        '<CdEuMasseDEau>': None,  # NotImplemented yet
        '<cdZoneHydro>': None,  # NotImplemented yet
        '<CdEntiteHydrographique>': None,  # NotImplemented yet
        '<FLG>': None  # mandatory
    },
    'sitehydro.coord': {
        '<CoordXSiteHydro>': 'x',
        '<CoordYSiteHydro>': 'y',
        '<ProjCoordSiteHydro>': 'proj'
    },
    'station': {
        '<CdStationHydro>': 'code',  # mandatory
        '<LbStationHydro>': 'libelle',
        '<TypStationHydro>': 'typestation',
        '<DtMiseServiceStationHydro>': None,  # NotImplemented yet
        '<DtFermetureStationHydro>': None,  # NotImplemented yetv
        '<CdCommune>': 'commune',
    },
    'station.coord': {
        '<CoordXStationHydro>': 'x',
        '<CoordYStationHydro>': 'y',
        '<ProjCoordStationHydro>': 'proj',
    },
    'sitemeteo': {
        '<CdSiteMeteo>': 'code',  # mandatory
        '<LbSiteMeteo>': 'libelle',
        '<AltitudeSiteMeteo>': None,  # NotImplemented yetv
        '<SysAltimetriqueSiteMeteo>': None,  # NotImplemented yetv
        '<FuseauHoraireSiteMeteo>': None,  # NotImplemented yetv
        '<DtOuvertureSiteMeteo>': None,  # NotImplemented yetv
        '<DtFermSiteMeteo>': None,  # NotImplemented yetv
        '<CdSousSecteurHydro>': None,  # NotImplemented yetv
        '<CdCommune>': 'commune',
    },
    'sitemeteo.coord': {
        '<CoordXSiteMeteo>': 'x',
        '<CoordYSiteMeteo>': 'y',
        '<ProjCoordSiteMeteo>': 'proj',
    },
    'grandeur': {
        '<CdGrdMeteo>': 'typemesure',  # mandatory
        '<DtMiseServiceGrdMeteo>': None,  # NotImplemented yet
        '<DtFermetureServiceGrdMeteo>': None,  # NotImplemented yet
    },

    'obshydro': {},

    # <CdSiteHydro>  # mandatory
    # <CdStationHydro>
    # <GrdSerie>  # mandatory
    # <DtObsHydro>  # mandatory
    # <ResObsHydro>  # mandatory
    # <MethObsHydro>
    # <StatutSerie>
    # '<FLG>': None  # mandatory

    'obsmeteo': {},

    # <CdSiteMeteo>  # mandatory
    # <CdGrdMeteo>  # mandatory
    # <DtObsMeteo>  # mandatory
    # <DureeObsMeteo>
    # <ResObsMeteo>  # mandatory
    # <IndiceQualObsMeteo>
    # <MethObsMeteo>
    # <StatutObsMeteo>
    # '<FLG>': None  # mandatory

}

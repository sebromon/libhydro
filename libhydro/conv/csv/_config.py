# -*- coding: utf-8 -*-
"""Module libhydro.conv.csv._config.

Configuration par defaut du codec CSV.

Cette configuration est basee sVurles regles de l"Echange de donnees
d'hydrometrie au format simplifie".

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
__date__ = """2014-12-16"""

#HISTORY¬
 #V0.1 - 2014-12-15¬
 #    first shot¬


#-- DIALECT config ------------------------------------------------------------
# FIXME - check Sandre rule to deal with semi columns in CSV
# CAREFUL, csv.Dialect values must be strings in Python 2
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

# SYNTAX: {object: {xml_tag: object_attr, ...}, ...}
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
    'stationhydro': {
        '<CdStationHydro>': 'code',
        '<LbStationHydro>': 'libelle',
        '<TypStationHydro>': 'typestation',
        '<DtMiseServiceStationHydro>': None,  # NotImplemented yet
        '<DtFermetureStationHydro>': None,  # NotImplemented yet
        '<CdCommune>': 'commune',
    },
    'stationhydro.coord': {
        '<CoordXStationHydro>': 'x',
        '<CoordYStationHydro>': 'y',
        '<ProjCoordStationHydro>': 'proj',
    },
    'sitemeteo': {},

    # <CdSiteMeteo>  # mandatory
    # <LbSiteMeteo>
    # <CoordXSiteMeteo>
    # <CoordYSiteMeteo>
    # <ProjCoordSiteMeteo>
    # <AltitudeSiteMeteo>
    # <SysAltimetriqueSiteMeteo>
    # <FuseauHoraireSiteMeteo>
    # <DtOuvertureSiteMeteo>
    # <DtFermSiteMeteo>
    # <CdSousSecteurHydro>
    # <CdCommune>

    # <CdGrdMeteo>
    # <DtMiseServiceGrdMeteo>
    # <DtFermetureServiceGrdMeteo>
    # '<FLG>': None  # mandatory

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

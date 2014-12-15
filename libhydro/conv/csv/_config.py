# -*- coding: utf-8 -*-
"""CSV codec defaut config.

Csv.dialect and mapping par defaut pour l"Echange de donnees d'hydrometrie au
format simplifie".

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
__version__ = """0.1a"""
__date__ = """2014-12-15"""

#HISTORY¬
 #V0.1 - 2014-12-15¬
 #    first shot¬

#-- todos ---------------------------------------------------------------------
# TODO - reverse the mapping
#    for python 2.7+ / 3+:
#        inv_map = {v: k for k, v in map.items()}
#    in python2.7+, using map.iteritems() would be more efficient


#-- config --------------------------------------------------------------------
# FIXME - check Sandre rule to deal with semi columns in CSV
# CAREFUL, csv dialect values must be strings in Python 2
DIALECT = {
    'delimiter': b';',
    'doublequote': True,
    # 'escapechar': '\\',
    'lineterminator': b'\r\n',
    'quotechar': b'"',
    'quoting': _csv.QUOTE_NONE,
    'skipinitialspace': True,
    'strict': False
}

# SYNTAX: xml_tag: object_attr
MAPPING = {
    'sitehydro': {
        '<CdSiteHydro>': 'code',  # mandatory
        '<LbSiteHydro>': 'libelle',
        '<TypSiteHydro>': 'typesite',
        '<CoordXSiteHydro>': 'coord.x',
        '<CoordYSiteHydro>': 'coord.y',
        '<ProjCoordSiteHydro>': 'coord.proj',
        '<AltitudeSiteHydro>': None,  # NotImplemented
        '<SysAltimetriqueSiteHydro>': None,  # NotImplemented
        '<BassinVersantSiteHydro>': None,  # NotImplemented
        '<FuseauHoraireSiteHydro>': None,  # NotImplemented
        '<CdEuMasseDEau>': None,  # NotImplemented
        '<cdZoneHydro>': None,  # NotImplemented
        '<CdEntiteHydrographique>': None,  # NotImplemented
        '<FLG>': None  # mandatory
    },
    'stationhydro': {
        '<CdStationHydro>': 'code',
        '<LbStationHydro>': 'libelle',
        '<TypStationHydro>': 'typestation',
        '<CoordXStationHydro>': 'coord.x',
        '<CoordYStationHydro>': 'coord.y',
        '<ProjCoordStationHydro>': 'coord.proj',
        '<DtMiseServiceStationHydro>': None,  # NotImplemented
        '<DtFermetureStationHydro>': None,  # NotImplemented
        '<CdCommune>': 'commune',
        '<FLG>': None  # mandatory
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

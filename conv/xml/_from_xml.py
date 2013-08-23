# -*- coding: utf-8 -*-
"""Module xml.from_xml.

Ce module contient des fonctions de lecture de fichiers au format
Xml Hydrometrie (version 1.1 exclusivement).

Fonctions disponibles:
    (TODO functions listing)

Exemples d'utilisation:
    (TODO examples)

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

# import numpy as _numpy
# from lxml import etree as _etree

from ._scenario import Scenario

from libhydro.core import (
    sitehydro as _sitehydro,
    modeleprevision as _modeleprevision,
    obshydro as _obshydro,
    simulation as _simulation,
    intervenant as _intervenant
)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1c"""
__date__ = """2013-08-23"""

#HISTORY
#V0.1 - 2013-08-18
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - if xpath is too slow to acess elements, use indexing
#        code=element[0].text,
#        but xpath is more readable and do not care of xml order

# TODO - XSD validation


# -- config -------------------------------------------------------------------
PREV_PROBABILITY = {
    'ResMoyPrev': 50,
    'ResMinPrev': 0,
    'ResMaxPrev': 100
}


# -- public functions ---------------------------------------------------------
def get_sitehydro(src, code=None):
    """Fonction get_sitehydro."""

    # # FIXME - probleme avec les namespace

    # parser = _etree.XMLParser(remove_blank_text=True)
    # tree = _etree.parse('test/data/xml/1.1/siteshydro.xml', parser=parser)
    # siteshydro = []
    # for sitehydro in tree.findall('*//SiteHydro'):
    #     siteshydro.append(
    pass


# -- atomic functions ---------------------------------------------------------
def _get_scenario_from_element(element):
    """Return a xml.Scenario from a <Scenario> element."""
    return Scenario(
        emetteur=_intervenant.Contact(
            code=_get_value(element.find('Emetteur'), 'CdContact'),
            intervenant=_intervenant.Intervenant(
                _get_value(element.find('Emetteur'), 'CdIntervenant')
            )
        ),
        destinataire=_intervenant.Intervenant(
            code=_get_value(element.find('Destinataire'), 'CdIntervenant'),
        ),
        dtprod=_get_value('DateHeureCreationfichier')
    )


def _sitehydro_from_element(element):
    """Return a sitehydro.Sitehydro from a <SiteHydro> element."""
    return _sitehydro.Sitehydro(
        code=_get_value(element, 'CdSiteHydro'),
        typesite=_get_value(element, 'TypSiteHydro'),
        libelle=_get_value(element, 'LbSiteHydro'),
        stations=[
            _stationhydro_from_element(e)
            for e in element.findall('StationsHydro/StationHydro')
        ]
    )


def _stationhydro_from_element(element):
    """Return a sitehydro.Stationhydro from a <Stationhydro> element."""
    return _sitehydro.Stationhydro(
        code=_get_value(element, 'CdStationHydro'),
        typestation=_get_value(element, 'TypStationHydro'),
        libelle=_get_value(element, 'LbStationHydro'),
        capteurs=[
            _capteur_from_element(e)
            for e in element.findall('Capteurs/Capteur')
        ]
    )


def _capteur_from_element(element):
    """Return a sitehydro.Capteur from a <Capteur> element."""
    return _sitehydro.Capteur(
        code=_get_value(element, 'CdCapteur'),
        typemesure=_get_value(element, 'TypMesureCapteur'),
        libelle=_get_value(element, 'LbCapteur')
    )


def _serie_from_element(element):
    """Return a obshydro.Serie from a <Serie> element."""
    # entite can be a Sitehydro, a Stationhydro or a Capteur
    entite = None
    if element.find('CdSiteHydro') is not None:
        entite = _sitehydro.Sitehydro(
            code=_get_value(element, 'CdSiteHydro')
        )
    elif element.find('CdStationHydro') is not None:
        entite = _sitehydro.Stationhydro(
            code=_get_value(element, 'CdStationHydro')
        )
    elif element.find('CdCapteur') is not None:
        entite = _sitehydro.Capteur(
            code=_get_value(element, 'CdCapteur')
        )
    # make the Serie
    return _obshydro.Serie(
        entite=entite,
        grandeur=_get_value('GrdSerie'),
        statut=_get_value('StatutSerie'),
        observations=_obshydro.Observations(element.find('ObssHydro'))
    )


def _observations_from_element(element):
    """Return a obshydro.Observations from a <ObssHydro> element."""
    return _obshydro.Observations(
        *[_obshydro.Observation(
            dte=_get_value(o, 'DtObsHydro', _UTC_date),
            res=_get_value(o, 'ResObsHydro'),
            mth=_get_value(o, 'MethObsHydro', int),
            qal=_get_value(o, 'QualifObsHydro', int),
            cnt=_get_value(o, 'ContObsHydro', bool)
        ) for o in element]
    )


def _simulation_from_element(element):
    """Return a simulation.Simulation from a <Simul> element."""
    # entite can be a Sitehydro or a Stationhydro
    entite = None
    if element.find('CdSiteHydro') is not None:
        entite = _sitehydro.Sitehydro(
            code=_get_value(element, 'CdSiteHydro')
        )
    elif element.find('CdStationHydro') is not None:
        entite = _sitehydro.Stationhydro(
            code=_get_value(element, 'CdStationHydro')
        )
    # make the Simulation
    return _simulation.Simulation(
        entite=entite,
        modeleprevision=_modeleprevision.Modeleprevision(
            code=_get_value(element, 'CdModelePrevision')
        ),
        grandeur=_get_value(element, 'GrdSimul'),
        statut=_get_value(element, 'StatutSimul', int),
        qualite=_get_value(element, 'IndicequaliteSimul', int),
        public=_get_value(element, 'PubliSimul', bool),
        commentaire=_get_value(element, 'ComSimul'),
        dtprod=_get_value(element, 'DtProdSimul', _UTC_date),
        previsions=_previsions_from_element(element.find('Prevs'))
    )


def _previsions_from_element(element):
    """Return a simulation.Previsions from a <Prevs> element."""
    previsions = []

    for prev in element:
        dte = _get_value(prev, 'DtPrev', _UTC_date)

        # -------------------
        # compute Res[Min|Moy|Max]Prev
        # -------------------
        # xpath syntax: p.xpath('ResMoyPrev|ResMinPrev|ResMaxPrev')
        for resprev in prev.xpath('|'.join(PREV_PROBABILITY)):
            previsions.append(
                _simulation.Prevision(
                    dte=dte,
                    res=resprev.text,
                    prb=PREV_PROBABILITY[resprev.tag]
                )
            )

        # -------------------
        # compute ProbsPrev
        # -------------------
        for probprev in prev.findall('.//ProbPrev'):
            previsions.append(
                _simulation.Prevision(
                    dte=dte,
                    res=_get_value(probprev, 'PProbPrev', int),
                    prb=_get_value(probprev, 'ResProbPrev', float)
                )
            )

    return _simulation.Previsions(*previsions)


# -- utility functions --------------------------------------------------------
def _UTC_date(dte):
    """Add +00 to the string dte if no time zone."""
    if dte.find('+') == -1:
        return '%s+00' % dte
    else:
        return dte


def _get_value(element, tag, cast=unicode):
    """Return cast(element/tag.text) or None."""
    e = element.find(tag)
    if e is not None:
        return cast(e.text)
    return e

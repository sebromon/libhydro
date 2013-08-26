# -*- coding: utf-8 -*-
"""Module xml._from_xml.

Ce module contient les fonctions de lecture des fichiers au format
Xml Hydrometrie (version 1.1 exclusivement).

Toutes les heures sont considerees UTC si le fuseau horaire n'est pas precise.

Les fonctions de ce module sont a usage prive, il est recommande d'utiliser la
classe xml.Message comme interface aux fichiers Xml Hydrometrie.

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from lxml import etree as _etree

from .xml import Scenario

from libhydro.core import (
    sitehydro as _sitehydro,
    modeleprevision as _modeleprevision,
    obshydro as _obshydro,
    simulation as _simulation,
    intervenant as _intervenant
)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1e"""
__date__ = """2013-08-26"""

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


# -- tests function -----------------------------------------------------------
def _parse(src):
    """Parse le fichier src, instancie et retourne les objets qu'il contient.

    Cette fonction est destinee au tests unitaires. Les utilisateurs sont
    invites a utiliser la classe xml.Message comme interface de lecture des
    fichiers Xml Hydrometrie.

    Arguments:
        src (nom de fichier, url, objet fichier...) = source de donnee. Les
            type de src acceptes sont ceux de lxml.etree.parse

    Retourne un dictionnaire avec les cles:
            # scenario: xml.Scenario
            # siteshydro: liste de sitehydro.Siteshydro ou None
            # series: liste de obshydro.Serie ou None
            # simulation: liste de simulation.Simulation ou None

    """

    # read the file
    parser = _etree.XMLParser(
        remove_blank_text=True, remove_comments=True, ns_clean=True
    )
    tree = _etree.parse(src, parser=parser)

    # deal with namespaces
    # TODO - we could certainly do better with namespaces
    if tree.getroot().nsmap != {}:
        raise ValueError("can't parse xml file with namespaces")

    return {
        'scenario': _scenario_from_element(tree.find('Scenario')),
        # 'intervenants':
        'siteshydro': _siteshydro_from_element(tree.find('RefHyd/SitesHydro')),
        # 'sitesmeteo'
        # 'modelesprevision': 'TODOS',
        # 'evenements'
        # 'courbestarage'
        # 'jaugeages'
        # 'courbescorrection'
        'series': _series_from_element(tree.find('Donnees/Series')),
        # 'obssmeteo'
        # 'obsselab'
        # 'gradshydro'
        # 'qualifsannee'
        'simulations': _simulations_from_element(tree.find('Donnees/Simuls'))
        # 'alarmes'
    }


# -- global functions ---------------------------------------------------------

# TODO - these 3 functions can be factorised

def _siteshydro_from_element(element):
    """Return a list of sitehydro.Sitehydro from a <SitesHydro> element."""
    if element is not None:
        siteshydro = []
        for sitehydro in element.findall('./SiteHydro'):
            siteshydro.append(_sitehydro_from_element(sitehydro))
        return siteshydro


def _series_from_element(element):
    """Return a list of obshydro.Serie from a <Series> element."""
    if element is not None:
        series = []
        for serie in element.findall('./Serie'):
            series.append(_serie_from_element(serie))
        return series


def _simulations_from_element(element):
    """Return a list of simulation.Simulation from a <Simuls> element."""
    if element is not None:
        simuls = []
        for simul in element.findall('./Simul'):
            simuls.append(_simulation_from_element(simul))
        return simuls


# -- atomic functions ---------------------------------------------------------
def _scenario_from_element(element):
    """Return a xml.Scenario from a <Scenario> element."""
    if element is not None:
        return Scenario(
            emetteur=_intervenant.Contact(
                code=_value(element.find('Emetteur'), 'CdContact'),
                intervenant=_intervenant.Intervenant(
                    _value(element.find('Emetteur'), 'CdIntervenant')
                )
            ),
            destinataire=_intervenant.Intervenant(
                code=_value(element.find('Destinataire'), 'CdIntervenant'),
            ),
            dtprod=_value(element, 'DateHeureCreationFichier', _UTC)
        )


def _sitehydro_from_element(element):
    """Return a sitehydro.Sitehydro from a <SiteHydro> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdSiteHydro')
        args['libelle'] = _value(element, 'LbSiteHydro')
        args['stations'] = [
            _stationhydro_from_element(e)
            for e in element.findall('StationsHydro/StationHydro')
        ]
        typesite = _value(element, 'TypSiteHydro')
        if typesite is not None:
            args['typesite'] = typesite
        # build Site
        return _sitehydro.Sitehydro(**args)


def _stationhydro_from_element(element):
    """Return a sitehydro.Stationhydro from a <Stationhydro> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdStationHydro')
        args['libelle'] = _value(element, 'LbStationHydro')
        args['capteurs'] = [
            _capteur_from_element(e)
            for e in element.findall('Capteurs/Capteur')
        ]
        typestation = _value(element, 'TypStationHydro')
        if typestation is not None:
            args['typestation'] = typestation
        # build Station
        return _sitehydro.Stationhydro(**args)


def _capteur_from_element(element):
    """Return a sitehydro.Capteur from a <Capteur> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdCapteur')
        args['libelle'] = _value(element, 'LbCapteur')
        typemesure = _value(element, 'TypMesureCapteur')
        if typemesure is not None:
            args['typemesure'] = typemesure
        # build Capteur
        return _sitehydro.Capteur(**args)


def _serie_from_element(element):
    """Return a obshydro.Serie from a <Serie> element."""
    if element is not None:

        # entite can be a Sitehydro, a Stationhydro or a Capteur
        entite = None
        if element.find('CdSiteHydro') is not None:
            entite = _sitehydro.Sitehydro(
                code=_value(element, 'CdSiteHydro')
            )
        elif element.find('CdStationHydro') is not None:
            entite = _sitehydro.Stationhydro(
                code=_value(element, 'CdStationHydro')
            )
        elif element.find('CdCapteur') is not None:
            entite = _sitehydro.Capteur(
                code=_value(element, 'CdCapteur')
            )

        # make the Serie
        return _obshydro.Serie(
            entite=entite,
            grandeur=_value(element, 'GrdSerie'),
            statut=_value(element, 'StatutSerie'),
            observations=_observations_from_element(element.find('ObssHydro'))
        )


def _observations_from_element(element):
    """Return a obshydro.Observations from a <ObssHydro> element."""
    if element is not None:

        # prepare a list of Observation
        observations = []
        for o in element:
            args = {}
            args['dte'] = _value(o, 'DtObsHydro', _UTC)
            args['res'] = _value(o, 'ResObsHydro')
            mth = _value(o, 'MethObsHydro', int)
            if mth is not None:
                args['mth'] = mth
            qal = _value(o, 'QualifObsHydro', int)
            if qal is not None:
                args['qal'] = qal
            # we can't use bool injection here because bool('False') is True
            cnt = _value(o, 'ContObsHydro')
            if cnt is not None:
                args['cnt'] = True if (cnt == 'True') else False
            observations.append(_obshydro.Observation(**args))

        # build Observations
        return _obshydro.Observations(*observations)


def _simulation_from_element(element):
    """Return a simulation.Simulation from a <Simul> element."""
    if element is not None:
        # entite can be a Sitehydro or a Stationhydro
        entite = None
        if element.find('CdSiteHydro') is not None:
            entite = _sitehydro.Sitehydro(
                code=_value(element, 'CdSiteHydro')
            )
        elif element.find('CdStationHydro') is not None:
            entite = _sitehydro.Stationhydro(
                code=_value(element, 'CdStationHydro')
            )
        # make the Simulation
        return _simulation.Simulation(
            entite=entite,
            modeleprevision=_modeleprevision.Modeleprevision(
                code=_value(element, 'CdModelePrevision')
            ),
            grandeur=_value(element, 'GrdSimul'),
            statut=_value(element, 'StatutSimul', int),
            qualite=int(_value(element, 'IndiceQualiteSimul', float)),  # int(float())
            public=_value(element, 'PubliSimul', bool),
            commentaire=_value(element, 'ComSimul'),
            dtprod=_value(element, 'DtProdSimul', _UTC),
            previsions=_previsions_from_element(element.find('Prevs'))
        )


def _previsions_from_element(element):
    """Return a simulation.Previsions from a <Prevs> element."""
    if element is not None:

        previsions = []
        for prev in element:
            dte = _value(prev, 'DtPrev', _UTC)

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
                        res=_value(probprev, 'ResProbPrev', float),
                        prb=_value(probprev, 'PProbPrev', int)
                    )
                )

        return _simulation.Previsions(*previsions)


# -- utility functions --------------------------------------------------------
def _UTC(dte):
    """Add +00 to the string dte if no time zone."""
    if (dte is not None) and (dte.find('+') == -1):
        return '%s+00' % dte
    else:
        return dte


def _value(element, tag, cast=unicode):
    """Return cast(element/tag.text) or None."""
    e = element.find(tag)
    if e is not None:
        return cast(e.text)
    return e

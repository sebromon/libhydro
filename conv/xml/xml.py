# -*- coding: utf-8 -*-
"""Module xml.

Ce module contient des convertisseurs pour lire le Xml Hydrometrie:
    (liste)

Et pour le generer:
    (liste fonctions)

La version de reference du scenario Xml Hydrometrie est 1.1.

Exemples d'utilisation:
    (todo)

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime
from lxml import etree as _etree

from . import mapping
from libhydro.core import sitehydro as _sitehydro
from libhydro.core import obshydro as _obshydro


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1a"""
__date__ = """2013-08-18"""

#HISTORY
#V0.1 - 2013-08-18
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - if xpath is too slow to acess elements, use indexing:
#    code=element[0].text,
# but xpath is more readable and do not care of xml order

# make 2 modules: to_xml et from_xml ??


# -- class Scenario -----------------------------------------------------------
class Scenario(object):

    # FIXME

    def __init__(self):
        self.code = 'hydrometrie'
        self.version = 1.1
        self.nom = 'Echange de données hydrométriques'
        self.dtfichier = _datetime.datetime.utcnow()

    # <Emetteur><CdIntervenant schemeAgencyID="SANDRE">1537</CdIntervenant>
    #           <CdContact schemeAgencyID="SANDRE">1</CdContact>

        # destinataire = destinataire


#-- functions -----------------------------------------------------------------
def to_xml(scenario, *args):

    # FIXME
    # import ipdb; ipdb.set_trace()

    tree = _etree.Element('hydrometrie')

    # add scenario
    s = _etree.SubElement(tree, 'Scenario')
    for (k, v) in mapping.scenario.iteritems():
        child = _etree.SubElement(s, v)
        child.text = unicode(getattr(scenario, k))

    # add args

    # return
    print(
        _etree.tostring(
            tree, encoding='utf-8', xml_declaration=1,  pretty_print=1
        )
    )
    return tree


# def get_sitehydro(src, code=None):

    # # FIXME - probleme avec les namespace

    # parser = _etree.XMLParser(remove_blank_text=True)
    # tree = _etree.parse('test/data/xml/1.1/siteshydro.xml', parser=parser)
    # siteshydro = []
    # for sitehydro in tree.findall('*//SiteHydro'):
    #     siteshydro.append(
    # pass


def _sitehydro_from_element(element):
    """Return a sitehydro.Sitehydro from a SiteHydro element."""
    return _sitehydro.Sitehydro(
        code=element.find('CdSiteHydro').text,
        typesite=element.find('TypSiteHydro'),
        libelle=element.find('LbSiteHydro').text,
        stations=[
            _stationhydro_from_element(e)
            for e in element.findall('StationsHydro/StationHydro')
        ]
    )


def _stationhydro_from_element(element):
    """Return a sitehydro.Stationhydro from a Stationhydro element."""
    return _sitehydro.Stationhydro(
        code=element.find('CdStationHydro').text,
        typestation=element.find('TypStationHydro'),
        libelle=element.find('LbStationHydro').text,
        capteurs=[
            _capteur_from_element(e)
            for e in element.findall('Capteurs/Capteur')
        ]
    )


def _capteur_from_element(element):
    """Return a sitehydro.Capteur from a Capteur element."""
    return _sitehydro.Capteur(
        code=element.find('CdCapteur').text,
        typemesure=element.find('TypMesureCapteur'),
        libelle=element.find('LbCapteur').text
    )


def _serie_from_element(element):
    """Return a obshydro.Serie from a Serie element."""
    # entite can be a Sitehydro, a Stationhydro or a Capteur
    entite = None
    if element.find('CdSiteHydro'):
        entite = _sitehydro.Sitehydro(
            code=element.find('CdSiteHydro').text
        )
    elif element.find('CdStationHydro'):
        entite = _sitehydro.Stationhydro(
            code=element.find('CdStationHydro').text
        )
    elif element.find('CdCapteur'):
        entite = _sitehydro.Capteur(
            code=element.find('CdCapteur').text
        )
    # get the Serie
    return _obshydro.Serie(
        entite=entite,
        grandeur=element.find('GrdSerie').text,
        statut=element.find('StatutSerie').text,
        observations=_obshydro.Observations(element.find('ObssHydro'))
    )


def _observations_from_element(element):
    """Return a obshydro.Observations for a ObssHydro element."""
    return _obshydro.Observations(
        *[_obshydro.Observation(
            dte=o.find('DtObsHydro').text,
            res=o.find('ResObsHydro').text,
            mth=int(o.find('MethObsHydro').text),
            qal=int(o.find('QualifObsHydro').text),
            cnt=o.find('Cont')  # FIXME - check tag name + pb if None
        ) for o in element]
    )


def _simulation_from_element(element):
    # TODO
    pass

# -*- coding: utf-8 -*-
"""Module xml._to_xml.

Ce module contient les fonctions de generation des fichiers au format
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


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1c"""
__date__ = """2013-08-27"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


#-- todos ---------------------------------------------------------------------
# FIXME - check strict = TRUE when requested


# -- testsfunction ------------------------------------------------------------
def _to_xml(scenario=None, siteshydro=None, series=None, simulations=None):
    """Genere un message Xml a partir des donnees passes en argument.

    Cette fonction est destinee au tests unitaires. Les utilisateurs sont
    invites a utiliser la classe xml.Message comme interface de lecture des
    fichiers Xml Hydrometrie.

    Arguments:
        scenario (xml.Scenario) = 1 element
        sitesydro (sitehydro.Sitehydro collection) = iterable or None
        series (obshydro.Serie collection) = iterable or None
        simulations (simulation.Simulation collection) = iterable or None

    """
    # make a deep copy of locals() which is a dict {arg_name: arg_value, ...}
    args = locals()

    # order matters in Xml, we must have the keys list !
    keys = ('scenario', 'siteshydro', 'series', 'simulations')

    #init the tree and add elements
    tree = _etree.Element('hydrometrie')
    for k in keys:
        if args[k] is not None:
            tree.append(
                eval('_{}_to_element(args[k])'.format(k))
            )

    # DEBUG -
    # print(
    #     _etree.tostring(
    #         tree, encoding='utf-8', xml_declaration=1,  pretty_print=1
    #     )
    # )

    # return
    return tree


# -- global functions ---------------------------------------------------------

# TODO - these 3 functions can be factorised

def _siteshydro_to_element(siteshydro):
    """Return a <SitesHydro> element from a list of sitehydro.Sitehydro."""
    if siteshydro is not None:
        element = _etree.Element('SitesHydro')
        for sitehydro in siteshydro:
            element.append(_sitehydro_to_element(sitehydro))
        return element


def _series_to_element(series):
    """Return a <Series> element from a list of obshydro.Serie."""
    if series is not None:
        element = _etree.Element('Series')
        for serie in series:
            element.append(_serie_to_element(serie))
        return element


def _simulations_to_element(simulations):
    """Return a <Simuls> element from a list of simulation.Simulation."""
    if simulations is not None:
        element = _etree.Element('Simuls')
        for simulation in simulations:
            element.append(_serie_to_element(simulation))
        return element


# -- atomic functions ---------------------------------------------------------
def _scenario_to_element(scenario):
    """Return a <Scenario> element from a xml.Scenario."""

    if scenario is not None:

        # template for scenario simple elements
        story = [
            ('CodeScenario', scenario.code, None),
            ('VersionScenario', scenario.version, None),
            ('NomScenario', scenario.nom, None),
            ('DateHeureCreationFichier', scenario.dtprod.isoformat(), None)
        ]
        # template for scenario sub-element <Emetteur>
        story.append(
            ('Emetteur', (
                ('CdIntervenant',
                 unicode(scenario.emetteur.intervenant.code),
                 {"schemaAgencyID": scenario.emetteur.intervenant.origine}),
                ('CdContact',
                 unicode(scenario.emetteur.code),
                 {"schemaAgencyID": "SANDRE"})
            ))
        )
        # template for scenario sub-element <Destinataire>
        story.append(
            ('Destinataire', (
                ('CdIntervenant',
                 unicode(scenario.destinataire.code),
                 {"schemaAgencyID": "SANDRE"}),
            ))
        )

        # action !
        return _factory(root=_etree.Element('Scenario'), story=story)


def _sitehydro_to_element(sitehydro):
    """Return a <SiteHydro> element from a sitehydro.Sitehydro."""

    if sitehydro is not None:

        # template for sitehydro simple elements
        story = [
            ('CdSiteHydro', sitehydro.code, None),
            ('LbSiteHydro', sitehydro.libelle, None),
            ('TypSiteHydro', sitehydro.typesite, None)
        ]

        # make element <SiteHydro>
        element = _factory(root=_etree.Element('SiteHydro'), story=story)

        # add the stations
        if sitehydro.stations is not None:
            child = _etree.SubElement(element, 'StationsHydro')
            for station in sitehydro.stations:
                child.append(_stationhydro_to_element(station))

        # return
        return element


def _stationhydro_to_element(stationhydro):
    """Return a <StationHydro> element from a sitehydro.Stationhydro."""

    if stationhydro is not None:

        # template for stationhydro simple elements
        story = [
            ('CdStationHydro', stationhydro.code, None),
            ('LbStationHydro', stationhydro.libelle, None),
            ('TypStationHydro', stationhydro.typestation, None)
        ]

        # make element <StationHydro>
        element = _factory(root=_etree.Element('StationHydro'), story=story)

        # add the capteurs
        if stationhydro.capteurs is not None:
            child = _etree.SubElement(element, 'Capteurs')
            for capteur in stationhydro.capteurs:
                child.append(_capteur_to_element(capteur))

        # return
        return element


def _capteur_to_element(capteur):
    """Return a <Capteur> element from a sitehydro.Capteur."""

    if capteur is not None:

        # capteur simple elements
        story = [
            ('CdCapteur', capteur.code, None),
            ('LbCapteur', capteur.libelle, None),
            ('TypMesureCapteur', capteur.typemesure, None)
        ]

        # action !
        return _factory(root=_etree.Element('Capteur'), story=story)


def _serie_to_element(serie):
    """Return a <Serie> element from a obshydro.Serie."""

    if serie is not None:

        # template for serie simple elements
        story = [
            (
                # Entite can be a Sitehydro, a Stationhydro or a Capteur
                'Cd%s' % (
                    serie.entite.__class__.__name__.replace('hydro', 'Hydro')
                ),
                serie.entite.code,
                None
            ),
            ('GrdSerie', serie.grandeur, None),
            ('StatutSerie', unicode(serie.statut), None),
        ]

        # make element <Serie>
        element = _factory(root=_etree.Element('Serie'), story=story)

        # add the observations
        if serie.observations is not None:
            element.append(_observations_to_element(serie.observations))

        # return
        return element


def _observations_to_element(observations):
    """Return a <ObssHydro> element from a obshydro.Observations."""

    if observations is not None:

        # make element <ObssHydro>
        element = _etree.Element('ObssHydro')

        # add the observations - iterrows gives tuples (index, (items))
        for observation in observations.iterrows():
            obs = _etree.SubElement(element, 'ObsHydro')
            # dte and res are mandatory...
            child = _etree.SubElement(obs, 'DtObsHydro')
            child.text = observation[0].isoformat()
            child = _etree.SubElement(obs, 'ResObsHydro')
            child.text = unicode(observation[1]['res'])
            # while mth, qal and cnt aren't
            if 'mth' in observation[1].index:
                child = _etree.SubElement(obs, 'MethObsHydro')
                child.text = unicode(observation[1]['mth'])
            if 'qal' in observation[1].index:
                child = _etree.SubElement(obs, 'QualifObsHydro')
                child.text = unicode(observation[1]['qal'])
            if 'cnt' in observation[1].index:
                child = _etree.SubElement(obs, 'ContObsHydro')
                child.text = unicode(observation[1]['cnt'])

        # return
        return element


def _simulation_to_element(simulation):
    # TODO
    pass


def _previsions_to_element(previsions):
    # TODO
    pass


# -- utility functions --------------------------------------------------------
def _factory(root, story):
        """Add to <root> element tags or sub-elements described in story.

        Syntax:
            # for an element => (tag_name, text, {tag_attributes}) - len is 3
            # for a sub-element => (sub_element_tag, (story)) - len is 2

        """
        # parse story
        for rule in story:
            # DEBUG - print(rule)
            # recursif cal for sub-element
            if len(rule) == 2:
                child = _etree.SubElement(root, rule[0])
                root.append(
                    _factory(root=child, story=rule[1])
                )
            #element
            elif len(rule) == 3:
                tag, text, attrib = rule
                if text is not None:
                    root.append(
                        _make_element(
                            tag_name=tag,
                            text=text,
                            tag_attrib=attrib)
                    )
            # error
            else:
                raise TypeError('bad rule {{%s}}' % rule)

        # return
        return root


def _make_element(tag_name, text, tag_attrib=None):
    """Return etree.Element <tag_name {attrib}>cast(text)</tag_name>."""
    # DEBUG - print(locals())
    if text is not None:
        element = _etree.Element(_tag=tag_name, attrib=tag_attrib)
        element.text = text
        return element

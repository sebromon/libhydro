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

from collections import OrderedDict as _OrderedDict

from lxml import etree as _etree
import numpy as _numpy


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1g"""
__date__ = """2014-02-25"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


#-- todos ---------------------------------------------------------------------
# FIXME - check strict = TRUE when requested


# -- config -------------------------------------------------------------------
# order matters in Xml, we must have the keys list !
ORDERED_ACCEPTED_KEYS = (
    'scenario', 'siteshydro', 'evenements', 'series', 'simulations'
)

PREV_PROBABILITY = {
    50: 'ResMoyPrev',
    0: 'ResMinPrev',
    100: 'ResMaxPrev'
}


# -- testsfunction ------------------------------------------------------------
def _to_xml(
    scenario=None, siteshydro=None,
    evenements=None, series=None, simulations=None
):
    """Return a etree.Element a partir des donnees passes en argument.

    Cette fonction est privee et les utilisateurs sont invites a utiliser la
    classe xml.Message comme interface d'ecriture des fichiers Xml Hydrometrie.

    Arguments:
        scenario (xml.Scenario) = 1 element
        sitesydro (sitehydro.Sitehydro collection) = iterable or None
        evenements (evenement.Evenement collection) = iterable ou None
        series (obshydro.Serie collection) = iterable or None
        simulations (simulation.Simulation collection) = iterable or None

    """
    # make a deep copy of locals() which is a dict {arg_name: arg_value, ...}
    args = locals()

    # init the tree
    tree = _etree.Element('hydrometrie')

    # TODO - we should factorise those lines

    # add the scenario
    if args['scenario'] is not None:
        tree.append(_scenario_to_element(args['scenario']))

    # add the siteshydro
    if args['siteshydro'] is not None:
        sub = _etree.SubElement(tree, 'RefHyd')
        for k in ORDERED_ACCEPTED_KEYS[1:2]:
            if args[k] is not None:
                sub.append(
                    eval('_{}_to_element(args[k])'.format(k))
                )

    # add the donnees
    if (
        (args['evenements'] is not None)
        or (args['series'] is not None)
        or (args['simulations'] is not None)
    ):
        sub = _etree.SubElement(tree, 'Donnees')
        for k in ('evenements', 'series', 'simulations'):
            if args[k] is not None:
                sub.append(
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


def _evenements_to_element(evenements):
    """Return a <Evenements> element from a list of evenement.Evenement."""
    if evenements is not None:
        element = _etree.Element('Evenements')
        for evenement in evenements:
            element.append(_evenement_to_element(evenement))
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
            element.append(_simulation_to_element(simulation))
        return element


# -- atomic functions ---------------------------------------------------------
def _scenario_to_element(scenario):
    """Return a <Scenario> element from a xml.Scenario."""

    if scenario is not None:

        # template for scenario simple element
        story = _OrderedDict((
            ('CodeScenario', {'value': scenario.code}),
            ('VersionScenario', {'value': scenario.version}),
            ('NomScenario', {'value': scenario.nom}),
            ('DateHeureCreationFichier',
                {'value': scenario.dtprod.isoformat()})
        ))
        # template for scenario sub-element <Emetteur>
        story['Emetteur'] = {
            'sub': _OrderedDict((
                ('CdIntervenant', {
                    'value': unicode(scenario.emetteur.intervenant.code),
                    'attr': {"schemeAgencyID":
                             scenario.emetteur.intervenant.origine}
                }),
                ('CdContact', {
                    'value': unicode(scenario.emetteur.code),
                    'attr': {"schemeAgencyID": "SANDRE"}  # FIXME -  wrong ?
                })
            ))
        }
        # template for scenario sub-element <Destinataire>
        story['Destinataire'] = {
            'sub': {
                'CdIntervenant': {
                    'value': unicode(scenario.destinataire.code),
                    'attr': {"schemeAgencyID":
                             scenario.emetteur.intervenant.origine}
                }
            }
        }

        # action !
        return _factory(root=_etree.Element('Scenario'), story=story)


def _sitehydro_to_element(sitehydro):
    """Return a <SiteHydro> element from a sitehydro.Sitehydro."""

    if sitehydro is not None:

        # template for sitehydro simple elements
        story = _OrderedDict((
            ('CdSiteHydro', {'value': sitehydro.code}),
            ('LbSiteHydro', {'value': sitehydro.libelle}),
            ('LbUsuelSiteHydro', {'value': sitehydro.libelleusuel}),
            ('TypSiteHydro', {'value': sitehydro.typesite}),
            ('CoordSiteHydro', {
                'value': None,
                'force': True if sitehydro.coord is not None else False
            }),
            ('CdCommune', {'value': sitehydro.communes}),
            ('CdSiteHydroAncienRef', {'value': sitehydro.codeh2}),
            ('StationsHydro', {
                'value': None,
                'force': True if (len(sitehydro.stations) > 0) else False
            })
        ))

        # update the coord if necessary
        if sitehydro.coord is not None:
            story['CoordSiteHydro'] = {
                'sub': _OrderedDict((
                    ('CoordXSiteHydro', {'value': sitehydro.coord.x}),
                    ('CoordYSiteHydro', {'value': sitehydro.coord.y}),
                    ('ProjCoordSiteHydro', {'value': sitehydro.coord.proj})
                ))
            }

        # make element <SiteHydro>
        element = _factory(root=_etree.Element('SiteHydro'), story=story)

        # add the stations if necessary
        if len(sitehydro.stations) > 0:
            child = element.find('StationsHydro')
            for station in sitehydro.stations:
                child.append(_stationhydro_to_element(station))

        # return
        return element


def _stationhydro_to_element(stationhydro):
    """Return a <StationHydro> element from a sitehydro.Stationhydro."""

    if stationhydro is not None:

        # template for stationhydro simple element
        story = _OrderedDict((
            ('CdStationHydro', {'value': stationhydro.code}),
            ('LbStationHydro', {'value': stationhydro.libelle}),
            ('TypStationHydro', {'value': stationhydro.typestation}),
            ('ComplementLibelleStationHydro', {
                'value': stationhydro.libellecomplement
            }),
            ('CoordStationHydro', {
                'value': None,
                'force': True if stationhydro.coord is not None else False
            }),
            ('NiveauAffichageStationHydro', {
                'value': stationhydro.niveauaffichage
            }),
            ('ReseauxMesureStationHydro', {
                'value': None,
                'force': True if (len(stationhydro.ddcs) > 0) else False
            }),
            ('Capteurs', {
                'value': None,
                'force': True if (len(stationhydro.capteurs) > 0) else False
            }),
            ('CdStationHydroAncienRef', {'value': stationhydro.codeh2}),
            ('CdCommune', {'value': stationhydro.commune})
        ))

        # update the coord if necessary
        if stationhydro.coord is not None:
            story['CoordStationHydro'] = {
                'sub': _OrderedDict((
                    ('CoordXStationHydro', {'value': stationhydro.coord.x}),
                    ('CoordYStationHydro', {'value': stationhydro.coord.y}),
                    ('ProjCoordStationHydro',
                        {'value': stationhydro.coord.proj})
                ))
            }

        # update ddcs if necessary
        if len(stationhydro.ddcs) > 0:
            story['ReseauxMesureStationHydro'] = {
                'sub': {
                    'CodeSandreRdd': {'value': stationhydro.ddcs}
                }
            }

        # make element <StationHydro>
        element = _factory(root=_etree.Element('StationHydro'), story=story)

        # add the capteurs if necessary
        if len(stationhydro.capteurs) > 0:
            child = element.find('Capteurs')
            for capteur in stationhydro.capteurs:
                child.append(_capteur_to_element(capteur))

        # return
        return element


def _capteur_to_element(capteur):
    """Return a <Capteur> element from a sitehydro.Capteur."""

    if capteur is not None:

        # template for capteur simple element
        story = _OrderedDict((
            ('CdCapteur', {'value': capteur.code}),
            ('LbCapteur', {'value': capteur.libelle}),
            ('TypMesureCapteur', {'value': capteur.typemesure}),
            ('CdCapteurAncienRef', {'value': capteur.codeh2})
        ))

        # action !
        return _factory(root=_etree.Element('Capteur'), story=story)


def _evenement_to_element(evenement):
    """Return a <Evenement> element from a evenement.Evenement."""

    if evenement is not None:

        # template for serie simple elements
        story = _OrderedDict()
        story['CdContact'] = {'value': evenement.contact.code}
        # entite can be a Sitehydro, a Stationhydro
        # TODO - or a Sitemeteo
        story['Cd%s' % evenement.entite.__class__.__name__.replace(
            'hydro', 'Hydro')] = {'value': evenement.entite.code}
        # suite
        story['DtEvenement'] = {'value': evenement.dt.isoformat()}
        story['DescEvenement'] = {'value': evenement.descriptif}
        story['TypPublicationEvenement'] = {'value': evenement.publication}
        story['DtMajEvenement'] = {'value': evenement.dtmaj.isoformat()}

        # action !
        return _factory(root=_etree.Element('Evenement'), story=story)


def _serie_to_element(serie):
    """Return a <Serie> element from a obshydro.Serie."""

    if serie is not None:

        # template for serie simple elements
        story = _OrderedDict()
        # entite can be a Sitehydro, a Stationhydro or a Capteur
        story['Cd%s' % serie.entite.__class__.__name__.replace(
            'hydro', 'Hydro')] = {'value': serie.entite.code}
        # suite
        story['GrdSerie'] = {'value': serie.grandeur}
        story['DtDebSerie'] = {'value': serie.dtdeb.isoformat()}
        story['DtFinSerie'] = {'value': serie.dtfin.isoformat()}
        story['StatutSerie'] = {'value': unicode(serie.statut)}
        story['DtProdSerie'] = {'value': serie.dtprod.isoformat()}

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
                child.text = unicode(observation[1]['cnt']).lower()

        # return
        return element


def _simulation_to_element(simulation):
    """Return a <Simul> element from a simulation.Simulation."""

    if simulation is not None:

        # template for simulation simple element
        story = _OrderedDict((
            ('GrdSimul', {'value': simulation.grandeur}),
            # dtprod is a numpy.datetime64 without any isoformat method
            ('DtProdSimul', {'value': simulation.dtprod.isoformat()}),
            ('IndiceQualiteSimul', {'value': unicode(simulation.qualite)}),
            ('StatutSimul', {'value': unicode(simulation.statut)}),
            ('PubliSimul', {'value': unicode(simulation.public).lower()}),
            ('ComSimul', {'value': simulation.commentaire})
        ))
        # entite can be a Sitehydro or a Stationhydro
        story['Cd%s' % simulation.entite.__class__.__name__.replace(
            'hydro', 'Hydro')] = {'value': simulation.entite.code}
        # suite
        story['CdModelePrevision'] = {'value': simulation.modeleprevision.code}
        story['CdIntervenant'] = {
            'value': unicode(simulation.intervenant.code),
            'attr': {"schemeAgencyID": simulation.intervenant.origine}
        }

        # make element <Simul>
        element = _factory(root=_etree.Element('Simul'), story=story)

        # add the previsions
        if simulation.previsions is not None:
            element.append(_previsions_to_element(simulation.previsions))

        # return
        return element


def _previsions_to_element(previsions):
    """Return a <Prevs> element from a simulation.Previsions."""

    # this one is very VERY painful #:~/

    if previsions is not None:

        # make element <Prevs>
        element = _etree.Element('Prevs')

        # iter by date and add the previsions
        for dte in previsions.index.levels[0].values:
            prev_elem = _etree.SubElement(element, 'Prev')
            # dte is mandatory...
            prev_elem.append(
                _make_element(
                    tag_name='DtPrev',
                    # dte is a numpy.datetime64 with perhaps nanoseconds
                    # it is better to cast it before getting the isoformat
                    text=_numpy.datetime64(dte, 's').item().isoformat()
                )
            )
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # for one date we can have multiple values
            # we put all of them in a dict {prb: res, ...}
            # so that we can pop them on by one
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            prevs = previsions[dte].to_dict()

            # we begin to deal with the direct tags...
            # order matters: moy, min and max !!
            for prob in (50, 0, 100):
                if prob in prevs:
                    prev_elem.append(
                        _make_element(
                            tag_name=PREV_PROBABILITY[prob],
                            text=prevs.pop(prob)
                        )
                    )
            # ... and then with the remaining <ProbPrev> elements
            if len(prevs) > 0:
                probsprev_elem = _etree.SubElement(prev_elem, 'ProbsPrev')
                # we sort the result by prob ascending order
                probs = prevs.keys()
                probs.sort()
                # add elems
                for prob in probs:
                    probprev_elem = _etree.SubElement(
                        probsprev_elem, 'ProbPrev'
                    )
                    probprev_elem.append(
                        _make_element(
                            tag_name='PProbPrev',
                            text=prob
                        )
                    )
                    probprev_elem.append(
                        _make_element(
                            tag_name='ResProbPrev',
                            text=prevs.pop(prob)
                        )
                    )

        # return
        return element


# -- utility functions --------------------------------------------------------
def _factory(root, story):
    """Return the <root> element including elements described in story.

    Story is a dictionnary which keys are the xml tags to create and values
    one of the possible 2 forms:

        1./ Rule to create a sub-element (recursif)
        -------------------------------------------
        This rule is processed like:
            {'sub': a sub-story dictionnary}

        2./ Rule to create a single element or a serie of the same element
        ------------------------------------------------------------------
        This rule is processed like:
            {
                'value': the text value or an iterable of text values,
                'attr': {the tag attributes} (default None)
                'force': bool (default False)
            }

        If value is a list or a tuple, an xml tag is created for each
        item of values.

        When force is True, a None value create the element tag, otherwise
        rule is left.

    WARNING: as order matters for Xml Hydrometrie files, one must use
             collections.OrderedDict to store the story.

    """
    # parse story
    for tag, rule in story.iteritems():

        # DEBUG - print(rule)

        # recursif call for sub-element
        if 'sub' in rule:
            child = _etree.SubElement(root, tag)
            root.append(
                _factory(root=child, story=rule.get('sub'))
            )

        # single element or multi elements
        if 'value' in rule:

            # init
            value = rule.get('value')
            attr = rule.get('attr', None)
            force = rule.get('force', False)

            # empty tag
            if (value is None) and (not force):
                continue

            # for a simple tag, we make a list
            if not isinstance(value, (list, tuple)):
                value = [value]

            # finally we create a tag for each item in the list
            for text in value:
                root.append(
                    _make_element(
                        tag_name=tag,
                        text=text,
                        tag_attrib=attr)
                )

    # return
    return root


def _make_element(tag_name, text, tag_attrib=None):
    """Return etree.Element <tag_name {attrib}>unicode(text)</tag_name>."""
    # DEBUG - print(locals())
    element = _etree.Element(_tag=tag_name, attrib=tag_attrib)
    if text is not None:
        element.text = unicode(text)
    return element

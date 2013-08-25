# -*- coding: utf-8 -*-
"""Module xml.to_xml.

Ce module contient des convertisseurs vers le format
Xml Hydrometrie (version 1.1 exclusivement).

Fonctions disponibles:
    (TODO)

Exemples d'utilisation:
    (TODO)

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
__version__ = """version 0.1b"""
__date__ = """2013-08-25"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


#-- todos ---------------------------------------------------------------------
# FIXME - check strict = TRUE when requested


#-- public functions ----------------------------------------------------------
def to_xml_file(dst, scenario, *args):
    """Fonction to_xm_file.

    Arguments:
        dst ** TODO **
        scenario (xml.Scenario) = requested
        sitesydro (sitehydro.Sitehydro collection)
        obsshydro ** TODO **
        simulations ** TODO **

    """

    tree = _etree.Element('hydrometrie')

    # add scenario

    # add args

    # DEBUG -
    print(
        _etree.tostring(
            tree, encoding='utf-8', xml_declaration=1,  pretty_print=1
        )
    )

    # return
    return tree


# -- global functions ---------------------------------------------------------
def _siteshydro_to_element(siteshydro):
    # TODO
    pass


def _series_to_element(series):
    # TODO
    pass


def _simulations_to_element(simulations):
    # TODO
    pass


# -- atomic functions ---------------------------------------------------------
def _scenario_to_element(scenario):
    """Return a <Scenario> element from a xml.Scenario."""

    if scenario is not None:

        # scenario elements
        SCENARIO = [
            ('CodeScenario', scenario.code, None),
            ('VersionScenario', scenario.version, None),
            ('NomScenario', scenario.nom, None),
            ('DateHeureCreationFichier', scenario.dtprod.isoformat(), None)
        ]
        # scenario sub-element Emetteur
        SCENARIO.append(
            ('Emetteur', (
                ('CdIntervenant',
                 unicode(scenario.emetteur.intervenant.code),
                 {"schemaAgencyID": scenario.emetteur.intervenant.origine}),
                ('CdContact',
                 unicode(scenario.emetteur.code),
                 {"schemaAgencyID": "SANDRE"})
            ))
        )
        # scenario sub-element Destinataire
        SCENARIO.append(
            ('Destinataire', (
                ('CdIntervenant',
                 unicode(scenario.destinataire.code),
                 {"schemaAgencyID": "SANDRE"}),
            ))
        )

        # action !
        return _factory(root=_etree.Element('Scenario'), story=SCENARIO)


def _sitehydro_to_element(sitehydro):
    # TODO
    pass


def _stationhydro_to_element(stationhydro):
    # TODO
    pass


def _capteur_to_element(capteur):
    # TODO
    pass


def _serie_to_element(serie):
    # TODO
    pass


def _observations_to_element(observations):
    # TODO
    pass


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
            # for an element => (tag, attribute, {tag_attributes}) - len is 3
            # for a sub-element => (sub_element_tag, (story)) - len is 2

        """
        # parse story
        for rule in story:
            # DEBUG - print(rule)
            # sub-element
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

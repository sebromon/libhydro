# -*- coding: utf-8 -*-
"""Module xml._to_xml.

Ce module contient les fonctions de generation des fichiers au format
XML Hydrometrie (version 1.1 exclusivement).

Toutes les heures sont considerees UTC si le fuseau horaire n'est pas precise.

Les fonctions de ce module sont a usage prive, il est recommande d'utiliser la
classe xml.Message comme interface aux fichiers XML Hydrometrie.

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import collections as _collections

import numpy as _numpy
from lxml import etree as _etree
import math as _math

from libhydro.core import (
    _composant,
    sitehydro as _sitehydro,
    sitemeteo as _sitemeteo,
    seuil as _seuil
)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.4f"""
__date__ = """2015-04-21"""

# HISTORY
# V0.4 - 2014-07-31
#   factorize the global functions
#   replace isoformat() by strftime()
#   add the to_xml.bdhydro argument
#   add the modelesprevision element
#   add the required function
# V0.3 - 2014-07-25
#   add the sitesmeteo and seriesmeteo elements
# V0.1 - 2013-08-20
#   first shot

# -- todos --------------------------------------------------------------------
# TODO - required could be a decorator

# -- config -------------------------------------------------------------------
# order matters in XML, we must have the keys list !
ORDERED_ACCEPTED_KEYS = [
    'scenario',
    # line 140: [1:6]
    'intervenants', 'siteshydro', 'sitesmeteo',
    'seuilshydro', 'modelesprevision',
    # line 180: [6:]
    'evenements', 'serieshydro', 'seriesmeteo', 'simulations'
]

PREV_PROBABILITY = {
    50: 'ResMoyPrev',
    0: 'ResMinPrev',
    100: 'ResMaxPrev'
}

# some tags mappings
CLS_MAPPINGS = {
    _sitehydro.Sitehydro: 'SiteHydro',
    _sitehydro.Station: 'StationHydro',
    _sitehydro.Capteur: 'Capteur',
    _sitemeteo.Sitemeteo: 'SiteMeteo',
    _sitemeteo.Grandeur: 'Grandeur'
}

# sandre hydrometrie namespaces
NS = (
    'http://xml.sandre.eaufrance.fr/scenario/hydrometrie/1.1',
    'http://www.w3.org/2001/XMLSchema-instance'
)
NS_ATTR = {
    'xmlns': NS[0],
    '{%s}schemaLocation' % NS[1]: '%s %s/sandre_sc_hydrometrie.xsd' % (
        NS[0], NS[0]
    )
}


# -- testsfunction ------------------------------------------------------------
def _to_xml(scenario=None, intervenants=None, siteshydro=None, sitesmeteo=None,
            seuilshydro=None, modelesprevision=None, evenements=None,
            serieshydro=None, seriesmeteo=None, simulations=None,
            bdhydro=False, strict=True, ordered=False):
    """Return a etree.Element a partir des donnees passes en argument.

    Cette fonction est privee et les utilisateurs sont invites a utiliser la
    classe xml.Message comme interface d'ecriture des fichiers XML Hydrometrie.

    Arguments:
        scenario (xml.Scenario) = 1 element
        intervenants (intervenant.Intervenant collection) = iterable or None
        siteshydro (sitehydro.Sitehydro collection) = iterable or None
        sitesmeteo (sitemeteo.Sitemeteo collection) = iterable or None
        seuilshydro (seuil.Seuilhydro collection) = iterable or None
        modelesprevision (modeleprevision.Modeleprevision collection) =
            iterable or None
        evenements (evenement.Evenement collection) = iterable ou None
        serieshydro (obshydro.Serie collection) = iterable or None
        seriesmeteo (obsmeteo.Serie collection) = iterable or None
        simulations (simulation.Simulation collection) = iterable or None
        bdhydro (bool, defaut False) = controle de conformite bdhydro
        strict (bool, defaut True) = controle de conformite XML Hydrometrie
        ordered (bool, default False) = essaie de conserver l'ordre de certains
            elements

    """
    # make a deep copy of locals() which is a dict {arg_name: arg_value, ...}
    # keep only Message items
    # and replace default empty lists with None
    args = {
        k: (v if v != [] else None) for k, v in locals().iteritems()
        if k in ORDERED_ACCEPTED_KEYS
    }

    # init the tree
    if bdhydro:
        tree = _etree.Element('hydrometrie')
    else:
        tree = _etree.Element('hydrometrie', attrib=NS_ATTR)

    # TODO - this is awful :/ we should factorize those lines

    # add the scenario
    if args['scenario'] is not None:
        tree.append(
            _scenario_to_element(
                args['scenario'], bdhydro=bdhydro, strict=strict
            )
        )

    # add the referentiel
    items = ORDERED_ACCEPTED_KEYS[1:6]
    choice = len(
        [args[i] for i in items if args[i] is not None]
    ) > 0
    if choice:
        sub = _etree.SubElement(tree, 'RefHyd')

        # intervenants
        if args['intervenants'] is not None:
            sub.append(_intervenants_to_element(
                args['intervenants'], bdhydro=bdhydro, strict=strict)
            )

        # siteshydro and seuilshydro
        if (args['siteshydro'], args['seuilshydro']) != (None, None):
            # we add the common SitesHydro tag and we remove it from
            # each element because seuilshydro are childs of siteshydro
            subsiteshydro = _etree.SubElement(sub, 'SitesHydro')
            if args['siteshydro'] is not None:
                element = _siteshydro_to_element(
                    args['siteshydro'], bdhydro=bdhydro, strict=strict
                )
                for elementsitehydro in element.findall('./SiteHydro'):
                    subsiteshydro.append(elementsitehydro)
            if args['seuilshydro'] is not None:
                element = _seuilshydro_to_element(
                    seuilshydro=args['seuilshydro'],
                    ordered=ordered,
                    bdhydro=bdhydro,
                    strict=strict
                )
                for elementsitehydro in element.findall('./SiteHydro'):
                    subsiteshydro.append(elementsitehydro)

        # sitesmeteo
        if args['sitesmeteo'] is not None:
            sub.append(_sitesmeteo_to_element(
                args['sitesmeteo'], bdhydro=bdhydro, strict=strict)
            )

        # modelesprevision
        if args['modelesprevision'] is not None:
            sub.append(_modelesprevision_to_element(
                args['modelesprevision'], bdhydro=bdhydro, strict=strict)
            )

    # add the datas
    items = ORDERED_ACCEPTED_KEYS[6:]
    choice = len(
        [args[i] for i in items if args[i] is not None]
    ) > 0
    if choice:
        sub = _etree.SubElement(tree, 'Donnees')
        for k in items:
            if args[k] is not None:
                sub.append(
                    eval(
                        '_{0}_to_element(args[k], '
                        'bdhydro={1}, strict={2})'.format(
                            k, bdhydro, strict
                        )
                    )
                )

    # DEBUG -
    # print(
    #     _etree.tostring(
    #         tree, encoding='utf-8', xml_declaration=1,  pretty_print=1
    #     )
    # )

    # return
    return tree


# -- atomic functions ---------------------------------------------------------
def _scenario_to_element(scenario, bdhydro=False, strict=True):
    """Return a <Scenario> element from a xml.Scenario."""

    # FIXME - we should check the scenario name <NomScenario>

    if scenario is not None:

        # prerequisites
        _required(scenario, ['dtprod', 'emetteur', 'destinataire'])
        if strict:
            _required(scenario, ['code', 'version'])
        if bdhydro:
            _required(scenario.emetteur, ['contact'])
            _required(scenario.emetteur.contact, ['code'])

        # template for scenario simple element
        story = _collections.OrderedDict((
            ('CodeScenario', {'value': scenario.code}),
            ('VersionScenario', {'value': scenario.version}),
            ('NomScenario', {'value': scenario.nom}),
            ('DateHeureCreationFichier',
                {'value': scenario.dtprod.strftime('%Y-%m-%dT%H:%M:%S')})
        ))
        # template for scenario sub-elements <Emetteur> and <Destinataire>
        for tag in ('Emetteur', 'Destinataire'):
            item = getattr(scenario, tag.lower())
            story[tag] = {
                'sub': _collections.OrderedDict((
                    ('CdIntervenant', {
                        'value': unicode(item.intervenant.code),
                        'attr': {'schemeAgencyID': item.intervenant.origine}
                    }),
                    ('NomIntervenant', {
                        'value': unicode(item.intervenant.nom)
                        if item.intervenant.nom is not None else None
                    }),
                    ('CdContact', {
                        'value': unicode(item.contact.code)
                        if (
                            (item.contact is not None) and
                            (item.contact.code is not None)
                        ) else None,
                        # bdhydro requires a junk attr for the contacts
                        'attr': {'schemeAgencyID': 'SANDRE'}
                        if bdhydro else None
                    })
                ))
            }

        # action !
        return _factory(root=_etree.Element('Scenario'), story=story)


def _intervenant_to_element(intervenant, bdhydro=False, strict=True):
    """Return a <Intervenant> element from a intervenant.Intervenant."""

    if intervenant is not None:

        # prerequisites
        if strict:
            _required(intervenant, ['code'])

        # template for intervenant simple elements
        story = _collections.OrderedDict((
            ('CdIntervenant', {
                'value': unicode(intervenant.code),
                'attr': {'schemeAgencyID': intervenant.origine}
            }),
            ('NomIntervenant', {'value': intervenant.nom}),
            ('MnIntervenant', {'value': intervenant.mnemo}),
            ('Contacts', {
                'value': None,
                'force': True if (len(intervenant.contacts) > 0) else False
            })
        ))

        # make element <Intervenant>
        element = _factory(root=_etree.Element('Intervenant'), story=story)

        # add the contacts if necessary
        if len(intervenant.contacts) > 0:
            child = element.find('Contacts')
            for contact in intervenant.contacts:
                child.append(
                    _contact_to_element(
                        contact, bdhydro=bdhydro, strict=strict
                    )
                )

        # return
        return element


def _contact_to_element(contact, bdhydro=False, strict=True):
    """Return a <Contact> element from a intervenant.Contact."""

    if contact is not None:

        # prerequisite
        if strict:
            _required(contact, ['code'])

        # template for contact simple elements
        story = _collections.OrderedDict((
            # FIXME - this tag can be factorize
            ('CdContact', {
                'value': contact.code
                if (
                    (contact is not None) and
                    (contact.code is not None)
                ) else None,
                # bdhydro requires a junk attr for the contacts
                'attr': {'schemeAgencyID': 'SANDRE'}
                if bdhydro else None
            }),
            ('NomContact', {'value': contact.nom}),
            ('PrenomContact', {'value': contact.prenom}),
            ('CiviliteContact', {'value': contact.civilite}),
        ))

        # make element <Contact> and return
        return _factory(root=_etree.Element('Contact'), story=story)


def _sitehydro_to_element(sitehydro, seuilshydro=None,
                          bdhydro=False, strict=True):
    """Return a <SiteHydro> element from a sitehydro.Sitehydro.

    Args:
        sitehydro (sitehydro.Sitehydro)
        seuilshydro (an iterable of seuil.Seuilhydro) = the seuilshydro
            belonging to the sitehydro. They are added to the sub tag
            <ValeursSeuilsSiteHydro>

    """

    if sitehydro is not None:

        if seuilshydro is None:
            seuilshydro = []

        # prerequisites
        if strict:
            _required(sitehydro, ['code'])

        # template for sitehydro simple elements
        story = _collections.OrderedDict((
            ('CdSiteHydro', {'value': sitehydro.code}),
            ('LbSiteHydro', {'value': sitehydro.libelle}),
            ('LbUsuelSiteHydro', {'value': sitehydro.libelleusuel}),
            ('TypSiteHydro', {'value': sitehydro.typesite}),
            ('CoordSiteHydro', {
                'value': None,
                'force': True if sitehydro.coord is not None else False
            }),
            ('TronconsVigilanceSiteHydro', {
                'value': None,
                'force': True if (
                    len(sitehydro.tronconsvigilance) > 0
                ) else False
            }),
            ('CdCommune', {'value': sitehydro.communes}),
            ('CdSiteHydroAncienRef', {'value': sitehydro.codeh2}),
            ('StationsHydro', {
                'value': None,
                'force': True if (len(sitehydro.stations) > 0) else False
            }),
            ('ValeursSeuilsSiteHydro', {
                'value': None,
                'force': True if (len(seuilshydro) > 0) else False
            })
        ))

        # update the coord if necessary
        if sitehydro.coord is not None:
            story['CoordSiteHydro'] = {
                'sub': _collections.OrderedDict((
                    ('CoordXSiteHydro', {'value': sitehydro.coord.x}),
                    ('CoordYSiteHydro', {'value': sitehydro.coord.y}),
                    ('ProjCoordSiteHydro', {'value': sitehydro.coord.proj})
                ))
            }

        # make element <SiteHydro>
        element = _factory(root=_etree.Element('SiteHydro'), story=story)

        # add the tronconsvigilance if necessary
        if len(sitehydro.tronconsvigilance) > 0:
            child = element.find('TronconsVigilanceSiteHydro')
            for tronconvigilance in sitehydro.tronconsvigilance:
                child.append(
                    _tronconvigilance_to_element(
                        tronconvigilance, strict=strict
                    )
                )

        # add the stations if necessary
        if len(sitehydro.stations) > 0:
            child = element.find('StationsHydro')
            for station in sitehydro.stations:
                child.append(
                    _station_to_element(
                        station, bdhydro=bdhydro, strict=strict
                    )
                )

        # add the seuils if necessary
        if len(seuilshydro) > 0:
            child = element.find('ValeursSeuilsSiteHydro')
            for seuilhydro in seuilshydro:
                child.append(_seuilhydro_to_element(seuilhydro, strict=strict))

        # return
        return element


def _sitemeteo_to_element(sitemeteo, bdhydro=False, strict=True):
    """Return a <SiteMeteo> element from a sitemeteo.Sitemeteo."""

    if sitemeteo is not None:

        # prerequisites
        if strict:
            _required(sitemeteo, ['code'])

        # template for sitemeteo simple elements
        story = _collections.OrderedDict((
            ('CdSiteMeteo', {'value': sitemeteo.code}),
            ('LbSiteMeteo', {'value': sitemeteo.libelle}),
            ('LbUsuelSiteMeteo', {'value': sitemeteo.libelleusuel}),
            ('CoordSiteMeteo', {
                'value': None,
                'force': True if sitemeteo.coord is not None else False
            }),
            ('CdCommune', {'value': sitemeteo.commune}),
            ('GrdsMeteo', {
                'value': None,
                'force': True if (len(sitemeteo.grandeurs) > 0) else False
            })
        ))

        # update the coord if necessary
        if sitemeteo.coord is not None:
            story['CoordSiteMeteo'] = {
                'sub': _collections.OrderedDict((
                    ('CoordXSiteMeteo', {'value': sitemeteo.coord.x}),
                    ('CoordYSiteMeteo', {'value': sitemeteo.coord.y}),
                    ('ProjCoordSiteMeteo', {'value': sitemeteo.coord.proj})
                ))
            }

        # make element <Sitemeteo>
        element = _factory(root=_etree.Element('SiteMeteo'), story=story)

        # add the grandeurs if necessary
        if len(sitemeteo.grandeurs) > 0:
            child = element.find('GrdsMeteo')
            for grandeur in sitemeteo.grandeurs:
                child.append(_grandeur_to_element(grandeur, strict=strict))

        # return
        return element


def _tronconvigilance_to_element(tronconvigilance, bdhydro=False, strict=True):
    """Return a <TronconVigilanceSiteHydro> element from a """
    """sitehydro.Tronconvigilance."""
    if tronconvigilance is not None:

        # prerequisites
        if strict:
            _required(tronconvigilance, ['code'])

        # template for tronconvigilance simple elements
        story = _collections.OrderedDict((
            ('CdTronconVigilance', {'value': tronconvigilance.code}),
            ('NomCTronconVigilance', {'value': tronconvigilance.libelle})
        ))

        # action !
        return _factory(
            root=_etree.Element('TronconVigilanceSiteHydro'), story=story
        )


def _seuilhydro_to_element(seuilhydro, bdhydro=False, strict=True):
    """Return a <ValeursSeuilSiteHydro> element from a seuil.Seuilhydro."""
    if seuilhydro is not None:

        # prerequisites
        if strict:
            _required(seuilhydro, ['code'])

        # extract the unique Valeurseuil for the site
        sitevaleurseuil = [
            valeur for valeur in seuilhydro.valeurs
            if isinstance(valeur.entite, _sitehydro.Sitehydro)
        ]
        if len(sitevaleurseuil) > 1:
            raise ValueError(
                'more than one site valeurseuil for seuil %s' % seuilhydro.code
            )
        elif len(sitevaleurseuil) == 1:
            sitevaleurseuil = sitevaleurseuil[0]
            seuilhydro.valeurs.remove(sitevaleurseuil)
        else:
            sitevaleurseuil = None

        # template for seuilhydro simple element
        story = _collections.OrderedDict((
            ('CdSeuilSiteHydro', {'value': seuilhydro.code}),
            ('TypSeuilSiteHydro', {'value': seuilhydro.typeseuil}),
            ('NatureSeuilSiteHydro', {'value': seuilhydro.nature}),
            ('DureeSeuilSiteHydro', {'value': seuilhydro.duree}),
            ('LbUsuelSeuilSiteHydro', {'value': seuilhydro.libelle}),
            ('MnemoSeuilSiteHydro', {'value': seuilhydro.mnemo}),
            ('DroitPublicationSeuilSiteHydro', {
                'value': unicode(seuilhydro.publication).lower() if
                seuilhydro.publication is not None else None
            }),
            ('IndiceGraviteSeuilSiteHydro', {'value': seuilhydro.gravite}),
            ('ValForceeSeuilSiteHydro', {
                'value': unicode(seuilhydro.valeurforcee).lower()
                if seuilhydro.valeurforcee is not None else None
            }),
            ('ComSeuilSiteHydro', {'value': seuilhydro.commentaire})
        ))

        # add site values
        if sitevaleurseuil is not None:
            story['ValDebitSeuilSiteHydro'] = {
                'value': sitevaleurseuil.valeur
            }
            story['DtActivationSeuilSiteHydro'] = {
                'value': sitevaleurseuil.dtactivation.strftime(
                    '%Y-%m-%dT%H:%M:%S'
                )
                if sitevaleurseuil.dtactivation is not None else None
            }
            story['DtDesactivationSeuilSiteHydro'] = {
                'value': sitevaleurseuil.dtdesactivation.strftime(
                    '%Y-%m-%dT%H:%M:%S'
                )
                if sitevaleurseuil.dtdesactivation is not None else None
            }

        # add the stations values
        if len(seuilhydro.valeurs) > 0:
            story['ValeursSeuilsStationHydro'] = {'value': None, 'force': True}

        # add the last tags, in disorder :)
        if sitevaleurseuil is not None:
            story['ToleranceSeuilSiteHydro'] = {
                'value': sitevaleurseuil.tolerance
            }
        story['DtMajSeuilSiteHydro'] = {
            'value': seuilhydro.dtmaj.strftime('%Y-%m-%dT%H:%M:%S')
            if seuilhydro.dtmaj is not None else None
        }

        # make element <ValeursSeuilsStationHydro>
        element = _factory(
            root=_etree.Element('ValeursSeuilSiteHydro'),
            story=story
        )

        # add the <ValeursSeuilsStationHydro> if necessary
        if len(seuilhydro.valeurs) > 0:
            child = element.find('ValeursSeuilsStationHydro')
            for valeur in seuilhydro.valeurs:
                child.append(
                    _valeurseuilstation_to_element(valeur, strict=strict)
                )

        # return
        return element


def _valeurseuilstation_to_element(valeurseuil, bdhydro=False,
                                   strict=True):
    """Return a <ValeursSeuilStationHydro> element from a seuil.Valeurseuil.

    Requires valeurseuil.entite.code to be a station hydro code.

    """
    if valeurseuil is not None:

        # prerequisites
        if strict:
            _required(valeurseuil, ['entite', 'valeur'])
            _required(valeurseuil.entite, ['code'])

        # prerequisite
        if not _composant.is_code_hydro(
            code=valeurseuil.entite.code, length=10, errors='ignore'
        ):
            raise TypeError(
                'valeurseuil.entite is not a sitehydro.Station'
            )

        # template for valeurseuilstation simple element
        story = _collections.OrderedDict((
            ('CdStationHydro', {'value': valeurseuil.entite.code}),
            ('ValHauteurSeuilStationHydro', {
                'value': valeurseuil.valeur
            }),
            ('DtActivationSeuilStationHydro', {
                'value': valeurseuil.dtactivation.strftime('%Y-%m-%dT%H:%M:%S')
                if valeurseuil.dtactivation is not None else None
            }),
            ('DtDesactivationSeuilStationHydro', {
                'value': valeurseuil.dtdesactivation.strftime(
                    '%Y-%m-%dT%H:%M:%S'
                )
                if valeurseuil.dtdesactivation is not None else None
            }),
            ('ToleranceSeuilStationHydro', {'value': valeurseuil.tolerance})
        ))

        # action !
        return _factory(
            root=_etree.Element('ValeursSeuilStationHydro'), story=story
        )


def _station_to_element(station, bdhydro=False, strict=True):
    """Return a <StationHydro> element from a sitehydro.Station."""

    if station is not None:

        # prerequisites
        if strict:
            _required(station, ['code'])

        # template for station simple element
        story = _collections.OrderedDict((
            ('CdStationHydro', {'value': station.code}),
            ('LbStationHydro', {'value': station.libelle}),
            ('TypStationHydro', {'value': station.typestation}),
            ('ComplementLibelleStationHydro', {
                'value': station.libellecomplement
            }),
            ('CoordStationHydro', {
                'value': None,
                'force': True if station.coord is not None else False
            }),
            ('NiveauAffichageStationHydro', {
                'value': station.niveauaffichage
            }),
            ('ReseauxMesureStationHydro', {
                'value': None,
                'force': True if (len(station.ddcs) > 0) else False
            }),
            ('Capteurs', {
                'value': None,
                'force': True if (len(station.capteurs) > 0) else False
            }),
            ('CdStationHydroAncienRef', {'value': station.codeh2}),
            ('CdCommune', {'value': station.commune})
        ))

        # update the coord if necessary
        if station.coord is not None:
            story['CoordStationHydro'] = {
                'sub': _collections.OrderedDict((
                    ('CoordXStationHydro', {'value': station.coord.x}),
                    ('CoordYStationHydro', {'value': station.coord.y}),
                    ('ProjCoordStationHydro',
                        {'value': station.coord.proj})
                ))
            }

        # update ddcs if necessary
        if len(station.ddcs) > 0:
            story['ReseauxMesureStationHydro'] = {
                'sub': {
                    'CodeSandreRdd': {'value': station.ddcs}
                }
            }

        # make element <StationHydro>
        element = _factory(root=_etree.Element('StationHydro'), story=story)

        # add the capteurs if necessary
        if len(station.capteurs) > 0:
            child = element.find('Capteurs')
            for capteur in station.capteurs:
                child.append(
                    _capteur_to_element(
                        capteur, bdhydro=bdhydro, strict=strict
                    )
                )

        # return
        return element


def _capteur_to_element(capteur, bdhydro=False, strict=True):
    """Return a <Capteur> element from a sitehydro.Capteur."""

    if capteur is not None:

        # prerequisites
        if strict:
            _required(capteur, ['code'])
        if bdhydro:
            _required(capteur, ['libelle'])

        # template for capteur simple element
        story = _collections.OrderedDict((
            ('CdCapteur', {'value': capteur.code}),
            ('LbCapteur', {'value': capteur.libelle}),
            ('TypMesureCapteur', {'value': capteur.typemesure}),
            ('CdCapteurAncienRef', {'value': capteur.codeh2})
        ))

        # action !
        return _factory(root=_etree.Element('Capteur'), story=story)


def _grandeur_to_element(grandeur, bdhydro=False, strict=True):
    """Return a <GrdMeteo> element from a sitehydro.grandeur."""

    if grandeur is not None:

        # prerequisites
        if strict:
            _required(grandeur, ['typemesure'])

        # template for grandeur simple element
        story = _collections.OrderedDict((
            ('CdGrdMeteo', {'value': grandeur.typemesure}),
        ))

        # action !
        return _factory(root=_etree.Element('GrdMeteo'), story=story)


def _modeleprevision_to_element(modeleprevision, bdhydro=False, strict=True):
    """Return a <ModelePrevision> element from a """
    """modeleprevision.Modeleprevision."""

    if modeleprevision is not None:

        # prerequisite
        if strict:
            _required(modeleprevision, ['code'])

        # template for modeleprevision simple elements
        story = _collections.OrderedDict((
            ('CdModelePrevision', {'value': modeleprevision.code}),
            ('LbModelePrevision', {'value': modeleprevision.libelle}),
            ('TypModelePrevision', {'value': modeleprevision.typemodele}),
            ('DescModelePrevision', {'value': modeleprevision.description}),
        ))

        # make element <modeleprevision> and return
        return _factory(root=_etree.Element('ModelePrevision'), story=story)


def _evenement_to_element(evenement, bdhydro=False, strict=True):
    """Return a <Evenement> element from a evenement.Evenement."""

    if evenement is not None:

        # prerequisite
        _required(evenement, ['contact', 'entite', 'dt'])
        if strict:
            _required(evenement.contact, ['code'])
            _required(evenement.entite, ['code'])
            _required(evenement, ['descriptif'])

        # template for serie simple elements
        story = _collections.OrderedDict()
        story['CdContact'] = {'value': evenement.contact.code}
        # entite can be a Sitehydro, a Station or a Sitemeteo
        story['Cd{}'.format(CLS_MAPPINGS[evenement.entite.__class__])] = {
            'value': evenement.entite.code
        }
        # suite
        story['DtEvenement'] = {
            'value': evenement.dt.strftime('%Y-%m-%dT%H:%M:%S')
        }
        story['DescEvenement'] = {'value': evenement.descriptif}
        story['TypPublicationEvenement'] = {'value': evenement.publication}
        story['DtMajEvenement'] = {
            'value': None if evenement.dtmaj is None
            else evenement.dtmaj.strftime('%Y-%m-%dT%H:%M:%S')
        }

        # action !
        return _factory(root=_etree.Element('Evenement'), story=story)


def _seriehydro_to_element(seriehydro, bdhydro=False, strict=True):
    """Return a <Serie> element from a obshydro.Serie."""

    if seriehydro is not None:

        # prerequisite
        _required(seriehydro, ['entite', 'dtdeb', 'dtfin', 'dtprod'])
        if strict:
            _required(seriehydro.entite, ['code'])
            _required(seriehydro, ['grandeur', 'statut'])

        # template for seriehydro simple elements
        story = _collections.OrderedDict()
        # entite can be a Sitehydro, a Station or a Capteur
        story['Cd{}'.format(CLS_MAPPINGS[seriehydro.entite.__class__])] = {
            'value': seriehydro.entite.code
        }
        # suite
        story['GrdSerie'] = {'value': seriehydro.grandeur}
        story['DtDebSerie'] = {
            'value': seriehydro.dtdeb.strftime('%Y-%m-%dT%H:%M:%S')
        }
        story['DtFinSerie'] = {
            'value': seriehydro.dtfin.strftime('%Y-%m-%dT%H:%M:%S')
        }
        story['StatutSerie'] = {'value': unicode(seriehydro.statut)}
        story['DtProdSerie'] = {
            'value': seriehydro.dtprod.strftime('%Y-%m-%dT%H:%M:%S')
        }
        story['CdContact'] = {
            'value': getattr(
                getattr(seriehydro, 'contact', None),
                'code',
                None
            )
        }

        # make element <Serie>
        element = _factory(root=_etree.Element('Serie'), story=story)

        # add the observations
        if seriehydro.observations is not None:
            element.append(_observations_to_element(seriehydro.observations))

        # return
        return element


def _observations_to_element(observations, bdhydro=False, strict=True):
    """Return a <ObssHydro> element from a obshydro.Observations."""

    if observations is not None:

        # make element <ObssHydro>
        element = _etree.Element('ObssHydro')

        # add the observations - iterrows gives tuples (index, (items))
        for observation in observations.iterrows():
            obs = _etree.SubElement(element, 'ObsHydro')
            # dte and res are mandatory...
            child = _etree.SubElement(obs, 'DtObsHydro')
            child.text = observation[0].strftime('%Y-%m-%dT%H:%M:%S')
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


def _obsmeteo_to_element(seriemeteo, index, obs, bdhydro=False, strict=True):
    """Return a <ObsMeteo> element from a obsmeteo.serie and a observation."""

    if (seriemeteo is not None) and (index is not None) and (obs is not None):

        # prerequisite
        _required(seriemeteo, ['grandeur', 'dtprod', 'duree'])
        _required(seriemeteo.grandeur, ['sitemeteo'])
        if strict:
            _required(seriemeteo.grandeur.sitemeteo, ['code'])
            _required(seriemeteo, ['statut'])  # contact is also mandatory

        # template for seriemeteo simple elements
        story = _collections.OrderedDict()
        story['CdGrdMeteo'] = {'value': seriemeteo.grandeur.typemesure}
        story['CdSiteMeteo'] = {'value': seriemeteo.grandeur.sitemeteo.code}
        story['DtProdObsMeteo'] = {
            'value': seriemeteo.dtprod.strftime('%Y-%m-%dT%H:%M:%S')
        }
        story['DtObsMeteo'] = {'value': index.strftime('%Y-%m-%dT%H:%M:%S')}
        story['StatutObsMeteo'] = {'value': seriemeteo.statut}
        story['ResObsMeteo'] = {'value': obs.res}
        if bdhydro:
            story['DureeObsMeteo'] = {
                'value': int(seriemeteo.duree.total_seconds() / 60)
            }
        else:
            story['DureeObsMeteo'] = {
                'value': None if (seriemeteo.duree.total_seconds() == 0)
                else int(seriemeteo.duree.total_seconds() / 60)
            }
        story['IndiceQualObsMeteo'] = {
            'value': None if _math.isnan(obs.qua) else int(obs.qua)
        }
        if obs.qal is not None:
            story['QualifObsMeteo'] = {'value': int(obs.qal)}
        if obs.mth is not None:
            story['MethObsMeteo'] = {'value': int(obs.mth)}
        story['CdContact'] = {
            'value': getattr(
                getattr(seriemeteo, 'contact', None),
                'code',
                None
            )
        }

        # make element <Serie>
        element = _factory(root=_etree.Element('ObsMeteo'), story=story)

        # return
        return element


def _simulation_to_element(simulation, bdhydro=False, strict=True):
    """Return a <Simul> element from a simulation.Simulation."""

    if simulation is not None:

        # prerequisite
        _required(
            simulation, ['dtprod', 'entite', 'intervenant', 'modeleprevision']
        )
        if strict:
            _required(simulation.entite, ['code'])
            _required(simulation, ['grandeur'])
            _required(simulation.modeleprevision, ['code'])
            _required(simulation.intervenant, ['code'])
        if bdhydro:
            _required(simulation, ['statut'])

        # template for simulation simple element
        story = _collections.OrderedDict((
            ('GrdSimul', {'value': simulation.grandeur}),
            ('DtProdSimul', {
                'value': simulation.dtprod.strftime('%Y-%m-%dT%H:%M:%S')
            }),
            ('IndiceQualiteSimul', {
                'value': unicode(simulation.qualite)
                if simulation.qualite is not None else None
            }),
            ('StatutSimul', {
                'value': unicode(simulation.statut)
                if simulation.statut is not None else None
            }),
            ('PubliSimul', {
                'value': unicode(simulation.public).lower()
                if simulation.public is not None else 'false'
            }),
            ('ComSimul', {'value': simulation.commentaire})
        ))
        # entite can be a Sitehydro or a Station
        story['Cd{}'.format(CLS_MAPPINGS[simulation.entite.__class__])] = {
            'value': simulation.entite.code
        }
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
            element.append(
                _previsions_to_element(simulation.previsions, strict=strict)
            )

        # return
        return element


# -- global functions ---------------------------------------------------------
def _global_function_builder(tag, func):
    """Return a function that returns an etree.Element 'tag' with
    func(item) children for each item in a items list.

    Arguments:
        tag  (str) = the parent etree.Element tag name
        func (str) = elementary function name to call

    """
    def closure(items, bdhydro=False, strict=True):
        """Items should be a list of item objects."""
        if items is not None:
            element = _etree.Element(tag)
            for item in items:
                element.append(
                    func(item, bdhydro=bdhydro, strict=strict)
                )
            return element
    return closure

# return a <Intervenants> element from a list of intervenant.Intervenants
_intervenants_to_element = _global_function_builder(
    'Intervenants', _intervenant_to_element
)
# return a <SitesHydro> element from a list of sitehydro.Sitehydro
_siteshydro_to_element = _global_function_builder(
    'SitesHydro', _sitehydro_to_element
)
# return a <SitesMeteo> element from a list of sitemeteo.Sitemeteo
_sitesmeteo_to_element = _global_function_builder(
    'SitesMeteo', _sitemeteo_to_element
)
# return a <ModelesPrevision> element from a list of Modeleprevision
_modelesprevision_to_element = _global_function_builder(
    'ModelesPrevision', _modeleprevision_to_element
)
# return a <Evenements> element from a list of evenement.Evenement
_evenements_to_element = _global_function_builder(
    'Evenements', _evenement_to_element
)
# return a <Series> element from a list of obshydro.Serie
_serieshydro_to_element = _global_function_builder(
    'Series', _seriehydro_to_element
)
# return a <Simuls> element from a list of simulation.Simulation
_simulations_to_element = _global_function_builder(
    'Simuls', _simulation_to_element
)


# these 3 functions doesn't fit with the _global_function_builder :-\
def _seriesmeteo_to_element(seriesmeteo, bdhydro=False, strict=True):
    """Return a <ObssMeteo> element from a list of obsmeteo.Serie."""
    if seriesmeteo is not None:
        element = _etree.Element('ObssMeteo')
        for serie in seriesmeteo:
            for row in serie.observations.iterrows():
                element.append(
                    _obsmeteo_to_element(
                        serie, *row, bdhydro=bdhydro, strict=strict
                    )
                )
        return element


def _seuilshydro_to_element(seuilshydro, ordered=False,
                            bdhydro=False, strict=True):
    """Return a <SitesHydro> element from a list of seuil.Seuilhydro."""
    if seuilshydro is not None:
        # the ugly XML doesn't support many Q values within a seuil
        # to deal with that use case, we have to split the values on
        # duplicates seuils
        newseuils = []
        for seuilhydro in seuilshydro:
            if seuilhydro.valeurs is not None:
                valeurs_site = [
                    valeur for valeur in seuilhydro.valeurs
                    if (valeur.entite == seuilhydro.sitehydro)
                ]
                if len(valeurs_site) > 1:
                    for valeur in valeurs_site[1:]:
                        # for each value except the first one, we make a new
                        # Seuilhydro with the same code and a uniq value
                        seuil = _seuil.Seuilhydro(
                            sitehydro=seuilhydro.sitehydro,
                            code=seuilhydro.code,
                            valeurs=[valeur]
                        )
                        newseuils.append(seuil)
                        # then we remove the value from the initial iterable
                        seuilhydro.valeurs.remove(valeur)
        seuilshydro.extend(newseuils)

        # now we group the seuilshydro by Sitehydro, putting them into a dict:
        #     {sitehydro: [seuilhydro, ...], ...}
        if ordered:
            siteshydro = _collections.OrderedDict()
        else:
            siteshydro = {}
        for seuilhydro in seuilshydro:
            siteshydro.setdefault(seuilhydro.sitehydro, []).append(seuilhydro)

        # make the elements
        element = _etree.Element('SitesHydro')
        for sitehydro in siteshydro:
            element.append(
                _sitehydro_to_element(
                    sitehydro=sitehydro,
                    seuilshydro=siteshydro[sitehydro],
                    strict=strict
                )
            )
        return element


def _previsions_to_element(previsions, bdhydro=False, strict=True):
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
                    text=_numpy.datetime64(dte, 's').item().strftime(
                        '%Y-%m-%dT%H:%M:%S'
                    )
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

    Story is a dictionnary which keys are the XML tags to create and values
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

        If value is an iterable, an XML tag is created for each item of values.

        When force is True, a None value create the element tag, otherwise
        rule is left.

    WARNING: as order matters for XML Hydrometrie files, one must use
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


def _required(obj, attrs):
    """Raise an exception if an attribute is missing or None.

    Arguments:
        obj = the object to test
        attrs (list of strings) = the list of attributes

    """
    for attr in attrs:
        try:
            if getattr(obj, attr) is None:
                raise ValueError()
        except Exception:
            raise ValueError(
                'attribute {attr} is requested with a value other '
                'than None for object {obj}'.format(
                    attr=attr,
                    obj=unicode(obj)
                )
            )
    return True

# coding: utf-8
"""Module xml._to_xml.

Ce module contient les fonctions de generation des fichiers au format
XML Hydrometrie (version 1.1 exclusivement).

Toutes les heures sont considerees UTC si le fuseau horaire n'est pas precise.

Les fonctions de ce module sont a usage prive, il est recommande d'utiliser la
classe xml.Message comme interface aux fichiers XML Hydrometrie.

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import collections as _collections
import math as _math

from lxml import etree as _etree
import numpy as _numpy

from libhydro.core import (
    _composant, sitehydro as _sitehydro, sitemeteo as _sitemeteo,
    seuil as _seuil, courbetarage as _courbetarage,
    obsmeteo as _obsmeteo, nomenclature as _nomenclature,
    intervenant as _intervenant)

from libhydro.conv.xml import sandre_tags as _sandre_tags

# -- strings ------------------------------------------------------------------
# contributor Sébastien ROMON
__version__ = '0.6.5'
__date__ = '2017-09-29'

# HISTORY
# SR - 2017-09-29 use itertuples intsead of iterrows
# SR - 2017-09- 25 export type capteur to xml
# V0.6.5 - SR- 2017-09-22
# export entitehydro, tronconhydro, zonehydro
# and precisioncoursdeau of site to xml
# V0.6.4 - SR- 2017-09-19
# export pdt of grandeur
# V0.6.3 - SR- 2017-09-05
# export plages d'utilisatin of station and capteur to xml
# V0.6.2 - SR- 2017-07-18
# export some properties of station to xml
# V0.6.1 - SR - 2017-07-05
# export jaugeages
# V0.6 - SR - 2017-06-20
# export des courbes de correction
# V0.5 - SR - 2017-06-20
# export CourbeTarage
# V0.4.9 - SR - 2017-06-09
# export sysalti and perim Serie properties
# V0.4.8
# export des prévisons de tendance puis des prévisions probabilistes
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
    # line 140: [1:7]
    'intervenants', 'siteshydro', 'sitesmeteo',
    'seuilshydro', 'seuilsmeteo', 'modelesprevision',
    # line 180: [7:]
    'evenements', 'courbestarage', 'jaugeages', 'courbescorrection',
    'serieshydro', 'seriesmeteo', 'seriesobselab', 'seriesobselabmeteo',
    'simulations']

PREV_PROBABILITY = {
    50: 'ResMoyPrev',
    0: 'ResMinPrev',
    100: 'ResMaxPrev'}

PREV_TENDANCE = {
    'moy': 'ResMoyPrev',
    'min': 'ResMinPrev',
    'max': 'ResMaxPrev'
}

# some tags mappings
CLS_MAPPINGS = {
    _sitehydro.Sitehydro: 'SiteHydro',
    _sitehydro.Station: 'StationHydro',
    _sitehydro.Capteur: 'Capteur',
    _sitemeteo.Sitemeteo: 'SiteMeteo',
    _sitemeteo.Grandeur: 'Grandeur'}

# sandre hydrometrie namespaces
NS = (
    'http://xml.sandre.eaufrance.fr/scenario/hydrometrie/{version}',
    'http://www.w3.org/2001/XMLSchema-instance')
NS_ATTR = {
    'xmlns': NS[0],
    '{%s}schemaLocation' % NS[1]: '%s %s/sandre_sc_hydrometrie.xsd' % (
        NS[0], NS[0])}


# -- testsfunction ------------------------------------------------------------
def _to_xml(scenario=None, intervenants=None, siteshydro=None, sitesmeteo=None,
            seuilshydro=None, seuilsmeteo=None, modelesprevision=None,
            evenements=None, courbestarage=None, jaugeages=None,
            courbescorrection=None, serieshydro=None, seriesmeteo=None,
            seriesobselab=None, seriesobselabmeteo=None,
            simulations=None, bdhydro=False, strict=True, ordered=False,
            version=None):
    """Return a etree.Element a partir des donnees passes en argument.

    Cette fonction est privee et les utilisateurs sont invites a utiliser la
    classe xml.Message comme interface d'ecriture des fichiers XML Hydrometrie.

    Arguments:
        scenario (xml.Scenario) = 1 element
        intervenants (intervenant.Intervenant collection) = iterable or None
        siteshydro (sitehydro.Sitehydro collection) = iterable or None
        sitesmeteo (sitemeteo.Sitemeteo collection) = iterable or None
        seuilshydro (seuil.Seuilhydro collection) = iterable or None
        seuilsmeteo (seuil.Seuilmeteo collection) = iterable or None
        modelesprevision (modeleprevision.Modeleprevision collection) =
            iterable or None
        evenements (evenement.Evenement collection) = iterable ou None
        courbestarage (courbetarage.CourbeTarage collection) = iterable ou None
        jaugeages (jaugeage.Jaugeage collection) = iterable ou None
        courbescorrection (courbecorrection.CourbeCorrection collection) =
            iterable ou None
        serieshydro (obshydro.Serie collection) = iterable or None
        seriesmeteo (obsmeteo.Serie collection) = iterable or None
        seriesobselab(obselaboreehydro.SerieObsElab collection) =
            iterable or None
        seriesobselabmeteo(obselaboreemeteo.SerieObsElabMeteo collection) =
            iterable or None
        simulations (simulation.Simulation collection) = iterable or None
        bdhydro (bool, defaut False) = controle de conformite bdhydro
        strict (bool, defaut True) = controle de conformite XML Hydrometrie
        ordered (bool, default False) = essaie de conserver l'ordre de certains
            elements
        version (str or None) = version Sandre 1.1 ou 2 ou None
            si None utilisation du la version du scenario

    """
    # make a deep copy of locals() which is a dict {arg_name: arg_value, ...}
    # keep only Message items
    # and replace default empty lists with None
    args = {
        k: (v if v != [] else None) for k, v in locals().items()
        if k in ORDERED_ACCEPTED_KEYS}

    # init the tree
    if bdhydro:
        tree = _etree.Element('hydrometrie')
    else:
        ns_attr = {}
        for key, value in NS_ATTR.items():
            ns_attr[key] = value.format(version=version)
        tree = _etree.Element('hydrometrie',
                              attrib=ns_attr)

    # TODO - this is awful :/ we should factorize those lines

    if version is None and args['scenario'] is not None:
        version = args['scenario'].version
    # add the scenario
    if args['scenario'] is not None:
        tree.append(
            _scenario_to_element(
                args['scenario'], bdhydro=bdhydro, strict=strict,
                version=version))

    # add the referentiel
    items = ORDERED_ACCEPTED_KEYS[1:7]
    choice = len([args[i] for i in items if args[i] is not None]) > 0
    if choice:
        sub = _etree.SubElement(tree, 'RefHyd')

        # intervenants
        if args['intervenants'] is not None:
            sub.append(_intervenants_to_element(
                args['intervenants'], bdhydro=bdhydro, strict=strict,
                version=version))

        # siteshydro and seuilshydro
        if (args['siteshydro'], args['seuilshydro']) != (None, None):
            # we add the common SitesHydro tag and we remove it from
            # each element because seuilshydro are childs of siteshydro
            if args['siteshydro'] is not None or version < '2':
                subsiteshydro = _etree.SubElement(sub, 'SitesHydro')
            if args['siteshydro'] is not None:
                element = _siteshydro_to_element(
                    args['siteshydro'], bdhydro=bdhydro, strict=strict,
                    version=version)
                for elementsitehydro in element.findall('./SiteHydro'):
                    subsiteshydro.append(elementsitehydro)
            if args['seuilshydro'] is not None:
                element = _seuilshydro_to_element(
                    seuilshydro=args['seuilshydro'],
                    ordered=ordered,
                    bdhydro=bdhydro,
                    strict=strict,
                    version=version)
                if version < '2':
                    for elementsitehydro in element.findall('./SiteHydro'):
                        subsiteshydro.append(elementsitehydro)
                else:
                    # Sandre V2 seuils rattachés directement à RefHyd
                    sub.append(element)

        # sitesmeteo
        if args['sitesmeteo'] is not None:
            sub.append(_sitesmeteo_to_element(
                args['sitesmeteo'], args['seuilsmeteo'], bdhydro=bdhydro,
                strict=strict, version=version))

        # seuilsmeteo
        if args['seuilsmeteo'] is not None and version >= '2':
            sub.append(_seuilsmeteo_to_element(
                args['seuilsmeteo'], bdhydro=bdhydro, strict=strict,
                version=version))

        # modelesprevision
        if args['modelesprevision'] is not None:
            sub.append(_modelesprevision_to_element(
                args['modelesprevision'], bdhydro=bdhydro, strict=strict))

    # add the datas
    items = ORDERED_ACCEPTED_KEYS[7:]
    choice = len([args[i] for i in items if args[i] is not None]) > 0
    if choice:
        sub = _etree.SubElement(tree, 'Donnees')
        for k in items:
            # version 1  les lames d'eau sont des obsmeteo
            if k == 'seriesmeteo':
                element = eval('_{0}_to_element(args[k], '
                               'args[\'seriesobselabmeteo\'], '
                               'bdhydro={1}, strict={2}, '
                               'version=\'{3}\')'.format(
                                   k, bdhydro, strict, version))
                if element is not None:
                    sub.append(element)

            elif args[k] is not None:
                element = eval('_{0}_to_element(args[k], '
                               'bdhydro={1}, strict={2}, '
                               'version=\'{3}\')'.format(
                                   k, bdhydro, strict, version))
                if element is not None:
                    sub.append(element)


    # DEBUG -
    # print(_etree.tostring(
    #     tree, encoding='utf-8', xml_declaration=1,  pretty_print=1))

    # return
    return tree


# -- atomic functions ---------------------------------------------------------
def _scenario_to_element(scenario, bdhydro=False, strict=True, version='1.1'):
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
            ('VersionScenario', {'value': version}),
            ('NomScenario', {'value': scenario.nom}),
            ('DateHeureCreationFichier',
                {'value': datetime2iso(scenario.dtprod)})))
        # template for scenario sub-elements <Emetteur> and <Destinataire>
        for tag in ('Emetteur', 'Destinataire'):
            item = getattr(scenario, tag.lower())
            story[tag] = {
                'sub': _collections.OrderedDict((
                    ('CdIntervenant', {
                        'value': str(item.intervenant.code),
                        'attr': {'schemeAgencyID': item.intervenant.origine}}),
                    ('NomIntervenant', {
                        'value': str(item.intervenant.nom)
                        if item.intervenant.nom is not None else None}),
                    ('CdContact', {
                        'value': str(item.contact.code)
                        if (
                            (item.contact is not None) and
                            (item.contact.code is not None)
                        ) else None,
                        # bdhydro requires a junk attr for the contacts
                        'attr': {'schemeAgencyID': 'SANDRE'}
                        if bdhydro else None})))}

        # action !
        return _factory(root=_etree.Element('Scenario'), story=story)


def _intervenant_to_element(intervenant, bdhydro=False, strict=True, version='1.1'):
    """Return a <Intervenant> element from a intervenant.Intervenant."""

    if intervenant is not None:

        # prerequisites
        if strict:
            _required(intervenant, ['code'])

        cdcommune = intervenant.commune.code \
            if intervenant.commune is not None else None
        adresse = intervenant.adresse \
            if intervenant.adresse is not None else None

        # template for intervenant simple elements
        story = _collections.OrderedDict((
            ('CdIntervenant', {
                'value': str(intervenant.code),
                'attr': {'schemeAgencyID': intervenant.origine}}),
            ('NomIntervenant', {'value': intervenant.nom}),
            ('StIntervenant', {'value': intervenant.statut}),
            ('DateCreationIntervenant', {'value': date2iso(intervenant.dtcreation)}),
            ('DateMajIntervenant', {'value': datetime2iso(intervenant.dtmaj)}),
            ('AuteurIntervenant', {'value': intervenant.auteur}),
            ('MnIntervenant', {'value': intervenant.mnemo}),
            ('BpIntervenant', {'value': adresse.boitepostale}),
            ('ImmoIntervenant', {'value': adresse.adresse1_cplt}),
            ('RueIntervenant', {'value': adresse.adresse1}),
            ('LieuIntervenant', {'value': adresse.lieudit}),
            ('VilleIntervenant', {'value': adresse.ville}),
            ('DepIntervenant', {'value': adresse.dep}),
            ('CommentairesIntervenant', {'value': intervenant.commentaire}),
            ('ActivitesIntervenant', {'value': intervenant.activite}),
            ('CPIntervenant', {'value': adresse.codepostal}),
            ('NomInternationalIntervenant', {'value': intervenant.nominternational}),
            ('CdSIRETRattacheIntervenant', {'value': intervenant.siret})))
        
        if cdcommune is not None:
            if version < '2':
                story['CdCommune'] = {'value': cdcommune}
            else :
                story['Commune'] = {
                    'value': None,
                    'sub': _collections.OrderedDict((
                            ('CdCommune', {'value': cdcommune}), ))}
        story['Contacts'] = {
                'value': None,
                'force': True if (len(intervenant.contacts) > 0) else False}
        story['PaysComplementIntervenant'] = {'value': adresse.pays}
        story['AdEtrangereComplementIntervenant'] = {'value': adresse.adresse2}
        story['TelephoneComplementIntervenant'] = {'value': intervenant.telephone}
        story['FaxComplementIntervenant'] = {'value': intervenant.fax}
        story['SiteWebComplementIntervenant'] = {'value': intervenant.siteweb}
        
        if intervenant.pere is not None:
            pere = {'CdIntervenant': {
                'value': intervenant.pere.code,
                'attr': {'schemeAgencyID': intervenant.pere.origine}}}
            story['IntervenantPere'] = {'value': None,
                                        'sub': pere}


        # make element <Intervenant>
        element = _factory(root=_etree.Element('Intervenant'), story=story)

        # add the contacts if necessary
        if len(intervenant.contacts) > 0:
            child = element.find('Contacts')
            for contact in intervenant.contacts:
                child.append(
                    _contact_to_element(
                        contact, bdhydro=bdhydro, strict=strict))

        # return
        return element

def _contact_to_element(contact, bdhydro=False, strict=True, version='1.1'):
    """Return a <Contact> element from a intervenant.Contact."""

    if contact is not None:

        # prerequisite
        if strict:
            _required(contact, ['code'])

        adresse = contact.adresse if contact.adresse is not None \
            else _intervenant.Adresse()

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
                if bdhydro else None}),
            ('NomContact', {'value': contact.nom}),
            ('PrenomContact', {'value': contact.prenom}),
            ('CiviliteContact', {'value': contact.civilite}),
            ('ProfilContact', {'value': contact.profilasstr}),
            ('AdContact', {'value': adresse.adresse1}),
            ('AdEtrangereContact', {'value': adresse.adresse2}),
            ('CpContact', {'value': adresse.codepostal}),
            ('VilleContact', {'value': adresse.ville}),
            ('FonctionContact', {'value': contact.fonction}),
            ('TelephoneContact', {'value': contact.telephone}),
            ('PortContact', {'value': contact.portable}),
            ('FaxContact', {'value': contact.fax}),
            ('MelContact', {'value': contact.mel}),
            ('PaysContact', {'value': adresse.pays}),
            ('DateMajContact', {'value': datetime2iso(contact.dtmaj)}),
            ('ProfilsAdminLocal', {
                'value': None,
                'force': True if len(contact.profilsadmin) > 0 else False}),
            ('AliasContact', {'value': contact.alias}),
            ('MotPassContact', {'value': contact.motdepasse}),
            ('DtActivationContact', {'value': datetime2iso(contact.dtactivation)}),
            ('DtDesactivationContact', {
                'value': datetime2iso(contact.dtdesactivation)})))

        # make element <Contact> and return
        element = _factory(root=_etree.Element('Contact'), story=story)

        # add profilsadmin if necessary
        if len(contact.profilsadmin) > 0:
            child = element.find('ProfilsAdminLocal')
            for profiladmin in contact.profilsadmin:
                child.append(_contactprofiladmin_to_element(profiladmin))

        # return
        return element


def _contactprofiladmin_to_element(profil):
    """Return a <ProfilAdminLocal> element
    from _intervenant.ProfilAdminLocal
    """
    if profil is None:
        return
    story = _collections.OrderedDict((
        ('CdProfilAdminLocal', {'value': profil.profil}),
        ('ZonesHydro', {
            'value': None,
            'sub': _collections.OrderedDict((
                    ('CdZoneHydro', {'value': profil.zoneshydro}), ))}),
        ('DtActivationProfilAdminLocal', {
            'value': datetime2iso(profil.dtactivation)}),
        ('DtDesactivationProfilAdminLocal', {
            'value': datetime2iso(profil.dtdesactivation)})
        ))

    return _factory(root=_etree.Element('ProfilAdminLocal'), story=story)


def _sitehydro_to_element(sitehydro, seuilshydro=None,
                          bdhydro=False, strict=True, version='1.1'):
    """Return a <SiteHydro> element from a sitehydro.Sitehydro.

    Args:
        sitehydro (sitehydro.Sitehydro)
        seuilshydro (an iterable of seuil.Seuilhydro) = the seuilshydro
            belonging to the sitehydro. They are added to the sub tag
            <ValeursSeuilsSiteHydro>

    """

    if sitehydro is not None:

        if version >= '2':
            tags = _sandre_tags.SandreTagsV2
        else:
            tags = _sandre_tags.SandreTagsV1

        if seuilshydro is None:
            seuilshydro = []

        # prerequisites
        if strict:
            _required(sitehydro, ['code'])

        dtmaj = datetime2iso(sitehydro.dtmaj)
        dtpremdonnee = None
        if sitehydro.dtpremieredonnee is not None:
            if version == '1.1':
                dtpremdonnee = date2iso(sitehydro.dtpremieredonnee)
            else:
                dtpremdonnee = datetime2iso(sitehydro.dtpremieredonnee)
        essai = None
        if sitehydro.essai is not None:
            if sitehydro.essai:
                essai = 'true'
            else:
                essai = 'false'
        # template for sitehydro simple elements
        story = _collections.OrderedDict((
            ('CdSiteHydro', {'value': sitehydro.code}),
            ('LbSiteHydro', {'value': sitehydro.libelle}),
            ('LbUsuelSiteHydro', {'value': sitehydro.libelleusuel}),
            ('TypSiteHydro', {'value': sitehydro.typesite}),
            ('MnSiteHydro', {'value': sitehydro.mnemo}),
            (tags.comtlbsitehydro, {'value': sitehydro.complementlibelle}),
            ('CoordSiteHydro', {
                'value': None,
                'force': True if sitehydro.coord is not None else False}),
            ('PkAmontSiteHydro', {'value': sitehydro.pkamont}),
            ('PkAvalSiteHydro', {'value': sitehydro.pkaval}),
            ('AltiSiteHydro', {
                'value': None,
                'force': True if sitehydro.altitude is not None else False}),
            (tags.dtmajsitehydro, {'value': dtmaj})))
        story['BassinVersantSiteHydro'] = {'value': sitehydro.bvtopo}
        if version == '2':
            story['BassinVersantHydroSiteHydro'] = {'value': sitehydro.bvhydro}
        story['FuseauHoraireSiteHydro'] = {'value': sitehydro.fuseau}
        story[tags.stsitehydro] = {'value': sitehydro.statut}
        # TODO version 1.1 balise Donponct
        story['DtPremDonSiteHydro'] = {'value': dtpremdonnee}
        story['PremMoisEtiageSiteHydro'] = {'value': sitehydro.moisetiage}
        story['PremMoisAnHydSiteHydro'] = {'value': sitehydro.moisanneehydro}
        if version == '2':
            story['DureeCarCruSiteHydro'] = {'value': sitehydro.dureecrues}
        story['DroitPublicationSiteHydro'] = {'value': sitehydro.publication}
        story['EssaiSiteHydro'] = {'value': essai}
        story['InfluGeneSiteHydro'] = {'value': sitehydro.influence}
        story['ComInfluGeneSiteHydro'] = {
                'value': sitehydro.influencecommentaire}
        story['ComSiteHydro'] = {'value': sitehydro.commentaire}
        if sitehydro.siteassocie is not None:
            story['SiteHydroAssocie'] = {
                'sub': _collections.OrderedDict((
                    ('CdSiteHydro', {'value': sitehydro.siteassocie.code}), ))}
        if len(sitehydro.sitesattaches) > 0:
            story['SitesHydroAttaches'] = {'value': None, 'force': True}
        story['CdEuMasseDEau'] = {'value': sitehydro.massedeau}
        story['CdEntiteHydrographique'] = {'value': sitehydro.entitehydro}
        if len(sitehydro.loisstat) > 0:
            story['LoisStatContexteSiteHydro'] = {'value': None, 'force': True}

        if len(sitehydro.images) > 0:
            story['ImagesSiteHydro'] = {'value': None, 'force': True}

        if len(sitehydro.roles) > 0:
            story[tags.rolscontactsitehydro] = {'value': None, 'force': True}

        story['CdTronconHydrographique'] = {'value': sitehydro.tronconhydro}
        if len(sitehydro.entitesvigicrues) > 0:
            story[tags.entsvigicru] = {'value': None, 'force': True}
        # Communes Version 1.1
        story['CdCommune'] = {
                'value': [commune.code for commune in sitehydro.communes]
                if version == '1.1' else None}
        # Communes version 2
        story['Communes'] = {
                    'value': None,
                    'force': True if (
                        version == '2' and len(sitehydro.communes) > 0
                    ) else False}
        story['CdSiteHydroAncienRef'] = {'value': sitehydro.codeh2}
        story['StationsHydro'] = {
                'value': None,
                'force': True if (len(sitehydro.stations) > 0) else False}
        story['ValeursSeuilsSiteHydro'] = {
                'value': None,
                'force': True if (len(seuilshydro) > 0) else False}
        story['CdZoneHydro'] = {'value': sitehydro.zonehydro}
        story['PrecisionCoursDEauSiteHydro'] = {
            'value': sitehydro.precisioncoursdeau}

        if version == '2':
            if len(sitehydro.sitesamont) > 0:
                story['SitesHydroAmont'] = {'value': None, 'force': True}
            if len(sitehydro.sitesaval) > 0:
                story['SitesHydroAval'] = {'value': None, 'force': True}

        # update the coord if necessary
        if sitehydro.coord is not None:
            story['CoordSiteHydro'] = {
                'sub': _collections.OrderedDict((
                    ('CoordXSiteHydro', {'value': sitehydro.coord.x}),
                    ('CoordYSiteHydro', {'value': sitehydro.coord.y}),
                    ('ProjCoordSiteHydro', {'value': sitehydro.coord.proj})))}

        # update the coord if necessary
        if sitehydro.altitude is not None:
            story['AltiSiteHydro'] = {
                'sub': _collections.OrderedDict((
                    ('AltitudeSiteHydro',
                     {'value': sitehydro.altitude.altitude}),
                    ('SysAltimetriqueSiteHydro',
                     {'value': sitehydro.altitude.sysalti}),
                    ))}

        # make element <SiteHydro>
        element = _factory(root=_etree.Element('SiteHydro'), story=story)
        
        # add communes for version == 2 if necessary
        if version == '2' and len(sitehydro.communes) > 0:
            child = element.find('Communes')
            for commune in sitehydro.communes:
                child.append(_commune_to_element(commune=commune))

        # add sitesamont for version == 2 if necessary
        if version == '2' and len(sitehydro.sitesamont) > 0:
            child = element.find('SitesHydroAmont')
            for siteamont in sitehydro.sitesamont:
                child.append(_siteamontaval_to_element(site=siteamont,
                                                       amont=True))

        # add sitesaval for version == 2 if necessary
        if version == '2' and len(sitehydro.sitesaval) > 0:
            child = element.find('SitesHydroAval')
            for siteaval in sitehydro.sitesaval:
                child.append(_siteamontaval_to_element(site=siteaval,
                                                       amont=False))

        # add sites attaches if necessary
        if len(sitehydro.sitesattaches) > 0:
            child = element.find('SitesHydroAttaches')
            for siteattache in sitehydro.sitesattaches:
                child.append(_siteattache_to_element(siteattache=siteattache,
                                                     version=version))

        # add lois stat if necessary
        if len(sitehydro.loisstat) > 0:
            child = element.find('LoisStatContexteSiteHydro')
            for loistat in sitehydro.loisstat:
                child.append(_loistat_to_element(loistat=loistat,
                                                 entite='SiteHydro'))

        # add images if necessary
        if len(sitehydro.images) > 0:
            child = element.find('ImagesSiteHydro')
            for image in sitehydro.images:
                child.append(_image_to_element(image=image,
                                                 entite='SiteHydro'))

        # add roles if necessary
        if len(sitehydro.roles) > 0:
            child = element.find(tags.rolscontactsitehydro)
            for role in sitehydro.roles:
                child.append(_role_to_element(role=role, version=version,
                                              tags=tags, entite='SiteHydro'))

        # add the tronconsvigilance if necessary
        if len(sitehydro.entitesvigicrues) > 0:
            child = element.find(tags.entsvigicru)
            for entitevigicrues in sitehydro.entitesvigicrues:
                child.append(
                    _tronconvigilance_to_element(
                        entitevigicrues, strict=strict, version=version))

        # add the stations if necessary
        if len(sitehydro.stations) > 0:
            child = element.find('StationsHydro')
            for station in sitehydro.stations:
                child.append(
                    _station_to_element(
                        station, bdhydro=bdhydro, strict=strict,
                        version=version))

        # add the seuils if necessary
        if len(seuilshydro) > 0:
            child = element.find('ValeursSeuilsSiteHydro')
            for seuilhydro in seuilshydro:
                child.append(_seuilhydro_to_element(seuilhydro, strict=strict))

        # return
        return element


def _image_to_element(image, entite):
    """Return a <Image*>  from a _composant_site.Image"""
    if image is None:
        return

    story = _collections.OrderedDict((
        ('AdressedelImage' + entite, {'value': image.adresse}),
        ('TypIll' + entite, {'value': image.typeill}),
        ('FormatIll' + entite, {'value': image.formatimg}),
        ('ComImg' + entite, {'value': image.commentaire})))

    return _factory(root=_etree.Element('Image' + entite), story=story)



def _role_to_element(role, version, tags, entite):
    """Return a <RoleContactSiteHydro>  or a <RolContactSiteHydro> element
    or a <RoleContactStationHydro>  or a <RolContactStationHydro> element
    from a _composant_site.commune"""
    if role is None:
        return

    dtdeb = datetime2iso(role.dtdeb)
    dtfin = datetime2iso(role.dtfin)
    dtmaj = datetime2iso(role.dtmaj)

    if version < '2' and entite == 'StationHydro':
        rolecontactbalise = 'RoleContact'
    else:
        rolecontactbalise  = 'RoleContact' + entite
    story = _collections.OrderedDict((
        ('CdContact', {'value': role.contact.code}),
        (rolecontactbalise, {'value': role.role}),
        ('DtDebutContact' + entite, {'value': dtdeb}),
        ('DtFinContact' + entite, {'value': dtfin}),
        (tags.dtmajrolecontact + entite, {'value': dtmaj})))

    return _factory(root=_etree.Element(tags.rolcontact + entite), story=story)


def _commune_to_element(commune):
    """Return a <Commune> element from a _composant_site.commune"""
    if commune is None:
        return
    story = _collections.OrderedDict((
        ('CdCommune', {'value': commune.code}),
        ('LbCommune', {'value': commune.libelle})))

    return _factory(root=_etree.Element('Commune'), story=story)


def _siteamontaval_to_element(site, amont):
    """Return a <SiteHydroAmont> or <SiteHydroAval> element
    from sitehydro.Sitehydro"""
    if site is None:
        return
    story = _collections.OrderedDict((
        ('CdSiteHydro', {'value': site.code}),
        ('LbSiteHydro', {'value': site.libelle})))
    if amont:
        tag = 'SiteHydroAmont'
    else:
        tag = 'SiteHydroAval'

    return _factory(root=_etree.Element(tag), story=story)


def _siteattache_to_element(siteattache, version):
    """Return a <SiteHydroAttache> element from a sitehydro.Sitehydroattache"""
    if siteattache is None:
        return
    story = _collections.OrderedDict((
        ('CdSiteHydro', {'value': siteattache.code}),
        ('PonderationSiteHydroAttache', {'value': siteattache.ponderation})))

    if version == '2':
        dtdeb = datetime2iso(siteattache.dtdeb)
        dtfin = datetime2iso(siteattache.dtfin)
        dtdebactivation = datetime2iso(siteattache.dtdebactivation)
        dtfinactivation = datetime2iso(siteattache.dtfinactivation)

        story['DecalSiteHydroAttache'] = {'value': siteattache.decalage}
        story['DtDebSiteHydroAttache'] = {'value': dtdeb}
        story['DtFinSiteHydroAttache'] = {'value': dtfin}
        story['DtDebActivationSiteHydroAttache'] = {'value': dtdebactivation}
        story['DtFinActivationSiteHydroAttache'] = {'value': dtfinactivation}

    return _factory(root=_etree.Element('SiteHydroAttache'), story=story)


def _loistat_to_element(loistat, entite):
    """Return <LoiStatContexteSiteHydro> or <LoiStatContexteStationHydro>
    element from a _composant_site.LoiStat"""
    if loistat is None:
        return
    story = _collections.OrderedDict((
        ('TypContexteLoiStat', {'value': loistat.contexte}),
        ('TypLoi' + entite, {'value': loistat.loi})))
    return _factory(root=_etree.Element('LoiStatContexte' + entite),
                    story=story)


def _codesitemeteo_to_value(sitemeteo, bdhydro=False, strict=True, version='1.1'):
    code = sitemeteo.code
    if strict:
        _required(sitemeteo, ['code'])
        # in bdhydro cdsitemeteo 8 or 9 char
        if bdhydro and sitemeteo.code[0] == '0':
                code = sitemeteo.code[1:]
    return code


def _sitemeteo_to_element(sitemeteo, seuilsmeteo=None, bdhydro=False, strict=True, version='1.1'):
    """Return a <SiteMeteo> element from a sitemeteo.Sitemeteo."""

    if sitemeteo is not None:

        if version >= '2':
            tags = _sandre_tags.SandreTagsV2
        else:
            tags = _sandre_tags.SandreTagsV1

        # prerequisites
        code = _codesitemeteo_to_value(sitemeteo, bdhydro, strict)

        # template for sitemeteo simple elements
        story = _collections.OrderedDict((
            ('CdSiteMeteo', {'value': code}),
            ('LbSiteMeteo', {'value': sitemeteo.libelle}),
            ('LbUsuelSiteMeteo', {'value': sitemeteo.libelleusuel}),
            ('MnSiteMeteo', {'value': sitemeteo.mnemo}),
            ('LieuDitSiteMeteo', {'value': sitemeteo.lieudit}),
            ('CoordSiteMeteo', {
                'value': None,
                'force': True if sitemeteo.coord is not None else False}),
            ('AltiSiteMeteo', {
                'value': None,
                'force': True if sitemeteo.altitude is not None else False}),
            ('FuseauHoraireSiteMeteo', {'value': sitemeteo.fuseau}),
            (tags.dtmajsitemeteo, {'value': datetime2iso(sitemeteo.dtmaj)}),
            ('DtOuvertureSiteMeteo', {
                'value': datetime2iso(sitemeteo.dtouverture)}),
            ('DtFermSiteMeteo', {
                'value': datetime2iso(sitemeteo.dtfermeture)}),
            ('DroitPublicationSiteMeteo', {
                'value': bool2xml(sitemeteo.droitpublication)}),
            ('EssaiSiteMeteo', {'value': bool2xml(sitemeteo.essai)}),
            ('ComSiteMeteo', {'value': sitemeteo.commentaire}),
            ('ImagesSiteMeteo', {
                'value': None,
                'force': True if (len(sitemeteo.images) > 0) else False}),
            ('ReseauxMesureSiteMeteo', {
                'value': None,
                'force': True if (len(sitemeteo.reseaux) > 0) else False}),
            (tags.rolscontactsitemeteo, {
                'value': None,
                'force': True if (len(sitemeteo.roles) > 0) else False}),
            ('CdZoneHydro', {'value': sitemeteo.zonehydro}),
            ('CdCommune', {'value': sitemeteo.commune}),
            ('GrdsMeteo', {
                'value': None,
                'force': True if (len(sitemeteo.grandeurs) > 0) else False}),
            ('VisitesSiteMeteo', {
                'value': None,
                'force': True if (len(sitemeteo.visites) > 0) else False})))

        # update the coord if necessary
        if sitemeteo.coord is not None:
            story['CoordSiteMeteo'] = {
                'sub': _collections.OrderedDict((
                    ('CoordXSiteMeteo', {'value': sitemeteo.coord.x}),
                    ('CoordYSiteMeteo', {'value': sitemeteo.coord.y}),
                    ('ProjCoordSiteMeteo', {'value': sitemeteo.coord.proj})))}

        # update the altitude if necessary
        if sitemeteo.altitude is not None:
            story['AltiSiteMeteo'] = {
                'sub': _collections.OrderedDict((
                    ('AltitudeSiteMeteo',{'value':
                        sitemeteo.altitude.altitude}),
                    ('SysAltimetriqueSiteMeteo', {'value':
                        sitemeteo.altitude.sysalti})))}

        # update reseaux if necessary
        if len(sitemeteo.reseaux) > 0 and version < '2':
            codesreseaux = [reseau.code for reseau in sitemeteo.reseaux]
            story['ReseauxMesureSiteMeteo'] = {
                'sub': {'CodeSandreRdd': {'value': codesreseaux}}}

        # make element <Sitemeteo>
        element = _factory(root=_etree.Element('SiteMeteo'), story=story)

        # update images if necessary
        if len(sitemeteo.images) > 0:
            child = element.find('ImagesSiteMeteo')
            for image in sitemeteo.images:
                child.append(_image_to_element(image, 'SiteMeteo'))

        # update reseaux if necessary
        if len(sitemeteo.reseaux) > 0 and version >= '2':
            child = element.find('ReseauxMesureSiteMeteo')
            for reseau in sitemeteo.reseaux:
                reseaustory = _collections.OrderedDict(
                    (('CodeSandreRdd', {'value': reseau.code}),
                     ('NomRdd', {'value': reseau.libelle})))

                child.append(
                        _factory(root=_etree.Element('RSX'),
                                 story=reseaustory))

        # add the grandeurs if necessary
        if len(sitemeteo.grandeurs) > 0:
            child = element.find('GrdsMeteo')
            for grandeur in sitemeteo.grandeurs:
                child.append(_grandeur_to_element(
                        grandeur,seuilsmeteo=seuilsmeteo, strict=strict,
                        version=version))


        # add roles if necessary
        if len(sitemeteo.roles) > 0:
            child = element.find(tags.rolscontactsitemeteo)
            for role in sitemeteo.roles:
                child.append(_role_to_element(role=role,
                                              version=version,
                                              tags=tags,
                                              entite='SiteMeteo'))

        # add visites if necessary
        if len(sitemeteo.visites) > 0:
            child = element.find('VisitesSiteMeteo')
            for visite in sitemeteo.visites:
                child.append(_visite_to_element(visite))

        # return
        return element


def _visite_to_element(visite):
    """Return a <VisiteSiteMeteo> from a sitemeteo.Visite"""
    if visite is None:
        return
    # template for tronconvigilance simple elements
    story = _collections.OrderedDict((
        ('DtVisiteSiteMeteo', {'value': datetime2iso(visite.dtvisite)}),
        ('CdContact', {'value': visite.contact.code
                       if visite.contact is not None else None}),
        ('MethClassVisiteSiteMeteo', {'value': visite.methode}),
        ('ModeOperatoireUtiliseVisiteSiteMeteo', {'value': visite.modeop})))

    # action !
    return _factory(
        root=_etree.Element('VisiteSiteMeteo'), story=story)


def _tronconvigilance_to_element(entitevigicrues, bdhydro=False, strict=True,
                                 version='1.1'):
    """Return a <TronconVigilanceSiteHydro> element or a <EntVigiCru> from a
    sitehydro.Tronconvigilance."""

    if entitevigicrues is None:
        return
    if version == '2':
        tags = _sandre_tags.SandreTagsV2
    else:
        tags = _sandre_tags.SandreTagsV1
    # prerequisites
    if strict:
        _required(entitevigicrues, ['code'])

    # template for tronconvigilance simple elements
    story = _collections.OrderedDict((
        (tags.cdentvigicru, {'value': entitevigicrues.code}),
        (tags.nomentvigicru, {'value': entitevigicrues.libelle})))

    # action !
    return _factory(
        root=_etree.Element(tags.entvigicru), story=story)


def _seuilmeteo_to_element(seuilmeteo, bdhydro=False, strict=True,
                           version='2'):
    """Return a <SeuilMeteo> from a seuil.Seuilmeteo"""
    if seuilmeteo is None:
        return

    if version >= '2':
        tags = _sandre_tags.SandreTagsV2
    else:
        tags = _sandre_tags.SandreTagsV1

    grd = seuilmeteo.grandeurmeteo
    cdsitemeteo = _codesitemeteo_to_value(grd.sitemeteo, bdhydro, strict)

    if version >= '2':
        dicsite = _collections.OrderedDict((
            ('CdSiteMeteo', {'value': cdsitemeteo}),
            ('LbSiteMeteo', {'value': grd.sitemeteo.libelle})
            ))
        dicgrd = _collections.OrderedDict((
            ('DtMiseServiceGrdMeteo',
             {'value': datetime2iso(grd.dtmiseservice)}),
            ('CdGrdMeteo', {'value': grd.typemesure})
            ))
        rulessite = {'value': None, 'sub': dicsite}
        rulesgrd = {'value': None, 'sub': dicgrd}
    else:
        rulessite = {'value': None}
        rulesgrd = {'value': None}
    # template for seuilhydro simple element
    story = _collections.OrderedDict((
        (tags.cdseuilmeteo, {'value': seuilmeteo.code}),
        ('SiteMeteo', rulessite),
        ('GrdMeteo', rulesgrd),
        (tags.typseuilmeteo, {'value': seuilmeteo.typeseuil}),
        (tags.natureseuilmeteo, {'value': seuilmeteo.nature}),
        (tags.dureeseuilmeteo, {'value': seuilmeteo.duree}),
        (tags.lbusuelseuilmeteo, {'value': seuilmeteo.libelle}),
        (tags.mnseuilmeteo, {'value': seuilmeteo.mnemo}),
        (tags.indicegraviteseuilmeteo, {'value': seuilmeteo.gravite})))

    if version >= '2':
        story[tags.dtmajseuilmeteo] = {'value': datetime2iso(seuilmeteo.dtmaj)}
        story[tags.comseuilmeteo] = {'value': seuilmeteo.commentaire}

        if len(seuilmeteo.valeurs) > 0:
            story['ValsSeuilMeteo'] = {'value': None, 'force': True}
    else:
        story[tags.comseuilmeteo] = {'value': seuilmeteo.commentaire}
        # add value
        if len(seuilmeteo.valeurs) > 0:
            valeur = seuilmeteo.valeurs[0]
            story[tags.valvalseuilmeteo] = {'value': valeur.valeur}
            story[tags.dtdesactivationvalseuilmeteo] = {
                    'value': datetime2iso(valeur.dtdesactivation)}
            story[tags.dtactivationvalseuilmeteo] = {
                    'value': datetime2iso(valeur.dtactivation)}
            story[tags.tolerancevalseuilmeteo] = {'value': valeur.tolerance}

        story[tags.dtmajseuilmeteo] = {'value': datetime2iso(seuilmeteo.dtmaj)}

    # make element <SeuilMeteo> 
    element = _factory(root=_etree.Element(tags.seuilmeteo), story=story)
    
    # add <ValSeuilMeteo>  if necessary
    if len(seuilmeteo.valeurs) > 0 and version >= '2':
        child = element.find('ValsSeuilMeteo')
        for valeur in seuilmeteo.valeurs:
            child.append(_valeurseuil_to_element_v2(valeur, strict=strict))
    return element


def _seuilhydro_to_element(seuilhydro, bdhydro=False, strict=True, version='1.1'):
    """Return a <ValeursSeuilSiteHydro> element from a seuil.Seuilhydro."""
    if seuilhydro is not None:

        if version >= '2':
            tags = _sandre_tags.SandreTagsV2
        else:
            tags = _sandre_tags.SandreTagsV1
        # prerequisites
        if strict:
            _required(seuilhydro, ['code'])

        # extract the unique Valeurseuil for the site
        if version < '2':
            sitevaleurseuil = [
                valeur for valeur in seuilhydro.valeurs
                if isinstance(valeur.entite, _sitehydro.Sitehydro)]
            if len(sitevaleurseuil) > 1:
                raise ValueError('more than one site valeurseuil for seuil %s' %
                                 seuilhydro.code)
            elif len(sitevaleurseuil) == 1:
                sitevaleurseuil = sitevaleurseuil[0]
                seuilhydro.valeurs.remove(sitevaleurseuil)
            else:
                sitevaleurseuil = None
        else:
            sitevaleurseuil = None

        if version >= '2' and seuilhydro.sitehydro is not None:
            forcesitehydro = True
        else:
            forcesitehydro = False

        if seuilhydro.publication is not None and version < '2':
            if seuilhydro.publication == 0:
                publication = None
            elif seuilhydro.publication in [10, 11, 12]:
                publication = 'true'
            else:
                publication = 'false'
        else:
            publication = seuilhydro.publication

        # template for seuilhydro simple element
        story = _collections.OrderedDict((
            (tags.cdseuilhydro, {'value': seuilhydro.code}),
            ('SiteHydro', {'value': None, 'force': forcesitehydro}),
            (tags.typseuilhydro, {'value': seuilhydro.typeseuil}),
            (tags.natureseuilhydro, {'value': seuilhydro.nature}),
            (tags.dureeseuilhydro, {'value': seuilhydro.duree}),
            (tags.lbusuelseuilhydro, {'value': seuilhydro.libelle}),
            (tags.mnseuilhydro, {'value': seuilhydro.mnemo}),
            (tags.typpubliseuilhydro, {'value': publication}),
            (tags.indicegraviteseuilhydro, {'value': seuilhydro.gravite}),
            (tags.valforceeseuilhydro, {
                'value': bool2xml(seuilhydro.valeurforcee)
                if seuilhydro.valeurforcee is not None else None})))
        if version >= '2':
            story[tags.dtmajseuilhydro] = {
                'value': datetime2iso(seuilhydro.dtmaj)}
        story[tags.comseuilhydro] = {'value': seuilhydro.commentaire}

        if version < '2':
            # add site values
            if sitevaleurseuil is not None:
                story['ValDebitSeuilSiteHydro'] = {
                    'value': sitevaleurseuil.valeur}
                story['DtActivationSeuilSiteHydro'] = {
                    'value': datetime2iso(sitevaleurseuil.dtactivation)}
                story['DtDesactivationSeuilSiteHydro'] = {
                    'value': datetime2iso(sitevaleurseuil.dtdesactivation)}

        # add the stations values
        if len(seuilhydro.valeurs) > 0:
            story[tags.valsseuilhydro] = {
                'value': None, 'force': True}

        if version < '2':
            # add the last tags, in disorder :)
            if sitevaleurseuil is not None:
                story['ToleranceSeuilSiteHydro'] = {
                    'value': sitevaleurseuil.tolerance}
            story['DtMajSeuilSiteHydro'] = {
                'value': datetime2iso(seuilhydro.dtmaj)}

        # add sitehydro in SandreV2
        if forcesitehydro:
            story['SiteHydro'] = {
                'sub': _collections.OrderedDict((
                    ('CdSiteHydro', {'value': seuilhydro.sitehydro.code}),
                    ('LbSiteHydro', {'value': seuilhydro.sitehydro.libelle})))}

        # make element <ValeursSeuilsStationHydro>
        element = _factory(
            root=_etree.Element(tags.seuilhydro),
            story=story)

        # add the <ValeursSeuilsStationHydro> or <ValsSeuilHydro> if necessary
        if len(seuilhydro.valeurs) > 0:
            child = element.find(tags.valsseuilhydro)
            for valeur in seuilhydro.valeurs:
                if version < '2':
                    child.append(
                            _valeurseuilstation_to_element(valeur, strict=strict))
                else:
                    child.append(
                            _valeurseuil_to_element_v2(valeur, strict=strict))

        # return
        return element


def _valeurseuilstation_to_element(valeurseuil, bdhydro=False,
                                   strict=True, version='1.1'):
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
                code=valeurseuil.entite.code, length=10, errors='ignore'):
            raise TypeError(
                'valeurseuil.entite is not a sitehydro.Station')

        # template for valeurseuilstation simple element
        story = _collections.OrderedDict((
            ('CdStationHydro', {'value': valeurseuil.entite.code}),
            ('ValHauteurSeuilStationHydro', {
                'value': valeurseuil.valeur}),
            ('DtActivationSeuilStationHydro', {
                'value': datetime2iso(valeurseuil.dtactivation)}),
            ('DtDesactivationSeuilStationHydro', {
                'value': datetime2iso(valeurseuil.dtdesactivation)}),
            ('ToleranceSeuilStationHydro', {'value': valeurseuil.tolerance})))

        # action !
        return _factory(
            root=_etree.Element('ValeursSeuilStationHydro'), story=story)


def _valeurseuil_to_element_v2(valeurseuil, bdhydro=False,
                               strict=True, version='2'):
    """Return a <ValeursSeuilStationHydro> element from a seuil.Valeurseuil.

    Requires valeurseuil.entite.code to be a station hydro code.

    """
    if valeurseuil is not None:

        # prerequisites
        if strict:
            _required(valeurseuil, ['entite', 'valeur'])
            # _required(valeurseuil.entite, ['code'])

        if not isinstance(valeurseuil.entite,
                          (_sitehydro.Station, _sitehydro.Sitehydro,
                           _sitehydro.Capteur, _sitemeteo.Grandeur)):
            raise TypeError(
                'valeurseuil.entite is not a Sitehydro'
                ' or a Station or a Capteur or a Grandeur')
        if isinstance(valeurseuil.entite, _sitemeteo.Grandeur):
            typeseuil = 'SeuilMeteo'
        else:
            typeseuil = 'SeuilHydro'

        # template for valeurseuilstation simple element
        story = _collections.OrderedDict((
            ('ValVal'+ typeseuil, {
                'value': valeurseuil.valeur}),
            ('ToleranceVal'+ typeseuil, {'value': valeurseuil.tolerance}),
            ('DtActivationVal'+ typeseuil, {
                'value': datetime2iso(valeurseuil.dtactivation)}),
            ('DtDesactivationVal'+ typeseuil, {
                'value': datetime2iso(valeurseuil.dtdesactivation)})))

        if isinstance(valeurseuil.entite, _sitehydro.Station):
            story['StationHydro'] = {
                'sub': _collections.OrderedDict((
                    ('CdStationHydro', {'value': valeurseuil.entite.code}),
                    ('LbStationHydro', {'value': valeurseuil.entite.libelle})))
                }
        if isinstance(valeurseuil.entite, _sitehydro.Sitehydro):
            story['SiteHydro'] = {
                'sub': _collections.OrderedDict((
                    ('CdSiteHydro', {'value': valeurseuil.entite.code}),
                    ('LbSiteHydro', {'value': valeurseuil.entite.libelle})))}
        if isinstance(valeurseuil.entite, _sitehydro.Capteur):
            story['Capteur'] = {
                'sub': _collections.OrderedDict((
                    ('CdCapteur', {'value': valeurseuil.entite.code}),
                    ('LbCapteur', {'value': valeurseuil.entite.libelle})))}
        # action !
        return _factory(
            root=_etree.Element('Val' + typeseuil), story=story)


def _station_to_element(station, bdhydro=False, strict=True, version='1.1'):
    """Return a <StationHydro> element from a sitehydro.Station."""

    if version >= '2':
        tags = _sandre_tags.SandreTagsV2
    else:
        tags = _sandre_tags.SandreTagsV1

    if station is not None:

        # prerequisites
        if strict:
            _required(station, ['code'])

        dtmaj = datetime2iso(station.dtmaj)
        dtmiseservice = datetime2iso(station.dtmiseservice)
        dtfermeture = datetime2iso(station.dtfermeture)
        surveillance = bool2xml(station.surveillance)
        essai = bool2xml(station.essai)
        # template for station simple element
        story = _collections.OrderedDict((
            ('CdStationHydro', {'value': station.code}),
            ('LbStationHydro', {'value': station.libelle}),
            ('TypStationHydro', {'value': station.typestation}),
            (tags.complementlibellestationhydro, {
                'value': station.libellecomplement}),
            (tags.comprivestationhydro, {'value': station.commentaireprive}),
            (tags.dtmajstationhydro, {'value': dtmaj}),
            ('CoordStationHydro', {
                'value': None,
                'force': True if station.coord is not None else False}),
            ('PkStationHydro', {'value': station.pointk}),
            ('DtMiseServiceStationHydro', {'value': dtmiseservice}),
            ('DtFermetureStationHydro', {'value': dtfermeture}),
            ('ASurveillerStationHydro', {'value': surveillance}),
            ('NiveauAffichageStationHydro', {
                'value': station.niveauaffichage}),
            ('DroitPublicationStationHydro', {'value': station.droitpublication}),
            ('DelaiDiscontinuiteStationHydro', {'value': station.delaidiscontinuite}),
            ('DelaiAbsenceStationHydro', {'value': station.delaiabsence}),
            ('EssaiStationHydro', {'value': essai}),
            ('InfluLocaleStationHydro', {'value': station.influence}),
            ('ComInfluLocaleStationHydro', {'value': station.influencecommentaire}),
            ('ComStationHydro', {'value': station.commentaire}),
            
            ('StationsHydroAnterieure', {
                    'value': None,
                    'force': True if (len(station.stationsanterieures) > 0
                        and version >= '2') else None}),
            # Sandre V1.1
            ('StationHydroAnterieure', {
                    'value': None,
                    'force': True if (len(station.stationsanterieures) > 0
                        and version < '2') else None}),
            ('StationsHydroPosterieure', {
                    'value': None,
                    'force': True if (len(station.stationsposterieures) > 0
                        and version >= '2') else None}),
            ('StationHydroFille', {
                    'value': None,
                    'force': True if (len(station.plagesstationsfille) > 0
                        and version < '2') else None}),
            ('QualifsDonneesStationHydro', {
                    'value': None,
                    'force': True if len(station.qualifsdonnees) > 0
                        else None}),
            ('FinalitesStationHydro', {
                    'value': None,
                    'force': True if len(station.finalites) > 0
                        else None}),
            ('LoisStatContexteStationHydro', {
                    'value': None,
                    'force': True if len(station.loisstat) > 0
                        else None}),
            ('ImagesStationHydro', {
                    'value': None,
                    'force': True if len(station.images) > 0
                        else None}),
            (tags.rolscontactstationhydro, {
                    'value': None,
                    'force': True if len(station.roles) > 0
                        else None}),
            ('PlagesUtilStationHydro', {
                'value': None,
                'force': True if (len(station.plages) > 0)
                    else False}),
            ('ReseauxMesureStationHydro', {
                'value': None,
                'force': True if (len(station.reseaux) > 0) else False}),
            ('Capteurs', {
                'value': None,
                'force': True if (len(station.capteurs) > 0) else False}),
            ('RefsAlti', {
                'value': None,
                'force': True if (len(station.refsalti) > 0) else False}),
            ('CdStationHydroAncienRef', {'value': station.codeh2}),
            ('CdCommune', {'value': station.commune})))
        
        if version >= '2':
            if len(station.stationsamont) > 0:
                story['StationsHydroAmont'] =  {'value': None, 'force': True}
            if len(station.stationsaval) > 0:
                story['StationsHydroAval'] =  {'value': None, 'force': True}
            if len(station.plagesstationsfille) > 0:
                story['PlagesAssoStationHydroFille'] = {'value': None,
                                                        'force': True}
            if len(station.plagesstationsmere) > 0:
                story['PlagesAssoStationHydroMere'] = {'value': None,
                                                       'force': True}

        # update the coord if necessary
        if station.coord is not None:
            story['CoordStationHydro'] = {
                'sub': _collections.OrderedDict((
                    ('CoordXStationHydro', {'value': station.coord.x}),
                    ('CoordYStationHydro', {'value': station.coord.y}),
                    ('ProjCoordStationHydro',
                        {'value': station.coord.proj})))}

        # update StationHydroAnterieure if necessary
        if len(station.stationsanterieures) > 0 and version < '2':
            story['StationHydroAnterieure'] = {
                'sub': {'CdStationHydro': {'value':
                    station.stationsanterieures[0].code}}}

        # update StationHydroAnterieure if necessary
        if len(station.plagesstationsfille) > 0 and version < '2':
            story['StationHydroFille'] = {
                'sub': {'CdStationHydro': {'value':
                    station.plagesstationsfille[0].code}}}

        # update reseaux if necessary
        if len(station.reseaux) > 0 and version < '2':
            codesreseaux = [reseau.code for reseau in station.reseaux]
            story['ReseauxMesureStationHydro'] = {
                'sub': {'CodeSandreRdd': {'value': codesreseaux}}}

        # update finaites if necessary
        if len(station.finalites) > 0 and version < '2':
            story['FinalitesStationHydro'] = {
                'sub': {'CdFinaliteStationHydro':
                        {'value': station.finalites}}}

        # make element <StationHydro>
        element = _factory(root=_etree.Element('StationHydro'), story=story)

        # add the stationsantieures if necessary
        if len(station.stationsanterieures) > 0 and version >= '2':
            child = element.find('StationsHydroAnterieure')
            for stationant in station.stationsanterieures:
                child.append(_substation_to_element(
                        station=stationant, tag='StationHydroAnterieure'))

        # add the stationsposterieures if necessary
        if len(station.stationsposterieures) > 0 and version >= '2':
            child = element.find('StationsHydroPosterieure')
            for stationpost in station.stationsposterieures:
                child.append(_substation_to_element(
                        station=stationpost, tag='StationHydroPosterieure'))

        # update finalites if necessary
        if len(station.finalites) > 0 and version >= '2':
            child = element.find('FinalitesStationHydro')
            for finalite in station.finalites:
                finalitetory = {'CdFinaliteStationHydro': {'value': finalite}}
                child.append(
                        _factory(root=_etree.Element('FinaliteStationHydro'),
                                 story=finalitetory))

        # update finalites if necessary
        if len(station.reseaux) > 0 and version >= '2':
            child = element.find('ReseauxMesureStationHydro')
            for reseau in station.reseaux:
                reseaustory = _collections.OrderedDict(
                    (('CodeSandreRdd', {'value': reseau.code}),
                     ('NomRdd', {'value': reseau.libelle})))

                child.append(
                        _factory(root=_etree.Element('RSX'),
                                 story=reseaustory))

        # add the capteurs if necessary
        if len(station.capteurs) > 0:
            child = element.find('Capteurs')
            for capteur in station.capteurs:
                child.append(
                    _capteur_to_element(
                        capteur, bdhydro=bdhydro, strict=strict,
                        version=version))

        # add qualifsdonnees if necessary
        if len(station.qualifsdonnees) > 0:
            child = element.find('QualifsDonneesStationHydro')
            for qualif in station.qualifsdonnees:
                child.append(_qualifdonnees_to_element(qualif))

        # add loisstat if necessary
        if len(station.loisstat) > 0:
            child = element.find('LoisStatContexteStationHydro')
            for loistat in station.loisstat:
                child.append(_loistat_to_element(loistat, 'StationHydro'))

        # add images if necessary
        if len(station.images) > 0:
            child = element.find('ImagesStationHydro')
            for image in station.images:
                child.append(_image_to_element(image, 'StationHydro'))

        # add roles if necessary
        if len(station.roles) > 0:
            child = element.find(tags.rolscontactstationhydro)
            for role in station.roles:
                child.append(_role_to_element(role=role,
                                              version=version,
                                              tags=tags,
                                              entite='StationHydro'))

        # add refsalti if necessary
        if len(station.refsalti) > 0:
            child = element.find('RefsAlti')
            for refalti in station.refsalti:
                child.append(_refalti_to_element(refalti))

        if len(station.plages) > 0:
            child = element.find('PlagesUtilStationHydro')
            for plage in station.plages:
                child.append(_plage_to_element(
                    plage, 'StationHydro'))

        if version >= '2':
            if len(station.stationsamont) > 0:
                child = element.find('StationsHydroAmont')
                for stationamont in station.stationsamont:
                    child.append(_substation_to_element(
                            station=stationamont, tag='StationHydroAmont'))
    
            if len(station.stationsaval) > 0:
                child = element.find('StationsHydroAval')
                for stationaval in station.stationsaval:
                    child.append(_substation_to_element(
                            station=stationaval, tag='StationHydroAval'))
            
            if len(station.plagesstationsfille) > 0:
                child = element.find('PlagesAssoStationHydroFille')
                for plagestation in station.plagesstationsfille:
                    child.append(_plagestation_to_element(
                        plagestation=plagestation, entite='StationHydroFille'))
    
            if len(station.plagesstationsmere) > 0:
                child = element.find('PlagesAssoStationHydroMere')
                for plagestation in station.plagesstationsmere:
                    child.append(_plagestation_to_element(
                        plagestation=plagestation, entite='StationHydroMere'))

        # return
        return element


def _substation_to_element(station, tag):
    """Return a element with only code and libelle from station"""
    if station is None:
        return
    story = _collections.OrderedDict()
    story['CdStationHydro'] = {'value': station.code}
    story['LbStationHydro'] = {'value': station.libelle}

    # action !
    return _factory(root=_etree.Element(tag),
                    story=story)


def _plagestation_to_element(plagestation, entite):
    """Return a <PlagesAssoStationHydroFille> or a <PlageAssoStationHydroMere>
    from a _copmosant_site.PlageStation"""
    if plagestation is None:
        return

    element = _etree.Element('PlageAsso' + entite)
    element.append(_substation_to_element(station=plagestation,
                                          tag='StationHydro'))
    # story['StationHydro'] = {'value': None, 'force': True}
    if plagestation.dtdeb is not None:
        element.append(_make_element(
            tag_name='DtDebPlageAssoStationHydroMereFille',
            text=datetime2iso(plagestation.dtdeb)))
    if plagestation.dtfin is not None:
        element.append(_make_element(
            tag_name='DtFinPlageAssoStationHydroMereFille',
            text=datetime2iso(plagestation.dtfin)))

    return element


def _plage_to_element(plage, entite):
    """Return a PlageUtilStationHydro or PlageUtilCapteur

    according to entite (StationHydro or Capteur)

    """
    if plage is None:
        return None

    story = _collections.OrderedDict()
    story['DtDebPlageUtil{}'.format(entite)] = {
            'value': datetime2iso(plage.dtdeb)}
    if plage.dtfin is not None:
        story['DtFinPlageUtil{}'.format(entite)] = {
            'value': datetime2iso(plage.dtfin)}
    if plage.dtactivation is not None:
        story['DtActivationPlageUtil{}'.format(entite)] = {
            'value': datetime2iso(plage.dtactivation)}
    if plage.dtdesactivation is not None:
        story['DtDesactivationPlageUtil{}'.format(entite)] = {
            'value': datetime2iso(plage.dtdesactivation)}
    if plage.active is not None:
        story['ActivePlageUtil{}'.format(entite)] = {
            'value': bool2xml(plage.active)}

    # action !
    return _factory(root=_etree.Element('PlageUtil{}'.format(entite)),
                    story=story)


def _qualifdonnees_to_element(qualif):
    """Return a QualifDonneesStationHydro"""
    if qualif is None:
        return None

    story = _collections.OrderedDict()
    story['CdRegime'] = {'value': qualif.coderegime}
    story['QualifDonStationHydro'] = {
            'value': qualif.qualification}
    story['ComQualifDonStationHydro'] = {'value': qualif.commentaire}

    # action !
    return _factory(root=_etree.Element('QualifDonneesStationHydro'),
                    story=story)


def _refalti_to_element(refalti):
    """Return a RefAlti element"""
    if refalti is None:
        return None

    dtfin = datetime2iso(refalti.dtfin)
    dtactivation = datetime2iso(refalti.dtactivation)
    dtdesactivation = datetime2iso(refalti.dtdesactivation)
    dtmaj = datetime2iso(refalti.dtmaj)

    story = _collections.OrderedDict()
    story['DtDebutRefAlti'] = {'value': datetime2iso(refalti.dtdeb)}
    story['DtFinRefAlti'] = {'value': dtfin}
    story['DtActivationRefAlti'] = {'value': dtactivation}
    story['DtDesactivationRefAlti'] = {'value': dtdesactivation}

    if refalti.altitude is not None:
        story['AltiRefAlti'] = {
            'sub': _collections.OrderedDict((
                ('AltitudeRefAlti', {'value': refalti.altitude.altitude}),
                ('SysAltiRefAlti', {'value': refalti.altitude.sysalti})))}

    story['DtMajRefAlti'] = {'value': dtmaj}
    
    # make element <StationHydro>
    return _factory(root=_etree.Element('RefAlti'), story=story)


def _capteur_to_element(capteur, bdhydro=False, strict=True, version='1.1'):
    """Return a <Capteur> element from a sitehydro.Capteur."""

    if capteur is not None:
        if version >= '2':
            tags = _sandre_tags.SandreTagsV2
        else:
            tags = _sandre_tags.SandreTagsV1

        # prerequisites
        if strict:
            _required(capteur, ['code'])
        if bdhydro:
            _required(capteur, ['libelle'])

        if capteur.surveillance is not None:
            surveillance = bool2xml(capteur.surveillance)
        else:
            surveillance = None

        if capteur.essai is not None:
            essai = bool2xml(capteur.essai)
        else:
            essai = None

        dtmaj = None
        if capteur.dtmaj is not None:
            dtmaj = datetime2iso(capteur.dtmaj)

        # template for capteur simple element
        story = _collections.OrderedDict((
            ('CdCapteur', {'value': capteur.code}),
            ('LbCapteur', {'value': capteur.libelle}),
            ('MnCapteur', {'value': capteur.mnemo}),
            ('TypCapteur', {'value': capteur.typecapteur}),
            ('TypMesureCapteur', {'value': capteur.typemesure}),
            ('ASurveillerCapteur', {'value': surveillance}),
            (tags.dtmajcapteur, {'value': dtmaj}),
            (tags.pdtcapteur, {'value': capteur.pdt}),
            ('EssaiCapteur', {'value': essai}),
            ('ComCapteur', {'value': capteur.commentaire})))
        
        if capteur.observateur is not None:
            story['Observateur'] = {'sub': {'CdContact': {
                'value': capteur.observateur.code}}}

        story['PlagesUtilCapteur'] = {
                'value': None,
                'force': True if len(capteur.plages) > 0 else False
                }
        story['CdCapteurAncienRef'] =  {'value': capteur.codeh2}

        # make element <Capteur>
        element = _factory(root=_etree.Element('Capteur'), story=story)

        if len(capteur.plages) > 0:
            child = element.find('PlagesUtilCapteur')
            for plage in capteur.plages:
                child.append(_plage_to_element(
                    plage, 'Capteur'))

        # return
        return element


def _grandeur_to_element(grandeur, seuilsmeteo=None, bdhydro=False,
                         strict=True, version='1.1'):
    """Return a <GrdMeteo> element from a sitehydro.grandeur."""

    if grandeur is not None:

        if version >= '2':
            tags = _sandre_tags.SandreTagsV2
        else:
            tags = _sandre_tags.SandreTagsV1

        # prerequisites
        if strict:
            _required(grandeur, ['typemesure'])

        surveillance = None
        delaiabsence = None
        if version >= '2':
            # surveillance and delai only Sandre V2
            surveillance = bool2xml(grandeur.surveillance)
            delaiabsence = grandeur.delaiabsence

        grdseuils = []
        if version < '2'and seuilsmeteo is not None:
            for seuil in seuilsmeteo:
                if seuil.grandeurmeteo == grandeur:
                    grdseuils.append(seuil)

        # template for grandeur simple element
        story = _collections.OrderedDict((
            ('CdGrdMeteo', {'value': grandeur.typemesure}),
            ('DtMiseServiceGrdMeteo', {'value':
                datetime2iso(grandeur.dtmiseservice)}),
            ('DtFermetureServiceGrdMeteo', {'value':
                datetime2iso(grandeur.dtfermeture)}),
            ('EssaiGrdMeteo', {'value': bool2xml(grandeur.essai)}),
            ('ASurveillerGrdMeteo', {'value': surveillance}),
            ('DelaiAbsGrdMeteo', {'value': delaiabsence}),
            (tags.pdtgrdmeteo, {'value': grandeur.pdt}),
            ('ClassesQualiteGrd', {
                'value': None,
                'force': True if len(grandeur.classesqualite) > 0 else False}),
            ('ValeursSeuilsGrdMeteo', {
                'value': None,
                'force': True if len(grdseuils) > 0 else False}),
            ('DtMajGrdMeteo', {'value': datetime2iso(grandeur.dtmaj)})))

        # action !
        element = _factory(root=_etree.Element('GrdMeteo'), story=story)

        if len(grandeur.classesqualite) > 0:
            child = element.find('ClassesQualiteGrd')
            for classequalite in grandeur.classesqualite:
                child.append(_classequalite_to_element(classequalite))

        if len(grdseuils) > 0:
            child = element.find('ValeursSeuilsGrdMeteo')
            for seuilmeteo in grdseuils:
                child.append(_seuilmeteo_to_element(
                    seuilmeteo, bdhydro=bdhydro, strict=strict,
                    version=version))

        return element


def _classequalite_to_element(classequalite):
    """Return a <ClasseQualiteGrd> from a sitemeteo.ClasseQualite"""
    if classequalite is None:
        return
    dtvisite = None
    if classequalite.visite is not None:
        dtvisite = datetime2iso(classequalite.visite.dtvisite)

    # template for classequalite simple element
    story = _collections.OrderedDict((
        ('CdqClasseQualiteGrd', {'value': classequalite.classe}),
        ('DtVisiteSiteMeteo', {'value': dtvisite}),
        ('DtDebutClasseQualiteGrd', {'value':
            datetime2iso(classequalite.dtdeb)}),
        ('DtFinClasseQualiteGrd', {'value':
            datetime2iso(classequalite.dtfin)})))

    return _factory(root=_etree.Element('ClasseQualiteGrd'), story=story)


def _modeleprevision_to_element(modeleprevision, bdhydro=False, strict=True, version='1.1'):
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
            ('DescModelePrevision', {'value': modeleprevision.description})))

        # make element <modeleprevision> and return
        return _factory(root=_etree.Element('ModelePrevision'), story=story)

def _evenement_to_element(evenement, bdhydro=False, strict=True, version='1.1'):
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
        if isinstance(evenement.entite, _sitemeteo.Sitemeteo):
            code = _codesitemeteo_to_value(sitemeteo=evenement.entite,
                                           bdhydro=bdhydro, strict=strict,
                                           version=version)
        else:
            code = evenement.entite.code

        story['Cd{}'.format(CLS_MAPPINGS[evenement.entite.__class__])] = {
            'value': code}
        # suite
        story['DtEvenement'] = {
            'value': datetime2iso(evenement.dt)}

        if version == '2':
            story['TypEvenement'] = {'value': evenement.typeevt}

        story['DescEvenement'] = {'value': evenement.descriptif}
        # Conversion Sandre V1.1 874 et 891 en 534
        if version == '1.1':
            if evenement.publication != 0:
                if evenement.publication in (20, 21, 22):
                    publication = 100  # prive
                elif evenement.publication in (30, 31, 32):
                    if evenement.typeevt == 7:  # cmnt vigicrues
                        publication = 20  # uniquement vigicrues
                    else:
                        publication = 100  # privé
                else:  # public 10 11 12
                    if evenement.typeevt == 7:  # cmnt vigicrues
                        publication = 10  # public + vigicrues
                    else:
                        publication = 1  # public
                story['TypPublicationEvenement'] = {'value': publication}
            elif evenement.typeevt == 7:  # inconnue et vigicrues
                #  uniquement vigicures
                story['TypPublicationEvenement'] = {'value': 20}
            elif evenement.dtfin is not None:
                story['TypPublicationEvenement'] = {'value': 25}
        else:
            story['TypPubliEvenement'] = {'value': evenement.publication}

        story['DtMajEvenement'] = {
            'value': None if evenement.dtmaj is None
            else datetime2iso(evenement.dtmaj)}

        if version == '2':
            if len(evenement.ressources) > 0:
                story['RessEvenement'] = {'value': None,
                                          'force': True}
            if evenement.dtfin is not None:
                story['DtFinEvenement'] = {
                    'value': datetime2iso(evenement.dtfin)}

        # action !
        element = _factory(root=_etree.Element('Evenement'), story=story)
        child = element.find('RessEvenement')
        for ressource in evenement.ressources:
            res_el = _etree.SubElement(child, 'ResEvenement')
            _etree.SubElement(res_el, 'UrlResEvenement').text = \
                str(ressource.url)
            if ressource.libelle is not None:
                _etree.SubElement(res_el, 'LbResEvenement').text = \
                    str(ressource.libelle)
        return element


def _courbetarage_to_element(courbe, bdhydro=False, strict=True, version='1.1'):
    """Return a <CourbeTarage> element from a courbetarage.CourbeTarage."""

    if courbe is not None:
        if version == '2':
            tags = _sandre_tags.SandreTagsV2
        else:
            tags = _sandre_tags.SandreTagsV1

        # prerequisite
        _required(courbe, ['code', 'libelle', 'typect', 'station'])
        if strict:
            pass
#            _required(courbe.contact, ['code'])
#            _required(courbe.entite, ['code'])
#            _required(courbe, ['descriptif'])

        # template for serie simple elements
        story = _collections.OrderedDict()
        story['CdCourbeTarage'] = {'value': courbe.code}
        story['LbCourbeTarage'] = {'value': courbe.libelle}
        story['TypCourbeTarage'] = {'value': courbe.typect}
        if version == '2'and courbe.dtcreation is not None:
            story['DtCreatCourbeTarage'] = {
                'value': datetime2iso(courbe.dtcreation)}
        story['LimiteInfCourbeTarage'] = {'value': courbe.limiteinf}
        story['LimiteSupCourbeTarage'] = {'value': courbe.limitesup}
        if version == '2':
            story['LimiteInfPubCourbeTarage'] = {'value': courbe.limiteinfpub}
            story['LimiteSupPubCourbeTarage'] = {'value': courbe.limitesuppub}
        story['DnCourbeTarage'] = {'value': courbe.dn}
        story['AlphaCourbeTarage'] = {'value': courbe.alpha}
        story['BetaCourbeTarage'] = {'value': courbe.beta}
        story['ComCourbeTarage'] = {'value': courbe.commentaire}
        story['CdStationHydro'] = {'value': courbe.station.code}
        story['CdContact'] = {
            'value': getattr(
                getattr(courbe, 'contact', None), 'code', None)}
        story['PivotsCourbeTarage'] = {'value': None,
            'force': True if (len(courbe.pivots) > 0) else False}
        story['PeriodesUtilisationCourbeTarage'] = {'value': None,
            'force': True if (len(courbe.periodes) > 0) else False}
        story['DtMajCourbeTarage'] = {
            'value': None if courbe.dtmaj is None
            else datetime2iso(courbe.dtmaj)}
        if version == '2':
            story['ComPrivCourbeTarage'] = {'value': courbe.commentaireprive}
        # make element <CourbeTarage>
        element = _factory(root=_etree.Element('CourbeTarage'), story=story)

        # add pivots if necessary
        if version == '1.1' and len(courbe.pivots) == 1:
            raise ValueError('Courbe cannot have only one pivot')
        if len(courbe.pivots) > 0:
            child = element.find('PivotsCourbeTarage')
            for pivot in courbe.pivots:
                child.append(
                    _pivotct_to_element(
                        pivot, strict=strict, version=version))

        # add periodes if necssary
        if len(courbe.periodes) > 0:
            child = element.find('PeriodesUtilisationCourbeTarage')
            for periode in courbe.periodes:
                child.append(
                    _periodect_to_element(
                        periode, strict=strict, version=version, tags=tags))
                # return
        return element


def _pivotct_to_element(pivot, strict=True, version='1.1'):
    _required(pivot, ['hauteur'])
    story = _collections.OrderedDict()
    story['HtPivotCourbeTarage'] = {'value': pivot.hauteur}
    if version == '1.1':
        story['QualifPivotCourbeTarage'] = {'value': pivot.qualif}

    if isinstance(pivot, _courbetarage.PivotCTPoly):
        _required(pivot, ['debit'])
        story['QPivotCourbeTarage'] = {'value': pivot.debit}
    elif isinstance(pivot, _courbetarage.PivotCTPuissance):
        _required(pivot, ['vara', 'varb', 'varh'])
        story['VarAPivotCourbeTarage'] = {'value': pivot.vara}
        story['VarBPivotCourbeTarage'] = {'value': pivot.varb}
        story['VarHPivotCourbeTarage'] = {'value': pivot.varh}

    else:
        raise TypeError('pivot is not a PivotCTPoly or a PivotCTPuissance')

    return _factory(root=_etree.Element('PivotCourbeTarage'), story=story)


def _periodect_to_element(periode, strict=True, version='1.1',
                          tags=_sandre_tags.SandreTagsV1):
    _required(periode, ['dtdeb', 'etat'])
    story = _collections.OrderedDict()
    story[tags.dtdebperiodeutilct] = {
        'value': datetime2iso(periode.dtdeb)}
    if periode.dtfin is not None:
        story['DtFinPeriodeUtilisationCourbeTarage'] = {
            'value': datetime2iso(periode.dtfin)}
    if periode.etat is not None:
        story['EtatPeriodeUtilisationCourbeTarage'] = {
            'value': periode.etat}
    if len(periode.histos) > 0:
        story[tags.histosactivationperiode] = {
            'value': None, 'force': True}
    element = _factory(root=_etree.Element('PeriodeUtilisationCourbeTarage'), story=story)

    # Add histos if necessary
    if len(periode.histos) > 0:
        child = element.find(tags.histosactivationperiode)
        for histo in periode.histos:
            child.append(
                _histoperiode_to_element(
                    histo, strict=strict, version=version, tags=tags))
    return element


def _histoperiode_to_element(histo, strict=True, version='1.1',
                             tags=_sandre_tags.SandreTagsV1):
    _required(histo, ['dtactivation'])
    story = _collections.OrderedDict()
    story[tags.dtactivationhistoperiode] = {
        'value': datetime2iso(histo.dtactivation)}
    if histo.dtdesactivation is not None:
        story[tags.dtdesactivationhistoperiode] = {
            'value': datetime2iso(histo.dtdesactivation)}

    return _factory(root=_etree.Element(tags.histoactivationperiode),
                    story=story)


def _jaugeage_to_element(jaugeage, bdhydro=False, strict=True, version='1.1'):
    """Return a <Jaugeage> element from a jaugeage.Jaugeage."""
    if jaugeage is not None:
        if version == '1.1':
            _required(jaugeage, ['code', 'site'])
            tags = _sandre_tags.SandreTagsV1
        else:
            _required(jaugeage, ['site', 'dtdeb'])
            tags = _sandre_tags.SandreTagsV2
        if strict:
            _required(jaugeage.site, ['code'])
        # template for seriehydro simple elements
        story = _collections.OrderedDict()
        story['CdJaugeage'] = {'value': jaugeage.code}
        if jaugeage.dte is not None:
            story['DtJaugeage'] = {
                'value': datetime2iso(jaugeage.dte)}
        story['DebitJaugeage'] = {'value': jaugeage.debit}
        if jaugeage.dtdeb is not None:
            story['DtDebJaugeage'] = {
                'value': datetime2iso(jaugeage.dtdeb)}
        if jaugeage.dtfin is not None:
            story['DtFinJaugeage'] = {
                'value': datetime2iso(jaugeage.dtfin)}
        story['SectionMouilJaugeage'] = {'value': jaugeage.section_mouillee}
        story['PerimMouilleJaugeage'] = {'value': jaugeage.perimetre_mouille}
        story['LargMiroirJaugeage'] = {'value': jaugeage.largeur_miroir}

        if version == '1.1':
            if jaugeage.mode != 0:
                story['ModeJaugeage'] = {
                    'value': _nomenclature.MODEJAUGEAGEMNEMO[jaugeage.mode]}
        else:
            story['ModeJaugeage'] = {'value': jaugeage.mode}

        story['ComJaugeage'] = {'value': jaugeage.commentaire}
        story['VitesseMoyJaugeage'] = {'value': jaugeage.vitessemoy}
        story['VitesseMaxJaugeage'] = {'value': jaugeage.vitessemax}
        story[tags.vitessemaxsurface] = {
            'value': jaugeage.vitessemax_surface}
        # TODO fuzzy mode
        story['CdSiteHydro'] = {'value': jaugeage.site.code}

        #story['HauteursJaugeage']
        if len(jaugeage.hauteurs) > 0:
            story['HauteursJaugeage'] = {'value': None,
                                         'force': True}

        if jaugeage.dtmaj is not None:
            story['DtMajJaugeage'] = {
                'value': datetime2iso(jaugeage.dtmaj)}

        if version == '2':
            if jaugeage.numero is not None:
                story['NumJaugeage'] = {'value': jaugeage.numero}
            if jaugeage.incertitude_calculee is not None:
                story['IncertCalJaugeage'] = {'value': jaugeage.incertitude_calculee}
            if jaugeage.incertitude_retenue is not None:
                story['IncertRetenueJaugeage'] = {'value': jaugeage.incertitude_retenue}
            if jaugeage.qualification is not None:
                story['QualifJaugeage'] = {'value': jaugeage.qualification}
            if jaugeage.commentaire_prive is not None:
                story['ComPrivJaugeage'] = {'value': jaugeage.commentaire_prive}
            if len(jaugeage.courbestarage) > 0:
                story['CourbesTarage'] = {'value': None,
                                          'force': True}

        # make element <CourbeTarage>
        element = _factory(root=_etree.Element('Jaugeage'), story=story)

        if len(jaugeage.hauteurs) > 0:
            child = element.find('HauteursJaugeage')
            for hauteur in jaugeage.hauteurs:
                child.append(
                    _hjaug_to_element(
                        hauteur, strict=strict))

        if version == '2' and len(jaugeage.courbestarage) > 0:
            child = element.find('CourbesTarage')
            for courbe in jaugeage.courbestarage:
                ctel = _etree.SubElement(child, 'CourbeTarage')
                _etree.SubElement(ctel, 'CdCourbeTarage').text = str(courbe.code)
                if courbe.libelle is not None:
                    _etree.SubElement(ctel, 'LbCourbeTarage').text = courbe.libelle

        return element


def _hjaug_to_element(hjaug, strict=True, version='1.1'):
    _required(hjaug, ['station', 'sysalti', 'coteretenue'])
    if strict:
        _required(hjaug.station, ['code'])
        if hjaug.stationfille is not None:
            _required(hjaug.stationfille, ['code'])
    # template for seriehydro simple elements
    story = _collections.OrderedDict()
    story['CdStationHydro'] = {'value': hjaug.station.code}
    story['SysAltiStationJaugeage'] = {'value': hjaug.sysalti}
    story['CoteRetenueStationJaugeage'] = {'value': hjaug.coteretenue}
    story['CoteDebutStationJaugeage'] = {'value': hjaug.cotedeb}
    story['CoteFinStationJaugeage'] = {'value': hjaug.cotefin}
    story['DnStationJaugeage'] = {'value': hjaug.denivele}
    story['DistanceStationJaugeage'] = {'value': hjaug.distancestation}
    if hjaug.stationfille is not None:
        story['StationFille'] = {'value': None, 'force': True}

    if hjaug.dtdeb_refalti is not None:
        story['DtDebutRefAlti'] = {
            'value': datetime2iso(hjaug.dtdeb_refalti)}

    # make element <StationFille>
    element = _factory(root=_etree.Element('HauteurJaugeage'), story=story)
    if hjaug.stationfille is not None:
        child = element.find('StationFille')
        child.append(_make_element(tag_name='CdStationHydro',
                                   text=hjaug.stationfille.code))

    return element


def _courbecorrection_to_element(courbe, bdhydro=False, strict=True, version='1.1'):
    """Return a <CourbeCorrH> element from a courbecorrection.CourbeCorrection."""
    if courbe is not None:
        # prerequisite
        _required(courbe, ['station'])
        if strict:
            _required(courbe.station, ['code'])
        # template for seriehydro simple elements
        story = _collections.OrderedDict()
        # TODO fuzzy mode
        story['CdStationHydro'] = {'value': courbe.station.code}
        story['LbCourbeCorrH'] = {'value': courbe.libelle}
        story['ComCourbeCorrH'] = {'value': courbe.commentaire}
        # story['PointsPivot']
        story['PointsPivot'] = {'value': None,
            'force': True if (len(courbe.pivots) > 0) else False}
        if courbe.dtmaj is not None:
            story['DtMajCourbeCorrH'] = {'value': datetime2iso(courbe.dtmaj)}

        # make element <CourbeTarage>
        element = _factory(root=_etree.Element('CourbeCorrH'), story=story)

        # add pivots if necessary
        if version == '1.1' and len(courbe.pivots) == 1:
            raise ValueError('Courbe cannot have only one pivot')
        if len(courbe.pivots) > 0:
            child = element.find('PointsPivot')
            for pivot in courbe.pivots:
                child.append(
                    _pivotcc_to_element(
                        pivot, strict=strict, version=version))
        return element


def _pivotcc_to_element(pivotcc, strict=True, version='1.1'):
    _required(pivotcc, ['dte', 'deltah'])

    if version == '2':
        tags = _sandre_tags.SandreTagsV2
    else:
        tags = _sandre_tags.SandreTagsV1

    story = _collections.OrderedDict()

    story['DtPointPivot'] = {'value': datetime2iso(pivotcc.dte)}
    story['DeltaHPointPivot'] = {'value': pivotcc.deltah}
    if pivotcc.dtactivation is not None:
        story['DtActivationPointPivot'] = {'value':
            datetime2iso(pivotcc.dtactivation)}
    if pivotcc.dtdesactivation is not None:
        story[tags.dtdesactivationpointpivot] = {'value':
            datetime2iso(pivotcc.dtdesactivation)}

    return _factory(root=_etree.Element('PointPivot'), story=story)


def _seriehydro_to_element(seriehydro, bdhydro=False, strict=True,
                           version='1.1', tags=_sandre_tags.SandreTagsV1):
    """Return a <Serie> element from a obshydro.Serie."""

    if seriehydro is not None:

        # prerequisite
        if version == '2':
            _required(seriehydro, ['entite'])
        else:
            _required(seriehydro, ['entite', 'dtdeb', 'dtfin', 'dtprod'])
        if strict:
            _required(seriehydro.entite, ['code'])
            _required(seriehydro, ['grandeur'])

        # template for seriehydro simple elements
        story = _collections.OrderedDict()
        # entite can be a Sitehydro, a Station or a Capteur
        story['Cd{}'.format(CLS_MAPPINGS[seriehydro.entite.__class__])] = {
            'value': seriehydro.entite.code}
        # suite
        story[tags.grdseriehydro] = {'value': seriehydro.grandeur}
        if seriehydro.dtdeb is not None:
            story[tags.dtdebseriehydro] = {
                'value': datetime2iso(seriehydro.dtdeb)}
        if seriehydro.dtfin is not None:
            story[tags.dtfinseriehydro] = {
                'value': datetime2iso(seriehydro.dtfin)}

        if version == '1.1':
            if seriehydro.observations is None:
                statut = 0
            else:
                statut = int(seriehydro.observations.iloc[0]['statut'].item())
            story['StatutSerie'] = {'value': str(statut)}

        if seriehydro.dtprod is not None:
            story[tags.dtprodseriehydro] = {
                'value': datetime2iso(seriehydro.dtprod)}

        if seriehydro.sysalti is not None:
            story[tags.sysaltiseriehydro] = {'value': str(seriehydro.sysalti)}
        if seriehydro.perime is not None:
            story[tags.serieperimhydro] = {
                'value': bool2xml(seriehydro.perime)}

        if seriehydro.pdt is not None:
            story[tags.pdtseriehydro] = {'value': str(seriehydro.pdt.to_int())}

        story['CdContact'] = {
            'value': getattr(
                getattr(seriehydro, 'contact', None), 'code', None)}

        # make element <Serie>
        element = _factory(root=_etree.Element(tags.seriehydro), story=story)

        # add the observations
        if seriehydro.observations is not None:
            element.append(_observations_to_element(
                observations=seriehydro.observations, version=version))

        # return
        return element


def _observations_to_element(observations, bdhydro=False, strict=True,
                             version='1.1'):
    """Return a <ObssHydro> element from a obshydro.Observations."""

    if observations is not None:

        # make element <ObssHydro>
        element = _etree.Element('ObssHydro')
        for observation in observations.itertuples():
            obs = _etree.SubElement(element, 'ObsHydro')
            # dte and res are mandatory...
            child = _etree.SubElement(obs, 'DtObsHydro')
            child.text = datetime2iso(observation.Index)
            child = _etree.SubElement(obs, 'ResObsHydro')
            child.text = str(observation.res)
            # while mth, qal and cnt aren't
            mth_elt = None
            if observation.mth is not None:
                # Conversion liste 512 en 507 Sandre V1.1
                mth = observation.mth
                if version == '1.1':
                    if mth in [8, 14]:
                        mth = 12
                    elif mth == 10:
                        mth = 4
                # child = _etree.SubElement(obs, 'MethObsHydro')
                # child.text = unicode(mth)
                mth_elt = _etree.Element('MethObsHydro')
                mth_elt.text = str(mth)

            qal_elt = None
            if observation.qal is not None:
                # child = _etree.SubElement(obs, 'QualifObsHydro')
                # child.text = unicode(observation.qal)
                qal_elt = _etree.Element('QualifObsHydro')
                qal_elt.text = str(observation.qal)

            if version == '2':
                if qal_elt is not None:
                    obs.append(qal_elt)
                if mth_elt is not None:
                    obs.append(mth_elt)
            else:
                if mth_elt is not None:
                    obs.append(mth_elt)
                if qal_elt is not None:
                    obs.append(qal_elt)

            if observation.cnt is not None:
                child = _etree.SubElement(obs, 'ContObsHydro')
                if version == '2':
                    child.text = str(observation.cnt)
                else:
                    child.text = 'true' if observation.cnt == 0 else 'false'

            if version == '2' and observation.statut is not None:
                _etree.SubElement(obs, 'StObsHydro').text = \
                    str(observation.statut)
        # return
        return element


def _obsmeteo_to_element(seriemeteo, index, obs, bdhydro=False, strict=True, version='1.1'):
    """Return a <ObsMeteo> element from a obsmeteo.serie and a observation."""

    if (seriemeteo is not None) and (index is not None) and (obs is not None):
        # template for seriemeteo simple elements
        story = _collections.OrderedDict()

        if isinstance(seriemeteo, _obsmeteo.Serie):
            # prerequisite
            _required(seriemeteo, ['grandeur', 'dtprod', 'duree'])
            _required(seriemeteo.grandeur, ['sitemeteo'])

            if strict:
                _required(seriemeteo.grandeur.sitemeteo, ['code'])
            # contact is also mandatory

            code = _codesitemeteo_to_value(
                sitemeteo=seriemeteo.grandeur.sitemeteo, bdhydro=bdhydro,
                strict=strict)

            story['CdGrdMeteo'] = {'value': seriemeteo.grandeur.typemesure}
            story['CdSiteMeteo'] = {'value': code}
        else:
            story['CdSiteHydro'] = {'value': seriemeteo.site.code}
        story['DtProdObsMeteo'] = {
            'value': datetime2iso(seriemeteo.dtprod)}
        story['DtObsMeteo'] = {'value': datetime2iso(index)}
        story['StatutObsMeteo'] = {'value': int(obs.statut)}
        story['ResObsMeteo'] = {'value': obs.res}
        if bdhydro:
            story['DureeObsMeteo'] = {
                'value': int(seriemeteo.duree.total_seconds() / 60)}
        else:
            story['DureeObsMeteo'] = {
                'value': None if (seriemeteo.duree.total_seconds() == 0)
                else int(seriemeteo.duree.total_seconds() / 60)}
        story['IndiceQualObsMeteo'] = {
            'value': None if _math.isnan(obs.qua) else int(obs.qua)}
        if obs.qal is not None:
            story['QualifObsMeteo'] = {'value': int(obs.qal)}
        if obs.mth is not None:
            story['MethObsMeteo'] = {'value': int(obs.mth)}
        story['CdContact'] = {
            'value': getattr(
                getattr(seriemeteo, 'contact', None), 'code', None)}

        # make element <Serie>
        element = _factory(root=_etree.Element('ObsMeteo'), story=story)

        # return
        return element



def _obselab_to_element(serie, obs, bdhydro=False, strict=True, version='1.1'):
    """Return a <ObsElabHydro> element
    from a SerieObsElab an ObservaionElaboree.
    """
    obsel = _etree.Element('ObsElabHydro')
    _etree.SubElement(obsel, 'DtProdObsElabHydro').text = \
        datetime2iso(serie.dtprod)

    if isinstance(serie.entite, _sitehydro.Sitehydro):
        _etree.SubElement(obsel, 'CdSiteHydro').text = \
            serie.entite.code
    else:
        _etree.SubElement(obsel, 'CdStationHydro').text = \
            serie.entite.code
    # dte and res are mandatory...
    _etree.SubElement(obsel, 'DtObsElabHydro').text = \
        datetime2iso(obs.Index)
    _etree.SubElement(obsel, 'ResObsElabHydro').text = \
        str(obs.res)
    if obs.statut is not None:
        _etree.SubElement(obsel, 'StatutObsElabHydro').text = \
            str(obs.statut)
    if obs.qal is not None:
        _etree.SubElement(obsel, 'QualifObsElabHydro').text = \
            str(obs.qal)
    if obs.mth is not None:
        _etree.SubElement(obsel, 'MethObsElabHydro').text = \
            str(obs.mth)
    if serie.sysalti is not None:
        _etree.SubElement(obsel, 'SysAltiObsElabHydro').text = \
            str(serie.sysalti)
    if serie.contact is not None:
        _etree.SubElement(obsel, 'CdContact').text = \
            str(serie.contact.code)
    if serie.dtdebrefalti is not None:
        _etree.SubElement(obsel, 'DtDebutRefAlti').text = \
            datetime2iso(serie.dtrefalti)
    # print(_etree.tostring(obsel, method='xml'))
    return obsel


def _simulation_to_element(simulation, bdhydro=False, strict=True, version='1.1'):
    """Return a <Simul> element from a simulation.Simulation."""

    if simulation is not None:

        # prerequisite
        _required(
            simulation, ['dtprod', 'entite', 'intervenant', 'modeleprevision'])
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
                'value': datetime2iso(simulation.dtprod)}),
            ('IndiceQualiteSimul', {
                'value': str(simulation.qualite)
                if simulation.qualite is not None else None}),
            ('StatutSimul', {
                'value': str(simulation.statut)
                if simulation.statut is not None else None}),
            ('PubliSimul', {
                'value': bool2xml(simulation.public)
                if simulation.public is not None else 'false'}),
            ('ComSimul', {'value': simulation.commentaire})))
        # entite can be a Sitehydro or a Station
        story['Cd{}'.format(CLS_MAPPINGS[simulation.entite.__class__])] = {
            'value': simulation.entite.code}
        # suite
        story['CdModelePrevision'] = {'value': simulation.modeleprevision.code}
        story['CdIntervenant'] = {
            'value': str(simulation.intervenant.code),
            'attr': {"schemeAgencyID": simulation.intervenant.origine}}

        # make element <Simul>
        element = _factory(root=_etree.Element('Simul'), story=story)

        # add the previsions
#        if simulation.previsions is not None:
#            element.append(
#                _previsions_to_element(simulation.previsions, strict=strict))

        if simulation.previsions_tend is not None \
            or simulation.previsions_prb is not None:
            previsions = {'tend': simulation.previsions_tend,
                          'prb': simulation.previsions_prb}
            element.append(
                _previsions_to_element(previsions, strict=strict)
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
    def closure(items, bdhydro=False, strict=True, version='1.1'):
        """Items should be a list of item objects."""
        if items is not None:
            element = _etree.Element(tag)
            for item in items:
                element.append(func(item, bdhydro=bdhydro, strict=strict,
                                    version=version))
            return element
    return closure

# return a <Intervenants> element from a list of intervenant.Intervenants
_intervenants_to_element = _global_function_builder(
    'Intervenants', _intervenant_to_element)
# return a <SitesHydro> element from a list of sitehydro.Sitehydro
_siteshydro_to_element = _global_function_builder(
    'SitesHydro', _sitehydro_to_element)
# return a <SitesMeteo> element from a list of sitemeteo.Sitemeteo
#_sitesmeteo_to_element = _global_function_builder(
#     'SitesMeteo', _sitemeteo_to_element)

def _sitesmeteo_to_element(sitesmeteo, seuilsmeteo=None,  bdhydro=False,
                           strict=True, version='1.1'):
    if sitesmeteo is None:
        return
    element = _etree.Element('SitesMeteo')
    for sitemeteo in sitesmeteo:
        element.append(_sitemeteo_to_element(
                sitemeteo=sitemeteo, seuilsmeteo=seuilsmeteo, bdhydro=bdhydro,
                strict=strict, version=version))
    return element
# return a <SeuilsMeteo> element from a list of seuil.Seuilmeteo
_seuilsmeteo_to_element = _global_function_builder(
    'SeuilsMeteo', _seuilmeteo_to_element)
# return a <ModelesPrevision> element from a list of Modeleprevision
_modelesprevision_to_element = _global_function_builder(
    'ModelesPrevision', _modeleprevision_to_element)
# return a <Evenements> element from a list of evenement.Evenement
_evenements_to_element = _global_function_builder(
    'Evenements', _evenement_to_element)
# return a <CourbesTarage> element from a list of courbetarage.CourbeTarage
_courbestarage_to_element = _global_function_builder(
    'CourbesTarage', _courbetarage_to_element)
# return a <Jaugeages> element from a list of jaugeage.Jaugeage
_jaugeages_to_element = _global_function_builder(
    'Jaugeages', _jaugeage_to_element)
# return a <CourbesTarage> element from a list of courbetarage.CourbeTarage
_courbescorrection_to_element = _global_function_builder(
    'CourbesCorrH', _courbecorrection_to_element)
# return a <Series> element from a list of obshydro.Serie
# _serieshydro_to_element = _global_function_builder(
#     'Series', _seriehydro_to_element)
# return a <Simuls> element from a list of simulation.Simulation
_simulations_to_element = _global_function_builder(
    'Simuls', _simulation_to_element)


def _serieshydro_to_element(serieshydro, bdhydro=False, strict=True,
                            version='1.1'):
    if serieshydro is None:
        return
    if version == '2':
        tags = _sandre_tags.SandreTagsV2
    else:
        tags = _sandre_tags.SandreTagsV1

    element = _etree.Element(tags.serieshydro)
    for seriehydro in serieshydro:
        element.append(_seriehydro_to_element(
            seriehydro, bdhydro=bdhydro, strict=strict,
            version=version, tags=tags))
    return element


# these 3 functions doesn't fit with the _global_function_builder :-\
def _seriesmeteo_to_element(seriesmeteo, seriesobselabmeteo, bdhydro=False,
                            strict=True, version='1.1'):
    """Return a <ObssMeteo> or a <SeriesObsMeteo>
    depending on Sandre version
    """
    if version == '2':
        return _seriesmeteo_v2(seriesmeteo, bdhydro, strict)
    return _seriesmeteo_v1(seriesmeteo, seriesobselabmeteo, bdhydro, strict)


def _seriesmeteo_v1(seriesmeteo, seriesobselabmeteo=None, bdhydro=False,
                    strict=True):
    """Return a <ObssMeteo> element from a list of obsmeteo.Serie."""
    if seriesmeteo is not None or seriesobselabmeteo is not None:
        element = _etree.Element('ObssMeteo')
        if seriesmeteo is not None:
            for serie in seriesmeteo:
                for row in serie.observations.iterrows():
                    element.append(_obsmeteo_to_element(
                        serie, *row, bdhydro=bdhydro, strict=strict))
        if seriesobselabmeteo is not None:
            for serie in seriesobselabmeteo:
                for row in serie.observations.iterrows():
                    element.append(_obsmeteo_to_element(
                        serie, *row, bdhydro=bdhydro, strict=strict))
        return element


def _seriesmeteo_v2(seriesmeteo, bdhydro=False, strict=True):
    """Return a <SeriesObsMeteo> element from a list of obsmeteo.Serie."""
    if seriesmeteo is None or not seriesmeteo:
        return
    element = _etree.Element('SeriesObsMeteo')
    for serie in seriesmeteo:
        element.append(_seriemeteo_v2(
                       serie=serie, bdhydro=bdhydro, strict=strict))
    return element


def _seriemeteo_v2(serie, bdhydro=False, strict=True):
    """Return a <SerieObsMeteo> element from a list of obsmeteo.Serie."""
    elt = _etree.Element('SerieObsMeteo')
    code = _codesitemeteo_to_value(sitemeteo=serie.grandeur.sitemeteo,
                                   bdhydro=bdhydro,
                                   strict=strict)
    _etree.SubElement(elt, 'CdSiteMeteo').text = code
    _etree.SubElement(elt, 'CdGrdMeteo').text = serie.grandeur.typemesure
    _etree.SubElement(elt, 'DureeSerieObsMeteo').text = \
        str(int(serie.duree.total_seconds() / 60))
    if serie.dtprod is not None:
        _etree.SubElement(elt, 'DtProdSerieObsMeteo').text = \
            datetime2iso(serie.dtprod)
    if serie.dtdeb is not None:
        _etree.SubElement(elt, 'DtDebSerieObsMeteo').text = \
            datetime2iso(serie.dtdeb)
    if serie.dtfin is not None:
        _etree.SubElement(elt, 'DtFinSerieObsMeteo').text = \
            datetime2iso(serie.dtfin)
    if serie.contact is not None:
        _etree.SubElement(elt, 'CdContact').text = serie.contact.code
    if serie.observations is not None:
        obss_el = _etree.SubElement(elt, 'ObssMeteo')
        for obs in serie.observations.itertuples():
            obs_el = _etree.SubElement(obss_el, 'ObsMeteo')
            _etree.SubElement(obs_el, 'DtObsMeteo').text = \
                datetime2iso(obs.Index)
            _etree.SubElement(obs_el, 'ResObsMeteo').text = \
                str(obs.res)
            if not _math.isnan(obs.qua):
                _etree.SubElement(obs_el, 'IndiceQualObsMeteo').text = \
                    str(int(obs.qua))
            _etree.SubElement(obs_el, 'ContxtObsMeteo').text = \
                str(obs.ctxt)
            _etree.SubElement(obs_el, 'QualifObsMeteo').text = \
                str(obs.qal)
            _etree.SubElement(obs_el, 'MethObsMeteo').text = \
                str(obs.mth)
            _etree.SubElement(obs_el, 'StObsMeteo').text = \
                str(obs.statut)
    return elt



def _seriesobselab_to_element(seriesobselab, bdhydro=False, strict=True,
                              version='1.1'):
    if version == '2':
        return _seriesobselab_v2(seriesobselab, bdhydro, strict)
    return _seriesobselab_v1(seriesobselab, bdhydro, strict)

def _seriesobselab_v1(seriesobselab, bdhydro=False, strict=True):
    """Return a <ObssElabHydro> element
    from a list of obselaboreehydro.SerieObsElab.
    """
    if seriesobselab is not None:
        element = _etree.Element('ObssElabHydro')
        # First series are group by typegrd
        dict_series = {}
        for serie in seriesobselab:
            typegrd = serie.typegrd
            # Conversion Sandre V2->V1 QIXnJ -> QIXJ
            if typegrd in ['QmnJ', 'QIXnJ', 'QINnJ', 'HIXnJ', 'HINnJ']:
                typegrd = '{}{}'.format(typegrd[0:-2], typegrd[-1])
            if typegrd not in dict_series:
                dict_series[typegrd] = []
            dict_series[typegrd].append(serie)
        for typegrd, series in dict_series.items():
            typel = _etree.SubElement(element, 'TypsDeGrdObsElabHydro')
            _etree.SubElement(typel, 'TypDeGrdObsElabHydro').text = typegrd
            # add observations
            for serie in series:
                for row in serie.observations.itertuples():
                    typel.append(_obselab_to_element(
                        serie, row, bdhydro=bdhydro, strict=strict))
        # print(_etree.tostring(element, method='xml'))
        return element


def _seriesobselab_v2(seriesobselab, bdhydro=False, strict=True):
    """Return a <ObssElabHydro> element
    from a list of obselaboreehydro.SerieObsElab.
    """
    if seriesobselab is None:
        return

    element = _etree.Element('SeriesObsElaborHydro')
    # First series are group by typegrd
    for serie in seriesobselab:
        element.append(_serieobselab_v2(serie, bdhydro, strict))

    # print(_etree.tostring(element, method='xml'))
    return element


def _serieobselab_v2(serieobselab, bdhydro=False, strict=True):
    if serieobselab is None:
        return
    element = _etree.Element('SerieObsElaborHydro')

    _etree.SubElement(element, 'DtProdSerieObsElaborHydro').text = \
        datetime2iso(serieobselab.dtprod)
    _etree.SubElement(element, 'TypDeGrdSerieObsElaborHydro').text = \
        serieobselab.typegrd

    if serieobselab.pdt is not None:
        _etree.SubElement(element, 'PDTSerieObsElaborHydro').text = \
            str(serieobselab.pdt.to_int())

    if serieobselab.dtdeb is not None:
        _etree.SubElement(element, 'DtDebPlagSerieObsElaborHydro').text = \
            datetime2iso(serieobselab.dtdeb)

    if serieobselab.dtfin is not None:
        _etree.SubElement(element, 'DtFinPlagSerieObsElaborHydro').text = \
            datetime2iso(serieobselab.dtfin)

    if serieobselab.dtdesactivation is not None:
        _etree.SubElement(element, 'DtDesactivationSerieObsElaborHydro').text = \
            datetime2iso(serieobselab.dtdesactivation)

    if serieobselab.dtactivation is not None:
        _etree.SubElement(element, 'DtActivationSerieObsElaborHydro').text = \
            datetime2iso(serieobselab.dtactivation)

    if serieobselab.sysalti is not None:
        _etree.SubElement(element, 'SysAltiSerieObsElaborHydro').text = \
            str(serieobselab.sysalti)

    if serieobselab.glissante is not None:
        _etree.SubElement(element, 'GlissanteSerieObsElaborHydro').text = \
            bool2xml(serieobselab.glissante)

    if serieobselab.dtdebrefalti is not None:
        _etree.SubElement(element, 'DtDebutRefAlti').text = \
            datetime2iso(serieobselab.dtdebrefalti)

    if serieobselab.contact is not None:
        _etree.SubElement(element, 'CdContact').text = \
            serieobselab.contact.code

    if isinstance(serieobselab.entite, _sitehydro.Sitehydro):
        _etree.SubElement(element, 'CdSiteHydro').text = \
            serieobselab.entite.code
    else:
        _etree.SubElement(element, 'CdStationHydro').text = \
            serieobselab.entite.code

    if serieobselab.observations is not None:
        obss = _etree.SubElement(element, 'ObssElaborHydro')
        for obs in serieobselab.observations.itertuples():
            obs_el = _etree.SubElement(obss, 'ObsElaborHydro')
            _etree.SubElement(obs_el, 'DtObsElaborHydro').text = \
                datetime2iso(obs.Index)
            _etree.SubElement(obs_el, 'ResObsElaborHydro').text = \
                str(obs.res)
            _etree.SubElement(obs_el, 'QualifObsElaborHydro').text = \
                str(obs.qal)
            _etree.SubElement(obs_el, 'MethObsElaborHydro').text = \
                str(obs.mth)
            _etree.SubElement(obs_el, 'ContObsElaborHydro').text = \
                str(obs.cnt)
            _etree.SubElement(obs_el, 'StObsElaborHydro').text = \
                str(obs.statut)

    return element


def _seriesobselabmeteo_to_element(seriesmeteo, bdhydro=False, strict=True,
                                   version='1.1'):
    """Return a <SeriesObsElaborMeteo> for Sandre V2"""
    if version != '2':
        return
    if seriesmeteo is None or not seriesmeteo:
        return
    element = _etree.Element('SeriesObsElaborMeteo')
    for seriemeteo in seriesmeteo:
        element.append(_serieobselabmeteo_v2(seriemeteo, bdhydro, strict))
    return element


def _serieobselabmeteo_v2(seriemeteo, bdhydro=False, strict=True):
    """Return a <SeriesObsElaborMeteo> for Sandre V2"""
    if seriemeteo is None:
        return
    element = _etree.Element('SerieObsElaborMeteo')
    if isinstance(seriemeteo.site, _sitehydro.Sitehydro):
        _etree.SubElement(element, 'CdSiteHydro').text = \
            seriemeteo.site.code
    elif isinstance(seriemeteo.site, _sitemeteo.SitemeteoPondere):
        _etree.SubElement(element, 'CdSiteMeteo').text = \
            _codesitemeteo_to_value(seriemeteo.site, bdhydro, strict,
                                    version='2')
        _etree.SubElement(element, 'ValPondSiteMeteo').text = \
            str(seriemeteo.site.ponderation)
    _etree.SubElement(element, 'CdGrdSerieObsElaborMeteo').text = \
        seriemeteo.grandeur
    _etree.SubElement(element, 'TypSerieObsElaborMeteo').text = \
        str(seriemeteo.typeserie)
    if seriemeteo.dtdeb is not None:
        _etree.SubElement(element, 'DtDebSerieObsElaborMeteo').text = \
            datetime2iso(seriemeteo.dtdeb)
    if seriemeteo.dtfin is not None:
        _etree.SubElement(element, 'DtFinSerieObsElaborMeteo').text = \
            datetime2iso(seriemeteo.dtfin)
    if seriemeteo.duree is not None:
        _etree.SubElement(element, 'DureeSerieObsElaborMeteo').text = \
            str(int(seriemeteo.duree.total_seconds() / 60))
    if seriemeteo.ipa is not None:
        ipa = _etree.SubElement(element, 'SerieObsElaborMeteoIpa')
        _etree.SubElement(ipa, 'KSerieObsElaborMeteoIpa').text = \
            str(seriemeteo.ipa.coefk)
        if seriemeteo.ipa.npdt is not None:
            _etree.SubElement(ipa, 'PDTSerieObsElaborMeteoIpa').text = \
                str(seriemeteo.ipa.npdt)
    if seriemeteo.observations is not None:
        obss = _etree.SubElement(element, 'ObssElaborMeteo')
        for obs in seriemeteo.observations.itertuples():
            obs_el = _etree.SubElement(obss, 'ObsElaborMeteo')
            _etree.SubElement(obs_el, 'DtObsElaborMeteo').text = \
                datetime2iso(obs.Index)
            _etree.SubElement(obs_el, 'ResObsElaborMeteo').text = \
                str(obs.res)
            if not _numpy.isnan(obs.qua):
                _etree.SubElement(obs_el, 'IndiceQualObsElaborMeteo').text = \
                    str(obs.qua)
            _etree.SubElement(obs_el, 'QualifObsElaborMeteo').text = \
                str(obs.qal)
            _etree.SubElement(obs_el, 'MethObsElaborMeteo').text = \
                str(obs.mth)
            _etree.SubElement(obs_el, 'StObsElaborMeteo').text = \
                str(obs.statut)

    return element


def _seuilshydro_to_element(seuilshydro, ordered=False,
                            bdhydro=False, strict=True, version='1.1'):
    """Return a <SitesHydro> element from a list of seuil.Seuilhydro."""
    if version >= '2':
        return _seuilshydro_to_element_v2(seuilshydro=seuilshydro,
                                          ordered=ordered, bdhydro=bdhydro,
                                          strict=strict, version=version)
    if seuilshydro is not None:
        # the ugly XML doesn't support many Q values within a seuil
        # to deal with that use case, we have to split the values on
        # duplicates seuils
        newseuils = []
        for seuilhydro in seuilshydro:
            if len(seuilhydro.valeurs) > 0:
                valeurs_site = [
                    valeur for valeur in seuilhydro.valeurs
                    if (valeur.entite == seuilhydro.sitehydro)]
                if len(valeurs_site) > 1:
                    for valeur in valeurs_site[1:]:
                        # for each value except the first one, we make a new
                        # Seuilhydro with the same code and a uniq value
                        seuil = _seuil.Seuilhydro(
                            sitehydro=seuilhydro.sitehydro,
                            code=seuilhydro.code,
                            valeurs=[valeur])
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
                    strict=strict))
        return element


def _seuilshydro_to_element_v2(seuilshydro, ordered=False,
                               bdhydro=False, strict=True, version='2'):
    """Return a <SeuilsHydro> element from a list of seuil.Seuilhydro."""
    if seuilshydro is not None:
        # make the elements
        element = _etree.Element('SeuilsHydro')
        for seuil in seuilshydro:
            element.append(_seuilhydro_to_element(
                    seuilhydro=seuil, bdhydro=bdhydro,
                    strict=strict, version=version))

        return element


def _previsions_to_element(previsions, bdhydro=False, strict=True, version='1.1'):
    """Return a <Prevs> element from a simulation.Previsions."""

    # make element <Prevs>
    element = _etree.Element('Prevs')

    # this one is very VERY painful #:~/
    if previsions['tend'] is not None:
        # iter by date and add the previsions
        for dte in previsions['tend'].index.levels[0].values:
            prev_elem = _etree.SubElement(element, 'Prev')
            # dte is mandatory...
            prev_elem.append(
                _make_element(
                    tag_name='DtPrev',
                    # dte is a numpy.datetime64 with perhaps nanoseconds
                    # it is better to cast it before getting the isoformat
                    text=datetime2iso(_numpy.datetime64(dte, 's').item())
                )
            )
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # for one date we can have multiple values
            # we put all of them in a dict {prb: res, ...}
            # so that we can pop them on by one
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            prevs = previsions['tend'][dte].to_dict()

            # we begin to deal with the direct tags...
            # order matters: moy, min and max !!
            for tend in ('moy', 'min', 'max'):
                if tend in prevs:
                    prev_elem.append(
                        _make_element(
                            tag_name=PREV_TENDANCE[tend],
                            text=prevs.pop(tend)
                        )
                    )

    if previsions['prb'] is not None:
        # iter by date and add the previsions
        for dte in previsions['prb'].index.levels[0].values:
            prev_elem = _etree.SubElement(element, 'Prev')
            # dte is mandatory...
            prev_elem.append(
                _make_element(
                    tag_name='DtPrev',
                    # dte is a numpy.datetime64 with perhaps nanoseconds
                    # it is better to cast it before getting the isoformat
                    text=datetime2iso(_numpy.datetime64(dte, 's').item())))
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # for one date we can have multiple values
            # we put all of them in a dict {prb: res, ...}
            # so that we can pop them on by one
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            prevs = previsions['prb'][dte].to_dict()

            # ... and then with the remaining <ProbPrev> elements
            if len(prevs) > 0:
                probsprev_elem = _etree.SubElement(prev_elem, 'ProbsPrev')
                # we sort the result by prob ascending order
                probs = list(prevs.keys())
                probs.sort()
                # add elems
                for prob in probs:
                    probprev_elem = _etree.SubElement(
                        probsprev_elem, 'ProbPrev')
                    probprev_elem.append(
                        _make_element(tag_name='PProbPrev', text=prob))
                    probprev_elem.append(
                        _make_element(
                            tag_name='ResProbPrev', text=prevs.pop(prob)))

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
    for tag, rule in story.items():

        # DEBUG - print(rule)

        # recursif call for sub-element
        if 'sub' in rule:
            child = _etree.SubElement(root, tag)
            root.append(_factory(root=child, story=rule.get('sub')))

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
                    _make_element(tag_name=tag, text=text, tag_attrib=attr))

    # return
    return root


def _make_element(tag_name, text, tag_attrib=None):
    """Return etree.Element <tag_name {attrib}>unicode(text)</tag_name>."""
    # DEBUG - print(locals())
    element = _etree.Element(_tag=tag_name, attrib=tag_attrib)
    if text is not None:
        element.text = str(text)
    return element


def datetime2iso(date):
    """Formatage au format iso d'une date supportant les dates avant 1900
    Arguments:
        date (datetime) = date à convertir
    """
    if date is None:
        return None
    return ('{0.year:04d}-{0.month:02d}-{0.day:02d}'
            'T{0.hour:02d}:{0.minute:02d}:{0.second:02d}').format(date)


def date2iso(date):
    """Formatage au format iso d'une date sans l'heure
    supportant les dates avant 1900
    Arguments:
        date (datetime) = date à convertir
    """
    if date is None:
        return None
    return ('{0.year:04d}-{0.month:02d}-{0.day:02d}').format(date)


def bool2xml(boolean):
    """Conversion boolean en texte"""
    return str(boolean).lower() if boolean is not None else None


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
                    attr=attr, obj=str(obj)))
    return True

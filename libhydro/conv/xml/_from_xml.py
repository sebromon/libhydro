# coding: utf-8
"""Module xml._from_xml.

Ce module expose la classe:
    # Scenario

Il contient les fonctions de lecture des fichiers au format
XML Hydrometrie (version 1.1 exclusivement).

Toutes les heures sont considerees UTC si le fuseau horaire n'est pas precise.

Les fonctions de ce module sont a usage prive, il est recommande d'utiliser la
classe xml.Message comme interface aux fichiers XML Hydrometrie.

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import datetime as _datetime
import collections as _collections

from lxml import etree as _etree

from libhydro.core import (
    _composant, intervenant as _intervenant, sitehydro as _sitehydro,
    sitemeteo as _sitemeteo, seuil as _seuil,
    modeleprevision as _modeleprevision, obshydro as _obshydro,
    obsmeteo as _obsmeteo, simulation as _simulation, evenement as _evenement,
    courbetarage as _courbetarage, courbecorrection as _courbecorrection,
    jaugeage as _jaugeage, obselaboreehydro as _obselaboreehydro,
    obselaboreemeteo as _obselaboreemeteo)

from libhydro.conv.xml import sandre_tags as _sandre_tags

# -- strings ------------------------------------------------------------------
# contributor Camillo Montes (SYNAPSE)
# contributor Sébastien ROMON
__version__ = '0.7.5'
__date__ = '2017-09-22'

# HISTORY
# SR - 2017-09-25 get type capteur from xml
# V0.7.5 - SR - 2017-09-22
# get entitehydro, tronconhydro, zonehydro
# and precisioncoursdeau of site from xml
# V0.7.4 - SR - 2017-09-19
#  get pdt of grandeur from xml
# V0.7.3 - SR - 2017-09-05
# get plages d'utilisation of station and capteur from xml
# V0.7.2 - SR - 2017-07-18
# get some properties of station from xml
# V0.7.1 - SR - 2017-07-05
# import jaugeages
# V0.7 - SR - 2017-06-22
# importation des courbes de correction
# V0.6 - SR - 2017-06-20
# importation courbes de tarage
# V0.5.4 - SR - 2017-06-09
# add SysAltiSerie and SeriePerim elements
# V0.5.3
# Séparation des prévisions en deux pandas : prévisions de tendande et
# et prévisions probabilistes
# V0.5 - 2017-04-20
#   fix numpy deprecated warnings around sort()
#   absence de contact dans l'emetteur et le destinataire si absence de
#     la balise CdContact
#   balise CdContact non obigatoire pour les series hydro
#   fix the Contact.code type
#   some refactoring
# V0.4 - 2014-08-22
#   factorize the global functions
#   add the intervenants
# V0.3 - 2014-07-31
#   add the modelesprevision element
#   change the Scenario.emetteur and destinataire properties
# V0.2 - 2014-07-21
#   add the sitesmeteo and seriesmeteo elements
# V0.1 - 2013-08-18
#   first shot


# -- todos --------------------------------------------------------------------
# FIXME- move the Scenario class and the named tuples in the _xml module
# FIXME- factorize Scenario.emetteur and destinataire properties, as well as
#        others Intervenants or Contacts
# TODO - if xpath is too slow to acess elements, use indexing
#        code=element[0].text,
#        but xpath is more readable and do not care of XML order
# TODO - XSD validation


# -- config -------------------------------------------------------------------
PREV_PROBABILITY = {'ResMoyPrev': 50, 'ResMinPrev': 0, 'ResMaxPrev': 100}
PREV_TENDANCE = {'ResMoyPrev': 'moy', 'ResMinPrev': 'min', 'ResMaxPrev': 'max'}

SANDRE_VERSIONS = ('1.1', '2')

# -- Emetteur and Destinataire named tuples -----------------------------------
Emetteur = _collections.namedtuple('Emetteur', ['intervenant', 'contact'])
Destinataire = _collections.namedtuple(
    'Destinataire', ['intervenant', 'contact'])


# -- class Scenario -----------------------------------------------------------
class Scenario(object):

    """Classe Scenario.

    Classe pour manipuler les scenarios des messages SANDRE.

    Proprietes:
        code = hydrometrie
        version = 1.1
        nom = 'Echange de donnees hydrometriques'
        dtprod (datetime.datetime) = date de production
        emetteur.intervenant (intervenant.Intervenant)
        emetteur.contact (Intervenant.Contact ou None)
        destinataire.intervenant (intervenant.Intervenant)
        destinataire.contact (Intervenant.Contact ou None)

    Emetteur et destinataire sont des collections.namedtuple et ne peuvent
    etre modifies que via la methode _replace().

    """

    # Scenario other properties

    # reference
    # envoi
    # contexte

    # class attributes
    code = 'hydrometrie'
    nom = 'Echange de données hydrométriques'

    # descriptors
    dtprod = _composant.Datefromeverything(required=True)

    def __init__(self, emetteur, destinataire, dtprod=None, version='1.1'):
        """Constructeur.

        Arguments:
            emetteur (intervenant.Intervenant ou Contact) = si un contact
                est utilise, sa propriete Intervenant doit etre renseignee
            destinataire (intervenant.Intervenant ou Contact) = si un contact
                est utilise, sa propriete Intervenant doit etre renseignee
            dtprod (numpy.datetime64 string, datetime.datetime...,
                defaut utcnow()) = date de production
            version (str) = version du Sandre 1.1 ou 2

        """
        # -- descriptors --
        self.dtprod = dtprod or _datetime.datetime.utcnow()

        # -- full properties --
        self._emetteur = Emetteur(None, None)
        self._destinataire = Destinataire(None, None)
        self.emetteur = emetteur
        self.destinataire = destinataire
        self._version = None
        self.version = version

    # -- property version --
    @property
    def version(self):
        """Return message Sandre version."""
        return self._version

    @version.setter
    def version(self, version):
        """Set Sandre version."""
        if version is None:
            raise TypeError('Sandre version is required')
        version = str(version)
        if version not in SANDRE_VERSIONS:
            raise ValueError('Sandre version must be in (\'{}\')'.format(
                '\', \''.join(SANDRE_VERSIONS)))
        self._version = version

    # -- property emetteur --
    @property
    def emetteur(self):
        """Return message emetteur."""
        return self._emetteur

    @emetteur.setter
    def emetteur(self, emetteur):
        """Set message emetteur."""
        if emetteur is None:
            raise TypeError('emetteur is required')
        elif isinstance(emetteur, _intervenant.Intervenant):
            try:
                # we try to use the first contact
                self._emetteur = Emetteur(emetteur, emetteur.contacts[0])
            except Exception:
                self._emetteur = Emetteur(emetteur, None)
        elif isinstance(emetteur, _intervenant.Contact):
            if not isinstance(emetteur.intervenant, _intervenant.Intervenant):
                raise TypeError(
                    'using a Contact without intervenant for an emetteur '
                    'is forbidden')
            self._emetteur = Emetteur(emetteur.intervenant, emetteur)
        else:
            raise TypeError('emetteur must be an Intervenant or a Contact')

    # -- property destinataire --
    @property
    def destinataire(self):
        """Return message destinataire."""
        return self._destinataire

    @destinataire.setter
    def destinataire(self, destinataire):
        """Set message destinataire."""
        if destinataire is None:
            raise TypeError('destinataire is required')
        elif isinstance(destinataire, _intervenant.Intervenant):
            try:
                # we try to use the first contact
                self._destinataire = Destinataire(
                    destinataire, destinataire.contacts[0])
            except Exception:
                self._destinataire = Destinataire(destinataire, None)
        elif isinstance(destinataire, _intervenant.Contact):
            if not isinstance(
                    destinataire.intervenant, _intervenant.Intervenant):
                raise TypeError(
                    'using a Contact without intervenant for an destinataire '
                    'is forbidden')
            self._destinataire = Destinataire(
                destinataire.intervenant, destinataire)
        else:
            raise TypeError('destinataire must be an Intervenant or a Contact')

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Message du {dt} de version {ver}\n Emetteur: {ei} [{ec}]\n' \
               'Destinataire: {di} [{dc}]'.format(
                   dt=self.dtprod,
                   ei=str(self.emetteur.intervenant),
                   ec=str(self.emetteur.contact) or '<sans contact>',
                   di=str(self.destinataire.intervenant),
                   dc=str(self.destinataire.contact) or '<sans contact>',
                   ver=self.version)

    __str__ = _composant.__str__


# -- tests function -----------------------------------------------------------
def _parse(src, ordered=True):
    """Return objects from XML source file.

    Cette fonction est destinee au tests unitaires. Les utilisateurs sont
    invites a utiliser la classe xml.Message comme interface de lecture des
    fichiers XML Hydrometrie.

    Arguments:
        src (nom de fichier, url, objet fichier...) = source de donnee. Les
            type de src acceptes sont ceux de lxml.etree.parse
        ordered (bool)

    Retourne un dictionnaire avec les cles:
            # scenario: xml.Scenario
            # intervenants: liste d'intervenant.Intervenant
            # siteshydro: liste de sitehydro.Siteshydro
            # sitesmeteo: liste de sitehydro.Siteshydro
            # seuilshydro: liste de seuil.Seuilhydro
            # modelesprevision: liste de modelesprevision.Modeleprevision
            # evenements: liste d'evenements
            # courbestarage: liste de courbes de tarage
            # jaugeages: liste des jaugeages
            # courbescorrection: liste de courbes de correction
            # serieshydro: liste de obshydro.Serie
            # seriesmeteo: liste de obsmeteo.Serie
            # seriesobselab: liste de obselaboreehydro.SerieObsElab
            # seriesobselabmeteo: liste de obselaboreemeteo.SerieObsElabMeteo
            # simulations: liste de simulation.Simulation
    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WARNING: the XML is awful for the seuils, which should be first order
    #          classes. When we read a file containing seuils which are
    #          included in a Site element, we have to instantiate the site AND
    #          the seuils
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # read the file
    parser = _etree.XMLParser(
        remove_blank_text=True, remove_comments=True, ns_clean=True)
    tree = _etree.parse(src, parser=parser)

    # deal with namespaces
    # TODO - we could certainly do better with namespaces
    if tree.getroot().nsmap != {}:
        raise ValueError("can't parse xml file with namespaces")

    scenario = _scenario_from_element(tree.find('Scenario'))

    if scenario.version == '2':
        tags = _sandre_tags.SandreTagsV2
        seriesmeteo = _seriesmeteo_from_element_v2(
            tree.find('Donnees/SeriesObsMeteo'))
        seriesobselab = _seriesobselab_from_element_v2(
            tree.find('Donnees/' + tags.seriesobselabhydro))
        seriesobselabmeteo = _seriesobselabmeteo_from_element_v2(
            tree.find('Donnees/SeriesObsElaborMeteo'))
    else:
        tags = _sandre_tags.SandreTagsV1
        # on récupére des obs élaboré depuis des séries météo
        seriesmeteo, seriesobselabmeteo = _seriesmeteo_from_element(
            tree.find('Donnees/ObssMeteo'))
        seriesobselab = _seriesobselab_from_element(
            tree.find('Donnees/' + tags.seriesobselabhydro))

    return {
        'scenario': scenario,
        'intervenants': _intervenants_from_element(
            tree.find('RefHyd/Intervenants')),
        'siteshydro': _siteshydro_from_element(tree.find('RefHyd/SitesHydro')),
        'sitesmeteo': _sitesmeteo_from_element(tree.find('RefHyd/SitesMeteo')),
        'seuilshydro': _seuilshydro_from_element(
            element=tree.find('RefHyd/SitesHydro'), ordered=ordered),
        'modelesprevision': _modelesprevision_from_element(
            tree.find('RefHyd/ModelesPrevision')),
        'evenements': _evenements_from_element(
            tree.find('Donnees/Evenements')),
        'courbestarage': _courbestarage_from_element(
            tree.find('Donnees/CourbesTarage')),
        'jaugeages': _jaugeages_from_element(
            tree.find('Donnees/Jaugeages')),
        'courbescorrection': _courbescorrection_from_element(
            tree.find('Donnees/CourbesCorrH')),
        'serieshydro': _serieshydro_from_element(
            tree.find('Donnees/' + tags.serieshydro),
            version=scenario.version, tags=tags),
        'seriesmeteo': seriesmeteo,
        'seriesobselab': seriesobselab,
        'seriesobselabmeteo': seriesobselabmeteo,
        # 'gradshydro'
        # 'qualifsannee'
        # 'alarmes'
        'simulations': _simulations_from_element(tree.find('Donnees/Simuls'))}


# -- atomic functions ---------------------------------------------------------
def _scenario_from_element(element):
    """Return a xml.Scenario from a <Scenario> element."""
    if element is not None:
        # emetteur pas de contacts si absence de balise CdContact
        emetteur_contacts = None
        emetteur_cdcontact = _value(element.find('Emetteur'), 'CdContact')
        if emetteur_cdcontact is not None:
            emetteur_contacts = _intervenant.Contact(code=emetteur_cdcontact)
        # destinataire pas de contacts si absence de balise CdContact
        dest_contacts = None
        dest_cdcontact = _value(element.find('Destinataire'), 'CdContact')
        if dest_cdcontact is not None:
            dest_contacts = _intervenant.Contact(code=dest_cdcontact)

        return Scenario(
            emetteur=_intervenant.Intervenant(
                code=_value(element.find('Emetteur'), 'CdIntervenant'),
                nom=_value(element.find('Emetteur'), 'NomIntervenant'),
                contacts=emetteur_contacts,),
            destinataire=_intervenant.Intervenant(
                code=_value(element.find('Destinataire'), 'CdIntervenant'),
                nom=_value(element.find('Destinataire'), 'NomIntervenant'),
                contacts=dest_contacts,),
            dtprod=_value(element, 'DateHeureCreationFichier'),
            version=_value(element, 'VersionScenario'))


def _intervenant_from_element(element):
    """Return a intervenant.Intervenant from a <Intervenant> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdIntervenant', int)
        args['origine'] = element.find('CdIntervenant').attrib[
            'schemeAgencyID']
        args['nom'] = _value(element, 'NomIntervenant')
        args['mnemo'] = _value(element, 'MnIntervenant')
        args['contacts'] = [_contact_from_element(e)
                            for e in element.findall('Contacts/Contact')]
        # build an Intervenant
        intervenant = _intervenant.Intervenant(**args)
        # update the Contacts
        for contact in intervenant.contacts:
            contact.intervenant = intervenant
        # return
        return intervenant


def _contact_from_element(element, intervenant=None):
    """Return a intervenant.Contact from a <Contact> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdContact')
        args['nom'] = _value(element, 'NomContact')
        args['prenom'] = _value(element, 'PrenomContact')
        args['civilite'] = _value(element, 'CiviliteContact', int)
        args['intervenant'] = intervenant
        args['profil'] = _value(element, 'ProfilContact')
        args['motdepasse'] = _value(element, 'MotPassContact')
        # build a Contact and return
        return _intervenant.Contact(**args)


def _sitehydro_from_element(element):
    """Return a sitehydro.Sitehydro from a <SiteHydro> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdSiteHydro')
        args['codeh2'] = _value(element, 'CdSiteHydroAncienRef')
        typesite = _value(element, 'TypSiteHydro')
        if typesite is not None:
            args['typesite'] = typesite
        args['libelle'] = _value(element, 'LbSiteHydro')
        args['libelleusuel'] = _value(element, 'LbUsuelSiteHydro')
        args['coord'] = _coord_from_element(
            element.find('CoordSiteHydro'), 'SiteHydro')
        args['stations'] = [
            _station_from_element(e)
            for e in element.findall('StationsHydro/StationHydro')]
        args['communes'] = [
            str(e.text) for e in element.findall('CdCommune')]
        args['tronconsvigilance'] = [
            _tronconvigilance_from_element(e)
            for e in element.findall(
                'TronconsVigilanceSiteHydro/TronconVigilanceSiteHydro')]
        args['entitehydro'] = _value(element, 'CdEntiteHydrographique')
        args['tronconhydro'] = _value(element, 'CdTronconHydrographique')
        args['zonehydro'] = _value(element, 'CdZoneHydro')
        args['precisioncoursdeau'] = _value(element,
                                            'PrecisionCoursDEauSiteHydro')
        # build a Sitehydro and return
        return _sitehydro.Sitehydro(**args)


def _sitemeteo_from_element(element):
    """Return a sitemeteo.Sitemeteo from a <SiteMeteo> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdSiteMeteo')
        args['libelle'] = _value(element, 'LbSiteMeteo')
        args['libelleusuel'] = _value(element, 'LbUsuelSiteMeteo')
        args['coord'] = _coord_from_element(
            element.find('CoordSiteMeteo'), 'SiteMeteo')
        args['commune'] = _value(element, 'CdCommune')
        # build a Sitemeteo
        sitemeteo = _sitemeteo.Sitemeteo(**args)
        # add the Grandeurs
        sitemeteo.grandeurs.extend([
            _grandeur_from_element(e, sitemeteo)
            for e in element.findall('GrdsMeteo/GrdMeteo')])
        # return
        return sitemeteo


def _tronconvigilance_from_element(element):
    """Return a sitehydro.Tronconvigilance from a <TronconVigilanceSiteHydro>
    element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdTronconVigilance')
        args['libelle'] = _value(element, 'NomCTronconVigilance')
        # build a Tronconvigilance and return
        return _sitehydro.Tronconvigilance(**args)


def _station_from_element(element):
    """Return a sitehydro.Station from a <StationHydro> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdStationHydro')
        args['codeh2'] = _value(element, 'CdStationHydroAncienRef')
        typestation = _value(element, 'TypStationHydro')
        if typestation is not None:
            args['typestation'] = typestation
        args['libelle'] = _value(element, 'LbStationHydro')
        args['libellecomplement'] = _value(
            element, 'ComplementLibelleStationHydro')
        args['descriptif'] = _value(element, 'DescriptifStationHydro')
        args['dtmaj'] = _value(element, 'DtMAJStationHydro')
        args['pointk'] = _value(element, 'PkStationHydro', float)
        args['dtmiseservice'] = _value(
            element, 'DtMiseServiceStationHydro')
        args['dtfermeture'] = _value(element, 'DtFermetureStationHydro')
        args['surveillance'] = _value(element, 'ASurveillerStationHydro', bool)
        niveauaffichage = _value(element, 'NiveauAffichageStationHydro')
        if niveauaffichage is not None:
            args['niveauaffichage'] = niveauaffichage
        args['coord'] = _coord_from_element(
            element.find('CoordStationHydro'), 'StationHydro')
        args['plages'] = [
            _plage_from_element(e, 'StationHydro')
            for e in element.findall(
                'PlagesUtilStationHydro/PlageUtilStationHydro')]
        args['capteurs'] = [
            _capteur_from_element(e)
            for e in element.findall('Capteurs/Capteur')]
        args['commune'] = _value(element, 'CdCommune')
        args['ddcs'] = [str(e.text) for e in element.findall(
            'ReseauxMesureStationHydro/CodeSandreRdd')]
        # build a Station and return
        return _sitehydro.Station(**args)


def _coord_from_element(element, entite):
    """Return a dict {'x': x, 'y': y, 'proj': proj}.

    Arg entite is the xml element suffix, a string in
    (SiteHydro, StationHydro).

    """
    if element is not None:
        coord = {}
        coord['x'] = _value(element, 'CoordX%s' % entite, float)
        coord['y'] = _value(element, 'CoordY%s' % entite, float)
        coord['proj'] = _value(element, 'ProjCoord%s' % entite, int)
        return coord


def _plage_from_element(element, entite):
    """Return a sitehydro.PlageUtil

    from a <PlageUtilStationHydro> element or >PlageUtilCapteur> element

    Arg entite is the xml element suffix, a string in
    (StationHydro, Capteur).

    """
    if element is None:
        return None
    args = {}
    args['dtdeb'] = _value(element, 'DtDebPlageUtil{}'.format(entite))
    args['dtfin'] = _value(element, 'DtFinPlageUtil{}'.format(entite))
    args['dtactivation'] = _value(element,
                                  'DtActivationPlageUtil{}'.format(entite))
    args['dtdesactivation'] = _value(element,
        'DtDesactivationPlageUtil{}'.format(entite))
    args['active'] = _value(element, 'ActivePlageUtil{}'.format(entite), bool)
    return _sitehydro.PlageUtil(**args)


def _capteur_from_element(element):
    """Return a sitehydro.Capteur from a <Capteur> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdCapteur')
        args['codeh2'] = _value(element, 'CdCapteurAncienRef')
        args['libelle'] = _value(element, 'LbCapteur')
        typecapteur = _value(element, 'TypCapteur')
        if typecapteur is not None:
            args['typecapteur'] = typecapteur
        typemesure = _value(element, 'TypMesureCapteur')
        if typemesure is not None:
            args['typemesure'] = typemesure
        args['plages'] = [
            _plage_from_element(e, 'Capteur')
            for e in element.findall(
                'PlagesUtilCapteur/PlageUtilCapteur')]
        # build a Capteur and return
        return _sitehydro.Capteur(**args)


def _grandeur_from_element(element, sitemeteo=None):
    """Return a sitemeteo.Grandeur from a <GrdMeteo> element."""
    if element is not None:
        # prepare args
        args = {}
        args['typemesure'] = _value(element, 'CdGrdMeteo')
        if sitemeteo is not None:
            args['sitemeteo'] = sitemeteo
        args['pdt'] = _value(element, 'PasDeTempsNominalGrdMeteo', int)
        # build a Grandeur and return
        return _sitemeteo.Grandeur(**args)


def _seuilhydro_from_element(element, sitehydro):
    """Return a seuil.Seuilhydro from a <ValeursSeuilSiteHydro> element."""
    if element is not None:
        # prepare args
        args = {}
        args['sitehydro'] = sitehydro
        args['code'] = _value(element, 'CdSeuilSiteHydro')
        typeseuil = _value(element, 'TypSeuilSiteHydro')
        if typeseuil is not None:
            args['typeseuil'] = typeseuil
        duree = _value(element, 'DureeSeuilSiteHydro')
        if duree is not None:
            args['duree'] = duree
        args['nature'] = _value(element, 'NatureSeuilSiteHydro')
        args['libelle'] = _value(element, 'LbUsuelSeuilSiteHydro')
        args['mnemo'] = _value(element, 'MnemoSeuilSiteHydro')
        args['gravite'] = _value(element, 'IndiceGraviteSeuilSiteHydro')
        args['commentaire'] = _value(element, 'ComSeuilSiteHydro')
        args['publication'] = _value(
            element, 'DroitPublicationSeuilSiteHydro', bool)
        args['valeurforcee'] = _value(element, 'ValForceeSeuilSiteHydro')
        args['dtmaj'] = _value(element, 'DtMajSeuilSiteHydro')
        seuil = _seuil.Seuilhydro(**args)
        # add the values
        args['valeurs'] = []
        valeurseuil = _valeurseuilsitehydro_from_element(
            element, sitehydro, seuil)
        if valeurseuil is not None:
            args['valeurs'].append(valeurseuil)
        args['valeurs'].extend([
            _valeurseuilstation_from_element(e, seuil)
            for e in element.findall(
                './ValeursSeuilsStationHydro/ValeursSeuilStationHydro')])
        # build a Seuilhydro and return
        # FIXME - why do we use a second Seuilhydro ????
        return _seuil.Seuilhydro(**args)


def _valeurseuilsitehydro_from_element(element, sitehydro, seuil):
    """Return a seuil.Valeurseuil from a <ValeursSeuilSiteHydro> element."""
    if element is not None:
        # prepare args
        args = {}
        valeur = _value(element, 'ValDebitSeuilSiteHydro')
        if valeur is None:
            # Q can be None if the seuil has only H values
            # all other Valeurseuil related tags are ignored
            return
        args['valeur'] = valeur
        args['seuil'] = seuil
        args['entite'] = sitehydro
        args['tolerance'] = _value(element, 'ToleranceSeuilSiteHydro')
        args['dtactivation'] = _value(
            element, 'DtActivationSeuilSiteHydro')
        args['dtdesactivation'] = _value(
            element, 'DtDesactivationSeuilSiteHydro')
        # build a Valeurseuil and return
        return _seuil.Valeurseuil(**args)


def _valeurseuilstation_from_element(element, seuil):
    """Return a seuil.Valeurseuil from a <ValeursSeuilStationHydro> element."""
    if element is not None:
        # prepare args
        args = {}
        args['valeur'] = _value(element, 'ValHauteurSeuilStationHydro')
        args['seuil'] = seuil
        args['entite'] = _sitehydro.Station(
            code=_value(element, 'CdStationHydro'))
        args['tolerance'] = _value(element, 'ToleranceSeuilStationHydro')
        args['dtactivation'] = _value(
            element, 'DtActivationSeuilStationHydro')
        args['dtdesactivation'] = _value(
            element, 'DtDesactivationSeuilStationHydro')
        # build a Valeurseuil and return
        return _seuil.Valeurseuil(**args)


def _modeleprevision_from_element(element):
    """Return a modeleprevision.Modeleprevision from a """
    """<ModelePrevision> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdModelePrevision')
        args['libelle'] = _value(element, 'LbModelePrevision')
        args['typemodele'] = _value(element, 'TypModelePrevision', int)
        args['description'] = _value(element, 'DescModelePrevision')
        # build a Modeleprevision and return
        return _modeleprevision.Modeleprevision(**args)


def _evenement_from_element(element):
    """Return a evenement.Evenement from a <Evenement> element."""
    if element is not None:
        # prepare args
        # entite can be a Sitehydro, a Station or a Sitemeteo
        entite = None
        if element.find('CdSiteHydro') is not None:
            entite = _sitehydro.Sitehydro(
                code=_value(element, 'CdSiteHydro'))
        elif element.find('CdStationHydro') is not None:
            entite = _sitehydro.Station(
                code=_value(element, 'CdStationHydro'))
        elif element.find('CdSiteMeteo') is not None:
            entite = _sitemeteo.Sitemeteo(
                code=_value(element, 'CdSiteMeteo'))
        # build an Evenement and return
        return _evenement.Evenement(
            entite=entite,
            descriptif=_value(element, 'DescEvenement'),
            contact=_intervenant.Contact(
                code=_value(element, 'CdContact')),
            dt=_value(element, 'DtEvenement'),
            publication=_value(element, 'TypPublicationEvenement'),
            dtmaj=_value(element, 'DtMajEvenement'))

def _courbetarage_from_element(element):
    """Return a courbetarage.CourbeTarage from a <CourbeTarage> element."""
    if element is None:
        raise TypeError("CourbesTarage must not be empty")
    # build a Contact
    # balise CodeContact Non obligatoire
    contact = None
    if element.find('CdContact') is not None:
        contact = _intervenant.Contact(code=_value(element, 'CdContact'))
    typect = _value(element, 'TypCourbeTarage', int)
    args = {
        'code': _value(element, 'CdCourbeTarage'),
        'libelle': _value(element, 'LbCourbeTarage'),
        'typect': typect,
        'limiteinf': _value(element, 'LimiteInfCourbeTarage', float),
        'limitesup': _value(element, 'LimiteSupCourbeTarage', float),
        'dn': _value(element, 'DnCourbeTarage', float),
        'alpha': _value(element, 'AlphaCourbeTarage', float),
        'beta': _value(element, 'BetaCourbeTarage', float),
        'commentaire': _value(element, 'ComCourbeTarage'),
        'station': _sitehydro.Station(code=_value(element, 'CdStationHydro')),
        'contact': contact,
        'pivots': [_pivotct_from_element(e, typect)
            for e in element.findall('PivotsCourbeTarage/PivotCourbeTarage')],
        'periodes': [_periodect_from_element(e)
            for e in element.findall(('PeriodesUtilisationCourbeTarage/'
                                      'PeriodeUtilisationCourbeTarage'))],
        'dtmaj': _value(element, 'DtMajCourbeTarage')
        }

    return _courbetarage.CourbeTarage(**args)


def _pivotct_from_element(element, typect):
    """Return PivotCTPuissance if typect = 4
       or PivotCTPoly if typect = 0
       from  <PivotsCourbeTarage> element.

    """
    # qualif is not mandatory
    args = {'hauteur': _value(element, 'HtPivotCourbeTarage', float)}
    qualif = _value(element, 'QualifPivotCourbeTarage', int)
    if qualif is not None:
        args['qualif'] = qualif
    if typect == 0:
        args['debit'] = _value(element, 'QPivotCourbeTarage', float)
        return _courbetarage.PivotCTPoly(**args)
    elif typect == 4:
        args['vara'] = _value(element, 'VarAPivotCourbeTarage', float)
        args['varb'] = _value(element, 'VarBPivotCourbeTarage', float)
        args['varh'] = _value(element, 'VarHPivotCourbeTarage', float)
        return _courbetarage.PivotCTPuissance(**args)
    else:
        raise ValueError('TypCourbeTarage must be 0 or 4')


def _periodect_from_element(element):
    """Return a PeriodeCT from  <PeriodeUtilisationCourbeTarage> element."""
    return _courbetarage.PeriodeCT(
        dtdeb=_value(element, 'DtDebutPeriodeUtilisationCourbeTarage'),
        dtfin=_value(element, 'DtFinPeriodeUtilisationCourbeTarage'),
        etat=_value(element, 'EtatPeriodeUtilisationCourbeTarage', int),
        histos=[_histoactiveperiode_from_element(e)
            for e in element.findall('HistosActivPeriod/HistoActivPeriod')]
        )

def _histoactiveperiode_from_element(element):
    """Return HistoActivePeriode from <HistoActivPeriod>"""
    return _courbetarage.HistoActivePeriode(
        dtactivation=_value(element, 'DtActivHistoActivPeriod'),
        dtdesactivation=_value(element, 'DtDesactivHistoActivPeriod')
        )


def _jaugeage_from_element(element):
    """Return a jaugeage.Jaugeage from a <Jaugeage> element."""
    if element is None:
        raise TypeError("Jaugeages must not be empty")

    codesite = _value(element, 'CdSiteHydro')
    site = _sitehydro.Sitehydro(code=codesite)
    # mode not mandatory -> constructor default value
    mode = _value(element, 'ModeJaugeage', int)
    args = {
        'code': _value(element, 'CdJaugeage'),
        'dte': _value(element, 'DtJaugeage'),
        'debit': _value(element, 'DebitJaugeage', float),
        'dtdeb': _value(element, 'DtDebJaugeage'),
        'dtfin': _value(element, 'DtFinJaugeage'),
        'section_mouillee': _value(element, 'SectionMouilJaugeage', float),
        'perimetre_mouille': _value(element, 'PerimMouilleJaugeage', float),
        'largeur_miroir': _value(element, 'LargMiroirJaugeage', float),
        'commentaire': _value(element, 'ComJaugeage'),
        'vitessemoy': _value(element, 'VitesseMoyJaugeage', float),
        'vitessemax': _value(element, 'VitesseMaxJaugeage', float),
        'vitessemoy_surface': _value(element, 'VitesseMoySurfaceJaugeage',
                                     float),
        'site': site,
        'hauteurs': [_hjaug_from_element(e)
            for e in element.findall('HauteursJaugeage/HauteurJaugeage')],
        'dtmaj': _value(element, 'DtMajJaugeage')
        }
    if mode is not None:
        args['mode'] = mode

    return _jaugeage.Jaugeage(**args)


def _hjaug_from_element(element):
    """Return a jaugeage.HauteurJaugeage from a <HauteurJaugeage> element."""
    codestation = _value(element, 'CdStationHydro')
    station = _sitehydro.Station(code=codestation)
    stationfille = None
    element_fille = element.find('StationFille')
    if element_fille is not None:
        codestationfille = _value(element_fille, 'CdStationHydro')
        stationfille = _sitehydro.Station(code=codestationfille)
    args = {
        'station': station,
        'sysalti': _value(element, 'SysAltiStationJaugeage'),
        'coteretenue': _value(element, 'CoteRetenueStationJaugeage'),
        'cotedeb': _value(element, 'CoteDebutStationJaugeage'),
        'cotefin': _value(element, 'CoteFinStationJaugeage'),
        'denivele': _value(element, 'DnStationJaugeage'),
        'distancestation': _value(element, 'DistanceStationJaugeage'),
        'stationfille': stationfille,
        'dtdeb_refalti': _value(element, 'DtDebutRefAlti')
        }
    return _jaugeage.HauteurJaugeage(**args)


def _courbecorrection_from_element(element):
    """Return a courbecorrection.CourbeCorrection from a <CourbeCorrH> element."""
    if element is None:
        raise TypeError("CourbesCorrH must not be empty")
    args = {
        'station': _sitehydro.Station(code=_value(element, 'CdStationHydro')),
        'libelle': _value(element, 'LbCourbeCorrH'),
        'commentaire': _value(element, 'ComCourbeCorrH'),
        'pivots': [_pivotcc_from_element(e)
            for e in element.findall('PointsPivot/PointPivot')],
        'dtmaj': _value(element, 'DtMajCourbeCorrH')
        }

    return _courbecorrection.CourbeCorrection(**args)

def _pivotcc_from_element(element):
    """Return courbecorrection.PivotCC from a <PointPivot> element."""
    return _courbecorrection.PivotCC(
        dte=_value(element, 'DtPointPivot'),
        deltah=_value(element, 'DeltaHPointPivot', float),
        dtactivation=_value(element, 'DtActivationPointPivot'),
        dtdesactivation=_value(element, 'DtDesactivPointPivot')
        )

def _seriehydro_from_element(element, version, tags):
    """Return a obshydro.Serie from a <Serie> element."""
    if element is not None:
        # prepare args
        # entite can be a Sitehydro, a Station or a Capteur
        if element.find('CdSiteHydro') is not None:
            entite = _sitehydro.Sitehydro(
                code=_value(element, 'CdSiteHydro'))
        elif element.find('CdStationHydro') is not None:
            entite = _sitehydro.Station(
                code=_value(element, 'CdStationHydro'))
        elif element.find('CdCapteur') is not None:
            entite = _sitehydro.Capteur(code=_value(element, 'CdCapteur'))
        # build a Contact
        # balise CodeContact Non obligatoire
        contact = None
        if element.find('CdContact') is not None:
            contact = _intervenant.Contact(code=_value(element, 'CdContact'))

        statut = None
        if version == '1.1':
            statut = _value(element, 'StatutSerie')
        # utilisation d'un dictionnaire afin que sysalti ne soit pas transmis
        # au constructeur si la balide n'existe pas
        args = {
            'entite': entite,
            'grandeur': _value(element, tags.grdseriehydro),
            'dtdeb': _value(element, tags.dtdebseriehydro),
            'dtfin': _value(element, tags.dtfinseriehydro),
            'dtprod': _value(element, tags.dtprodseriehydro),
            'perime': _value(element, tags.serieperimhydro, bool),
            'contact': contact,
            'observations': _obsshydro_from_element(element.find('ObssHydro'),
                                                    statut, version, tags)}
        # balise sysalti
        sysalti = _value(element, tags.sysaltiseriehydro, int)
        if sysalti is not None:
            args['sysalti'] = sysalti

        # balise pdt
        if version == '2':
            pdt_duree = _value(element, tags.pdtseriehydro, int)
            if pdt_duree is not None:
                args['pdt'] = _composant.PasDeTemps(
                    duree=pdt_duree, unite=_composant.PasDeTemps.MINUTES)

        # build a Serie and return
        return _obshydro.Serie(**args)
#        return _obshydro.Serie(
#            entite=entite,
#            grandeur=_value(element, 'GrdSerie'),
#            statut=_value(element, 'StatutSerie'),
#            dtdeb=_value(element, 'DtDebSerie'),
#            dtfin=_value(element, 'DtFinSerie'),
#            dtprod=_value(element, 'DtProdSerie'),
#            sysalti=sysalti,
#            perime=_value(element, 'SeriePerim', bool),
#            contact=contact,
#            observations=_obsshydro_from_element(element.find('ObssHydro')))


def _seriemeteo_from_element(element):
    """Return a obsmeteo.Serie from a <ObsMeteo> element.

    Warning, the serie here does not contains observations, dtdeb or dtfin.

    """
    if element is not None:
                # prepare the duree in minutes
        duree = _value(element, 'DureeObsMeteo', int) or 0
        # build a Contact
        contact = _intervenant.Contact(code=_value(element, 'CdContact'))

        cdsitemeteo = _value(element, 'CdSiteMeteo')
        if cdsitemeteo is not None:
            # build a Grandeur
            grandeur = _sitemeteo.Grandeur(
                typemesure=_value(element, 'CdGrdMeteo'),
                sitemeteo=_sitemeteo.Sitemeteo(cdsitemeteo))
            # build a Serie without the observations and return
            return _obsmeteo.Serie(
                grandeur=grandeur,
                duree=duree * 60,
                dtprod=_value(element, 'DtProdObsMeteo'),
                contact=contact)
        else:
            sitehydro = _sitehydro.Sitehydro(_value(element, 'CdSiteHydro'))
            return _obselaboreemeteo.SerieObsElabMeteo(site=sitehydro,
                                                       grandeur='RR',
                                                       typeserie=1,
                                                       dtprod=_value(element, 'DtProdObsMeteo'),
                                                       duree=duree * 60)

def _seriemeteo_from_element_v2(element):
    """Return a obsmeteo.Serie from a <SerieObsMeteo> element."""
    if element is None:
        return
    # build a Grandeur
    grandeur = _sitemeteo.Grandeur(
        typemesure=_value(element, 'CdGrdMeteo'),
        sitemeteo=_sitemeteo.Sitemeteo(_value(element, 'CdSiteMeteo')))
    # prepare the duree in minutes
    duree = _value(element, 'DureeSerieObsMeteo', int) or 0
    # build a Contact
    cdcontact = _value(element, 'CdContact')
    if cdcontact is not None:
        contact = _intervenant.Contact(code=cdcontact)
    else:
        contact = None

    # build a Serie without the observations and return
    return _obsmeteo.Serie(
        grandeur=grandeur,
        duree=duree * 60,
        dtprod=_value(element, 'DtProdSerieObsMeteo'),
        dtdeb=_value(element, 'DtDebSerieObsMeteo'),
        dtfin=_value(element, 'DtFinSerieObsMeteo'),
        contact=contact,
        observations=_obssmeteo_from_element(element.find('ObssMeteo'),
                                             version='2')
    )


def _serieobselab_from_element(element):
    """Return a obselaboreehydro.SerieObsElab
       from a TypsDeGrdObsElabHydro element.
    """
    # use an orderdDict to save the order of series
    series = _collections.OrderedDict()
    typegrd = _value(element, 'TypDeGrdObsElabHydro')  # mandatory
    # Conversion Sandre V1.1 to V2 (QmJ ->QmnJ)
    pdt = None
    if typegrd in ['QmJ', 'QIXJ', 'QINJ', 'HIXJ', 'HINJ']:
        typegrd = '{}n{}'.format(typegrd[0:-1], typegrd[-1])
        pdt = _composant.PasDeTemps(duree=1,
                                    unite=_composant.PasDeTemps.JOURS)
    observations = {}
    for obs in element.findall('ObsElabHydro'):
        dtprod = _value(obs, 'DtProdObsElabHydro')
        # CdSiteHydro or CdstationHydro mandatory
        entite = None
        code = None
        if obs.find('CdSiteHydro') is not None:
            code = _value(obs, 'CdSiteHydro')
            entite = _sitehydro.Sitehydro(
                code=code)
        elif obs.find('CdStationHydro') is not None:
            code = _value(obs, 'CdStationHydro')
            entite = _sitehydro.Station(
                code=code)

        args = {}
        args['dte'] = _value(obs, 'DtObsElabHydro')  # mandatory
        args['res'] = _value(obs, 'ResObsElabHydro', float)  # mandatory
        statut = _value(obs, 'StatutObsElabHydro', int)
        if statut is not None:
            args['statut'] = statut
        qal = _value(obs, 'QualifObsElabHydro', int)
        if qal is not None:
            args['qal'] = qal
        mth = _value(obs, 'MethObsElabHydro', int)
        if mth is not None:
            args['mth'] = mth
        sysalti = _value(obs, 'SysAltiObsElabHydro')

        contact = None
        cdcontact = _value(obs, 'CdContact')
        if cdcontact is not None:
            contact = _intervenant.Contact(code=cdcontact)
        dtdebrefalti = _value(obs, 'DtDebutRefAlti')
        # print(args)
        key = (code, typegrd)
        if key not in series:
            series[key] = _obselaboreehydro.SerieObsElab(
                entite=entite, dtprod=dtprod, typegrd=typegrd, pdt=pdt,
                sysalti=sysalti, contact=contact, dtdebrefalti=dtdebrefalti)
            observations[key] = []
        else:
            dtprod = _datetime.datetime.strptime(dtprod, '%Y-%m-%dT%H:%M:%S')
            if dtprod > series[key].dtprod:
                series[key].dtprod = dtprod
        observations[key].append(
            _obselaboreehydro.ObservationElaboree(**args))

    # add observations to series
    for key, serie in series.items():
        serie.observations = _obselaboreehydro.ObservationsElaborees(
            *observations[key]).sort_index()
    return list(series.values())


def _serieobselab_from_element_v2(element):
    """Return a obselaboreehydro.SerieObsElab
       from a SerieObsElaborHydro element.
    """
    args_serie = {}
    if element.find('CdSiteHydro') is not None:
        code = _value(element, 'CdSiteHydro')
        args_serie['entite'] = _sitehydro.Sitehydro(
            code=code)
    elif element.find('CdStationHydro') is not None:
        code = _value(element, 'CdStationHydro')
        args_serie['entite'] = _sitehydro.Station(
            code=code)

    args_serie['dtprod'] = _value(element, 'DtProdSerieObsElaborHydro')

    args_serie['typegrd'] = _value(element, 'TypDeGrdSerieObsElaborHydro')  # mandatory

    unite = None
    if args_serie['typegrd'][-1] == 'J':
        unite = _composant.PasDeTemps.JOURS
    elif args_serie['typegrd'][-1] == 'H':
        unite = _composant.PasDeTemps.HEURES

    pdt = None
    duree = _value(element, 'PDTSerieObsElaborHydro', int)
    if duree is not None:
        args_serie['pdt'] = _composant.PasDeTemps(duree=duree,
                                                  unite=unite)

    args_serie['dtdeb'] = _value(element, 'DtDebPlagSerieObsElaborHydro')
    args_serie['dtfin'] = _value(element, 'DtFinPlagSerieObsElaborHydro')
    args_serie['dtdesactivation'] = _value(
        element, 'DtDesactivationSerieObsElaborHydro')
    args_serie['dtactivation'] = _value(element,
                                        'DtActivationSerieObsElaborHydro')

    sysalti = _value(element, 'SysAltiSerieObsElaborHydro', int)
    if sysalti is not None:
        args_serie['sysalti'] = sysalti

    glissante = _value(element, 'GlissanteSerieObsElaborHydro', bool)
    if glissante is not None:
        args_serie['glissante'] = glissante

    args_serie['dtdebrefalti'] = _value(element, 'DtDebutRefAlti')

    cdcontact = _value(element, 'CdContact')
    if cdcontact is not None:
        args_serie['contact'] = _intervenant.Contact(code=cdcontact)

    serie = _obselaboreehydro.SerieObsElab(**args_serie)

    observations = []
    for obs in element.findall('./ObssElaborHydro/ObsElaborHydro'):
        args = {}
        args['dte'] = _value(obs, 'DtObsElaborHydro')  # mandatory
        args['res'] = _value(obs, 'ResObsElaborHydro', float)  # mandatory

        cnt = _value(obs, 'ContObsElaborHydro', int)
        if cnt is not None:
            args['cnt'] = cnt

        statut = _value(obs, 'StObsElaborHydro', int)
        if statut is not None:
            args['statut'] = statut

        qal = _value(obs, 'QualifObsElaborHydro', int)
        if qal is not None:
            args['qal'] = qal
        mth = _value(obs, 'MethObsElaborHydro', int)
        if mth is not None:
            args['mth'] = mth
        observations.append(_obselaboreehydro.ObservationElaboree(**args))

    # add observations to serie
    if len(observations) > 0:
        serie.observations = _obselaboreehydro.ObservationsElaborees(
            *observations).sort_index()
    return serie


def _obsshydro_from_element(element, statut, version, tags):
    """Return a sorted obshydro.Observations from a <ObssHydro> element."""
    if element is not None:
        # prepare a list of Observation
        observations = []
        for o in element:
            args = {}
            args['dte'] = _value(o, 'DtObsHydro')
            args['res'] = _value(o, 'ResObsHydro')
            if args['res'] is None:
                continue
            mth = _value(o, 'MethObsHydro', int)
            if mth is not None:
                # chgt de liste Sandre V1.1 -> V2
                if mth == 12:
                    mth = 8
                args['mth'] = mth
            qal = _value(o, 'QualifObsHydro', int)
            if qal is not None:
                args['qal'] = qal
            if version == '2':
                continuite = _value(o, 'ContObsHydro', int)
                statut = _value(o, tags.statutobshydro)
                if statut is not None:
                    args['statut'] = statut
            else:
                continuite = _value(o, 'ContObsHydro', bool)
                if statut is not None:
                    args['statut'] = statut  # statut de la série
            if continuite is not None:
                args['cnt'] = continuite

            observations.append(_obshydro.Observation(**args))
        # build the Observations and return
        return _obshydro.Observations(*observations).sort_index()


def _obssmeteo_from_element(element, version):
    """Return a sorted obsmeteo.Observations from a <ObssMeteo> element."""
    if element is None:
        return
    observations = []
    for obs in element:
        observations.append(_obsmeteo_from_element(element=obs,
                                                   version=version))
    # build the Observations and return
    return _obsmeteo.Observations(*observations).sort_index()


def _obsmeteo_from_element(element, version='1.1'):
    """Return a obsmeteo.Observation from a <ObsMeteo> element."""
    if element is not None:
        # prepare args
        args = {}
        args['dte'] = _value(element, 'DtObsMeteo')
        args['res'] = _value(element, 'ResObsMeteo')
        if args['res'] is None:
            return
        mth = _value(element, 'MethObsMeteo', int)
        if mth is not None:
            args['mth'] = mth
        qal = _value(element, 'QualifObsMeteo', int)
        if qal is not None:
            args['qal'] = qal
        qua = _value(element, 'IndiceQualObsMeteo', int)
        if qua is not None:
            args['qua'] = qua

        if version == '2':
            statut = _value(element, 'StObsMeteo', int)
            if statut is not None:
                args['statut'] = statut
        else:
            args['statut'] = _value(element, 'StatutObsMeteo', int)

        if version == '2':
            ctxt = _value(element, 'ContxtObsMeteo', int)
            if ctxt is not None:
                args['ctxt'] = ctxt
        # build the Observation and return
        return _obsmeteo.Observation(**args)


def _simulation_from_element(element):
    """Return a simulation.Simulation from a <Simul> element."""
    if element is not None:
        # prepare args
        # entite can be a Sitehydro or a Station
        entite = None
        if element.find('CdSiteHydro') is not None:
            entite = _sitehydro.Sitehydro(
                code=_value(element, 'CdSiteHydro'))
        elif element.find('CdStationHydro') is not None:
            entite = _sitehydro.Station(
                code=_value(element, 'CdStationHydro'))
        # prepare qualite
        # warning: qualite is int(float())
        qualite = _value(element, 'IndiceQualiteSimul', float)
        if qualite is not None:
            qualite = int(qualite)
        # build a Simulation and return
        previsions = _previsions_from_element(element.find('Prevs'))
        return _simulation.Simulation(
            entite=entite,
            modeleprevision=_modeleprevision.Modeleprevision(
                code=_value(element, 'CdModelePrevision')),
            grandeur=_value(element, 'GrdSimul'),
            statut=_value(element, 'StatutSimul', int),
            qualite=qualite,
            public=_value(element, 'PubliSimul', bool),
            commentaire=_value(element, 'ComSimul'),
            dtprod=_value(element, 'DtProdSimul'),
            #previsions=previsions['all'],
            previsions_tend=previsions['tend'],
            previsions_prb=previsions['prb'],
            intervenant=_intervenant.Intervenant(
                _value(element, 'CdIntervenant')))


def _previsions_from_element(element):
    # prepare
    previsions_tend = []
    previsions_prb = []
    """Return a simulation.Previsions from a <Prevs> element."""
    if element is not None:

        for prev in element:
            dte = _value(prev, 'DtPrev')

            # -------------------
            # compute Res[Min|Moy|Max]Prev
            # -------------------
            # xpath syntax: p.xpath('ResMoyPrev|ResMinPrev|ResMaxPrev')
            for resprev in prev.xpath('|'.join(PREV_PROBABILITY)):
                previsions_tend.append(
                    _simulation.PrevisionTendance(
                        dte=dte, res=resprev.text,
                        tend=PREV_TENDANCE[resprev.tag]))

            # -------------------
            # compute ProbsPrev
            # -------------------
            for probprev in prev.findall('.//ProbPrev'):
                previsions_prb.append(
                    _simulation.PrevisionPrb(
                        dte=dte, res=_value(probprev, 'ResProbPrev', float),
                        prb=_value(probprev, 'PProbPrev', int)))

    # build a Previsions and return
    prvs_tend = _simulation.PrevisionsTendance(*previsions_tend) \
        if len(previsions_tend) > 0 else None
    prvs_prb = _simulation.PrevisionsPrb(*previsions_prb) \
        if len(previsions_prb) > 0 else None
    return {'tend': prvs_tend, 'prb': prvs_prb}


# -- global functions ---------------------------------------------------------
def _global_function_builder(xpath, func):
    """Return a function that returns a list of func(item) for each item in a
    etree.Element returned by the xpath search.

    Arguments:
        xpath (str) = xpath tags to search in etree.Element closure
        func (function object) = elementary function to call on each item

    """
    def closure(elem):
        """Elem should be a etree.Element."""
        items = []
        if elem is not None:
            for item in elem.findall(xpath):
                items.append(func(item))
        return items
    return closure

# return a list of intervenant.Intervenant from a <Intervenants> element
_intervenants_from_element = _global_function_builder(
    './Intervenant', _intervenant_from_element)
# return a list of sitehydro.Sitehydro from a <SitesHydro> element
_siteshydro_from_element = _global_function_builder(
    './SiteHydro', _sitehydro_from_element)
# return a list of sitemeteo.Sitemeteo from a <SitesMeteo> element
_sitesmeteo_from_element = _global_function_builder(
    './SiteMeteo', _sitemeteo_from_element)
# return a list of Modeleprevision from a <ModelesPrevision> element
_modelesprevision_from_element = _global_function_builder(
    './ModelePrevision', _modeleprevision_from_element)
# return a list of evenement.Evenement from a <Evenements> element
_evenements_from_element = _global_function_builder(
    './Evenement', _evenement_from_element)
# return a list of courbetarage.CourbeTarage from a <CourbesTarage> element
_courbestarage_from_element = _global_function_builder(
    './CourbeTarage', _courbetarage_from_element)
# return a list of jaugeage.Jaugeage from a <Jaugeage> element
_jaugeages_from_element = _global_function_builder(
    './Jaugeage', _jaugeage_from_element)
# return a list of courbecorrection.CourbeCorrection from a <CourbesCorrH> element
_courbescorrection_from_element = _global_function_builder(
    './CourbeCorrH', _courbecorrection_from_element)
# return a list of obshydro.Serie from a <Series> element
# _serieshydro_from_element = _global_function_builder(
#     './Serie', _seriehydro_from_element)
# return a list of obsmeteo.Serie from a <SeriesObsMeteo> element
_seriesmeteo_from_element_v2 = _global_function_builder(
    './SerieObsMeteo', _seriemeteo_from_element_v2)
# return a list of simulation.Simulation from a <Simuls> element
_simulations_from_element = _global_function_builder(
    './Simul', _simulation_from_element)


def _serieshydro_from_element(elem, version, tags):
    serieshydro = []
    if elem is not None:
        for item in elem.findall('./' + tags.seriehydro):
            serieshydro.append(_seriehydro_from_element(item, version, tags))
    return serieshydro


# these 2 functions doesn't fit with the _global_function_builder :-\
def _seuilshydro_from_element(element, ordered=False):
    """Return a list of seuil.Seuilhydro from a <SitesHydro> element.

    When ordered is True, we use an OrderedDict to keep the XML initial order.

    """
    # -------------
    # no seuil case
    # -------------
    if ((element is None) or element.find(
            './SiteHydro/ValeursSeuilsSiteHydro/ValeursSeuilSiteHydro')
            is None):
        return []

    # -------------
    # other cases
    # -------------
    # here we get all the seuils and put them in a dictionnary:
    #     {(cdsitehydro, cdseuil): seuil.Seuilhydro,...}
    # grouping similar seuils (bdhydro output is awful!)
    seuilshydro = _collections.OrderedDict() if ordered else {}
    for elementsitehydro in element.findall('./SiteHydro'):
        # FIXME - we should/could use the already build sitehydro
        sitehydro = _sitehydro_from_element(elementsitehydro)
        for elementseuilhydro in elementsitehydro.findall(
                './ValeursSeuilsSiteHydro/ValeursSeuilSiteHydro'):
            seuilhydro = _seuilhydro_from_element(elementseuilhydro, sitehydro)
            if (sitehydro.code, seuilhydro.code) in seuilshydro:
                # check that the seuil complies with it predecessors
                if not seuilhydro.__eq__(
                        other=seuilshydro[(sitehydro.code, seuilhydro.code)],
                        lazzy=True, ignore=['valeurs']):
                    raise ValueError(
                        'seuilhydro %s from sitehydro %s '
                        'has inconsistent metadatas' % (
                            seuilhydro.code, sitehydro.code))
                # change the seuil object in the new seuil values
                # to assure the navigability
                for valeur in seuilhydro.valeurs:
                    valeur.seuil = seuilshydro[
                        (sitehydro.code, seuilhydro.code)]
                # add the valeurs to an existing entry
                seuilshydro[
                    (sitehydro.code, seuilhydro.code)
                ].valeurs.extend(seuilhydro.valeurs)
            else:
                # new entry
                seuilshydro[
                    (sitehydro.code, seuilhydro.code)] = seuilhydro

    # return a list of seuils
    return list(seuilshydro.values())

def _seriesmeteo_from_element(element):
    """Return a list of obsmeteo.Serie from a <ObssMeteo> element.

    Painful because the XML does not contain series:
        # for each <ObsMeteo> we build a serie and obs
        # then we group obs by identical series
        # we make observations (dataframe) after grouping obs
        # at last we sort the series and update dtdeb and dtfin

    """
    seriesmeteo = []  # set()
    serieselabmeteo = []
    # TempSerie : a serie with a list of observations
    # use a temporary serie to make only once a dataframe
    TmpSerie = _collections.namedtuple('TmpSerie', ['serie', 'obss'])
    tmpseriesmeteo = []
    tmpserieselab = []
    if element is not None:

        for obsmeteo in element.findall('./ObsMeteo'):

            ser = _seriemeteo_from_element(obsmeteo)
            obs = _obsmeteo_from_element(obsmeteo, version='1.1')
            if obs is None:
                continue
            if isinstance(ser, _obsmeteo.Serie):
                tmpseries = tmpseriesmeteo
            else:
                tmpseries = tmpserieselab
            for tmpserie in tmpseries:
                # if serie == ser:
                if tmpserie.serie.__eq__(ser, ignore=['observations',
                                                      'dtprod']):

                    tmpserie.obss.append(obs)
                    if ser.dtprod > tmpserie.serie.dtprod:
                        tmpserie.serie.dtprod = ser.dtprod
                    break
            else:
                # new serie
                tmpseries.append(TmpSerie(serie=ser, obss=[obs]))
        # Add observations to serie
        for tmpserie in tmpseriesmeteo:
            serie = tmpserie.serie
            serie.observations = _obsmeteo.Observations(*tmpserie.obss)
            serie.dtdeb = min(serie.observations.index)
            serie.dtfin = max(serie.observations.index)
            seriesmeteo.append(serie)

        # Add observations to serie
        for tmpserie in tmpserieselab:
            serie = tmpserie.serie
            serie.observations = _obsmeteo.Observations(*tmpserie.obss)
            serie.dtdeb = min(serie.observations.index)
            serie.dtfin = max(serie.observations.index)
            serieselabmeteo.append(serie)

    return seriesmeteo, serieselabmeteo


def _seriesobselab_from_element(element):
    """return a list of obselaboreehydro.SerieObsElab
    from a <ObssElabHydro> element
    """
    series = []
    if element is None:
        return series
    for typegrd in element.findall('./TypsDeGrdObsElabHydro'):
        series.extend(_serieobselab_from_element(typegrd))
    return series


def _seriesobselab_from_element_v2(element):
    """return a list of obselaboreehydro.SerieObsElab
    from a <SeriesObsElaborHydro> element
    """
    series = []
    if element is None:
        return series
    for serie in element.findall('./SerieObsElaborHydro'):
        series.append(_serieobselab_from_element_v2(serie))
    return series


def _seriesobselabmeteo_from_element_v2(element):
    """return a list of obselaboreemeteo.SerieObsElabMeteo
        from a <SeriesObsElaborMeteo> element"""
    series = []
    if element is None:
        return series
    for serie in element.findall('./SerieObsElaborMeteo'):
        series.append(_serieobselabmeteo_from_element_v2(serie))
    return series


def _serieobselabmeteo_from_element_v2(element):
    """Return a obselaboreemeteo.SerieObsElabMeteo
       from a SeriesObsElaborMeteo element.
    """
    args_serie = {}
    if element.find('CdSiteHydro') is not None:
        code = _value(element, 'CdSiteHydro')
        args_serie['site'] = _sitehydro.Sitehydro(
            code=code)
    elif element.find('CdSiteMeteo') is not None:
        code = _value(element, 'CdSiteMeteo')
        ponderation = _value(element, 'ValPondSiteMeteo', float)
        args_serie['site'] = _sitemeteo.SitemeteoPondere(
            sitemeteo=_sitemeteo.Sitemeteo(code=code),
            ponderation=ponderation)
    args_serie['grandeur'] = _value(element, 'CdGrdSerieObsElaborMeteo')
    args_serie['typeserie'] = _value(element, 'TypSerieObsElaborMeteo')
    dtdeb = _value(element, 'DtDebSerieObsElaborMeteo')
    if dtdeb is not None:
        args_serie['dtdeb'] = dtdeb
    dtfin = _value(element, 'DtFinSerieObsElaborMeteo')
    if dtfin is not None:
        args_serie['dtfin'] = dtfin
    duree = _value(element, 'DureeSerieObsElaborMeteo', int)
    if duree is not None:
        args_serie['duree'] = 60 * duree
    ipa = element.find('SerieObsElaborMeteoIpa')
    if ipa is not None:
        args_ipa = {}
        args_ipa['coefk'] = _value(ipa, 'KSerieObsElaborMeteoIpa', float)
        npdt = _value(ipa, 'PDTSerieObsElaborMeteoIpa', int)
        if npdt is not None:
            args_ipa['npdt'] = npdt
        args_serie['ipa'] = _obselaboreemeteo.Ipa(**args_ipa)

    serie = _obselaboreemeteo.SerieObsElabMeteo(**args_serie)

    observations = []
    for obs in element.findall('./ObssElaborMeteo/ObsElaborMeteo'):
        args = {}
        args['dte'] = _value(obs, 'DtObsElaborMeteo')  # mandatory
        args['res'] = _value(obs, 'ResObsElaborMeteo', float)  # mandatory
        qua = _value(obs, 'IndiceQualObsElaborMeteo', float)
        if qua is not None:
            args['qua'] = qua
        qal = _value(obs, 'QualifObsElaborMeteo', int)
        if qal is not None:
            args['qal'] = qal
        mth = _value(obs, 'MethObsElaborMeteo', int)
        if mth is not None:
            args['mth'] = mth
        statut = _value(obs, 'StObsElaborMeteo', int)
        if statut is not None:
            args['statut'] = statut

        observations.append(_obselaboreemeteo.ObsElabMeteo(**args))

    # add observations to serie
    if len(observations) > 0:
        serie.observations = _obselaboreemeteo.ObssElabMeteo(
            *observations).sort_index()
    return serie


# -- utility functions --------------------------------------------------------
def _UTC(dte):
    """Return string date with suffix +00 if no time zone specified."""
    return dte
#     if (dte is not None) and (dte.find('+') == -1):
#         return '%s+00' % dte
#     else:
#         return dte


def _value(element, tag, cast=str):
    """Return cast(element/tag.text) or None."""
    if element is not None:
        e = element.find(tag)
        if (e is not None) and (e.text is not None):
            if cast == bool:
                # return wether text is a kind of True... or not
                return (str(e.text).lower() in ('true', 'vrai', '1'))
            # else
            return cast(e.text)
    # return None

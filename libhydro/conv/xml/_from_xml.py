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
    obsmeteo as _obsmeteo, simulation as _simulation, evenement as _evenement)


# -- strings ------------------------------------------------------------------
# contributor Camillo Montes (SYNAPSE)
__version__ = '0.5.3'
__date__ = '2017-05-03'

# HISTORY
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
    version = '1.1'
    nom = 'Echange de données hydrométriques'

    # descriptors
    dtprod = _composant.Datefromeverything(required=True)

    def __init__(self, emetteur, destinataire, dtprod=None):
        """Constructeur.

        Arguments:
            emetteur (intervenant.Intervenant ou Contact) = si un contact
                est utilise, sa propriete Intervenant doit etre renseignee
            destinataire (intervenant.Intervenant ou Contact) = si un contact
                est utilise, sa propriete Intervenant doit etre renseignee
            dtprod (numpy.datetime64 string, datetime.datetime...,
                defaut utcnow()) = date de production

        """
        # -- descriptors --
        self.dtprod = dtprod or _datetime.datetime.utcnow()

        # -- full properties --
        self._emetteur = Emetteur(None, None)
        self._destinataire = Destinataire(None, None)
        self.emetteur = emetteur
        self.destinataire = destinataire

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
        return 'Message du {dt}\n Emetteur: {ei} [{ec}]\n' \
               'Destinataire: {di} [{dc}]'.format(
                   dt=self.dtprod,
                   ei=unicode(self.emetteur.intervenant),
                   ec=unicode(self.emetteur.contact) or '<sans contact>',
                   di=unicode(self.destinataire.intervenant),
                   dc=unicode(self.destinataire.contact) or '<sans contact>')

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
            # serieshydro: liste de obshydro.Serie
            # seriesmeteo: liste de obsmeteo.Serie
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

    return {
        'scenario': _scenario_from_element(tree.find('Scenario')),
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
        # 'courbestarage'
        # 'jaugeages'
        # 'courbescorrection'
        'serieshydro': _serieshydro_from_element(tree.find('Donnees/Series')),
        'seriesmeteo': _seriesmeteo_from_element(
            tree.find('Donnees/ObssMeteo')),
        # 'obsselab'
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
            dtprod=_value(element, 'DateHeureCreationFichier', _UTC))


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
            unicode(e.text) for e in element.findall('CdCommune')]
        args['tronconsvigilance'] = [
            _tronconvigilance_from_element(e)
            for e in element.findall(
                'TronconsVigilanceSiteHydro/TronconVigilanceSiteHydro')]
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
        niveauaffichage = _value(element, 'NiveauAffichageStationHydro')
        if niveauaffichage is not None:
            args['niveauaffichage'] = niveauaffichage
        args['coord'] = _coord_from_element(
            element.find('CoordStationHydro'), 'StationHydro')
        args['capteurs'] = [
            _capteur_from_element(e)
            for e in element.findall('Capteurs/Capteur')]
        args['commune'] = _value(element, 'CdCommune')
        args['ddcs'] = [unicode(e.text) for e in element.findall(
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


def _capteur_from_element(element):
    """Return a sitehydro.Capteur from a <Capteur> element."""
    if element is not None:
        # prepare args
        args = {}
        args['code'] = _value(element, 'CdCapteur')
        args['codeh2'] = _value(element, 'CdCapteurAncienRef')
        args['libelle'] = _value(element, 'LbCapteur')
        typemesure = _value(element, 'TypMesureCapteur')
        if typemesure is not None:
            args['typemesure'] = typemesure
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
        args['dtmaj'] = _value(element, 'DtMajSeuilSiteHydro', _UTC)
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
            element, 'DtActivationSeuilSiteHydro', _UTC)
        args['dtdesactivation'] = _value(
            element, 'DtDesactivationSeuilSiteHydro', _UTC)
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
            element, 'DtActivationSeuilStationHydro', _UTC)
        args['dtdesactivation'] = _value(
            element, 'DtDesactivationSeuilStationHydro', _UTC)
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
            dt=_value(element, 'DtEvenement', _UTC),
            publication=_value(element, 'TypPublicationEvenement'),
            dtmaj=_value(element, 'DtMajEvenement', _UTC))


def _seriehydro_from_element(element):
    """Return a obshydro.Serie from a <Serie> element."""
    if element is not None:
        # prepare args
        # entite can be a Sitehydro, a Station or a Capteur
        entite = None
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
        # build a Serie and return
        return _obshydro.Serie(
            entite=entite,
            grandeur=_value(element, 'GrdSerie'),
            statut=_value(element, 'StatutSerie'),
            dtdeb=_value(element, 'DtDebSerie', _UTC),
            dtfin=_value(element, 'DtFinSerie', _UTC),
            dtprod=_value(element, 'DtProdSerie', _UTC),
            contact=contact,
            observations=_obsshydro_from_element(element.find('ObssHydro')))


def _seriemeteo_from_element(element):
    """Return a obsmeteo.Serie from a <ObsMeteo> element.

    Warning, the serie here does not contains observations, dtdeb or dtfin.

    """
    if element is not None:
        # build a Grandeur
        grandeur = _sitemeteo.Grandeur(
            typemesure=_value(element, 'CdGrdMeteo'),
            sitemeteo=_sitemeteo.Sitemeteo(_value(element, 'CdSiteMeteo')))
        # prepare the duree in minutes
        duree = _value(element, 'DureeObsMeteo', int) or 0
        # build a Contact
        contact = _intervenant.Contact(code=_value(element, 'CdContact'))
        # build a Serie without the observations and return
        return _obsmeteo.Serie(
            grandeur=grandeur,
            duree=duree * 60,
            statut=_value(element, 'StatutObsMeteo', int),
            dtprod=_value(element, 'DtProdObsMeteo', _UTC),
            contact=contact)


def _obsshydro_from_element(element):
    """Return a sorted obshydro.Observations from a <ObssHydro> element."""
    if element is not None:
        # prepare a list of Observation
        observations = []
        for o in element:
            args = {}
            args['dte'] = _value(o, 'DtObsHydro', _UTC)
            args['res'] = _value(o, 'ResObsHydro')
            if args['res'] is None:
                return
            mth = _value(o, 'MethObsHydro', int)
            if mth is not None:
                args['mth'] = mth
            qal = _value(o, 'QualifObsHydro', int)
            if qal is not None:
                args['qal'] = qal
            continuite = _value(o, 'ContObsHydro', bool)
            if continuite is not None:
                args['cnt'] = continuite
            observations.append(_obshydro.Observation(**args))
        # build the Observations and return
        return _obshydro.Observations(*observations).sort_index()


def _obsmeteo_from_element(element):
    """Return a obsmeteo.Observation from a <ObssHydro> element."""
    if element is not None:
        # prepare args
        args = {}
        args['dte'] = _value(element, 'DtObsMeteo', _UTC)
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
            dtprod=_value(element, 'DtProdSimul', _UTC),
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
            dte = _value(prev, 'DtPrev', _UTC)

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
# return a list of obshydro.Serie from a <Series> element
_serieshydro_from_element = _global_function_builder(
    './Serie', _seriehydro_from_element)
# return a list of simulation.Simulation from a <Simuls> element
_simulations_from_element = _global_function_builder(
    './Simul', _simulation_from_element)


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
    return seuilshydro.values()


def _seriesmeteo_from_element(element):
    """Return a list of obsmeteo.Serie from a <ObssMeteo> element.

    Painful because the XML does not contain series:
        # for each <ObsMeteo> we build a serie and obs
        # then we group obs by identical series in a set
        # at last we sort the series and update dtdeb and dtfin

    """
    seriesmeteo = set()
    if element is not None:

        for obsmeteo in element.findall('./ObsMeteo'):

            ser = _seriemeteo_from_element(obsmeteo)
            obs = _obsmeteo_from_element(obsmeteo)
            if obs is None:
                continue

            for serie in seriesmeteo:
                # if serie == ser:
                if serie.__eq__(ser, ignore=['observations']):
                    # add obs to an exisitng serie
                    serie.observations = \
                        _obsmeteo.Observations.concat((
                            serie.observations,
                            _obsmeteo.Observations(obs)))
                    break
            else:
                # new serie
                ser.observations = _obsmeteo.Observations(obs)
                seriesmeteo.add(ser)

        # update the serie
        for serie in seriesmeteo:
            serie.observations = serie.observations.sort_index()
            serie.dtdeb = min(serie.observations.index)
            serie.dtfin = max(serie.observations.index)

    return list(seriesmeteo)


# -- utility functions --------------------------------------------------------
def _UTC(dte):
    """Return string date with suffix +00 if no time zone specified."""
    if (dte is not None) and (dte.find('+') == -1):
        return '%s+00' % dte
    else:
        return dte


def _value(element, tag, cast=unicode):
    """Return cast(element/tag.text) or None."""
    if element is not None:
        e = element.find(tag)
        if (e is not None) and (e.text is not None):
            if cast == bool:
                # return wether text is a kind of True... or not
                return (unicode(e.text).lower() in ('true', 'vrai', '1'))
            # else
            return cast(e.text)
    # return None

# -*- coding: utf-8 -*-
"""Module xml._from_xml.

Ce module expose la classe:
    # Scenario

Il contient les fonctions de lecture des fichiers au format
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

import datetime as _datetime
import collections as _collections

import numpy as _numpy
from lxml import etree as _etree

from libhydro.core import (
    _composant,
    sitehydro as _sitehydro,
    sitemeteo as _sitemeteo,
    seuil as _seuil,
    modeleprevision as _modeleprevision,
    obshydro as _obshydro,
    obsmeteo as _obsmeteo,
    simulation as _simulation,
    intervenant as _intervenant,
    evenement as _evenement
)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__contributor__ = """Camillo Montes (SYNAPSE)"""
__version__ = """0.2e"""
__date__ = """2014-07-30"""

#HISTORY
#V0.2 - 2014-07-21
#    add sitesmeteo and seriesmeteo
#V0.1 - 2013-08-18
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - move the Scenario class in the _xml module
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


# -- class Scenario -----------------------------------------------------------
class Scenario(object):

    """Classe Scenario.

    Classe pour manipuler les scenarios des messages SANDRE.

    Proprietes:
        code = hydrometrie
        version = 1.1
        nom = 'Echange de donnees hydrometriques'
        dtprod (datetime.datetime)
        emetteur (intervenant.Contact)
        destinataire (intervenant.Intervenant)

    """

    # Scenario other properties

    # reference
    # envoi
    # contexte

    # class attributes
    code = 'hydrometrie'
    version = '1.1'
    nom = 'Echange de données hydrométriques'

    def __init__(self, emetteur, destinataire, dtprod=None):
        """Constructeur.

        Arguments:
            emetteur (intervenant.Contact)
            destinataire (intervenant.Intervenant)
            dtprod (datetime ou isoformat, defaut utcnow())

        """

        # -- full properties --
        self._emetteur = self._destinataire = self._dtprod = None
        self.emetteur = emetteur
        self.destinataire = destinataire
        self.dtprod = dtprod

    # -- property emetteur --
    @property
    def emetteur(self):
        """Return message emetteur."""
        return self._emetteur

    @emetteur.setter
    def emetteur(self, emetteur):
        """Set message emetteur."""
        try:
            # None case
            if emetteur is None:
                raise TypeError('emetteur is required')
            # other cases
            if not isinstance(emetteur, _intervenant.Contact):
                raise TypeError('emetteur incorrect')
            self._emetteur = emetteur
        except:
            raise

    # -- property destinataire --
    @property
    def destinataire(self):
        """Return message destinataire."""
        return self._destinataire

    @destinataire.setter
    def destinataire(self, destinataire):
        """Set message destinataire."""
        try:
            # None case
            if destinataire is None:
                raise TypeError('destinataire is required')
            # other cases
            if not isinstance(destinataire, _intervenant.Intervenant):
                raise TypeError('destinataire incorrect')
            self._destinataire = destinataire
        except:
            raise

    # -- property dtprod --
    @property
    def dtprod(self):
        """Return message generation date."""
        return self._dtprod

    @dtprod.setter
    def dtprod(self, dtprod):
        """Set message generation date."""
        try:
            # None case
            if dtprod is None:
                dtprod = _datetime.datetime.utcnow()

            # other cases
            if isinstance(dtprod, (str, unicode)):
                dtprod = _numpy.datetime64(dtprod)
            if isinstance(dtprod, _numpy.datetime64):
                dtprod = dtprod.item()
            if not isinstance(dtprod, _datetime.datetime):
                raise TypeError('dtprod must be a datetime')

            # all is well
            self._dtprod = dtprod

        except:
            raise

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return "Message du {0}\nEmis par le {1} pour l'{2}".format(
            self.dtprod,
            self.emetteur,
            self.destinataire
        )

    __str__ = _composant.__str__


# -- tests function -----------------------------------------------------------
def _parse(src):
    """Return objects from xml source file.

    Cette fonction est destinee au tests unitaires. Les utilisateurs sont
    invites a utiliser la classe xml.Message comme interface de lecture des
    fichiers Xml Hydrometrie.

    Arguments:
        src (nom de fichier, url, objet fichier...) = source de donnee. Les
            type de src acceptes sont ceux de lxml.etree.parse

    Retourne un dictionnaire avec les cles:
            # scenario: xml.Scenario
            # siteshydro: liste de sitehydro.Siteshydro ou None
            # sitesmeteo: liste de sitehydro.Siteshydro ou None
            # seuilshydro: liste de seuil.Seuilhydro ou None
            # evenements: liste d'evenements ou None
            # serieshydro: liste de obshydro.Serie ou None
            # seriesmeteo: liste de obsmeteo.Serie ou None
            # simulations: liste de simulation.Simulation ou None

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
        'sitesmeteo': _sitesmeteo_from_element(tree.find('RefHyd/SitesMeteo')),
        'seuilshydro': _seuilshydro_from_element(
            element=tree.find('RefHyd/SitesHydro'),
            ordered=True
        ),
        # 'modelesprevision': '',
        'evenements': _evenements_from_element(
            tree.find('Donnees/Evenements')
        ),
        # 'courbestarage'
        # 'jaugeages'
        # 'courbescorrection'
        'serieshydro': _serieshydro_from_element(tree.find('Donnees/Series')),
        'seriesmeteo': _seriesmeteo_from_element(
            tree.find('Donnees/ObssMeteo')
        ),
        # 'obsselab'
        # 'gradshydro'
        # 'qualifsannee'
        'simulations': _simulations_from_element(tree.find('Donnees/Simuls'))
        # 'alarmes'
    }


# -- global functions ---------------------------------------------------------

# TODO - some functions could be factorised

def _siteshydro_from_element(element):
    """Return a list of sitehydro.Sitehydro from a <SitesHydro> element."""
    siteshydro = []
    if element is not None:
        for sitehydro in element.findall('./SiteHydro'):
            siteshydro.append(_sitehydro_from_element(sitehydro))
    return siteshydro


def _sitesmeteo_from_element(element):
    """Return a list of sitemeteo.Sitemeteo from a <SitesMeteo> element."""
    sitesmeteo = []
    if element is not None:
        for sitemeteo in element.findall('./SiteMeteo'):
            sitesmeteo.append(_sitemeteo_from_element(sitemeteo))
    return sitesmeteo


def _seuilshydro_from_element(element, ordered=False):
    """Return a list of seuil.Seuilhydro from a <SitesHydro> element.

    When ordered is True, we use an OrderedDict to keep the XML initial order.

    """
    # -------------
    # no seuil case
    # -------------
    if (
        (element is None) or
        element.find(
            './SiteHydro/ValeursSeuilsSiteHydro/ValeursSeuilSiteHydro'
        ) is None
    ):
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
            './ValeursSeuilsSiteHydro/ValeursSeuilSiteHydro'
        ):
            seuilhydro = _seuilhydro_from_element(
                elementseuilhydro, sitehydro
            )
            if (sitehydro.code, seuilhydro.code) in seuilshydro:
                # check that the seuil complies with it predecessors
                if not seuilhydro.__eq__(
                    other=seuilshydro[(sitehydro.code, seuilhydro.code)],
                    lazzy=True,
                    cmp_values=False
                ):
                    raise ValueError(
                        'seuilhydro %s from sitehydro %s '
                        'has inconsistent metadatas' % (
                            seuilhydro.code, sitehydro.code
                        )
                    )
                # change the seuil object in the new seuil values
                # to assure the navigability
                for valeur in seuilhydro.valeurs:
                    valeur.seuil = seuilshydro[
                        (sitehydro.code, seuilhydro.code)
                    ]
                # add the valeurs to an existing entry
                seuilshydro[
                    (sitehydro.code, seuilhydro.code)
                ].valeurs.extend(seuilhydro.valeurs)
            else:
                # new entry
                seuilshydro[
                    (sitehydro.code, seuilhydro.code)
                ] = seuilhydro

    # return a list of seuils
    return seuilshydro.values()


def _evenements_from_element(element):
    """Return a list of evenement.Evenement from a <Evenements> element."""
    evenements = []
    if element is not None:
        for evenement in element.findall('./Evenement'):
            evenements.append(_evenement_from_element(evenement))
    return evenements


def _serieshydro_from_element(element):
    """Return a list of obshydro.Serie from a <Series> element."""
    serieshydro = []
    if element is not None:
        for seriehydro in element.findall('./Serie'):
            serieshydro.append(_seriehydro_from_element(seriehydro))
    return serieshydro


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
                if serie == ser:
                    # add obs to an exisitng serie
                    serie.observations = \
                        _obsmeteo.Observations.concat(
                            serie.observations,
                            _obsmeteo.Observations(obs)
                        )
                    break
            else:
                # new serie
                ser.observations = _obsmeteo.Observations(obs)
                seriesmeteo.add(ser)

        # update the serie
        for serie in seriesmeteo:
            serie.observations = serie.observations.sort()
            serie.dtdeb = min(serie.observations.index)
            serie.dtfin = max(serie.observations.index)

    return list(seriesmeteo)


def _simulations_from_element(element):
    """Return a list of simulation.Simulation from a <Simuls> element."""
    simuls = []
    if element is not None:
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
        args['codeh2'] = _value(element, 'CdSiteHydroAncienRef')
        typesite = _value(element, 'TypSiteHydro')
        if typesite is not None:
            args['typesite'] = typesite
        args['libelle'] = _value(element, 'LbSiteHydro')
        args['libelleusuel'] = _value(element, 'LbUsuelSiteHydro')
        args['coord'] = _coord_from_element(
            element.find('CoordSiteHydro'), 'SiteHydro'
        )
        args['stations'] = [
            _stationhydro_from_element(e)
            for e in element.findall('StationsHydro/StationHydro')
        ]
        args['communes'] = [
            unicode(e.text) for e in element.findall('CdCommune')
        ]
        args['tronconsvigilance'] = [
            _tronconvigilance_from_element(e)
            for e in element.findall(
                'TronconsVigilanceSiteHydro/TronconVigilanceSiteHydro'
            )
        ]

        # build Sitehydro
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
            element.find('CoordSiteMeteo'), 'SiteMeteo'
        )
        args['commune'] = _value(element, 'CdCommune')
        # build a Sitemeteo
        sitemeteo = _sitemeteo.Sitemeteo(**args)
        # add the grandeurs
        sitemeteo.grandeurs.extend([
            _grandeur_from_element(e, sitemeteo)
            for e in element.findall('GrdsMeteo/GrdMeteo')
        ])
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

        # build Tronconvigilance
        return _sitehydro.Tronconvigilance(**args)


def _stationhydro_from_element(element):
    """Return a sitehydro.Stationhydro from a <StationHydro> element."""
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
            element, 'ComplementLibelleStationHydro'
        )
        niveauaffichage = _value(element, 'NiveauAffichageStationHydro')
        if niveauaffichage is not None:
            args['niveauaffichage'] = niveauaffichage
        args['coord'] = _coord_from_element(
            element.find('CoordStationHydro'), 'StationHydro'
        )
        args['capteurs'] = [
            _capteur_from_element(e)
            for e in element.findall('Capteurs/Capteur')
        ]
        args['commune'] = _value(element, 'CdCommune')
        args['ddcs'] = [
            unicode(e.text)
            for e in element.findall('ReseauxMesureStationHydro/CodeSandreRdd')
        ]
        # build Station
        return _sitehydro.Stationhydro(**args)


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
        # build Capteur
        return _sitehydro.Capteur(**args)


def _grandeur_from_element(element, sitemeteo=None):
    """Return a sitemeteo.Grandeur from a <GrdMeteo> element."""
    if element is not None:
        # prepare args
        args = {}
        args['typemesure'] = _value(element, 'CdGrdMeteo')
        if sitemeteo is not None:
            args['sitemeteo'] = sitemeteo
        # build Grandeur
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
        args['publication'] = _istrue(
            _value(element, 'DroitPublicationSeuilSiteHydro')
        )
        args['valeurforcee'] = _value(element, 'ValForceeSeuilSiteHydro')
        args['dtmaj'] = _value(element, 'DtMajSeuilSiteHydro', _UTC)
        seuil = _seuil.Seuilhydro(**args)
        # add the values
        args['valeurs'] = []
        valeurseuil = _valeurseuilsitehydro_from_element(
            element, sitehydro, seuil
        )
        if valeurseuil is not None:
            args['valeurs'].append(valeurseuil)
        args['valeurs'].extend([
            _valeurseuilstationhydro_from_element(e, seuil)
            for e in element.findall(
                './ValeursSeuilsStationHydro/ValeursSeuilStationHydro'
            )
        ])
        # build Seuilhydro
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
            element, 'DtActivationSeuilSiteHydro', _UTC
        )
        args['dtdesactivation'] = _value(
            element, 'DtDesactivationSeuilSiteHydro', _UTC
        )
        # build Valeurseuil
        return _seuil.Valeurseuil(**args)


def _valeurseuilstationhydro_from_element(element, seuil):
    """Return a seuil.Valeurseuil from a <ValeursSeuilStationHydro> element."""
    if element is not None:
        # prepare args
        args = {}
        args['valeur'] = _value(element, 'ValHauteurSeuilStationHydro')
        args['seuil'] = seuil
        args['entite'] = _sitehydro.Stationhydro(
            code=_value(element, 'CdStationHydro')
        )
        args['tolerance'] = _value(element, 'ToleranceSeuilStationHydro')
        args['dtactivation'] = _value(
            element, 'DtActivationSeuilStationHydro', _UTC
        )
        args['dtdesactivation'] = _value(
            element, 'DtDesactivationSeuilStationHydro', _UTC
        )
        # build Valeurseuil
        return _seuil.Valeurseuil(**args)


def _evenement_from_element(element):
    """Return a evenement.Evenement from a <Evenement> element."""
    if element is not None:

        # entite can be a Sitehydro, a Stationhydro or a Sitemeteo
        entite = None
        if element.find('CdSiteHydro') is not None:
            entite = _sitehydro.Sitehydro(
                code=_value(element, 'CdSiteHydro')
            )
        elif element.find('CdStationHydro') is not None:
            entite = _sitehydro.Stationhydro(
                code=_value(element, 'CdStationHydro')
            )
        elif element.find('CdSiteMeteo') is not None:
            raise NotImplementedError('Sitemeteo is not already implemented')
        #     entite = _sitemeteo.Sitemeteo(
        #         code=_value(element, 'CdSiteMeteo')
        #     )

        # make the Evenement
        return _evenement.Evenement(
            entite=entite,
            descriptif=_value(element, 'DescEvenement'),
            contact=_intervenant.Contact(
                code=_value(element, 'CdContact'),
            ),
            dt=_value(element, 'DtEvenement', _UTC),
            publication=_value(element, 'TypPublicationEvenement'),
            dtmaj=_value(element, 'DtMajEvenement', _UTC),
        )


def _seriehydro_from_element(element):
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

        # get the contact
        contact = _intervenant.Contact(code=_value(element, 'CdContact'))

        # make the Serie
        return _obshydro.Serie(
            entite=entite,
            grandeur=_value(element, 'GrdSerie'),
            statut=_value(element, 'StatutSerie'),
            dtdeb=_value(element, 'DtDebSerie', _UTC),
            dtfin=_value(element, 'DtFinSerie', _UTC),
            dtprod=_value(element, 'DtProdSerie', _UTC),
            contact=contact,
            observations=_obsshydro_from_element(element.find('ObssHydro'))
        )


def _seriemeteo_from_element(element):
    """Return a obsmeteo.Serie from a <ObsMeteo> element.

    Warning, the serie here does not contains observations, dtdeb or dtfin.

    """
    if element is not None:

        # compute grandeur
        grandeur = _sitemeteo.Grandeur(
            typemesure=_value(element, 'CdGrdMeteo'),
            sitemeteo=_sitemeteo.Sitemeteo(_value(element, 'CdSiteMeteo'))
        )

        # get duree in minutes
        duree = _value(element, 'DureeObsMeteo', int) or 0

        # get the contact
        contact = _intervenant.Contact(code=_value(element, 'CdContact'))

        # make the Serie without the observations
        return _obsmeteo.Serie(
            grandeur=grandeur,
            duree=duree * 60,
            statut=_value(element, 'StatutObsMeteo', int),
            dtprod=_value(element, 'DtProdObsMeteo', _UTC),
            contact=contact
        )


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
            continuite = _istrue(_value(o, 'ContObsHydro'))
            if continuite is not None:
                args['cnt'] = continuite
            observations.append(_obshydro.Observation(**args))

        # build Observations
        return _obshydro.Observations(*observations).sort()


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
        # build Observation
        return _obsmeteo.Observation(**args)


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
        # prepare the qualite
        # warning: qualite is int(float())
        qualite = _value(element, 'IndiceQualiteSimul', float)
        if qualite is not None:
            qualite = int(qualite)
        # make the Simulation
        return _simulation.Simulation(
            entite=entite,
            modeleprevision=_modeleprevision.Modeleprevision(
                code=_value(element, 'CdModelePrevision')
            ),
            grandeur=_value(element, 'GrdSimul'),
            statut=_value(element, 'StatutSimul', int),
            qualite=qualite,
            public=_value(element, 'PubliSimul', bool),
            commentaire=_value(element, 'ComSimul'),
            dtprod=_value(element, 'DtProdSimul', _UTC),
            previsions=_previsions_from_element(element.find('Prevs')),
            intervenant=_intervenant.Intervenant(
                _value(element, 'CdIntervenant')
            )
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
def _istrue(s):
    """Return wether s is a sort of True or None."""
    # bool('False') is True...
    if s is None:
        return None
    return (unicode(s).lower() in ('true', 'vrai', '1'))


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
            return cast(e.text)
    #return None

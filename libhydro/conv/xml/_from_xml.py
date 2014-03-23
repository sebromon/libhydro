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

import sys as _sys
import datetime as _datetime
import collections as _collections

import numpy as _numpy
from lxml import etree as _etree

from libhydro.core import (
    sitehydro as _sitehydro,
    seuil as _seuil,
    modeleprevision as _modeleprevision,
    obshydro as _obshydro,
    simulation as _simulation,
    intervenant as _intervenant,
    evenement as _evenement
)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__contributor__ = """Camillo Montes (SYNAPSE)"""
__version__ = """0.1k"""
__date__ = """2014-03-20"""

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

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode('utf8')


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
            # seuilshydro: liste de seuil.Seuilhydro ou None
            # evenements: liste d'evenements ou None
            # series: liste de obshydro.Serie ou None
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
        'seuilshydro': _seuilshydro_from_element(
            element=tree.find('RefHyd/SitesHydro'),
            ordered=True
        ),
        # 'sitesmeteo'
        # 'modelesprevision': '',
        'evenements': _evenements_from_element(
            tree.find('Donnees/Evenements')
        ),
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

# TODO - these functions can be factorised

def _siteshydro_from_element(element):
    """Return a list of sitehydro.Sitehydro from a <SitesHydro> element."""
    if element is not None:
        siteshydro = []
        for sitehydro in element.findall('./SiteHydro'):
            siteshydro.append(_sitehydro_from_element(sitehydro))
        return siteshydro


def _seuilshydro_from_element(element, ordered=False):
    """Return a list of seuil.Seuilhydro from a <SitesHydro> element.

    When ordered is True, we use an OrderedDict to keep the XML initial order.

    """
    # FIXME - we have to group some seuil here
    if (
        (element is not None) and
        element.find(
            './SiteHydro/ValeursSeuilsSiteHydro/ValeursSeuilSiteHydro'
        ) is not None
    ):
        # get all seuils
        # we put them in a {(cdsitehydro, cdseuil): seuil.Seuilhydro,...}
        # dictionnary to group similar seuils (bdhydro output is awful!)
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
                        print(seuilhydro)
                        print(seuilshydro[(sitehydro.code, seuilhydro.code)])
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
    if element is not None:
        evenements = []
        for evenement in element.findall('./Evenement'):
            evenements.append(_evenement_from_element(evenement))
        return evenements


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

        # build Site
        return _sitehydro.Sitehydro(**args)


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
        # build Capteur
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
            dtdeb=_value(element, 'DtDebSerie', _UTC),
            dtfin=_value(element, 'DtFinSerie', _UTC),
            dtprod=_value(element, 'DtProdSerie', _UTC),
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
            continuite = _istrue(_value(o, 'ContObsHydro'))
            if continuite is not None:
                args['cnt'] = continuite
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
            # warning: qualite is int(float())
            qualite=int(_value(element, 'IndiceQualiteSimul', float)),
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
    e = element.find(tag)
    if e is not None:
        return cast(e.text)
    return e

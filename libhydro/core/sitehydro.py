# -*- coding: utf-8 -*-
"""Module sitehydro.

Ce module contient les classes:
    # Sitehydro
    # Stationhydro
    # Capteur

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys as _sys

from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from . import _composant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__contributor__ = """Camillo Montes (SYNAPSE)"""
__version__ = """0.3a"""
__date__ = """2014-02-20"""

#HISTORY
#V0.3 - 2014-02-20
#    merge Camillo (CMO) work
#V0.1 - 2013-07-12
#    first shot


#-- todos ---------------------------------------------------------------------
# FIXME - generalize typeentite in _Entite.typentite ?
# TODO - add navigability for Capteur => Station and Station => Site


#-- config --------------------------------------------------------------------
# config use classes definitions and is at the bottom


#-- class _Entitehydro --------------------------------------------------------
class _Entitehydro(object):

    """Abstract base class for all hydro entities.

    Properties:
        code (string(x)) = hydro code
        codeh2 (string(8)) = ancien code hydro2
        libelle (string)
        _strict (bool) = strict or fuzzy mode

    """

    def __init__(self, code, codeh2=None, libelle=None, strict=True):
        """Constructor.

        Arguments:
            code (string(8, 10, 12)) = hydro code
            codeh2 (string(8), defaut None) = ancien code hydro2
            libelle (string, defaut None)
            strict (bool, defaut True) = strict or fuzzy mode

        """

        # -- simple properties --
        self._strict = bool(strict)
        self.libelle = unicode(libelle) if (libelle is not None) else None

        # -- full properties --
        self._code = self._codeh2 = None
        self.code = code
        self.codeh2 = codeh2

    # -- property code --
    @property
    def code(self):
        """Return code hydro."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code hydro."""
        try:
            if code is None:
                # None case
                if self._strict:
                    raise TypeError('code is required')

            else:
                # other cases
                code = unicode(code)
                if self._strict and (self.__class__ in _CODE_HYDRO_LENGTH):
                    # check code hydro
                    _composant.is_code_hydro(
                        code=code,
                        length=_CODE_HYDRO_LENGTH[self.__class__]
                    )

            # all is well
            self._code = code

        except:
            raise

    # -- property codeh2 --
    @property
    def codeh2(self):
        """Return code hydro2."""
        return self._codeh2

    @codeh2.setter
    def codeh2(self, code):
        """Set code hydro2."""
        try:
            if code is not None:
                code = unicode(code)
                _composant.is_code_hydro(code, 8)

            # all is well
            self._codeh2 = code

        except:
            raise


#-- class _Site_or_station ---------------------------------------------------
class _Site_or_station(_Entitehydro):

    """Abstract base class for Sitehydro and Stationhydro.

    Properties:

        -- properties of _Entitehydro --

        coord (liste ou dict) = (x, y, proj) ou
            {'x': x, 'y': y, 'proj': proj}

    """

    def __init__(
        self, code, codeh2=None, libelle=None,
        coord=None, strict=True
    ):
        """Constructor.

        Arguments:

            -- args of _Entitehydro --

            coord (liste ou dict) = (x, y, proj) ou
                {'x': x, 'y': y, 'proj': proj}

        """

        # -- super --
        super(_Site_or_station, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle, strict=strict
        )

        # -- simple properties --

        # -- full properties --
        self._coord = None
        self.coord = coord

    # -- property coord --
    @property
    def coord(self):
        """Return coord."""
        return self._coord

    @coord.setter
    def coord(self, coord):
        """Set coord."""
        self._coord = None
        if coord is not None:
            if isinstance(coord, _composant.Coord):
                self._coord = coord
            else:
                try:
                    # instanciate with a list
                    self._coord = _composant.Coord(*coord)
                except Exception:
                    try:
                        # instanciate with a dict
                        self._coord = _composant.Coord(**coord)
                    except Exception:
                        raise TypeError('coord must be a list or a dict')


#-- class Sitehydro -----------------------------------------------------------
class Sitehydro(_Site_or_station):

    """Classe Sitehydro.

    Classe pour manipuler des sites hydrometriques.

    Proprietes:
        code (string(8)) = code hydro
        codeh2 (string(8)) = ancien code hydro2
        typesite (string parmi NOMENCLATURE[530])
        libelle (string)
        libelleusuel (string)
        coord (Coord)
        stations (une liste de Station)
        communes (une liste de codes communes, char(5)) = code INSEE commune

    """

    # Sitehydro other properties

    #libellecomplement
    #mnemonique
    #precisionce
    #pkamont
    #pkaval
    #altitude
    #sysalti
    #dtmaj
    #bv
    #fuseau
    #statut
    #ponctuel
    #dtpremieredonnee
    #moisetiage
    #moisanneehydro
    #publication
    #essai
    #influence
    #influencecommentaire
    #commentaire

    #siteattache
    #siteassocie
    #masses
    #entitehydro
    #loistats
    #images
    #rolecontact
    #zonehydro
    #tronconhydro
    #communes
    #tronconsvivilance

    def __init__(
        self, code, codeh2=None, typesite='REEL',
        libelle=None, libelleusuel=None, coord=None, stations=None,
        communes=None, strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(8)) = code hydro
            codeh2 (string(8)) = ancien code hydro2
            typesite (string parmi NOMENCLATURE[530], defaut REEL)
            libelle (string)
            libelleusuel (string)
            stations (une Station ou un iterable de Station)
            communes (un code commmune ou un iterable de codes)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type, du code et des stations

        """

        # -- super --
        super(Sitehydro, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle,
            coord=coord, strict=strict
        )

        # -- simple properties --
        self.libelleusuel = unicode(libelleusuel) \
            if (libelleusuel is not None) else None

        # -- full properties --
        self._typesite = None
        self.typesite = typesite
        self._stations = self._communes = []
        self.stations = stations
        self.communes = communes

    # -- property typesite --
    @property
    def typesite(self):
        """Return type site hydro."""
        return self._typesite

    @typesite.setter
    def typesite(self, typesite):
        """Set type site hydro."""
        try:

            # None case
            if typesite is None:
                raise TypeError('typesite is required')

            # other cases
            typesite = unicode(typesite)
            if (self._strict) and (typesite not in _NOMENCLATURE[530]):
                raise ValueError('typesite incorrect')

            # all is well
            self._typesite = typesite

        except:
            raise

    # -- property stations --
    @property
    def stations(self):
        """Return stations."""
        return self._stations

    @stations.setter
    def stations(self, stations):
        """Set stations."""
        self._stations = []
        # None case
        if stations is None:
            return
        # one station, we make a list with it
        if isinstance(stations, Stationhydro):
            stations = [stations]
        # an iterable of stations
        for station in stations:
            # some checks
            if self._strict:
                if not isinstance(station, Stationhydro):
                    raise TypeError(
                        'stations must be a Station or an iterable of Station'
                    )
                elif station.typestation not in \
                        _SITE_ACCEPTED_STATION[self.typesite]:
                    raise ValueError(
                        '{0} station forbidden for {1} site'.format(
                            station.typestation, self.typesite
                        )
                    )
            # add station
            self._stations.append(station)

    # -- property communes --
    @property
    def communes(self):
        """Return codes communes."""
        return self._communes

    @communes.setter
    def communes(self, communes):
        """Set code commune."""
        self._communes = []
        # None case
        if communes is None:
            return
        # one commune, we make a list with it
        if _composant.is_code_commune(communes, raises=False):
            communes = [communes]
        # an iterable of communes
        for commune in communes:
            if _composant.is_code_commune(commune):
                self._communes.append(unicode(commune))

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Site {0} {1}::{2} [{3} station{4}]'.format(
            self.typesite or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.stations),
            '' if (len(self.stations) < 2) else 's'
        )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


#-- class Stationhydro --------------------------------------------------------
class Stationhydro(_Site_or_station):

    """Classe Stationhydro.

    Classe pour manipuler des stations hydrometriques.

    Proprietes:
        code (string(10)) = code hydro
        codeh2 (string(8)) = ancien code hydro2
        typestation (string parmi NOMENCLATURE[531])
        libelle (string)
        libellecomplement (string)
        niveauaffichage (int) = niveau d'affichage
        coord (Coord)
        capteurs (une liste de Capteur)
        commune (char(5)) = code INSEE commune
        ddcs (liste de char(10)) = liste de reseaux de mesure SANDRE
            (dispositifs de collecte)

    """

    # Stationhydro other properties

    #descriptif
    #dtmaj
    #pk
    #dtes
    #dths
    #surveillance
    #publication
    #delaidiscontinuite
    #delaiabsence
    #essai
    #influence
    #influencecommentaire
    #commentaire

    #remplace
    #stationfille
    #qualifications
    #finalites
    #loisstat
    #sitehydro
    #images
    #rolecontact
    #stationattachee
    #plageutilisation

    def __init__(
        self, code, codeh2=None, typestation='LIMNI', libelle=None,
        libellecomplement=None, niveauaffichage=0, coord=None, capteurs=None,
        commune=None, ddcs=None, strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(10)) = code hydro
            codeh2 (string(8)) = ancien code hydro2
            typestation (string parmi NOMENCLATURE[531], defaut LIMNI)
            libelle (string)
            libellecomplement (string)
            niveauaffichage (int) = niveau d'affichage
            coord (liste ou dict) = (x, y, proj) ou
                {'x': x, 'y': y, 'proj': proj}
            capteurs (un Capteur ou un iterable de Capteur)
            commune (char(5)) = code INSEE commune
            ddcs (un code char(10) ou un iterable de char(10)) = reseaux de
                mesure SANDRE
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type et du code

        """

        # -- super --
        super(Stationhydro, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle,
            coord=coord, strict=strict
        )

        # -- simple properties --
        self.libellecomplement = unicode(libellecomplement) \
            if (libellecomplement is not None) else None

        # -- full properties --
        self._typestation = 'LIMNI'
        self.typestation = typestation
        self._niveauaffichage = 0
        self.niveauaffichage = niveauaffichage
        self._capteurs = []
        self.capteurs = capteurs
        self._commune = None
        self.commune = commune
        self._ddcs = []
        self.ddcs = ddcs

    # -- property typestation --
    @property
    def typestation(self):
        """Return type station hydro."""
        return self._typestation

    @typestation.setter
    def typestation(self, typestation):
        """Set type station hydro."""
        try:

            # none case
            if typestation is None:
                raise TypeError('typestation is required')

            # other cases
            typestation = unicode(typestation)
            if (self._strict) and (typestation not in _NOMENCLATURE[531]):
                raise ValueError('typestation incorrect')

            # all is well
            self._typestation = typestation

        except:
            raise

    # -- property niveauaffichage --
    @property
    def niveauaffichage(self):
        """Return niveau d'affichage."""
        return self._niveauaffichage

    @niveauaffichage.setter
    def niveauaffichage(self, niveauaffichage):
        """Set niveau d'affichage."""
        # FIXME - Bd Hydro requires one of (0 111 191 311 391 511 591 911 991)
        #         but it is not a SANDRE nomencature
        self._niveauaffichage = int(niveauaffichage)

    # -- property capteurs --
    @property
    def capteurs(self):
        """Return capteurs."""
        return self._capteurs

    @capteurs.setter
    def capteurs(self, capteurs):
        """Set capteurs."""
        self._capteurs = []
        # None case
        if capteurs is None:
            return
        # one capteur, we make a list with it
        if isinstance(capteurs, Capteur):
            capteurs = [capteurs]
        # an iterable of capteurs
        for capteur in capteurs:
            # some checks
            if self._strict:
                if not isinstance(capteur, Capteur):
                    raise TypeError(
                        'capteurs must be a Capteur or an iterable of Capteur'
                    )
                elif capteur.typemesure not in \
                        _STATION_ACCEPTED_CAPTEUR[self.typestation]:
                    raise ValueError(
                        '{0} capteur forbidden for {1} station'.format(
                            capteur.typemesure, self.typestation
                        )
                    )
            # add capteur
            self._capteurs.append(capteur)

    # -- property commune --
    @property
    def commune(self):
        """Return code commune."""
        return self._commune

    @commune.setter
    def commune(self, commune):
        """Set code commune."""
        if commune is not None:
            commune = unicode(commune)
            _composant.is_code_commune(commune)
        self._commune = commune

    # -- property ddcs --
    @property
    def ddcs(self):
        """Return ddcs."""
        return self._ddcs

    @ddcs.setter
    def ddcs(self, ddcs):
        """Set ddcs."""
        self._ddcs = []
        # None case
        if ddcs is None:
            return
        # one ddc, we make a list with it
        if not hasattr(ddcs, '__iter__'):
            ddcs = [ddcs]
        # an iterable of ddcs
        for ddc in ddcs:
            ddc = unicode(ddc)
            # if len(ddc) != 10:
            if len(ddc) > 10:
                raise ValueError('ddc code must be 10 chars long')
            self._ddcs.append(ddc)

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Station {0} {1}::{2} [{3} capteur{4}]'.format(
            self.typestation or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.capteurs),
            '' if (len(self.capteurs) < 2) else 's'
        )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


#-- class Capteur -------------------------------------------------------------
class Capteur(_Entitehydro):

    """Classe Capteur.

    Classe pour manipuler des capteurs hydrometriques.

    Proprietes:
        code (string(12)) = code hydro
        codeh2 (string(8)) = ancien code hydro2
        typemesure (caractere parmi NOMENCLATURE[531]) = H ou Q
        libelle (string)

    """

    # Capteur other properties

    #mnemonique
    #typecapteur
    #surveillance
    #dtmaj
    #pdt
    #essai
    #commentaire

    #stationhydro
    #plageutilisation
    #observateur

    def __init__(
        self, code, codeh2=None, typemesure='H', libelle=None,
        strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(12)) = code hydro
            codeh2 (string(8)) = ancien code hydro2
            typemesure (caractere parmi NOMENCLATURE[531], defaut H) = H ou Q
            libelle (string)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du code et du type de mesure

        """

        # -- super --
        super(Capteur, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle, strict=strict
        )

        # -- simple properties --

        # -- full properties --
        self._typemesure = 'H'
        self.typemesure = typemesure

    # -- property typemesure --
    @property
    def typemesure(self):
        """Return type de mesure."""
        return self._typemesure

    @typemesure.setter
    def typemesure(self, typemesure):
        """Set type de mesure."""
        try:

            # None case
            if typemesure is None:
                raise TypeError('typemesure is required')

            # other cases
            typemesure = unicode(typemesure)
            if (self._strict) and (typemesure not in _NOMENCLATURE[520]):
                raise ValueError('typemesure incorrect')

            # all is well
            self._typemesure = typemesure

        except:
            raise

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Capteur {0} {1}::{2}'.format(
            self.typemesure or '<sans type de mesure>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>'
        )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


# -- config -------------------------------------------------------------------
# -- HYDRO ENTITY _ARTICLE --
_ARTICLE = {
    # classe name: article
    Sitehydro: 'le',
    Stationhydro: 'la',
    Capteur: 'le'
}

# -- HYDRO CODE LENGTH --
_CODE_HYDRO_LENGTH = {
    # class name: hydro code length
    Sitehydro: 8,
    Stationhydro: 10,
    Capteur: 12
}

# -- HYDRO ENTITY DEPEDENCY RULES --
# rules for checking which Stationhydro a Sitehydro does accept
_SITE_ACCEPTED_STATION = {
    # type site : [type station, ...]
    'REEL': ('LIMNI', 'DEB', 'HC', 'LIMNIMERE', 'LIMNIFILLE'),
    'SOURCE':  ('LIMNI', 'DEB', 'HC', 'LIMNIMERE', 'LIMNIFILLE'),
    'MAREGRAPHE': ('LIMNI',),
    'PLANDEAU': ('LIMNI',),
    'FICTIF': tuple(),
    'PONCTUEL': tuple(),
    'VIRTUEL': tuple(),
    'RECONSTITUE': tuple()
}
# rules for checking which Capteur a Stationhydro does accept
_STATION_ACCEPTED_CAPTEUR = {
    'LIMNI': ('H',),
    'DEB': ('H', 'Q'),
    'HC': tuple(),
    'LIMNIMERE': ('H',),
    'LIMNIFILLE': ('H',)
}

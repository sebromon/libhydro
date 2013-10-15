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


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2e"""
__date__ = """2013-09-03"""

#HISTORY
#V0.1 - 2013-07-12
#    first shot


#-- todos ---------------------------------------------------------------------
# FIXME - generalize typeentite in _Entite.typentite
# TODO - add navigability for Capteur => Station and Station => Site


# -- config -------------------------------------------------------------------
# config use classes definitions and is at the bottom


#-- class _Entitehydro --------------------------------------------------------
class _Entitehydro(object):
    """Abstract base class for hydro entities.

    Properties:
        code (string(x)) = hydro code
        libelle (string)
        _strict (bool) = strict or fuzzy mode

    """

    def __init__(self, code, libelle=None, strict=True):
        """Constructor.

        Arguments:
            code (string(8, 10, 12)) = hydro code
            libelle (string)
            strict (bool, defaut True) = strict or fuzzy mode

        """

        # -- simple properties --
        self._strict = strict
        self.libelle = unicode(libelle) if (libelle is not None) else None

        # -- full properties --
        self.code = code

    # -- property code --
    @property
    def code(self):
        """Code hydro."""
        return self._code

    @code.setter
    def code(self, code):
        try:
            if code is None:
                # None case
                if self._strict:
                    raise TypeError('code is required')
            else:
                # other cases
                code = unicode(code)
                if self._strict and (self.__class__ in _CODE_HYDRO_LENGTH):
                    #code must be like 'A0334450(xx)(yy)'
                    if (
                        (len(code) != _CODE_HYDRO_LENGTH[self.__class__]) or
                        (not code[0].isupper()) or
                        (not code[1:].isdigit())
                    ):
                        raise ValueError('code incorrect')
            # all is well
            self._code = code

        except:
            raise


#-- class Sitehydro -----------------------------------------------------------
class Sitehydro(_Entitehydro):
    """Classe Sitehydro.

    Classe pour manipuler des sites hydrometriques.

    Proprietes:
        code (string(8)) = code hydro
        typesite (string parmi NOMENCLATURE[530])
        libelle (string)
        stations (une liste de Station)

    """

    # TODO - Sitehydro other properties

    #libelleusuel
    #libellecomplement
    #mnemonique
    #precisionce
    #x
    #y
    #sysproj
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
    #codeh2
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
        self, code, typesite='REEL', libelle=None, stations=[],
        strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(8)) = code hydro
            typesite (string parmi NOMENCLATURE[530], defaut REEL)
            libelle (string)
            stations (une Station ou un iterable de Station)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type, du code et des stations

        """

        # -- super --
        super(Sitehydro, self).__init__(
            code=code, libelle=libelle, strict=strict
        )

        # -- simple properties --

        # -- full properties --
        self.typesite = typesite
        self.stations = stations

    # -- property typesite --
    @property
    def typesite(self):
        """Type de site hydro."""
        return self._typesite

    @typesite.setter
    def typesite(self, typesite):
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
        """Stations."""
        return self._stations

    @stations.setter
    def stations(self, stations):
        self._stations = []
        # None case
        if stations is None:
            return
        # others cases
        if isinstance(stations, Stationhydro):
            stations = [stations]
        for station in stations:
            # some checks
            if self._strict:
                if not isinstance(station, Stationhydro):
                    raise TypeError(
                        'stations must be a Station or an iterable of Station'
                    )
                if station.typestation not in \
                        _SITE_ACCEPTED_STATION[self.typesite]:
                    raise ValueError(
                        '{0} station forbidden for {1} site'.format(
                            station.typestation, self.typesite
                        )
                    )
            # add station
            self._stations.append(station)

    # -- other methods --
    def __unicode__(self):
        """Unicode representation."""
        return 'Site {0} {1}::{2} [{3} station{4}]'.format(
            self.typesite or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.stations),
            '' if (len(self.stations) < 2) else 's'
        )

    def __str__(self):
        """String representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


#-- class Stationhydro --------------------------------------------------------
class Stationhydro(_Entitehydro):
    """Classe Stationhydro.

    Classe pour manipuler des stations hydrometriques.

    Proprietes:
        code (string(10)) = code hydro
        typestation (string parmi NOMENCLATURE[531])
        libelle (string)
        capteurs (une liste de Capteur)

    """

    # TODO - Stationhydro other properties

    #capteurs

    #libellecomplement
    #descriptif
    #dtmaj
    #x
    #y
    #projection
    #pk
    #dtes
    #dths
    #surveillance
    #niveauaffichage
    #publication
    #delaidiscontinuite
    #delaiabsence
    #essai
    #cdh2
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
        self, code, typestation='LIMNI', libelle=None, capteurs=[],
        strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(10)) = code hydro
            typestation (string parmi NOMENCLATURE[531], defaut LIMNI)
            libelle (string)
            capteurs (un Capteur ou un iterable de Capteur)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type et du code

        """

        # -- super --
        super(Stationhydro, self).__init__(
            code=code, libelle=libelle, strict=strict
        )

        # -- simple properties --

        # -- full properties --
        self.typestation = typestation
        self.capteurs = capteurs

    # -- property typestation --
    @property
    def typestation(self):
        """Type de station hydro."""
        return self._typestation

    @typestation.setter
    def typestation(self, typestation):
        try:

            # None case
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

    # -- property capteurs --
    @property
    def capteurs(self):
        """capteurs."""
        return self._capteurs

    @capteurs.setter
    def capteurs(self, capteurs):
        self._capteurs = []
        # None caqe
        if capteurs is None:
            return
        # other cases
        if isinstance(capteurs, Capteur):
            capteurs = [capteurs]
        for capteur in capteurs:
            # some checks
            if self._strict:
                if not isinstance(capteur, Capteur):
                    raise TypeError(
                        'capteurs must be a Capteur or an iterable of Capteur'
                    )
                if capteur.typemesure not in \
                        _STATION_ACCEPTED_CAPTEUR[self.typestation]:
                    raise ValueError(
                        '{0} capteur forbidden for {1} station'.format(
                            capteur.typemesure, self.typestation
                        )
                    )
            # add station
            self._capteurs.append(capteur)

    # -- other methods --
    def __unicode__(self):
        """Unicode representation."""
        return 'Station {0} {1}::{2} [{3} capteur{4}]'.format(
            self.typestation or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.capteurs),
            '' if (len(self.capteurs) < 2) else 's'

        )

    def __str__(self):
        """String representation."""
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
        typemesure (caractere parmi NOMENCLATURE[531]) = H ou Q
        libelle (string)

    """

    # TODO - Capteur other properties

    #mnemonique
    #typecapteur
    #surveillance
    #dtmaj
    #pdt
    #essai
    #codeh2
    #commentaire

    #stationhydro
    #plageutilisation
    #observateur

    def __init__(self, code, typemesure='H', libelle=None, strict=True):
        """Initialisation.

        Arguments:
            code (string(12)) = code hydro
            typemesure (caractere parmi NOMENCLATURE[531], defaut H) = H ou Q
            libelle (string)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du code et du type de mesure

        """

        # -- super --
        super(Capteur, self).__init__(
            code=code, libelle=libelle, strict=strict
        )

        # -- simple properties --

        # -- full properties --
        self.typemesure = typemesure

    # -- property typemesure --
    @property
    def typemesure(self):
        """Type de mesure."""
        return self._typemesure

    @typemesure.setter
    def typemesure(self, typemesure):
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
        """Unicode representation."""
        return 'Capteur {0} {1}::{2}'.format(
            self.typemesure or '<sans type de mesure>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>'
        )

    def __str__(self):
        """String representation."""
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

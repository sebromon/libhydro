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

from .nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.2a"""
__date__ = """2013-08-16"""

#HISTORY
#V0.1 - 2013-07-12
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - many many properties
# TODO - generalize typexxx in _Entite.typentite ???

# -- config -------------------------------------------------------------------
# look at end of file


#-- class _Entitehydro --------------------------------------------------------
class _Entitehydro(object):
    """Abstract base class for hydro entities.

    Properties:
        code (string(x)) = hydro code
        libelle (string)
        _strict (bool) = strict or fuzzy mode

    """

    def __init__(self, code=None, libelle=None, strict=True):
        """Constructor.

        Parameters:
            code (string(8, 10, 12)) = hydro code
            libelle (string)
            strict (bool, defaut True) = strict or fuzzy mode

        """

        # -- simple properties --
        self._strict = strict
        if libelle:
            self.libelle = unicode(libelle)
        else:
            self.libelle = None

        # -- full properties --
        self._code = None
        if code:
            self.code = code

    # -- property code --
    @property
    def code(self):
        """Code hydro."""
        return self._code

    @code.setter
    def code(self, code):
        try:
            code = unicode(code)
            if self._strict and (self.__class__ in CODE_LENGTH):
                #code must be like 'A0334450(xx)(yy)'
                if (
                    (len(code) != CODE_LENGTH[self.__class__]) or
                    (not code[0].isupper()) or
                    (not code[1:].isdigit())
                ):
                    raise ValueError('code incorrect')
            self._code = code
        except:
            raise

    # -- other methods --
    # FIXME
    # def _admit_serie(self, grandeur, statut):
    #     if not self.typemesure:
    #         raise
    #     if self.typemesure != grandeur:
    #         return False
    #     if statut not in (4, 8):  # brute, corrige
    #         return False
    #     return True

    # def _admit_simulation(self, grandeur):
    #      return ADMIT_SIMULATION[self.__class][grandeur]


#-- class Sitehydro -----------------------------------------------------------
class Sitehydro(_Entitehydro):
    """Class Sitehydro.

    Classe pour manipuler des sites hydrometriques.

    Proprietes:
        typesite (string parmi NOMENCLATURE[530])
        code (string(8)) = code hydro
        libelle (string)
        stations (un iterable de Station)

    """

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
        self, typesite=None, code=None, libelle=None, stations=None,
        strict=True
    ):
        """Constructeur.

        Parametres:
            typesite (string parmi NOMENCLATURE[530])
            code (string(8)) = code hydro
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
        self._typesite = None
        self._stations = []
        if typesite:
            self.typesite = typesite
        if stations:
            self.stations = stations

    # -- property typesite --
    @property
    def typesite(self):
        """Type de site hydro."""
        return self._typesite

    @typesite.setter
    def typesite(self, typesite):
        try:
            typesite = unicode(typesite)
            if (self._strict) and (typesite not in _NOMENCLATURE[530]):
                raise Exception
            self._typesite = typesite
        except:
            raise ValueError('typesite incorrect')

    # -- property stations --
    @property
    def stations(self):
        """Stations."""
        return self._stations

    @stations.setter
    def stations(self, stations):
        if stations is None:
            self._stations = []
        elif isinstance(stations, Stationhydro):
            self._stations = [stations]
        else:
            try:
                self._stations = []
                for station in stations:
                    if (self._strict) and (not isinstance(station, Stationhydro)):
                        raise Exception
                    self._stations.append(station)
            except:
                raise TypeError(
                    'stations must be a Station or a iterable of Station'
                )

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'Site {0} {1}::{2} [{3} station{4}]'.format(
            self.typesite or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.stations),
            '' if (len(self.stations) < 2) else 's'
        ).encode('utf-8')


#-- class Stationhydro --------------------------------------------------------
class Stationhydro(_Entitehydro):
    """Class Stationhydro.

    Classe pour manipuler des stations hydrometriques.

    Proprietes:
        typestation (string parmi NOMENCLATURE[531])
        code (string(10)) = code hydro
        libelle (string)

    """

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

    def __init__(self, typestation=None, code=None, libelle=None, strict=True):
        """Constructeur.

        Parametres:
            typestation (string parmi NOMENCLATURE[531])
            code (string(10)) = code hydro
            libelle (string)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type et du code

        """

        # -- super --
        super(Stationhydro, self).__init__(
            code=code, libelle=libelle, strict=strict
        )

        # -- simple properties --

        # -- full properties --
        self._typestation = None
        if typestation:
            self.typestation = typestation

    # -- property typestation --
    @property
    def typestation(self):
        """Type de station hydro."""
        return self._typestation

    @typestation.setter
    def typestation(self, typestation):
        try:
            typestation = unicode(typestation)
            if (self._strict) and (typestation not in _NOMENCLATURE[531]):
                raise Exception
            self._typestation = typestation
        except:
            raise ValueError('typestation incorrect')

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'Station {0} {1}::{2}'.format(
            self.typestation or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>'
        ).encode('utf-8')


#-- class Capteur -------------------------------------------------------------
class Capteur(_Entitehydro):
    """Class Capteur.

    Classe pour manipuler des capteurs hydrometriques.

    Proprietes:
        code (string(12)) = code hydro
        libelle (string)
        typemesure (caractere parmi NOMENCLATURE[531]) = H ou Q

    """

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

    def __init__(self, code=None, libelle=None, typemesure=None, strict=True):
        """Constructeur.

        Parametres:
            code (string(12)) = code hydro
            libelle (string)
            typemesure (caractere parmi NOMENCLATURE[531]) = H ou Q
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du code et du type de mesure

        """

        # -- super --
        super(Capteur, self).__init__(
            code=code, libelle=libelle, strict=strict
        )

        # -- simple properties --

        # -- full properties --
        self._typemesure = None
        if typemesure:
            self.typemesure = typemesure

    # -- property typemesure --
    @property
    def typemesure(self):
        """Type de mesure."""
        return self._typemesure

    @typemesure.setter
    def typemesure(self, typemesure):
        try:
            typemesure = unicode(typemesure)
            if (self._strict) and (typemesure not in _NOMENCLATURE[520]):
                raise Exception
            self._typemesure = typemesure
        except:
            raise ValueError('typemesure incorrect')

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'Capteur {0} {1}::{2}'.format(
            self.typemesure or '<sans type de mesure>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>'
        ).encode('utf-8')


# -- config -------------------------------------------------------------------
# -- HYDRO ENTITY ARTICLE --
# classe name, article
ARTICLE = {
    Sitehydro: 'le',
    Stationhydro: 'la',
    Capteur: 'le'
}

# -- HYDRO CODE LENGTH --
# class name, hydro code length
CODE_LENGTH = {
    Sitehydro: 8,
    Stationhydro: 10,
    Capteur: 12
}


# ADMIT_SERIE = {
#     Sitehydro: True,
#     Stationhydro: True,
#     Capteur: True
# }
#
# ADMIT_SIMULATION = {
#     Sitehydro: {'H': False, 'Q': True},
#     Stationhydro: {'H': True, 'Q': False},
#     Capteur: {'H': False, 'Q':False}
# }

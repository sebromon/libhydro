# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function
"""Module de classe python sitehydro.

Ce module contient les classes:
    # Sitehydro
    # Stationhydro
    # Capteur -- NOT IMPLEMENTED --

"""

#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1c"""
__date__ = """2013-07-31"""

#HISTORY
#V0.1 - 2013-07-12
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - many many properties
# FIXME - nothing


#-- imports -------------------------------------------------------------------
from string import ascii_uppercase, digits

try:
    from nomenclature import NOMENCLATURE
except Exception:
    from libhydro.core.nomenclature import NOMENCLATURE

# -- config -------------------------------------------------------------------
# classe name, article
ARTICLE = {
    'Sitehydro': 'le',
    'Stationhydro': 'la',
    'Capteur': 'le'
}


#-- class Sitehydro -----------------------------------------------------------
class Sitehydro(object):
    """Class Sitehydro.

    Classe pour manipuler des sites hydrometriques.

    Proprietes:
        typesite (string parmi NOMENCLATURE[530])
        code (string(8)) = code hydro
        libelle (string)
        stations (un iterable de Station)

    """

    def __init__(
        self, typesite=None, code=None, libelle=None, stations=None,
        strict=True
    ):
        """Constructor.

        Parametres:
            typesite (string parmi NOMENCLATURE[530])
            code (string(8)) = code hydro
            libelle (string)
            stations (une Station ou un iterable de Station)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite du type, du code et des stations

        """

        # -- simple properties --
        self._strict = strict
        if libelle:
            self.libelle = unicode(libelle)
        else:
            self.libelle = None

        # -- full properties --
        self._typesite = self._code = None
        self._stations = []
        if typesite:
            self.typesite = typesite
        if code:
            self.code = code
        if stations:
            self.stations = stations

    # -- property typesite --
    @property
    def typesite(self):
        """typesite hydro."""
        return self._typesite

    @typesite.setter
    def typesite(self, typesite):
        try:
            typesite = unicode(typesite)
            if (self._strict) and (typesite not in NOMENCLATURE[530]):
                raise Exception
            self._typesite = typesite
        except:
            raise ValueError('typesite incorrect')

    # @typesite.deleter
    # def typesite(self):
    #     del self._typesite

    # -- property code --
    @property
    def code(self):
        """Code hydro."""
        return self._code

    @code.setter
    def code(self, code):
        #code sitehydro is like 'A0334450'
        try:
            code = unicode(code)
            if (
                self._strict and (
                    (len(code) != 8) or
                    (code[0] not in ascii_uppercase) or
                    (not set(code[1:]).issubset(set(digits)))
                )
            ):
                raise Exception
            self._code = code
        except:
            raise ValueError('code incorrect')

    # @code.deleter
    # def code(self):
    #     del self._code

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

    # @stations.deleter
    # def stations(self):
    #     del self._code

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'site {0} {1}::{2} [{3} station{4}]'.format(
            self.typesite or '-',
            self.code or '-',
            self.libelle or '-',
            len(self.stations),
            '' if (len(self.stations) < 2) else 's'
        ).encode('utf-8')


#-- class Stationhydro --------------------------------------------------------
class Stationhydro(object):
    """Class Stationhydro.

    Classe pour manipuler des stations hydrometriques.

    Proprietes:
        typestation (string parmi NOMENCLATURE[531])
        code (string(10)) = code hydro
        libelle (string)

    """

    def __init__(self, typestation=None, code=None, libelle=None, strict=True):
        """Constructor.

        Parametres:
            typestation (string parmi NOMENCLATURE[531])
            code (string(10)) = code hydro
            libelle (string)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite du type et du code

        """

        # -- simple properties --
        self._strict = strict
        if libelle:
            self.libelle = unicode(libelle)
        else:
            self.libelle = None

        # -- full properties --
        self._typestation = self._code = None
        if typestation:
            self.typestation = typestation
        if code:
            self.code = code

    # -- property typestation --
    @property
    def typestation(self):
        """typestation hydro."""
        return self._typestation

    @typestation.setter
    def typestation(self, typestation):
        try:
            typestation = unicode(typestation)
            if (self._strict) and (typestation not in NOMENCLATURE[531]):
                raise Exception
            self._typestation = typestation
        except:
            raise ValueError('typestation incorrect')

    # @typestation.deleter
    # def typestation(self):
    #     del self._typestation

    # -- property code --
    @property
    def code(self):
        """Code hydro."""
        return self._code

    @code.setter
    def code(self, code):
        #code stationhydro is like 'A033445001'
        try:
            code = unicode(code)
            if (
                (self._strict) and (
                    (len(code) != 10) or
                    (code[0] not in ascii_uppercase) or
                    (not set(code[1:]).issubset(set(digits)))
                )
            ):
                raise Exception
            self._code = code
        except:
            raise ValueError('code incorrect')

    # @code.deleter
    # def code(self):
    #     del self._code

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'station {0} {1}::{2}'.format(
            self.typestation or '-',
            self.code or '-',
            self.libelle or '-'
        ).encode('utf-8')


#-- class Capteur -------------------------------------------------------------
class Capteur(object):

    # TODO - not implemented

    def __init__(self, code):
        self.code = code

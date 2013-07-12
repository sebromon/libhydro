# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function
"""Module de classe python sitehydro.

Ce module contient les classes:
    # Sitehydro
    # Stationhydro
    # Capteur


"""

#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1a"""
__date__ = """2013-07-12"""

#HISTORY
#V0.1 - 2013-07-12
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - many many properties
# FIXME - nothing


#-- imports -------------------------------------------------------------------
from string import ascii_uppercase, digits


#-- class ---------------------------------------------------------------------
class Sitehydro(object):
    """Class Sitehydro.

    Classe pour manipuler des sites hydrométriques.

    """

    def __init__(self, code=None, libelle=None, stations=None):
        """Constructor.

        Paramètres:
            codehydro (string(8))
            libellé (string)
            stations (a Station or a iterable of Station) => une liste

        """
        # super(Sitehydro, self).__init__()
        self._code = self._libelle = None
        self._stations = []
        if code:
            self.code = code
        if libelle:
            self.libelle = libelle
        if stations:
            self.stations = stations

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
                (len(code) != 8) or
                (code[0] not in ascii_uppercase) or
                (not set(code[1:]).issubset(set(digits)))
            ):
                raise Exception
        except:
            raise ValueError('code incorrect')
        self._code = code

    # @code.deleter
    # def code(self):
    #     del self._code

    # -- property libelle --
    @property
    def libelle(self):
        """Libelle."""
        return self._libelle

    @libelle.setter
    def libelle(self, libelle):
        self._libelle = unicode(libelle)

    # @libelle.deleter
    # def libelle(self):
    #     del self._code

    # -- property stations --
    @property
    def stations(self):
        """Stations."""
        return self._stations

    @stations.setter
    def stations(self, stations):
        if isinstance(stations, Stationhydro):
            self._stations = list(stations)
        else:
            try:
                self._stations = []
                for station in stations:
                    if isinstance(station, Stationhydro):
                        self._stations.append(station)
            except:
                raise TypeError(
                    'stations must be a Station or a iterable of Stations'
                )

    # @stations.deleter
    # def stations(self):
    #     del self._code

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'site {0}::{1}::{2} stations'.format(
            self._code, self._libelle, len(self.stations)
        ).encode('utf-8')


class Stationhydro(object):
    """Class Stationhydro.

    Classe pour manipuler des stations hydrométriques.

    """

    def __init__(self, code=None, libelle=None):
        """Constructor.

        Paramètres:
            codehydro (string(10))
            libellé (string)

        """
        # super(Sitehydro, self).__init__()
        self._code = self._libelle = None
        if code:
            self.code = code
        if libelle:
            self.libelle = libelle

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
                (len(code) != 10) or
                (code[0] not in ascii_uppercase) or
                (not set(code[1:]).issubset(set(digits)))
            ):
                raise Exception
        except:
            raise ValueError('code incorrect')
        self._code = code

    # @code.deleter
    # def code(self):
    #     del self._code

    # -- property libelle --
    @property
    def libelle(self):
        """Libelle."""
        return self._libelle

    @libelle.setter
    def libelle(self, libelle):
        self._libelle = unicode(libelle)

    # @libelle.deleter
    # def libelle(self):
    #     del self._code

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'station {0}::{1}'.format(
            self._code, self._libelle
        ).encode('utf-8')

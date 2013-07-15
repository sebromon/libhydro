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
__version__ = """version 0.1b"""
__date__ = """2013-07-15"""

#HISTORY
#V0.1 - 2013-07-12
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - many many properties
# FIXME - nothing


#-- imports -------------------------------------------------------------------
from string import ascii_uppercase, digits
from libhydro.core.nomenclature import NOMENCLATURE


#-- class ---------------------------------------------------------------------
class Sitehydro(object):
    """Class Sitehydro.

    Classe pour manipuler des sites hydrométriques.

    Propriétés:
        typesite (string in NOMENCLATURE[530])
        code (string(8)) = code hydro
        libellé (string)
        stations (a list of Station)

    """

    def __init__(self, typesite=None, code=None, libelle=None, stations=None):
        """Constructor.

        Paramètres:
            typesite (string in NOMENCLATURE[530])
            code (string(8)) = code hydro
            libellé (string)
            stations (a Station or a iterable of Station)

        """
        # super(Sitehydro, self).__init__()

        # -- full properties --
        self._typesite = self._code = None
        self._stations = []
        if typesite:
            self.typesite = typesite
        if code:
            self.code = code
        if stations:
            self.stations = stations

        # -- simple properties --
        if libelle:
            self.libelle = unicode(libelle)
        else:
            self.libelle = None

    # -- property typesite --
    @property
    def typesite(self):
        """typesite hydro."""
        return self._typesite

    @typesite.setter
    def typesite(self, typesite):
        try:
            typesite = unicode(typesite)
            if typesite in NOMENCLATURE[530]:
                self._typesite = typesite
            else:
                raise Exception
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

    # -- property stations --
    @property
    def stations(self):
        """Stations."""
        return self._stations

    @stations.setter
    def stations(self, stations):
        if isinstance(stations, Stationhydro):
            self._stations = [stations]
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
        return 'site {0} {1}::{2} - {3} stations'.format(
            self.typesite or '-',
            self.code or '-',
            self.libelle or '-',
            len(self.stations)
        ).encode('utf-8')


class Stationhydro(object):
    """Class Stationhydro.

    Classe pour manipuler des stations hydrométriques.

    Propriétés:
        typestation (string in NOMENCLATURE[531])
        code (string(10)) = code hydro
        libellé (string)

    """

    def __init__(self, typestation=None, code=None, libelle=None):
        """Constructor.

        Paramètres:
            typestation (string in NOMENCLATURE[531])
            code (string(10)) = code hydro
            libellé (string)

        """
        # super(Sitehydro, self).__init__()

        # -- full properties --
        self._typestation = self._code = None
        if typestation:
            self.typestation = typestation
        if code:
            self.code = code

        # -- simple properties --
        if libelle:
            self.libelle = unicode(libelle)
        else:
            self.libelle = None

    # -- property typestation --
    @property
    def typestation(self):
        """typestation hydro."""
        return self._typestation

    @typestation.setter
    def typestation(self, typestation):
        try:
            typestation = unicode(typestation)
            if typestation in NOMENCLATURE[531]:
                self._typestation = typestation
            else:
                raise Exception
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

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'station {0} {1}::{2}'.format(
            self.typestation or '-',
            self.code or '-',
            self.libelle or '-'
        ).encode('utf-8')

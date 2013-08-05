# -*- coding: utf-8 -*-
"""Module sitehydro.

Ce module contient les classes:
    # Sitehydro
    # Stationhydro
    # Capteur

"""
#-- imports -------------------------------------------------------------------
from __future__ import unicode_literals, absolute_import, division, print_function
from string import ascii_uppercase, digits

try:
    from nomenclature import NOMENCLATURE
except ImportError:
    from libhydro.core.nomenclature import NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1d"""
__date__ = """2013-08-05"""

#HISTORY
#V0.1 - 2013-07-12
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - many many properties
# FIXME - nothing


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
        """Constructor.

        Parametres:
            typesite (string parmi NOMENCLATURE[530])
            code (string(8)) = code hydro
            libelle (string)
            stations (une Station ou un iterable de Station)
            strict (bool, defaut True) = le mode permissif permet de lever les
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
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type et du code

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

    def __init__(self, code=None, libelle=None, typemesure=None, strict=True):

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

        # -- simple properties --
        self._strict = strict
        if libelle:
            self.libelle = unicode(libelle)
        else:
            self.libelle = None

        # -- full properties --
        self._typemesure = self._code = None
        if typemesure:
            self.typemesure = typemesure
        if code:
            self.code = code

    # -- property code --
    @property
    def code(self):
        """Code hydro."""
        return self._code

    @code.setter
    def code(self, code):
        #code capteur is like 'A03344500101'
        try:
            code = unicode(code)
            if (
                (self._strict) and (
                    (len(code) != 12) or
                    (code[0] not in ascii_uppercase) or
                    (not set(code[1:]).issubset(set(digits)))
                )
            ):
                raise Exception
            self._code = code
        except:
            raise ValueError('code incorrect')

    # -- property typemesure --
    @property
    def typemesure(self):
        """typemesure hydro."""
        return self._typemesure

    @typemesure.setter
    def typemesure(self, typemesure):
        try:
            typemesure = unicode(typemesure)
            if (self._strict) and (typemesure not in NOMENCLATURE[520]):
                raise Exception
            self._typemesure = typemesure
        except:
            raise ValueError('typemesure incorrect')

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'capteur {0} {1}::{2}'.format(
            self.typemesure or '-',
            self.code or '-',
            self.libelle or '-'
        ).encode('utf-8')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function
"""Module de classe python obshydro.

Ce module contient les classes:
    # Observation
    # Observations
    # Serie

Pour des usages simples, on peux utiliser directement les classes de la
    librairie Pandas, les Series ou les DataFrame.

Exemple pour instancier une Series:
    hauteurs = pandas.Series(
        data = [100, 110, 120],
        index = [
            datetime.datetime(2012, 5, 1),
            datetime.datetime(2012, 5, 2),
            datetime.datetime(2012, 5, 3)
        ]
        dtype = None,
        name='H2352303'
)

Exemple pour instancier un DataFrame:
    hauteurs = pandas.DataFrame({
        'H2354310': Series_de_hauteurs_1,
        'H4238907': Series_de_hauteurs_2,
        ...
    })

"""

#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1b"""
__date__ = """2013-07-26"""

#HISTORY
#V0.1 - 2013-07-18
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - many many properties
# FIXME - nothing


#-- imports -------------------------------------------------------------------
import numpy
import pandas

try:
    from nomenclature import NOMENCLATURE
except Exception:
    from libhydro.core.nomenclature import NOMENCLATURE


#-- class Observation ---------------------------------------------------------
class Observation(numpy.ndarray):
    """Une observation.

    Subclasse de numpy.array('dte', 'res', 'mth', 'qal', 'cnt'), les elements
    etant du type DTYPE.

    Date et resultat sont obligatoires, les autres elements ont une valeur par
    defaut.

    Proprietes:
        dte (numpy.datetime64 ou string) = date UTC de l'observation au format
            ISO 8601, arrondie a la seconde. A l'initialisation si le fuseau
            horaire n'est pas precise, la date est consideree en heure locale.
            Pour forcer la sasie d'une date UTC utiliser le fuseau +00:
                np.datetime64('2000-01-01T09:28:00+00')
        res (numpy.float) = resultat
        mth (numpy.int8, defaut 0) = methode d'obtention de la donnees suivant
            la NOMENCLATURE[507])
        qal (numpy.int8, defaut 16) = qualification de la donnees suivant la
            NOMENCLATURE[515]
        cnt (numpy.bool, defaut True) = continuite

    Usage:¬
        Getter => observation.['x'].item()
        Setter => observation.['x'] = value

    """

    DTYPE = numpy.dtype([
        (str('dte'), numpy.datetime64(None, str('s'))),
        (str('res'), numpy.float),
        (str('mth'), numpy.int8),
        (str('qal'), numpy.int8),
        (str('cnt'), numpy.bool)
    ])

    def __new__(cls, dte, res, mth=0, qal=16, cnt=True):
        if not isinstance(dte, numpy.datetime64):
            dte = numpy.datetime64(dte)
        if (mth != 0) and (mth not in NOMENCLATURE[507]):
            raise ValueError('methode incorrecte')
        if (qal != 16) and (qal not in NOMENCLATURE[515]):
            raise ValueError('qualification incorrecte')
        obj = numpy.array(
            (dte, res, mth, qal, cnt),
            dtype=Observation.DTYPE
        ).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

    def __str__(self):
        """String representation."""
        return '{0} le {4} a {5} UTC (valeur obtenue par {1}, {2} et {3})'.format(
            self['res'].item(),
            NOMENCLATURE[507][self['mth'].item()],
            NOMENCLATURE[515][self['qal'].item()],
            'continue' if self['cnt'].item() else 'discontinue',
            *self['dte'].item().isoformat().split('T')
        ).encode('utf-8')


#-- class Observations --------------------------------------------------------
class Observations(pandas.DataFrame):
    """Class Observations.

    Classe pour manipuler une collection d'observations hydrometriques, sous la
    forme d'un pandas.DataFrame.

    L'index est un pandas.DatetimeIndex qui represente les dates d'observation.

    Les donnees sont contenues dans 4 colonnes du DataFrame (voir Observation).

Propriétés

Méthodes:



    Un objet Obervations peux etre instancie de multiples façons a l'aide des
    fonctions proposees par Pandas, sous reserve de respecter le nom des
    colonnes et leur typage:
        DataFrame.from_records: constructor from tuples, also record arrays
        DataFrame.from_dict: from dicts of Series, arrays, or dicts
        DataFrame.from_csv: from CSV files
        DataFrame.from_items: from sequence of (key, value) pairs
        read_csv / read_table / read_clipboard
        ...

    Un objet simplifie ne contenant que l'index et res est obtenu avec:
        obs = observations[['res']]

    """

    def __new__(cls, *observations):
        """Constructeur.

        Parametres:
            observations (un nombre quelconque d'Observation)

        Exemples:
            obs = Observations(obs1)  # une seule Observation
            obs = Observations(obs1, obs2, ..., obsn)  # n Observation
            obs = Observations(*observations)  #  une liste d'Observation

        """

        # prepare a list of observations
        obss = []
        try:
            for obs in observations:
                if not isinstance(obs, Observation):
                    raise Exception
                obss.append(obs)

        except Exception:
            raise TypeError('{} in not an Observation'.format(obs))

        # prepare a tmp numpy.array
        array = numpy.array(object=obss)

        # get the pandas.DataFrame
        obj = pandas.DataFrame(
            data=array[list(array.dtype.names[1:])],
            index=array['dte']
        )
        # obj.concat = Observations.__concat
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

    # def __concat(obs, observations):
    #     """Ajoute (concatène) une ou plusieurs observations.

    #     Arguments: observations (Observation ou Observations)

    #     """
    #     try:
    #         # if isinstance(observations, Observations):
    #             # observation is an Observations instance
    #             # self = pandas.concat([self, observations])
    #             return pandas.concat([obs, observations])
    #         # else:
    #             # otherwise it might be a simple Observation
    #             # self = pandas.concat([self, Observations(Observations)])

    #     except Exception:
    #         # self = pandas.concat([self, Observations(Observations)])
    #         return pandas.concat([obs, Observations(Observations)])
    #         # raise TypeError("observations can't be concateneted")


#-- class Serie ---------------------------------------------------------------
class Serie(object):
    """Classe Serie.

    Classe pour manipuler des series d'observations hydrometriques.

    Proprietes:
        entitehydro (site, station ou capteur)
        grandeur (char in NOMENCLATURE[509]) = H ou Q
        statut (int in NOMENCALTURE[510]) = donnee brute, corrigee...
        observations (Observations)

    """

    # ** TODO **
    # strict (bool, defaut True) = en mode permissif, les contrôles de
    #     validite sur les proprietes ne sont paa appliques
    # datedebut
    # datefin
    # dateprod
    # sysalti
    # perime
    # contact
    # refalti OU courbetarage

    pass

    #
    #     def __init__(self, typesite=None, code=None, libelle=None, stations=None):
    #         """Constructeur.
    #
    #         Parametres:
    #             typesite (string in NOMENCLATURE[530])
    #             code (string(8)) = code hydro
    #             libelle (string)
    #             stations (a Station or a iterable of Station)
    #
    #         """
    #         # super(Sitehydro, self).__init__()
    #
    #         # -- full properties --
    #         self._typesite = self._code = None
    #         self._stations = []
    #         if typesite:
    #             self.typesite = typesite
    #         if code:
    #             self.code = code
    #         if stations:
    #             self.stations = stations
    #
    #         # -- simple properties --
    #         if libelle:
    #             self.libelle = unicode(libelle)
    #         else:
    #             self.libelle = None
    #
    #     # -- property typesite --
    #     @property
    #     def typesite(self):
    #         """typesite hydro."""
    #         return self._typesite
    #
    #     @typesite.setter
    #     def typesite(self, typesite):
    #         try:
    #             typesite = unicode(typesite)
    #             if typesite in NOMENCLATURE[530]:
    #                 self._typesite = typesite
    #             else:
    #                 raise Exception
    #         except:
    #             raise ValueError('typesite incorrect')
    #
    #     # @typesite.deleter
    #     # def typesite(self):
    #     #     del self._typesite
    #
    #     # -- property code --
    #     @property
    #     def code(self):
    #         """Code hydro."""
    #         return self._code
    #
    #     @code.setter
    #     def code(self, code):
    #         #code sitehydro is like 'A0334450'
    #         try:
    #             code = unicode(code)
    #             if (
    #                 (len(code) != 8) or
    #                 (code[0] not in ascii_uppercase) or
    #                 (not set(code[1:]).issubset(set(digits)))
    #             ):
    #                 raise Exception
    #         except:
    #             raise ValueError('code incorrect')
    #         self._code = code
    #
    #     # @code.deleter
    #     # def code(self):
    #     #     del self._code
    #
    #     # -- property stations --
    #     @property
    #     def stations(self):
    #         """Stations."""
    #         return self._stations
    #
    #     @stations.setter
    #     def stations(self, stations):
    #         if isinstance(stations, Stationhydro):
    #             self._stations = [stations]
    #         else:
    #             try:
    #                 self._stations = []
    #                 for station in stations:
    #                     if isinstance(station, Stationhydro):
    #                         self._stations.append(station)
    #             except:
    #                 raise TypeError(
    #                     'stations must be a Station or a iterable of Stations'
    #                 )
    #
    #     # @stations.deleter
    #     # def stations(self):
    #     #     del self._code
    #
    #     # -- other methods --
    #     def __str__(self):
    #         """String representation."""
    #         return 'site {0} {1}::{2} - {3} stations'.format(
    #             self.typesite or '-',
    #             self.code or '-',
    #             self.libelle or '-',
    #             len(self.stations)
    #         ).encode('utf-8')

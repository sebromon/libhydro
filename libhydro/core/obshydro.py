# -*- coding: utf-8 -*-
"""Module obshydro.

Ce module contient les classes:
    # Serie
    # Observations
    # Observation

et quelques fonctions utiles:
    # Observations.concat() pour concatener des observations

La Serie est le conteneur de reference pour les observations hydrometriques.
Les observations y sont contenues dans l'attribut du meme nom, sous la forme
d'un pandas.DataFrame dont l'index est une serie de timestamp.

"""

# On peux aussi utiliser directement les classes de la librairie Pandas, les
# Series ou les DataFrame.
#
# Exemple pour instancier une Series:
#     datas = pandas.Series(
#         data = [100, 110, 120],
#         index = [
#             numpy.datetime64('2012-05-01 10:00', 's'),
#             numpy.datetime64('2012-05-01 11:00', 's'),
#             numpy.datetime64('2012-05-01 12:00', 's')
#         ]
#         dtype = None,
#         name='observations de debit'
# )
#
# Exemple pour instancier un DataFrame, avec plusieurs series (colonnes) de
# donnees:
#     hauteurs = pandas.DataFrame({
#         'H2354310': Series_de_hauteurs_1,
#         'H4238907': Series_de_hauteurs_2,
#         ...
#     })

#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys as _sys

import numpy as _numpy
import pandas as _pandas

from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from . import _composant
from . import sitehydro as _sitehydro


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1l"""
__date__ = """2014-03-09"""

#HISTORY
#V0.1 - 2013-07-18
#    first shot


#-- todos ---------------------------------------------------------------------
# PROGRESS - Serie 60% - Observations 100% - Observation 100%
# FIXME - integriey checks entity / grandeur /statut
# ADMIT_SERIE = {
#     Sitehydro: 'Q',

#     Stationhydro: type station...

#     Capteur: 'H', brut corrige
#                'Q' brut corrige
# }
# def _admit_serie(self, grandeur, statut):
#     if not self.typemesure:
#         raise
#     if self.typemesure != grandeur:
#         return False
#     if statut not in (4, 8):  # brute, corrige
#         return False
#     return True

# TODO - add a sort argument/method ?


#-- class Observation ---------------------------------------------------------
class Observation(_numpy.ndarray):

    """Classe observation.

    Classe pour manipuler une observation elementaire.

    Subclasse de numpy.array('dte', 'res', 'mth', 'qal', 'cnt'), les elements
    etant du type DTYPE.

    Date et resultat sont obligatoires, les autres elements ont une valeur par
    defaut.

    Proprietes:
        dte (numpy.datetime64) = date UTC de l'observation au format
            ISO 8601, arrondie a la seconde. A l'initialisation par une string
            si le fuseau horaire n'est pas precise, la date est consideree eni
            heure locale.  Pour forcer la sasie d'une date UTC utiliser
            le fuseau +00:
                np.datetime64('2000-01-01T09:28+00')
                ou
                np.datetime64('2000-01-01 09:28Z')
        res (numpy.float) = resultat
        mth (numpy.int8, defaut 0) = methode d'obtention de la donnees suivant
            la NOMENCLATURE[507])
        qal (numpy.int8, defaut 16) = qualification de la donnees suivant la
            NOMENCLATURE[515]
        cnt (numpy.bool, defaut True) = continuite

    Usage:
        Getter => observation.['x'].item()
        Setter => observation.['x'] = value

    """

    DTYPE = _numpy.dtype([
        (str('dte'), _numpy.datetime64(None, str('s'))),
        (str('res'), _numpy.float),
        (str('mth'), _numpy.int8),
        (str('qal'), _numpy.int8),
        (str('cnt'), _numpy.bool)
    ])

    def __new__(cls, dte, res, mth=0, qal=16, cnt=True):
        if not isinstance(dte, _numpy.datetime64):
            dte = _numpy.datetime64(dte, 's')
        if (mth != 0) and (mth not in _NOMENCLATURE[507]):
            raise ValueError('methode incorrecte')
        if (qal != 16) and (qal not in _NOMENCLATURE[515]):
            raise ValueError('qualification incorrecte')
        obj = _numpy.array(
            (dte, res, mth, qal, cnt),
            dtype=Observation.DTYPE
        ).view(cls)
        return obj

    # def __array_finalize__(self, obj):
    #     if obj is None:
    #         return

    def __unicode__(self):
        """Return unicode representation."""
        return '''{0} le {4} a {5} UTC ''' \
               '''(valeur obtenue par {1}, {2} et {3})'''.format(
                   self['res'].item(),
                   _NOMENCLATURE[507][self['mth'].item()],
                   _NOMENCLATURE[515][self['qal'].item()],
                   'continue' if self['cnt'].item() else 'discontinue',
                   *self['dte'].item().isoformat().split('T')
               )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


#-- class Observations --------------------------------------------------------
class Observations(_pandas.DataFrame):

    """Classe Observations.

    Classe pour manipuler une collection d'observations hydrometriques, sous la
    forme d'un pandas.DataFrame (les objets instancies sont des DataFrame).

    L'index est un pandas.DatetimeIndex qui represente les dates d'observation.

    Les donnees sont contenues dans 4 colonnes du DataFrame (voir Observation).

    Un objet Observations peux etre instancie de multiples facons a l'aide des
    fonctions proposees par Pandas, sous reserve de respecter le nom des
    colonnes et leur typage:
        DataFrame.from_records: constructor from tuples, also record arrays
        DataFrame.from_dict: from dicts of Series, arrays, or dicts
        DataFrame.from_csv: from CSV files
        DataFrame.from_items: from sequence of (key, value) pairs
        read_csv / read_table / read_clipboard
        ...

    On peux obtenir une pandas.Series ne contenant que l'index et res avec:
        obs = observations.res

    """

    def __new__(cls, *observations):
        """Constructeur.

        Arguments:
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
                    raise TypeError('{} in not an Observation'.format(obs))
                obss.append(obs)

        except Exception:
            raise

        # prepare a tmp numpy.array
        array = _numpy.array(object=obss)

        # get the pandas.DataFrame
        index = _pandas.Index(array['dte'], name='dte')
        obj = _pandas.DataFrame(
            data=array[list(array.dtype.names[1:])],
            index=index
        )
        # TODO - can't subclass the DataFRame object
        # return obj.view(cls)
        return obj

    @staticmethod
    def concat(observations, others):
        """Ajoute (concatene) une ou plusieurs observations.

        Arguments:
            observations (Observations)
            others (Observation ou Observations) = observation(s) a ajouter

        Pour agreger 2 Observations, on peux aussi utiliser la methode append
        des DataFrame ou bien directement la fonction concat de pandas.

        Attention, les DataFrame ne sont JAMAIS modifies, ces fonctions
        retournent un nouveau DataFrame.

        """

        # TODO - can't write a instance method to do that
        #        (can't subclass DataFrame !)

        try:
            return _pandas.concat([observations, others])

        except Exception:
            return _pandas.concat([observations, Observations(others)])


#-- class Serie ---------------------------------------------------------------
class Serie(object):

    """Classe Serie.

    Classe pour manipuler des series d'observations hydrometriques.

    Proprietes:
        entite (Sitehydro, Stationhydro ou Capteur)
        grandeur (char in NOMENCLATURE[509]) = H ou Q
        statut (int in NOMENCLATURE[510]) = donnee brute, corrigee...
        dtdeb (datetime.datetime)
        dtfin (datetime.datetime)
        dtprod (datetime.datetime)
        observations (Observations)

    """

    dtdeb = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)
    dtprod = _composant.Datefromeverything(required=False)
    grandeur = _composant.Nomenclatureitem(nomenclature=509)
    statut = _composant.Nomenclatureitem(nomenclature=510)

    # TODO - Serie others attributes

    # sysalti
    # perime
    # contact
    # refalti OU courbetarage

    def __init__(
        self, entite=None, grandeur=None, statut=0,
        dtdeb=None, dtfin=None, dtprod=None, observations=None, strict=True
    ):
        """Initialisation.

        Arguments:
            entite (Sitehydro, Stationhydro ou Capteur)
            grandeur (char in NOMENCLATURE[509]) = H ou Q
            statut (int in NOMENCLATURE[510], defaut 0) = donnee brute,
                corrigee...
            dtdeb (numpy.datetime64)
            dtfin (numpy.datetime64)
            dtprod (numpy.datetime64)
            observations (Observations)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite des parametres

        """

        # -- simple properties --
        self._strict = bool(strict)

        # adjust the descriptor
        vars(self.__class__)['grandeur'].strict = self._strict
        vars(self.__class__)['grandeur'].required = self._strict
        vars(self.__class__)['statut'].strict = self._strict

        # -- descriptors --
        self.dtdeb = dtdeb
        self.dtfin = dtfin
        self.dtprod = dtprod
        self.grandeur = grandeur
        self.statut = statut

        # -- full properties --
        self._entite = self._observations = None
        self.entite = entite
        self.observations = observations

    # -- property entite --
    @property
    def entite(self):
        """Return entite hydro."""
        return self._entite

    @entite.setter
    def entite(self, entite):
        """Set entite hydro."""
        # entite must be a site, a station or a capteur
        try:
            if (
                (self._strict) and (
                    not isinstance(
                        entite,
                        (
                            _sitehydro.Sitehydro, _sitehydro.Stationhydro,
                            _sitehydro.Capteur
                        )
                    )
                )
            ):
                raise TypeError(
                    'entite must be a Sitehydro, a Stationhydro or a Capteur'
                )
            self._entite = entite
        except:
            raise

    # -- property observations --
    @property
    def observations(self):
        """Return observations."""
        return self._observations

    @observations.setter
    def observations(self, observations):
        """Set observations."""
        try:

            if (self._strict):
                # we check we have a res column...
                # ... and that index contains datetimes
                observations.res
                # FIXME - should fail with datetime64 object.
                #         Use .item().isoformat()
                observations.index[0].isoformat()
            self._observations = observations

        except:
            raise TypeError('observations incorrect')

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        # compute entite name
        if self.entite is None:
            entite = '<une entite inconnue>'
        else:
            try:
                entite = '{} {}'.format(
                    _sitehydro._ARTICLE[self.entite.__class__],
                    self.entite.__unicode__()
                )
            except (AttributeError, KeyError):
                entite = self.entite

        # prepare observations
        if self.observations is None:
            obs = '<sans observations>'
        elif len(self.observations) <= 30:
            obs = self.observations.to_string()
            obs += '\n%s values' % len(self.observations)
        else:
            obs = '{0}\n...\n{1}'.format(
                self.observations[:15].to_string(),
                '\n'.join(self.observations[-15:].to_string().split('\n')[2:])
            )
            obs += '\n%s' % self.observations.__unicode__()

        # action !
        return 'Serie {0} sur {1}\n'\
               'Statut {2}::{3}\n'\
               '{4}\n'\
               'Observations:\n{5}'.format(
                   self.grandeur or '<grandeur inconnue>',
                   entite,
                   self.statut,
                   _NOMENCLATURE[510][self.statut].lower(),
                   '-' * 72,
                   obs
               )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)

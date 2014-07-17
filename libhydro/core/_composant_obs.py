# -*- coding: utf-8 -*-
"""Module composant_obs.

Ce module contient les elements communs aux modules obshydro et obsmeteo.

Il integre les classes:
    # Observations
    # Serie

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import numpy as _numpy
import pandas as _pandas

from . import _composant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """1.0b"""
__date__ = """2014-07-17"""

#HISTORY
#V0.1 - 2014-07-16
#    split the composant file in 3 parts


#-- class Observations --------------------------------------------------------
class Observations(_pandas.DataFrame):

    """Base class observations for both hydrometrie and meteorologie.

    Returns a pandas.DataFrame from an iterable of elementary observations.

    """

    def __new__(cls, observation_class, observations):
        """Constructeur.

        Arguments:
            observation_class (class)
            observations (iterable) = an iterable of observation_class elements

        """

        # FIXME - awfully slow process :-/

        # prepare a list of observations
        obss = []
        try:
            for i, obs in enumerate(observations):
                if not isinstance(obs, observation_class):
                    raise TypeError(
                        'element {} is not a {}'.format(
                            i, observation_class
                        )
                    )
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
        # TODO - can't subclass the DataFrame object
        # return obj.view(cls)
        return obj

    @staticmethod
    def concat(observations, others):
        """Ajoute (concatene) une ou plusieurs observations.

        Arguments:
            observations (Observations)
            others (Observation ou Observations) = observation(s) a ajouter

        Pour agreger 2 Observations, on peut aussi utiliser la methode append
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

    """Base class Serie.

    Classe de base pour manipuler des series d'observations hydrometriques ou
    meteorologiques.

    Proprietes:
        dtdeb (datetime.datetime)
        dtfin (datetime.datetime)
        dtprod (datetime.datetime)
        observations (Observations)

    """

    # TODO - Serie others attributes

    # contact

    dtdeb = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)
    dtprod = _composant.Datefromeverything(required=False)

    def __init__(
        self, dtdeb=None, dtfin=None, dtprod=None, observations=None,
        strict=True
    ):
        """Initialisation.

        Arguments:
            dtdeb (numpy.datetime64)
            dtfin (numpy.datetime64)
            dtprod (numpy.datetime64)
            observations (Observations)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite des parametres

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- descriptors --
        self.dtdeb = dtdeb
        self.dtfin = dtfin
        self.dtprod = dtprod

        # -- full properties --
        self._observations = None
        self.observations = observations

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

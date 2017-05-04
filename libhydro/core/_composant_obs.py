# coding: utf-8
"""Module composant_obs.

Ce module contient les elements communs aux modules obshydro et obsmeteo.

Il integre les classes:
    # Observations
    # Serie

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import numpy as _numpy
import pandas as _pandas

from . import (_composant, intervenant as _intervenant)


# -- strings ------------------------------------------------------------------
__version__ = '1.0.5'
__date__ = '2017-05-03'

# HISTORY
# V1.0 - 2014-07-16
#   add the Serie.concat function
#   split the composant file in 3 parts


# -- class Observations -------------------------------------------------------
class Observations(_pandas.DataFrame):

    """Base class observations for both hydrometrie and meteorologie.

    Returns a pandas.DataFrame from an iterable of elementary observations.

    WARNING, comparison of Pandas.DataFrames requires:
        (obs == obs).all().all()

    """

    def __new__(cls, observation_class, observations):
        """Constructeur.

        Arguments:
            observation_class (class)
            observations (iterable) = an iterable of observation_class elements

        """

        # FIXME - awfully slow process :-/

        # None case
        if observations is None:
            return

        # other cases
        # prepare a list of observations
        obss = []
        try:
            for i, obs in enumerate(observations):
                if not isinstance(obs, observation_class):
                    raise TypeError('element {} is not a {}'.format(
                        i, observation_class))
                obss.append(obs)

        except Exception:
            raise

        # prepare a tmp numpy.array
        array = _numpy.array(object=obss)

        # get the pandas.DataFrame
        index = _pandas.Index(array['dte'], name='dte')
        obj = _pandas.DataFrame(
            data=array[list(array.dtype.names[1:])], index=index)
        # TODO - can't subclass the DataFrame object
        # obj.__eq__ = _composant.__eq__
        # obj.__ne__ = _composant.__ne__
        # return obj.view(cls)
        return obj

    # -- static methods --
    @staticmethod
    def concat(observations, duplicates='raise', sort=False):
        """Concatene plusieurs observations.

        Arguments:
            observations (iterable d'Observations) = observations a concatener
            duplicates (string in ['raise' (defaut), 'drop']) = comportement
                vis-a-vis des doublons dans l'index temporel
            sort (bool, defaut False) = tri par l'index

        Pour agreger 2 Observations, on peut aussi utiliser la methode append
        des DataFrame ou bien directement la fonction concat de pandas.

        Attention, les DataFrame ne sont JAMAIS modifies, ces fonctions
        retournent un nouveau DataFrame.

        """

        # TODO - can't write a instance method to do that
        #        (can't subclass DataFrame !)

        # pre-conditions
        if not isinstance(duplicates, (str, unicode)) or \
                duplicates not in ('raise', 'drop'):
            raise ValueError(
                "invalid str for duplicates: '{}'".format(duplicates))

        # action
        df = _pandas.concat(
            observations, verify_integrity=(duplicates != 'drop'))
        if duplicates == 'drop':
            # group by the datetime index and take the most recent chunk
            df = df.groupby(level=0).last()
        if sort:
            df.sort(inplace=True)

        # return
        return df


# -- class Serie --------------------------------------------------------------
class Serie(object):

    """Base class Serie.

    Classe de base pour manipuler des series d'observations hydrometriques ou
    meteorologiques.

    Proprietes:
        dtdeb (datetime.datetime)
        dtfin (datetime.datetime)
        dtprod (datetime.datetime)
        contact (intervenant.Contact)
        observations (Observations)

    """

    # TODO - Serie others attributes

    # contact

    dtdeb = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)
    dtprod = _composant.Datefromeverything(required=False)

    def __init__(self, dtdeb=None, dtfin=None, dtprod=None, contact=None,
                 observations=None, strict=True):
        """Initialisation.

        Arguments:
            dtdeb (numpy.datetime64)
            dtfin (numpy.datetime64)
            dtprod (numpy.datetime64)
            observations (Observations)
            contact (intervenant.Contact)
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
        self._contact = self._observations = None
        self.contact = contact
        self.observations = observations

    # -- property contact --
    @property
    def contact(self):
        """Return contact."""
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Set contact."""
        if self._strict and contact is not None and \
                not isinstance(contact, _intervenant.Contact):
            raise TypeError('contact incorrect')
        self._contact = contact

    # -- property observations --
    @property
    def observations(self):
        """Return observations."""
        return self._observations

    @observations.setter
    def observations(self, observations):
        """Set observations."""
        try:

            if (self._strict) and (observations is not None):
                # we check we have a res column...
                if not hasattr(observations, 'res'):
                    raise TypeError()
                # ... and that index contains datetimes
                # FIXME - should fail with datetime64 object.
                #         Use .item().isoformat()
                if not hasattr(observations.index[0], 'isoformat'):
                    raise TypeError()
            self._observations = observations

        except:
            raise TypeError('observations incorrect')

    # -- static methods --
    @staticmethod
    def concat(series, duplicates='raise', sort=False):
        """Concatene des series de base.

        Methode a surcharger pour les series hydro et meteo.

        Return a dic: {'dtdeb': dtdeb, 'dtfin': dtfin, 'dtprod': dtprod,
                       'contact': contact, 'observations': observations}

        Arguments:
            series (iterable de Serie) = series a concatener
            duplicates (str in ['raise' (defaut), 'drop']) = comportement
                vis-a-vis des doublons dans l'index temporel des observations
            sort (bool, defaut False) = tri des observations par l'index

        """
        # init
        dtdeb, dtfin, dtprod, contact, observations = (None, ) * 5

        # concatenate simple properties
        for serie in series:
            dtdeb = serie.dtdeb if dtdeb is None else min(dtdeb, serie.dtdeb)
            dtfin = serie.dtfin if dtfin is None else max(dtfin, serie.dtfin)
            dtprod = serie.dtprod if dtprod is None \
                else min(dtprod, serie.dtprod)
            if contact is None:
                contact = serie.contact
            elif contact != serie.contact:
                raise ValueError(
                    "can't concatenate series, contact doesn't match")

        # concatenate observations
        observations = Observations.concat(
            [s.observations for s in series], duplicates=duplicates, sort=sort)

        # return
        return {'dtdeb': dtdeb, 'dtfin': dtfin, 'dtprod': dtprod,
                'contact': contact, 'observations': observations}

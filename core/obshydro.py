# -*- coding: utf-8 -*-
"""Module obshydro.

Ce module contient les classes:
    # Observation
    # Observations
    # Serie

et quelques fonctions utiles:
    # concat() pour concatener des observations


On peux aussi utiliser directement les classes de la librairie Pandas, les
Series ou les DataFrame.

Exemple pour instancier une Series:
    datas = pandas.Series(
        data = [100, 110, 120],
        index = [
            datetime.datetime(2012, 5, 1),
            datetime.datetime(2012, 5, 2),
            datetime.datetime(2012, 5, 3)
        ]
        dtype = None,
        name='observations de debit'
)

Exemple pour instancier un DataFrame:
    hauteurs = pandas.DataFrame({
        'H2354310': Series_de_hauteurs_1,
        'H4238907': Series_de_hauteurs_2,
        ...
    })

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import numpy as _np
import pandas as _pd

from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from . import sitehydro as _sitehydro


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1b"""
__date__ = """2013-07-31"""

#HISTORY
#V0.1 - 2013-07-18
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - many many properties


#-- class Observation ---------------------------------------------------------
class Observation(_np.ndarray):
    """Classe observation.

    Classe pour manipuler une observation elementaire.

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

    Usage:
        Getter => observation.['x'].item()
        Setter => observation.['x'] = value

    """

    DTYPE = _np.dtype([
        (str('dte'), _np.datetime64(None, str('s'))),
        (str('res'), _np.float),
        (str('mth'), _np.int8),
        (str('qal'), _np.int8),
        (str('cnt'), _np.bool)
    ])

    def __new__(cls, dte, res, mth=0, qal=16, cnt=True):
        if not isinstance(dte, _np.datetime64):
            dte = _np.datetime64(dte)
        if (mth != 0) and (mth not in _NOMENCLATURE[507]):
            raise ValueError('methode incorrecte')
        if (qal != 16) and (qal not in _NOMENCLATURE[515]):
            raise ValueError('qualification incorrecte')
        obj = _np.array(
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
            _NOMENCLATURE[507][self['mth'].item()],
            _NOMENCLATURE[515][self['qal'].item()],
            'continue' if self['cnt'].item() else 'discontinue',
            *self['dte'].item().isoformat().split('T')
        ).encode('utf-8')


#-- class Observations --------------------------------------------------------
class Observations(_pd.DataFrame):
    """Class Observations.

    Classe pour manipuler une collection d'observations hydrometriques, sous la
    forme d'un pandas.DataFrame (les objets instancies sont des DataFrame).

    L'index est un pandas.DatetimeIndex qui represente les dates d'observation.

    Les donnees sont contenues dans 4 colonnes du DataFrame (voir Observation).

    Un objet Obervations peux etre instancie de multiples facons a l'aide des
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
                    raise TypeError('{} in not an Observation'.format(obs))
                obss.append(obs)

        except Exception:
            raise

        # prepare a tmp numpy.array
        array = _np.array(object=obss)

        # get the pandas.DataFrame
        obj = _pd.DataFrame(
            data=array[list(array.dtype.names[1:])],
            index=array['dte']
        )
        # FIXME - can't subclass the DataFRame object
        # return obj.view(cls)
        return obj


#-- Observations functions ----------------------------------------------------
def concat(observations, others):
    """Ajoute (concatene) une ou plusieurs observations.

    Arguments:
        observations (Observations)
        others (Observation ou Observations) = observation(s) a ajouter

    Pour agreger 2 Observations, on peux aussi utiliser la methode append des
    DataFrame ou bien directement la fonction concat de pandas.

    Attention, les DataFrame ne sont JAMAIS modifies, ces fonctions retournent
    un nouveau DataFrame.

    """

    # TODO - can't write a method to do that (subclassing DataFrame is hard !)

    try:
        return _pd.concat([observations, others])
    except Exception:
        return _pd.concat([observations, Observations(others)])


#-- class Serie ---------------------------------------------------------------
class Serie(object):
    """Classe Serie.

    Classe pour manipuler des series d'observations hydrometriques.

    Proprietes:
        entite (Sitehydro, Stationhydro ou Capteur)
        grandeur (char in NOMENCLATURE[509]) = H ou Q
        statut (int in NOMENCALTURE[510]) = donnee brute, corrigee...
        observations (Observations)

    """

    # ** TODO - others attributes **
    # strict (bool, defaut True) = en mode permissif, les contrôles de
    #     validite sur les proprietes ne sont paa appliques
    # datedebut
    # datefin
    # dateprod
    # sysalti
    # perime
    # contact
    # refalti OU courbetarage

    def __init__(
        self, entite=None, grandeur=None, statut=0,
        observations=None, strict=True
    ):
        """Constructeur.

        Parametres:
            entite (Sitehydro, Stationhydro ou Capteur)
            grandeur (char in NOMENCLATURE[509]) = H ou Q
            statut (int in NOMENCALTURE[510], defaut 0) = donnee brute,
                corrigee...
            observations (Observations)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite des parametres

        """

        # -- simple properties --
        self._strict = strict

        # FIXME - shouldn't we control something here ?
        self.observations = observations

        # -- full properties --
        self._entite = self._grandeur = self._observations = None
        self._statut = 0
        if entite:
            self.entite = entite
        if grandeur:
            self.grandeur = grandeur
        if statut:
            self.statut = statut

    # -- property entite --
    @property
    def entite(self):
        """entite hydro."""
        return self._entite

    @entite.setter
    def entite(self, entite):
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
                raise Exception
            self._entite = entite
        except:
            raise TypeError(
                'entite must be a Sitehydro, a Stationhydro or a Capteur'
            )

    # @entite.deleter
    # def entite(self):
    #     del self._entite

    # -- property grandeur --
    @property
    def grandeur(self):
        """grandeur hydro."""
        return self._grandeur

    @grandeur.setter
    def grandeur(self, grandeur):
        try:
            grandeur = unicode(grandeur)
            if (self._strict) and (grandeur not in _NOMENCLATURE[509]):
                raise Exception
            self._grandeur = grandeur
        except:
            raise ValueError('grandeur incorrect')

    # @grandeur.deleter
    # def grandeur(self):
    #     del self._grandeur

    # -- property statut --
    @property
    def statut(self):
        """statut hydro."""
        return self._statut

    @statut.setter
    def statut(self, statut):
        try:
            statut = int(statut)
            if statut in _NOMENCLATURE[510]:
                self._statut = statut
            else:
                if (self._strict):
                    raise Exception
                else:
                    self._statut = 0
        except:
            raise ValueError('statut incorrect')

    # @statut.deleter
    # def statut(self):
    #     del self._statut

    # -- other methods --
    def __str__(self):
        """String representation."""
        # compute class name: cls = (article, classe)
        try:
            cls = unicode(self.entite.__class__.__name__)
            cls = ('{} '.format(_sitehydro.ARTICLE[cls]), cls.lower())
        except Exception:
            cls = ("l'", 'entite')

        # compute code
        if self.entite is not None:
            try:
                code = self.entite.code
            except Exception:
                code = self.entite

        # action !
        return 'Serie {0} sur {1}{2} {3}\nstatut {4}::{5}\n{6}\n{7} '.format(
            self.grandeur or '-',
            cls[0],
            cls[1],
            code,
            self.statut,
            _NOMENCLATURE[510][self.statut].lower(),
            '-' * 72,
            self.observations.__str__ or '-'
        ).encode('utf-8')

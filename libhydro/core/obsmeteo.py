# -*- coding: utf-8 -*-
"""Module obsmeteo.

Ce module contient les classes:
    # Serie
    # Observations
    # Observation

et quelques fonctions utiles:
    # Observations.concat() pour concatener des observations

 La Serie est le conteneur de reference pour les observations meteorologiques.
 Les observations y sont contenues dans l'attribut du meme nom, sous la forme
 d'un pandas.DataFrame dont l'index est une serie de timestamp.

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import numpy as _numpy

from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from . import _composant
from . import sitemeteo as _sitemeteo


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1c"""
__date__ = """2014-07-16"""

#HISTORY
#V0.1 - 2014-07-11
#    first shot

#-- todos ---------------------------------------------------------------------
# PROGRESS - Serie 0% - Observations 0% - Observation 0%


#-- class Observation ---------------------------------------------------------
class Observation(_numpy.ndarray):

    """Classe observation.

    Classe pour manipuler une observation meteorologique elementaire.

    Subclasse de numpy.array('dte', 'res', 'ind', 'mth', 'qal'), les elements
    etant du type DTYPE.

    Date et resultat sont obligatoires, les autres elements ont une valeur par
    defaut. Pour les observations de pluie, la date est celle de la fin du
    cumul (et la duree n'est pas indiquee ici, mais dans la Serie).

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
            la NOMENCLATURE[512])
        qal (numpy.int8, defaut 16) = qualification de la donnees suivant la
            NOMENCLATURE[508]
        qua (int de 0 a 100, defaut 100) = indice de qualite de la mesure

    Usage:
        Getter => observation.['x'].item()
        Setter => observation.['x'] = value

    """

    DTYPE = _numpy.dtype([
        (str('dte'), _numpy.datetime64(None, str('s'))),
        (str('res'), _numpy.float),
        (str('mth'), _numpy.int8),
        (str('qal'), _numpy.int8),
        (str('qua'), _numpy.int8)
    ])

    def __new__(cls, dte, res, mth=0, qal=16, qua=100):
        if not isinstance(dte, _numpy.datetime64):
            dte = _numpy.datetime64(dte, 's')
        if mth not in _NOMENCLATURE[512]:
            raise ValueError('incorrect method ')
        if qal not in _NOMENCLATURE[508]:
            raise ValueError('incorrect qualification')
        if not (0 <= qua <= 100):
            raise ValueError('incorrect quality')
        obj = _numpy.array(
            (dte, res, mth, qal, qua),
            dtype=Observation.DTYPE
        ).view(cls)
        return obj

    # def __array_finalize__(self, obj):
    #     if obj is None:
    #         return

    def __unicode__(self):
        """Return unicode representation."""
        return '''{0} le {4} a {5} UTC ''' \
               '''(valeur obtenue par {1}, {2}, qualite {3}%)'''.format(
                   self['res'].item(),
                   _NOMENCLATURE[512][self['mth'].item()],
                   _NOMENCLATURE[508][self['qal'].item()],
                   self['qua'].item(),
                   *self['dte'].item().isoformat().split('T')
               )

    def __str__(self):
        return _composant.__str__(self)


#-- class Observations --------------------------------------------------------
class Observations(_composant.Observations):

    """Classe Observations.

    Classe pour manipuler une collection d'observations meteorologiques, sous
    la forme d'un pandas.DataFrame (les objets instancies sont des DataFrame).

    L'index est un pandas.DatetimeIndex qui represente les dates d'observation
    (date de fin du cumul pour les donnees de pluie) [Nb: les pandas.Period ne
    conviennent actuellement pas pour notre usage]

    A la difference des observations hydrometriques, les observations
    meteorologiques devraient etre a pas de temps fixe et les donnes manquantes
    representees par la valeur 'Nan' (not a number).

    Les donnees sont contenues dans 4 colonnes du DataFrame (voir Observation).

    Un objet Observations peut etre instancie de multiples facons a l'aide des
    fonctions proposees par Pandas, sous reserve de respecter le nom des
    colonnes et leur typage:
        DataFrame.from_records: constructor from tuples, also record arrays
        DataFrame.from_dict: from dicts of Series, arrays, or dicts
        DataFrame.from_csv: from CSV files
        DataFrame.from_items: from sequence of (key, value) pairs
        read_csv / read_table / read_clipboard
        ...

    On peut obtenir une pandas.Series ne contenant que l'index et res avec:
        obs = observations.res

    """

    # NB: les pandas.Period ne conviennent pas pour les observations meteo,
    # car la frequence ne peux pas etre un multiple des unites elementaires
    # (heure, minute...). A noter aussi que la date de reference est le debut
    # de la periode (et non pas la fin)

    def __new__(cls, *observations):
        """Constructeur.

        Arguments:
            observations (un nombre quelconque d'Observation)

        Exemples:
            obs = Observations(obs1)  # une seule Observation
            obs = Observations(obs1, obs2, ..., obsn)  # n Observation
            obs = Observations(*observations)  #  une liste d'Observation

        """
        return _composant.Observations.__new__(cls, Observation, observations)


#-- class Serie ---------------------------------------------------------------
class Serie(object):

    """Classe Serie.

    Classe pour manipuler des series d'observations meteorologiques.

    Proprietes:
        grandeurmeteo (Grandeurmeteo)
        duree (int, defaut 0) =
            duree des cumuls, 0 pour les donnees instantanees
        statut (int parmi NOMENCLATURE[511]) = donnee brute, corrigee...
        dtdeb (datetime.datetime)
        dtfin (datetime.datetime)
        dtprod (datetime.datetime)
        observations (Observations)

    """

    # TODO - Serie others attributes

    # contact (in the base class)

    statut = _composant.Nomenclatureitem(nomenclature=511)

    def __init__(
        self, grandeurmeteo=None, duree=0, statut=0,
        dtdeb=None, dtfin=None, dtprod=None, observations=None, strict=True
    ):
        """Initialisation.

        Arguments:
            grandeurmeteo (Grandeurmeteo)
            duree (int, defaut 0) = duree des cumuls, 0 pour les donnees
                instantanees
            statut (int parmi NOMENCLATURE[511], defaut 0) = donnee brute,
                corrigee...
            dtdeb (numpy.datetime64)
            dtfin (numpy.datetime64)
            dtprod (numpy.datetime64)
            observations (Observations)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite des parametres

        """

        # -- super --
        super(Serie, self).__init__(
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod,
            observations=observations, strict=strict
        )

        # adjust the descriptor
        vars(self.__class__)['statut'].strict = self._strict

        # -- descriptors --
        self.statut = statut

        # -- full properties --
        self._grandeurmeteo = None
        self.grandeurmeteo = grandeurmeteo

    # -- property grandeurmeteo --
    @property
    def grandeurmeteo(self):
        """Return grandeurmeteo."""
        return self._grandeurmeteo

    @grandeurmeteo.setter
    def grandeurmeteo(self, grandeurmeteo):
        """Set grandeurmeteo."""
        try:
            if (
                (self._strict) and
                not isinstance(grandeurmeteo, _sitemeteo.Grandeurmeteo)
            ):
                raise TypeError(
                    'grandeurmeteo must be a Grandeurmeteo'
                )
            self._grandeurmeteo = grandeurmeteo
        except:
            raise

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        # prepare observations
        # FIXME - factorize
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
        return 'Serie {0} sur le site meteorologique {1}\n'\
               'Statut {2}::{3}\n'\
               '{4}\n'\
               'Observations:\n{5}'.format(
                   self.grandeurmeteo.typegrandeur or
                   '<grandeurmeteo inconnue>',
                   self.grandeurmeteo.sitemeteo.code or '<sans code>',
                   self.statut,
                   _NOMENCLATURE[511][self.statut].lower(),
                   '-' * 72,
                   obs
               )

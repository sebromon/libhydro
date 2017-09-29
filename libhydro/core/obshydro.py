# coding: utf-8
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

# On peut aussi utiliser directement les classes de la librairie Pandas, les
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

# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import numpy as _numpy

from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from . import (_composant, _composant_obs)
from . import sitehydro as _sitehydro


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.3"""
__date__ = """2017-06-09"""

# HISTORY
# V0.3.1 - SR - 2016-06-29
# change type of cnt to int (nomenclature[923]
# V0.3 - SR - 2016-06-09
# add sysalti and perim properties
# V0.2 - 2014-07-15
#   add the Serie.concat static method
#   use the composant_obs module
# V0.1 - 2013-07-18
#   first shot


# -- todos --------------------------------------------------------------------
# PROGRESS - Serie 70% - Observations 100% - Observation 100%
# FIXME - integriey checks entity / grandeur /statut
# ADMIT_SERIE = {
#     Sitehydro: 'Q',

#     Station: type station...

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


# -- class Observation --------------------------------------------------------
class Observation(_numpy.ndarray):

    """Classe observation.

    Classe pour manipuler une observation hydrometrique elementaire.

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
        cnt (numpy.int8, defaut 0) = continuite de la donnee suivant la
            NOMENCLATURE[923]

    Usage:
        Getter => observation.['x'].item()
        Setter => observation.['x'] = value

    """

    DTYPE = _numpy.dtype([
        (str('dte'), _numpy.datetime64(None, str('s'))),
        (str('res'), _numpy.float),
        (str('mth'), _numpy.int8),
        (str('qal'), _numpy.int8),
        (str('cnt'), _numpy.int8)
    ])

    def __new__(cls, dte, res, mth=0, qal=16, cnt=0):
        if not isinstance(dte, _numpy.datetime64):
            dte = _numpy.datetime64(dte, 's')
        if int(mth) not in _NOMENCLATURE[507]:
            raise ValueError('incorrect method')
        if int(qal) not in _NOMENCLATURE[515]:
            raise ValueError('incorrect qualification')
        # cnt bol SANDRE V1.1 int in V2
        # conversion booleen  to int
        if isinstance(cnt, bool):
            cnt = 0 if cnt else 1
        if int(cnt) not in _NOMENCLATURE[923]:
            raise ValueError('incorrect continuite')
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
                   'continue' if self['cnt'].item() == 0 else 'discontinue',
                   *self['dte'].item().isoformat().split('T')
               )

    __str__ = _composant.__str__


# -- class Observations -------------------------------------------------------
class Observations(_composant_obs.Observations):

    """Classe Observations.

    Classe pour manipuler une collection d'observations hydrometriques, sous la
    forme d'un pandas.DataFrame (les objets instancies sont des DataFrame).

    L'index est un pandas.DatetimeIndex qui represente les dates d'observation.

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

    On peut iterer dans le DataFrame avec la fonction iterrows().

    ATTENTION, la comparaison de Pandas.DataFrames necessite d'ecrire:
        (obs == obs).all().all()

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
        return _composant_obs.Observations.__new__(
            cls, Observation, observations
        )


# -- class Serie --------------------------------------------------------------
class Serie(_composant_obs.Serie):

    """Classe Serie.

    Classe pour manipuler des series d'observations hydrometriques.

    Proprietes:
        entite (Sitehydro, Station ou Capteur)
        grandeur (char parmi NOMENCLATURE[509]) = H ou Q
        statut (int parmi NOMENCLATURE[510]) = donnee brute, corrigee...
        dtdeb (datetime.datetime)
        dtfin (datetime.datetime)
        dtprod (datetime.datetime)
        sysalti (int parmi NOMENCLATURE[76])
        perim (booleen ou None)
        contact (intervenant.Contact)
        observations (Observations)

    """

    # TODO - Serie others attributes

    # refalti OU courbetarage

    grandeur = _composant.Nomenclatureitem(nomenclature=509)
    statut = _composant.Nomenclatureitem(nomenclature=510)
    sysalti = _composant.Nomenclatureitem(nomenclature=76)

    def __init__(
            self, entite=None, grandeur=None, statut=0,
            dtdeb=None, dtfin=None, dtprod=None, sysalti=31, perime=None,
            contact=None, observations=None, strict=True
    ):
        """Initialisation.

        Arguments:
            entite (Sitehydro, Station ou Capteur)
            grandeur (char parmi NOMENCLATURE[509]) = H ou Q
            statut (int parmi NOMENCLATURE[510], defaut 0) = donnee brute,
                corrigee...
            dtdeb (numpy.datetime64)
            dtfin (numpy.datetime64)
            dtprod (numpy.datetime64)
            sysalti (int parmi NOMENCLATURE[76])
            perim (booleen ou None)
            contact (intervenant.Contact)
            observations (Observations)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite des parametres

        """

        # -- super --
        super(Serie, self).__init__(
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, contact=contact,
            observations=observations, strict=strict
        )

        # -- adjust the descriptor --
        vars(Serie)['grandeur'].strict = self._strict
        vars(Serie)['grandeur'].required = self._strict
        vars(Serie)['statut'].strict = self._strict
        vars(Serie)['sysalti'].strict = self._strict

        # -- descriptors --
        self.grandeur = grandeur
        self.statut = statut
        self.sysalti = sysalti

        # -- full properties --
        self._entite = None
        self.entite = entite
        self._perime = None
        self.perime = perime

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
                            _sitehydro.Sitehydro, _sitehydro.Station,
                            _sitehydro.Capteur
                        )
                    )
                )
            ):
                raise TypeError(
                    'entite must be a Sitehydro, a Station or a Capteur'
                )
            self._entite = entite
        except:
            raise

    # -- property perime --
    @property
    def perime(self):
        """Return perime."""
        return self._perime

    @perime.setter
    def perime(self, perime):
        """Set perime."""
        self._perime = bool(perime) if (perime is not None) else None

    # -- static methods --
    @staticmethod
    def concat(series, duplicates='raise', sort=False):
        """Concatene plusieurs series.

        Leve une exception si l'entite ou la grandeur des series differe, sinon
        retourne une nouvelle serie dont le statut est le plus faible de celui
        des series a concatener.

        Arguments:
            series (iterable de Serie) = series a concatener
            duplicates (string in ['raise' (defaut), 'drop']) = comportement
                vis-a-vis des doublons dans l'index temporel des observations
            sort (bool, defaut False) = tri des observations par l'index

        """
        # check the specific attributes
        entite, grandeur, statut = (None, ) * 3
        for serie in series:
            if entite is None:
                entite = serie.entite
            elif entite != serie.entite:
                raise ValueError(
                    "can't concatenate series, entite doesn't match"
                )
            if grandeur is None:
                grandeur = serie.grandeur
            elif grandeur != serie.grandeur:
                raise ValueError(
                    "can't concatenate series, grandeur doesn't match"
                )
            statut = serie.statut if statut is None \
                else min(statut, serie.statut)

        # call the base serie concat function
        concat = _composant_obs.Serie.concat(
            series=series, duplicates=duplicates, sort=sort
        )

        # return
        return Serie(entite=entite, grandeur=grandeur, statut=statut, **concat)

    # -- special methods --
    __all__attrs__ = (
        'entite', 'grandeur', 'statut', 'dtdeb', 'dtfin', 'dtprod',
        'contact', 'observations'
    )
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        # init
        try:
            entite = '{} {}'.format(
                _sitehydro._ARTICLE[self.entite.__class__],
                self.entite.__unicode__()
            )
        except Exception:
            entite = '<une entite inconnue>'
        try:
            obs = self.observations.to_string(
                max_rows=15, show_dimensions=True
            )
        except Exception:
            obs = '<sans observations>'

        perime = ''
        if self.perime is not None:
            if self.perime:
                perime = ' perime'
            else:
                perime = ' non perime'
        # action !
        return 'Serie {0}{6} sur {1}\n'\
               'Statut {2}::{3}\n'\
               '{4}\n'\
               'Observations:\n{5}'.format(
                   self.grandeur or '<grandeur inconnue>',
                   entite,
                   self.statut,
                   _NOMENCLATURE[510][self.statut].lower(),
                   '-' * 72,
                   obs,
                   perime
               )

    __str__ = _composant.__str__

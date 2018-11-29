# -*- coding: utf-8 -*-
"""Module obselaboreehydro.

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
import pandas as _pandas
import datetime as _datetime

from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from libhydro.core import (_composant,
                           sitehydro as _sitehydro,
                           intervenant as _intervenant)


# -- strings ------------------------------------------------------------------
__author__ = """Sébastien ROMON """ \
             """<sebastien.romon@developpement-durable.gouv.fr>"""
__version__ = """0.1"""
__date__ = """2018-02-12"""

# HISTORY
# V0.1 - 2018-02-12
#    first shot


# -- todos --------------------------------------------------------------------
# PROGRESS - Serie 70% - Observations 100% - Observation 100%
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


# -- class ObservationElaboree ------------------------------------------------
# TODO balises sysalti,cdcontact et dtdebutRefAlti
class ObservationElaboree(_numpy.ndarray):

    """Classe observation élaborée.

    Classe pour manipuler une observation hydrometrique élaborée.

    Subclasse de numpy.array('entite', 'dte', 'res', 'statut', 'mth', 'qal'),
    les elements etant du type DTYPE.

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
        qal (numpy.int8, defaut 16) = qualification de la donnees suivant la
            NOMENCLATURE[515]
        mth (numpy.int8, defaut 0) = methode d'obtention de la donnees suivant
            la NOMENCLATURE[512])
        cnt (numpy.int8, defaut 0) = continuite de la donnee suivant la
            NOMENCLATURE[923]
        statut (numpy.int8 défaut 4) = statut de l'observation élaborée suivant
            la NOMENCLATURE[510]

    Usage:
        Getter => observation.['x'].item()
        Setter => observation.['x'] = value

    """

    DTYPE = _numpy.dtype([
        (str('dte'), _numpy.datetime64(None, str('s'))),
        (str('res'), _numpy.float),
        (str('mth'), _numpy.int8),
        (str('qal'), _numpy.int8),
        (str('cnt'), _numpy.int8),
        (str('statut'), _numpy.int8)])

    def __new__(cls, dte=None, res=0.0, mth=0, qal=16, cnt=0, statut=0):
        if not isinstance(dte, _numpy.datetime64):
            dte = _numpy.datetime64(dte, 's')
        if qal not in _NOMENCLATURE[515]:
            raise ValueError('incorrect qualification')
        if mth not in _NOMENCLATURE[512]:
            raise ValueError('incorrect method')
        if cnt not in _NOMENCLATURE[923]:
            raise ValueError('incorrect continuite')
        if statut not in _NOMENCLATURE[510]:
            raise ValueError('incorrect statut')

        obj = _numpy.array(
            (dte, res, mth, qal, cnt, statut),
            dtype=ObservationElaboree.DTYPE
        ).view(cls)
        return obj

    # def __array_finalize__(self, obj):
    #     if obj is None:
    #         return

    def __unicode__(self):
        """Return unicode representation."""
        return '''{0} le {5} a {6} UTC de statut {1} ''' \
               '''(valeur obtenue par {2}, {3}, {4})'''.format(
                   self['res'].item(),
                   _NOMENCLATURE[510][self['statut'].item()].lower(),
                   _NOMENCLATURE[512][self['mth'].item()].lower(),
                   _NOMENCLATURE[515][self['qal'].item()].lower(),
                   _NOMENCLATURE[923][self['cnt'].item()].lower(),
                   *self['dte'].item().isoformat().split('T')
               )

    __str__ = _composant.__str__


# -- class ObservationsElaborees ----------------------------------------------
class ObservationsElaborees(object):

    """Classe Observations élaborées.

    Classe pour manipuler une collection d'observations élaborées
    hydrometriques, sous la forme d'un pandas.DataFrame
    (les objets instancies sont des DataFrame).

    L'index est un pandas.DatetimeIndex   les dates d'observation.

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
        if observations is None:
            return

        # other cases
        # prepare a list of observations
        obss = []
        try:
            for i, obs in enumerate(observations):
                if not isinstance(obs, ObservationElaboree):
                    raise TypeError(
                        'element {} is not a {}'.format(
                            i, ObservationElaboree
                        )
                    )
                # obss.append(obs)
                obss.append(obs.tolist())

        except Exception:
            raise

        # prepare a tmp numpy.array
        # array = _numpy.array(object=obss)
        array = _numpy.array(object=obss, dtype=ObservationElaboree.DTYPE)

        # make index
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
            return _pandas.concat([observations,
                                   ObservationsElaborees(others)])


# -- class SerieObsElab -------------------------------------------------------
class SerieObsElab(object):

    """Classe Serie d'observations élaborées.

    Classe pour manipuler des séries d'observations
        hydrometriques élaborées.

    Proprietes:
        entite (Sitehydro or Station): Site ou station hydro
        dtprod (datetime.datetime): Date de production
        typegrd(int): type de grandeur suivant la nomenclature 513
        pdt (int or None): pas de temps en minutes
        dtdeb (datetime.datetime): date de début
        dtfin (datetime.datetime): date de fin
        dtactivation (datetime.datetime): date d'activation
        dtdesactivation (datetime.datetime): date de désactivation
        sysalti (int): système altimétrique suiavnt nomenclature 76
        glissante (bool ou None): série glissante
        dtdebrefalti (datetime.datetime ou None): Date de début de validité
            de la référence altimétrique
        contact (intervenant.Contact ou None)
        observations (ObservationsElaborees): observations élaborées
        strict (bool, defaut True)
    """

    typegrd = _composant.Nomenclatureitem(nomenclature=513)
    sysalti = _composant.Nomenclatureitem(nomenclature=76)
    dtprod = _composant.Datefromeverything(required=True)
    dtdeb = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)
    dtactivation = _composant.Datefromeverything(required=False)
    dtdesactivation = _composant.Datefromeverything(required=False)
    dtdebrefalti = _composant.Datefromeverything(required=False)

    def __init__(self, entite=None, dtprod=None, typegrd=None, pdt=None,
                 dtdeb=None, dtfin=None, dtdesactivation=None,
                 dtactivation=None, sysalti=31, glissante=None,
                 dtdebrefalti=None, contact=None, observations=None,
                 strict=True):

        """Initialisation.

        Arguments:
            grandeur (char parmi NOMENCLATURE[513]) = QmJ,qmM
            observations (Observations)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite des paramètres
        """
        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(self.__class__)['typegrd'].strict = self._strict

        # -- descriptors --
        self.dtprod = dtprod
        self.dtdeb = dtdeb
        self.dtfin = dtfin
        self.dtactivation = dtactivation
        self.dtdesactivation = dtdesactivation
        self.dtdebrefalti = dtdebrefalti
        self.sysalti = sysalti
        self.typegrd = typegrd

        # -- full properties --
        self._observations = None
        self.observations = observations
        self._entite = None
        self.entite = entite
        self._pdt = None
        self.pdt = pdt
        self._glissante = None
        self.glissante = glissante
        self._contact = None
        self.contact = contact

    # -- property entite --
    @property
    def entite(self):
        """Return entite hydro."""
        return self._entite

    @entite.setter
    def entite(self, entite):
        """Set entite."""
        try:
            if self._strict:
                # entite must be a site or a station
                if not isinstance(
                        entite, (_sitehydro.Sitehydro, _sitehydro.Station)):
                    raise TypeError('entite must be a Sitehydro or a Station')

            self._entite = entite

        except Exception:
            raise

    # -- property pdt --
    @property
    def pdt(self):
        """Return pdt."""
        return self._pdt

    @pdt.setter
    def pdt(self, pdt):
        """Set pdt."""
        if pdt is None:
            self._pdt = None
            return
        lastc = self.typegrd[-1]
        if isinstance(pdt, _composant.PasDeTemps):
            if lastc == 'H':
                if pdt.unite != _composant.PasDeTemps.HEURES:
                    raise ValueError('pdt must be in hours')
            elif lastc == 'J':
                if pdt.unite != _composant.PasDeTemps.JOURS:
                    raise ValueError('pdt must be in jours')
            # pas de contrôle si différent de H et J
            self._pdt = pdt
        else:
            pdt = int(pdt)
            if lastc == 'H':
                unite = _composant.PasDeTemps.MINUTES
            else:
                unite = _composant.PasDeTemps.JOURS
            self._pdt = _composant.PasDeTemps(
                duree=pdt,
                unite=unite)

    # -- property glissante --
    @property
    def glissante(self):
        """Return glissante."""
        return self._glissante

    @glissante.setter
    def glissante(self, glissante):
        """Set glissante."""
        try:
            if self._strict:
                if glissante not in [None, 0, 1, True, False]:
                    raise TypeError('glissante incorrect')
            if glissante is not None:
                self._glissante = bool(glissante)
            else:
                self._glissante = glissante
        except Exception:
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

            if (self._strict) and (observations is not None):
                # we check we have a res column...
                if not hasattr(observations, 'res'):
                    raise TypeError()
                # ... and that index contains datetimes
                # FIXME - should fail with datetime64 object.
                #         Use .item().isoformat()
                # if not hasattr(observations.index[0], 'isoformat'):
                #     raise TypeError()
            self._observations = observations

        except Exception:
            raise TypeError('observations incorrect')

    @property
    def contact(self):
        """Return contact"""
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Set contact."""
        if self._strict and contact is not None and \
                not isinstance(contact, _intervenant.Contact):
            raise TypeError('contact must be an instance of Contact')
        self._contact = contact

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        if self.typegrd in _NOMENCLATURE[513]:
            lbgrandeur = _NOMENCLATURE[513][self.typegrd]
        else:
            lbgrandeur = 'inconnu'
        try:
            obs = self.observations.to_string(
                max_rows=15, show_dimensions=True
            )
        except Exception:
            obs = '<sans observations>'
        pdt = ''
        if self.pdt is not None:
            pdt = ' de pas de temps {}'.format(self.pdt)
        # action !
        return 'Série de type {0} ({1}){4}\n'\
               '{2}\n'\
               'Observations:\n{3}'.format(
                   self.typegrd or '<type grandeur inconnu>',
                   lbgrandeur,
                   '-' * 72,
                   obs, pdt
               )

    __str__ = _composant.__str__

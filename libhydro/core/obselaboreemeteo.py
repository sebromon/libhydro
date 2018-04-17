# -*- coding: utf-8 -*-
"""Module obselaboreemeteo.

Ce module contient les classes:
    # ObsElabMeteo
    # ObssElabMeteo
    # Ipa
    # SerieObsElabMeteo

et quelques fonctions utiles:
    # ObssElabMeteo.concat() pour concatener des observations

SerieObsElabMeteo est le conteneur de reference
pour les observations élaborées météo.
Les observations y sont contenues dans l'attribut du meme nom, sous la forme
d'un pandas.DataFrame dont l'index est une serie de timestamp.

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime
import math as _math
import numpy as _numpy
import pandas as _pandas


from libhydro.core.nomenclature import NOMENCLATURE as _NOMENCLATURE
from libhydro.core import (_composant,
                           sitehydro as _sitehydro,
                           sitemeteo as _sitemeteo)


class ObsElabMeteo(_numpy.ndarray):
    """Classe ObsElabMeteo.

    Classe pour manipuler une observation élaborée meteorologique élémentaire.

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
        qua (int de 0 a 100, defaut Nan) = indice de qualite de la mesure
        statut (int parmi NOMENCLATURE[510]) = donnee brute, corrigee...

    ATTENTION, Nan != Nan et deux observations sans qualite sont differentes.

    Usage:
        Getter => observation.['x'].item()
        Setter => observation.['x'] = value

    """

    DTYPE = _numpy.dtype([
        (str('dte'), _numpy.datetime64(None, str('s'))),
        (str('res'), _numpy.float),
        (str('mth'), _numpy.int8),
        (str('qal'), _numpy.int8),
        (str('qua'), _numpy.float),  # required for NaN
        (str('statut'), _numpy.int8)])

    def __new__(cls, dte, res, mth=0, qal=16, qua=_numpy.NaN, statut=0):
        if not isinstance(dte, _numpy.datetime64):
            dte = _numpy.datetime64(dte, 's')
        if int(mth) not in _NOMENCLATURE[512]:
            raise ValueError('incorrect method ')
        if int(qal) not in _NOMENCLATURE[508]:
            raise ValueError('incorrect qualification')
        if int(statut) not in _NOMENCLATURE[510]:
            raise ValueError('incorrect statut')
        try:
            qua = float(qua)
            if not _math.isnan(qua):
                if not (0 <= qua <= 100):
                    raise ValueError()
        except Exception:
            raise ValueError('incorrect quality')

        obj = _numpy.array(
            (dte, res, mth, qal, qua, statut),
            dtype=ObsElabMeteo.DTYPE).view(cls)
        return obj

    def __unicode__(self):
        """Return unicode representation."""
        qualite = '%s%%' % self['qua'].item() \
            if not _math.isnan(self['qua'].item()) else '<inconnue>'
        return '''{0} le {5} a {6} UTC de statut {4}''' \
               ''' (valeur obtenue par {1}, {2},''' \
               ''' qualite {3})'''.format(
                   self['res'].item(),
                   _NOMENCLATURE[512][self['mth'].item()].lower(),
                   _NOMENCLATURE[508][self['qal'].item()].lower(),
                   qualite,
                   _NOMENCLATURE[510][self['statut'].item()].lower(),
                   *self['dte'].item().isoformat().split('T'))

    __str__ = _composant.__str__


class ObssElabMeteo(object):
    """Classe Observations élaborées météo.

    Classe pour manipuler une collection d'observations élaborées météo,
    sous la forme d'un pandas.DataFrame
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
                if not isinstance(obs, ObsElabMeteo):
                    raise TypeError(
                        'element {} is not a {}'.format(
                            i, ObsElabMeteo
                        )
                    )
                # obss.append(obs)
                obss.append(obs.tolist())

        except Exception:
            raise

        # prepare a tmp numpy.array
        # array = _numpy.array(object=obss)
        array = _numpy.array(object=obss, dtype=ObsElabMeteo.DTYPE)

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
                                   ObsElabMeteo(others)])


class Ipa(object):
    """Classe Ipa

    Classe pour manipuler des indices de précipitations antérieures.

    Proprietes:
        coefk (float): Coefficient k
        npdt (int or None): Nombre de pas de temps
    """
    def __init__(self, coefk=None, npdt=None):
        self._coefk = None
        self.coefk = coefk

        self._npdt = None
        self.npdt = npdt

    @property
    def coefk(self):
        """Return grandeur."""
        return self._coefk

    @coefk.setter
    def coefk(self, coefk):
        """Set coefk."""
        try:
            coefk = float(coefk)
        except Exception:
            raise TypeError('Coefficient k must a a numeric')
        if coefk <= 0 or coefk >= 1:
                raise ValueError('Coefficient k must be in ]0;1[')
        self._coefk = coefk

    @property
    def npdt(self):
        """Return grandeur."""
        return self._npdt

    @npdt.setter
    def npdt(self, npdt):
        """Set coefk."""
        if npdt is None:
            self._npdt = npdt
            return
        try:
            npdt = int(npdt)
        except Exception:
            raise TypeError('Number of pdt must be an integer or None')
        if npdt < 0:
            raise ValueError('Number of pdt must be positive')
        self._npdt = npdt

    def __unicode__(self):
        """Return unicode representation."""
        npdt = 'inconnu'
        if self.npdt is not None:
            npdt = self.npdt
        return '''Indice de precipitations antérieures ''' \
               '''de coefficient k {0} ''' \
               '''Nombre de pas de temps: {1}'''.format(
                   self.coefk, npdt)

    __str__ = _composant.__str__


class SitemeteoPondere(object):
    """Classe SiteMeteoPondere

    Classe permettant de manipuler des sites météo pondérés
    Proprietes:
        sitemeteo (Sitemeteo): Site météo
        pondération (float): Pondération du site
    """
    def __init__(self, sitemeteo, ponderation):
        self._sitemeteo = None
        self.sitemeteo = sitemeteo
        self._ponderation = None
        self.ponderation = ponderation

    # -- property entite --
    @property
    def sitemeteo(self):
        """Return entite hydro."""
        return self._sitemeteo

    @sitemeteo.setter
    def sitemeteo(self, sitemeteo):
        """Set entite."""
        try:
            # sitemeteo must be a Sitemeteo
            if not isinstance(sitemeteo, _sitemeteo.Sitemeteo):
                raise TypeError('sitemeteo must be a Sitemeteo')

            self._sitemeteo = sitemeteo

        except Exception:
            raise

    # -- property ponderation --
    @property
    def ponderation(self):
        """Return ponderation."""
        return self._ponderation

    @ponderation.setter
    def ponderation(self, ponderation):
        """Set ponderation."""
        try:
            self._ponderation = float(ponderation)
        except Exception:
            raise TypeError('ponderation must be a numeric')

    def __unicode__(self):
        return "Site météo {0} avec pondération {1}".format(
            self.sitemeteo.code, self.ponderation)

    __str__ = _composant.__str__


# -- class SerieObsElab -------------------------------------------------------
class SerieObsElabMeteo(object):
    """Classe SerieObsElabMeteo

    Classe permettant de manipuler des séries d'observations élaborées météo
    Proprietes:
        site (SitemeteoPondere or Sitehydro): Site météo pondéré ou site hydro
        grandeur (float):grandeur de la série
        typeserie: type de série (nomenclature 876 )
        dtprod: date de production
        dtdeb date de début de le série
        dtfin: date de fin de la série
        duree (int or None)
        ipas (iterable of Ipa: Indices de précipitations antérieures
        observations (): observations élaborées
    """
    dtprod = _composant.Datefromeverything(required=False)
    dtdeb = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)
    grandeur = _composant.Nomenclatureitem(nomenclature=523)
    typeserie = _composant.Nomenclatureitem(nomenclature=876)

    def __init__(self, site=None, grandeur=None, typeserie=None, dtprod=None,
                 dtdeb=None, dtfin=None, duree=None, ipas=None,
                 observations=None, strict=True):
        """Constructeur"""
        self.grandeur = grandeur
        self.typeserie = typeserie
        self.dtprod = dtprod
        self.dtdeb = dtdeb
        self.dtfin = dtfin

        self._strict = bool(strict)

        self._site = None
        self.site = site
        self._duree = None
        self.duree = duree

        self._ipas = None
        self.ipas = ipas

        self._observations = None
        self.observations = observations

    # -- property site --
    @property
    def site(self):
        """Return site."""
        return self._site

    @site.setter
    def site(self, site):
        """Set site."""
        try:
            if self._strict and \
                    not isinstance(site, (_sitehydro.Sitehydro,
                                          SitemeteoPondere)):
                raise
            self._site = site
        except:
            raise TypeError(
                    'site must be a Site Hydro or SiteMeteoPondere')

    # -- property duree --
    @property
    def duree(self):
        """Return duree."""
        return self._duree

    @duree.setter
    def duree(self, duree):
        """Set duree."""
        if duree is None:
            self._duree = duree
            return
        try:
            if not isinstance(duree, _datetime.timedelta):
                duree = int(duree)
                if duree < 0:
                    raise ValueError(
                        'duree must be a timedelta or a positive integer')
                duree = _datetime.timedelta(minutes=duree)
        except:
            raise
        self._duree = duree

    # -- property ipas --
    @property
    def ipas(self):
        """Return observations."""
        return self._ipas

    @ipas.setter
    def ipas(self, ipas):
        """Set ipas."""
        if ipas is None:
            self._ipas = ipas
            return
        try:
            if self._strict:
                for ipa in ipas:
                    if not isinstance(ipa, Ipa):
                        raise TypeError('ipas is not an iterable of Ipa')

            self._ipas = ipas
        except Exception:
            raise TypeError('ipas incorrect')

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

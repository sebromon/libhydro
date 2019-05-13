# -*- coding: utf-8 -*-
"""Module gradienthydro.

Ce module contient les classes:
    # Gradienthydro
    # Gradientshydro

"""

# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import numpy as _numpy
import pandas as _pandas
from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from libhydro.core import (sitehydro as _sitehydro, _composant,
                           intervenant as _intervenant)


class Gradient(_numpy.ndarray):
    """Classe Gradient

    Classe pour manipuler un gradient hydrometrique.

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
        (str('statut'), _numpy.int8)])

    def __new__(cls, dte=None, res=0.0, mth=0, qal=16, statut=0):
        if not isinstance(dte, _numpy.datetime64):
            dte = _numpy.datetime64(dte, 's')
        if qal not in _NOMENCLATURE[515]:
            raise ValueError('incorrect qualification')
        if mth not in _NOMENCLATURE[512]:
            raise ValueError('incorrect method')
        if statut not in _NOMENCLATURE[510]:
            raise ValueError('incorrect statut')

        obj = _numpy.array(
            (dte, res, mth, qal, statut),
            dtype=Gradient.DTYPE
        ).view(cls)
        return obj

    def __unicode__(self):
        """Return unicode representation."""
        return '''{0} le {4} a {5} UTC de statut {1} ''' \
               '''(valeur obtenue par {2}, {3})'''.format(
                   self['res'].item(),
                   _NOMENCLATURE[510][self['statut'].item()].lower(),
                   _NOMENCLATURE[512][self['mth'].item()].lower(),
                   _NOMENCLATURE[515][self['qal'].item()].lower(),
                   *self['dte'].item().isoformat().split('T')
               )

    __str__ = _composant.__str__


class Gradients(object):
    """Classe Gradients.

    Classe pour manipuler une collection de gradients
    hydrometriques, sous la forme d'un pandas.DataFrame
    (les objets instancies sont des DataFrame).

    L'index est un pandas.DatetimeIndex   les dates d'observation.

    Les donnees sont contenues dans 4 colonnes du DataFrame
    (voir Gradienthydro).

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

    def __new__(cls, *gradients):
        """Constructeur.

        Arguments:
            observations (un nombre quelconque d'Observation)

        Exemples:
            obs = Observations(obs1)  # une seule Observation
            obs = Observations(obs1, obs2, ..., obsn)  # n Observation
            obs = Observations(*observations)  #  une liste d'Observation

        """
        if gradients is None:
            return

        # other cases
        # prepare a list of observations
        obss = []
        try:
            for i, gradient in enumerate(gradients):
                if not isinstance(gradient, Gradient):
                    raise TypeError(
                        'element {} is not a {}'.format(
                            i, Gradient
                        )
                    )
                # obss.append(obs)
                obss.append(gradient.tolist())

        except Exception:
            raise

        # prepare a tmp numpy.array
        # array = _numpy.array(object=obss)
        array = _numpy.array(object=obss, dtype=Gradient.DTYPE)

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
    def concat(gradients, others):
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
            return _pandas.concat([gradients, others])

        except Exception:
            return _pandas.concat([gradients,
                                   Gradients(others)])


# -- class SerieGradients ------------------------------------------------
class SerieGradients(object):

    """Classe Serie de gradients hydro.

    Classe pour manipuler des séries de gradients hydrometriques.

    Proprietes:
        entite (Sitehydro or Station or Capteur):
            Site ou station ou capteur hydro
        grd (char parmi nomenclature[509]): H ou Q
        duree (int): durée en minutes
        gradients (Gradients): gradients hydro
        contact (intervenant.Contact ou None)
        dtprod (datetime.datetime): Date de production
    """

    grd = _composant.Nomenclatureitem(nomenclature=509)
    dtprod = _composant.Datefromeverything(required=True)

    def __init__(self, entite=None, grd=None, duree=None, gradients=None,
                 contact=None, dtprod=None):

        """Initialisation.

        Arguments:
            entite (Sitehydro or Station or Capteur):
                Site ou station ou capteur hydro
            grd (char parmi nomenclature[509]): H ou Q
            duree (int): durée en minutes
            gradients (Gradients): gradients hydro
            contact (intervenant.Contact ou None)
            dtprod (datetime.datetime): Date de production
        """
        # -- descriptors --
        self.grd = grd
        self.dtprod = dtprod

        # -- full properties --
        self._duree = None
        self.duree = duree
        self._gradients = None
        self.gradients = gradients
        self._entite = None
        self.entite = entite
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
            # entite must be a site or a station
            if not isinstance(
                    entite, (_sitehydro.Sitehydro, _sitehydro.Station,
                             _sitehydro.Capteur)):
                raise TypeError('entite must be a Sitehydro or a Station'
                                ' or a Capteur')

            self._entite = entite

        except Exception:
            raise

    # -- property duree --
    @property
    def duree(self):
        """Return pdt."""
        return self._duree

    @duree.setter
    def duree(self, duree):
        """Set duree."""
        if duree is None:
            raise TypeError('duree is not defined')
        duree = int(duree)
        if duree <= 0:
            raise ValueError('duree must be > 0')
        self._duree = duree

    # -- property gradients --
    @property
    def gradients(self):
        """Return gradients."""
        return self._gradients

    @gradients.setter
    def gradients(self, gradients):
        """Set gradients."""
        try:

            if gradients is not None:
                # we check we have a res column...
                if not hasattr(gradients, 'res'):
                    raise TypeError()
                # ... and that index contains datetimes
                # FIXME - should fail with datetime64 object.
                #         Use .item().isoformat()
                # if not hasattr(gradients.index[0], 'isoformat'):
                #     raise TypeError()
            self._gradients = gradients

        except Exception:
            raise TypeError('gradients incorrect')

    @property
    def contact(self):
        """Return contact"""
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Set contact."""
        if contact is not None and \
                not isinstance(contact, _intervenant.Contact):
            raise TypeError('contact must be an instance of Contact')
        self._contact = contact

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        try:
            gradients = self.gradients.to_string(
                max_rows=15, show_dimensions=True
            )
        except Exception:
            gradients = '<sans gradients>'

        # action !
        return 'Série de gradients {0} de durée {1}\n'\
               '{2}\n'\
               'Gradients:\n{3}'.format(
                   self.grd,
                   self.duree,
                   '-' * 72,
                   gradients
               )

    __str__ = _composant.__str__

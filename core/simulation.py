# -*- coding: utf-8 -*-
"""Module simulation.

Ce module contient les classes:
    # Simulation
    # Previsions
    # Prevision

La Simulation est le conteneur de reference pour les previsions hydrometriques.
Les previsions y sont contenues dans l'attribut du meme nom, sous la forme
d'une pandas.Series a double index, un timestamp et une probabilite.

"""

# On peux aussi utiliser directement les classes de la librairie Pandas, les
# Series ou les DataFrame.
#
# Exemple pour instancier une Series:
#     datas = pandas.Series(
#         data = [100, 110, 120],
#         index = [
#             numpy.datetime64('2012-05 01:00', 's'),
#             numpy.datetime64('2012-05 02:00', 's'),
#             numpy.datetime64('2012-05 03:00', 's')
#         ]
#         dtype = None,
#         name='previsions de debit'
# )
#
# Exemple pour instancier un DataFrame:
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
from . import (sitehydro as _sitehydro, modeleprevision as _modeleprevision)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1g"""
__date__ = """2013-09-03"""

#HISTORY
#V0.1 - 2013-08-07
#    first shot


#-- todos ---------------------------------------------------------------------
# FIXME - integrity checks entite / grandeur
# ADMIT_SIMULATION = {
#     Sitehydro: {'H': False, 'Q': True},
#     Stationhydro: {'H': True, 'Q': False},
#     Capteur: {'H': False, 'Q':False}
# }
# def _admit_simulation(self, grandeur):
#      return ADMIT_SIMULATION[self.__class][grandeur]

# TODO - add a sort argument/method ?


#-- class Prevision -----------------------------------------------------------
class Prevision(_numpy.ndarray):
    """Classe prevision.

    Classe pour manipuler une prevision elementaire.

    Subclasse de numpy.array('dte', 'res', 'prb'), les elements etant du
    type DTYPE.

    Date et resultat sont obligatoires, la probabilite vaut 50 par defaut.

    L'implementation differe de celle du modele de donnees car on utilise une
    seule classe pour les previsions deterministes (min ,moy et max) et les
    previsions probabilistes (probabilite + valeur) en applicant la regle:
        # la valeur min est celle de probabilite 0
        # la valeur moyenne est celle de probabilite 50
        # la valeur maximum est celle de probabilite 100

    Proprietes:
        dte (numpy.datetime64 ou string) = date UTC de la prevision au format
            ISO 8601, arrondie a la seconde. A l'initialisation si le fuseau
            horaire n'est pas precise, la date est consideree en heure locale.
            Pour forcer la sasie d'une date UTC utiliser le fuseau +00:
                np.datetime64('2000-01-01T09:28:00+00')
        res (numpy.float) = resultat
        prb (numpy.int entre 0 et 100, defaut 50) = probabilite du resultat

    """

    DTYPE = _numpy.dtype([
        (str('dte'), _numpy.datetime64(None, str('s'))),
        (str('res'), _numpy.float),
        (str('prb'), _numpy.int8)
    ])

    def __new__(cls, dte, res, prb=50):
        if not isinstance(dte, _numpy.datetime64):
            dte = _numpy.datetime64(dte, 's')
        try:
            prb = int(prb)
            if (prb < 0) or (prb > 100):
                raise ValueError('probabilite incorrecte')
        except Exception:
            raise
        obj = _numpy.array(
            (dte, res, prb),
            dtype=Prevision.DTYPE
        ).view(cls)
        return obj

    # def __array_finalize__(self, obj):
    #     if obj is None:
    #         return

    def __unicode__(self):
        """Unicode representation."""
        return '{0} avec une probabilite de {1}% pour le {2} a {3} UTC'.format(
            self['res'].item(),
            self['prb'].item(),
            *self['dte'].item().isoformat().split('T')
        )

    def __str__(self):
        """String representation."""
        if _sys.version_info[0] >= 3:  # Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode('utf8')


#-- class Previsions ----------------------------------------------------------
class Previsions(_pandas.Series):
    """Classe Previsions.

    Classe pour manipuler un jeux de previsions, sous la forme d'une Series
    pandas avec un double index, le premier etant la date du resultat, le second
    sa probabilite.

    Illustration d'une Series pandas de previsions pour 3 dates et avec 2 jeux
    de probabilite:
        dte                  prb
        1972-10-01 10:00:00  50     33
                             40     44
        1972-10-01 11:00:00  50     35
                             40     45
        1972-10-01 12:00:00  50     55
                             40     60
        Name: res, dtype: float64

    Se reporter a la documentation de la classe Prevision pour l'utilisation du
    parametre prb.

    Pour filtrer la serie de resultats de meme probabilite, par exemple 50%,
    entre 2 dates:
        previsions[:,50]['2013-01':'2013-01-23 01:00']
    ou à une date précise:
        previsions['2013-01-23 01:00'][50]

    On peux slicer une série mais il faut que l'index soit ordonné par la
    colonne utilisée:
        # trier par la date
        ordered_prev = previsions.sortlevel(0)
        # slicer
        ordered_prev['2013-01-23 00:00':'2013-01-23- 10:00']
        # sinon...
        ordered_prev = previsions.sortlevel(1)
        ordered_prev['2013-01-23 00:00':'2013-01-23- 10:00']
        >> KeyError: 'MultiIndex lexsort depth 0, key was length 1'

    Pour agréger 2 séries de prévisions:
        previsions.append(other_previsions)

    """

    def __new__(cls, *previsions):
        """Initialisation+

        Arguments:
            previsions (un nombre quelconque de Prevision)

        Exemples:
            prv = Previsions(prv1)  # une seule Prevision
            prv = Previsions(prv1, prv2, ..., prvn)  # n Prevision
            prv = Previsions(*previsions)  #  une liste de Prevision

        """

        # prepare a list of previsions
        prvs = []
        try:
            for prv in previsions:
                if not isinstance(prv, Prevision):
                    raise TypeError('{} in not a Prevision'.format(prv))
                prvs.append(prv)

        except Exception:
            raise

        # prepare a tmp numpy.array
        array = _numpy.array(object=prvs)

        # make index
        index = _pandas.MultiIndex.from_tuples(
            zip(array['dte'], array['prb']),
            names=['dte', 'prb']
        )

        # get the pandas.Series
        obj = _pandas.Series(
            data=array['res'],
            index=index,
            name='res'
        )

        # return
        # TODO - can't subclass the DataFRame object
        # return obj.view(cls)
        return obj


#-- class Simulation ----------------------------------------------------------
class Simulation(object):
    """Classe simulation.

    classe pour manipuler les simulations hydrauliques ou hydrologiques.

    Proprietes:
        entite (Sitehydro, Stationhydro)
        modeleprevision (Modeleprevision)
        grandeur (char in NOMENCLATURE[509]) = H ou Q
        statut (int in NOMENCLATURE[516]) = brute ou critiquee
        qualite (0 < int < 100) = indice de qualite
        public (bool, defaut False) = si True publication libre
        commentaire (texte)
        dtprod (datetime.datetime) = date de production
        previsions (Previsions)

    """

    # TODO - Simulation others attributes

    # sysalti
    # responsable
    # refalti
    # courbetarage

    def __init__(
        self, entite=None, modeleprevision=None, grandeur=None, statut=4,
        qualite=None, public=False, commentaire=None, dtprod=None,
        previsions=None, strict=True
    ):
        """Initialisation.

        Arguments:
            entite (Sitehydro ou Stationhydro)
            modeleprevision (Modeleprevision)
            grandeur (char in NOMENCLATURE[509]) = H ou Q
            statut (int in NOMENCLATURE[516], defaut 4) = brute ou critiquee
            qualite (0 < int < 100) = indice de qualite
            public (bool, defaut False) = si True publication libre
            commentaire (texte)
            dtprod (string ou datetime.datetime) = date de production
            previsions (Previsions)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite des parametres

        """

        # -- simple properties --
        self.public = bool(public)
        self.commentaire = unicode(commentaire) if commentaire else None
        self._strict = strict

        # -- full properties --
        self.entite = entite
        self.modeleprevision = modeleprevision
        self.grandeur = grandeur
        self.statut = statut
        self.qualite = qualite
        self.dtprod = dtprod
        self.previsions = previsions

    # -- property entite --
    @property
    def entite(self):
        """Entite hydro."""
        return self._entite

    @entite.setter
    def entite(self, entite):
        try:
            if (self._strict) and (entite is not None):

                # entite must be a site or a station
                if not isinstance(
                    entite,
                    (_sitehydro.Sitehydro, _sitehydro.Stationhydro)
                ):
                    raise TypeError(
                        'entite must be a Sitehydro or a Stationhydro'
                    )

                # Q prevs on Sitehydro only, H prevs on Stationhydro

                # FIXME - integrity checks
                try:

                    if (self.grandeur is not None):
                        if (self.grandeur == 'Q') and \
                                not isinstance(entite, _sitehydro.Sitehydro):
                            raise TypeError(
                                'Q previsions, entite must be a Sitehydro'
                            )
                        if (self.grandeur == 'H') and \
                                not isinstance(entite, _sitehydro.Stationhydro):
                            raise TypeError(
                                'H previsions, entite must be a Stationhydro'
                            )

                except AttributeError:
                    pass

            # all is well
            self._entite = entite

        except Exception:
            raise

    # -- property modeleprevision --
    @property
    def modeleprevision(self):
        """Modele de prevision."""
        return self._modeleprevision

    @modeleprevision.setter
    def modeleprevision(self, modeleprevision):
        try:
            if (self._strict) and (modeleprevision is not None):
                if not isinstance(
                    modeleprevision,
                    _modeleprevision.Modeleprevision
                ):
                    raise TypeError('modeleprevision must be a Modeleprevision')
            self._modeleprevision = modeleprevision

        except:
            raise

    # -- property grandeur --
    @property
    def grandeur(self):
        """Grandeur."""
        return self._grandeur

    @grandeur.setter
    def grandeur(self, grandeur):
        try:
            if (grandeur is not None):
                grandeur = unicode(grandeur)
                if (self._strict) and (grandeur not in _NOMENCLATURE[509]):
                    raise ValueError('grandeur incorrect')
            self._grandeur = grandeur

        except:
            raise

    # -- property statut --
    @property
    def statut(self):
        """Statut."""
        return self._statut

    @statut.setter
    def statut(self, statut):
        try:
            # None case
            if statut is None:
                raise TypeError('statut is required')
            # other cases
            statut = int(statut)
            if (self._strict) and (statut not in _NOMENCLATURE[516]):
                raise ValueError('statut incorrect')
            # all is well
            self._statut = statut

        except:
            raise

    # -- property qualite --
    @property
    def qualite(self):
        """Indice de qualite."""
        return self._qualite

    @qualite.setter
    def qualite(self, qualite):
        try:
            if qualite is not None:
                qualite = int(qualite)
                if (qualite < 0) or (qualite > 100):
                    raise ValueError('qualite is not in 0-100 range')
            self._qualite = qualite

        except:
            raise

    # -- property dtprod --
    @property
    def dtprod(self):
        """Date de production."""
        return self._dtprod

    @dtprod.setter
    def dtprod(self, dtprod):
        try:
            if dtprod is not None:
                if not isinstance(dtprod, _numpy.datetime64):
                    try:
                        dtprod = _numpy.datetime64(dtprod, 's')
                    except Exception:
                        try:
                            dtprod = _numpy.datetime64(dtprod.isoformat(), 's')
                        except Exception:
                            raise TypeError('dtprod must be a date')
            self._dtprod = dtprod

        except:
            raise

    # -- property previsions --
    @property
    def previsions(self):
        """Previsions."""
        return self._previsions

    @previsions.setter
    def previsions(self, previsions):
        try:
            if previsions is not None:
                # we check we have a Series...
                # ... and that index contains datetimes
                if (self._strict):
                    if (
                        (not isinstance(previsions, _pandas.Series)) or
                        (previsions.index.names != ['dte', 'prb'])
                    ):

                        raise TypeError('previsions incorrect')
                    previsions.index[0][0].isoformat()
            # all seeem's ok :-)
            self._previsions = previsions
        except:
            raise

    # -- other methods --
    def __unicode__(self):
        """Unicode representation."""
        # compute entite name
        if self.entite is None:
            entite = '<une entite inconnue>'
        else:
            try:
                entite = '{} {}'.format(
                    _sitehydro.ARTICLE[self.entite.__class__],
                    self.entite.__unicode__()
                )
            except Exception:
                entite = self.entite

        # prepare previsions
        if self.previsions is None:
            prev = '<sans previsions>'
        else:
            prev = self.previsions.__unicode__()

        # action !
        return  'Simulation {0} de {1} sur {2}\n'\
                'Date de production: {3} - Qualite {4}\n'\
                'Commentaire: {5}\n'\
                '{6}\n'\
                '{7}\n'\
                '{8}\n'\
                'Previsions:\n {9}'.format(
                    '<sans statut>' if (self.statut is None)
                    else _NOMENCLATURE[516][self.statut].lower(),
                    self.grandeur or '<sans grandeur>',
                    entite,
                    '<inconnue>' if not self.dtprod
                    else self.dtprod.item().isoformat(),
                    '<inconnue>' if not self.qualite else '%i%%' % self.qualite,
                    self.commentaire or '<sans>',
                    '-' * 72,
                    self.modeleprevision or '<modele inconnu>',
                    '-' * 72,
                    prev
                )

    def __str__(self):
        """String representation."""
        if _sys.version_info[0] >= 3:  # Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode('utf8')

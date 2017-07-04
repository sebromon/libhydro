# coding: utf-8
"""Module simulation.

Ce module contient les classes:
    # Simulation
    # Previsions
    # Prevision

La Simulation est le conteneur de reference pour les previsions hydrometriques.
Les previsions y sont contenues dans l'attribut du meme nom, sous la forme
d'une pandas.Series a double index, un timestamp et une probabilite.

"""

# On peut aussi utiliser directement les classes de la librairie Pandas, les
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

# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import numpy as _numpy
import pandas as _pandas

from . import _composant
from . import sitehydro as _sitehydro, modeleprevision as _modeleprevision
from .nomenclature import NOMENCLATURE as _NOMENCLATURE


# -- strings ------------------------------------------------------------------
__version__ = '0.8.0'
__date__ = '2017-05-24'

# HISTORY
# V0.8 - 2017-05-17
#  séparation des prévisions de tendance des previsions probabilistes
# V0.7 - 2014-03-02
#   use descriptors
# V0.1 - 2013-08-07
#   first shot

# -- todos --------------------------------------------------------------------
# PROGRESS - Prevision 100% - Previsions 90% - Simulation 80%
# FIXME - integrity checks entite / grandeur
#     grandeur is a descriptor, it needs a callback
#     ADMIT_SIMULATION = {
#         Sitehydro: {'H': False, 'Q': True},
#         Station: {'H': True, 'Q': False},
#         Capteur: {'H': False, 'Q':False}
#     }
# def _admit_simulation(self, grandeur):
#      # be careful with  self._class_ and inheritance
#      return ADMIT_SIMULATION[self.__class][grandeur]

# TODO - add a sort argument/method ?


# -- class PrevisionPrb -------------------------------------------------------
class PrevisionPrb(_numpy.ndarray):

    """Classe PrevisionPrb.

    Classe pour manipuler une prevision probabiliste.

    Subclasse de numpy.array('dte', 'res', 'prb'), les elements etant du
    type DTYPE.

    Date et resultat sont obligatoires, la probabilite vaut 50 par defaut.

    Proprietes:
        dte (numpy.datetime64) = date UTC de la prevision au format
            ISO 8601, arrondie a la seconde. A l'initialisation par une string,
            si le fuseau horaire n'est pas precise, la date est consideree en
            heure locale. Pour forcer la sasie d'une date UTC utiliser
            le fuseau +00:
                numpy.datetime64('2000-01-01T09:28:00+00')
        res (numpy.float) = resultat
        prb (numpy.int entre 0 et 100, defaut 50) = probabilite du resultat

    """

    DTYPE = _numpy.dtype([
        (str('dte'), _numpy.datetime64(None, str('s'))),
        (str('res'), _numpy.float), (str('prb'), _numpy.int8)])

    def __new__(cls, dte, res, prb=50):
        if not isinstance(dte, _numpy.datetime64):
            dte = _numpy.datetime64(dte, 's')
        try:
            prb = int(prb)
            if (prb < 0) or (prb > 100):
                raise ValueError('probabilite incorrect')
        except Exception:
            raise
        obj = _numpy.array((dte, res, prb), dtype=PrevisionPrb.DTYPE).view(cls)
        return obj

    def __unicode__(self):
        """Return unicode representation."""
        return '{0} avec une probabilite de {1}% pour le {2} a {3} UTC'.format(
            self['res'].item(), self['prb'].item(),
            *self['dte'].item().isoformat().split('T'))

    __str__ = _composant.__str__


# -- class PrevisionTendance --------------------------------------------------
class PrevisionTendance(_numpy.ndarray):

    """Classe PrevisionTendance.

    Classe pour manipuler une prevision de tendance elementaire.

    Subclasse de numpy.array('dte', 'res', 'tend'), les elements etant du
    type DTYPE.

    Date et resultat sont obligatoires. La tendance peut prendre la valeur
    'min', 'moy' (valeur par defaut) ou 'max'

    Proprietes:
        dte (numpy.datetime64) = date UTC de la prevision au format
            ISO 8601, arrondie a la seconde. A l'initialisation par une string,
            si le fuseau horaire n'est pas precise, la date est consideree en
            heure locale. Pour forcer la sasie d'une date UTC utiliser
            le fuseau +00:
                numpy.datetime64('2000-01-01T09:28:00+00')
        res (numpy.float) = resultat
        tend (numpy.unicode 3 caractères parmi 'min', 'moy' ou 'max') =
            tendance de la prevision

    """

    DTYPE = _numpy.dtype([
        (str('dte'), _numpy.datetime64(None, str('s'))),
        (str('res'), _numpy.float), (str('tend'), _numpy.unicode_, 3)])

    def __new__(cls, dte, res, tend='moy'):
        if not isinstance(dte, _numpy.datetime64):
            dte = _numpy.datetime64(dte, 's')
        try:
            tend = str(tend)
            if tend not in ('min','max','moy'):
                raise ValueError('tendance incorrect {}'.format(tend))
        except Exception:
            raise
        obj = _numpy.array(
            (dte, res, tend), dtype=PrevisionTendance.DTYPE).view(cls)
        return obj

    def __unicode__(self):
        """Return unicode representation."""
        return '{0} de tendance {1} pour le {2} a {3} UTC'.format(
            self['res'].item(), self['tend'].item(),
            *self['dte'].item().isoformat().split('T'))

    __str__ = _composant.__str__


# -- class PrevisionsPrb ------------------------------------------------------
class PrevisionsPrb(_pandas.Series):

    """Classe PrevisionsPrb.

    Classe pour manipuler un jeux de previsions, sous la forme d'une Series
    pandas avec un double index, le premier etant la date du resultat, le
    second sa probabilite.

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

    Se reporter a la documentation de la classe PrevisionPrb pour l'utilisation
    du parametre prb.

    Pour filtrer la serie de resultats de meme probabilite, par exemple 50%,
    entre 2 dates:
        previsions[:,50]['2013-01':'2013-01-23 01:00']
    ou a une date precise:
        previsions['2013-01-23 01:00'][50]

    On peut slicer une serie mais il faut que l'index soit ordonne par la
    colonne utilisee:
        # trier par la date
        ordered_prev = previsions.sortlevel(0)
        # slicer
        ordered_prev['2013-01-23 00:00':'2013-01-23 10:00']
        # si l'index n'est pas correctement trie on leve une exception...
        ordered_prev = previsions.sortlevel(1)
        ordered_prev['2013-01-23 00:00':'2013-01-23- 10:00']
        >> KeyError: 'MultiIndex lexsort depth 0, key was length 1'

    Pour agreger 2 series de previsions:
        previsions.append(other_previsions)

    """

    def __new__(cls, *previsions):
        """Constructeur.

        Arguments:
            previsions (un nombre quelconque de PrevisionPrb)

        Exemples:
            prv = Previsions(prv1)  # une seule Prevision
            prv = Previsions(prv1, prv2, ..., prvn)  # n Prevision
            prv = Previsions(*previsions)  #  une liste de Prevision

        """

        # prepare a list of previsions
        prvs = []
        try:
            for prv in previsions:
                if not isinstance(prv, PrevisionPrb):
                    raise TypeError(
                        '{} is not a probabilist Prevision'.format(prv))
                # python 3 avois error provide tuple instead array
                # dtype is specified after
                #prvs.append(prv)
                prvs.append(prv.tolist())

        except Exception:
            raise

        # prepare a tmp numpy.array
        # python 3 error: ValueError: cannot include dtype 'M' in a buffer
        # to avoid this error provide tuple instead of _numpy.array
        # and dtype
        #array = _numpy.array(object=prvs)
        array = _numpy.array(object=prvs, dtype=PrevisionPrb.DTYPE)

        # make index
        index = _pandas.MultiIndex.from_tuples(
            list(zip(array['dte'], array['prb'])), names=['dte', 'prb'])

        # get the pandas.Series
        obj = _pandas.Series(data=array['res'], index=index, name='res')

        # return
        # TODO - we can't subclass the DataFrame object
        # return obj.view(cls)
        return obj


# -- class PrevisionsTendance -------------------------------------------------
class PrevisionsTendance(_pandas.Series):

    """Classe PrevisionsTendance.

    Classe pour manipuler un jeux de previsions de tendande, sous la forme
    d'une Series pandas avec un double index, le premier etant la date du
    resultat, le second la tendance ('moy', 'min' ou 'max').

    Illustration d'une Series pandas de previsions pour 3 dates et avec 2 jeux
    de probabilite:
        dte                  tend
        1972-10-01 10:00:00  moy     33
                             max     44
        1972-10-01 11:00:00  min     35
                             moy     45
                             max     55
        1972-10-01 12:00:00  min     55
                             moy     60
        Name: res, dtype: float64

    Se reporter a la documentation de la classe PrevisionTendance pour
    l'utilisation du parametre tend.

    Pour filtrer la serie de resultats de meme tendance, par exemple 'moy',
    entre 2 dates:
        previsions[:,'moy']['2013-01':'2013-01-23 01:00']
    ou a une date precise:
        previsions['2013-01-23 01:00']['moy']

    On peut slicer une serie mais il faut que l'index soit ordonne par la
    colonne utilisee:
        # trier par la date
        ordered_prev = previsions.sortlevel(0)
        # slicer
        ordered_prev['2013-01-23 00:00':'2013-01-23 10:00']
        # si l'index n'est pas correctement trie on leve une exception...
        ordered_prev = previsions.sortlevel(1)
        ordered_prev['2013-01-23 00:00':'2013-01-23- 10:00']
        >> KeyError: 'MultiIndex lexsort depth 0, key was length 1'

    Pour agreger 2 series de previsions:
        previsions.append(other_previsions)

    """

    def __new__(cls, *previsions):
        """Constructeur.

        Arguments:
            previsions (un nombre quelconque de PrevisionTendance)

        Exemples:
            prv = Previsions(prv1)  # une seule Prevision
            prv = Previsions(prv1, prv2, ..., prvn)  # n PrevisionTendance
            prv = Previsions(*previsions)  #  une liste de PrevisionTendance

        """

        # prepare a list of previsions
        prvs = []
        try:
            for prv in previsions:
                if not isinstance(prv, PrevisionTendance):
                    raise TypeError(
                        '{} is not a tendency Prevision'.format(prv))
                # python 3 avois error provide tuple instead array
                # dtype is specified after
                #prvs.append(prv)
                prvs.append(prv.tolist())

        except Exception:
            raise

        # prepare a tmp numpy.array
        # python 3 error: ValueError: cannot include dtype 'M' in a buffer
        # to avoid this error provide tuple instead of _numpy.array
        # and dtype
        #array = _numpy.array(object=prvs)
        array = _numpy.array(object=prvs, dtype=PrevisionTendance.DTYPE)
        # make index
        index = _pandas.MultiIndex.from_tuples(
            list(zip(array['dte'], array['tend'])), names=['dte', 'tend'])

        # get the pandas.Series
        obj = _pandas.Series(data=array['res'], index=index, name='res')

        # return
        # TODO - can't subclass the DataFRame object
        # return obj.view(cls)
        return obj


# -- class Simulation ---------------------------------------------------------
class Simulation(object):

    """Classe simulation.

    classe pour manipuler les simulations hydrauliques ou hydrologiques.

    Proprietes:
        entite (Sitehydro, Station)
        modeleprevision (Modeleprevision)
        grandeur (char in NOMENCLATURE[509]) = H ou Q
        statut (int in NOMENCLATURE[516]) = brute ou critiquee
        qualite (0 < int < 100) = indice de qualite
        public (bool, defaut False) = si True publication libre
        commentaire (texte)
        dtprod (datetime.datetime) = date de production
        previsions (Previsions)
        previsions_tend (PrevisionsTendance)
        previsions_prb (PrevisionsPrb)
        intervenant (Intervenant)

    """

    # FIXME - add a callback to grandeur to check inconsistency with entite
    grandeur = _composant.Nomenclatureitem(nomenclature=509, required=False)
    statut = _composant.Nomenclatureitem(nomenclature=516)
    dtprod = _composant.Datefromeverything(required=False)

    # Simulation others attributes

    # sysalti
    # refalti
    # courbetarage

    def __init__(self, entite=None, modeleprevision=None, grandeur=None,
                 statut=4, qualite=None, public=False, commentaire=None,
                 dtprod=None, previsions_tend=None, previsions_prb=None,
                 intervenant=None, strict=True):
        """Initialisation.

        Arguments:
            entite (Sitehydro ou Station)
            modeleprevision (Modeleprevision)
            grandeur (char in NOMENCLATURE[509]) = H ou Q
            statut (int in NOMENCLATURE[516], defaut 4) = brute ou critiquee
            qualite (0 < int < 100) = indice de qualite
            public (bool, defaut False) = si True publication libre
            commentaire (texte)
            dtprod (numpy.datetime64 string, datetime.datetime...) =
                date de production
            previsions_tend (PrevisionsTendance)
            previsions_prb (PrevisionsPrb)
            intervenant (Intervenant)
            strict (bool, defaut True) = en mode permissif il n'y a pas de
                controles de validite des parametres

        """

        # -- simple properties --
        self._strict = bool(strict)
        self.public = bool(public)
        self.commentaire = str(commentaire) if commentaire else None
        self.intervenant = intervenant

        # -- adjust the descriptors --
        vars(Simulation)['grandeur'].strict = self._strict
        vars(Simulation)['statut'].strict = self._strict

        # -- descriptors --
        self.grandeur = grandeur
        self.statut = statut
        self.dtprod = dtprod

        # -- full properties --
        self._entite = self._modeleprevision = \
            self._qualite = self._previsions_tend = \
            self._previsions_prb = None
        self.entite = entite
        self.modeleprevision = modeleprevision
        self.qualite = qualite
        self.previsions_tend = previsions_tend
        self.previsions_prb = previsions_prb

    # -- property entite --
    @property
    def entite(self):
        """Return entite hydro."""
        return self._entite

    @entite.setter
    def entite(self, entite):
        """Set entite hydro."""
        try:
            if self._strict and (entite is not None):

                # entite must be a site or a station
                if not isinstance(
                        entite, (_sitehydro.Sitehydro, _sitehydro.Station)):
                    raise TypeError('entite must be a Sitehydro or a Station')

                # Q prevs on Sitehydro only, H prevs on Station
                if (self.grandeur is not None):
                    if (self.grandeur == 'Q') and \
                            not isinstance(entite, _sitehydro.Sitehydro):
                        raise TypeError(
                            'Q previsions, entite must be a Sitehydro')
                    if self.grandeur == 'H' and \
                            not isinstance(entite, _sitehydro.Station):
                        raise TypeError(
                            'H previsions, entite must be a Station')

            # all is well
            self._entite = entite

        except Exception:
            raise

    # -- property modeleprevision --
    @property
    def modeleprevision(self):
        """Return modele de prevision."""
        return self._modeleprevision

    @modeleprevision.setter
    def modeleprevision(self, modeleprevision):
        """Set modele de prevision."""
        try:
            if self._strict and (modeleprevision is not None):
                if not isinstance(
                        modeleprevision, _modeleprevision.Modeleprevision):
                    raise TypeError(
                        'modeleprevision must be a Modeleprevision')
            self._modeleprevision = modeleprevision

        except:
            raise

    # -- property qualite --
    @property
    def qualite(self):
        """Return indice de qualite."""
        return self._qualite

    @qualite.setter
    def qualite(self, qualite):
        """Set indice de qualite."""
        try:
            if qualite is not None:
                qualite = int(qualite)
                if qualite < 0 or qualite > 100:
                    raise ValueError('qualite is not in 0-100 range')
            self._qualite = qualite

        except:
            raise

    # -- property previsions_tend --
    @property
    def previsions_tend(self):
        """Return previsions_tend."""
        return self._previsions_tend

    @previsions_tend.setter
    def previsions_tend(self, previsions_tend):
        """Set previsions_tend."""
        try:
            if previsions_tend is not None:
                # we check we have a Series...
                # ... and that index contains datetimes
                if self._strict:
                    if not isinstance(previsions_tend, _pandas.Series) or \
                            previsions_tend.index.names != ['dte', 'tend']:
                        raise TypeError('previsions incorrect')
                    previsions_tend.index[0][0].isoformat()
            # all seeem's ok :-)
            self._previsions_tend = previsions_tend
        except:
            raise

    # -- property previsions --
    @property
    def previsions_prb(self):
        """Return previsions_prb."""
        return self._previsions_prb

    @previsions_prb.setter
    def previsions_prb(self, previsions_prb):
        """Set previsions_prb."""
        try:
            if previsions_prb is not None:
                # we check we have a Series...
                # ... and that index contains datetimes
                if self._strict:
                    if not isinstance(previsions_prb, _pandas.Series) or \
                            previsions_prb.index.names != ['dte', 'prb']:
                        raise TypeError('previsions incorrect')
                    previsions_prb.index[0][0].isoformat()
            # all seeem's ok :-)
            self._previsions_prb = previsions_prb
        except:
            raise

    # -- special methods --
    __all__attrs__ = ('entite', 'modeleprevision', 'grandeur', 'statut',
                      'qualite', 'public', 'commentaire', 'dtprod',
                      'previsions_prb', 'previsions_tend','intervenant')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        # init
        try:
            statut = _NOMENCLATURE[516][self.statut].lower()
        except Exception:
            statut = '<sans statut>'
        try:
            entite = '{} {}'.format(
                _sitehydro._ARTICLE[self.entite.__class__],
                self.entite.__unicode__())
        except (AttributeError, KeyError):
            entite = '<une entite inconnue>'
        try:
            prev = self.previsions_tend.__unicode__()
        except Exception:
            prev = '<sans previsions de tendance>'
        try:
            prev = self.previsions_prb.__unicode__()
        except Exception:
            prev = '<sans previsions probalistes>'
        try:
            dtprod = self.dtprod.isoformat(),
        except Exception:
            dtprod = '<inconnue>'
        try:
            qualite = '%i%%' % self.qualite
        except Exception:
            qualite = '<inconnue>'

        # action !
        return '''Simulation {0} de {1} sur {2}\n''' \
               '''Date de production: {3} - Qualite {4}\n''' \
               '''Commentaire: {5}\n''' \
               '''{6}\n''' \
               '''{7}\n''' \
               '''{8}\n''' \
               '''Previsions:\n {9}'''.format(
                   statut,
                   self.grandeur or '<sans grandeur>',
                   entite,
                   dtprod,
                   qualite,
                   self.commentaire or '<sans>',
                   '-' * 72,
                   self.modeleprevision or '<modele inconnu>',
                   '-' * 72,
                   prev)

    __str__ = _composant.__str__

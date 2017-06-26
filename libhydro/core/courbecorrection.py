# -*- coding: utf-8 -*-
"""Module courbecorrection.

Ce module contient les classes:
    # PivotCC
    # CourbeCorrection

"""

# imports recommandés
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from . import (_composant, sitehydro as _sitehydro)

#-- strings -------------------------------------------------------------------
__author__ = """Sebastien ROMON"""
__version__ = """0.1"""
__date__ = """2017-06-21"""


class PivotCC(object):
    """Classe PivotCC

    Classe pour manipuler les points pivots d'une courbe de correction

    Proprietes:
        dte (datetime.datetime) = date du point pivot
        deltah (float) = delta de hauteur
        dtactivation (string, defaut None) = date d'activation
        dtdesactivation (datetime.datetime) = date de désactivation
        strict (bool, defaut True) = strict or fuzzy mode

    """
    dte = _composant.Datefromeverything(required=True)
    dtactivation = _composant.Datefromeverything(required=False)
    dtdesactivation = _composant.Datefromeverything(required=False)

    def __init__(self, dte=None, deltah=None, dtactivation=None,
                 dtdesactivation=None, strict=True):
        """Constructor.

        Arguments:
            dte (datetime.datetime) = date du point pivot
            deltah (float) = delta de hauteur
            dtactivation (string, defaut None) = date d'activation
            dtdesactivation (datetime.datetime) = date de désactivation
            strict (bool, defaut True) = strict or fuzzy mode

        """

        self._strict = bool(strict)

        self.dte = dte
        self.dtactivation = dtactivation
        self.dtdesactivation = dtdesactivation

        # -- full properties --
        self._deltah = None
        self.deltah = deltah

    @property
    def deltah(self):
        """Return deltah."""
        return self._deltah

    @deltah.setter
    def deltah(self, deltah):
        """Set deltah."""
        if deltah is None:
            # None case
            if self._strict:
                raise TypeError('deltah is required')
        else:
            # other cases
            deltah = float(deltah)
        # all is well
        self._deltah = deltah

    def __unicode__(self):
        """Return unicode representation."""
        return 'Point pivot dte : {0} deltah : {1}'.format(
            self.dte if self.dte is not None else '<sans date>',
            self.deltah if self.deltah is not None else '<sans libelle>'
        )

    __str__ = _composant.__str__

    # pivot ordered by dte
    def __lt__(self, other):
        return self.dte < other.dte

    def __gt__(self, other):
        return self.dte > other.dte


class CourbeCorrection(object):
    """Classe CourbeCorrection

    Classe pour manipuler une courbe de correction
    Proprietes:
        station (sitehydro.Station)
        libelle (string ou None) = libellé
        commentaire (string ou None)
        pivots= Liste de points pivots
        dtmaj (datetime.datetime) = date de mise à jour
        tri_pivots (bool) = tri de spoints pivots par hauteur si True
    """

    dtmaj = _composant.Datefromeverything(required=False)

    def __init__(self, station=None, libelle=None,
                 commentaire=None, pivots=None, dtmaj=None, tri_pivots=True,
                 strict=True):

        self._strict = bool(strict)
        self._tri_pivots = bool(tri_pivots)

        # -- simple properties --
        self.libelle = unicode(libelle) \
            if (libelle is not None) else None
        self.commentaire = unicode(commentaire) \
            if (commentaire is not None) else None

        self.dtmaj = dtmaj

        # -- full properties --
        self._pivots = []
        self.pivots = pivots

        self._station = None
        self.station = station

    # -- property station --
    @property
    def station(self):
        """Return code courbe tarage."""
        return self._station

    @station.setter
    def station(self, station):
        """Set code station."""
        if station is None:
            # None case
            if self._strict:
                raise TypeError('station is required')
        else:
            # other cases
            if self._strict and not isinstance(station, _sitehydro.Station):
                raise TypeError('station is not a sitehydro.Station')
        # all is well
        self._station = station

    # -- property pivots --
    @property
    def pivots(self):
        """Return capteurs."""
        return self._pivots

    @pivots.setter
    def pivots(self, pivots):
        """Set pivots."""
        self._pivots = []
        # None case
        if pivots is None: #pivots facultatifs
            return

        # one Pivot, we make a list if not strict
        if not hasattr(pivots, '__iter__'):
            if self._strict:
                raise TypeError('pivots is not iterable')
            else:
                self._pivots = [pivots]
                return

        # an iterable of pivots
        if self._strict and len(pivots) == 1:
            raise TypeError('pivots must be an iterable of minimum 2 PivotCC')
        dtes = set()
        for pivot in pivots:
            # some checks
            if self._strict:
                if not isinstance(pivot, PivotCC):
                    raise TypeError(
                        'pivots must be a PivotCC or an iterable of PivotCC'
                    )

            if self._strict and pivot.dtdesactivation is None:
                if pivot.dte in dtes:
                    raise ValueError('pivots contains 2 pivots with same date')
                dtes.add(pivot.dte)

            # add pivot
            self._pivots.append(pivot)

        # Sort pivots if necessary
        if self._tri_pivots:
            # pivots my not be sorted if fuzzy mode
            try:
                self._pivots.sort()
            except TypeError:
                pass


    def remove_deactived_pivots(self):
        """remove pivots which dtdesactivation is not None"""
        self.pivots = self.get_actived_pivots()

    def get_actived_pivots(self):
        """remove pivots which dtdesactivation is not None"""
        pivots = []
        for pivot in self.pivots:
            if pivot.dtdesactivation is None:
                pivots.append(pivot)
        return pivots

    def __unicode__(self):
        """Return unicode representation."""
        if self.station is None:
            codestation = '<sans codestation>'
        elif hasattr(self.station, 'code'):
            codestation = self.station.code
        else:
            codestation = unicode(self.station.__str__())
#        elif hasattr(self.station, '__str__'):
#            codestation = unicode(self.station.__str__())
#        else:
#            codestation = 'non affichable'
        return 'Courbe de correction {0}::{1} [{2} pivot{3}]'.format(
            codestation,
            self.libelle if self.libelle is not None else '<sans libelle>',
            len(self.pivots),
            '' if (len(self.pivots) < 2) else 's'
        )

    __str__ = _composant.__str__

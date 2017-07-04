# -*- coding: utf-8 -*-
"""
Module courbetarage

Ce module contient les classes:
    # CourbeTarage
    # PivotCT
    # PivotCTPuissance
    # PivotCTPOly
    # PeriodeCT
    # HistoActivePeriode

"""

# imports recommandés
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime

from . import (_composant, sitehydro as _sitehydro)
from . import intervenant as _intervenant
from .nomenclature import NOMENCLATURE as _NOMENCLATURE

__author__ = """Sebastien ROMON"""
__version__ = """0.1"""
__date__ = """2017-06-13"""


class PivotCT(object):
    """Classe CourbeTarage.

    Classe abstraite commune aux deux classes PivotCTPoly et PivotCTPuissance

    Proprietes:
        hauteur (float)
        qualif (int in NOMENCLATURE[505]) = qualification du point pivot
    """

    qualif = _composant.Nomenclatureitem(nomenclature=505)

    def __init__(self, hauteur=None, qualif=16, strict=True):
        """Initialisation

        Arguments:
           hauteur (float)
           qualif (int in NOMENCLATURE[505])
        """
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(PivotCT)['qualif'].strict = self._strict

        # -- descriptors --
        self.qualif = qualif

        # -- full properties --
        self._hauteur = None
        self.hauteur = hauteur


    @property
    def hauteur(self):
        """Return hauteur."""
        return self._hauteur

    @hauteur.setter
    def hauteur(self, hauteur):
        """Set hauteur."""
        if hauteur is None:
            # None case
            if self._strict:
                raise TypeError('hauteur is required')
        else:
            # other cases
            hauteur = float(hauteur)
        # all is well
        self._hauteur = hauteur

    # pivot ordered by hauteur
    def __lt__(self, other):
        return self.hauteur < other.hauteur

    def __gt__(self, other):
        return self.hauteur > other.hauteur

class PivotCTPuissance(PivotCT):
    """Classe PivotPolyCT

    Classe pour manipuler des points pivots d'une courbe de tarage puissance.

    Proprietes:
        hauteur (float)
        qualif (int in NOMENCLATURE[505])
        vara (float)
        varb (float)
        varh (float)
        libelle (string)
    """
    def __init__(self, hauteur=None, qualif=16,
                 vara=None, varb=None, varh=None, strict=True):
        # -- super --
        super(PivotCTPuissance, self).__init__(
            hauteur=hauteur, qualif=qualif, strict=strict
        )

        # -- full properties --
        self._vara = None
        self.vara = vara
        self._varb = None
        self.varb = varb
        self._varh = None
        self.varh = varh

    @property
    def vara(self):
        """Return vara."""
        return self._vara

    @vara.setter
    def vara(self, vara):
        """Set coefa."""
        if vara is None:
            # None case
            if self._strict:
                raise TypeError('vara is required')
        else:
            # other cases
            vara = float(vara)
        # all is well
        self._vara = vara

    @property
    def varb(self):
        """Return varb."""
        return self._varb

    @varb.setter
    def varb(self, varb):
        """Set varb."""
        if varb is None:
            # None case
            if self._strict:
                raise TypeError('varb is required')
        else:
            # other cases
            varb = float(varb)
        # all is well
        self._varb = varb

    @property
    def varh(self):
        """Return varh."""
        return self._varh

    @varh.setter
    def varh(self, varh):
        """Set varh."""
        if varh is None:
            # None case
            if self._strict:
                raise TypeError('varh is required')
        else:
            # other cases
            varh = float(varh)
        # all is well
        self._varh = varh

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Point pivot de hauteur {0}'\
               ' et de coefficients a={1} b={2} et h0={3}'.format(
                   self.hauteur or '<sans hauteur>',
                   self.vara or '<sans coef a>',
                   self.varb or '<sans coef b>',
                   self.varh or '<sans coef h0>'
                   )

    __str__ = _composant.__str__

class PivotCTPoly(PivotCT):
    """Classe PivotPolyCT

    Classe pour manipuler des points pivots d'une courbe de tarage puissance.

    Proprietes:
        hauteur (float)
        qualif (int in NOMENCLATURE 505)
        debit (float)
    """
    def __init__(self, hauteur=None, qualif=16, debit=None, strict=True):
        # -- super --
        super(PivotCTPoly, self).__init__(
            hauteur=hauteur, qualif=qualif, strict=strict
        )

        # -- full properties --
        self._debit = None
        self.debit = debit

    @property
    def debit(self):
        """Return debit."""
        return self._debit

    @debit.setter
    def debit(self, debit):
        """Set debit."""
        if debit is None:
            # None case
            if self._strict:
                raise TypeError('debit is required')
        else:
            # other cases
            debit = float(debit)
        # all is well
        self._debit = debit

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Point pivot de hauteur {0} et de debit {1}'.format(
            self.hauteur, self.debit
            )

    __str__ = _composant.__str__


class HistoActivePeriode(object):
    """Classe HistoActivePeriode

    Classe pour manipuler l'historique d'activation des periodes
    d'une courbe de tarage.
    Vérification que la date de désactivation si elle est définie
    est ultérieure à la date d'activation

    Proprietes:
        dtactivation (datetime.datetime)
        dtdesactivation (datetime.datetime ou None)
    """
    dtactivation = _composant.Datefromeverything(required=True)
    _dtdesactivation = _composant.Datefromeverything(required=False)

    def __init__(self, dtactivation=None, dtdesactivation=None):
        self.dtactivation = dtactivation

        # descripor inside full properties
        self._dtdesactivation = None
        self.dtdesactivation = dtdesactivation

    @property
    def dtdesactivation(self):
        """Return dtdesactivation"""
        return self._dtdesactivation

    @dtdesactivation.setter
    def dtdesactivation(self, dtdesactivation):
        self._dtdesactivation = dtdesactivation
        if self._dtdesactivation is not None and self._dtdesactivation < self.dtactivation:
            raise ValueError('deactivation date must be later than activation date')

class PeriodeCT(object):
    """Classe Periode CT.

    Classe pour manipuler des périodes d'activation d'une courbe de tarage.

    Proprietes:
        dtdeb (datetime.datetime)
        dtfin (datetime.datetime)
        etat (int in NOMENCLATURE[504])
            0: 'Non utilisable', 4:'Utilisable', 8: 'Utilisée', 12: 'Travail'
        histos (iterable of HistoActivePeriode ou None)

    """
    dtdeb = _composant.Datefromeverything(required=True)
    dtfin = _composant.Datefromeverything(required=False)
    etat = _composant.Nomenclatureitem(nomenclature=504)

    def __init__(self, dtdeb=None, dtfin=None, etat=8, histos=None,
                 strict=True):

        self._strict = bool(strict)

        self.dtdeb = dtdeb
        self.dtfin = dtfin
        if self.dtfin is not None and self.dtfin < self.dtdeb:
            raise ValueError('dtfin must be later than dtdeb')
        self.etat = etat

        self._histos = None
        self.histos = histos

    @property
    def histos(self):
        """Return histos."""
        return self._histos

    @histos.setter
    def histos(self, histos):
        """Set histos."""
        self._histos = []
        if histos is None:
            return
        elif isinstance(histos, HistoActivePeriode):
            self._histos = [histos]
        else:
            for histo in histos:
                if isinstance(histo, HistoActivePeriode):
                    self._histos.append(histo)
                else:
                    if self._strict:
                        raise TypeError(('histos is not a HistoActivePeriode'
                                         ' or an iterable of HistoActivePeriode'))

class CourbeTarage(object):
    """Classe CourbeTarage.

    Classe pour manipuler des courbes de tarage.

    Proprietes:
        code (string) = code courbe tarage
        typect (int parmi NOMENCLATURE[503]) 0 ou 4
        libelle (string)
        limiteinf (float) = limite inférieure d'utilisation
        limitesup (float) = limite supérieure d'utilisation
        dn (float or None) = dénivelé (station à pente)
        alpha (float or None) (station à pente)
        beta (float or None) (station à pente)
        commentaire (string or Noe)
        station (sitehydro.Station)
        contact (intervenant.Contact or None)
        pivots (iterable of PivotCTPoly (typect = 0))
        periodes (PeriodeCT or an iterable of PeriodeCT)
            or PivotCTPoly (typect = 4)
        dtmaj (datetime.datetime) = date de mise à jour
        tri_pivots (bool) = tri de spoints pivots par hauteur si True
    """

    typect = _composant.Nomenclatureitem(nomenclature=503)
    _dtmaj = _composant.Datefromeverything(required=False)

    def __init__(self, code=None, libelle=None, station=None,
                 typect=0, limiteinf=None, limitesup=None, dn=None, alpha=None,
                 beta=None, commentaire=None, contact=None, pivots=None,
                 periodes=None, dtmaj=None, tri_pivots=True, strict=True):
        """
            tri_pivots (bool) tri des points en fonction de la hauteur
        """

        self._strict = bool(strict)
        self._tri_pivots = bool(tri_pivots)

        # -- adjust the descriptor --
        vars(self.__class__)['typect'].strict = self._strict

        # -- descriptors --
        self.typect = typect

        # descripor inside full properties
        self._dtmaj = None
        self.dtmaj = dtmaj

        # -- simple properties --
        self.commentaire = str(commentaire) \
            if (commentaire is not None) else None

        # -- full properties --
        self._code = None
        self.code = code

        self._libelle = None
        self.libelle = libelle

        # self._limiteinf and self._limitesupmust exist before
        # setting limiteinf and limitesup
        self._limiteinf = self._limitesup = None
        self.limiteinf = limiteinf
        self.limitesup = limitesup

        self._dn = None
        self.dn = dn

        self._alpha = None
        self.alpha = alpha

        self._beta = None
        self.beta = beta

        self._contact = None
        self.contact = contact

        self._pivots = []
        self.pivots = pivots

        self._periodes = []
        self.periodes = periodes

        self._station = None
        self.station = station

    # -- property code --
    @property
    def code(self):
        """Return code courbe tarage."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code courbe tarage."""
        if code is None:
            # None case
            if self._strict:
                raise TypeError('code is required')
        else:
            # other cases
            code = str(code)
        # all is well
        self._code = code

    # -- property libelle --
    @property
    def libelle(self):
        """Return libelle courbe tarage."""
        return self._libelle

    @libelle.setter
    def libelle(self, libelle):
        """Set libelle courbe tarage."""
        if libelle is None:
            # None case
            if self._strict:
                raise TypeError('libelle is required')
        else:
            # other cases
            libelle = str(libelle)
        # all is well
        self._libelle = libelle

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

    @property
    def limiteinf(self):
        """Return limiteinf."""
        return self._limiteinf

    @limiteinf.setter
    def limiteinf(self, limiteinf):
        """Set debit."""
        if limiteinf is not None:
            # other cases
            limiteinf = float(limiteinf)
            if self.limitesup is not None and self.limitesup < limiteinf:
                raise ValueError("limiteinf must be smaller than limitesup")
        # all is well
        self._limiteinf = limiteinf

    @property
    def limitesup(self):
        """Return limitesup."""
        return self._limitesup

    @limitesup.setter
    def limitesup(self, limitesup):
        """Set debit."""
        if limitesup is not None:
            # other cases
            limitesup = float(limitesup)
            if self.limiteinf is not None and limitesup < self.limiteinf:
                raise ValueError("limiteinf must be smaller than limitesup")
        # all is well
        self._limitesup = limitesup

    @property
    def dn(self):
        """Return denivelle."""
        return self._dn

    @dn.setter
    def dn(self, dn):
        """Set dn."""
        if dn is not None:
            # other cases
            dn = float(dn)
        # all is well
        self._dn = dn

    @property
    def alpha(self):
        """Return alpha."""
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        """Set alpha."""
        if alpha is not None:
            # other cases
            alpha = float(alpha)
        # all is well
        self._alpha = alpha

    @property
    def beta(self):
        """Return coefficient beta."""
        return self._beta

    @beta.setter
    def beta(self, beta):
        """Set beta."""
        if beta is not None:
            # other cases
            beta = float(beta)
            if beta < 0:
                raise ValueError("beta must be positive")
        # all is well
        self._beta = beta


    # -- property contact --
    @property
    def contact(self):
        """Return contact."""
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Set contact."""
        if contact is not None:
            if self._strict and not isinstance(contact, _intervenant.Contact):
                raise TypeError('contact incorrect')

        self._contact = contact

    @property
    def periodes(self):
        """Return periodes."""
        return self._periodes

    @periodes.setter
    def periodes(self, periodes):
        """Set periodes courbe tarage."""
        self._periodes = []
        if periodes is None:
            # None case
            return
        elif isinstance(periodes, PeriodeCT):
            self._periodes = [periodes]
        else:
            for periode in periodes:
                if isinstance(periode, PeriodeCT):
                    self._periodes.append(periode)
                else:
                    if self._strict:
                        raise TypeError('periodes is not a PeriodeCT'\
                                        ' or an iterable of PeriodeCT')

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
        if pivots is None:
            return
        if not hasattr(pivots, '__iter__'):
            if self._strict:
                raise TypeError('pivots is not iterable')
            else:
                self._pivots = [pivots]
                return

        if self._strict and len(pivots) == 1:
            raise TypeError('pivots must not contain only one pivot')
        # an iterable of pivots
        hauteurs = set()
        for pivot in pivots:
            # some checks
            if self._strict:
                if self.typect == 0:
                    if not isinstance(pivot, PivotCTPoly):
                        raise TypeError(
                            'pivots must be a PivotCTPoly'\
                            ' or an iterable of PivotCTPoly'
                        )
                if self.typect == 4:
                    if not isinstance(pivot, PivotCTPuissance):
                        raise TypeError(
                            'pivots must be a PivotCTPuissance'\
                            ' or an iterable of PivotCTPuissance'
                        )
                if self._strict: #and pivot.dtdesactivation is None:
                    if pivot.hauteur in hauteurs:
                        raise ValueError(
                            "pivots contains pivots with same hauteur")
                    hauteurs.add(pivot.hauteur)
            # add pivot
            self._pivots.append(pivot)

        # Sort pivots if necessary
        if self._tri_pivots:
            self._pivots.sort()

    # -- property dtmaj --
    @property
    def dtmaj(self):
        """Return contact."""
        return self._dtmaj

    @dtmaj.setter
    def dtmaj(self, dtmaj):
        self._dtmaj = dtmaj
        if self._dtmaj is not None and \
                self._dtmaj > _datetime.datetime.utcnow():
            raise ValueError('dtmaj cannot be in the future')

    def get_used_actived_periodes(self):
        """Return periodes used (periode.etat=8) and not deactived """
        periodes = []
        for periode in self.periodes:
            if periode.etat == 8:
                actived = False
                if len(periode.histos) == 0:
                    actived = True
                for histo in periode.histos:
                    if histo.dtdesactivation is None:
                        actived = True
                        break
                if actived:
                    periodes.append(periode)
        return periodes

    def is_used(self, dte):
        """check if the CourbeTarge is used and actived at dte"""
        for periode in self.periodes:
            if periode.etat == 8 and periode.dtdeb <= dte and \
                    (periode.dtfin is None or periode.dtfin >= dte):
                if len(periode.histos) == 0:
                    return True
                for histo in periode.histos:
                    if histo.dtdesactivation is None:
                        return True
        return False

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        try:
            typect = _NOMENCLATURE[503][self.typect].lower()
        except Exception:
            typect = '<sans type>'
        return 'Courbe de tarage de type {0} {1}::{2} [{3} point{4} pivot]'.format(
            typect,
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.pivots),
            '' if (len(self.pivots) < 2) else 's'
        )

    __str__ = _composant.__str__

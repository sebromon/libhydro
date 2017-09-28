# -*- coding: utf-8 -*-
"""
Module jaugeage

Ce module contient les classes:
    # HauteurJaugeage
    # Jaugeage

"""

# imports recommandés
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from . import (_composant, sitehydro as _sitehydro)

# -- strings ------------------------------------------------------------------
__author__ = """Sebastien ROMON"""
__version__ = """0.1"""
__date__ = """2017-06-30"""


class HauteurJaugeage(object):
    """Class HauteurJaugeage
    Classe pour manipuler une hauteur d'un jaugeage
    Proprietes:
        station (sitehydro.Station)
        sysalti (int parmi NOMENCLATURE[76]): système altimétrique default 31
        coteretenue (float)
        cotedeb (float)
        cotefin (float)
        denivele (float ou None)
        distancestation (float ou None)
        stationfille (sitehydro.Station ou None)
        dtdeb_refalti (datetime.datetime ou None)
    """

    sysalti = _composant.Nomenclatureitem(nomenclature=76)
    dtdeb_refalti = _composant.Datefromeverything(required=False)

    def __init__(self, station=None, sysalti=31,
                 coteretenue=None, cotedeb=None, cotefin=None, denivele=None,
                 distancestation=None, stationfille=None, dtdeb_refalti=None,
                 strict=True):

        self._strict = bool(strict)

        self.sysalti = sysalti
        self.dtdeb_refalti = dtdeb_refalti

        self._station = None
        self.station = station
        self._stationfille = None
        self.stationfille = stationfille

        self._coteretenue = self._cotedeb = self._cotefin = None
        self.coteretenue = coteretenue
        self.cotedeb = cotedeb
        self.cotefin = cotefin

        self._denivele = None
        self.denivele = denivele

        self._distancestation = None
        self.distancestation = distancestation

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
    def coteretenue(self):
        """Return coteretenue."""
        return self._coteretenue

    @coteretenue.setter
    def coteretenue(self, coteretenue):
        """Set coteretenue."""
        if coteretenue is not None:
            coteretenue = float(coteretenue)
        else:
            raise ValueError('coteretenue is required')
        # all is well
        self._coteretenue = coteretenue

    @property
    def cotedeb(self):
        """Return deltah."""
        return self._cotedeb

    @cotedeb.setter
    def cotedeb(self, cotedeb):
        """Set deltah."""
        if cotedeb is not None:
            cotedeb = float(cotedeb)

        # all is well
        self._cotedeb = cotedeb

    @property
    def cotefin(self):
        """Return deltah."""
        return self._cotefin

    @cotefin.setter
    def cotefin(self, cotefin):
        """Set deltah."""
        if cotefin is not None:
            cotefin = float(cotefin)

        # all is well
        self._cotefin = cotefin

    @property
    def denivele(self):
        """Return denivele."""
        return self._denivele

    @denivele.setter
    def denivele(self, denivele):
        """Set denivele."""
        if denivele is not None:
            denivele = float(denivele)

        # all is well
        self._denivele = denivele

    @property
    def distancestation(self):
        """Return distancestation."""
        return self._distancestation

    @distancestation.setter
    def distancestation(self, distancestation):
        """Set distancestation."""
        if distancestation is not None:
            distancestation = float(distancestation)

        # all is well
        self._distancestation = distancestation

    # -- property stationfille --
    @property
    def stationfille(self):
        """Return code courbe tarage."""
        return self._stationfille

    @stationfille.setter
    def stationfille(self, stationfille):
        """Set code station."""
        if stationfille is not None:
            if self._strict \
                    and not isinstance(stationfille, _sitehydro.Station):
                raise TypeError('stationfille is not a sitehydro.Station')
        # all is well
        self._stationfille = stationfille

    # pivot ordered by dte
    def __lt__(self, other):
        return self.coteretenue < other.coteretenue

    def __gt__(self, other):
        return self.coteretenue > other.coteretenue

    def __unicode__(self):
        """return unicode"""
        cote = self.coteretenue if self.coteretenue is not None \
            else '<sans cote>'
        if self.station is None:
            station = '<sans station>'
        else:
            if isinstance(self.station, _sitehydro.Station):
                station = self.station.code
            else:
                station = self.station
        return 'Hauteur de jaugeage de cote {}\n' \
               'Station {}'.format(cote, station)

    __str__ = _composant.__str__


class Jaugeage(object):
    """Class Jaugeage
    Classe pour manipuler les points pivots d'une courbe de correction

    Proprietes:
    """

    dte = _composant.Datefromeverything(required=False)
    dtdeb = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)
    dtmaj = _composant.Datefromeverything(required=False)

    mode = _composant.Nomenclatureitem(nomenclature=873, required=False)

    def __init__(self, code=None, dte=None, debit=None, dtdeb=None, dtfin=None,
                 section_mouillee=None, perimetre_mouille=None,
                 largeur_miroir=None, mode=None, commentaire=None,
                 vitessemoy=None, vitessemax=None, vitessemoy_surface=None,
                 site=None, hauteurs=None, dtmaj=None, tri_hauteurs=True, strict=True):

        self._strict = bool(strict)
        self._tri_hauteurs = bool(tri_hauteurs)

        self.commentaire = str(commentaire) \
            if commentaire is not None else None

        self.dte = dte
        self.dtdeb = dtdeb
        self.dtfin = dtfin
        self.dtmaj = dtmaj
        self.mode = mode

        # -- full properties --
        self._code = None
        self.code = code

        self._site = None
        self.site = site

        self._debit = None
        self.debit = debit

        self._section_mouillee = None
        self.section_mouillee = section_mouillee

        self._perimetre_mouille = None
        self.perimetre_mouille = perimetre_mouille

        self._largeur_miroir = None
        self.largeur_miroir = largeur_miroir

        self._vitessemoy = None
        self.vitessemoy = vitessemoy
        self._vitessemax = None
        self.vitessemax = vitessemax
        self._vitessemoy_surface = None
        self.vitessemoy_surface = vitessemoy_surface

        self._hauteurs = []
        self.hauteurs = hauteurs

    @property
    def code(self):
        """Return code."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code."""
        if code is None:
            raise TypeError('code is required')
        else:
            code = str(code)
        # all is well
        self._code = code

    @property
    def debit(self):
        """Return debit."""
        return self._debit

    @debit.setter
    def debit(self, debit):
        """Set debit."""
        if debit is not None:
            debit = float(debit)
        # all is well
        self._debit = debit

    @property
    def perimetre_mouille(self):
        """Return perimetre_mouille."""
        return self._perimetre_mouille

    @perimetre_mouille.setter
    def perimetre_mouille(self, perimetre_mouille):
        """Set deltah."""
        if perimetre_mouille is not None:
            perimetre_mouille = float(perimetre_mouille)
        # all is well
        self._perimetre_mouille = perimetre_mouille

    @property
    def section_mouillee(self):
        """Return section_mouillee."""
        return self._section_mouillee

    @section_mouillee.setter
    def section_mouillee(self, section_mouillee):
        """Set section_mouillee."""
        if section_mouillee is not None:
            section_mouillee = float(section_mouillee)
        # all is well
        self._section_mouillee = section_mouillee

    @property
    def largeur_miroir(self):
        """Return largeur_miroir."""
        return self._largeur_miroir

    @largeur_miroir.setter
    def largeur_miroir(self, largeur_miroir):
        """Set largeur_miroir."""
        if largeur_miroir is not None:
            largeur_miroir = float(largeur_miroir)
        # all is well
        self._largeur_miroir = largeur_miroir

    @property
    def vitessemoy(self):
        """Return vitessemoy."""
        return self._vitessemoy

    @vitessemoy.setter
    def vitessemoy(self, vitessemoy):
        """Set vitessemoy."""
        if vitessemoy is not None:
            vitessemoy = float(vitessemoy)
        # all is well
        self._vitessemoy = vitessemoy

    @property
    def vitessemax(self):
        """Return vitessemax."""
        return self._vitessemax

    @vitessemax.setter
    def vitessemax(self, vitessemax):
        """Set vitessemax."""
        if vitessemax is not None:
            vitessemax = float(vitessemax)
        # all is well
        self._vitessemax = vitessemax

    @property
    def vitessemoy_surface(self):
        """Return vitessemoy_surface."""
        return self._vitessemoy_surface

    @vitessemoy_surface.setter
    def vitessemoy_surface(self, vitessemoy_surface):
        """Set vitessemoy_surface."""
        if vitessemoy_surface is not None:
            vitessemoy_surface = float(vitessemoy_surface)
        # all is well
        self._vitessemoy_surface = vitessemoy_surface

    # -- property station --
    @property
    def site(self):
        """Return site."""
        return self._site

    @site.setter
    def site(self, site):
        """Set site."""
        if site is None:
            # None case
            if self._strict:
                raise TypeError('site is required')
        else:
            # other cases
            if self._strict and not isinstance(site, _sitehydro.Sitehydro):
                raise TypeError('site is not a sitehydro.Sitehydro')
        # all is well
        self._site = site

    # -- property hauteurs --
    @property
    def hauteurs(self):
        """Return hauteurs."""
        return self._hauteurs

    @hauteurs.setter
    def hauteurs(self, hauteurs):
        """Set hauteurs."""
        self._hauteurs = []
        if hauteurs is None:
            return
        if isinstance(hauteurs, HauteurJaugeage):
            self._hauteurs = [hauteurs]
            return
        for hauteur in hauteurs:
            if not isinstance(hauteur, HauteurJaugeage):
                if self._strict:
                    raise TypeError('hauteurs is not an iterable'
                                    ' of HauteurJaugeage')
            self._hauteurs.append(hauteur)
        if self._tri_hauteurs:
            self._hauteurs.sort()

    def __unicode__(self):
        code = self.code if self.code is not None else '<sans code>'
        debit = self.debit if self.debit is not None else '<sans debit>'
        # site to string
        if self.site is None:
            site = '<sans site>'
        else:
            if isinstance(self.site, _sitehydro.Sitehydro):
                site = self.site.code
            else:
                site = self.site
        # dte to string
        if self.dte is not None:
            dte = self.dte.isoformat()
        else:
            dte = '<sans date>'
        nhauteurs = len(self.hauteurs)
        return 'Jaugeage {} du site {}\n' \
               'Date: {}\n' \
               'Debit {} associe a {} hauteur(s)\n'.format(code, site, dte,
                                                           debit, nhauteurs)

    __str__ = _composant.__str__

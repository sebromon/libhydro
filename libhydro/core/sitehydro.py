# coding: utf-8
"""Module sitehydro.

Ce module contient les classes:
    # Sitehydro
    # Station
    # Capteur
    # Tronconvigilance

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from . import (_composant, _composant_site)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__contributor__ = """Camillo Montes (SYNAPSE)"""
__version__ = """0.4a"""
__date__ = """2015-10-30"""

# HISTORY
# V0.4 - 2014-12-17
#   change the class Stationhydro name to Station which is far better for
#       metaprogramming regarding the Sitehydro stations list name
# V0.3 - 2014-02-20
#   add the _Entitehydro comparison methods, the switch it to the _composant
#       module
#   use descriptors
#   merge Camillo (CMO) work
# V0.1 - 2013-07-12
#   first shot

# -- todos --------------------------------------------------------------------
# PROGRESS - Sitehydro 20% - Station 30% - Capteur 30%
#            Tronconvigilance 100%
# FIXME - generalize typeentite in _Entite.typentite ?
# TODO - add navigability for Capteur => Station and Station => Site


# -- config -------------------------------------------------------------------
# config use classes definitions and is at the bottom


# -- class _Entitehydro -------------------------------------------------------
class _Entitehydro(object):

    """Abstract base class for all hydro entities.

    Properties:
        code (string(x)) = hydro code
        codeh2 (string(8)) = ancien code hydro2
        libelle (string)
        _strict (bool) = strict or fuzzy mode

    """

    def __init__(self, code, codeh2=None, libelle=None, strict=True):
        """Constructor.

        Arguments:
            code (string(8, 10, 12)) = hydro code
            codeh2 (string(8), defaut None) = ancien code hydro2
            libelle (string, defaut None)
            strict (bool, defaut True) = strict or fuzzy mode

        """

        # -- simple properties --
        self._strict = bool(strict)
        self.libelle = unicode(libelle) if (libelle is not None) else None

        # -- full properties --
        self._code = self._codeh2 = None
        self.code = code
        self.codeh2 = codeh2

    # -- property code --
    @property
    def code(self):
        """Return code hydro."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code hydro."""
        try:
            if code is None:
                # None case
                if self._strict:
                    raise TypeError('code is required')

            else:
                # other cases
                code = unicode(code)
                if self._strict and (self.__class__ in _CODE_HYDRO_LENGTH):
                    # check code hydro
                    _composant.is_code_hydro(
                        code=code,
                        length=_CODE_HYDRO_LENGTH[self.__class__],
                        errors='strict'
                    )

            # all is well
            self._code = code

        except:
            raise

    # -- property codeh2 --
    @property
    def codeh2(self):
        """Return code hydro2."""
        return self._codeh2

    @codeh2.setter
    def codeh2(self, code):
        """Set code hydro2."""
        try:
            if code is not None:
                code = unicode(code)
                _composant.is_code_hydro(code, 8, errors='strict')

            # all is well
            self._codeh2 = code

        except:
            raise

    # -- special methods --
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__


# -- class _Site_or_station --------------------------------------------------
class _Site_or_station(_Entitehydro):

    """Abstract base class for Sitehydro and Station.

    Properties:
        -- properties of _Entitehydro     --
        -- properties of _composant.Coord --

    """

    def __init__(
        self, code, codeh2=None, libelle=None,
        coord=None, strict=True
    ):
        """Constructor.

        Arguments:
            -- args of _Entitehydro --
            coord (liste ou dict) = (x, y, proj) ou
                {'x': x, 'y': y, 'proj': proj}

        """

        # -- super --
        super(_Site_or_station, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle, strict=strict
        )

        # -- full properties --
        self._coord = None
        self.coord = coord

    # -- property coord --
    @property
    def coord(self):
        """Return coord."""
        return self._coord

    @coord.setter
    def coord(self, coord):
        """Set coord."""
        self._coord = None
        if coord is not None:
            if isinstance(coord, _composant_site.Coord):
                self._coord = coord
            else:
                try:
                    # instanciate with a list
                    self._coord = _composant_site.Coord(*coord)
                except (TypeError, ValueError, AttributeError):
                    try:
                        # instanciate with a dict
                        self._coord = _composant_site.Coord(**coord)
                    except (TypeError, ValueError, AttributeError):
                        raise TypeError('coord incorrect')


# -- class Sitehydro ----------------------------------------------------------
class Sitehydro(_Site_or_station):

    """Classe Sitehydro.

    Classe pour manipuler des sites hydrometriques.

    Proprietes:
        code (string(8)) = code hydro
        codeh2 (string(8)) = ancien code hydro2
        typesite (string parmi NOMENCLATURE[530])
        libelle (string)
        libelleusuel (string)
        coord (Coord) =
            x, y (float)
            proj (int parmi NOMENCLATURE[22]) = systeme de projection
        stations (une liste de Station)
        communes (une liste de codes communes, string(5)) = code INSEE commune
        tronconsvigilance (une liste de Tronconvigilance)

    """

    # Sitehydro other properties

    # libellecomplement
    # mnemonique
    # precisionce
    # pkamont
    # pkaval
    # altitude, sysalti
    # dtmaj
    # bv
    # fuseau
    # statut
    # ponctuel
    # dtpremieredonnee
    # moisetiage
    # moisanneehydro
    # publication
    # essai
    # influence
    # influencecommentaire
    # commentaire

    # siteattache
    # siteassocie
    # masses d'eau
    # entitehydro
    # loistats
    # images
    # rolecontact
    # zonehydro
    # tronconhydro

    typesite = _composant.Nomenclatureitem(nomenclature=530)

    def __init__(
        self, code, codeh2=None, typesite='REEL',
        libelle=None, libelleusuel=None, coord=None, stations=None,
        communes=None, tronconsvigilance=None, strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(8)) = code hydro
            codeh2 (string(8)) = ancien code hydro2
            typesite (string parmi NOMENCLATURE[530], defaut REEL)
            libelle (string)
            libelleusuel (string)
            coord (list ou dict) =
                (x, y, proj) ou {'x': x, 'y': y, 'proj': proj}
                avec proj (int parmi NOMENCLATURE[22]) = systeme de projection
            stations (une Station ou un iterable de Station)
            communes (un code commmune ou un iterable de codes)
            tronconsvigilance (un Tronconvigilance ou un iterable)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type, du code et des stations

        """

        # -- super --
        super(Sitehydro, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle,
            coord=coord, strict=strict
        )

        # -- adjust the descriptor --
        vars(Sitehydro)['typesite'].strict = self._strict

        # -- simple properties --
        self.libelleusuel = unicode(libelleusuel) \
            if (libelleusuel is not None) else None

        # -- descriptors --
        self.typesite = typesite

        # -- full properties --
        self._stations = self._communes = self._tronconsvigilance = []
        self.stations = stations
        self.communes = communes
        self.tronconsvigilance = tronconsvigilance

    # -- property stations --
    @property
    def stations(self):
        """Return stations."""
        return self._stations

    @stations.setter
    def stations(self, stations):
        """Set stations."""
        self._stations = []
        # None case
        if stations is None:
            return
        # one station, we make a list with it
        if isinstance(stations, Station):
            stations = [stations]
        # an iterable of stations
        for station in stations:
            # some checks
            if self._strict:
                if not isinstance(station, Station):
                    raise TypeError(
                        'stations must be a Station or an iterable of Station'
                    )
                elif station.typestation not in \
                        _SITE_ACCEPTED_STATION[self.typesite]:
                    raise ValueError(
                        '{0} station forbidden for {1} site'.format(
                            station.typestation, self.typesite
                        )
                    )
            # add station
            self._stations.append(station)

    # -- property communes --
    @property
    def communes(self):
        """Return codes communes."""
        return self._communes

    @communes.setter
    def communes(self, communes):
        """Set code commune."""
        self._communes = []
        # None case
        if communes is None:
            return
        # one commune, we make a list with it
        if _composant.is_code_insee(communes, length=5, errors='ignore'):
            communes = [communes]
        # an iterable of communes
        for commune in communes:
            if _composant.is_code_insee(commune, length=5, errors='strict'):
                self._communes.append(unicode(commune))

    # -- property tronconsvigilance --
    @property
    def tronconsvigilance(self):
        """Return tronconsvigilance."""
        return self._tronconsvigilance

    @tronconsvigilance.setter
    def tronconsvigilance(self, tronconsvigilance):
        """Set tronconsvigilance."""
        self._tronconsvigilance = []
        # None case
        if tronconsvigilance is None:
            return
        # one troncon, we make a list with it
        if isinstance(tronconsvigilance, Tronconvigilance):
            tronconsvigilance = [tronconsvigilance]
        # an iterable of tronconsvigilance
        for tronconvigilance in tronconsvigilance:
            # some checks
            if self._strict:
                if not isinstance(tronconvigilance, Tronconvigilance):
                    raise TypeError(
                        'tronconsvigilance must be a Tronconvigilance '
                        'or an iterable of Tronconvigilance'
                    )
            # add station
            self._tronconsvigilance.append(tronconvigilance)

    # -- special methods --
    __all__attrs__ = (
        'code', 'codeh2', 'typesite', 'libelle', 'libelleusuel', 'coord',
        'stations', 'communes', 'tronconsvigilance'
    )

    def __unicode__(self):
        """Return unicode representation."""
        return 'Site {0} {1}::{2} [{3} station{4}]'.format(
            self.typesite or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.stations),
            '' if (len(self.stations) < 2) else 's'
        )

    __str__ = _composant.__str__


# -- class Station ------------------------------------------------------------
class Station(_Site_or_station):

    """Classe Station.

    Classe pour manipuler des stations hydrometriques.

    Proprietes:
        code (string(10)) = code hydro
        codeh2 (string(8)) = ancien code hydro2
        typestation (string parmi NOMENCLATURE[531])
        libelle (string)
        libellecomplement (string)
        niveauaffichage (int) = niveau d'affichage
        coord (Coord) =
            x, y (float)
            proj (int parmi NOMENCLATURE[22]) = systeme de projection
        capteurs (une liste de Capteur)
        commune (string(5)) = code INSEE commune
        ddcs (liste de string(10)) = liste de reseaux de mesure SANDRE
            (dispositifs de collecte)

    """

    # Station other properties

    # sitehydro

    # descriptif
    # dtmaj
    # pk
    # dtes
    # dths
    # surveillance
    # publication
    # delaidiscontinuite
    # delaiabsence
    # essai
    # influence
    # influencecommentaire
    # commentaire

    # remplace
    # stationfille
    # qualifications
    # finalites
    # loisstat
    # images
    # rolecontact
    # stationattachee
    # plageutilisation

    typestation = _composant.Nomenclatureitem(nomenclature=531)

    def __init__(
        self, code, codeh2=None, typestation='LIMNI', libelle=None,
        libellecomplement=None, niveauaffichage=0, coord=None, capteurs=None,
        commune=None, ddcs=None, strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(10)) = code hydro
            codeh2 (string(8)) = ancien code hydro2
            typestation (string parmi NOMENCLATURE[531], defaut LIMNI)
            libelle (string)
            libellecomplement (string)
            niveauaffichage (int) = niveau d'affichage
            coord (list ou dict) =
                (x, y, proj) ou {'x': x, 'y': y, 'proj': proj}
                avec proj (int parmi NOMENCLATURE[22]) = systeme de projection
            capteurs (un Capteur ou un iterable de Capteur)
            commune (string(5)) = code INSEE commune
            ddcs (un code string(10) ou un iterable de string(10)) = reseaux de
                mesure SANDRE
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type et du code

        """

        # -- super --
        super(Station, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle,
            coord=coord, strict=strict
        )

        # -- adjust the descriptor --
        vars(Station)['typestation'].strict = self._strict

        # -- simple properties --
        self.libellecomplement = unicode(libellecomplement) \
            if (libellecomplement is not None) else None

        # -- descriptors --
        self.typestation = typestation

        # -- full properties --
        self._niveauaffichage = 0
        self.niveauaffichage = niveauaffichage
        self._capteurs = []
        self.capteurs = capteurs
        self._commune = None
        self.commune = commune
        self._ddcs = []
        self.ddcs = ddcs

    # -- property niveauaffichage --
    @property
    def niveauaffichage(self):
        """Return niveau d'affichage."""
        return self._niveauaffichage

    @niveauaffichage.setter
    def niveauaffichage(self, niveauaffichage):
        """Set niveau d'affichage."""
        # FIXME - Bd Hydro requires one of (0 111 191 311 391 511 591 911 991)
        #         but it is not a SANDRE nomencature
        self._niveauaffichage = int(niveauaffichage)

    # -- property capteurs --
    @property
    def capteurs(self):
        """Return capteurs."""
        return self._capteurs

    @capteurs.setter
    def capteurs(self, capteurs):
        """Set capteurs."""
        self._capteurs = []
        # None case
        if capteurs is None:
            return
        # one capteur, we make a list with it
        if isinstance(capteurs, Capteur):
            capteurs = [capteurs]
        # an iterable of capteurs
        for capteur in capteurs:
            # some checks
            if self._strict:
                if not isinstance(capteur, Capteur):
                    raise TypeError(
                        'capteurs must be a Capteur or an iterable of Capteur'
                    )
                elif capteur.typemesure not in \
                        _STATION_ACCEPTED_CAPTEUR[self.typestation]:
                    raise ValueError(
                        '{0} capteur forbidden for {1} station'.format(
                            capteur.typemesure, self.typestation
                        )
                    )
            # add capteur
            self._capteurs.append(capteur)

    # -- property commune --
    @property
    def commune(self):
        """Return code commune."""
        return self._commune

    @commune.setter
    def commune(self, commune):
        """Set code commune."""
        if commune is not None:
            commune = unicode(commune)
            _composant.is_code_insee(commune, length=5, errors='strict')
        self._commune = commune

    # -- property ddcs --
    @property
    def ddcs(self):
        """Return ddcs."""
        return self._ddcs

    @ddcs.setter
    def ddcs(self, ddcs):
        """Set ddcs."""
        self._ddcs = []
        # None case
        if ddcs is None:
            return
        # one ddc, we make a list with it
        if not hasattr(ddcs, '__iter__'):
            ddcs = [ddcs]
        # an iterable of ddcs
        for ddc in ddcs:
            ddc = unicode(ddc)
            # if len(ddc) != 10:
            if len(ddc) > 10:
                raise ValueError('ddc code must be 10 chars long')
            self._ddcs.append(ddc)

    # -- special methods --
    __all__attrs__ = (
        'code', 'codeh2', 'typestation', 'libelle', 'libellecomplement',
        'niveauaffichage', 'coord', 'capteurs', 'commune', 'ddcs',
    )

    def __unicode__(self):
        """Return unicode representation."""
        return 'Station {0} {1}::{2} [{3} capteur{4}]'.format(
            self.typestation or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.capteurs),
            '' if (len(self.capteurs) < 2) else 's'
        )

    __str__ = _composant.__str__


# -- class Capteur ------------------------------------------------------------
class Capteur(_Entitehydro):

    """Classe Capteur.

    Classe pour manipuler des capteurs hydrometriques.

    Proprietes:
        code (string(12)) = code hydro
        codeh2 (string(8)) = ancien code hydro2
        typemesure (caractere parmi NOMENCLATURE[520]) = H ou Q
        libelle (string)

    """

    # Capteur other properties

    # station

    # mnemonique
    # typecapteur
    # surveillance
    # dtmaj
    # pdt
    # essai
    # commentaire

    # plageutilisation
    # observateur

    typemesure = _composant.Nomenclatureitem(nomenclature=520)

    def __init__(
        self, code, codeh2=None, typemesure='H', libelle=None,
        strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(12)) = code hydro
            codeh2 (string(8)) = ancien code hydro2
            typemesure (caractere parmi NOMENCLATURE[520], defaut H) = H ou Q
            libelle (string)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du code et du type de mesure

        """

        # -- super --
        super(Capteur, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle, strict=strict
        )

        # -- adjust the descriptor --
        vars(Capteur)['typemesure'].strict = self._strict

        # -- descriptors --
        self.typemesure = typemesure

    # -- special methods --
    __all__attrs__ = ('code', 'codeh2', 'typemesure', 'libelle')
    # __eq__ = _composant.__eq__
    # __ne__ = _composant.__ne__

    def __unicode__(self):
        """Return unicode representation."""
        return 'Capteur {0} {1}::{2}'.format(
            self.typemesure or '<sans type de mesure>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>'
        )

    __str__ = _composant.__str__


# -- class Tronconvigilance ---------------------------------------------------
class Tronconvigilance(object):

    """Classe Tronconvigilance.

    Classe pour manipuler les troncons de vigilance.

    Proprietes:
        code (string(8)) = code alphanumerique du troncon
        libelle (string) = libelle du troncon

    """

    def __init__(self, code=None, libelle=None):
        """Initialisation.

        Arguments:
            code (string(8)) = code alphanumerique du troncon
            libelle (string) = libelle du troncon

        """
        self.code = unicode(code) if (code is not None) else None
        self.libelle = unicode(libelle) if (libelle is not None) else None

    # -- special methods --
    __all__attrs__ = ('code', 'libelle')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__

    def __unicode__(self):
        """Return unicode representation."""
        return 'Troncon de vigilance {0}::{1}'.format(
            self.code or '<sans code>',
            self.libelle or '<sans libelle>'
        )

    __str__ = _composant.__str__


# -- config -------------------------------------------------------------------
# -- HYDRO ENTITY _ARTICLE --
_ARTICLE = {
    # classe name: article
    Sitehydro: 'le',
    Station: 'la',
    Capteur: 'le'
}

# -- HYDRO CODE LENGTH --
_CODE_HYDRO_LENGTH = {
    # class name: hydro code length
    Sitehydro: 8,
    Station: 10,
    Capteur: 12
}

# -- HYDRO ENTITY DEPEDENCY RULES --
# rules for checking which Station a Sitehydro does accept
_SITE_ACCEPTED_STATION = {
    # type site : [type station, ...]
    'REEL': ('LIMNI', 'DEB', 'HC', 'LIMNIMERE', 'LIMNIFILLE'),
    'SOURCE':  ('LIMNI', 'DEB', 'HC', 'LIMNIMERE', 'LIMNIFILLE'),
    'MAREGRAPHE': ('LIMNI',),
    'PLANDEAU': ('LIMNI',),
    'FICTIF': tuple(),
    'PONCTUEL': tuple(),
    'VIRTUEL': tuple(),
    'RECONSTITUE': tuple()
}
# rules for checking which Capteur a Station does accept
_STATION_ACCEPTED_CAPTEUR = {
    'LIMNI': ('H',),
    'DEB': ('H', 'Q'),
    'HC': tuple(),
    'LIMNIMERE': ('H',),
    'LIMNIFILLE': ('H',)
}

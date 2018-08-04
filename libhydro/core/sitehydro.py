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
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

from . import _composant, _composant_site, sitemeteo as _sitemeteo
from libhydro.core.nomenclature import NOMENCLATURE as _NOMENCLATURE


# -- strings ------------------------------------------------------------------
# contributor Camillo Montes (SYNAPSE)
# contributor Sébastien ROMON
__version__ = '0.4.4'
__date__ = '2017-09-22'

# HISTORY
# SR add typecapteur to Capteur
# V 0.4.4 - SR - 2017-09-22
# add entitehydro, zonehydro, tronconhydro and precisioncoursdeau to Site
# V 0.4.3 - SR - 2017-09-05
# add plages to Station
# V 0.4.2 - SR -2017-07-18
# add descriptif,dtmaj,dtmiseservice, dtfermeture,surveillance properties
# to class Station
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
        self.libelle = str(libelle) if (libelle is not None) else None

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
                code = str(code)
                if self._strict and (self.__class__ in _CODE_HYDRO_LENGTH):
                    # check code hydro
                    _composant.is_code_hydro(
                        code=code, errors='strict',
                        length=_CODE_HYDRO_LENGTH[self.__class__])

            # all is well
            self._code = code

        except Exception:
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
                code = str(code)
                _composant.is_code_hydro(code, 8, errors='strict')

            # all is well
            self._codeh2 = code

        except Exception:
            raise

    # -- special methods --
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__


# -- class _Site_or_station --------------------------------------------------
class _Site_or_station(_Entitehydro):

    """Abstract base class for Sitehydro and Station.

    Properties:
        -- properties of _Entitehydro     --
        -- properties of _composant.Coord --

    """

    def __init__(self, code, codeh2=None, libelle=None, coord=None,
                 strict=True):
        """Constructor.

        Arguments:
            -- args of _Entitehydro --
            coord (liste ou dict) = (x, y, proj) ou
                {'x': x, 'y': y, 'proj': proj}

        """

        # -- super --
        super(_Site_or_station, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle, strict=strict)

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


# -- class Sitehydroattache
class Sitehydroattache(object):
    """Classe Sitehydroattache.

    Classe pour manipuler des sites hydrometriques attachés.

    Proprietes:
        code (string(8)) = code hydro
        ponderation = pondération du site
        decalage = décalage en minutes de l'hydrogramme
        dtdeb = date de début
        dtfin = date de fin
        dtdebactivation = date de début d'activation
        dtfinactivation = date de fin d'activation
    """

    dtdeb = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)
    dtdebactivation = _composant.Datefromeverything(required=False)
    dtfinactivation = _composant.Datefromeverything(required=False)

    def __init__(self, sitehydro=None, ponderation=None, decalage=None,
                 dtdeb=None, dtfin=None, dtdebactivation=None,
                 dtfinactivation=None):
        """Constructor.

        Arguments:
            code (string(8)) = code hydro
            ponderation = pondération du site
            decalage = décalage en minutes de l'hydrogramme
            dtdeb = date de début
            dtfin = date de fin
            dtdebactivation = date de début d'activation
            dtfinactivation = date de fin d'activation
        """
        self.dtdeb = dtdeb
        self.dtfin = dtfin
        self.dtdebactivation = dtdebactivation
        self.dtfinactivation = dtfinactivation

        self._sitehydro = None
        self.sitehydro = sitehydro
        self._ponderation = None
        self.ponderation = ponderation
        self._decalage = None
        self.decalage = decalage

    # -- property sitehydro --
    @property
    def sitehydro(self):
        """Return sitehydro."""
        return self._sitehydro

    @sitehydro.setter
    def sitehydro(self, sitehydro):
        """Set sitehydro."""
        # None case
        if not isinstance(sitehydro, Sitehydro):
            raise TypeError('sitehydro must be a Sitehydro')
        self._sitehydro = sitehydro

    # -- property ponderation --
    @property
    def ponderation(self):
        """Return ponderation."""
        return self._ponderation

    @ponderation.setter
    def ponderation(self, ponderation):
        """Set ponderation."""
        # None case
        if ponderation is None:
            self._ponderation = None
        else:
            self._ponderation = float(ponderation)

    # -- property decalage --
    @property
    def decalage(self):
        """Return decalage."""
        return self._decalage

    @decalage.setter
    def decalage(self, decalage):
        """Set decalage."""
        # None case
        if decalage is None:
            self._decalage = None
        else:
            self._decalage = int(decalage)

    # -- special methods --
    __all__attrs__ = (
        'code', 'ponderation', 'decalage', 'dtdeb', 'dtfin',
        'dtdebactivation', 'dtfinactivation')

    def __unicode__(self):
        """Return unicode representation."""
        decalage = '{0} minutes'.format(self.decalage) \
            if self.decalage is not None else '<sans décalage>'
        return 'Site attaché {0} de pondération {1} décalé de {2}'.format(
            self.sitehydro.code or '<sans code>',
            self.ponderation or '<sans libelle>',
            decalage)

    __str__ = _composant.__str__


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
        communes (une liste de _composant_site.Commune) = liste de communes
        entitehydro (string(8) = entité hydrographique
        zonehydro (string(4)) = zone hydrographique
        tronconhydro (string(8)) = troncon hydrographique
        precisioncoursdeau (string) = precision du cours d'eau
        mnemo (string ou None) = mnémo du site
        complementlibelle (string ou None) = complément du libellé
        pkamont (float ou None) = pk amont
        pkaval (float ou None) = pk aval
        altitude (_composant_site.Altitude ou None) = Altitude du site
        dtmaj (datetime.datetime ou None) = Date de mise à jour
        bvtopo (float ou None = bassin versant topologique
        bvhydro (float ou None) = bassin versant hydrologique
        fuseau (int parmi NOMENCLATURE[530]) = fuseau horaire
        statut (int parmi NOMENCLATURE[460]) = statut du site
        dtpremieredonnee (datetime.datetime ou None) =
            date de la première donnée
        moisetiage (int ou None) = mois étiage
        moisanneehydro (int ou None) = mois année hydro
        dureecrues (int ou None) = durée caractéristique des crues
        publication (int parmi NOMENCLATURE[871]) = droit de publication
        essai (bool ou None) = site d'essai
        influence (int parmi NOMENCLATURE[104]) = influende du site
        influencecommentaire (unicode ou None) = commentaire de l'influence
        commentaire (unicode ou None) = commentaire
        siteassocie (Sitehydro ou None) = site associé
        sitesattaches (iterable of Sitehydroattache) = sites attachés
        massedeau (unidoe ou None) = masse d'eau
        loisstat (iterable of _composant_site.LoiStat = lois statistiques
        entitesvigicrues (iterable of _composant_site.EntiteVigiCrues) =
            entités de vigilance crues
        lamesdeau (iterable of SitemeteoPondere) = lames d'eau associées
        sitesamont (iterable of Sitehydro) = sites hydro amont
        sitesaval (iterbale of Sitehydro) = sites hydro aval
    """

    # Sitehydro other properties

    # ponctuel
    # images
    # rolecontact

    typesite = _composant.Nomenclatureitem(nomenclature=530)
    statut = _composant.Nomenclatureitem(nomenclature=460, required=False)
    publication = _composant.Nomenclatureitem(nomenclature=871, required=False)
    influence = _composant.Nomenclatureitem(nomenclature=104, required=False)
    dtmaj = _composant.Datefromeverything(required=False)
    dtpremieredonnee = _composant.Datefromeverything(required=False)

    def __init__(self, code, codeh2=None, typesite='REEL', libelle=None,
                 libelleusuel=None, coord=None, stations=None, communes=None,
                 entitehydro=None, zonehydro=None,
                 tronconhydro=None, precisioncoursdeau=None, mnemo=None,
                 complementlibelle=None, pkamont=None, pkaval=None,
                 altitude=None, dtmaj=None, bvtopo=None,
                 bvhydro=None, fuseau=None, statut=None,
                 dtpremieredonnee=None, moisetiage=None,
                 moisanneehydro=None, dureecrues=None, publication=None,
                 essai=None, influence=None, influencecommentaire=None,
                 commentaire=None, siteassocie=None, sitesattaches=None,
                 massedeau=None, loisstat=None, entitesvigicrues=None,
                 lamesdeau=None, sitesamont=None, sitesaval=None,
                 strict=True):
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
            communes (a _composant_site.Commune
                or an iterable of _composant_site.Commune))
            entitehydro (string(8) = entité hydrographique
            zonehydro (string(4)) = zone hydrographique
            tronconhydro (string(8)) = troncon hydrographique
            precisioncoursdeau (string) = precision du cours d'eau
            mnemo (string ou None) = mnémo du site
            complementlibelle (string ou None) = complément du libellé
            pkamont (float ou None) = pk amont
            pkaval (float ou None) = pk aval
            altitude (_composant_site.Altitude ou None) = Altitude du site
            dtmaj (datetime.datetime ou None) = Date de mise à jour
            bvtopo (float ou None = bassin versant topologique
            bvhydro (float ou None) = bassin versant hydrologique
            fuseau (int parmi NOMENCLATURE[530]) = fuseau horaire
            statut (int parmi NOMENCLATURE[460]) = statut du site
            dtpremieredonnee (datetime.datetime ou None) =
                date de la première donnée
            moisetiage (int ou None) = mois étiage
            moisanneehydro (int ou None) = mois année hydro
            dureecrues (int ou None) = durée caractéristique des crues
            publication (int parmi NOMENCLATURE[871]) = droit de publication
            essai (bool ou None) = site d'essai
            influence (int parmi NOMENCLATURE[104]) = influende du site
            influencecommentaire (unicode ou None) = commentaire de l'influence
            commentaire (unicode ou None) = commentaire
            siteassocie (Sitehydro ou None) = site associé
            sitesattaches (iterable of Sitehydroattache) = sites attachés
            massedeau (unidoe ou None) = masse d'eau
            loisstat (iterable of _composant_site.LoiStat = lois statistiques
            entitesvigicrues (iterable of _composant_site.EntiteVigiCrues) =
                entités de vigilance crues
            lamesdeau (iterable of SitemeteoPondere) = lames d'eau associées
            sitesamont (iterable of Sitehydro) = sites hydro amont
            sitesaval (iterbale of Sitehydro) = sites hydro aval
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type, du code et des stations

        """

        # -- super --
        super(Sitehydro, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle,
            coord=coord, strict=strict)

        # -- adjust the descriptor --
        vars(Sitehydro)['typesite'].strict = self._strict

        # -- simple properties --
        self.libelleusuel = str(libelleusuel) \
            if (libelleusuel is not None) else None
        self.precisioncoursdeau = str(precisioncoursdeau) \
            if (precisioncoursdeau is not None) else None
        self.mnemo = str(mnemo) if mnemo is not None else None
        self.complementlibelle = str(complementlibelle) \
            if (complementlibelle is not None) else None
        self.influencecommentaire = str(influencecommentaire) \
            if (influencecommentaire is not None) else None
        self.commentaire = str(commentaire) \
            if (commentaire is not None) else None
        self.massedeau = str(massedeau) \
            if (massedeau is not None) else None

        # -- descriptors --
        self.typesite = typesite
        self.dtmaj = dtmaj
        self.statut = statut
        self.publication = publication
        self.influence = influence
        self.dtpremieredonnee = dtpremieredonnee

        # -- full properties --
        self._stations = self._communes = []
        self.stations = stations
        self.communes = communes
        self._entitehydro = None
        self.entitehydro = entitehydro
        self._tronconhydro = None
        self.tronconhydro = tronconhydro
        self._zonehydro = None
        self.zonehydro = zonehydro
        self._pkaval = None
        self.pkaval = pkaval
        self._pkamont = None
        self.pkamont = pkamont
        self._altitude = None
        self.altitude = altitude
        self._bvtopo = None
        self.bvtopo = bvtopo
        self._bvhydro = None
        self.bvhydro = bvhydro
        self._fuseau = None
        self.fuseau = fuseau
        self._moisetiage = None
        self.moisetiage = moisetiage
        self._moisanneehydro = None
        self.moisanneehydro = moisanneehydro
        self._dureecrues = None
        self.dureecrues = dureecrues
        self._essai = None
        self.essai = essai
        self._siteassocie = None
        self.siteassocie = siteassocie
        self._sitesattaches = []
        self.sitesattaches = sitesattaches
        self._loisstat = []
        self.loisstat = loisstat
        self._entitesvigicrues = []
        self.entitesvigicrues = entitesvigicrues
        self._lamesdeau = []
        self.lamesdeau = lamesdeau
        self._sitesamont = []
        self.sitesamont = sitesamont
        self._sitesaval = []
        self.sitesaval = sitesaval

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
                            station.typestation, self.typesite))
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
        if isinstance(communes, _composant_site.Commune):
            communes = [communes]
        # an iterable of communes
        for commune in communes:
            if not isinstance(commune, _composant_site.Commune):
                raise TypeError('communes must be a _composant_site.Commune'
                                ' or an iterable of _composant_site.Commune')
            self._communes.append(commune)

    # -- property zonehydro --
    @property
    def zonehydro(self):
        """Return zonehydro."""
        return self._zonehydro

    @zonehydro.setter
    def zonehydro(self, zonehydro):
        """Set zonehydro."""
        self._zonehydro = None
        # None case
        if zonehydro is None:
            return
        zonehydro = str(zonehydro)
        if self._strict and len(zonehydro) != 4:
            raise ValueError(
                'length of zone hydro ({}) must be 4'.format(zonehydro))
        self._zonehydro = zonehydro

    # -- property tronconhydro --
    @property
    def tronconhydro(self):
        """Return tronconhydro."""
        return self._tronconhydro

    @tronconhydro.setter
    def tronconhydro(self, tronconhydro):
        """Set tronconhydro."""
        self._tronconhydro = None
        # None case
        if tronconhydro is None:
            return
        tronconhydro = str(tronconhydro)
        if self._strict and len(tronconhydro) != 8:
            raise ValueError(
                'length of troncon hydro ({}) must be 8'.format(tronconhydro))
        self._tronconhydro = tronconhydro

    # -- property entitehydro --
    @property
    def entitehydro(self):
        """Return zonehydro."""
        return self._entitehydro

    @entitehydro.setter
    def entitehydro(self, entitehydro):
        """Set tronconhydro."""
        self._entitehydro = None
        # None case
        if entitehydro is None:
            return
        entitehydro = str(entitehydro)
        if self._strict and len(entitehydro) != 8:
            raise ValueError(
                'length of entite hydro ({}) must be 8'.format(entitehydro))
        self._entitehydro = entitehydro

    # -- property pkamont --
    @property
    def pkamont(self):
        """Return pkamont."""
        return self._pkamont

    @pkamont.setter
    def pkamont(self, pkamont):
        """Set pkamont."""
        # None case
        if pkamont is None:
            self._pkamont = None
        else:
            self._pkamont = float(pkamont)

    # -- property pkaval --
    @property
    def pkaval(self):
        """Return pkaval."""
        return self._pkaval

    @pkaval.setter
    def pkaval(self, pkaval):
        """Set pkaval."""
        # None case
        if pkaval is None:
            self._pkaval = None
        else:
            self._pkaval = float(pkaval)

    # -- property altitude --
    @property
    def altitude(self):
        """Return altitude."""
        return self._altitude

    @altitude.setter
    def altitude(self, altitude):
        """Set altitude."""
        # None case
        if altitude is None:
            self._altitude = None
        else:
            if not isinstance(altitude, _composant_site.Altitude) \
                    and self._strict:
                raise TypeError('altitude must be a _composant_site.Altitude')
            self._altitude = altitude

    # -- property bvtopo --
    @property
    def bvtopo(self):
        """Return bvtopo."""
        return self._bvtopo

    @bvtopo.setter
    def bvtopo(self, bvtopo):
        """Set bvtopo."""
        # None case
        if bvtopo is None:
            self._bvtopo = None
        else:
            self._bvtopo = float(bvtopo)

    # -- property bvhydro --
    @property
    def bvhydro(self):
        """Return bvhydro."""
        return self._bvhydro

    @bvhydro.setter
    def bvhydro(self, bvhydro):
        """Set bvhydro."""
        # None case
        if bvhydro is None:
            self._bvhydro = None
        else:
            self._bvhydro = float(bvhydro)

    # -- property fuseau --
    @property
    def fuseau(self):
        """Return fuseau."""
        return self._fuseau

    @fuseau.setter
    def fuseau(self, fuseau):
        """Set fuseau."""
        # None case
        # TODO check fuseau
        if fuseau is None:
            self._fuseau = None
        else:
            self._fuseau = int(fuseau)

    # -- property moisetiage --
    @property
    def moisetiage(self):
        """Return moisetiage."""
        return self._moisetiage

    @moisetiage.setter
    def moisetiage(self, moisetiage):
        """Set moisetiage."""
        # None case
        if moisetiage is None:
            self._moisetiage = None
        else:
            self._moisetiage = int(moisetiage)

    # -- property moisanneehydro --
    @property
    def moisanneehydro(self):
        """Return moisanneehydro."""
        return self._moisanneehydro

    @moisanneehydro.setter
    def moisanneehydro(self, moisanneehydro):
        """Set moisanneehydro."""
        # None case
        if moisanneehydro is None:
            self._moisanneehydro = None
        else:
            self._moisanneehydro = int(moisanneehydro)

    # -- property dureecrues --
    @property
    def dureecrues(self):
        """Return dureecrues."""
        return self._dureecrues

    @dureecrues.setter
    def dureecrues(self, dureecrues):
        """Set dureecrues."""
        # None case
        if dureecrues is None:
            self._dureecrues = None
        else:
            self._dureecrues = int(dureecrues)

    # -- property essai --
    @property
    def essai(self):
        """Return essai."""
        return self._essai

    @essai.setter
    def essai(self, essai):
        """Set essai."""
        # None case
        if essai is None:
            self._essai = None
        else:
            self._essai = bool(essai)

    # -- property siteassocie --
    @property
    def siteassocie(self):
        """Return siteassocie."""
        return self._siteassocie

    @siteassocie.setter
    def siteassocie(self, siteassocie):
        """Set siteassocie."""
        # None case
        if siteassocie is None:
            self._siteassocie = None
        else:
            if not isinstance(siteassocie, Sitehydro):
                raise TypeError('siteasocie must be a Sitehydro')
            self._siteassocie = siteassocie

    # -- property sitesattaches --
    @property
    def sitesattaches(self):
        """Return sitesattaches."""
        return self._sitesattaches

    @sitesattaches.setter
    def sitesattaches(self, sitesattaches):
        """Set sitesattaches."""
        self._sitesattaches = []
        # None case
        if sitesattaches is None:
            return
        # one station, we make a list with it
        if isinstance(sitesattaches, Sitehydroattache):
            sitesattaches = [sitesattaches]
        # an iterable of sitesattaches
        for site in sitesattaches:
            # some checks
            if self._strict:
                if not isinstance(site, Sitehydroattache):
                    raise TypeError(
                        'sitesattaches must be a Sitehydroattache'
                        ' or an iterable of Sitehydroattache'
                    )
            # add site1
            self._sitesattaches.append(site)

    # -- property loisstat --
    @property
    def loisstat(self):
        """Return loisstat."""
        return self._loisstat

    @loisstat.setter
    def loisstat(self, loisstat):
        """Set loisstat."""
        self._loisstat = []
        # None case
        if loisstat is None:
            return
        # one station, we make a list with it
        if isinstance(loisstat, _composant_site.LoiStat):
            loisstat = [loisstat]
        # an iterable of loisstat
        for loi in loisstat:
            # some checks
            if self._strict:
                if not isinstance(loi, _composant_site.LoiStat):
                    raise TypeError(
                        'loisstat must be a LoiStat'
                        ' or an iterable of LoiStat'
                    )
            # add site1
            self._loisstat.append(loi)

    # -- property entitesvigicrues --
    @property
    def entitesvigicrues(self):
        """Return entitesvigicrues."""
        return self._entitesvigicrues

    @entitesvigicrues.setter
    def entitesvigicrues(self, entitesvigicrues):
        """Set entitesvigicrues."""
        self._entitesvigicrues = []
        # None case
        if entitesvigicrues is None:
            return
        # one station, we make a list with it
        if isinstance(entitesvigicrues, _composant_site.EntiteVigiCrues):
            entitesvigicrues = [entitesvigicrues]
        # an iterable of entitesvigicrues
        for entite in entitesvigicrues:
            # some checks
            if self._strict:
                if not isinstance(entite, _composant_site.EntiteVigiCrues):
                    raise TypeError(
                        'entitesvigicrues must be a EntiteVigiCrues'
                        ' or an iterable of EntiteVigiCrues'
                    )
            # add site1
            self._entitesvigicrues.append(entite)

    # -- property lamesdeau --
    @property
    def lamesdeau(self):
        """Return lamesdeau."""
        return self._lamesdeau

    @lamesdeau.setter
    def lamesdeau(self, lamesdeau):
        """Set lamesdeau."""
        self._lamesdeau = []
        # None case
        if lamesdeau is None:
            return
        # one station, we make a list with it
        if isinstance(lamesdeau, _sitemeteo.SitemeteoPondere):
            lamesdeau = [lamesdeau]
        # an iterable of lamesdeau
        for lame in lamesdeau:
            # some checks
            if self._strict:
                if not isinstance(lame, _sitemeteo.SitemeteoPondere):
                    raise TypeError(
                        'lamesdeau must be a SitemeteoPondere'
                        ' or an iterable of SitemeteoPondere'
                    )
            # add site1
            self._lamesdeau.append(lame)

    # -- property sitesamont --
    @property
    def sitesamont(self):
        """Return sitesamont."""
        return self._sitesamont

    @sitesamont.setter
    def sitesamont(self, sitesamont):
        """Set sitesamont."""
        # None case
        if sitesamont is None:
            self._sitesamont = []
        else:
            if isinstance(sitesamont, Sitehydro):
                self._sitesamont = [sitesamont]
            else:
                for site in sitesamont:
                    if not isinstance(site, Sitehydro):
                        raise TypeError('sitesamont must be a Sitehydro'
                                        'or an iterbale of Sitehydro')
                self._sitesamont = sitesamont

    # -- property sitesaval --
    @property
    def sitesaval(self):
        """Return sitesaval."""
        return self._sitesaval

    @sitesaval.setter
    def sitesaval(self, sitesaval):
        """Set sitesaval."""
        # None case
        if sitesaval is None:
            self._sitesaval = []
        else:
            if isinstance(sitesaval, Sitehydro):
                self._sitesaval = [sitesaval]
            else:
                for site in sitesaval:
                    if not isinstance(site, Sitehydro):
                        raise TypeError('sitesaval must be a Sitehydro'
                                        'or an iterbale of Sitehydro')
                self._sitesaval = sitesaval

    # -- special methods --
    __all__attrs__ = (
        'code', 'codeh2', 'typesite', 'libelle', 'libelleusuel', 'coord',
        'stations', 'communes', 'entitehydro',
        'zonehydro', 'tronconhydro', 'precisioncoursdeau', 'mnemo',
        'complementlibelle', 'pkamont', 'pkaval',
        'altitude', 'dtmaj', 'bvtopo',
        'bvhydro', 'fuseau', 'statut',
        'dtpremieredonnee', 'moisetiage',
        'moisanneehydro', 'dureecrues', 'publication',
        'essai', 'influence', 'influencecommentaire',
        'commentaire', 'siteassocie', 'sitesattaches',
        'massedeau', 'loisstat', 'entitesvigicrues',
        'lamesdeau', 'sitesamont', 'sitesaval')

    def __unicode__(self):
        """Return unicode representation."""
        return 'Site {0} {1}::{2} [{3} station{4}]'.format(
            self.typesite or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.stations),
            '' if (len(self.stations) < 2) else 's')

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
        descriptif (string)
        niveauaffichage (int) = niveau d'affichage
        coord (Coord) =
            x, y (float)
            proj (int parmi NOMENCLATURE[22]) = systeme de projection
        pointk (float) = point kilomètrique
        dtmiseservice (datetime.datetime) = Date de mise en service
        dtfermeture (datetime.datetime) = Date de fermeture
        surveillance (boolean) = statin à surveiller
        capteurs (une liste de Capteur)
        commune (string(5)) = code INSEE commune
        ddcs (liste de string(10)) = liste de reseaux de mesure SANDRE
            (dispositifs de collecte)
        plages (PlageUtil ou un iterable
            de PlageUtil) = plages d'utilisation

    """

    # Station other properties

    # sitehydro

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

    typestation = _composant.Nomenclatureitem(nomenclature=531)
    dtmaj = _composant.Datefromeverything(required=False)
    dtmiseservice = _composant.Datefromeverything(required=False)
    dtfermeture = _composant.Datefromeverything(required=False)

    def __init__(self, code, codeh2=None, typestation='LIMNI', libelle=None,
                 libellecomplement=None, descriptif=None, dtmaj=None,
                 pointk=None, dtmiseservice=None, dtfermeture=None,
                 surveillance=None, niveauaffichage=0,
                 coord=None, capteurs=None, commune=None, ddcs=None,
                 plages=None, strict=True):
        """Initialisation.

        Arguments:
            code (string(10)) = code hydro
            codeh2 (string(8)) = ancien code hydro2
            typestation (string parmi NOMENCLATURE[531], defaut LIMNI)
            libelle (string)
            libellecomplement (string)
            descriptif (string)
            dtmaj (datetime.datetime)
            niveauaffichage (int) = niveau d'affichage
            coord (list ou dict) =
                (x, y, proj) ou {'x': x, 'y': y, 'proj': proj}
                avec proj (int parmi NOMENCLATURE[22]) = systeme de projection
            pointk (float) = point kilomètrique
            dtmiseservice (datetime.datetime) = Date de mise en service
            dtfermeture (datetime.datetime) = Date de fermeture
            surveillance (boolean) = statin à surveiller
            capteurs (un Capteur ou un iterable de Capteur)
            commune (string(5)) = code INSEE commune
            ddcs (un code string(10) ou un iterable de string(10)) = reseaux de
                mesure SANDRE
            plages (PlageUtil ou un iterable
                de PlageUtil) = plages d'utilisation
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type et du code

        """

        # -- super --
        super(Station, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle,
            coord=coord, strict=strict)

        # -- adjust the descriptor --
        vars(Station)['typestation'].strict = self._strict

        # -- simple properties --
        self.libellecomplement = str(libellecomplement) \
            if (libellecomplement is not None) else None

        self.descriptif = str(descriptif) \
            if descriptif is not None else None
        # -- descriptors --
        self.typestation = typestation
        self.dtmaj = dtmaj
        self.dtmiseservice = dtmiseservice
        self.dtfermeture = dtfermeture
        # -- full properties --
        self._niveauaffichage = 0
        self.niveauaffichage = niveauaffichage
        self._pointk = None
        self.pointk = pointk
        self._surveillance = None
        self.surveillance = surveillance
        self._capteurs = []
        self.capteurs = capteurs
        self._commune = None
        self.commune = commune
        self._ddcs = []
        self.ddcs = ddcs
        self._plages = []
        self.plages = plages

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

    # -- property pointk --
    @property
    def pointk(self):
        """Return pointk."""
        return self._pointk

    @pointk.setter
    def pointk(self, pointk):
        """Set pointk."""
        self._pointk = None
        if pointk is None:
            return
        self._pointk = float(pointk)

    # -- property surveillance --
    @property
    def surveillance(self):
        """Return surveillance."""
        return self._surveillance

    @surveillance.setter
    def surveillance(self, surveillance):
        """Set pointk."""
        self._surveillance = None
        if surveillance is None:
            return
        self._surveillance = bool(surveillance)

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
                        'capteurs must be a Capteur or an iterable of Capteur')
                elif capteur.typemesure not in \
                        _STATION_ACCEPTED_CAPTEUR[self.typestation]:
                    raise ValueError(
                        '{0} capteur forbidden for {1} station'.format(
                            capteur.typemesure, self.typestation))
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
            commune = str(commune)
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
        # python3 strings are iterable
        if isinstance(ddcs, (str, bytes)):
            ddcs = [ddcs]
        # an iterable of ddcs
        for ddc in ddcs:
            ddc = str(ddc)
            # if len(ddc) != 10:
            if len(ddc) > 10:
                raise ValueError('ddc code must be 10 chars long')
            self._ddcs.append(ddc)

    # -- property plages --
    @property
    def plages(self):
        """Return plages."""
        return self._plages

    @plages.setter
    def plages(self, plages):
        """Set plages."""
        self._plages = []
        # None case
        if plages is None:
            return
        # one ddc, we make a list with it
        if not hasattr(plages, '__iter__'):
            plages = [plages]
        # an iterable of PlageUtil
        for plage in plages:
            if self._strict and not isinstance(plage, PlageUtil):
                raise TypeError('plages utilisation is not'
                                ' a PlageUtil'
                                ' or an iterable of PlageUtil ')
            self._plages.append(plage)

    # -- special methods --
    __all__attrs__ = (
        'code', 'codeh2', 'typestation', 'libelle', 'libellecomplement',
        'descriptif',
        'niveauaffichage', 'coord', 'capteurs', 'commune', 'ddcs',
        'plages')

    def __unicode__(self):
        """Return unicode representation."""
        return 'Station {0} {1}::{2} [{3} capteur{4}]'.format(
            self.typestation or '<sans type>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.capteurs),
            '' if (len(self.capteurs) < 2) else 's')

    __str__ = _composant.__str__


# -- class Capteur ------------------------------------------------------------
class Capteur(_Entitehydro):

    """Classe Capteur.

    Classe pour manipuler des capteurs hydrometriques.

    Proprietes:
        code (string(12)) = code hydro
        codeh2 (string(8)) = ancien code hydro2
        typemesure (caractere parmi NOMENCLATURE[520]) = H ou Q
        typecapteur (int parmi NOMENCLATURE[519])
        libelle (string)
        plages (PlageUtil ou un iterable
            de PlageUtil ou None) = plages d'utilisation

    """

    # Capteur other properties

    # station

    # mnemonique

    # surveillance
    # dtmaj
    # pdt
    # essai
    # commentaire

    # observateur

    typemesure = _composant.Nomenclatureitem(nomenclature=520)
    typecapteur = _composant.Nomenclatureitem(nomenclature=519)

    def __init__(self, code, codeh2=None, typemesure='H', libelle=None,
                 typecapteur=0,
                 plages=None, strict=True):
        """Initialisation.

        Arguments:
            code (string(12)) = code hydro
            codeh2 (string(8)) = ancien code hydro2
            typemesure (caractere parmi NOMENCLATURE[520], defaut H) = H ou Q
            typecapteur (int parmi NOMENCLATURE[519])
            libelle (string)
            plages (PlageUtil ou un iterable
                de PlageUtil ou None) = plages d'utilisation
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du code et du type de mesure

        """

        # -- super --
        super(Capteur, self).__init__(
            code=code, codeh2=codeh2, libelle=libelle, strict=strict)

        # -- adjust the descriptor --
        vars(Capteur)['typemesure'].strict = self._strict

        # -- descriptors --
        self.typemesure = typemesure
        self.typecapteur = typecapteur

        self._plages = []
        self.plages = plages

    # TODO plages utilisation communes aux stations et capteurs
    # -- property plages --
    @property
    def plages(self):
        """Return plages."""
        return self._plages

    @plages.setter
    def plages(self, plages):
        """Set plages."""
        self._plages = []
        # None case
        if plages is None:
            return
        # one ddc, we make a list with it
        if not hasattr(plages, '__iter__'):
            plages = [plages]
        # an iterable of PlageUtil
        for plage in plages:
            if self._strict and not isinstance(plage, PlageUtil):
                raise TypeError('plages utilisation is not'
                                ' a PlageUtil'
                                ' or an iterable of PlageUtil ')
            self._plages.append(plage)

    # -- special methods --
    __all__attrs__ = ('code', 'codeh2', 'typemesure', 'libelle',
                      'typecapteur',
                      'plages')
    # __eq__ = _composant.__eq__
    # __ne__ = _composant.__ne__

    def __unicode__(self):
        """Return unicode representation."""
        return 'Capteur de type {0} {1} {2}::{3}'.format(
            _NOMENCLATURE[519][self.typecapteur].lower(),
            self.typemesure or '<sans type de mesure>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>')

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
        self.code = str(code) if (code is not None) else None
        self.libelle = str(libelle) if (libelle is not None) else None

    # -- special methods --
    __all__attrs__ = ('code', 'libelle')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__

    def __unicode__(self):
        """Return unicode representation."""
        return 'Troncon de vigilance {0}::{1}'.format(
            self.code or '<sans code>',
            self.libelle or '<sans libelle>')

    __str__ = _composant.__str__


class PlageUtil(object):
    """Classe  PlageUtil.

    Classe pour manipuler les plages d'activations des capteurs et stations.

    Proprietes:
        dteb (datetime.datetime) = date de début
        dtfin (datetime.datetime or None) = datefin
        dtactivation (datetime.datetime or None) = date d'activation
        dtdesactivation (datetime.datetime or None) = date de desactivation
        active (bool or None) = True plage activé

    """
    dtdeb = _composant.Datefromeverything(required=True)
    dtfin = _composant.Datefromeverything(required=False)
    dtactivation = _composant.Datefromeverything(required=False)
    dtdesactivation = _composant.Datefromeverything(required=False)

    def __init__(self, dtdeb=None, dtfin=None,
                 dtactivation=None, dtdesactivation=None,
                 active=True):
        """Initialisation."""
        self.dtdeb = dtdeb
        self.dtfin = dtfin
        self.dtactivation = dtactivation
        self.dtdesactivation = dtdesactivation

        self._active = None
        self.active = active

    # -- property active --
    @property
    def active(self):
        """Return active."""
        return self._active

    @active.setter
    def active(self, active):
        if active is None:
            self._active = active
            return
        self._active = bool(active)

    # -- special methods --
    __all__attrs__ = ('dtdeb', 'dtfin', 'dtactivation', 'dtdesactivation',
                      'active')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        if self.active is None:
            active = '<sans active>'
        elif self.active:
            active = 'active'
        else:
            active = 'inactive'
        return 'Plage d\'utilisation {0} [{1} - {2}]'.format(
            active,
            self.dtdeb,
            self.dtfin if self.dtfin is not None else '<sans date de fin>')

    __str__ = _composant.__str__


# -- config -------------------------------------------------------------------
# -- HYDRO ENTITY _ARTICLE --
_ARTICLE = {
    # classe name: article
    Sitehydro: 'le',
    Station: 'la',
    Capteur: 'le'}

# -- HYDRO CODE LENGTH --
_CODE_HYDRO_LENGTH = {
    # class name: hydro code length
    Sitehydro: 8,
    Sitehydroattache: 8,
    Station: 10,
    Capteur: 12}

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
    'RECONSTITUE': tuple()}
# rules for checking which Capteur a Station does accept
_STATION_ACCEPTED_CAPTEUR = {
    'LIMNI': ('H',),
    'DEB': ('H', 'Q'),
    'HC': tuple(),
    'LIMNIMERE': ('H',),
    'LIMNIFILLE': ('H',)}

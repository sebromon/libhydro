# coding: utf-8
"""Module sitemeteo.

Ce module contient les classes:
    # Sitemeteo
    # Grandeur
    # Visite - not implemented
    # Classequalite - not implemented

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from . import (_composant, _composant_site, rolecontact as _rolecontact,
               intervenant as _intervenant)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.3b"""
__date__ = """2017-09-19"""

# HISTORY
# V0.3b -SR - 2017-09-19
# Add pdt to grandeur meteo
# V0.3 - 2014-12-17
#   change the __eq__ and __ne__ methods
# V0.1 - 2014-07-07
#   first shot


# -- todos --------------------------------------------------------------------
# PROGRESS - Sitemeteo 50% - Grandeur 10% - Visite 0% - Classequalite 0%


# -- class Sitemeteo ----------------------------------------------------------
class Sitemeteo(object):

    """Classe Sitemeteo.

    Classe pour manipuler des sites meteorologiques.

    Proprietes:
        code (string(9)) = code INSEE. Un code de 8 caracteres est prefixe
            d'un zero
        libelle (string ou None) = libellé
        libelleusuel (string ou None) = libellé usuel
        mnemo (str ou None) = Mnémonique
        lieudit (str ou None) = lieu-dit
        coord (list ou dict) =
            (x, y, proj) ou {'x': x, 'y': y, 'proj': proj}
            avec proj (int parmi NOMENCLATURE[22]) = systeme de projection
        altitude (_composant_site.Altitude) = altitude du site
        fuseau (int) = fuseau horaire
        dtmaj (datetime.datetime) = date de mise à jour
        dtouverture (datetime.datetime) = date d'ouverture
        dtfermeture (datetime.datetime) = date de fermeture
        droitpublication (bool) = publication publiques
        essai (bool ou None) = site d'essai
        commentaire (str ou None) = commentaire
        reseaux (_composant_site.ReseauMesure
            or iterable of _composant_site.ReseauMesure)
            = réseaux de mesure
        roles (rolecontact.RoleContact or iterable
            of rolecontact.RoleContact) = roles des contacts
        zonehydro (str(4) ou None) = zone hydro
        commune (string(5) ou None) = code INSEE commune
        grandeurs (une liste de Grandeur) = grandeurs du site
        visites (Visite or iterable of Visite) = visites deu site
        strict (bool, defaut True) = le mode permissif permet de lever les
            controles de validite du code et des grandeurs

    """

    # Sitemeteo other properties
    # images

    dtmaj = _composant.Datefromeverything(required=False)
    dtouverture = _composant.Datefromeverything(required=False)
    dtfermeture = _composant.Datefromeverything(required=False)

    def __init__(
        self, code, libelle=None, libelleusuel=None, mnemo=None, lieudit=None,
        coord=None, altitude=None, fuseau=None, dtmaj=None, dtouverture=None,
        dtfermeture=None, droitpublication=None, essai=None, commentaire=None,
        reseaux=None, roles=None, zonehydro=None, commune=None,
        grandeurs=None, visites=None, strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(9)) = code INSEE. Un code de 8 caracteres est prefixe
                d'un zero
            libelle (string ou None) = libellé
            libelleusuel (string ou None) = libellé usuel
            mnemo (str ou None) = Mnémonique
            lieudit (str ou None) = lieu-dit
            coord (list ou dict) =
                (x, y, proj) ou {'x': x, 'y': y, 'proj': proj}
                avec proj (int parmi NOMENCLATURE[22]) = systeme de projection
            altitude (_composant_site.Altitude) = altitude du site
            fuseau (int) = fuseau horaire
            dtmaj (datetime.datetime) = date de mise à jour
            dtouverture (datetime.datetime) = date d'ouverture
            dtfermeture (datetime.datetime) = date de fermeture
            droitpublication (bool) = publication publiques
            essai (bool ou None) = site d'essai
            commentaire (str ou None) = commentaire
            reseaux (_composant_site.ReseauMesure
                or iterable of _composant_site.ReseauMesure)
                = réseaux de mesure
            roles (rolecontact.RoleContact or iterable
                of rolecontact.RoleContact) = roles des contacts
            zonehydro (str(4) ou None) = zone hydro
            commune (string(5) ou None) = code INSEE commune
            grandeurs (une liste de Grandeur) = grandeurs du site
            visites (Visite or iterable of Visite) = visites deu site
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du code et des grandeurs

        """

        # -- simple properties --
        self._strict = bool(strict)
        self.libelle = str(libelle) \
            if (libelle is not None) else None
        self.libelleusuel = str(libelleusuel) \
            if (libelleusuel is not None) else None
        self.mnemo = str(mnemo) if mnemo is not None else None
        self.lieudit = str(lieudit) if lieudit is not None else None
        self.commentaire = str(commentaire) \
            if (commentaire is not None) else None

        self.dtmaj = dtmaj
        self.dtouverture = dtouverture
        self.dtfermeture = dtfermeture

        # -- full properties --
        self._code = self._coord = self._commune = self._altitude = None
        self._grandeurs = []
        self.code = code
        self.coord = coord
        self.commune = commune
        self.grandeurs = grandeurs
        self.altitude = altitude
        self._fuseau = None
        self.fuseau = fuseau
        self._droitpublication = None
        self.droitpublication = droitpublication
        self._essai = None
        self.essai = essai
        self._reseaux = []
        self.reseaux = reseaux
        self._roles = []
        self.roles = roles
        self._zonehydro = None
        self.zonehydro = zonehydro
        self._visites = []
        self.visites = visites

    # -- property code --
    @property
    def code(self):
        """Return code INSEE."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code INSEE."""
        try:
            if code is None:
                # None case
                if self._strict:
                    raise TypeError('code is required')

            else:
                # other cases
                code = str(code)
                if self._strict:
                    if len(code) == 8:
                        code = '0{}'.format(code)
                    _composant.is_code_insee(
                        code=code, length=9, errors='strict'
                    )

            # all is well
            self._code = code

        except:
            raise

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

    # -- property droitpublication --
    @property
    def droitpublication(self):
        """Return droitpublication."""
        return self._droitpublication

    @droitpublication.setter
    def droitpublication(self, droitpublication):
        """Set droitpublication."""
        # None case
        # TODO check droitpublication
        if droitpublication is None:
            self._droitpublication = None
        else:
            self._droitpublication = bool(droitpublication)

    # -- property essai --
    @property
    def essai(self):
        """Return essai."""
        return self._essai

    @essai.setter
    def essai(self, essai):
        """Set essai."""
        # None case
        # TODO check essai
        if essai is None:
            self._essai = None
        else:
            self._essai = bool(essai)

    # -- property reseaux --
    @property
    def reseaux(self):
        """Return reseaux."""
        return self._reseaux

    @reseaux.setter
    def reseaux(self, reseaux):
        """Set reseaux."""
        self._reseaux = []
        # None case
        if reseaux is None:
            return
        # one grandeur, we make a list with it
        if isinstance(reseaux, _composant_site.ReseauMesure):
            reseaux = [reseaux]
        # an iterable of reseaux
        for reseau in reseaux:
            # some checks
            if self._strict:
                if not isinstance(reseau, _composant_site.ReseauMesure):
                    raise TypeError(
                        'reseaux must be a ReseauMesure or an iterable '
                        'of ReseauMesure'
                    )
            # add capteur
            self._reseaux.append(reseau)

    # -- property roles --
    @property
    def roles(self):
        """Return roles."""
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Set roles."""
        self._roles = []
        # None case
        if roles is None:
            return
        # one role, we make a list with it
        if isinstance(roles, _rolecontact.RoleContact):
            roles = [roles]
        # an iterable of roles
        for role in roles:
            # some checks
            if self._strict:
                if not isinstance(role, _rolecontact.RoleContact):
                    raise TypeError(
                        'roles must be a RoleContact or an iterable '
                        'of RoleContact'
                    )
            # add role
            self._roles.append(role)

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

    # -- property visites --
    @property
    def visites(self):
        """Return visites."""
        return self._visites

    @visites.setter
    def visites(self, visites):
        """Set visites."""
        self._visites = []
        # None case
        if visites is None:
            return
        # one grandeur, we make a list with it
        if isinstance(visites, Visite):
            visites = [visites]
        # an iterable of visites
        for visite in visites:
            # some checks
            if self._strict:
                if not isinstance(visite, Visite):
                    raise TypeError(
                        'visites must be a Visite or an iterable '
                        'of Visite'
                    )
            # add capteur
            self._visites.append(visite)


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

    # -- property grandeurs --
    @property
    def grandeurs(self):
        """Return grandeurs."""
        return self._grandeurs

    @grandeurs.setter
    def grandeurs(self, grandeurs):
        """Set grandeurs."""
        self._grandeurs = []
        # None case
        if grandeurs is None:
            return
        # one grandeur, we make a list with it
        if isinstance(grandeurs, Grandeur):
            grandeurs = [grandeurs]
        # an iterable of grandeurs
        for grandeur in grandeurs:
            # some checks
            if self._strict:
                if not isinstance(grandeur, Grandeur):
                    raise TypeError(
                        'grandeurs must be a Grandeur or an iterable '
                        'of Grandeur'
                    )
            # add capteur
            self._grandeurs.append(grandeur)

    # -- special methods --
    __all__attrs__ = (
        'code', 'libelle', 'libelleusuel', 'coord', 'commune', 'grandeurs',
        'mnemo', 'lieudit', 'altitude', 'fuseau', 'dtmaj', 'dtouverture',
        'dtfermeture', 'droitpublication', 'essai', 'commentaire',
        'reseaux', 'roles', 'zonehydro', 'visites')

    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        return 'Sitemeteo {0}::{1} [{2} grandeur{3}]'.format(
            self.code if self.code is not None else '<sans code>',
            self.libelle if self.libelle is not None else '<sans libelle>',
            len(self.grandeurs),
            '' if (len(self.grandeurs) < 2) else 's'
        )

    __str__ = _composant.__str__


# -- class Grandeur -----------------------------------------------------------
class Grandeur(object):

    """Classe Grandeur.

    Classe pour manipuler des grandeurs meteorologiques.

    Proprietes:
        typegrandeur (string parmi NOMENCLATURE[523]) = type de grandeur
        sitemeteo (Sitemeteo ou None) : site dont dépend la grandeur
        dtmiseservice (datetime.datetime ou None) = date de mise en service
        dtfermeture (datetime.datetime ou None) = date de fermeture
        essai (bool ou None) = grandeur d'essai
        surveillance (bool ou None) = à surveiller
        delaiabsence (int ou None) = délai d'absence
        pdt (int ou None) = pas de temps pour un capteur RR
        classesqualite (ClasseQualite or iterbale of ClasseQualite)
            = classes de qualité
        dtmaj (datetime.datetime ou None) = date de mise à jour
        strict (bool, defaut True) = le mode permissif permet de lever les
            controles de validite du sitemeteo et du type

    """

    # Grandeur other properties

    # valeursseuils

    typemesure = _composant.Nomenclatureitem(nomenclature=523)
    dtmaj = _composant.Datefromeverything(required=False)
    dtmiseservice = _composant.Datefromeverything(required=False)
    dtfermeture = _composant.Datefromeverything(required=False)

    def __init__(self, typemesure, sitemeteo=None, dtmiseservice=None,
                 dtfermeture=None, essai=None, surveillance=None,
                 delaiabsence=None, pdt=None, classesqualite=None, dtmaj=None,
                 strict=True):
        """Initialisation.

        Arguments:
            typegrandeur (string parmi NOMENCLATURE[523]) = type de grandeur
            sitemeteo (Sitemeteo ou None) : site dont dépend la grandeur
            dtmiseservice (datetime.datetime ou None) = date de mise en service
            dtfermeture (datetime.datetime ou None) = date de fermeture
            essai (bool ou None) = grandeur d'essai
            surveillance (bool ou None) = à surveiller
            delaiabsence (int ou None) = délai d'absence
            pdt (int ou None) = pas de temps pour un capteur RR
            classesqualite (ClasseQualite or iterbale of ClasseQualite)
                = classes de qualité
            dtmaj (datetime.datetime ou None) = date de mise à jour
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du sitemeteo et du type

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(Grandeur)['typemesure'].strict = self._strict
        vars(Grandeur)['typemesure'].required = self._strict

        # -- descriptors --
        self.typemesure = typemesure
        self.dtmiseservice = dtmiseservice
        self.dtfermeture = dtfermeture
        self.dtmaj = dtmaj

        # -- full properties --
        self._sitemeteo = None
        self.sitemeteo = sitemeteo
        self._pdt = None
        self.pdt = pdt
        self._essai = None
        self.essai = essai
        self._surveillance = None
        self.surveillance = surveillance
        self._delaiabsence = None
        self.delaiabsence = delaiabsence
        self._classesqualite = []
        self.classesqualite = classesqualite

    # -- property sitemeteo --
    @property
    def sitemeteo(self):
        """Return sitemeteo."""
        return self._sitemeteo

    @sitemeteo.setter
    def sitemeteo(self, sitemeteo):
        """Set sitemeteo."""
        if (sitemeteo is not None) and self._strict:
            if not isinstance(sitemeteo, Sitemeteo):
                raise TypeError('sitemeteo must be a Sitemeteo')
        self._sitemeteo = sitemeteo

    # -- property sitemeteo --
    @property
    def pdt(self):
        """Return pdt."""
        return self._pdt

    @pdt.setter
    def pdt(self, pdt):
        """Set pdt."""
        self._pdt = None
        if pdt is None:
            return
        pdt = int(pdt)
        if pdt < 0:
            raise ValueError('pdt must be positive')
        self._pdt = pdt

    # -- property sitemeteo --
    @property
    def essai(self):
        """Return essai."""
        return self._essai

    @essai.setter
    def essai(self, essai):
        """Set essai."""
        self._essai = bool(essai) if essai is not None else None

    # -- property sitemeteo --
    @property
    def surveillance(self):
        """Return surveillance."""
        return self._surveillance

    @surveillance.setter
    def surveillance(self, surveillance):
        """Set surveillance."""
        self._surveillance = bool(surveillance) \
            if surveillance is not None else None

    # -- property delaiabsence --
    @property
    def delaiabsence(self):
        """Return delaiabsence."""
        return self._delaiabsence

    @delaiabsence.setter
    def delaiabsence(self, delaiabsence):
        """Set delaiabsence."""
        self._delaiabsence = None
        if delaiabsence is None:
            return
        delaiabsence = int(delaiabsence)
        if delaiabsence < 0:
            raise ValueError('delaiabsence must be positive')
        self._delaiabsence = delaiabsence

    # -- property classesqualite --
    @property
    def classesqualite(self):
        """Return classesqualite."""
        return self._classesqualite

    @classesqualite.setter
    def classesqualite(self, classesqualite):
        """Set classesqualite."""
        self._classesqualite = []
        # None case
        if classesqualite is None:
            return
        # one grandeur, we make a list with it
        if isinstance(classesqualite, ClasseQualite):
            classesqualite = [classesqualite]
        # an iterable of classesqualite
        for classe in classesqualite:
            # some checks
            if self._strict:
                if not isinstance(classe, ClasseQualite):
                    raise TypeError(
                        'classesqualite must be a ClasseQualite or an iterable'
                        ' of ClasseQualite'
                    )
            # add capteur
            self._classesqualite.append(classe)

    # -- special methods --
    __all__attrs__ = ('typemesure', 'sitemeteo', 'pdt')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        str_pdt = 'de pas de temps {}'.format(self.pdt) \
            if self.pdt is not None else ''
        return 'Grandeur {0} {1} sur le site meteo {2}'.format(
            self.typemesure if self.typemesure is not None
            else '<sans type de mesure>',
            str_pdt,
            self.sitemeteo.code if (
                (self.sitemeteo is not None) and
                (self.sitemeteo.code is not None)
            ) else '<inconnu>'
        )

    __str__ = _composant.__str__


class SitemeteoPondere(Sitemeteo):
    """Classe SiteMeteoPondere

    Classe permettant de manipuler des sites météo pondérés
    Proprietes:
        proprietes de Sitemeteo
        pondération (float): Pondération du site
    """
    def __init__(self, code, ponderation):
        # -- super --
        super(SitemeteoPondere, self).__init__(code=code)

        self._ponderation = None
        self.ponderation = ponderation

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
            self.code, self.ponderation)

    __str__ = _composant.__str__

# -- class Visite -------------------------------------------------------------
class Visite(object):
    """Classe Visite

    Classe permettant de manipuler des visites de sites météo pondérés
    Proprietes:
        dtvisite (datetime.datetime) = date de la viiste
        contact (intervenant.Contact ou None) = contact ayant réalisé la visite
        methode (str ou None) = méthode
        modeop (str ou None) = mode opératoire
    """
    dtvisite = _composant.Datefromeverything(required=True)

    def __init__(self, dtvisite=None, contact=None, methode=None, modeop=None):
        """Initialisation.

        Arguments:
            dtvisite (datetime.datetime) = date de la viiste
            contact (intervenant.Contact ou None) = contact lié à la visite
            methode (str ou None) = méthode
            modeop (str ou None) = mode opératoire

        """
        self.dtvisite = dtvisite
        self._contact = None
        self.contact = contact
        self.methode = str(methode) if methode is not None else None
        self.modeop = str(modeop) if modeop is not None else None

    # -- property contact --
    @property
    def contact(self):
        """Return entite hydro."""
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Set contact."""
        self._contact = None
        if contact is None:
            return
        try:
            # contact must be a contact
            if not isinstance(contact, _intervenant.Contact):
                raise TypeError('contact must be a Contact')

            self._contact = contact

        except Exception:
            raise

    def __unicode__(self):
        strcontact = ''
        if self.contact is not None:
            strcontact = ' par le contact {}'.format(self.contact.code)
        return "Visite du {0}{1}".format(
            self.dtvisite, strcontact)

    __str__ = _composant.__str__


# -- class ClasseQualite ------------------------------------------------------
class ClasseQualite(object):
    """ClasseQualite

    Classe permettant de manipuler des classes de qualité
    Proprietes:
        classe (int) = classe de qualité compris entre 1 et 5
        visite (Visite ou None) = Visite associée à la classe de qualité
        dtdeb (datetime.datetime ou None) = date de début
        dtfin (datetime.datetime ou None) = mode opératoire
    """
    dtdeb = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)

    def __init__(self, classe, visite=None, dtdeb=None, dtfin=None):
        """Initialisation.

        Arguments:
            classe (int) = classe de qualité compris entre 1 et 5
            visite (Visite ou None) = Visite associée à la classe de qualité
            dtdeb (datetime.datetime ou None) = date de début
            dtfin (datetime.datetime ou None) = mode opératoire

        """
        self._classe = None
        self.classe = classe
        self._visite = None
        self.visite = visite
        self.dtdeb = dtdeb
        self.dtfin = dtfin

    # -- property classe --
    @property
    def classe(self):
        """Return classe."""
        return self._classe

    @classe.setter
    def classe(self, classe):
        """Set classe."""
        classe = int(classe)
        if classe < 1 or classe > 5:
            raise ValueError('classe de qualite must be between 1 and 5')
        self._classe = classe

    # -- property visite --
    @property
    def visite(self):
        """Return visite."""
        return self._visite

    @visite.setter
    def visite(self, visite):
        """Set visite."""
        self._visite = None
        if visite is None:
            return
        if not isinstance(visite, Visite):
            raise TypeError('visite must be an instance of Visite')
        self._visite = visite

    def __unicode__(self):
        strvisite = ''
        if self.visite is not None:
            strvisite = ' (visite du {})'.format(self.visite.dtvisite)
        strdeb = ''
        if self.dtdeb is not None:
            strdeb = ' de {}'.format(self.dtdeb)
        strfin = ''
        if self.dtfin is not None:
            strfin = ' à {}'.format(self.dtfin)
        return "Classe de qualité {0}{1}{2}{3}".format(
            self.classe, strvisite, strdeb, strfin)

    __str__ = _composant.__str__

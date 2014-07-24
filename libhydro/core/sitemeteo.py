# -*- coding: utf-8 -*-
"""Module sitemeteo.

Ce module contient les classes:
    # Sitemeteo
    # Grandeur
    # Visite - not implemented
    # Classequalite - not implemented

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from . import (_composant, _composant_site)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1g"""
__date__ = """2014-07-24"""

#HISTORY
#V0.1 - 2014-07-07
#    first shot


#-- todos ---------------------------------------------------------------------
# PROGRESS - Sitemeteo 50% - Grandeur 10% - Visite 0% - Classequalite 0%


#-- class Sitemeteo -----------------------------------------------------------
class Sitemeteo(object):

    """Classe Sitemeteo.

    Classe pour manipuler des sites meteorologiques.

    Proprietes:
        code (string(9)) = code INSEE
        libelle (string)
        libelleusuel (string)
        coord (Coord) =
            x, y (float)
            proj (int parmi NOMENCLATURE[22]) = systeme de projection
        commune (string(5)) = code INSEE commune
        grandeurs (une liste de Grandeur)

    """

    # Sitemeteo other properties

    #mnemonique
    #lieu-dit
    #altitude, sysalti
    #fuseau
    #dtmaj
    #dtes
    #dths
    #publication
    #essai
    #commentaire

    #images
    #rolecontact
    #soussecteurhydro

    #visites

    def __init__(
        self, code, libelle=None, libelleusuel=None, coord=None, commune=None,
        grandeurs=None, strict=True
    ):
        """Initialisation.

        Arguments:
            code (string(9)) = code INSEE. Un code de 8 caracteres est prefixe
                d'un zero
            libelle (string)
            libelleusuel (string)
            coord (list ou dict) =
                (x, y, proj) ou {'x': x, 'y': y, 'proj': proj}
                avec proj (int parmi NOMENCLATURE[22]) = systeme de projection
            commune (string(5)) = code INSEE commune
            grandeurs (une liste de Grandeur)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du code et des grandeurs

        """

        # -- simple properties --
        self._strict = bool(strict)
        self.libelle = unicode(libelle) \
            if (libelle is not None) else None
        self.libelleusuel = unicode(libelleusuel) \
            if (libelleusuel is not None) else None

        # -- full properties --
        self._code = self._coord = self._commune = None
        self._grandeurs = []
        self.code = code
        self.coord = coord
        self.commune = commune
        self.grandeurs = grandeurs

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
                code = unicode(code)
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

    # -- other methods --
    def __eq__(self, other):
        """Return True ou False."""
        if self is other:
            return True
        for attr in ('code', ):
            if getattr(self, attr, True) != getattr(other, attr, False):
                return False
        return True

    def __ne__(self, other):
        """Return True ou False."""
        return not self.__eq__(other)

    def __unicode__(self):
        """Return unicode representation."""
        return 'Sitemeteo {0}::{1} [{2} grandeur{3}]'.format(
            self.code if self.code is not None else '<sans code>',
            self.libelle if self.libelle is not None else '<sans libelle>',
            len(self.grandeurs),
            '' if (len(self.grandeurs) < 2) else 's'
        )

    __str__ = _composant.__str__


#-- class Grandeur ------------------------------------------------------------
class Grandeur(object):

    """Classe Grandeur.

    Classe pour manipuler des grandeurs meteorologiques.

    Proprietes:
        typemesure (string parmi NOMENCLATURE[523])
        sitemeteo (Sitemeteo)

    """

    # Grandeur other properties

    # dtes
    # dths
    # essai
    # pdt
    # dtmaj

    # classesqualites

    # valeursseuils

    typemesure = _composant.Nomenclatureitem(nomenclature=523)

    def __init__(self, typemesure, sitemeteo=None, strict=True):
        """Initialisation.

        Arguments:
            typegrandeur (string parmi NOMENCLATURE[523])
            sitemeteo (Sitemeteo)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du sitemeteo et du type

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(self.__class__)['typemesure'].strict = self._strict
        vars(self.__class__)['typemesure'].required = self._strict

        # -- descriptors --
        self.typemesure = typemesure

        # -- full properties --
        self._sitemeteo = None
        self._sitemeteo = sitemeteo

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

    # -- other methods --
    def __eq__(self, other):
        """Return True ou False."""
        if self is other:
            return True
        for attr in ('typemesure', 'sitemeteo'):
            if getattr(self, attr, True) != getattr(other, attr, False):
                return False
        return True

    def __ne__(self, other):
        """Return True ou False."""
        return not self.__eq__(other)

    def __unicode__(self):
        """Return unicode representation."""
        return 'Grandeur {0} sur le site meteo {1}'.format(
            self.typemesure if self.typemesure is not None
            else '<sans type de mesure>',
            self.sitemeteo.code if (
                (self.sitemeteo is not None) and
                (self.sitemeteo.code is not None)
            ) else '<inconnu>'
        )

    __str__ = _composant.__str__

#-- class Visite --------------------------------------------------------------
# class Visite(object):
#
#     raise NotImplementedError
#
# Properties:
#     dt
#     contact (visiteur)
#     methode
#     modop
#     sitemeteo


#-- class Classequalite -------------------------------------------------------
# class Classequalite(object):
#
#     raise NotImplementedError

# Properties:
#     classe
#     visite
#     dtdeb
#     dtfin

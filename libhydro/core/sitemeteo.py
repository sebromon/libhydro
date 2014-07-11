# -*- coding: utf-8 -*-
"""Module sitemeteo.

Ce module contient les classes:
    # Sitemeteo
    # Grandeurmeteo
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

import sys as _sys
import locale as _locale

from . import _composant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1c"""
__date__ = """2014-07-11"""

#HISTORY
#V0.1 - 2014-07-07
#    first shot


#-- todos ---------------------------------------------------------------------
# PROGRESS - Sitemeteo 50% - Grandeurmeteo 10% - Visite 0% - Classequalite 0%
# TODO - add navigability for Grandeurmeteo => Sitemeteo


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
            code (string(9)) = code INSEE
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
                    _composant.is_code_insee(code=code, length=9)

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
            if isinstance(coord, _composant.Coord):
                self._coord = coord
            else:
                try:
                    # instanciate with a list
                    self._coord = _composant.Coord(*coord)
                except (TypeError, ValueError, AttributeError):
                    try:
                        # instanciate with a dict
                        self._coord = _composant.Coord(**coord)
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
            _composant.is_code_insee(commune, length=5)
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
        if isinstance(grandeurs, Grandeurmeteo):
            grandeurs = [grandeurs]
        # an iterable of grandeurs
        for grandeur in grandeurs:
            # some checks
            if self._strict:
                if not isinstance(grandeur, Grandeurmeteo):
                    raise TypeError(
                        'grandeurs must be a Grandeur or an iterable '
                        'of Grandeur'
                    )
            # add capteur
            self._grandeurs.append(grandeur)

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Sitemeteo {0}::{1} [{2} grandeur{3}]'.format(
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            len(self.grandeurs),
            '' if (len(self.grandeurs) < 2) else 's'
        )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(
                _sys.stdout.encoding or
                _locale.getpreferredencoding() or
                'ascii',
                'replace'
            )


#-- class Grandeurmeteo -------------------------------------------------------
class Grandeurmeteo(object):

    """Classe Grandeurmeteo.

    Classe pour manipuler des grandeurs meteorologiques.

    Proprietes:
        typegrandeur (string parmi NOMENCLATURE[523])

    """

    # Grandeurmeteo other properties

    # dtes
    # dths
    # essai
    # pdt
    # dtmaj

    # classesqualites

    # valeursseuils

    typegrandeur = _composant.Nomenclatureitem(nomenclature=523)

    def __init__(self, typegrandeur, strict=True):
        """Initialisation.

        Arguments:
            typegrandeur (string parmi NOMENCLATURE[523])
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du type

        """

        # -- simple properties --
        self._strict = bool(strict)

        # adjust the descriptor
        vars(self.__class__)['typegrandeur'].strict = self._strict
        vars(self.__class__)['typegrandeur'].required = self._strict

        # -- descriptors --
        self.typegrandeur = typegrandeur

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Grandeurmeteo {0}'.format(self.typegrandeur or '<sans type>')

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(
                _sys.stdout.encoding or
                _locale.getpreferredencoding() or
                'ascii',
                'replace'
            )


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

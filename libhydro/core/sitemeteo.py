# -*- coding: utf-8 -*-
"""Module sitemeteo.

Ce module contient les classes:
    # Sitemeteo
    # Grandeur

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
__version__ = """0.1b"""
__date__ = """2014-07-11"""

#HISTORY
#V0.1 - 2014-07-07
#    first shot


#-- todos ---------------------------------------------------------------------
# PROGRESS - Sitemeteo 0% - Grandeurmeteo 0%
# TODO - classes # Visite and # Qualite


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

    # # -- property communes --
    # @property
    # def communes(self):
    #     """Return codes communes."""
    #     return self._communes

    # @communes.setter
    # def communes(self, communes):
    #     """Set code commune."""
    #     self._communes = []
    #     # None case
    #     if communes is None:
    #         return
    #     # one commune, we make a list with it
    #     if _composant.is_code_commune(communes, raises=False):
    #         communes = [communes]
    #     # an iterable of communes
    #     for commune in communes:
    #         if _composant.is_code_commune(commune):
    #             self._communes.append(unicode(commune))

    # # -- property tronconsvigilance --
    # @property
    # def tronconsvigilance(self):
    #     """Return tronconsvigilance."""
    #     return self._tronconsvigilance

    # @tronconsvigilance.setter
    # def tronconsvigilance(self, tronconsvigilance):
    #     """Set tronconsvigilance."""
    #     self._tronconsvigilance = []
    #     # None case
    #     if tronconsvigilance is None:
    #         return
    #     # one troncon, we make a list with it
    #     if isinstance(tronconsvigilance, Tronconvigilance):
    #         tronconsvigilance = [tronconsvigilance]
    #     # an iterable of tronconsvigilance
    #     for tronconvigilance in tronconsvigilance:
    #         # some checks
    #         if self._strict:
    #             if not isinstance(tronconvigilance, Tronconvigilance):
    #                 raise TypeError(
    #                     'tronconsvigilance must be a Tronconvigilance '
    #                     'or an iterable of Tronconvigilance'
    #                 )
    #         # add station
    #         self._tronconsvigilance.append(tronconvigilance)

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

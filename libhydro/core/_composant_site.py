# coding: utf-8
"""Module composant_site.

Ce module contient les elements communs aux modules sitehydro et sitemeteo.

Il integre les classes:
    # Coord

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from . import _composant
from .nomenclature import NOMENCLATURE as _NOMENCLATURE


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """1.0b"""
__date__ = """2014-07-18"""

# HISTORY
# V0.1 - 2014-07-16
#   split the composant file in 3 parts


# -- class Coord --------------------------------------------------------------
class Coord(object):

    """Classe Coord.

    Classe pour manipuler des coordonnees.

    Proprietes:
        x, y (float)
        proj (int parmi NOMENCLATURE[22]) = systeme de projection

    """

    proj = _composant.Nomenclatureitem(nomenclature=22)

    def __init__(self, x, y, proj=None, strict=True):
        """Initialisation.

        Arguments:
            x, y (float)
            proj (int parmi NOMENCLATURE[22]) = systeme de projection
            strict (bool, defaut True) = le mode permissif permet de rendre
                facultatif le parametre proj

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(self.__class__)['proj'].required = self._strict

        for crd in ('x', 'y'):
            try:
                self.__setattr__(crd, float(locals()[crd]))
            except Exception:
                raise TypeError('{} must be a number'.format(crd))

        # -- descriptors --
        self.proj = proj

    # -- other methods --
    __all__attrs__ = ('x', 'y', 'proj')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        # init
        try:
            proj = _NOMENCLATURE[22][self.proj]
        except Exception:
            proj = '<projection inconnue>'

        # action !
        return 'Coord (x={0}, y={1}) [proj {2}]'.format(
            self.x,
            self.y,
            proj
        )

    __str__ = _composant.__str__

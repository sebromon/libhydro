# -*- coding: utf-8 -*-
"""Module zonehydro.

Ce module contient la classe:
    # Zonehydro

"""

# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

from libhydro.core import _composant


class Zonehydro(object):
    """Classe Zonehydro.

    Classe pour manipuler des zones hydro.
    Propriétés:
        code (string(4)) = code de la zone hydro
        libelle (str)= libellé
    """

    def __init__(self, code=None, libelle=None):
        """Initialisation.

        Arguments:
            code (string(4)) = code de la zone hydro
            libelle (str ou None) = libellé
        """
        self.libelle = str(libelle) if libelle is not None else None

        self._code = None
        self.code = code

    # -- property code --
    @property
    def code(self):
        """Return code."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code."""
        self._code = None
        # None case
        if code is None:
            raise TypeError('code is required')
        code = str(code)
        if len(code) != 4:
            raise ValueError(
                    'length of zone hydro ({}) must be 4'.format(code))
        self._code = code

    def __unicode__(self):
        libelle = self.libelle if self.libelle is not None else '<sans libellé>'
        return "{} ({})".format(self.code, libelle)

    __str__ = _composant.__str__

# -*- coding: utf-8 -*-
"""Module composants.

Ce module contient les elements communs a plusieurs modules.

Il integre les classes:
    # Coord

et les fonctions:
    # is_code_hydro()
    # is_code_commune()

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys as _sys

from libhydro.core.nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2013-11-07"""

#HISTORY
#V0.1 - 2013-11-06
#    first shot


#-- todos ---------------------------------------------------------------------


#-- class Coord ---------------------------------------------------------------
class Coord(object):

    """Classe Coord.

    Classe pour manipuler des coordonnees.

    Proprietes:
        x, y (numerique)
        proj (caractere parmi NOMENCLATURE[22]) = systeme de projection

    """

    def __init__(self, x, y, proj=None, strict=True):
        """Initialisation.

        Arguments:
            x, y (numeriques)
            proj (caractere parmi NOMENCLATURE[22]) = systeme de projection
            strict (bool, defaut True) = le mode permissif permet de rendre
                facultatif le parametre sysproj

        """

        # -- super --
        # super(Coord, self).__init__(
        #     x=float(x), y=float(y)
        # )

        # -- simple properties --
        for crd in ('x', 'y'):
            try:
                self.__setattr__(crd, float(locals()[crd]))
            except Exception:
                raise TypeError('{} must be a number'.format(crd))
        self._strict = bool(strict)

        # -- full properties --
        self._proj = None
        self.proj = proj

    # -- property proj --
    @property
    def proj(self):
        """Return proj."""
        return self._proj

    @proj.setter
    def proj(self, proj):
        """Set proj."""
        try:
            if self._strict:
                # none case
                if proj is None:
                    raise TypeError('proj is required')

                # other cases
                proj = int(proj)
                if proj not in _NOMENCLATURE[22]:
                    raise ValueError('unknown proj')

            # all is well
            self._proj = proj

        except:
            raise

    # -- other methods --
    def __eq__(self, other):
        return (
            (self.x == other.x)
            and (self.y == other.y)
            and (self.proj == other.proj)
        )

    def __unicode__(self):
        """Return unicode representation."""
        return 'Coord (x={0}, y={1}) [proj {2}]'.format(
            self.x,
            self.y,
            _NOMENCLATURE[22][self.proj] if (self.proj is not None) else
            '<projection inconnue>'
        )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


#-- functions -----------------------------------------------------------------
def is_code_hydro(code, length=8, raises=True):
    """Return whether or not code is a valid code hydro.

    Arguments:
       code (char)
       length (int, default 8) = code size
       raises (bool, default True) = if False doesn't raise

    """
    try:
        # (length) chars length
        if len(code) != length:
            raise ValueError(
                'code hydro must be {0:d} chars long'.format(length)
            )

        # upper first char
        if not code[0].isupper():
            raise ValueError('code hydro first char must be upper')

        # [1:] digits
        if not code[1:].isdigit():
            raise ValueError('code hydro [1:] chars must be digits')

        # all is well
        return True

    except Exception:
        if raises:
            raise
        else:
            return False


def is_code_commune(code, raises=True):
    """Return whether or not code is a valid INSEE commune code.

    Le numero de la commune est le numero INSEE de la commune base sur 5
    caracteres. Pour les communes de metropoles, les deux premiers caracteres
    correspondent au numero du departement auquel la commune appartient. Pour
    les DOM, les trois premiers caracteres correspondent au code du departement
    auquel la commune appartient.  Il est a noter que ce numero de la commune
    est au format caractere afin de gerer les communes de la Corse (2A et 2B).

    Arguments:
       code (char)
       raises (bool, default True) = if False doesn't raise

    """
    try:
        # prepare
        code = unicode(code)

        # 5 chars length
        if len(code) != 5:
            raise ValueError('code must be 5 chars long')

        # code commune must be all digit or 2(A|B)xxx
        if not code.isdigit():
            if not ((code[:2] in ('2A', '2B')) and (code[2:].isdigit())):
                raise ValueError('illegal char in code')

        # all is well
        return True

    except Exception:
        if raises:
            raise
        else:
            return False

# -*- coding: utf-8 -*-
"""Module composants.

Ce module contient les elements communs a plusieurs modules.

Il integre les classes:
    # Coord

les descripteurs:
    # Datefromeverything
    # Nomenclatureitem

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
import weakref as _weakref
import numpy as _numpy
import datetime as _datetime

from .nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2a"""
__date__ = """2014-03-01"""

#HISTORY
#V0.2 - 2014-02-01
#    add 2 descriptors
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


#-- class Datefromeverything --------------------------------------------------
class Datefromeverything(object):

    """Class Datefromeverything.

    A descriptor to store a datetime.datetime property that can be initiated
    in different manners using numpy.datetime64 facilities.

    """

    def __init__(self, required=True, default=None):
        """Initialization.

        Args:
            required (bool, defaut True) = wether instance's value can
                be None or not

        """
        self.required = bool(required)
        self.default = default
        self.data = _weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        """Return instance value."""
        return self.data.get(instance, default=self.default)

    def __set__(self, instance, value):
        """Set the datetime.datetime property.

        Args:
            value (
                numpy.datetime64 or string to make one
                datetime.datetime or iterable or dict to make it
            )

        String format: look at
          [http://docs.scipy.org/doc/numpy-dev/reference/arrays.datetime.html]

        """
        if self.required and (value is None):
            raise TypeError('a value other than None is required')
        if (
            (value is not None)
            and not isinstance(value, _datetime.datetime)
            and not isinstance(value, _numpy.datetime64)
        ):
            try:
                if isinstance(value, dict):
                    value = _datetime.datetime(**value)
                elif isinstance(value, (str, unicode)):
                    value = _numpy.datetime64(value, 's')
                else:  # can be an iterable for datetime.datetime
                    value = _datetime.datetime(*value)
            except (ValueError, TypeError, AttributeError):
                raise ValueError(
                    'could not convert object to datetime.datetime'
                )

        # all is well
        if isinstance(value, _numpy.datetime64):
            value = value.item()
        self.data[instance] = value


#-- class Nomenclatureitem ----------------------------------------------------
class Nomenclatureitem(object):

    """Class Nomenclatureitem.

    A descriptor to deal with 'in nomenclature.NOMENCLATURES' properties.

    """

    def __init__(self, nomenclature, strict=True, required=True, default=None):
        """Initialization.

        Args:
            nomenclature (int) = the nomenclature ref
            required (bool, defaut True) = wether instance's value can
                be None or not

        """
        self.nomenclature = int(nomenclature)
        self.strict = bool(strict)
        self.required = bool(required)
        self.default = default
        self.data = _weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        """Return instance value."""
        return self.data.get(instance, default=self.default)

    def __set__(self, instance, value):
        """Set the 'in nomenclature' property."""
        # None case
        if (value is None):
            if self.required:
                raise TypeError('a value other than None is required')

        # other cases
        if (self.strict) and (value not in _NOMENCLATURE[self.nomenclature]):
            raise ValueError(
                'value should be in nomenclature %i' % self.nomenclature
            )

        # all is well
        self.data[instance] = value


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

    except (ValueError, TypeError):
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

    except (ValueError, TypeError):
        if raises:
            raise
        else:
            return False

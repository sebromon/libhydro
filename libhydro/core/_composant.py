# -*- coding: utf-8 -*-
"""Module composant.

Ce module contient des elements de base de la librairie.

Il integre les descripteurs:
    # Datefromeverything
    # Nomenclatureitem

et les fonctions:
    # is_code_hydro()
    # is_code_insee()
    # __str__()

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

import weakref as _weakref
import numpy as _numpy
import datetime as _datetime

from .nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.9e"""
__date__ = """2014-07-16"""

#HISTORY
#V0.9 - 2014-07-16
#    split the module in 3 parts
#V0.8 - 2014-02-01
#    add and use descriptors
#V0.1 - 2013-11-06
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - use regex for codes matching functions


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

    Should raise only a ValueError when value is not allowed (even with
    the None case).

    Properties:
        nomenclature (int) = the nomenclature ref
        valuetype (type) = a function to cast values to the nomenclature's
            items type
        strict (bool, default True) = wether or not the instance value has
            to be in the nomenclature items
        required (bool, defaut True) = wether or not instance's value can
            be None
        default =  a defautl value returned if the instance's value is not
            in the dictionnary. Should be unused if the property has been
            initialized.
        data (weakref.WeakKeyDictionary)

    """

    def __init__(self, nomenclature, strict=True, required=True, default=None):
        """Initialization.

        Args:
            nomenclature (int) = the nomenclature ref
            strict (bool, default True) = wether or not the instance value has
                to be in the nomenclature items
            required (bool, defaut True) = wether or not instance's value can
                be None
            default =  a defautl value returned if the instance's value is not
                in the dictionnary. Should be unused if the property has been
                initialized.

        """
        self.nomenclature = int(nomenclature)
        if self.nomenclature not in _NOMENCLATURE:
            raise ValueError('unknown nomenclature')
        self.valuetype = type(_NOMENCLATURE[self.nomenclature].keys()[0])
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
                raise ValueError('a value other than None is required')

        # other cases
        else:
            value = self.valuetype(value)
            if (
                (self.strict) and
                (value not in _NOMENCLATURE[self.nomenclature])
            ):
                raise ValueError(
                    'value should be in nomenclature %i' % self.nomenclature
                )

        # all is well
        self.data[instance] = value


#-- functions -----------------------------------------------------------------
def is_code_hydro(code, length=8, raises=True):
    """Return whether or not code is a valid code hydro.

    Arguments:
       code (string)
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

        # [1:-1] digits
        if not code[1:-1].isdigit():
            raise ValueError(
                'code hydro chars except first and last must be digits'
            )

        # digit or upper last char
        if not (code[-1].isdigit() or code[-1].isupper()):
            raise ValueError('code hydro last char must be digit or upper')

        # all is well
        return True

    except (ValueError, TypeError):
        if raises:
            raise
        else:
            return False


def is_code_insee(code, length=5, raises=True):
    """Return whether or not code is a valid INSEE code.

    Un code INSEE de commune est construit sur 5 caracteres. Pour les
    communes de metropole, les deux premiers caracteres correspondent
    au numero du departement de la commune. Pour les DOM, les trois
    premiers caracteres correspondent au numero du departement de la
    commune. Il est a noter que ce code est au format caractere afin de
    gerer les communes de la Corse (2A et 2B).

    Un code INSEE de site meteorologique est construit sur 9 caracteres.
    Les 6 premiers forment le code INSEE de la commune de localisation,
    prefixe d'un zero significatif, ou bien un code de pays pour les
    postes hors du territoire national. Les 3 derniers caracteres sont
    un numero d'ordre du site meteorologique.

    Arguments:
       code (string(length), default length is 5)
       raises (bool, default True) = if False doesn't raise

    """
    # pre-condition
    if length not in (5, 9):
        raise ValueError('length must be 5 or 9')

    try:
        # prepare
        code = unicode(code)

        # chars length
        if len(code) != length:
            raise ValueError('INSEE code must be %i chars long' % length)

        # code commune must be all digit or 2(A|B)xxx
        if not code.isdigit():
            start = length is 9  # 0 or 1
            if not (
                (code[start:start + 2] in ('2A', '2B')) and
                (code[start + 2:].isdigit())
            ):
                raise ValueError('illegal char in INSEE code')

        # all is well
        return True

    except (ValueError, TypeError):
        if raises:
            raise
        else:
            return False


def __str__(self):
    """Return string representation from __unicode__ method."""
    if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
        return self.__unicode__()
    else:  # Python 2
        return self.__unicode__().encode(
            _sys.stdout.encoding or
            _locale.getpreferredencoding() or
            'ascii',
            'replace'
        )

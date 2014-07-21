# -*- coding: utf-8 -*-
"""Module composant.

Ce module contient des elements de base de la librairie.

Il integre:
    # un gestionnaire d'erreurs (ERROR_HANDLERS)

la classe:
    # Rlist

les descripteurs:
    # Rlistproperty
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
import warnings as _warnings

import weakref as _weakref
import numpy as _numpy
import datetime as _datetime

from .nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.9f"""
__date__ = """2014-07-20"""

#HISTORY
#V0.9 - 2014-07-16
#    add the error_handler, the Rlist and the Rlistproperty
#    split the module in 3 parts
#V0.8 - 2014-02-01
#    add and use descriptors
#V0.1 - 2013-11-06
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - use regex for codes matching functions


#-- a basic errors handler ----------------------------------------------------
def _warn_handler(msg, *args, **kwargs):
    """Print msg on stderr."""
    _warnings.warn(msg)


def _strict_handler(msg, error):
    """Raise error(msg)."""
    raise error(msg)


ERROR_HANDLERS = {
    "ignore": lambda *args, **kwargs: None,  # 'ignore' returns None
    "warn": _warn_handler,  # 'warn' emit 'warn(msg)'
    "strict": _strict_handler  # 'strict' raises 'error(msg)'
}


#-- class Rlist ---------------------------------------------------------------
class Rlist(list):

    """Class Rlist.

    A class of restricted lists that can only contains items of type 'cls'.

    Read only property:
        cls (type)

    Methods:
        all list methods
        check()

    """

    def __init__(self, cls, iterable=None):
        """Initialisation.

        Arguments:
            cls (type) = the class of authorized items
            iterable (iterable, default None) = the list elements

        """
        # a read only property
        self._cls = cls

        # check and init
        self.checkiterable(iterable)
        super(Rlist, self).__init__(iterable)

    # -- read only property cls --
    @property
    def cls(self):
        """Get cls."""
        return self._cls

    # -- list overwritten methods --
    def append(self, y):
        """Append method."""
        self.checkiterable([y])
        super(Rlist, self).append(y)

    def extend(self, iterable):
        """Extend method."""
        self.checkiterable(iterable)
        super(Rlist, self).extend(iterable)

    def insert(self, i, y):
        """Insert method."""
        self.checkiterable([y])
        super(Rlist, self).insert(i, y)

    def __setitem__(self, i, y):
        """Setitem method."""
        self.checkiterable([y])
        super(Rlist, self).__setitem__(i, y)

    def __setslice__(self, i, j, y):
        """Setitem method."""
        self.checkiterable(y)
        super(Rlist, self).__setslice__(i, j, y)

    # -- other methods --
    def checkiterable(self, iterable, errors='strict'):
        """Check iterable items type.

        Arguments:
            iterable (iterable)
            errors (str in 'strict' (default), 'ignore', 'warn')

        """
        # get the error handler
        try:
            error_handler = ERROR_HANDLERS[errors]
        except Exception:
            raise ValueError("unknown error handler name '%s'" % errors)
        # check
        if iterable is not None:
            for obj in iterable:
                if not isinstance(obj, self.cls):
                    error_handler(
                        msg="the object '%s' is not of %s" % (obj, self.cls),
                        error=TypeError
                    )
                    return False
        # return
        return True

# reset docstrings to their original 'list' values
Rlist.append.__func__.__doc__ = list.append.__doc__
Rlist.extend.__func__.__doc__ = list.extend.__doc__
Rlist.insert.__func__.__doc__ = list.insert.__doc__
Rlist.__setitem__.__func__.__doc__ = list.__setitem__.__doc__
Rlist.__setslice__.__func__.__doc__ = list.__setslice__.__doc__


#-- class  Rlistproperty ------------------------------------------------------
class Rlistproperty(object):

    """Class Rlistproperty

    A descriptor to deal with a list of restricted items.

    Raises a TypeError when value is not allowed.

    Properties:
        cls (class) = the type of the list items
        strict (bool, default True) = wether or not the instance value has
            to be a Rlist or a regular list
        required (bool, defaut True) = wether or not instance's value can
            be None
        default =  a defautl value returned if the instance's value is not
            in the dictionnary. Should be unused if the property has been
            initialized.
        data (weakref.WeakKeyDictionary)

    """

    def __init__(self, cls, strict=True, required=True, default=None):
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
        self.cls = cls
        self.strict = bool(strict)
        self.required = bool(required)
        self.default = default
        self.data = _weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        """Return instance value."""
        return self.data.get(instance, default=self.default)

    def __set__(self, instance, items):
        """Set the instance list."""
        # None case
        if (items is None):
            if self.required:
                raise ValueError('a value other than None is required')
            rlist = Rlist(self.cls) if self.strict else []

        # other cases
        else:
            rlist = Rlist(self.cls, items) if self.strict else list(items)

        # all is well
        self.data[instance] = rlist


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
def is_code_hydro(code, length=8, errors='ignore'):
    """Return wether or not code is a valid code hydro as a bool.

    Arguments:
       code (string)
       length (int, default 8) = code size
       errors (str in 'ignore' (default), 'strict') = 'strict' raises an
           exception

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

    except Exception as err:
        if errors not in ('ignore', 'strict'):
            raise ValueError("unknown error handler name '%s'" % errors)
        ERROR_HANDLERS[errors](msg=err.message, error=type(err))


def is_code_insee(code, length=5, errors='ignore'):
    """Return whether or not code is a valid INSEE code as a bool.

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
       errors (str in 'ignore' (default), 'strict') = 'strict' raises an
           exception

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

    except Exception as err:
        if errors not in ('ignore', 'strict'):
            raise ValueError("unknown error handler name '%s'" % errors)
        ERROR_HANDLERS[errors](msg=err.message, error=type(err))


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

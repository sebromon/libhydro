# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 11:24:36 2017

@author: seb
"""

from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime


def interpolation_date(dt, dt1, v1, dt2, v2):
    """ Interpolation d'un valeur entre deux dates

    :param datetime dt: Date de l'interpolation
    :param dt1: Première date
    :param v1:  valeur associée à dt1
    :param dt2: Deuxième date
    :param v2: valeur associée à dt2
    :return: la valeur interpolée ou None si dt1=dt2
    :rtype: float ou None
    """
    v1 = float(v1)
    v2 = float(v2)
    delta_dt = (dt2 - dt1).total_seconds()
    # print(delta_dt)
    if delta_dt == 0:
        return None
    coeff = (v2 - v1) / delta_dt
    # print(coeff)
    # print((dt-dt1).total_seconds())
    return v1 + coeff * (dt - dt1).total_seconds()


def interpolation_date_from_value(val, dt1, val1, dt2, val2):
    """ Interpolation d'une date à partir d'une valeur et deux points

    :param val: valeur de l'interpolation
    :param dt1: Première date
    :param val1:  valeur associée à dt1
    :param dt2: Deuxième date
    :param val2: valeur associée à dt2
    :return: la date de l'interpolation
    :rtype: datetime.datetime ou None
    """
    val = float(val)
    val1 = float(val1)
    val2 = float(val2)
    if val1 == val2:
        raise ValueError(
            'val1 {} and val2 {} must be different for interpolation'.format(
                val1, val2))
    delta_dt = (dt2 - dt1).total_seconds()
    # print(delta_dt)
    if delta_dt == 0:
        raise ValueError(
            'dt1 {} and dt2 {} must be different for interpolation'.format(
                dt1, dt2))
    delta2 = (val - val1) * delta_dt / (val2 - val1)
    return dt1 + _datetime.timedelta(seconds=int(round(delta2)))


def interpolation(x, x1, y1, x2, y2):
    """ Interpolation linéaire entre deux points (x1,y1) et (x2,y2)

    :param float x: abscisse du point à interpoler
    :param float x1: abscisse du premier point
    :param float y1: ordonnée du premier point
    :param float x2: abscisse du deuxième point
    :param float y2: ordonnée du deuxième point

    :type: ordonnée du point interpolée ou None si x1=x2
    :rtype: float ou None

    """
    x = float(x)
    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)

    if x1 == x2:
        return None
    coeff = (y2 - y1) / (x2 - x1)
    return y1 + coeff * (x - x1)

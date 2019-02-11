# -*- coding: utf-8 -*-

"""Test program for module libhydro.processing.interpolation.

To run all tests just type:
    python -m unittest test_processing_interpolation

To run only a class test:
    python -m unittest test_processing_interpolation.TestClass

To run only a specific test:
    python -m unittest test_processing_interpolation.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import unittest
import datetime as _datetime
from libhydro.processing import interpolation as _interpolation


# -- strings ------------------------------------------------------------------
__version__ = '0.1'
__date__ = '2019-02-11'

# HISTORY
# V0.1 - SR - 2019-02-11
#   first shot


class TestInterpolation(unittest.TestCase):

    def test_interpolation_date(self):
        dt = _datetime.datetime(2016, 12, 1, 0, 30, 0)
        dt1 = _datetime.datetime(2016, 12, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2016, 12, 1, 1, 0, 0)
        res = _interpolation.interpolation_date(dt, dt1, 100, dt2, 200)
        self.assertAlmostEquals(res, 150.0, 5)
        dt = _datetime.datetime(2016, 12, 1, 2, 00, 0)
        res = _interpolation.interpolation_date(dt, dt1, 100, dt2, 200)
        self.assertAlmostEquals(res, 300.0, 5)

        dt2 = _datetime.datetime(2016, 12, 1, 0, 0, 0)
        res = _interpolation.interpolation_date(dt=dt, dt1=dt1, v1=100,
                                                dt2=dt2, v2=200)
        self.assertIsNone(res)

    def test_interpolation(self):

        res = _interpolation.interpolation(x=150, x1=100, y1=200,
                                           x2=200, y2=300)
        self.assertAlmostEquals(res, 250.0, 5)

        res = _interpolation.interpolation(x=150, x1=100.0, y1=200,
                                           x2=100.0, y2=300)
        self.assertIsNone(res)

    def test_interpolation_date_from_value(self):
        """test val between val1 and val2"""
        dt1 = _datetime.datetime(2016, 12, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2016, 12, 1, 1, 0, 0)
        dte = _interpolation.interpolation_date_from_value(
                val=150, dt1=dt1, val1=100, dt2=dt2, val2=200)
        self.assertEqual(dte, _datetime.datetime(2016, 12, 1 , 0, 30, 0))

    def test_interpolation_date_from_value_02(self):
        """test interpolation val < val1 and val2"""
        dt1 = _datetime.datetime(2016, 12, 1, 11, 0, 0)
        dt2 = _datetime.datetime(2016, 12, 1, 12, 0, 0)
        dte = _interpolation.interpolation_date_from_value(
                val=0, dt1=dt1, val1=100, dt2=dt2, val2=200)
        self.assertEqual(dte, _datetime.datetime(2016, 12, 1, 10, 0, 0))

        dte = _interpolation.interpolation_date_from_value(
                val=0, dt1=dt1, val1=200, dt2=dt2, val2=100)
        self.assertEqual(dte, _datetime.datetime(2016, 12, 1, 13, 0, 0))

    def test_interpolation_date_from_value_03(self):
        """test interpolation val > val1 and val2"""
        dt1 = _datetime.datetime(2016, 12, 1, 11, 0, 0)
        dt2 = _datetime.datetime(2016, 12, 1, 12, 0, 0)
        dte = _interpolation.interpolation_date_from_value(
                val=300, dt1=dt1, val1=100, dt2=dt2, val2=200)
        self.assertEqual(dte, _datetime.datetime(2016, 12, 1, 13, 0, 0))

        dte = _interpolation.interpolation_date_from_value(
                val=300, dt1=dt1, val1=200, dt2=dt2, val2=100)
        self.assertEqual(dte, _datetime.datetime(2016, 12, 1, 10, 0, 0))

    def test_interpolation_date_from_value_04(self):
        """test with val= val1 or val=val2"""
        dt1 = _datetime.datetime(2016, 12, 1, 11, 0, 0)
        dt2 = _datetime.datetime(2016, 12, 1, 12, 0, 0)
        dte = _interpolation.interpolation_date_from_value(
                val=100, dt1=dt1, val1=100, dt2=dt2, val2=200)
        self.assertEqual(dte, dt1)

        dte = _interpolation.interpolation_date_from_value(
                val=200, dt1=dt1, val1=100, dt2=dt2, val2=200)
        self.assertEqual(dte, dt2)

    def test_interpolation_date_from_value_05(self):
        """Test round seconds"""
        dt1 = _datetime.datetime(2016, 12, 1, 11, 0, 0)
        dt2 = _datetime.datetime(2016, 12, 1, 11, 0, 5)
        dte = _interpolation.interpolation_date_from_value(
                val=160, dt1=dt1, val1=100, dt2=dt2, val2=200)
        self.assertEqual(dte, _datetime.datetime(2016, 12, 1, 11, 0, 3))

    def test_error_interpolation_date_from_value(self):
        """Test round seconds"""
        dt1 = _datetime.datetime(2016, 12, 1, 11, 0, 0)
        dt2 = _datetime.datetime(2016, 12, 1, 11, 0, 5)
        val = 150
        val1 = 100
        val2 = 200
        _interpolation.interpolation_date_from_value(
                val=val, dt1=dt1, val1=val1, dt2=dt2, val2=val2)
        # values error
        with self.assertRaises(ValueError):
            _interpolation.interpolation_date_from_value(
                val=val, dt1=dt1, val1=val1, dt2=dt2, val2=val1)
        # dates error
        with self.assertRaises(ValueError):
            _interpolation.interpolation_date_from_value(
                val=val, dt1=dt1, val1=val1, dt2=dt1, val2=val2)

# -*- coding: utf-8 -*-
"""Test program for csv converter.

To run all tests just type:
    python -m unittest test_conv_csv

To run only a class test:
    python -m unittest test_conv_csv.TestClass

To run only a specific test:
    python -m unittest test_conv_csv.TestClass.test_method

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys
import os
import csv
sys.path.append(os.path.join('..', '..'))

import unittest
# import datetime
# import pandas

from libhydro.conv import csv as lhcsv
# from libhydro.core import sitehydro


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-12-16"""

#HISTORY
#V0.1 - 2014-12-16
#    first shot


#-- config --------------------------------------------------------------------
# SRC = os.path.join('data', 'csv', 'LOCMARIAQUER.hfs')


#-- class TestMapKeys ---------------------------------------------------------
class TestMapKeys(unittest.TestCase):

    """MapKeys class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.base = {'a': 1, 'b': 2, 'c': 3, 'n': ''}

    def test_base(self):
        """Base test."""
        mapper = {'a': 'aa', 'b': 'bb', 'c': 'cc', 'd': 'dd', 'n': 'nn'}
        self.assertEqual(
            lhcsv._map_keys(self.base, mapper),
            {'aa': 1, 'bb': 2, 'cc': 3}
        )

    def test_none_mapper_keys(self):
        """None mapper key test."""
        mapper = {'a': 'aa', 'b': None, 'c': 'cc', 'd': 'dd'}
        self.assertEqual(
            lhcsv._map_keys(self.base, mapper),
            {'aa': 1, 'cc': 3}
        )
        mapper = {'a': None, 'b': None, 'c': None, 'd': 'dd'}
        self.assertEqual(
            lhcsv._map_keys(self.base, mapper),
            {}
        )

    def test_strict_and_loose(self):
        """Strict and loose mode test."""
        mapper = {'b': 'bb', 'c': 'cc', 'd': 'dd'}
        self.assertEqual(
            lhcsv._map_keys(self.base, mapper, strict=False),
            {'bb': 2, 'cc': 3}
        )
        mapper = {}
        self.assertEqual(
            lhcsv._map_keys(self.base, mapper, strict=False),
            {}
        )
        with self.assertRaises(csv.Error):
            lhcsv._map_keys(self.base, mapper, strict=True),

    def test_ietrator(self):
        """Iterator test."""
        mapper = {'a': 'aa', 'b': 'bb', 'c': 'cc', 'd': 'dd'}
        self.assertEqual(
            lhcsv._map_keys(self.base, mapper, iterator='items'),
            lhcsv._map_keys(self.base, mapper, iterator='iteritems'),
        )
        with self.assertRaises(AttributeError):
            lhcsv._map_keys(self.base, mapper, iterator='')

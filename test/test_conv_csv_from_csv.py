# -*- coding: utf-8 -*-
"""Test program for csv._from_csv converter.

To run all tests just type:
    python -m unittest test_conv_csv_from_csv

To run only a class test:
    python -m unittest test_conv_csv_from_csv.TestClass

To run only a specific test:
    python -m unittest test_conv_csv_from_csv.TestClass.test_method

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
sys.path.append(os.path.join('..', '..'))

import csv
import unittest

from libhydro.conv.csv import _from_csv as lhcsv


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-12-16"""

#HISTORY
#V0.1 - 2014-12-16
#    first shot

CSV_DIR = os.path.join('data', 'csv')


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


#-- class TestFromCsv ---------------------------------------------------------
class TestFromCsv(unittest.TestCase):

    """FromCsv class tests."""

    def test_base(self):
        """Quick read all hydrometrie files test."""
        files = (
            # fname,            data,         encoding
            ('siteshydro_full', 'siteshydro', 'utf-8'),
            ('siteshydro_full_8859-1', 'siteshydro', 'latin1'),
            ('siteshydro_minimum', 'siteshydro', 'utf-8'),
            ('siteshydro_partial', 'siteshydro', 'utf-8'),
            # TODO sitesmeteo, serieshydro, seriesmeteo
        )
        for f in files:
            fname = os.path.join(CSV_DIR, '{}.csv'.format(f[0]))
            lhcsv.from_csv(fname=fname, data=f[1], encoding=f[2])


#-- class TestSitesHydroFromCsv -----------------------------------------------
class TestsitesHydroFromCsv(unittest.TestCase):

    """SitesHydroFromCsv class tests."""

    def test_base(self):
        """Base test."""
        fname = os.path.join(CSV_DIR, 'siteshydro_minimum.csv')
        # merge = True
        siteshydro = lhcsv.siteshydro_from_csv(fname)
        self.assertEqual(len(siteshydro), 4)
        self.assertEqual(siteshydro[1].code, 'A0330810')
        self.assertEqual(len(siteshydro[3].stations), 3)
        self.assertEqual(siteshydro[3].stations[2].code, 'W001102512')
        # merge = False
        siteshydro = lhcsv.siteshydro_from_csv(fname, merge=False)
        self.assertEqual(len(siteshydro), 8)
        self.assertEqual(siteshydro[2].code, 'A0330810')
        self.assertEqual(len(siteshydro[6].stations), 1)
        self.assertEqual(siteshydro[6].stations[0].code, 'W001102511')

#2

#3

#4
        #5
        #free format
        #g=c.siteshydro_from_csv('test/data/csv/siteshydro_free.csv', mapping={'sitehydro': {'Code':'code'}}, delimiter=',')

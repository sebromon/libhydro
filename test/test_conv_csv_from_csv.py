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
__version__ = """0.1c"""
__date__ = """2014-12-19"""

#HISTORY
#V0.1 - 2014-12-16
#    first shot

#-- config --------------------------------------------------------------------
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
            lhcsv.map_keys(self.base, mapper),
            {'aa': 1, 'bb': 2, 'cc': 3}
        )

    def test_none_mapper_keys(self):
        """None mapper key test."""
        mapper = {'a': 'aa', 'b': None, 'c': 'cc', 'd': 'dd'}
        self.assertEqual(
            lhcsv.map_keys(self.base, mapper),
            {'aa': 1, 'cc': 3}
        )
        mapper = {'a': None, 'b': None, 'c': None, 'd': 'dd'}
        self.assertEqual(
            lhcsv.map_keys(self.base, mapper),
            {}
        )

    def test_strict_and_loose(self):
        """Strict and loose mode test."""
        mapper = {'b': 'bb', 'c': 'cc', 'd': 'dd'}
        self.assertEqual(
            lhcsv.map_keys(self.base, mapper, strict=False),
            {'bb': 2, 'cc': 3}
        )
        mapper = {}
        self.assertEqual(
            lhcsv.map_keys(self.base, mapper, strict=False),
            {}
        )
        with self.assertRaises(csv.Error):
            lhcsv.map_keys(self.base, mapper, strict=True),

    def test_ietrator(self):
        """Iterator test."""
        mapper = {'a': 'aa', 'b': 'bb', 'c': 'cc', 'd': 'dd'}
        self.assertEqual(
            lhcsv.map_keys(self.base, mapper, iterator='items'),
            lhcsv.map_keys(self.base, mapper, iterator='iteritems'),
        )
        with self.assertRaises(AttributeError):
            lhcsv.map_keys(self.base, mapper, iterator='')


#-- class TestSitesHydroFromCsv -----------------------------------------------
class TestSitesHydroFromCsv(unittest.TestCase):

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

    def test_full(self):
        """Full csv file test."""
        fname = os.path.join(CSV_DIR, 'siteshydro_full.csv')
        # merge = True
        siteshydro = lhcsv.siteshydro_from_csv(fname)
        self.assertEqual(len(siteshydro), 3)
        self.assertEqual(siteshydro[1].code, 'W8230456')
        self.assertEqual(len(siteshydro[1].stations), 1)
        self.assertEqual(siteshydro[1].stations[0].commune, '2A002')
        # merge = False
        self.assertEqual(len(siteshydro), 3)
        self.assertEqual(siteshydro[2].code, 'A0330810')
        self.assertEqual(len(siteshydro[2].stations), 0)
        self.assertEqual(siteshydro[2].coord.x, 892000.5)
        self.assertEqual(siteshydro[2].coord.y, 2445000.1)

    def test_encoding(self):
        """Encoding test."""
        fname = os.path.join(CSV_DIR, 'siteshydro_full_8859-1.csv')
        siteshydro = lhcsv.siteshydro_from_csv(fname, encoding='latin1')
        ref = os.path.join(CSV_DIR, 'siteshydro_full.csv')
        sitesref = lhcsv.siteshydro_from_csv(ref)
        self.assertEqual(siteshydro, sitesref)

    def test_partial(self):
        """Partial csv file test."""
        fname = os.path.join(CSV_DIR, 'siteshydro_partial.csv')
        # merge = True
        siteshydro = lhcsv.siteshydro_from_csv(fname)
        self.assertEqual(len(siteshydro), 5)
        self.assertEqual(siteshydro[1].code, 'D0137011')
        self.assertEqual(siteshydro[3].typesite, 'REEL')
        self.assertEqual(siteshydro[3].libelle, 'Site hydrométrique 4')
        # merge = False
        siteshydro = lhcsv.siteshydro_from_csv(fname, merge=False)
        self.assertEqual(len(siteshydro), 5)
        self.assertEqual(siteshydro[1].code, 'D0137011')
        self.assertEqual(siteshydro[3].typesite, 'REEL')
        self.assertEqual(siteshydro[3].libelle, 'Site hydrométrique 4')

    def test_free(self):
        """Free format test."""
        fname = os.path.join(CSV_DIR, 'siteshydro_free.csv')
        # merge = True
        siteshydro = lhcsv.siteshydro_from_csv(
            fname,
            merge=True,
            flag=None, second_line=None, decimal=None,
            mapper={
                'libhydro.core.sitehydro.Sitehydro': {
                    'code': 'code', 'label': 'libelle', 'family': 'typesite'
                },
                'libhydro.core.sitehydro.Sitehydro.coord': {
                    'x': 'x', 'y': 'y', 'proj': 'proj'
                }
            },
            delimiter=b',',  # byte !
            escapechar=b'\\'
        )
        self.assertEqual(len(siteshydro), 4)
        self.assertEqual(siteshydro[3].code, 'D0137014')
        self.assertEqual(siteshydro[2].typesite, 'VIRTUEL')
        self.assertEqual(len(siteshydro[3].stations), 0)
        self.assertTrue(',' in siteshydro[3].libelle)
        self.assertEqual(siteshydro[3].coord.x, 50.55)
        self.assertEqual(siteshydro[3].coord.y, 51.5)
        # merge = True and no mapper for coord
        siteshydro = lhcsv.siteshydro_from_csv(
            fname,
            merge=True,
            flag=None, second_line=None, decimal=None,
            mapper={
                'libhydro.core.sitehydro.Sitehydro': {
                    'code': 'code', 'label': 'libelle', 'family': 'typesite'
                },
            },
            delimiter=b',',  # byte !
            escapechar=b'\\'
        )
        self.assertEqual(len(siteshydro), 4)
        self.assertEqual(siteshydro[3].code, 'D0137014')
        self.assertEqual(siteshydro[2].typesite, 'VIRTUEL')
        self.assertEqual(len(siteshydro[3].stations), 0)
        self.assertTrue(',' in siteshydro[3].libelle)
        self.assertIsNone(siteshydro[3].coord)
        # merge = False
        siteshydro = lhcsv.siteshydro_from_csv(
            fname,
            merge=False,
            flag=None, second_line=None, decimal=None,
            mapper={
                'libhydro.core.sitehydro.Sitehydro': {
                    'code': 'code', 'label': 'libelle', 'family': 'typesite'
                },
                'libhydro.core.sitehydro.Sitehydro.coord': {
                    'x': 'x', 'y': 'y', 'proj': 'proj'
                }
            },
            delimiter=b',',  # byte !
            escapechar=b'\\'
        )
        self.assertEqual(len(siteshydro), 5)
        self.assertEqual(siteshydro[4].code, 'D0137014')
        self.assertEqual(siteshydro[3].typesite, 'VIRTUEL')
        self.assertEqual(len(siteshydro[4].stations), 0)
        self.assertTrue(',' in siteshydro[4].libelle)
        self.assertEqual(siteshydro[4].coord.x, 50.55)
        self.assertEqual(siteshydro[4].coord.y, 51.5)


#-- class TestSitesMeteoFromCsv -----------------------------------------------
class TestSitesMeteoFromCsv(unittest.TestCase):

    """SitesMeteoFromCsv class tests."""

    def test_base(self):
        """Base test."""
        fname = os.path.join(CSV_DIR, 'sitesmeteo_minimum.csv')
        # merge = True
        sitesmeteo = lhcsv.sitesmeteo_from_csv(fname)
        self.assertEqual(len(sitesmeteo), 4)
        self.assertEqual(sitesmeteo[0].code, '185238001')
        self.assertEqual(sitesmeteo[3].code, '185238004')
        # merge = False
        sitesmeteo = lhcsv.sitesmeteo_from_csv(fname, merge=False)
        self.assertEqual(len(sitesmeteo), 8)
        self.assertEqual(sitesmeteo[2].code, '185238002')
        self.assertEqual(sitesmeteo[7].code, '185238004')

    def test_full(self):
        """Full csv file test."""
        fname = os.path.join(CSV_DIR, 'sitesmeteo_full.csv')
        # merge = True
        sitesmeteo = lhcsv.sitesmeteo_from_csv(fname)
        self.assertEqual(len(sitesmeteo), 2)
        self.assertEqual(sitesmeteo[0].code, '285238001')
        self.assertEqual(sitesmeteo[1].code, '285238002')
        self.assertEqual(sitesmeteo[0].commune, '85238')
        self.assertEqual(sitesmeteo[1].commune, '65748')
        # merge = False
        sitesmeteo = lhcsv.sitesmeteo_from_csv(fname, merge=False)
        self.assertEqual(len(sitesmeteo), 2)
        self.assertEqual(sitesmeteo[0].code, '285238001')
        self.assertEqual(sitesmeteo[1].code, '285238002')
        self.assertEqual(sitesmeteo[0].commune, '85238')
        self.assertEqual(sitesmeteo[1].commune, '65748')

    def test_bad(self):
        """Bad csv file test."""
        fname = os.path.join(CSV_DIR, 'sitesmeteo_bad.csv')
        with self.assertRaises(csv.Error):
            lhcsv.sitesmeteo_from_csv(fname)

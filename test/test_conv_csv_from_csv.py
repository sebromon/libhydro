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
__version__ = """0.5b"""
__date__ = """2014-12-29"""

#HISTORY
#V0.5 - 2014-12-20
#    add serieshydro tests
#    add seriesmeteo tests
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


#-- class TestSeriesHydroFromCsv ----------------------------------------------
class TestSeriesHydroFromCsv(unittest.TestCase):

    """SeriesHydroFromCsv class tests."""

    def test_base(self):
        """Base test."""
        fname = os.path.join(CSV_DIR, 'serieshydro_minimum.csv')
        # merge = True
        serieshydro = lhcsv.serieshydro_from_csv(fname)
        self.assertEqual(len(serieshydro), 2)
        self.assertEqual(serieshydro[0].entite.code, 'O8231530')
        self.assertEqual(serieshydro[1].entite.code, 'A0330101')
        self.assertEqual(serieshydro[0].grandeur, 'Q')
        self.assertEqual(serieshydro[1].grandeur, 'Q')
        self.assertEqual(
            serieshydro[0].observations.loc['2010-10-02 05:00', 'res'],
            55.3
        )
        self.assertEqual(
            serieshydro[0].observations.loc['2010-10-02 06:00', 'res'],
            55.8
        )
        # merge = False
        serieshydro = lhcsv.serieshydro_from_csv(fname, merge=False)
        self.assertEqual(len(serieshydro), 4)
        self.assertEqual(serieshydro[0].entite.code, 'O8231530')
        self.assertEqual(serieshydro[1].entite.code, 'O8231530')
        self.assertEqual(serieshydro[2].entite.code, 'A0330101')
        self.assertEqual(serieshydro[3].entite.code, 'A0330101')
        self.assertEqual(
            serieshydro[3].observations.loc['2010-10-02 09:00', 'res'],
            55
        )

    def test_full(self):
        """Full csv file test."""
        fname = os.path.join(CSV_DIR, 'serieshydro_full.csv')
        # merge = True
        serieshydro = lhcsv.serieshydro_from_csv(fname, decimal=b',')
        self.assertEqual(len(serieshydro), 5)
        self.assertEqual(serieshydro[0].entite.code, 'A2331020')
        self.assertEqual(serieshydro[1].entite.code, 'R789122010')
        self.assertEqual(serieshydro[4].entite.code, 'O823153001')
        self.assertEqual(serieshydro[0].grandeur, 'Q')
        self.assertEqual(serieshydro[1].grandeur, 'H')
        self.assertEqual(serieshydro[0].statut, 0)
        self.assertEqual(serieshydro[4].statut, 4)
        self.assertEqual(
            serieshydro[0].observations.loc['1999-02-13 05', 'res'].get(0),
            123.33
        )
        self.assertEqual(
            serieshydro[0].observations.loc['1999-02-13 05', 'mth'].get(0),
            0
        )
        # merge = False
        serieshydro = lhcsv.serieshydro_from_csv(fname, decimal=b',', merge=0)
        self.assertEqual(len(serieshydro), 6)
        self.assertEqual(serieshydro[0].entite.code, 'A2331020')
        self.assertEqual(serieshydro[1].entite.code, 'R789122010')
        self.assertEqual(serieshydro[4].entite.code, 'O823153001')
        self.assertEqual(serieshydro[0].grandeur, 'Q')
        self.assertEqual(serieshydro[1].grandeur, 'H')
        self.assertEqual(serieshydro[0].statut, 0)
        self.assertEqual(serieshydro[5].statut, 8)
        self.assertEqual(
            serieshydro[0].observations.loc['1999-02-13 05', 'res'].get(0),
            123.33
        )
        self.assertEqual(
            serieshydro[0].observations.loc['1999-02-13 05', 'mth'].get(0),
            0
        )


#-- class TestSeriesMeteoFromCsv ----------------------------------------------
class TestSeriesMeteoFromCsv(unittest.TestCase):

    """SeriesMeteoFromCsv class tests."""

    def test_base(self):
        """Base test."""
        fname = os.path.join(CSV_DIR, 'seriesmeteo_minimum.csv')
        # merge = True
        seriesmeteo = lhcsv.seriesmeteo_from_csv(fname)
        self.assertEqual(len(seriesmeteo), 1)
        self.assertEqual(seriesmeteo[0].grandeur.typemesure, 'VV')
        self.assertEqual(seriesmeteo[0].grandeur.sitemeteo.code, '031239004')
        self.assertEqual(
            seriesmeteo[0].observations.loc['2011-02-02 15:00', 'res'],
            100
        )
        self.assertEqual(
            seriesmeteo[0].observations.loc['2011-02-02 18:00', 'res'],
            82.56
        )
        # merge = False
        seriesmeteo = lhcsv.seriesmeteo_from_csv(fname, merge=False)
        self.assertEqual(len(seriesmeteo), 4)
        for i in range(4):
            self.assertEqual(seriesmeteo[i].grandeur.typemesure, 'VV')
            self.assertEqual(
                seriesmeteo[0].grandeur.sitemeteo.code, '031239004'
            )
            self.assertEqual(
                seriesmeteo[i].grandeur.sitemeteo.code, '031239004'
            )
            self.assertEqual(len(seriesmeteo[i].observations), 1)
        self.assertEqual(
            seriesmeteo[0].observations.loc['2011-02-02 15:00', 'res'],
            100
        )
        self.assertEqual(
            seriesmeteo[1].observations.loc['2011-02-02 16:00', 'res'],
            852
        )
        self.assertEqual(
            seriesmeteo[2].observations.loc['2011-02-02 17:00', 'res'],
            5
        )
        self.assertEqual(
            seriesmeteo[3].observations.loc['2011-02-02 18:00', 'res'],
            82.56
        )

    def test_full(self):
        """Full csv file test."""
        fname = os.path.join(CSV_DIR, 'seriesmeteo_full.csv')
        # merge = True
        seriesmeteo = lhcsv.seriesmeteo_from_csv(fname, decimal=b',')
        self.assertEqual(len(seriesmeteo), 3)
        self.assertEqual(seriesmeteo[0].grandeur.typemesure, 'VV')
        self.assertEqual(seriesmeteo[1].grandeur.typemesure, 'RR')
        self.assertEqual(seriesmeteo[2].grandeur.typemesure, 'RR')
        self.assertEqual(seriesmeteo[0].grandeur.sitemeteo.code, '02A004001')
        self.assertEqual(seriesmeteo[1].grandeur.sitemeteo.code, '031239004')
        self.assertEqual(seriesmeteo[2].grandeur.sitemeteo.code, '031239004')
        self.assertEqual(seriesmeteo[0].statut, 0)
        self.assertEqual(seriesmeteo[1].statut, 4)
        self.assertEqual(seriesmeteo[2].statut, 8)
        self.assertEqual(len(seriesmeteo[0].observations), 2)
        self.assertEqual(len(seriesmeteo[1].observations), 2)
        self.assertEqual(len(seriesmeteo[2].observations), 2)
        self.assertEqual(
            seriesmeteo[0].observations.to_string().split('\n')[2:],
            [
                '2011-02-02 14:00:00  10.1    0   16   55',
                '2011-02-02 14:05:00  20.0    4   16   66'
            ]
        )
        self.assertEqual(
            seriesmeteo[1].observations.to_string().split('\n')[2:],
            [
                '2011-02-02 14:00:00   30   12   16  100',
                '2011-02-02 15:00:00   40    0   16   75'
            ]
        )
        self.assertEqual(
            seriesmeteo[2].observations.to_string().split('\n')[2:],
            [
                '2011-02-02 16:00:00  50.5    8   16  100',
                '2011-02-02 17:00:00   0.0    8   16  100'
            ]
        )
        # merge = False
        seriesmeteo = lhcsv.seriesmeteo_from_csv(fname, decimal=b',', merge=0)
        self.assertEqual(len(seriesmeteo), 6)
        self.assertEqual(seriesmeteo[0].grandeur.typemesure, 'VV')
        self.assertEqual(seriesmeteo[1].grandeur.typemesure, 'VV')
        self.assertEqual(seriesmeteo[3].grandeur.typemesure, 'RR')
        self.assertEqual(seriesmeteo[5].grandeur.typemesure, 'RR')
        self.assertEqual(seriesmeteo[0].grandeur.sitemeteo.code, '02A004001')
        self.assertEqual(seriesmeteo[2].grandeur.sitemeteo.code, '031239004')
        self.assertEqual(seriesmeteo[5].grandeur.sitemeteo.code, '031239004')
        self.assertEqual(seriesmeteo[1].statut, 0)
        self.assertEqual(seriesmeteo[3].statut, 4)
        self.assertEqual(seriesmeteo[5].statut, 8)
        self.assertEqual(len(seriesmeteo[0].observations), 1)
        self.assertEqual(len(seriesmeteo[3].observations), 1)
        self.assertEqual(len(seriesmeteo[5].observations), 1)
        self.assertEqual(
            seriesmeteo[0].observations.to_string().split('\n')[2:],
            [
                '2011-02-02 14:00:00  10.1    0   16   55',
            ]
        )
        self.assertEqual(
            seriesmeteo[1].observations.to_string().split('\n')[2:],
            [
                '2011-02-02 14:05:00   20    4   16   66'
            ]
        )
        self.assertEqual(
            seriesmeteo[4].observations.to_string().split('\n')[2:],
            [
                '2011-02-02 16:00:00  50.5    8   16  100',
            ]
        )
        self.assertEqual(
            seriesmeteo[5].observations.to_string().split('\n')[2:],
            [
                '2011-02-02 17:00:00    0    8   16  100'
            ]
        )

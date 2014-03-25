# -*- coding: utf-8 -*-
"""Test program for shom converter.

To run all tests just type:
    './test_conv_shom.py' or 'python test_conv_shom.py'

To run only a class test:
    python -m unittest test_conv_shom.TestClass

To run only a specific test:
    python -m unittest test_conv_shom.TestClass
    python -m unittest test_conv_shom.TestClass.test_method

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

import unittest
import datetime
import pandas

from libhydro.conv import shom
from libhydro.core import sitehydro


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1c"""
__date__ = """2014-02-25"""

#HISTORY
#V0.1 - 2013-08-16
#    first shot


#-- config --------------------------------------------------------------------
SRC = os.path.join('data', 'shom', 'LOCMARIAQUER.hfs')


#-- class TestSimulationFromHFS -----------------------------------------------
class TestSimulationFromHSF(unittest.TestCase):

    """SimulationFromHFS class tests."""

    def test_base_01(self):
        """Base test."""
        sim = shom.simulation_from_hfs(SRC)
        self.assertEqual(
            (sim.entite.code, sim.entite.typestation, sim.entite.libelle),
            (None, 'LIMNI', 'LOCMARIAQUER')
        )
        self.assertEqual(
            (sim.grandeur, sim.qualite, sim.commentaire),
            ('H', 100, 'data SHOM')
        )
        self.assertEqual(sim.modeleprevision.code, 'SCnMERshom')
        self.assertEqual(len(sim.previsions), 144)
        self.assertEqual(
            (sim.previsions[10], sim.previsions.index[10]),
            (3.71, (datetime.datetime(2013, 1, 23, 1, 40), 50))
        )

    def test_base_02(self):
        """Second base test."""
        station = sitehydro.Stationhydro(code='-', libelle='LOC', strict=False)
        dtprod = datetime.datetime(2010, 12, 12, 15, 33)
        sim = shom.simulation_from_hfs(
            src=SRC,
            stationhydro=station,
            begin='2013-01-23 12:00',
            end='2013-01-23 12:25',
            dtprod=dtprod
        )
        self.assertEqual(sim.entite, station)
        self.assertEqual(
            (sim.grandeur, sim.qualite, sim.commentaire, sim.dtprod),
            ('H', 100, 'data SHOM', dtprod)
        )
        self.assertEqual(sim.modeleprevision.code, 'SCnMERshom')
        self.assertEqual(len(sim.previsions), 3)
        self.assertEqual(
            (sim.previsions[1], sim.previsions.index[1]),
            (3.34, (datetime.datetime(2013, 1, 23, 12, 10), 50))
        )

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        sim = shom.simulation_from_hfs(
            src=SRC,
            stationhydro='X1',
            strict=False
        )
        self.assertEqual(sim.entite, 'X1')

    def test_error_01(self):
        """Dtprod error."""
        self.assertRaises(
            ValueError,
            shom.simulation_from_hfs,
            # **{'src': SRC, 'dtprod': '2013-01-01'}
            **{'src': SRC, 'dtprod': '2013-1-1'}
        )


#-- class TestSerieFromHFS -----------------------------------------------
class TestSerieFromHSF(unittest.TestCase):

    """SerieFromHFS class tests."""

    def test_base_01(self):
        """Base test."""
        serie = shom.serie_from_hfs(SRC)
        self.assertEqual(
            (
                serie.entite.code, serie.entite.typestation,
                serie.entite.libelle
            ),
            (None, 'LIMNI', 'LOCMARIAQUER')
        )
        self.assertEqual(
            (serie.grandeur, serie.statut),
            ('H', 0)
        )
        self.assertEqual(len(serie.observations), 144)
        self.assertEqual(
            (serie.observations.irow(10).item(), serie.observations.irow(10).name),
            (3.71, datetime.datetime(2013, 1, 23, 1, 40))
        )

    def test_base_02(self):
        """Second base test."""
        station = sitehydro.Stationhydro(code='X231101001', libelle='LOC')
        serie = shom.serie_from_hfs(
            src=SRC,
            stationhydro=station,
            begin='2013-01-23 12:00',
            end='2013-01-23 12:25'
        )
        self.assertEqual(serie.entite, station)
        self.assertEqual(
            (serie.grandeur, serie.statut),
            ('H', 0)
        )
        self.assertEqual(len(serie.observations), 3)
        self.assertEqual(
            (serie.observations.irow(1).item(), serie.observations.irow(1).name),
            (3.34, datetime.datetime(2013, 1, 23, 12, 10))
        )

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        serie = shom.serie_from_hfs(
            src=SRC,
            stationhydro='X1',
            strict=False
        )
        self.assertEqual(serie.entite, 'X1')
        self.assertEqual(
            (serie.grandeur, serie.statut),
            ('H', 0)
        )
        self.assertEqual(len(serie.observations), 144)
        self.assertEqual(
            (serie.observations.irow(73).item(), serie.observations.irow(73).name),
            (3.34, datetime.datetime(2013, 1, 23, 12, 10))
        )

    def test_error_01(self):
        """Src error."""
        self.assertRaises(
            IOError,
            shom.serie_from_hfs,
            **{'src': 'LOCMARI'}
        )

    def test_error_02(self):
        """Check dates format error."""
        self.assertRaises(
            pandas.tseries.tools.DateParseError,
            shom.serie_from_hfs,
            # **{'src': SRC, 'begin': '2013-1-1'}
            **{'src': SRC, 'begin': '20131'}
        )
        self.assertRaises(
            pandas.tseries.tools.DateParseError,
            shom.serie_from_hfs,
            # **{'src': SRC, 'end': '2013-1-25'}
            **{'src': SRC, 'end': '20131'}
        )

    def test_error_03(self):
        """Check dates values error."""
        self.assertRaises(
            ValueError,
            shom.serie_from_hfs,
            # **{'src': SRC, 'begin': '2013-1-1'}
            **{'src': SRC, 'begin': '2013-1-25'}
        )
        self.assertRaises(
            ValueError,
            shom.serie_from_hfs,
            # **{'src': SRC, 'end': '2013-1-25'}
            **{'src': SRC, 'end': '2013-1-22'}
        )

    def test_error_04(self):
        """Entity error."""
        station = sitehydro.Stationhydro(code='X1', strict=False)
        shom.serie_from_hfs(
            src=SRC,
            stationhydro=station
        )
        self.assertRaises(
            TypeError,
            shom.serie_from_hfs,
            **{'src': SRC, 'stationhydro': 33}
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

# coding: utf-8
"""Test program for shom converter.

To run all tests just type:
    python -m unittest test_conv_shom

To run only a class test:
    python -m unittest test_conv_shom.TestClass

To run only a specific test:
    python -m unittest test_conv_shom.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import os
import unittest
import datetime
import pandas

from libhydro.conv import shom
from libhydro.core import sitehydro


# -- strings ------------------------------------------------------------------
# version = 0.3.0
# date = 2018-12-11

# HISTORY
# V0.3 - 2018-12-11
#   h10 codec tests
# V0.2 - 2017-05-04
#   fix some deprecated warnings
# V0.1 - 2013-08-16
#   first shot


# -- config -------------------------------------------------------------------
PATH = os.path.join('data', 'shom')
SRC = {'hfs': os.path.join(PATH, 'LOCMARIAQUER.hfs'),
       'h10': os.path.join(PATH, 'BORDEAUX.h10')}


# -- class TestSimulationFromHFS ----------------------------------------------
class TestSimulationFromHSF(unittest.TestCase):

    """Class SimulationFromHFS."""

    def test_base_01(self):
        """Base test."""
        sim = shom.simulation_from_hfs(
            src=SRC['hfs'], codemodeleprevision='00nMERSHOM')
        self.assertEqual(
            (sim.entite.code, sim.entite.typestation, sim.entite.libelle),
            (None, 'LIMNI', 'LOCMARIAQUER'))
        self.assertEqual(
            (sim.grandeur, sim.qualite, sim.commentaire),
            ('H', 100, 'data SHOM'))
        self.assertEqual(sim.modeleprevision.code, '00nMERSHOM')
        self.assertEqual(len(sim.previsions_tend), 144)
        self.assertEqual(
            (sim.previsions_tend[10], sim.previsions_tend.index[10]),
            (3710, (datetime.datetime(2013, 1, 23, 1, 40), 'moy')))

    def test_base_02(self):
        """Second base test."""
        station = sitehydro.Station(code='-', libelle='LOC', strict=False)
        dtprod = datetime.datetime(2010, 12, 12, 15, 33)
        sim = shom.simulation_from_hfs(
            src=SRC['hfs'], station=station, codemodeleprevision='00nMERSHOM',
            begin='2013-01-23 12:00', end='2013-01-23 12:25',
            dtprod=dtprod)
        self.assertEqual(sim.entite, station)
        self.assertEqual(
            (sim.grandeur, sim.qualite, sim.commentaire, sim.dtprod),
            ('H', 100, 'data SHOM', dtprod))
        self.assertEqual(sim.modeleprevision.code, '00nMERSHOM')
        self.assertEqual(len(sim.previsions_tend), 3)
        self.assertEqual(
            (sim.previsions_tend[1], sim.previsions_tend.index[1]),
            (3340, (datetime.datetime(2013, 1, 23, 12, 10), 'moy')))

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        sim = shom.simulation_from_hfs(
            src=SRC['hfs'], station='X1', strict=False,
            codemodeleprevision='00nMERSHOM')
        self.assertEqual(sim.entite, 'X1')

    def test_error_01(self):
        """Dtprod error."""
        with self.assertRaises(ValueError):
            shom.simulation_from_hfs(
            # **{'src': SRC['hfs'], 'dtprod': '2013-01-01',
            **{'src': SRC['hfs'], 'dtprod': '2013-1-1',
               'codemodeleprevision': '00nMERSHOM'})


# -- class TestSerieFromHFS ---------------------------------------------------
class TestSerieFromHSF(unittest.TestCase):

    """Class SerieFromHFS."""

    def test_base_01(self):
        """Base test."""
        serie = shom.serie_from_hfs(SRC['hfs'])
        self.assertEqual(
            (serie.entite.code, serie.entite.typestation,
             serie.entite.libelle),
            (None, 'LIMNI', 'LOCMARIAQUER'))
        self.assertEqual(serie.grandeur, 'H')
        self.assertEqual(len(serie.observations), 144)
        self.assertEqual(
            (serie.observations.iloc[100].item(),
             serie.observations.iloc[100].name),
            (3040, datetime.datetime(2013, 1, 23, 16, 40)))

    def test_base_02(self):
        """Second base test."""
        station = sitehydro.Station(code='X231101001', libelle='LOC')
        serie = shom.serie_from_hfs(
            src=SRC['hfs'], station=station,
            begin='2013-01-23 20:05', end='2013-01-23 20:35')
        self.assertEqual(serie.entite, station)
        self.assertEqual(serie.grandeur, 'H')
        self.assertEqual(len(serie.observations), 3)
        self.assertEqual(
            (serie.observations.iloc[1].item(),
             serie.observations.iloc[1].name),
            (1550, datetime.datetime(2013, 1, 23, 20, 20)))

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        serie = shom.serie_from_hfs(
            src=SRC['hfs'], station='X1', strict=False)
        self.assertEqual(serie.entite, 'X1')
        self.assertEqual(serie.grandeur, 'H')
        self.assertEqual(len(serie.observations), 144)
        self.assertEqual(
            (serie.observations.iloc[73].item(),
             serie.observations.iloc[73].name),
            (3340, datetime.datetime(2013, 1, 23, 12, 10)))

    def test_error_01(self):
        """Src error."""
        with self.assertRaises(IOError):
            shom.serie_from_hfs(src='LOCMARI')

    def test_error_02(self):
        """Check dates format error."""
        with self.assertRaises(ValueError):
            # pandas.tseries.tools.DateParseError,
            shom.serie_from_hfs(
            # **{'src': SRC['hfs'], 'begin': '2013-1-1'}
            **{'src': SRC['hfs'], 'begin': '20131'})
        with self.assertRaises(ValueError):
            # pandas.tseries.tools.DateParseError,
            shom.serie_from_hfs(
            # **{'src': SRC['hfs'], 'end': '2013-1-25'}
            **{'src': SRC['hfs'], 'end': '20131'})

    def test_error_03(self):
        """Check dates values error."""
        with self.assertRaises(ValueError):
            shom.serie_from_hfs(
            # **{'src': SRC['hfs'], 'begin': '2013-1-1'}
            **{'src': SRC['hfs'], 'begin': '2013-1-25'})
        with self.assertRaises(ValueError):
            shom.serie_from_hfs(
            # **{'src': SRC['hfs'], 'end': '2013-1-25'}
            **{'src': SRC['hfs'], 'end': '2013-1-22'})

    def test_error_04(self):
        """Entity error."""
        station = sitehydro.Station(code='X1', strict=False)
        shom.serie_from_hfs(
            src=SRC['hfs'], station=station)
        with self.assertRaises(TypeError):
            shom.serie_from_hfs(**{'src': SRC['hfs'], 'station': 33})


# -- class TestSimulationFromH10 ----------------------------------------------
class TestSimulationFromH10(unittest.TestCase):

    """Class SimulationFromH10."""

    def test_base_01(self):
        """Base test."""
        sim = shom.simulation_from_h10(
            src=SRC['h10'], codemodeleprevision='00nMERSHOM')
        self.assertEqual(
            (sim.entite.code, sim.entite.typestation, sim.entite.libelle),
            (None, 'LIMNI', 'BORDEAUX'))
        self.assertEqual(
            (sim.grandeur, sim.qualite, sim.commentaire),
            ('H', 100, 'data SHOM'))
        self.assertEqual(sim.modeleprevision.code, '00nMERSHOM')
        self.assertEqual(len(sim.previsions_tend), 144 * 5)
        self.assertEqual(
            (sim.previsions_tend[10], sim.previsions_tend.index[10]),
            (4430, (datetime.datetime(2018, 12, 30, 0, 40), 'moy')))

    def test_base_02(self):
        """Second base test."""
        station = sitehydro.Station(code='-', libelle='BOR', strict=False)
        dtprod = datetime.datetime(2018, 12, 11, 15, 33)
        sim = shom.simulation_from_h10(
            src=SRC['h10'], station=station, codemodeleprevision='00nMERSHOM',
            begin='2019-01-01 01:00', end='2019-01-01 02:00',
            dtprod=dtprod)
        self.assertEqual(sim.entite, station)
        self.assertEqual(
            (sim.grandeur, sim.qualite, sim.commentaire, sim.dtprod),
            ('H', 100, 'data SHOM', dtprod))
        self.assertEqual(sim.modeleprevision.code, '00nMERSHOM')
        self.assertEqual(len(sim.previsions_tend), 7)
        self.assertEqual(
            (sim.previsions_tend[1], sim.previsions_tend.index[1]),
            (3950, (datetime.datetime(2019, 1, 1, 1, 10), 'moy')))

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        sim = shom.simulation_from_h10(
            src=SRC['h10'], station='X1', strict=False,
            codemodeleprevision='00nMERSHOM')
        self.assertEqual(sim.entite, 'X1')

    def test_error_01(self):
        """Dtprod error."""
        with self.assertRaises(ValueError):
            shom.simulation_from_h10(
            # **{'src': SRC['h10'], 'dtprod': '2019-01-01',
            **{'src': SRC['h10'], 'dtprod': '2019-1-1',
               'codemodeleprevision': '00nMERSHOM'})


# -- class TestSerieFromH10 ---------------------------------------------------
class TestSerieFromH10(unittest.TestCase):

    """Class SerieFromH10."""

    def test_base_01(self):
        """Base test."""
        serie = shom.serie_from_h10(SRC['h10'])
        # DEBUG - print(serie)
        self.assertEqual(
            (serie.entite.code, serie.entite.typestation,
             serie.entite.libelle),
            (None, 'LIMNI', 'BORDEAUX'))
        self.assertEqual(serie.grandeur, 'H')
        self.assertEqual(len(serie.observations), 144 * 5)
        self.assertEqual(
            (serie.observations.iloc[0].item(),
             serie.observations.iloc[0].name),
            (4080, datetime.datetime(2018, 12, 29, 23, 0)))
        self.assertEqual(
            (serie.observations.iloc[144].item(),
             serie.observations.iloc[144].name),
            (3200, datetime.datetime(2018, 12, 30, 23, 0)))
        self.assertEqual(
            (serie.observations.iloc[-1].item(),
             serie.observations.iloc[-1].name),
            (980, datetime.datetime(2019, 1, 3, 22, 50)))

    def test_base_02(self):
        """Second base test."""
        station = sitehydro.Station(code='X231101001', libelle='LOC')
        serie = shom.serie_from_h10(
            src=SRC['h10'], station=station,
            begin='2019-01-01 10:10', end='2019-01-01 10:40')
        # DEBUG - print(serie)
        self.assertEqual(serie.entite, station)
        self.assertEqual(serie.grandeur, 'H')
        self.assertEqual(len(serie.observations), 4)
        self.assertEqual(
            (serie.observations.iloc[0].item(),
             serie.observations.iloc[0].name),
            (390, datetime.datetime(2019, 1, 1, 10, 10)))
        self.assertEqual(
            (serie.observations.iloc[3].item(),
             serie.observations.iloc[3].name),
            (860, datetime.datetime(2019, 1, 1, 10, 40)))

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        serie = shom.serie_from_h10(
            src=SRC['h10'], station='X1', strict=False)
        # DEBUG - print(serie)
        self.assertEqual(serie.entite, 'X1')
        self.assertEqual(serie.grandeur, 'H')
        self.assertEqual(len(serie.observations), 144 * 5)
        self.assertEqual(
            (serie.observations.iloc[73].item(),
             serie.observations.iloc[73].name),
            (3990, datetime.datetime(2018, 12, 30, 11, 10)))

    def test_error_01(self):
        """Src error."""
        with self.assertRaises(IOError):
            shom.serie_from_h10(src='LOCMARI')

    def test_error_02(self):
        """Check dates format error."""
        with self.assertRaises(ValueError):
            # pandas.tseries.tools.DateParseError,
            shom.serie_from_h10(
            # **{'src': SRC, 'begin': '2013-1-1'}
            **{'src': SRC['h10'], 'begin': '20131'})
        with self.assertRaises(ValueError):
            # pandas.tseries.tools.DateParseError,
            shom.serie_from_h10(
            # **{'src': SRC, 'end': '2013-1-25'}
            **{'src': SRC['h10'], 'end': '20131'})

    def test_error_03(self):
        """Check dates values error."""
        with self.assertRaises(ValueError):
            shom.serie_from_h10(
            # **{'src': SRC['h10'], 'begin': '2013-1-1'}
            **{'src': SRC['h10'], 'begin': '2018-12-33'})
        with self.assertRaises(ValueError):
            shom.serie_from_h10(
            # **{'src': SRC['h10'], 'end': '2013-1-25'}
            **{'src': SRC['h10'], 'end': '2013-1-22'})

    def test_error_04(self):
        """Entity error."""
        station = sitehydro.Station(code='X1', strict=False)
        shom.serie_from_h10(
            src=SRC['h10'], station=station)
        with self.assertRaises(TypeError):
            shom.serie_from_h10(**{'src': SRC['h10'], 'station': 33})

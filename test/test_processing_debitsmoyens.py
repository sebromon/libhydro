# -*- coding: utf-8 -*-

"""Test program for module libhydro.processing.htoq.

To run all tests just type:
    python -m unittest test_processing_to_obsealb

To run only a class test:
    python -m unittest test_processing_htoq.TestClass

To run only a specific test:
    python -m unittest test_processing_htoq.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import unittest
import datetime as _datetime
import numpy as _numpy

from libhydro.core import (sitehydro as _sitehydro,
                           obshydro as _obshydro,
                           obselaboreehydro as _obselaboreehydro,
                           _composant)
from libhydro.core.courbecorrection import PivotCC, CourbeCorrection
from libhydro.core.courbetarage import (PivotCTPoly, PivotCTPuissance,
                                        PeriodeCT, CourbeTarage)

import libhydro.processing.debitsmoyens as _debitsmoyens


# -- strings ------------------------------------------------------------------
__version__ = '0.1'
__date__ = '2017-05-04'


class TestIndexPivotApres(unittest.TestCase):
    """Tests fonction index_pivot_calcul"""

    def test_index_pivot_calcul_01(self):
        """Tests avec courbe poly"""
        code = '159'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'libelle'
        pivots = [PivotCTPoly(hauteur=10.4, debit=27.4),
                  PivotCTPoly(hauteur=20.5, debit=38.4),
                  PivotCTPoly(hauteur=31.8, debit=38.4)]
        ctar = CourbeTarage(code=code, station=station,
                            libelle=libelle,
                            pivots=pivots)

        self.assertIsNone(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=10.3))
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=10.4), 0)
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=20.4), 1)
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=20.5), 1)
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=31.7), 2)
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=31.8), 2)
        self.assertIsNone(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=31.9))

    def test_index_pivot_ct_puissance(self):
        pivots = [PivotCTPuissance(hauteur=1860, qualif=20,
                                   vara=1, varb=1, varh=1),
                  PivotCTPuissance(hauteur=2050, qualif=20,
                                   vara=0.001126, varb=1, varh=1814.7),
                  PivotCTPuissance(hauteur=2205, qualif=20,
                                   vara=0.005541, varb=1.1531, varh=2021.4),
                  PivotCTPuissance(hauteur=2410, qualif=20,
                                   vara=2.916e-5, varb=1.9683, varh=1900.2),
                  PivotCTPuissance(hauteur=2615, qualif=20,
                                   vara=0.0007625, varb=1.5107, varh=2021.6),
                  PivotCTPuissance(hauteur=3400, qualif=20,
                                   vara=0.001033, varb=1.5212, varh=2149.9),
                  PivotCTPuissance(hauteur=4010, qualif=20,
                                   vara=0.001118, varb=1.5289, varh=2254.7),
                  PivotCTPuissance(hauteur=4400, qualif=20,
                                   vara=0.001702, varb=1.5289, varh=2676.8),
                  PivotCTPuissance(hauteur=5000, qualif=20,
                                   vara=0.002383, varb=1.5289, varh=3017.3),
                  PivotCTPuissance(hauteur=5530, qualif=20,
                                   vara=0.003782, varb=1.5289, varh=3534.3),
                  PivotCTPuissance(hauteur=6000, qualif=20,
                                   vara=0.004471, varb=1.5289, varh=3741.2)]
        station = _sitehydro.Station(code='A123456789')
        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]
        ctar = CourbeTarage(code=-1,
                            typect=4,
                            station=station,
                            libelle='toto', pivots=pivots,
                            periodes=periodes)
        self.assertIsNone(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=1800))
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=1860), 1)
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=1900), 1)
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=2050), 1)
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=2050.1), 2)
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=2200), 2)
        self.assertEqual(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=6000), 10)
        self.assertIsNone(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=6000.1))

    def test_02_no_pivots(self):
        """Test courbetarage without pivots"""
        code = '159'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'libelle'
        ctar = CourbeTarage(code=code, station=station,
                            libelle=libelle)
        self.assertIsNone(
            _debitsmoyens.index_pivot_calcul(ctar=ctar, hauteur=31.9))


class TestVolumePoly(unittest.TestCase):
    """Test calcul du volume élémentaire courbe poly"""

    @classmethod
    def setUpClass(cls):
        code = '159'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'libelle'
        pivots = [PivotCTPoly(hauteur=0, debit=0),
                  PivotCTPoly(hauteur=200, debit=400),
                  PivotCTPoly(hauteur=400, debit=1000),
                  PivotCTPoly(hauteur=600, debit=1400),
                  PivotCTPoly(hauteur=800, debit=1600),
                  ]

        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]
        cls.ctar_poly = CourbeTarage(code=code, station=station,
                                     libelle=libelle,
                                     pivots=pivots, periodes=periodes)

    def test_01(self):
        """Test un point intercalé"""
        hauteur1 = 100
        hauteur2 = 300
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 1, 0, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        #
        # volume = 1800 * (200 + 400) / 2 + 1800 *(400 + 700) / 2
        self.assertEqual(volume, 1530000)

        # hauteurs décroissantes
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertEqual(volume, 1530000)

    def test_02(self):
        """Test points between the first and second pivot"""
        hauteur1 = 0
        hauteur2 = 200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        # volume = 1800 * (0 +400) / 2
        self.assertEqual(volume, 360000)

        obsh1['res'] = 100
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        # volume = 1800 * (200 +400) / 2
        self.assertEqual(volume, 540000)

        obsh1['res'] = 0
        obsh2['res'] = 100
        # volume = 1800 * (0 +200) / 2
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertEqual(volume, 180000)

    def test_03(self):
        """Test dernier point"""
        hauteur1 = 700
        hauteur2 = 800
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        # 1800 * (1500 +1600) /2 
        self.assertEqual(volume, 2790000)
        obsh1['res'] = 600
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        # 1800 * (1400 +1600) /2
        self.assertEqual(volume, 2700000)

        obsh1['res'] = 800
        # 1800 * (1600 +1600) /2
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertEqual(volume, 2880000)

    def test_04(self):
        hauteur1 = 0
        hauteur2 = 200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertIsNotNone(volume)

        obsh1['res'] = -10
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        # self.assertIsNone(volume)
        self.assertTrue(_numpy.isnan(volume))
        self.assertEqual(obsv['cnt'].item(), 4)

        obsh2['res'] = -5
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))
        self.assertEqual(obsv['cnt'].item(), 4)
        # self.assertIsNone(volume)

    def test_05(self):
        """test une des deux hauteurs"""
        hauteur1 = 0
        hauteur2 = 200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertIsNotNone(volume)

        obsh2['res'] = 800
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertIsNotNone(volume)

        obsh2['res'] = 801
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        # self.assertIsNone(volume)
        self.assertTrue(_numpy.isnan(volume))
        self.assertEqual(obsv['cnt'].item(), 8)

        obsh1['res'] = 900
        obsh2['res'] = 500
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        # self.assertIsNone(volume)
        self.assertTrue(_numpy.isnan(volume))
        self.assertEqual(obsv['cnt'].item(), 8)

    def test_obsh1_none(self):
        """test without first obs"""
        hauteur1 = 0
        hauteur2 = 200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertIsNotNone(volume)

        obsv = _debitsmoyens.obsh_to_obsv(None, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))

    def test_without_active_ctar(self):
        hauteur1 = 0
        hauteur2 = 200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertIsNotNone(volume)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [])
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, None)
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))

        # ctart not active
        obsh2['dte'] = _datetime.datetime(2018, 3, 4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))

    def test_hauteur_none(self):
        hauteur1 = 0
        hauteur2 = 200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertIsNotNone(volume)

        obsh3 = _obshydro.Observation(dte=dt1, res=None,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh3, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))

        obsh2['res'] = _numpy.nan
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))

    def test_limitesinfsup(self):
        code = '159'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'libelle'
        pivots = [PivotCTPoly(hauteur=0, debit=0),
                  PivotCTPoly(hauteur=200, debit=400),
                  PivotCTPoly(hauteur=400, debit=1000),
                  PivotCTPoly(hauteur=600, debit=1400),
                  PivotCTPoly(hauteur=800, debit=1600),
                  ]

        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]
        limiteinf = 100.5
        limitesup = 754.2
        ctar = CourbeTarage(code=code, station=station, libelle=libelle,
                           limiteinf=limiteinf, limitesup=limitesup,
                           pivots=pivots, periodes=periodes)

        hauteur1 = 100.6
        hauteur2 = 200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [ctar])
        self.assertFalse(_numpy.isnan(obsv['res'].item()))
        self.assertEqual(obsv['qal'].item(), 16)

        obsh1['res'] = 100.5
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [ctar])
        self.assertFalse(_numpy.isnan(obsv['res'].item()))
        self.assertEqual(obsv['qal'].item(), 12)

        obsh1['res'] = 150
        obsh2['res'] = 100
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [ctar])
        self.assertFalse(_numpy.isnan(obsv['res'].item()))
        self.assertEqual(obsv['qal'].item(), 12)

        obsh1['res'] = 88.4
        obsh2['res'] = 54.2
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [ctar])
        self.assertFalse(_numpy.isnan(obsv['res'].item()))
        self.assertEqual(obsv['qal'].item(), 12)

        obsh1['res'] = 754.2
        obsh2['res'] = 700
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [ctar])
        self.assertFalse(_numpy.isnan(obsv['res'].item()))
        self.assertEqual(obsv['qal'].item(), 12)

        obsh1['res'] = 700
        obsh2['res'] = 780
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [ctar])
        self.assertFalse(_numpy.isnan(obsv['res'].item()))
        self.assertEqual(obsv['qal'].item(), 12)

        obsh1['res'] = 780
        obsh2['res'] = 780
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [ctar])
        self.assertFalse(_numpy.isnan(obsv['res'].item()))
        self.assertEqual(obsv['qal'].item(), 12)

    def test_error_obsh2_none(self):
        hauteur1 = 0
        hauteur2 = 200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)

        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ctar_poly])
        volume = obsv['res'].item()
        self.assertIsNotNone(volume)
        with self.assertRaises(TypeError):
            _debitsmoyens.obsh_to_obsv(obsh1, None, [self.ctar_poly])


class TestVolumePuissance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pivots = [PivotCTPuissance(hauteur=1860, qualif=20,
                                   vara=1, varb=1, varh=1),
                  PivotCTPuissance(hauteur=2050, qualif=20,
                                   vara=0.001126, varb=1, varh=1814.7),
                  PivotCTPuissance(hauteur=2205, qualif=20,
                                   vara=0.005541, varb=1.1531, varh=2021.4),
                  PivotCTPuissance(hauteur=2410, qualif=20,
                                   vara=2.916e-5, varb=1.9683, varh=1900.2),
                  PivotCTPuissance(hauteur=2615, qualif=20,
                                   vara=0.0007625, varb=1.5107, varh=2021.6),
                  PivotCTPuissance(hauteur=3400, qualif=20,
                                   vara=0.001033, varb=1.5212, varh=2149.9),
                  PivotCTPuissance(hauteur=4010, qualif=20,
                                   vara=0.001118, varb=1.5289, varh=2254.7),
                  PivotCTPuissance(hauteur=4400, qualif=20,
                                   vara=0.001702, varb=1.5289, varh=2676.8),
                  PivotCTPuissance(hauteur=5000, qualif=20,
                                   vara=0.002383, varb=1.5289, varh=3017.3),
                  PivotCTPuissance(hauteur=5530, qualif=20,
                                   vara=0.003782, varb=1.5289, varh=3534.3),
                  PivotCTPuissance(hauteur=6000, qualif=20,
                                   vara=0.004471, varb=1.5289, varh=3741.2)]
        station = _sitehydro.Station(code='A123456789')
        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]
        cls.ct_puissance = CourbeTarage(code=-1,
                                        typect=4,
                                        station=station,
                                        libelle='toto', pivots=pivots,
                                        periodes=periodes)

    def test_01(self):
        hauteur1 = 2200
        hauteur2 = 2200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 5, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ct_puissance])
        volume = obsv['res'].item()
        # v = 1000 * 0.005541 * 300 * (2200 -2021.4)^1.1531 = 
        self.assertAlmostEqual(volume, 656680.18, 2)
        self.assertIsNotNone(volume)

    def test_premier_point(self):
        """Premier point pivot"""
        hauteur1 = 1860
        hauteur2 = 1860
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 10, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ct_puissance])
        volume = obsv['res'].item()
        # v = 1000 * 0.001126 * 600 * (1860 -1814.7)^1 = 
        self.assertAlmostEqual(volume, 30604.68, 2)
        self.assertIsNotNone(volume)

        obsh2['res'] = 2000
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ct_puissance])
        volume = obsv['res'].item()
        # v = 1000 * 0.001126 * 600 * (1860 -1814.7)^1
        # a = (h1-h2) / (t1-t2) = (2200-2100) / 3600 = 0.0278888
        # v = 1000 * A * 1/( a*(B+1) * ((h2-H0)^(B+1) - (h1 -H0)^(B+1)) = 5420102.36974578")
        self.assertAlmostEqual(volume, 77896.68, 2)

        obsh2['res'] = 2050
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ct_puissance])
        volume = obsv['res'].item()
        self.assertAlmostEqual(volume, 94786.68, 2)

    def test_entre_deux_points(self):
        hauteur1 = 2100
        hauteur2 = 2200
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 1, 0, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ct_puissance])
        volume = obsv['res'].item()
        # v = 1000 * 0.001126 * 600 * (1860 -1814.7)^1 = 
        self.assertAlmostEqual(volume, 5420102.37, 2)

    def test_entre_hauteurs_decroissantes(self):
        hauteur1 = 2200
        hauteur2 = 2100
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 1, 0, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ct_puissance])
        volume = obsv['res'].item()
        # v = 1000 * 0.001126 * 600 * (1860 -1814.7)^1 = 
        self.assertAlmostEqual(volume, 5420102.37, 2)

    def test_1_point_intercale(self):
        hauteur1 = 2100
        hauteur2 = 2300
        dt1 = _datetime.datetime(2015, 1, 1, 11, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 11, 10, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ct_puissance])
        volume = obsv['res'].item()
        self.assertAlmostEqual(volume, 1346472.35, 2)

    def test_2_points_intercales(self):
        hauteur1 = 2100
        hauteur2 = 2500
        dt1 = _datetime.datetime(2015, 1, 1, 11, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 11, 30, 0)
        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt2, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ct_puissance])
        volume = obsv['res'].item()
        self.assertAlmostEqual(volume, 7467710.61, 2)

    def test_same_dte(self):
        hauteur1 = 2100
        hauteur2 = 2100
        dt1 = _datetime.datetime(2015, 1, 1, 11, 0, 0)

        obsh1 = _obshydro.Observation(dte=dt1, res=hauteur1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsh2 = _obshydro.Observation(dte=dt1, res=hauteur2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsh_to_obsv(obsh1, obsh2, [self.ct_puissance])
        volume = obsv['res'].item()
        self.assertAlmostEqual(volume, 0, 2)

class ObsQToObsV(unittest.TestCase):

    def test_calcul(self):
        deb1 = 1000
        deb2 = 2000
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 5, 0)
        obsq1 = _obshydro.Observation(dte=dt1, res=deb1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsq2 = _obshydro.Observation(dte=dt2, res=deb2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsq_to_obsv(obsq1, obsq2)
        volume = obsv['res'].item()
        # 1500 * 5 *60
        self.assertAlmostEqual(volume, 450000, 2)

    def test_obsq1_None(self):
        deb1 = 1000
        deb2 = 2000
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 5, 0)
        obsq1 = _obshydro.Observation(dte=dt1, res=deb1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsq2 = _obshydro.Observation(dte=dt2, res=deb2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsq_to_obsv(obsq1, obsq2)
        volume = obsv['res'].item()
        self.assertFalse(_numpy.isnan(volume))

        obsv = _debitsmoyens.obsq_to_obsv(None, obsq2)
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))

    def test_obsq2_None(self):
        deb1 = 1000
        deb2 = 2000
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 5, 0)
        obsq1 = _obshydro.Observation(dte=dt1, res=deb1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsq2 = _obshydro.Observation(dte=dt2, res=deb2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsq_to_obsv(obsq1, obsq2)
        volume = obsv['res'].item()
        self.assertFalse(_numpy.isnan(volume))

        with self.assertRaises(TypeError):
            _debitsmoyens.obsq_to_obsv(obsq1, None)

    def test_debit_nan(self):
        deb1 = 1000
        deb2 = 2000
        dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        dt2 = _datetime.datetime(2015, 1, 1, 0, 5, 0)
        obsq1 = _obshydro.Observation(dte=dt1, res=deb1,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsq2 = _obshydro.Observation(dte=dt2, res=deb2,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsq_to_obsv(obsq1, obsq2)
        volume = obsv['res'].item()
        self.assertFalse(_numpy.isnan(volume))

        obsq3 = _obshydro.Observation(dte=dt1, res=None,
                                      qal=16, mth=0, cnt=0, statut=4)
        obsv = _debitsmoyens.obsq_to_obsv(obsq3, obsq2)
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))

        obsq2['res'] = _numpy.nan
        obsv = _debitsmoyens.obsq_to_obsv(obsq1, obsq2)
        volume = obsv['res'].item()
        self.assertTrue(_numpy.isnan(volume))


class TestSerieToQmJ(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        code = '159'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'libelle'
        pivots = [PivotCTPoly(hauteur=0, debit=0),
                  PivotCTPoly(hauteur=200, debit=400),
                  PivotCTPoly(hauteur=400, debit=1000),
                  PivotCTPoly(hauteur=600, debit=1400),
                  PivotCTPoly(hauteur=800, debit=1600),
                  ]

        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]
        cls.ctar_poly = CourbeTarage(code=code, station=station,
                                     libelle=libelle,
                                     pivots=pivots, periodes=periodes)

    def test_serie_h_ctar_poly(self):
        """Test calcul qmj with courbe poly"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-09-27 15:00', 100),
            _obshydro.Observation('2015-10-03 00:00', 100),
            _obshydro.Observation('2015-10-03 06:00', 100),
            _obshydro.Observation('2015-10-03 07:00', 100),
            _obshydro.Observation('2015-10-03 08:00', 100),
            _obshydro.Observation('2015-10-03 09:00', 100),
            _obshydro.Observation('2015-10-03 10:00', 100),
            _obshydro.Observation('2015-10-03 11:00', 200),
            _obshydro.Observation('2015-10-04 00:00', 100)
        )
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, observations=obss, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )

        debits = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[self.ctar_poly])
        self.assertEqual(len(debits), 7)
        self.assertTrue(_numpy.isnan(debits.loc['2015-09-27', 'res']))
        self.assertEqual(debits.loc['2015-09-28', 'res'], 200)
        self.assertAlmostEqual(debits.loc['2015-10-03', 'res'], 258.33, 2)

        station = _sitehydro.Station(code='O123456789')
        pivot1 = PivotCC(dte=_datetime.datetime(2010, 1, 1), deltah=-50)
        pivot2 = PivotCC(dte=_datetime.datetime(2020, 1, 1), deltah=-50)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)
        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)
        debits = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[self.ctar_poly],
            courbecorrection=ccor)
        self.assertEqual(len(debits), 7)
        self.assertTrue(_numpy.isnan(debits.loc['2015-09-27', 'res']))
        self.assertEqual(debits.loc['2015-09-28', 'res'], 100)
        self.assertAlmostEqual(debits.loc['2015-10-03', 'res'], 158.33, 2)

    def test_serie_h_ctar_poly_invalide_ccor(self):
        """Test calcul with an invalid courbe correction"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-09-27 15:00', 100),
            _obshydro.Observation('2015-10-03 00:00', 100),
            _obshydro.Observation('2015-10-03 06:00', 100),
            _obshydro.Observation('2015-10-03 07:00', 100),
            _obshydro.Observation('2015-10-03 08:00', 100),
            _obshydro.Observation('2015-10-03 09:00', 100),
            _obshydro.Observation('2015-10-03 10:00', 100),
            _obshydro.Observation('2015-10-03 11:00', 200),
            _obshydro.Observation('2015-10-04 00:00', 100)
        )
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, observations=obss, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )

        station = _sitehydro.Station(code='O123456789')
        pivot1 = PivotCC(dte=_datetime.datetime(2010, 1, 1), deltah=-50)
        pivot2 = PivotCC(dte=_datetime.datetime(2015, 10, 3, 11, 54, 23),
                         deltah=-50)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)
        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        debits = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[self.ctar_poly],
            courbecorrection=None)
        self.assertFalse(_numpy.isnan(debits.loc['2015-10-03', 'res']))

        debits = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[self.ctar_poly],
            courbecorrection=ccor)
        self.assertTrue(_numpy.isnan(debits.loc['2015-10-03', 'res']))

    def test_without_observations(self):
        """test without observations"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-09-27 15:00', 100),
            _obshydro.Observation('2015-10-03 00:00', 100),
            _obshydro.Observation('2015-10-03 06:00', 100),
            _obshydro.Observation('2015-10-03 07:00', 100),
            _obshydro.Observation('2015-10-03 08:00', 100),
            _obshydro.Observation('2015-10-03 09:00', 100),
            _obshydro.Observation('2015-10-03 10:00', 100),
            _obshydro.Observation('2015-10-03 11:00', 200),
            _obshydro.Observation('2015-10-04 00:00', 100)
        )
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, observations=obss, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )

        debits = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[self.ctar_poly])
        self.assertIsNotNone(debits)
        serie.observations = None
        debits = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[self.ctar_poly])
        self.assertIsNone(debits)

    def test_without_courbestarage(self):
        """test without courbes de tarage"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-09-27 15:00', 100),
            _obshydro.Observation('2015-10-03 00:00', 100),
            _obshydro.Observation('2015-10-03 06:00', 100),
            _obshydro.Observation('2015-10-03 07:00', 100),
            _obshydro.Observation('2015-10-03 08:00', 100),
            _obshydro.Observation('2015-10-03 09:00', 100),
            _obshydro.Observation('2015-10-03 10:00', 100),
            _obshydro.Observation('2015-10-03 11:00', 200),
            _obshydro.Observation('2015-10-04 00:00', 100)
        )
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, observations=obss, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )

        debits = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[self.ctar_poly])
        self.assertIsNotNone(debits)

        debits = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=None)
        self.assertIsNone(debits)

        debits = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[])
        self.assertIsNone(debits)

    def test_02(self):
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-08-03 00:00', 0),
            _obshydro.Observation('2015-08-03 12:00', 100),
            _obshydro.Observation('2015-08-04 00:00', 0),
            _obshydro.Observation('2015-08-04 12:00', 200),
            _obshydro.Observation('2015-08-05 00:00', 0)
        )
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, observations=obss, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )

        obss = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[self.ctar_poly])
        self.assertEqual(len(obss), 2)
        tuples = [obs for obs in obss.itertuples()]
        self.assertEqual(tuples[0].res, 100)
        self.assertEqual(tuples[1].res, 200)

    def test_serie_q(self):
        """Test serie grandeur Q"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'Q'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-08-03 00:00', 0),
            _obshydro.Observation('2015-08-03 12:00', 100),
            _obshydro.Observation('2015-08-04 00:00', 0),
            _obshydro.Observation('2015-08-04 12:00', 200),
            _obshydro.Observation('2015-08-05 00:00', 0)
        )
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, observations=obss, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )
        qmj = _debitsmoyens.serie_to_qmj(seriehydro=serie)
        self.assertIsNotNone(qmj)
        self.assertEqual(len(qmj), 2)
        self.assertEqual(qmj.loc['2015-08-03', 'res'], 50)
        self.assertEqual(qmj.loc['2015-08-04', 'res'], 100)


class TestQmjToQmm(unittest.TestCase):
    """Tests function qmj_to_qmm"""
    @classmethod
    def setUpClass(cls):
        code = '159'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'libelle'
        pivots = [PivotCTPoly(hauteur=0, debit=0),
                  PivotCTPoly(hauteur=200, debit=400),
                  PivotCTPoly(hauteur=400, debit=1000),
                  PivotCTPoly(hauteur=600, debit=1400),
                  PivotCTPoly(hauteur=800, debit=1600),
                  ]

        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]
        cls.ctar_poly = CourbeTarage(code=code, station=station,
                                     libelle=libelle,
                                     pivots=pivots, periodes=periodes)

    def test_01(self):
        """Test with a month of qmj"""
        obss = []
        for jour in range(1, 32):
            dte = _datetime.datetime(2016, 1, jour)
            obss.append(_obselaboreehydro.ObservationElaboree(dte=dte,
                                                              res=200,
                                                              statut=12,
                                                              qal=20,
                                                              mth=8,
                                                              cnt=0))

        observations = _obselaboreehydro.ObservationsElaborees(*obss)
        # print(observations)
        qmm = _debitsmoyens.qmj_to_qmm(observations)
        self.assertEqual(len(qmm), 1)
        self.assertEqual(qmm.loc['2016-01-01'].tolist(),
                         [200, 8, 20, 0, 12])

    def test_without_observations(self):
        """test without observations"""
        qmm = _debitsmoyens.qmj_to_qmm(debitsjournaliers=None)
        self.assertIsNone(qmm)
        dtprod = _datetime.datetime(2016, 1, 17, 23, 14, 57)
        typegrd = 'QmnJ'
        entite = _sitehydro.Station(code='A123456789')
        serie = _obselaboreehydro.SerieObsElab(dtprod=dtprod,
                                               typegrd=typegrd,
                                               entite=entite)
        qmm = _debitsmoyens.qmj_to_qmm(debitsjournaliers=serie)
        self.assertIsNone(qmm)

    def test_serie_obs_elab(self):
        """Test with a serie os a month of qmj"""
        obss = []
        for jour in range(1, 32):
            dte = _datetime.datetime(2016, 1, jour)
            obss.append(_obselaboreehydro.ObservationElaboree(dte=dte,
                                                              res=200,
                                                              statut=12,
                                                              qal=20,
                                                              mth=8,
                                                              cnt=0))

        observations = _obselaboreehydro.ObservationsElaborees(*obss)
        dtprod = _datetime.datetime(2016, 1, 17, 23, 14, 57)
        typegrd = 'QmnJ'
        entite = _sitehydro.Station(code='A123456789')
        serie = _obselaboreehydro.SerieObsElab(dtprod=dtprod,
                                               typegrd=typegrd,
                                               entite=entite,
                                               observations=observations)
        # print(observations)
        qmm = _debitsmoyens.qmj_to_qmm(serie)
        self.assertEqual(len(qmm), 1)
        self.assertEqual(qmm.loc['2016-01-01'].tolist(),
                         [200, 8, 20, 0, 12])

    def test_02(self):
        """Test witthout all debits"""
        obss = []
        for jour in range(1, 31):
            dte = _datetime.datetime(2016, 1, jour)
            obss.append(_obselaboreehydro.ObservationElaboree(dte=dte,
                                                              res=200,
                                                              statut=12,
                                                              qal=20,
                                                              mth=8,
                                                              cnt=0))

        observations = _obselaboreehydro.ObservationsElaborees(*obss)
        # print(observations)
        qmm = _debitsmoyens.qmj_to_qmm(observations)
        self.assertEqual(len(qmm), 1)
        self.assertTrue(_numpy.isnan(qmm.loc['2016-01-01']['res']))

    def test_03(self):
        """Test with only débit janvier mars """
        obss = []
        for jour in range(1, 32):
            for month in [1, 3]:
                dte = _datetime.datetime(2016, month, jour)
                obss.append(_obselaboreehydro.ObservationElaboree(
                    dte=dte, res=month * 100, statut=16, qal=12, mth=8, cnt=0))

        observations = _obselaboreehydro.ObservationsElaborees(*obss)
        # print(observations)
        qmm = _debitsmoyens.qmj_to_qmm(observations)
        self.assertEqual(len(qmm), 2)
        self.assertEqual(qmm.loc['2016-01-01']['res'], 100)
        self.assertEqual(qmm.loc['2016-03-01']['res'], 300)

    def test_04(self):
        """Test calcul qmm"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-08-03 15:24:13', 158.4),
            _obshydro.Observation('2015-11-04 12:34:49', 158.4)
        )
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, observations=obss, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )

        qmj = _debitsmoyens.serie_to_qmj(
            seriehydro=serie, courbestarage=[self.ctar_poly])
        qmm = _debitsmoyens.qmj_to_qmm(qmj)
        self.assertEqual(len(qmm), 4)
        self.assertTrue(_numpy.isnan(qmm.loc['2015-08-01']['res']))
        self.assertAlmostEqual(qmm.loc['2015-09-01']['res'], 316.8, 2)
        self.assertAlmostEqual(qmm.loc['2015-10-01']['res'], 316.8, 2)
        self.assertTrue(_numpy.isnan(qmm.loc['2015-11-01']['res']))

    def test_qmj_nan(self):
        """ Test qmj with nan values"""
        obss = []
        for jour in range(1, 32):
            for mois in [1, 3]:
                dte = _datetime.datetime(2016, mois, jour)
                obss.append(_obselaboreehydro.ObservationElaboree(
                    dte=dte, res=mois * 100, statut=12, qal=20, mth=8, cnt=0))

        observations = _obselaboreehydro.ObservationsElaborees(*obss)
        # print(observations)
        qmm = _debitsmoyens.qmj_to_qmm(observations)
        self.assertEqual(len(qmm), 2)
        self.assertEqual(qmm.loc['2016-01-01'].tolist(),
                         [100, 8, 20, 0, 12])
        observations.iloc[0, 0] = _numpy.nan
        qmm = _debitsmoyens.qmj_to_qmm(observations)
        self.assertTrue(_numpy.isnan(qmm.loc['2016-01-01', 'res']))

    def test_qmj_cnt(self):
        """Test continuite qmj"""
        obss = []
        for jour in range(1, 32):
            for mois in [1, 3]:
                dte = _datetime.datetime(2016, mois, jour)
                obss.append(_obselaboreehydro.ObservationElaboree(
                    dte=dte, res=mois * 100, statut=12, qal=20, mth=8, cnt=0))

        observations = _obselaboreehydro.ObservationsElaborees(*obss)
        # print(observations)
        qmm = _debitsmoyens.qmj_to_qmm(observations)
        self.assertEqual(len(qmm), 2)
        self.assertEqual(qmm.loc['2016-01-01'].tolist(),
                         [100, 8, 20, 0, 12])
        observations.loc['2016-01-15', 'cnt'] = 8
        qmm = _debitsmoyens.qmj_to_qmm(observations)
        self.assertEqual(qmm.loc['2016-01-01', 'cnt'], 1)

    def test_error_typegrd_serieobselab(self):
        """Test error typegrd serie"""
        obss = []
        for jour in range(1, 32):
            dte = _datetime.datetime(2016, 1, jour)
            obss.append(_obselaboreehydro.ObservationElaboree(
                dte=dte, res=200, statut=12, qal=20, mth=8, cnt=0))

        observations = _obselaboreehydro.ObservationsElaborees(*obss)
        dtprod = _datetime.datetime(2016, 1, 17, 23, 14, 57)
        typegrd = 'QmnJ'
        entite = _sitehydro.Station(code='A123456789')
        serie = _obselaboreehydro.SerieObsElab(dtprod=dtprod,
                                               typegrd=typegrd,
                                               entite=entite,
                                               observations=observations)
        # print(observations)
        qmm = _debitsmoyens.qmj_to_qmm(serie)
        self.assertTrue(len(qmm), 1)
        serie.typegrd = 'QmM'
        with self.assertRaises(TypeError):
            _debitsmoyens.qmj_to_qmm(serie)

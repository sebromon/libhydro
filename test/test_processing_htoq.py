# -*- coding: utf-8 -*-

"""Test program for module libhydro.processing.htoq.

To run all tests just type:
    python -m unittest test_processing_htoq

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
                           _composant)
from libhydro.core.courbecorrection import PivotCC, CourbeCorrection
from libhydro.core.courbetarage import (PivotCTPoly, PivotCTPuissance,
                                        PeriodeCT, CourbeTarage)
from libhydro.processing import htoq as _htoq


# -- strings ------------------------------------------------------------------
__version__ = '0.1'
__date__ = '2017-05-04'

# HISTORY
# V0.1 - SR - 2017-05-04
#   first shot


class TestHauteurCorrigee(unittest.TestCase):
    """Classe de tests hauteur corrigée"""

    def test_base_00(self):
        """Check calculation hauteur corrigéee between two points pivots"""
        dte = _datetime.datetime(2017, 9, 23, 12, 10, 15)

        dt1 = _datetime.datetime(2010, 10, 18, 11, 10, 15)
        deltah1 = -10
        dt2 = _datetime.datetime(2017, 9, 23, 12, 10, 15)
        deltah2 = -20
        dt3 = _datetime.datetime(2018, 2, 14, 23, 41, 33)
        deltah3 = -10
        hauteur = 155.89
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivot3 = PivotCC(dte=dt3, deltah=deltah3)
        pivots = [pivot1, pivot2, pivot3]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        hcor = _htoq.hauteur_corrigee(dte=dte, hauteur=hauteur, ccor=ccor)
        self.assertEqual(hcor, 135.89)

    def test_base_01(self):
        """Check calculation hauteur corrigéee between two points pivots"""
        dte = _datetime.datetime(2017, 9, 23, 12, 10, 15)
        dt1 = _datetime.datetime(2017, 9, 23, 11, 10, 15)
        deltah1 = -10
        dt2 = _datetime.datetime(2017, 9, 23, 13, 10, 15)
        deltah2 = -20
        hauteur = 155.89
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        hcor = _htoq.hauteur_corrigee(dte=dte, hauteur=hauteur, ccor=ccor)
        self.assertEqual(hcor, 140.89)

    def test_base_02(self):
        """Check calculation hauteur corrigéee right courbe
        Last point deltah !=0
        """
        dte = _datetime.datetime(2017, 9, 25, 12, 10, 15)

        dt1 = _datetime.datetime(2017, 9, 20, 11, 10, 15)
        deltah1 = 0
        dt2 = _datetime.datetime(2017, 9, 23, 13, 10, 15)
        deltah2 = -50
        hauteur = 155.89
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        hcor = _htoq.hauteur_corrigee(dte=dte, hauteur=hauteur, ccor=ccor)
        self.assertIsNone(hcor)

    def test_base_03(self):
        """Check calculation hauteur corrigéee right courbe
        Last point deltah = 0
        """
        dte = _datetime.datetime(2017, 9, 25, 12, 10, 15)

        dt1 = _datetime.datetime(2017, 9, 20, 11, 10, 15)
        deltah1 = 0
        dt2 = _datetime.datetime(2017, 9, 23, 13, 10, 15)
        deltah2 = 0
        hauteur = 155.89
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        hcor = _htoq.hauteur_corrigee(dte=dte, hauteur=hauteur, ccor=ccor)
        self.assertEqual(hcor, hauteur)

    def test_base_04(self):
        """Check calculation hauteur corrigéee left courbe
        first point deltah = 0
        """
        dte = _datetime.datetime(2010, 9, 25, 12, 10, 15)

        dt1 = _datetime.datetime(2015, 9, 20, 11, 10, 15)
        deltah1 = 0
        dt2 = _datetime.datetime(2016, 9, 23, 13, 10, 15)
        deltah2 = -50
        hauteur = 155.89
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        hcor = _htoq.hauteur_corrigee(dte=dte, hauteur=hauteur, ccor=ccor)
        self.assertEqual(hcor, hauteur)

    def test_base_05(self):
        """Check calculation hauteur corrigéee left courbe
        first point deltah != 0
        """
        dte = _datetime.datetime(2010, 9, 25, 12, 10, 15)

        dt1 = _datetime.datetime(2015, 9, 20, 11, 10, 15)
        deltah1 = -10
        dt2 = _datetime.datetime(2016, 9, 23, 13, 10, 15)
        deltah2 = -50
        hauteur = 155.89
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        hcor = _htoq.hauteur_corrigee(dte=dte, hauteur=hauteur, ccor=ccor)
        self.assertIsNone(hcor)


class TestCorrectionHauteurs(unittest.TestCase):
    """Class de test method correctionhauteurs"""

    def test_base_01(self):
        """test with simple courbe correction"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2012-10-03 05:00', 30),
            _obshydro.Observation('2012-10-03 06:00', 33),
            _obshydro.Observation('2012-10-03 06:30', 38),
            _obshydro.Observation('2012-10-03 07:00', 37),
            _obshydro.Observation('2012-10-03 08:00', 42),
            _obshydro.Observation('2012-10-03 09:00', 50),
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

        dt1 = _datetime.datetime(2012, 10, 3, 6, 0, 0)
        deltah1 = 0
        dt2 = _datetime.datetime(2012, 10, 3, 7, 0, 0)
        deltah2 = -10
        dt3 = _datetime.datetime(2012, 10, 3, 8, 0, 0)
        deltah3 = 0
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivot3 = PivotCC(dte=dt3, deltah=deltah3)
        pivots = [pivot1, pivot2, pivot3]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        serie_hcor = _htoq.correction_hauteurs(seriehydro=serie,
                                               courbecorrection=ccor)

        self.assertEqual(len(serie_hcor.observations), len(serie.observations))
        self.assertEqual(serie_hcor.dtdeb, serie.dtdeb)
        self.assertEqual(serie_hcor.dtfin, serie.dtfin)
        self.assertNotEqual(serie_hcor.dtprod, serie.dtprod)
        self.assertEqual(serie_hcor.observations['res'].tolist(),
                         [30, 33, 33, 27, 42, 50])
        self.assertEqual(serie_hcor.observations['mth'].tolist(),
                         [8, 8, 8, 8, 8, 8])

    def test_base_02(self):
        """Check nan values"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2012-10-03 05:00', 30),
            _obshydro.Observation('2012-10-03 06:00', 33),
            _obshydro.Observation('2012-10-03 06:30', 38),
            _obshydro.Observation('2012-10-03 07:00', 37),
            _obshydro.Observation('2012-10-03 08:00', 42),
            _obshydro.Observation('2012-10-03 09:00', 50),
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

        dt1 = _datetime.datetime(2012, 10, 3, 6, 0, 0)
        deltah1 = -20
        dt2 = _datetime.datetime(2012, 10, 3, 7, 0, 0)
        deltah2 = -10
        dt3 = _datetime.datetime(2012, 10, 3, 8, 0, 0)
        deltah3 = -20
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivot3 = PivotCC(dte=dt3, deltah=deltah3)
        pivots = [pivot1, pivot2, pivot3]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        serie_hcor = _htoq.correction_hauteurs(seriehydro=serie,
                                               courbecorrection=ccor)

        self.assertEqual(len(serie_hcor.observations), len(serie.observations))
        self.assertEqual(serie_hcor.dtdeb, serie.dtdeb)
        self.assertEqual(serie_hcor.dtfin, serie.dtfin)
        self.assertNotEqual(serie_hcor.dtprod, serie.dtprod)
        debits = serie_hcor.observations['res'].tolist()

        self.assertTrue(_numpy.isnan(debits[0]))
        self.assertTrue(_numpy.isnan(debits[-1]))
        self.assertEqual(debits[1:-1], [13, 23, 27, 22])
        self.assertEqual(serie_hcor.observations['mth'].tolist(),
                         [8, 8, 8, 8, 8, 8])

    def test_base_03(self):
        """Test serie without observations"""

        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )
        dt1 = _datetime.datetime(2012, 10, 3, 6, 0, 0)
        deltah1 = -20
        dt2 = _datetime.datetime(2012, 10, 3, 7, 0, 0)
        deltah2 = -10
        dt3 = _datetime.datetime(2012, 10, 3, 8, 0, 0)
        deltah3 = -20
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivot3 = PivotCC(dte=dt3, deltah=deltah3)
        pivots = [pivot1, pivot2, pivot3]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)
        serie_hcor = _htoq.correction_hauteurs(seriehydro=serie,
                                               courbecorrection=ccor)
        self.assertNotEqual(serie_hcor, serie)

    def test_pivots_01(self):
        """test with adding pivots of courbe de correction"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obs_dt1 = _datetime.datetime(2012, 10, 1)
        obs_dt2 = _datetime.datetime(2012, 11, 1)
        obss = _obshydro.Observations(
            _obshydro.Observation(obs_dt1, 0),
            _obshydro.Observation(obs_dt2, 0),
        )
        dtdeb = '2012-10-01 00:00'
        dtfin = '2012-11-01 00:00'
        dtprod = '2012-10-03 10:00'

        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, observations=obss)

        dt1 = _datetime.datetime(2012, 10, 3, 6, 0, 0)
        deltah1 = 0
        dt2 = _datetime.datetime(2012, 10, 3, 7, 0, 0)
        deltah2 = -10
        dt3 = _datetime.datetime(2012, 10, 3, 8, 0, 0)
        deltah3 = 0
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivot3 = PivotCC(dte=dt3, deltah=deltah3)
        pivots = [pivot1, pivot2, pivot3]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        serie_hcor = _htoq.correction_hauteurs(seriehydro=serie,
                                               courbecorrection=ccor,
                                               pivots=False)

        self.assertEqual(len(serie_hcor.observations), 2)
        serie_hcor = _htoq.correction_hauteurs(seriehydro=serie,
                                               courbecorrection=ccor,
                                               pivots=True)
        self.assertEqual(len(serie_hcor.observations), 5)
        self.assertEqual(serie_hcor.observations['res'].tolist(),
                         [0, 0, -10, 0, 0])
        self.assertEqual(
            serie_hcor.observations.index.to_pydatetime().tolist(),
            [obs_dt1, dt1, dt2, dt3, obs_dt2])

    def test_pivots_02(self):
        """test with adding pivots with wrong courbe de correction"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obs_dt1 = _datetime.datetime(2012, 10, 3, 0, 0)
        obs_dt2 = _datetime.datetime(2012, 10, 3, 6, 0)
        obss = _obshydro.Observations(
            _obshydro.Observation(obs_dt1, 0),
            _obshydro.Observation(obs_dt2, 60),
        )
        dtdeb = '2012-10-01 00:00'
        dtfin = '2012-11-01 00:00'
        dtprod = '2012-10-03 10:00'

        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, observations=obss)

        dt1 = _datetime.datetime(2012, 10, 3, 1, 0, 0)
        deltah1 = -10
        dt2 = _datetime.datetime(2012, 10, 3, 2, 0, 0)
        deltah2 = -15
        dt3 = _datetime.datetime(2012, 10, 3, 3, 0, 0)
        deltah3 = -20
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivot3 = PivotCC(dte=dt3, deltah=deltah3)
        pivots = [pivot1, pivot2, pivot3]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)

        serie_hcor = _htoq.correction_hauteurs(seriehydro=serie,
                                               courbecorrection=ccor,
                                               pivots=False)

        self.assertEqual(len(serie_hcor.observations), 2)
        serie_hcor = _htoq.correction_hauteurs(seriehydro=serie,
                                               courbecorrection=ccor,
                                               pivots=True)
        # print(serie_hcor.observations)
        self.assertEqual(len(serie_hcor.observations), 5)
        hcors = serie_hcor.observations['res'].tolist()
        self.assertTrue(_numpy.isnan(hcors[0]))
        self.assertEqual(hcors[1:4], [0, 5, 10])
        self.assertTrue(_numpy.isnan(hcors[4]))
        self.assertEqual(
            serie_hcor.observations.index.to_pydatetime().tolist(),
            [obs_dt1, dt1, dt2, dt3, obs_dt2])


    def test_error_01(self):
        """Wrong serie"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )

        dt1 = _datetime.datetime(2012, 10, 3, 6, 0, 0)
        deltah1 = -20
        dt2 = _datetime.datetime(2012, 10, 3, 7, 0, 0)
        deltah2 = -10
        dt3 = _datetime.datetime(2012, 10, 3, 8, 0, 0)
        deltah3 = -20
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivot3 = PivotCC(dte=dt3, deltah=deltah3)
        pivots = [pivot1, pivot2, pivot3]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)
        _htoq.correction_hauteurs(seriehydro=serie,
                                  courbecorrection=ccor)
        serie.grandeur = 'Q'
        with self.assertRaises(ValueError):
            _htoq.correction_hauteurs(seriehydro=serie, courbecorrection=ccor)


class TestCourbeTarageActive(unittest.TestCase):
    """courbetarage_active function tests."""

    def test_base_01(self):
        """Test with one courbetarage"""
        station = _sitehydro.Station(code='A123456789')
        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]
        ctar1 = CourbeTarage(code=-1, typect=4, station=station,
                             libelle='toto', periodes=periodes)
        dtes = [_datetime.datetime(2015, 1, 1),
                _datetime.datetime(2015, 8, 4, 17, 13, 25),
                _datetime.datetime(2016, 1, 1),
                _datetime.datetime(2016, 2, 1),
                _datetime.datetime(2016, 2, 18, 10, 9, 8),
                _datetime.datetime(2016, 11, 23, 4, 54, 31),
                _datetime.datetime(2017, 1, 1)]
        for dte in dtes:
            ctar = _htoq.courbetarage_active(courbestarage=ctar1, dte=dte)
            self.assertIsNotNone(ctar)
            self.assertEqual(ctar, ctar1)

        dtes = [_datetime.datetime(2010, 1, 1),
                _datetime.datetime(2011, 8, 4, 17, 13, 25),
                _datetime.datetime(2016, 1, 15),
                _datetime.datetime(2016, 1, 18, 10, 9, 8),
                _datetime.datetime(2017, 1, 1, 4, 7, 16)]
        for dte in dtes:
            ctar = _htoq.courbetarage_active(courbestarage=ctar1, dte=dte)
            self.assertIsNone(ctar)

    def test_base_02(self):
        """Test with two courbes de tarage"""
        station = _sitehydro.Station(code='A123456789')
        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))

        ctar1 = CourbeTarage(code=-1, typect=4, station=station,
                             libelle='toto', periodes=[periode1])

        ctar2 = CourbeTarage(code=-1, typect=4, station=station,
                             libelle='toto', periodes=[periode2])

        dtes = [_datetime.datetime(2015, 1, 1),
                _datetime.datetime(2015, 8, 4, 17, 13, 25),
                _datetime.datetime(2016, 1, 1)]
        for dte in dtes:
            ctar = _htoq.courbetarage_active(courbestarage=[ctar1, ctar2],
                                             dte=dte)
            self.assertIsNotNone(ctar)
            self.assertEqual(ctar, ctar1)
            self.assertNotEqual(ctar, ctar2)

        dtes = [_datetime.datetime(2016, 2, 1),
                _datetime.datetime(2016, 2, 18, 10, 9, 8),
                _datetime.datetime(2016, 11, 23, 4, 54, 31),
                _datetime.datetime(2017, 1, 1)]

        for dte in dtes:
            ctar = _htoq.courbetarage_active(courbestarage=[ctar1, ctar2],
                                             dte=dte)
            self.assertIsNotNone(ctar)
            self.assertEqual(ctar, ctar2)
            self.assertNotEqual(ctar, ctar1)

        dtes = [_datetime.datetime(2010, 1, 1),
                _datetime.datetime(2011, 8, 4, 17, 13, 25),
                _datetime.datetime(2016, 1, 15),
                _datetime.datetime(2016, 1, 18, 10, 9, 8),
                _datetime.datetime(2017, 1, 1, 4, 7, 16)]
        for dte in dtes:
            ctar = _htoq.courbetarage_active(courbestarage=[ctar1, ctar2],
                                             dte=dte)
            self.assertIsNone(ctar)

    def test_base_03(self):
        """Test courbetarage without periodes"""
        station = _sitehydro.Station(code='A123456789')
        ct1 = CourbeTarage(code=-1, typect=4, station=station,
                           libelle='toto')
        dte = _datetime.datetime(2015, 3, 4, 11, 12, 57)
        ctar = _htoq.courbetarage_active(courbestarage=[ct1], dte=dte)
        self.assertIsNone(ctar)

    def test_base_04(self):
        """Test without courbestarage"""
        dte = _datetime.datetime(2015, 3, 4, 11, 12, 57)
        ctar = _htoq.courbetarage_active(courbestarage=[], dte=dte)
        self.assertIsNone(ctar)

    def test_error_01(self):
        """Test with wrong courbestarage"""
        dte = _datetime.datetime(2015, 3, 4, 11, 12, 57)
        with self.assertRaises(TypeError):
            _htoq.courbetarage_active(courbestarage=['toto'], dte=dte)


class TestObshToObsq(unittest.TestCase):
    """Class test for conversion obsh to obsq"""

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

    def test_ct_poly(self):
        """Test courbe de tarage poly"""
        hauteur1 = 10
        debit1 = 20
        pivot1 = PivotCTPoly(hauteur=hauteur1, debit=debit1)

        hauteur2 = 30
        debit2 = 60
        pivot2 = PivotCTPoly(hauteur=hauteur2, debit=debit2)

        pivots = [pivot1, pivot2]
        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]

        code = 'tre'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        limiteinf = 11.3
        limitesup = 28.7

        ctar = CourbeTarage(code=code, libelle=libelle, station=station,
                            limiteinf=limiteinf, limitesup=limitesup,
                            pivots=pivots, periodes=periodes)

        dte = _datetime.datetime(2016, 8, 1)
        hauteurs = [10, 11.3, 15, 20, 28.6, 28.7, 28.9, 30]
        expected = [20, 22.6, 30, 40, 57.2, 57.4, 57.8, 60]
        expected_qal = [12, 12, 16, 16, 16, 12, 12, 12]
        for index, hauteur in enumerate(hauteurs):
            obsh = _obshydro.Observation(dte=dte, res=hauteur,
                                         qal=16, mth=0, cnt=0, statut=4)
            obsq = _htoq.obsh_to_obsq(obsh=obsh,
                                      courbestarage=[ctar])
            self.assertEqual(obsq['res'].item(), expected[index])
            self.assertEqual(obsq['qal'].item(), expected_qal[index])
        hauteurs = [5, 40]
        for index, hauteur in enumerate(hauteurs):
            obsh = _obshydro.Observation(dte=dte, res=hauteur,
                                         qal=16, mth=0, cnt=0, statut=4)
            obsq = _htoq.obsh_to_obsq(obsh=obsh,
                                      courbestarage=[ctar])
            self.assertTrue(_numpy.isnan(obsq['res'].item()))


    def test_ct_puissance(self):
        """Test courbe de tarage puissance"""
        hauteurs = [1860, 2000, 2050, 2060, 5800, 6000]

        expected_debits = [51.0078, 208.6478, 264.9478,
                           374.1812067, 520702.1351, 599996.0707]
        dte = _datetime.datetime(2016, 6, 1)

        for index, hauteur in enumerate(hauteurs):
            obsh = _obshydro.Observation(dte=dte, res=hauteur,
                                         qal=16, mth=0, cnt=0, statut=4)
            obsq = _htoq.obsh_to_obsq(obsh=obsh,
                                      courbestarage=[self.ct_puissance])

            self.assertAlmostEqual(obsq['res'].item(),
                                   expected_debits[index], 4)
            self.assertEqual(obsq['mth'].item(), 8)

        hauteurs = [1000, 1850, 6500]
        for hauteur in hauteurs:
            obsh = _obshydro.Observation(dte=dte, res=hauteur,
                                         qal=16, mth=0, cnt=0, statut=4)
            obsq = _htoq.obsh_to_obsq(obsh=obsh,
                                      courbestarage=[self.ct_puissance])

            self.assertTrue(_numpy.isnan(obsq['res'].item()))
            self.assertEqual(obsq['mth'].item(), 8)

    def test_sans_courbes(self):
        """test without courbestarage"""
        dte = _datetime.datetime(2015, 1, 2)
        hauteur = 156.15
        obsh = _obshydro.Observation(dte=dte, res=hauteur,
                                     qal=16, mth=0, cnt=0, statut=4)
        obsq = _htoq.obsh_to_obsq(obsh=obsh,
                                  courbestarage=[])
        self.assertTrue(_numpy.isnan(obsq['res'].item()))

    def test_error_01(self):
        """Test wrong ct puissance"""
        pivots = [PivotCTPuissance(hauteur=1860, qualif=20,
                                   vara=1, varb=1, varh=1),
                  PivotCTPuissance(hauteur=2050, qualif=20,
                                   vara=0.001126, varb=1, varh=1814.7)]
        station = _sitehydro.Station(code='A123456789')
        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]
        ctar = CourbeTarage(code=-1, typect=4, station=station,
                            libelle='toto', pivots=pivots, periodes=periodes)
        hauteur = 2000
        _htoq._debit_ctar_puissance(hauteur=hauteur, ctar=ctar)

        ctar.pivots[1].varh = 2100
        with self.assertRaises(ValueError):
            _htoq._debit_ctar_puissance(hauteur=hauteur, ctar=ctar)


class TestSerieHToSerieQ(unittest.TestCase):
    """serieh_to_serieq function tests."""

    @classmethod
    def setUpClass(cls):
        hauteur1 = 10
        debit1 = 20
        pivot1 = PivotCTPoly(hauteur=hauteur1, debit=debit1)

        hauteur2 = 30
        debit2 = 60
        pivot2 = PivotCTPoly(hauteur=hauteur2, debit=debit2)

        hauteur3 = 130
        debit3 = 160
        pivot3 = PivotCTPoly(hauteur=hauteur3, debit=debit3)

        pivots = [pivot1, pivot2, pivot3]
        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]

        code = 'tre'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')

        cls.ctar_poly = CourbeTarage(code=code, libelle=libelle,
                                     station=station, pivots=pivots,
                                     periodes=periodes)
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
        cls.ctar_puissance = CourbeTarage(code=-1,
                                          typect=4,
                                          station=station,
                                          libelle='toto', pivots=pivots,
                                          periodes=periodes)

    def test_base_01(self):
        """basic test"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-10-03 06:00', 0),
            _obshydro.Observation('2015-10-03 07:00', 10),
            _obshydro.Observation('2015-10-03 08:00', 30),
            _obshydro.Observation('2015-10-03 09:00', 50),
            _obshydro.Observation('2015-10-03 10:00', 100),
            _obshydro.Observation('2015-10-03 11:00', 150),
            _obshydro.Observation('2015-10-03 12:00', 100)
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
        serieq = _htoq.serieh_to_serieq(seriehydro=serie,
                                        courbestarage=[self.ctar_poly])

        self.assertEqual(serieq.grandeur, 'Q')
        self.assertEqual(len(serieq.observations), len(serie.observations))
        debits = serieq.observations['res'].tolist()

        # Vérification des débits
        self.assertTrue(_numpy.isnan(debits[0]))
        self.assertEqual(debits[1:5], [20, 60, 80, 130])
        self.assertTrue(_numpy.isnan(debits[5]))
        self.assertTrue(debits[6], 130)

        # Vérification des continuités
        cnts = serieq.observations['cnt'].tolist()
        self.assertEqual(cnts, [4, 4, 0, 0, 0, 8, 8])

    def test_base_02(self):
        """test with wrong courbecorrection"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-10-03 06:00', 0),
            _obshydro.Observation('2015-10-03 07:00', 10),
            _obshydro.Observation('2015-10-03 08:00', 30),
            _obshydro.Observation('2015-10-03 09:00', 50),
            _obshydro.Observation('2015-10-03 10:00', 100),
            _obshydro.Observation('2015-10-03 11:00', 150),
            _obshydro.Observation('2015-10-03 12:00', 100)
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

        dt1 = _datetime.datetime(2010, 10, 3, 8, 0, 0)
        deltah1 = 0
        dt2 = _datetime.datetime(2011, 10, 3, 10, 0, 0)
        deltah2 = -10
        station = _sitehydro.Station(code='O123456789')

        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)
        serieq = _htoq.serieh_to_serieq(seriehydro=serie,
                                        courbestarage=[self.ctar_poly],
                                        courbecorrection=ccor)
        self.assertEqual(serieq.grandeur, 'Q')
        for obs in serieq.observations.itertuples():
            self.assertTrue(_numpy.isnan(obs.res))
            self.assertEqual(obs.cnt, 1)
            self.assertEqual(obs.mth, 8)

    def test_base_03(self):
        """serie witout observations"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        dtdeb = '2012-10-03 05:00'
        dtfin = '2012-10-03 09:00'
        dtprod = '2012-10-03 10:00'
        strict = True
        sysalti = 0
        perime = False
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.MINUTES)
        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur, strict=strict,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, sysalti=sysalti,
            pdt=pdt, perime=perime
        )
        serieq = _htoq.serieh_to_serieq(seriehydro=serie,
                                        courbestarage=[self.ctar_poly])
        self.assertNotEqual(serieq, serie)
        self.assertNotEqual(serieq.dtprod, serie.dtprod)

    def test_base_04(self):
        """test without courbestarage"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-10-03 06:00', 0),
            _obshydro.Observation('2015-10-03 07:00', 10),
            _obshydro.Observation('2015-10-03 08:00', 30),
            _obshydro.Observation('2015-10-03 09:00', 50),
            _obshydro.Observation('2015-10-03 10:00', 100),
            _obshydro.Observation('2015-10-03 11:00', 150),
            _obshydro.Observation('2015-10-03 12:00', 100)
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
        serieq = _htoq.serieh_to_serieq(seriehydro=serie)
        self.assertEqual(len(serieq.observations), len(serie.observations))
        for res in serieq.observations['res'].tolist():
            self.assertTrue(_numpy.isnan(res))

    def test_pivots_ct_01(self):
        """test with adding pivots with courbe tarage poly"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obs_dt1 = _datetime.datetime(2015, 10, 3, 0, 0)
        obs_dt2 = _datetime.datetime(2015, 10, 3, 6, 0)
        obss = _obshydro.Observations(
            _obshydro.Observation(obs_dt1, 20),
            _obshydro.Observation(obs_dt2, 40),
        )
        dtdeb = '2015-10-03 00:00'
        dtfin = '2015-10-04 00:00'
        dtprod = '2015-10-04 00:00'

        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, observations=obss)

        serie_hcor = _htoq.serieh_to_serieq(seriehydro=serie,
                                            courbestarage=[self.ctar_poly],
                                            pivots=False)
        self.assertEqual(len(serie_hcor.observations), 2)

        serie_hcor = _htoq.serieh_to_serieq(seriehydro=serie,
                                            courbestarage=[self.ctar_poly],
                                            pivots=True)

        self.assertEqual(len(serie_hcor.observations), 3)
        self.assertEqual(serie_hcor.observations['res'].tolist(),
                         [40, 60, 70])

        self.assertEqual(
           serie_hcor.observations.index.to_pydatetime().tolist(),
           [obs_dt1, _datetime.datetime(2015, 10, 3, 3, 0), obs_dt2])

    def test_pivots_ct_02(self):
        """test with adding pivots with courbe tarage puissance"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obs_dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        obs_dt2 = _datetime.datetime(2015, 1, 2, 0, 0, 0)
        obss = _obshydro.Observations(
            _obshydro.Observation(obs_dt1, 1000),
            _obshydro.Observation(obs_dt2, 7000),
        )
        dtdeb = '2012-10-01 00:00'
        dtfin = '2012-11-01 00:00'
        dtprod = '2012-10-03 10:00'

        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, observations=obss)

        serie_hcor = _htoq.serieh_to_serieq(seriehydro=serie,
                                            courbestarage=self.ctar_puissance,
                                            pivots=False)
        self.assertEqual(len(serie_hcor.observations), 2)

        serie_hcor = _htoq.serieh_to_serieq(seriehydro=serie,
                                            courbestarage=self.ctar_puissance,
                                            pivots=True)
        self.assertEqual(len(serie_hcor.observations),
                         len(self.ctar_puissance.pivots) + 2)
        debits = serie_hcor.observations['res'].tolist()
        dtes = serie_hcor.observations.index.tolist()
        for index in range(1, len(self.ctar_puissance.pivots)):
            self.assertTrue(debits[index] < debits[index + 1])
            self.assertTrue(dtes[index] < dtes[index + 1])

        self.assertEqual(serie_hcor.observations['cnt'].tolist(),
                         [4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8])

        serie.observations = _obshydro.Observations(
            _obshydro.Observation(obs_dt1, 7000),
            _obshydro.Observation(obs_dt2, 1000),
        )
        serie_hcor = _htoq.serieh_to_serieq(seriehydro=serie,
                                            courbestarage=self.ctar_puissance,
                                            pivots=True)
        self.assertEqual(len(serie_hcor.observations),
                         len(self.ctar_puissance.pivots) + 2)

        debits = serie_hcor.observations['res'].tolist()
        dtes = serie_hcor.observations.index.tolist()
        for index in range(1, len(self.ctar_puissance.pivots)):
            self.assertTrue(debits[index] > debits[index + 1])
            self.assertTrue(dtes[index] < dtes[index + 1])

        self.assertEqual(serie_hcor.observations['cnt'].tolist(),
                         [8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4])

    def test_pivots_ct_03(self):
        """Test check no points with same date"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obs_dt1 = _datetime.datetime(2015, 1, 1, 0, 0, 0)
        obs_dt2 = _datetime.datetime(2015, 1, 1, 0, 0, 5)
        obss = _obshydro.Observations(
            _obshydro.Observation(obs_dt1, 1000),
            _obshydro.Observation(obs_dt2, 7000),
        )
        dtdeb = '2012-10-01 00:00'
        dtfin = '2012-11-01 00:00'
        dtprod = '2012-10-03 10:00'

        serie = _obshydro.Serie(
            entite=entite, grandeur=grandeur,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, observations=obss)

        serie_hcor = _htoq.serieh_to_serieq(seriehydro=serie,
                                            courbestarage=self.ctar_puissance,
                                            pivots=False)
        self.assertEqual(len(serie_hcor.observations), 2)

        serie_hcor = _htoq.serieh_to_serieq(seriehydro=serie,
                                            courbestarage=self.ctar_puissance,
                                            pivots=True)
        obss = serie_hcor.observations
        self.assertEqual(len(obss), 6)
        expected_dates = [_datetime.datetime(2015, 1, 1, 0, 0, seconds)
                          for seconds in range(0, 6)]
        self.assertEqual(obss.index.to_pydatetime().tolist(),
                         expected_dates)

        serie.observations = _obshydro.Observations(
            _obshydro.Observation(obs_dt1, 7000),
            _obshydro.Observation(obs_dt2, 1000),
        )
        serie_hcor = _htoq.serieh_to_serieq(seriehydro=serie,
                                            courbestarage=self.ctar_puissance,
                                            pivots=True)
        obss = serie_hcor.observations
        self.assertEqual(len(obss), 6)
        expected_dates = [_datetime.datetime(2015, 1, 1, 0, 0, seconds)
                          for seconds in range(0, 6)]
        self.assertEqual(obss.index.to_pydatetime().tolist(),
                         expected_dates)

    def test_error_01(self):
        """Test serie error"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'H'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-10-03 06:00', 0),
            _obshydro.Observation('2015-10-03 07:00', 10),
            _obshydro.Observation('2015-10-03 08:00', 30),
            _obshydro.Observation('2015-10-03 09:00', 50),
            _obshydro.Observation('2015-10-03 10:00', 100),
            _obshydro.Observation('2015-10-03 11:00', 150),
            _obshydro.Observation('2015-10-03 12:00', 100)
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
        _htoq.serieh_to_serieq(seriehydro=serie,
                               courbestarage=[self.ctar_poly])

        serie.grandeur = 'Q'
        with self.assertRaises(ValueError):
            _htoq.serieh_to_serieq(seriehydro=serie,
                                   courbestarage=[self.ctar_poly])

        serie = 'toto'
        with self.assertRaises(TypeError):
            _htoq.serieh_to_serieq(seriehydro=serie,
                                   courbestarage=[self.ctar_poly])


class TestCTarGetPivotsBetweenDebits(unittest.TestCase):
    """ctar_get_pivots_between_debits function tests."""

    def test_ctar_get_pivots_between_debits_poly(self):
        """Test function get_pivots_between_debits with ctar poly"""
        hauteur1 = 100.6
        debit1 = 2.3
        pivot1 = PivotCTPoly(hauteur=hauteur1, debit=debit1)

        hauteur2 = 145.2
        debit2 = 3.4
        pivot2 = PivotCTPoly(hauteur=hauteur2, debit=debit2)

        hauteur3 = 160.1
        debit3 = 4.8
        pivot3 = PivotCTPoly(hauteur=hauteur3, debit=debit3)

        code = 'tre'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')

        ctar = CourbeTarage(code=code, libelle=libelle, station=station,
                            pivots=[pivot1, pivot2, pivot3])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=2.3,
                                                      qmax=3.4)
        self.assertEqual(pivots, [pivot1, pivot2])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=2.4,
                                                      qmax=3.4)
        self.assertEqual(pivots, [pivot2])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=2.4,
                                                      qmax=3.3)
        self.assertEqual(pivots, [])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=2,
                                                      qmax=5)
        self.assertEqual(pivots, [pivot1, pivot2, pivot3])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=None,
                                                      qmax=3.0)
        self.assertEqual(pivots, [pivot1])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=4,
                                                      qmax=None)
        self.assertEqual(pivots, [pivot3])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=None,
                                                      qmax=None)
        self.assertEqual(pivots, [pivot1, pivot2, pivot3])

    def test_ctar_get_pivots_between_debits_puissance(self):
        """Test function get_pivots_between_debits with ctar puissance"""

        pivots_ct = [PivotCTPuissance(hauteur=1860, qualif=20,
                                      vara=1, varb=1, varh=1),
                     PivotCTPuissance(hauteur=2050, qualif=20,
                                      vara=0.001126, varb=1, varh=1814.7),
                     PivotCTPuissance(hauteur=2205, qualif=20,
                                      vara=0.005541, varb=1.1531, varh=2021.4)]
        station = _sitehydro.Station(code='A123456789')
        periode1 = PeriodeCT(dtdeb=_datetime.datetime(2015, 1, 1),
                             dtfin=_datetime.datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=_datetime.datetime(2016, 2, 1),
                             dtfin=_datetime.datetime(2017, 1, 1))
        periodes = [periode1, periode2]

        # débits des 3 pivots: 51.0078, 264.9478, 2259.7466]
        ctar = CourbeTarage(code=-1, typect=4, station=station,
                            libelle='toto', pivots=pivots_ct,
                            periodes=periodes)

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=51,
                                                      qmax=265)
        self.assertEqual(pivots, [pivots_ct[0], pivots_ct[1]])
        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=51.5,
                                                      qmax=265)
        self.assertEqual(pivots, [pivots_ct[1]])
        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=51.5,
                                                      qmax=264.8)
        self.assertEqual(pivots, [])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=50,
                                                      qmax=2260)
        self.assertEqual(pivots, [pivots_ct[0], pivots_ct[1], pivots_ct[2]])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=None,
                                                      qmax=2000)
        self.assertEqual(pivots, [pivots_ct[0], pivots_ct[1]])

        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=250,
                                                      qmax=None)
        self.assertEqual(pivots, [pivots_ct[1], pivots_ct[2]])
        pivots = _htoq.ctar_get_pivots_between_debits(ctar=ctar, qmin=None,
                                                      qmax=None)
        self.assertEqual(pivots, [pivots_ct[0], pivots_ct[1], pivots_ct[2]])

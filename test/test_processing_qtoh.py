# -*- coding: utf-8 -*-

"""Test program for module libhydro.processing.qtoh.

To run all tests just type:
    python -m unittest test_processing_qtoh

To run only a class test:
    python -m unittest test_processing_qtoh.TestClass

To run only a specific test:
    python -m unittest test_processing_qtoh.TestClass.test_method

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
from libhydro.processing import qtoh as _qtoh


# -- strings ------------------------------------------------------------------
__version__ = '0.1'
__date__ = '2019-02-07'

# HISTORY
# V0.1 - SR - 2017-05-04
#   first shot


class TestObsqToObsh(unittest.TestCase):
    """Class test for conversion obsq to obsh"""

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

        expected = [10, 11.3, 15, 20, 28.6, 28.7, 28.9, 30]
        debits = [20, 22.6, 30, 40, 57.2, 57.4, 57.8, 60]
        expected_qal = [12, 12, 16, 16, 16, 12, 12, 12]
        for index, debit in enumerate(debits):
            obsq = _obshydro.Observation(dte=dte, res=debit,
                                         qal=16, mth=0, cnt=0, statut=4)
            obsh = _qtoh.obsq_to_obsh(obsq=obsq,
                                      courbestarage=[ctar])
            self.assertEqual(obsh['res'].item(), expected[index])
            self.assertEqual(obsh['qal'].item(), expected_qal[index])

        debits = [0, 10, 80]
        for index, debit in enumerate(debits):
            obsq = _obshydro.Observation(dte=dte, res=debit,
                                         qal=16, mth=0, cnt=0, statut=4)
            obsh = _qtoh.obsq_to_obsh(obsq=obsq,
                                      courbestarage=[ctar])
            self.assertTrue(_numpy.isnan(obsh['res'].item()))

    def test_ct_puissance(self):
        """Test courbe de tarage puissance"""
        dte = _datetime.datetime(2016, 6, 1)

        expected_hauteurs = [1860, 2000, 2050, 2060, 5800, 6000]

        debits = [51.0078, 208.6478, 264.9478,
                  374.1812067, 520702.1351, 599996.0707]

        for index, debit in enumerate(debits):
            obsq = _obshydro.Observation(dte=dte, res=debit,
                                         qal=16, mth=0, cnt=0, statut=4)
            obsh = _qtoh.obsq_to_obsh(obsq=obsq,
                                      courbestarage=[self.ct_puissance])

            self.assertAlmostEqual(obsh['res'].item(),
                                   expected_hauteurs[index], 4)
            self.assertEqual(obsh['mth'].item(), 8)

        # hauteurs = [1000, 1850, 6500]
        debits = [0, 50, 600000]
        for debit in debits:
            obsq = _obshydro.Observation(dte=dte, res=debit,
                                         qal=16, mth=0, cnt=0, statut=4)
            obsh = _qtoh.obsq_to_obsh(obsq=obsq,
                                      courbestarage=[self.ct_puissance])

            self.assertTrue(_numpy.isnan(obsh['res'].item()))
            self.assertEqual(obsh['mth'].item(), 8)

    def test_sans_courbes(self):
        """test without courbestarage"""
        dte = _datetime.datetime(2015, 1, 2)
        debit = 156.15
        obsq = _obshydro.Observation(dte=dte, res=debit,
                                     qal=16, mth=0, cnt=0, statut=4)
        obsh = _qtoh.obsq_to_obsh(obsq=obsq,
                                  courbestarage=[])
        self.assertTrue(_numpy.isnan(obsh['res'].item()))

    @unittest.skip("ct error")
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
        debit = 200
        hauteur, qualif = _qtoh._hauteur_ctar_puissance(debit=debit, ctar=ctar)
        self.assertIsNotNone(hauteur)
        ctar.pivots[1].vara = 0
        with self.assertRaises(ValueError):
            hauteur, qual = _qtoh._hauteur_ctar_puissance(debit=debit, ctar=ctar)
        ctar.pivots[1].varb = 0
        with self.assertRaises(ValueError):
            hauteur, qual = _qtoh._hauteur_ctar_puissance(debit=debit, ctar=ctar)


class TestSerieQToSerieH(unittest.TestCase):
    """serieq_to_serieh function tests."""

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

    def test_base_01(self):
        """basic test"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'Q'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-10-03 06:00', 10),
            _obshydro.Observation('2015-10-03 07:00', 20),
            _obshydro.Observation('2015-10-03 08:00', 60),
            _obshydro.Observation('2015-10-03 09:00', 80),
            _obshydro.Observation('2015-10-03 10:00', 130),
            _obshydro.Observation('2015-10-03 11:00', 170),
            _obshydro.Observation('2015-10-03 12:00', 130)
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
        serieh = _qtoh.serieq_to_serieh(seriehydro=serie,
                                        courbestarage=[self.ctar_poly])

        self.assertEqual(serieh.grandeur, 'H')
        self.assertEqual(len(serieh.observations), len(serie.observations))
        hauteurs = serieh.observations['res'].tolist()

        # Vérification des débits
        self.assertTrue(_numpy.isnan(hauteurs[0]))
        # self.assertEqual(hauteurs[1:5], [20, 60, 80, 130])
        self.assertEqual(hauteurs[1:5], [10, 30, 50, 100])
        self.assertTrue(_numpy.isnan(hauteurs[5]))
        self.assertTrue(hauteurs[6], 100)

        # Vérification des continuités
        cnts = serieh.observations['cnt'].tolist()
        self.assertEqual(cnts, [4, 4, 0, 0, 0, 8, 8])

    def test_base_02(self):
        """test with courbe de tarage and courbe de correction"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'Q'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-10-03 06:00', 10),
            _obshydro.Observation('2015-10-03 07:00', 20),
            _obshydro.Observation('2015-10-03 08:00', 60),
            _obshydro.Observation('2015-10-03 09:00', 80),
            _obshydro.Observation('2015-10-03 10:00', 130),
            _obshydro.Observation('2015-10-03 11:00', 170),
            _obshydro.Observation('2015-10-03 12:00', 130)
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
        
        dt1 = _datetime.datetime(2015, 1, 1)
        dt2 = _datetime.datetime(2016, 1, 1)
        deltah1 = -10
        deltah2 = -10
        station = _sitehydro.Station(code='O123456789')
        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)
        
        serieh = _qtoh.serieq_to_serieh(seriehydro=serie,
                                        courbestarage=self.ctar_poly,
                                        courbecorrection=ccor)

        self.assertEqual(serieh.grandeur, 'H')
        self.assertEqual(len(serieh.observations), len(serie.observations))
        hauteurs = serieh.observations['res'].tolist()

        # Vérification des débits
        self.assertTrue(_numpy.isnan(hauteurs[0]))
        # self.assertEqual(hauteurs[1:5], [20, 60, 80, 130])
        self.assertEqual(hauteurs[1:5], [20, 40, 60, 110])
        self.assertTrue(_numpy.isnan(hauteurs[5]))
        self.assertTrue(hauteurs[6], 110)

        # Vérification des continuités
        cnts = serieh.observations['cnt'].tolist()
        self.assertEqual(cnts, [4, 4, 0, 0, 0, 8, 8])
        
        # Test avec une courbe ce correction incmplete
        pivot2.dte = _datetime.datetime(2015, 10, 3, 9, 0, 0)
        serieh = _qtoh.serieq_to_serieh(seriehydro=serie,
                                        courbestarage=[self.ctar_poly],
                                        courbecorrection=ccor)
        self.assertEqual(serieh.grandeur, 'H')
        self.assertEqual(len(serieh.observations), len(serie.observations))
        hauteurs = serieh.observations['res'].tolist()

        # Vérification des débits
        self.assertTrue(_numpy.isnan(hauteurs[0]))
        # self.assertEqual(hauteurs[1:5], [20, 60, 80, 130])
        self.assertEqual(hauteurs[1:4], [20, 40, 60])
        self.assertTrue(_numpy.isnan(hauteurs[4]))
        self.assertTrue(_numpy.isnan(hauteurs[5]))
        self.assertTrue(_numpy.isnan(hauteurs[6]))

        # Vérification des continuités
        cnts = serieh.observations['cnt'].tolist()
        self.assertEqual(cnts, [4, 4, 0, 0, 1, 1, 1])


    def test_base_03(self):
        """test with wrong courbecorrection"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'Q'
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
        serieh = _qtoh.serieq_to_serieh(seriehydro=serie,
                                        courbestarage=[self.ctar_poly],
                                        courbecorrection=ccor)
        self.assertEqual(serieh.grandeur, 'H')
        for obs in serieh.observations.itertuples():
            self.assertTrue(_numpy.isnan(obs.res))
            self.assertEqual(obs.cnt, 1)
            self.assertEqual(obs.mth, 8)

    def test_base_04(self):
        """serie witout observations"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'Q'
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
        serieq = _qtoh.serieq_to_serieh(seriehydro=serie,
                                        courbestarage=[self.ctar_poly])
        self.assertNotEqual(serieq, serie)
        self.assertNotEqual(serieq.dtprod, serie.dtprod)

    def test_base_05(self):
        """test without courbestarage"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'Q'
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
        serieq = _qtoh.serieq_to_serieh(seriehydro=serie)
        self.assertEqual(len(serieq.observations), len(serie.observations))
        for res in serieq.observations['res'].tolist():
            self.assertTrue(_numpy.isnan(res))

    def test_base_06(self):
        """test with nan"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'Q'
        obss = _obshydro.Observations(
            _obshydro.Observation('2015-10-03 06:00', 10),
            _obshydro.Observation('2015-10-03 07:00', 20),
            _obshydro.Observation('2015-10-03 08:00', 60),
            _obshydro.Observation('2015-10-03 09:00', None),
            _obshydro.Observation('2015-10-03 10:00', 130),
            _obshydro.Observation('2015-10-03 11:00', 170),
            _obshydro.Observation('2015-10-03 12:00', 130)
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
        
        dt1 = _datetime.datetime(2015, 1, 1)
        dt2 = _datetime.datetime(2016, 1, 1)
        deltah1 = -10
        deltah2 = -10
        station = _sitehydro.Station(code='O123456789')
        pivot1 = PivotCC(dte=dt1, deltah=deltah1)
        pivot2 = PivotCC(dte=dt2, deltah=deltah2)
        pivots = [pivot1, pivot2]
        dtmaj = _datetime.datetime(2017, 6, 21, 8, 37, 15)

        ccor = CourbeCorrection(station=station, pivots=pivots, dtmaj=dtmaj)
        
        serieh = _qtoh.serieq_to_serieh(seriehydro=serie,
                                        courbestarage=self.ctar_poly,
                                        courbecorrection=ccor)

        self.assertEqual(serieh.grandeur, 'H')
        self.assertEqual(len(serieh.observations), len(serie.observations))
        hauteurs = serieh.observations['res'].tolist()

        # Vérification des débits
        self.assertTrue(_numpy.isnan(hauteurs[0]))
        self.assertEqual((hauteurs[1], hauteurs[2], hauteurs[4]),
                         (20, 40, 110))
        self.assertTrue(_numpy.isnan(hauteurs[3]))
        self.assertTrue(_numpy.isnan(hauteurs[5]))
        self.assertTrue(hauteurs[6], 110)

        # Vérification des continuités
        cnts = serieh.observations['cnt'].tolist()
        self.assertEqual(cnts, [4, 4, 0, 1, 1, 8, 8])

    def test_error_01(self):
        """Test serie error"""
        entite = _sitehydro.Capteur(
            code='A12345678901', libelle='Le Rhône à Marseille'
        )
        grandeur = 'Q'
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
        _qtoh.serieq_to_serieh(seriehydro=serie,
                               courbestarage=[self.ctar_poly])

        serie.grandeur = 'H'
        with self.assertRaises(ValueError):
            _qtoh.serieq_to_serieh(seriehydro=serie,
                                   courbestarage=[self.ctar_poly])

        serie = 'toto'
        with self.assertRaises(TypeError):
            _qtoh.serieq_to_serieh(seriehydro=serie,
                                   courbestarage=[self.ctar_poly])

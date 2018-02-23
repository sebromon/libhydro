# -*- coding: utf-8 -*-
"""Test program for obselaboreehydro.

To run all tests just type:
    python -m unittest test_core_obselaboreehydro

To run only a class test:
    python -m unittest test_core_obselaboreehydro.TestClass

To run only a specific test:
    python -m unittest test_core_obselaboreehydro.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import unittest
import datetime
import numpy as _numpy

from libhydro.core.obselaboreehydro import (ObservationElaboree,
                                            ObservationsElaborees,
                                            SerieObsElab)
from libhydro.core import (intervenant as _intervenant,
                           sitehydro as _sitehydro,
                           _composant)

# -- strings ------------------------------------------------------------------
__author__ = """Sébastien ROMON""" \
             """<sebastien.romon@developpement-durable.gouv.fr>"""
__version__ = """0.1"""
__date__ = """2018-02-12"""

# HISTORY
# V0.1
# V0.1 - 2018-02-12
#   first shot


# -- class TestObservationElaboree --------------------------------------------
class TestObservationElaboree(unittest.TestCase):
    """"ObservationElaboree class tests."""

    def test_base_01(self):
        """Base case test."""
        dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        cnt = 1
        statut = 8
        obs = ObservationElaboree(dte=dte,
                                  res=res,
                                  mth=mth,
                                  qal=qal,
                                  cnt=cnt,
                                  statut=statut
                                  )
        self.assertEqual(obs.item(),
                         (dte, res, mth, qal, cnt, statut))

    def test_base_02(self):
        """Check default values."""
        # dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        obs = ObservationElaboree()
        statut = 4
        qal = 16
        mth = 0
        cnt = 0
        dte = None
        res = 0.0
        self.assertEqual(obs.item(),
                         (dte, res, mth, qal, cnt, statut))

    def test_base_03(self):
        """Check instanciatiosn."""
        dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        cnt = 1
        statut = 8
        obs = ObservationElaboree(dte=dte,
                                  res=res,
                                  mth=mth,
                                  qal=qal,
                                  cnt=cnt,
                                  statut=statut
                                  )
        self.assertEqual(obs.item(),
                         (dte, res, mth, qal, cnt, statut))
        obs = ObservationElaboree(dte, res, mth, qal, cnt, statut)
        self.assertEqual(obs.item(),
                         (dte, res, mth, qal, cnt, statut))
        dte2 = '2016-02-10T09:17:43'
        obs = ObservationElaboree(dte2, res, mth, qal, cnt, statut)
        self.assertEqual(obs.item(),
                         (dte, res, mth, qal, cnt, statut))
        dte3 = _numpy.datetime64(dte, 's')
        obs = ObservationElaboree(dte3, res, mth, qal, cnt, statut)
        self.assertEqual(obs.item(),
                         (dte, res, mth, qal, cnt, statut))

    def test_str_01(self):
        dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        cnt = 1
        statut = 8
        obs = ObservationElaboree(dte=dte,
                                  res=res,
                                  mth=mth,
                                  qal=qal,
                                  cnt=cnt,
                                  statut=statut
                                  )
        obs.__str__()
        # print(obs)

    def test_error_02(self):
        """dte error."""
        dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        cnt = 1
        statut = 8
        ObservationElaboree(dte=dte,
                            res=res,
                            mth=mth,
                            qal=qal,
                            cnt=cnt,
                            statut=statut
                            )
        dte = 'a'
        with self.assertRaises(ValueError) as cm:
            ObservationElaboree(dte=dte,
                                res=res,
                                mth=mth,
                                qal=qal,
                                cnt=cnt,
                                statut=statut)

        dte = '2018-15-01 00:05:06'
        with self.assertRaises(ValueError) as cm:
            ObservationElaboree(dte=dte,
                                res=res,
                                mth=mth,
                                qal=qal,
                                cnt=cnt,
                                statut=statut)

    def test_error_03(self):
        """res error."""
        dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        cnt = 1
        statut = 8
        ObservationElaboree(dte=dte,
                            res=res,
                            mth=mth,
                            qal=qal,
                            cnt=cnt,
                            statut=statut
                            )
        res = 'a'
        with self.assertRaises(ValueError) as cm:
            ObservationElaboree(dte=dte,
                                res=res,
                                mth=mth,
                                qal=qal,
                                cnt=cnt,
                                statut=statut)

    def test_error_04(self):
        """qal error."""
        dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        cnt = 1
        statut = 8
        ObservationElaboree(dte=dte,
                            res=res,
                            mth=mth,
                            qal=qal,
                            cnt=cnt,
                            statut=statut
                            )
        for qal in [-5, 102, 'a']:
            with self.assertRaises(ValueError) as cm:
                ObservationElaboree(dte=dte,
                                    res=res,
                                    mth=mth,
                                    qal=qal,
                                    cnt=cnt,
                                    statut=statut)
            self.assertEqual(str(cm.exception),
                             'incorrect qualification')

    def test_error_05(self):
        """mth error."""
        dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        cnt = 1
        statut = 8
        ObservationElaboree(dte=dte,
                            res=res,
                            mth=mth,
                            qal=qal,
                            cnt=cnt,
                            statut=statut
                            )
        for mth in [-5, 102, 'a']:
            with self.assertRaises(ValueError) as cm:
                ObservationElaboree(dte=dte,
                                    res=res,
                                    mth=mth,
                                    qal=qal,
                                    cnt=cnt,
                                    statut=statut)
            self.assertEqual(str(cm.exception),
                             'incorrect method')

    def test_error_06(self):
        """cnt error."""
        dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        cnt = 1
        statut = 8
        ObservationElaboree(dte=dte,
                            res=res,
                            mth=mth,
                            qal=qal,
                            cnt=cnt,
                            statut=statut
                            )
        for cnt in [-5, 102, 'a']:
            with self.assertRaises(ValueError) as cm:
                ObservationElaboree(dte=dte,
                                    res=res,
                                    mth=mth,
                                    qal=qal,
                                    cnt=cnt,
                                    statut=statut)
            self.assertEqual(str(cm.exception),
                             'incorrect continuite')

    def test_error_07(self):
        """statut error."""
        dte = datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        cnt = 1
        statut = 8
        ObservationElaboree(dte=dte,
                            res=res,
                            mth=mth,
                            qal=qal,
                            cnt=cnt,
                            statut=statut
                            )
        for statut in [-5, 102, 'a']:
            with self.assertRaises(ValueError) as cm:
                ObservationElaboree(dte=dte,
                                    res=res,
                                    mth=mth,
                                    qal=qal,
                                    cnt=cnt,
                                    statut=statut)
            self.assertEqual(str(cm.exception),
                             'incorrect statut')


# -- class TestObservationsElaborees ------------------------------------------
class TestObservationsElaborees(unittest.TestCase):
    """ObservationsElaborees class tests."""

    def test_base_01(self):
        """Simple test."""
        # The simpliest __init_: datetime and res
        obs = ObservationsElaborees(
            ObservationElaboree('2012-10-03 06:00', 33),
            ObservationElaboree('2012-10-03 07:00', 37),
            ObservationElaboree('2012-10-03 08:00', 42)
        )
        self.assertEqual(
            obs['res'].tolist(),
            [33, 37, 42]
        )

    def test_base_02(self):
        """Simple test."""
        # The simpliest __init_: datetime and res
        obs = ObservationsElaborees(
            ObservationElaboree(res=33),
            ObservationElaboree('2012-10-03 07:00', 37),
            ObservationElaboree('2012-10-03 08:00', 42)
        )
        self.assertEqual(
            obs['res'].tolist(),
            [33, 37, 42]
        )

    def test_base_03(self):
        observations = []
        obs = ObservationsElaborees(*observations)
        ObservationsElaborees()
        # self.assertIsNone(obs)

    def test_error_01(self):
        """Error test"""
        with self.assertRaises(TypeError):
            ObservationsElaborees(
                33,
                ObservationElaboree('2012-10-03 07:00', 37),
                ObservationElaboree('2012-10-03 08:00', 42)
                )


# -- class TestObservationsElaboreesConcat ------------------------------------
class TestObservationsElaboreesConcat(unittest.TestCase):
    """Test static method concat class ObservationsElaborees"""

    def test_base_01(self):
        obs1 = ObservationsElaborees(
            ObservationElaboree('2012-10-03 06:00', 33),
            ObservationElaboree('2012-10-03 07:00', 37),
            ObservationElaboree('2012-10-03 08:00', 42)
        )
        obs2 = ObservationsElaborees(
            ObservationElaboree('2012-10-04 06:00', 330),
            ObservationElaboree('2012-10-04 07:00', 370),
            ObservationElaboree('2012-10-04 08:00', 420)
        )

        obs = ObservationsElaborees.concat(obs1, obs2)
        self.assertEqual(len(obs), 6)

    def test_base_02(self):
        obs1 = ObservationsElaborees(
            ObservationElaboree('2012-10-03 06:00', 33),
            ObservationElaboree('2012-10-03 07:00', 37),
            ObservationElaboree('2012-10-03 08:00', 42)
        )
        obs2 = ObservationElaboree('2012-10-04 06:00', 330)
        obs = ObservationsElaborees.concat(obs1, obs2)
        self.assertEqual(len(obs), 4)


# -- class TestSerieObsElab ------------------------------------------
class TestSerieObsElab(unittest.TestCase):
    """"SerieObsElab class tests."""

    def test_base_01(self):
        """Simple test"""
        entite = _sitehydro.Sitehydro(code='A1234567')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        dtdeb = datetime.datetime(2013, 8, 15, 23, 14, 13)
        dtfin = datetime.datetime(2014, 2, 21, 8, 4, 55)
        dtactivation = datetime.datetime(2016, 9, 23, 11, 29, 37)
        dtdesactivation = datetime.datetime(2017, 4, 29, 17, 11, 30)
        contact = _intervenant.Contact(code='154')
        typegrd = 'QINnJ'
        pdt = _composant.PasDeTemps(duree=1,
                                    unite=_composant.PasDeTemps.JOURS)
        glissant = True
        sysalti = 1
        obs = ObservationsElaborees(
            ObservationElaboree(res=33),
            ObservationElaboree('2012-10-03 07:00', 37),
            ObservationElaboree('2012-10-03 08:00', 42)
        )
        serie = SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                             pdt=pdt, dtdeb=dtdeb, dtfin=dtfin,
                             dtdesactivation=dtdesactivation, sysalti=sysalti,
                             dtactivation=dtactivation, glissant=glissant,
                             contact=contact, observations=obs)
        self.assertEqual((serie.entite, serie.dtprod, serie.typegrd, serie.pdt,
                          serie.dtdeb, serie.dtfin, serie.dtdesactivation,
                          serie.sysalti, serie.dtactivation, serie.glissant,
                          serie.contact),
                         (entite, dtprod, typegrd, pdt,
                          dtdeb, dtfin, dtdesactivation,
                          sysalti, dtactivation, glissant, contact))

    def test_base_02(self):
        """default value"""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmM'
        serie = SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd)
        self.assertEqual((serie.entite, serie.dtprod, serie.typegrd, serie.pdt,
                          serie.dtdeb, serie.dtfin, serie.dtdesactivation,
                          serie.sysalti, serie.dtactivation, serie.glissant,
                          serie.contact),
                         (entite, dtprod, typegrd, None,
                          None, None, None,
                          31, None, None, None))

    def test_base_03(self):
        """different values of typegrd and pdt"""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'HIXnJ'
        pdt = _composant.PasDeTemps(duree=2,
                                    unite=_composant.PasDeTemps.JOURS)
        serie = SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                             pdt=pdt)
        self.assertEqual((serie.entite, serie.dtprod, serie.typegrd, serie.pdt,
                          serie.dtdeb, serie.dtfin, serie.dtdesactivation,
                          serie.sysalti, serie.dtactivation, serie.glissant,
                          serie.contact),
                         (entite, dtprod, typegrd, pdt,
                          None, None, None,
                          31, None, None, None))

        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmnH'
        pdt = _composant.PasDeTemps(duree=3,
                                    unite=_composant.PasDeTemps.HEURES)
        serie = SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                             pdt=pdt)
        self.assertEqual((serie.entite, serie.dtprod, serie.typegrd, serie.pdt,
                          serie.dtdeb, serie.dtfin, serie.dtdesactivation,
                          serie.sysalti, serie.dtactivation, serie.glissant,
                          serie.contact),
                         (entite, dtprod, typegrd, pdt,
                          None, None, None,
                          31, None, None, None))

    def test_str_01(self):
        """Serie representation test"""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmM'
        serie = SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd)
        self.assertTrue(serie.__str__().find('<sans observations>') != -1)

    def test_str_02(self):
        """Serie representation with observations test"""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmM'
        obs = ObservationsElaborees(
            ObservationElaboree(res=33),
            ObservationElaboree('2012-10-03 07:00', 37),
            ObservationElaboree('2012-10-03 08:00', 42)
        )
        serie = SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                             observations=obs)
        self.assertTrue(serie.__str__().find(typegrd) != -1)
        self.assertTrue(serie.__str__().find('37') != -1)
        self.assertTrue(serie.__str__().find('2012-10-03 08:00:00') != -1)
        # print(serie)

    def test_str_03(self):
        """Serie representation fuzzy mode  test"""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'toto'
        serie = SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                             strict=False)
        self.assertTrue(serie.__str__().find(typegrd) != -1)
        # type de grandeur inconnu
        self.assertTrue(serie.__str__().find('inconnu') != -1)

    def test_error_01(self):
        """entite errorr"""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmM'
        SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd)

        for entite in [None, 'A1234567']:
            with self.assertRaises(TypeError) as cm:
                SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd)
            # print(cm.exception)

    def test_error_02(self):
        """dtprod error."""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmM'
        SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd)

        for dtprod in [None, 'a']:
            with self.assertRaises(Exception) as cm:
                SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd)
            # print(cm.exception)

    def test_error_03(self):
        """typegrd error."""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmM'
        SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd)

        for typegrd in [None, 'abc']:
            with self.assertRaises(Exception) as cm:
                SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd)
            # print(cm.exception)

    def test_error_pdt_01(self):
        """test error pdt in days"""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'HINnJ'
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.JOURS)
        SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                     pdt=pdt)
        pdt = 'toto'
        with self.assertRaises(Exception) as cm:
            SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                         pdt=pdt)

        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.HEURES)
        with self.assertRaises(ValueError) as cm:
            SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                         pdt=pdt)

    def test_error_pdt_02(self):
        """test error pdt in hours"""
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'HmnH'
        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.HEURES)
        SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                     pdt=pdt)
        pdt = 'toto'
        with self.assertRaises(Exception) as cm:
            SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                         pdt=pdt)

        pdt = _composant.PasDeTemps(duree=5,
                                    unite=_composant.PasDeTemps.JOURS)

        with self.assertRaises(ValueError):
            SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                         pdt=pdt)

    def test_error_glissant(self):
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmM'
        glissant = True
        SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                     glissant=glissant)
        glissant = 'toto'
        with self.assertRaises(Exception) as cm:
            SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                         glissant=glissant)

    def test_error_contact(self):
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmM'
        contact = _intervenant.Contact(code='1234')
        SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                     contact=contact)
        for contact in ['123', 'toto']:
            with self.assertRaises(Exception):
                SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                             contact=contact)

    def test_error_observations(self):
        entite = _sitehydro.Station(code='A123456789')
        dtprod = datetime.datetime(2015, 3, 4, 15, 47, 23)
        typegrd = 'QmM'
        obs = ObservationsElaborees(
            ObservationElaboree(res=33),
            ObservationElaboree('2012-10-03 07:00', 37),
            ObservationElaboree('2012-10-03 08:00', 42)
        )
        SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                     observations=obs)
        for obs in [[45, 18], 38]:
            with self.assertRaises(Exception):
                SerieObsElab(entite=entite, dtprod=dtprod, typegrd=typegrd,
                             observations=obs)

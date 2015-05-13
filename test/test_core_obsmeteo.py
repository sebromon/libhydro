# coding: utf-8
"""Test program for obsmeteo.

To run all tests just type:
    python -m unittest test_core_obsmeteo

To run only a class test:
    python -m unittest test_core_obsmeteo.TestClass

To run only a specific test:
    python -m unittest test_core_obsmeteo.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys
sys.path.append('..')

import unittest
import datetime
import numpy

from libhydro.core import (sitemeteo, obsmeteo, intervenant)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin""" \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1d"""
__date__ = """2014-07-30"""

# HISTORY
# V0.1 - 2014-07-16
#   first shot


# -- class TestObservation ----------------------------------------------------
class TestObservation(unittest.TestCase):

    """Observation class tests."""

    def test_base_01(self):
        """Base case test."""
        dte = '2000-01-01 10:33:01+0000'
        res = 20.5
        mth = 4
        qal = 0
        qua = 98
        obs = obsmeteo.Observation(dte, res, mth, qal, qua)
        self.assertEqual(
            obs.item(),
            (datetime.datetime(2000, 1, 1, 10, 33, 1), res, mth, qal, qua)
        )

    def test_base_02(self):
        """Some instanciation use cases."""
        obsmeteo.Observation('2000-01-01 10:33:01', 20)
        obsmeteo.Observation('2000-01-01 10:33', 0, 4)
        obsmeteo.Observation('2000-01-01 00:00+0100', 10, 4, 12, True)
        obsmeteo.Observation(
            datetime.datetime(2000, 1, 1, 10), 10, mth=4, qal=16
        )
        obsmeteo.Observation(datetime.datetime(2000, 1, 1), '20', qua=10)
        self.assertTrue(True)  # avoid pylint warning !

    def test_str_01(self):
        """Test __str__ method."""
        dte = '2000-01-01 10:33:01+0000'
        res = 20.5
        mth = 4
        qal = 12
        qua = 25.3
        obs = obsmeteo.Observation(dte, res, mth, qal, qua)
        self.assertTrue(obs.__str__().rfind('UTC') > -1)
        self.assertTrue(obs.__str__().rfind('qualite') > -1)

    def test_error_01(self):
        """Date error."""
        obsmeteo.Observation(**{'dte': '2000-10-10 10:00', 'res': 10})
        with self.assertRaises(TypeError):
            obsmeteo.Observation(**{'dte': '2000-10', 'res': 10})

    def test_error_02(self):
        """Test Res error."""
        obsmeteo.Observation(**{'dte': '2000-10-05 10:00', 'res': 10})
        with self.assertRaises(ValueError):
            obsmeteo.Observation(**{'dte': '2000-10-05 10:00', 'res': 'aaa'})

    def test_error_03(self):
        """Mth error."""
        obsmeteo.Observation(
            **{'dte': '2000-10-05 10:00', 'res': 20, 'mth': 4}
        )
        with self.assertRaises(ValueError):
            obsmeteo.Observation(
                **{'dte': '2000-10-05 10:00', 'res': 20, 'mth': 1000}
            )

    def test_error_04(self):
        """Qal error."""
        obsmeteo.Observation(
            **{'dte': '2000-10-05 10:00', 'res': 20, 'qal': 16}
        )
        with self.assertRaises(ValueError):
            obsmeteo.Observation(
                **{'dte': '2000-10-05 10:00', 'res': 20, 'qal': 1000}
            )

    def test_error_05(self):
        """Qua error."""
        obsmeteo.Observation(
            **{'dte': '2000-10-05 10:00', 'res': 20, 'qua': 95.8}
        )
        with self.assertRaises(ValueError):
            obsmeteo.Observation(
                **{'dte': '2000-10-05 10:00', 'res': 20, 'qua': '95.aaa'}
            )
        with self.assertRaises(ValueError):
            obsmeteo.Observation(
                **{'dte': '2000-10-05 10:00', 'res': 20, 'qua': -1}
            )
        with self.assertRaises(ValueError):
            obsmeteo.Observation(
                **{'dte': '2000-10-05 10:00', 'res': 20, 'qua': 101}
            )


# -- class TestObservations ---------------------------------------------------
class TestObservations(unittest.TestCase):

    """Observations class tests."""

    def test_base_01(self):
        """Simple test."""
        # The simpliest __init_: datetime and res
        obs = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00', 33),
            obsmeteo.Observation('2012-10-03 07:00', 37),
            obsmeteo.Observation('2012-10-03 08:00', 42)
        )
        self.assertEqual(
            obs['res'].tolist(),
            [33, 37, 42]
        )

    def test_base_02(self):
        """Base case test."""
        # Datetime, res and others attributes
        obs = obsmeteo.Observations(
            obsmeteo.Observation(
                '2012-10-03 06:00', 33, mth=4, qal=0, qua=100),
            obsmeteo.Observation(
                '2012-10-03 07:00', 37, mth=0, qal=12),
            obsmeteo.Observation(
                '2012-10-03 08:00', 42, mth=12, qal=20, qua=99)
        )
        self.assertEqual(
            obs['mth'].tolist(),
            [4, 0, 12]
        )
        self.assertEqual(
            obs['qal'].tolist(),
            [0, 12, 20]
        )
        self.assertEqual(
            obs['qua'].tolist()[::2],
            [100, 99]
        )
        self.assertTrue(numpy.isnan(obs['qua'].tolist()[1]))

    def test_error_01(self):
        """List of observation error."""
        # check that init works when call regurlaly...
        o = obsmeteo.Observation(
            '2012-10-03 06:00', 33, mth=4, qal=0, qua=25.2
        )
        obsmeteo.Observations(*[o, o])
        # ...and fails otherwise
        with self.assertRaises(TypeError):
            # *[o, o]  # is good !
            obsmeteo.Observations(*[o, 33])  # is wrong !!


# -- class TestObservationsConcat ---------------------------------------------
class TestObservationsConcat(unittest.TestCase):

    """Observations.concat function tests."""

    def test_base_01(self):
        """Concat base test."""
        obs1 = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00+00:00', 33, qua=22),
            obsmeteo.Observation('2012-10-03 07:00+00:00', 37, qua=22),
            obsmeteo.Observation('2012-10-03 08:00+00:00', 42, qua=22)
        )
        obs2 = obsmeteo.Observations(
            obsmeteo.Observation('2014-10-03 09:00+00:00', 330, qua=22),
            obsmeteo.Observation('2014-10-03 10:00+00:00', 370, qua=22),
            obsmeteo.Observation('2014-10-03 11:00+00:00', 420, qua=22)
        )
        expected = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00+00:00', 33, qua=22),
            obsmeteo.Observation('2012-10-03 07:00+00:00', 37, qua=22),
            obsmeteo.Observation('2012-10-03 08:00+00:00', 42, qua=22),
            obsmeteo.Observation('2014-10-03 09:00+00:00', 330, qua=22),
            obsmeteo.Observation('2014-10-03 10:00+00:00', 370, qua=22),
            obsmeteo.Observation('2014-10-03 11:00+00:00', 420, qua=22)
        )
        concat = obsmeteo.Observations.concat(obs1, obs2)
        self.assertTrue(numpy.array_equal(concat, expected))

    def test_error_01(self):
        """Concat error test."""
        obs1 = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00', 33),
            obsmeteo.Observation('2012-10-03 07:00', 37),
            obsmeteo.Observation('2012-10-03 08:00', 42)
        )
        with self.assertRaises(TypeError):
            obsmeteo.Observations.concat(*(obs1, '33'))


# -- class TestSerie ----------------------------------------------------------
class TestSerie(unittest.TestCase):

    """Serie class tests."""

    def test_base_01(self):
        """Base case test."""
        g = sitemeteo.Grandeur('RR')
        d = datetime.timedelta(days=1)
        t = 4
        o = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00', 33),
            obsmeteo.Observation('2012-10-03 07:00', 37),
            obsmeteo.Observation('2012-10-03 08:00', 42)
        )
        dtdeb = '2012-10-03 05:00+00'
        dtfin = '2012-10-03 09:00+00'
        dtprod = '2012-10-03 10:00+00'
        c = intervenant.Contact(999)
        i = True
        serie = obsmeteo.Serie(
            grandeur=g, duree=d, statut=t, observations=o, strict=i,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod, contact=c
        )
        self.assertEqual(
            (
                serie.grandeur, serie.duree, serie.statut,
                serie.observations, serie._strict, serie.contact
            ),
            (g, d, t, o, i, c)
        )
        self.assertEqual(
            (serie.dtdeb, serie.dtfin, serie.dtprod),
            (
                datetime.datetime(2012, 10, 3, 5),
                datetime.datetime(2012, 10, 3, 9),
                datetime.datetime(2012, 10, 3, 10)
            )
        )

    def test_base_02(self):
        """Minimum serie."""
        g = sitemeteo.Grandeur('EP')
        o = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00', 33),
        )
        serie = obsmeteo.Serie(
            grandeur=g, observations=o,
        )
        self.assertEqual(
            (
                serie.grandeur, serie.duree, serie.statut, serie._strict,
                serie.dtdeb, serie.dtfin, serie.dtprod, serie.observations,
                serie.contact
            ),
            (g, datetime.timedelta(0), 0, True, None, None, None, o, None)
        )

    def test_resample(self):
        """Resample method test."""
        g = sitemeteo.Grandeur('RR')
        o = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00', 6),
            obsmeteo.Observation('2012-10-03 07:00', 7),
            obsmeteo.Observation('2012-10-03 09:00', 9)
        )
        serie = obsmeteo.Serie(
            grandeur=g,
            observations=o,
            duree=datetime.timedelta(hours=1)
        )
        self.assertEqual(len(serie.observations), 3)
        serie.resample(serie.duree)
        self.assertEqual(len(serie.observations), 4)
        self.assertTrue(
            numpy.isnan(serie.observations.iloc[2]['res'])
        )
        with self.assertRaises(ValueError):
            serie.resample('1H')

    def test_equal_01(self):
        """Test __eq__ method."""
        # avec qualite
        grd1 = sitemeteo.Grandeur('EP')
        obs1 = obsmeteo.Observation('2012-10-03 06:00', 33, qua=100)
        obss1 = obsmeteo.Observations(obs1, )
        serie1 = obsmeteo.Serie(grandeur=grd1, observations=obss1)

        grd2 = sitemeteo.Grandeur('EP')
        obs2 = obsmeteo.Observation('2012-10-03 06:00', 33, qua=100)
        obss2 = obsmeteo.Observations(obs2, )
        serie2 = obsmeteo.Serie(grandeur=grd2, observations=obss2)

        grd3 = sitemeteo.Grandeur('VV')
        obs3 = obsmeteo.Observation('2012-10-03 06:00', 33, qua=50)
        obss3 = obsmeteo.Observations(obs3, )
        serie3 = obsmeteo.Serie(grandeur=grd3, observations=obss3)

        self.assertEqual(grd1, grd2)
        self.assertNotEqual(grd1, grd3)
        self.assertEqual(obs1, obs2)
        self.assertNotEqual(obs1, obs3)
        # print(
        #     "\nWarning, comparison of obsmeteo.Observations requires "
        #     "'(obs == obs).all().all()'\n"
        # )
        # self.assertEqual(obss1, obss2)
        # self.assertNotEqual(obss1, obss3)
        self.assertTrue((obss1 == obss2).all().all())
        self.assertFalse((obss1 == obss3).all().all())
        self.assertEqual(serie1, serie2)
        self.assertNotEqual(serie1, serie3)
        serie2.statut = 4
        self.assertNotEqual(serie1, serie2)
        self.assertTrue(serie1.__eq__(serie2, ignore=['statut']))

        # sans qualite => Nan != Nan
        grd1 = sitemeteo.Grandeur('EP')
        obs1 = obsmeteo.Observation('2012-10-03 06:00', 33)
        obss1 = obsmeteo.Observations(obs1, )
        serie1 = obsmeteo.Serie(grandeur=grd1, observations=obss1)

        grd2 = sitemeteo.Grandeur('EP')
        obs2 = obsmeteo.Observation('2012-10-03 06:00', 33)
        obss2 = obsmeteo.Observations(obs2, )
        serie2 = obsmeteo.Serie(grandeur=grd2, observations=obss2)

        self.assertNotEqual(obs1, obs2)
        self.assertFalse((obss1 == obss2).all().all())
        self.assertNotEqual(serie1, serie2)

    def test_non_equal_01(self):
        """Test __ne__ method."""
        g1 = sitemeteo.Grandeur('EP')
        o1 = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00', 33),
        )
        serie1 = obsmeteo.Serie(
            grandeur=g1, observations=o1,
        )
        g2 = sitemeteo.Grandeur('RR')
        o2 = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00', 33),
        )
        serie2 = obsmeteo.Serie(
            grandeur=g2, observations=o2,
        )
        self.assertNotEqual(serie1, serie2)

    def test_str_01(self):
        """Test __str__ method with minimum values."""
        # None values
        serie = obsmeteo.Serie(strict=False)
        self.assertTrue(serie.__str__().rfind('Serie') > -1)
        self.assertTrue(serie.__str__().rfind('Statut') > -1)
        self.assertTrue(serie.__str__().rfind('Observations') > -1)
        # a junk entite
        serie = obsmeteo.Serie(grandeur='XL', strict=False)
        self.assertTrue(serie.__str__().rfind('grandeur inconnue') > -1)

    def test_str_02(self):
        """Test __str__ method with a small Observations."""
        g = sitemeteo.Grandeur('ER')
        o = obsmeteo.Observations(
            obsmeteo.Observation('2012-10-03 06:00', 33),
            obsmeteo.Observation('2012-10-03 08:00', 42)
        )
        serie = obsmeteo.Serie(grandeur=g, observations=o)
        self.assertTrue(serie.__str__().rfind('Serie') > -1)
        self.assertTrue(serie.__str__().rfind('Statut') > -1)
        self.assertTrue(serie.__str__().rfind('Observations') > -1)

    def test_str_03(self):
        """Test __str__ method with a big Observations."""
        g = sitemeteo.Grandeur('ER')
        o = obsmeteo.Observations(
            *[obsmeteo.Observation('20%i-01-01 00:00' % x, x)
              for x in xrange(10, 50)]
        )
        serie = obsmeteo.Serie(grandeur=g, observations=o)
        self.assertTrue(serie.__str__().rfind('Serie') > -1)
        self.assertTrue(serie.__str__().rfind('Statut') > -1)
        self.assertTrue(serie.__str__().rfind('Observations') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        g = 'XX'
        t = 123
        o = [10, 13, 25, 8]
        serie = obsmeteo.Serie(
            grandeur=g, statut=t, observations=o, strict=False
        )
        self.assertEqual(
            (
                serie.grandeur, serie.duree, serie.statut,
                serie.observations, serie._strict
            ),
            (g, datetime.timedelta(0), t, o, False)
        )
        serie = obsmeteo.Serie(strict=False)
        self.assertEqual(
            (
                serie.grandeur, serie.duree, serie.statut,
                serie.observations, serie._strict
            ),
            (None, datetime.timedelta(0), 0, None, False)
        )

    def test_error_01(self):
        """Grandeur error."""
        g = sitemeteo.Grandeur('RR', strict=False)
        o = obsmeteo.Observations(obsmeteo.Observation('2012-10-03 06:00', 33))
        obsmeteo.Serie(**{'grandeur': g, 'observations': o})
        with self.assertRaises(TypeError):
            obsmeteo.Serie(**{'grandeur': None, 'observations': o})
        obsmeteo.Serie(**{
            'grandeur': 'X', 'observations': o, 'strict': False
        })
        with self.assertRaises(TypeError):
            obsmeteo.Serie(**{'grandeur': 'X', 'observations': o})

    def test_error_02(self):
        """Duree error."""
        g = sitemeteo.Grandeur('RR')
        o = obsmeteo.Observations(obsmeteo.Observation('2012-10-03 06:00', 33))
        obsmeteo.Serie(**{'grandeur': g, 'duree': 10, 'observations': o})
        with self.assertRaises(ValueError):
            obsmeteo.Serie(**{'grandeur': g, 'duree': -1, 'observations': o})
        with self.assertRaises(ValueError):
            obsmeteo.Serie(
                **{'grandeur': g, 'duree': 'hex', 'observations': o}
            )

    def test_error_03(self):
        """Statut error."""
        g = sitemeteo.Grandeur('XX', strict=False)
        o = obsmeteo.Observations(obsmeteo.Observation('2012-10-03 06:00', 33))
        obsmeteo.Serie(
            **{'grandeur': g, 'statut': 8, 'observations': o}
        )
        with self.assertRaises(ValueError):
            obsmeteo.Serie(
                **{'grandeur': g, 'statut': None, 'observations': o}
            )
        with self.assertRaises(ValueError):
            obsmeteo.Serie(**{'grandeur': g, 'statut': 124, 'observations': o})

    def test_error_04(self):
        """Observations error."""
        g = sitemeteo.Grandeur('XX', strict=False)
        obsmeteo.Serie(
            **{
                'grandeur': g, 'observations': 12, 'strict': False
            }
        )
        with self.assertRaises(TypeError):
            obsmeteo.Serie(
                **{'grandeur': g, 'observations': 12, 'strict': True}
            )

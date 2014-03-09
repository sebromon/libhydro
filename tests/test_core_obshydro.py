# -*- coding: utf-8 -*-
"""Test program for obshydro.

To run all tests just type:
    './test_core_obshydro.py' or 'python test_core_obshydro.py'

To run only a class test:
    python -m unittest test_core_obshydro.TestClass

To run only a specific test:
    python -m unittest test_core_obshydro.TestClass
    python -m unittest test_core_obshydro.TestClass.test_method

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
import numpy

from libhydro.core import (sitehydro, obshydro)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin""" \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1f"""
__date__ = """2014-03-09"""

#HISTORY
#V0.1 - 2013-07-15
#    first shot


#-- class TestObservation -----------------------------------------------------
class TestObservation(unittest.TestCase):

    """Observation class tests."""

    def test_base_01(self):
        """Base case test."""
        dte = '2000-01-01 10:33:01+0000'
        res = 20.5
        mth = 4
        qal = 8
        cnt = False
        obs = obshydro.Observation(dte, res, mth, qal, cnt)
        self.assertEqual(
            obs.item(),
            (datetime.datetime(2000, 1, 1, 10, 33, 1), res, mth, qal, cnt)
        )

    def test_base_02(self):
        """Some instanciation use cases."""
        obshydro.Observation('2000-01-01 10:33:01', 20)
        obshydro.Observation('2000-01-01 10:33', 0, 4)
        obshydro.Observation('2000-01-01 00:00+0100', 10, 4, 8, True)
        obshydro.Observation(
            datetime.datetime(2000, 1, 1, 10), 10, mth=4, qal=8
        )
        obshydro.Observation(datetime.datetime(2000, 1, 1), '20', cnt=True)
        self.assertTrue(True)  # avoid pylint warning !

    def test_str_01(self):
        """Test __str__ method."""
        dte = '2000-01-01 10:33:01+0000'
        res = 20.5
        mth = 4
        qal = 8
        cnt = False
        obs = obshydro.Observation(dte, res, mth, qal, cnt)
        self.assertTrue(obs.__str__().rfind('UTC') > -1)
        self.assertTrue(obs.__str__().rfind('continue') > -1)

    def test_error_01(self):
        """Date error."""
        obshydro.Observation(**{'dte': '2000-10-10 10:00', 'res': 10})
        self.assertRaises(
            TypeError,
            obshydro.Observation,
            **{'dte': '2000-10', 'res': 10}
        )

    def test_error_02(self):
        """Test Res error."""
        obshydro.Observation(**{'dte': '2000-10-05 10:00', 'res': 10})
        self.assertRaises(
            ValueError,
            obshydro.Observation,
            **{'dte': '2000-10-05 10:00', 'res': 'aaa'}
        )

    def test_error_03(self):
        """Mth error."""
        obshydro.Observation(
            **{'dte': '2000-10-05 10:00', 'res': 20, 'mth': 4}
        )
        self.assertRaises(
            ValueError,
            obshydro.Observation,
            **{'dte': '2000-10-05 10:00', 'res': 20, 'mth': 1000}
        )

    def test_error_04(self):
        """Qal error."""
        obshydro.Observation(
            **{'dte': '2000-10-05 10:00', 'res': 20, 'qal': 16}
        )
        self.assertRaises(
            ValueError,
            obshydro.Observation,
            **{'dte': '2000-10-05 10:00', 'res': 20, 'qal': 1000}
        )


#-- class TestObservations ----------------------------------------------------
class TestObservations(unittest.TestCase):

    """Observations class tests."""

    def test_base_01(self):
        """Simple test."""
        # The simpliest __init_: datetime and res
        obs = obshydro.Observations(
            obshydro.Observation('2012-10-03 06:00', 33),
            obshydro.Observation('2012-10-03 07:00', 37),
            obshydro.Observation('2012-10-03 08:00', 42)
        )
        self.assertEqual(
            obs['res'].tolist(),
            [33, 37, 42]
        )

    def test_base_02(self):
        """Base case test."""
        # Datetime, res and others attributes
        obs = obshydro.Observations(
            obshydro.Observation(
                '2012-10-03 06:00', 33, mth=4, qal=0, cnt=True),
            obshydro.Observation(
                '2012-10-03 07:00', 37, mth=0, qal=12, cnt=False),
            obshydro.Observation(
                '2012-10-03 08:00', 42, mth=12, qal=20, cnt=True)
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
            obs['cnt'].tolist(),
            [True, False, True]
        )

    def test_error_01(self):
        """List of observation error."""
        # check that init works when call regurlaly...
        o = obshydro.Observation(
            '2012-10-03 06:00', 33, mth=4, qal=0, cnt=True
        )
        obshydro.Observations(*[o, o])
        # ...and fails otherwise
        self.assertRaises(
            TypeError,
            obshydro.Observations,
            # *[o, o]  # is good !
            *[o, 33]  # is wrong !!
        )


#-- class TestObservationsConcat ----------------------------------------------
class TestObservationsConcat(unittest.TestCase):

    """Observations.concat function tests."""

    def test_base_01(self):
        """Concat base test."""
        obs1 = obshydro.Observations(
            obshydro.Observation('2012-10-03 06:00', 33),
            obshydro.Observation('2012-10-03 07:00', 37),
            obshydro.Observation('2012-10-03 08:00', 42)
        )
        obs2 = obshydro.Observations(
            obshydro.Observation('2014-10-03 06:00', 330),
            obshydro.Observation('2014-10-03 07:00', 370),
            obshydro.Observation('2014-10-03 08:00', 420)
        )
        expected = obshydro.Observations(
            obshydro.Observation('2012-10-03 06:00', 33),
            obshydro.Observation('2012-10-03 07:00', 37),
            obshydro.Observation('2012-10-03 08:00', 42),
            obshydro.Observation('2014-10-03 06:00', 330),
            obshydro.Observation('2014-10-03 07:00', 370),
            obshydro.Observation('2014-10-03 08:00', 420)
        )
        concat = obshydro.Observations.concat(obs1, obs2)
        self.assertTrue(numpy.array_equal(concat, expected))

    def test_error_01(self):
        """Concat error test."""
        obs1 = obshydro.Observations(
            obshydro.Observation('2012-10-03 06:00', 33),
            obshydro.Observation('2012-10-03 07:00', 37),
            obshydro.Observation('2012-10-03 08:00', 42)
        )
        self.assertRaises(
            TypeError,
            obshydro.Observations.concat,
            *(obs1, '33')
        )


#-- class TestSerie -----------------------------------------------------------
class TestSerie(unittest.TestCase):

    """Serie class tests."""

    def test_base_01(self):
        """Serie on a site."""
        s = sitehydro.Sitehydro(
            code='A0445810', libelle='Le Rhône à Marseille'
        )
        g = 'Q'
        t = 16
        o = obshydro.Observations(
            obshydro.Observation('2012-10-03 06:00', 33),
            obshydro.Observation('2012-10-03 07:00', 37),
            obshydro.Observation('2012-10-03 08:00', 42)
        )
        dtdeb = '2012-10-03 05:00+00'
        dtfin = '2012-10-03 09:00+00'
        dtprod = '2012-10-03 10:00+00'
        i = True
        serie = obshydro.Serie(
            entite=s, grandeur=g, statut=t, observations=o, strict=i,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod
        )
        self.assertEqual(
            (
                serie.entite, serie.grandeur, serie.statut,
                serie.observations, serie._strict
            ),
            (s, g, t, o, i)
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
        """Serie on a station with no statut."""
        s = sitehydro.Stationhydro(code='A044581001')
        g = 'Q'
        o = obshydro.Observations(
            obshydro.Observation('2012-10-03 06:00', 33),
            obshydro.Observation('2012-10-03 08:00', 42)
        )
        dtdeb = datetime.datetime(2012, 10, 3, 5)
        dtfin = datetime.datetime(2012, 10, 3, 9)
        dtprod = datetime.datetime(2012, 10, 3, 10)
        serie = obshydro.Serie(
            entite=s, grandeur=g, observations=o,
            dtdeb=dtdeb, dtfin=dtfin, dtprod=dtprod
        )
        self.assertEqual(
            (
                serie.entite, serie.grandeur, serie.statut,
                serie.observations, serie._strict
            ),
            (s, g, 0, o, True)
        )
        self.assertEqual(
            (serie.dtdeb, serie.dtfin, serie.dtprod),
            (
                datetime.datetime(2012, 10, 3, 5),
                datetime.datetime(2012, 10, 3, 9),
                datetime.datetime(2012, 10, 3, 10)
            )
        )

    def test_str_01(self):
        """Test __str__ method with minimum values."""
        # None values
        serie = obshydro.Serie(strict=False)
        self.assertTrue(serie.__str__().rfind('Serie') > -1)
        self.assertTrue(serie.__str__().rfind('Statut') > -1)
        self.assertTrue(serie.__str__().rfind('Observations') > -1)
        # a junk entite
        serie = obshydro.Serie(entite='station 33', strict=False)
        self.assertTrue(serie.__str__().rfind('station 33') > -1)

    def test_str_02(self):
        """Test __str__ method with a small Observations."""
        s = sitehydro.Stationhydro(code='A044581001')
        o = obshydro.Observations(
            obshydro.Observation('2012-10-03 06:00', 33),
            obshydro.Observation('2012-10-03 08:00', 42)
        )
        serie = obshydro.Serie(entite=s, grandeur='Q', observations=o)
        self.assertTrue(serie.__str__().rfind('Serie') > -1)
        self.assertTrue(serie.__str__().rfind('Statut') > -1)
        self.assertTrue(serie.__str__().rfind('Observations') > -1)

    def test_str_03(self):
        """Test __str__ method with a big Observations."""
        s = sitehydro.Stationhydro(code='A044581001', libelle='Toulouse')
        o = obshydro.Observations(
            *[obshydro.Observation('20%i-01-01 00:00' % x, x)
              for x in xrange(10, 50)]
        )
        serie = obshydro.Serie(entite=s, grandeur='H', observations=o)
        self.assertTrue(serie.__str__().rfind('Serie') > -1)
        self.assertTrue(serie.__str__().rfind('Statut') > -1)
        self.assertTrue(serie.__str__().rfind('Observations') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        s = 4
        g = 'RR'
        t = 123
        o = [10, 13, 25, 8]
        serie = obshydro.Serie(
            entite=s, grandeur=g, statut=t, observations=o, strict=False
        )
        self.assertEqual(
            (
                serie.entite, serie.grandeur, serie.statut,
                serie.observations, serie._strict
            ),
            (s, g, t, o, False)
        )
        serie = obshydro.Serie(strict=False)
        self.assertEqual(
            (
                serie.entite, serie.grandeur, serie.statut,
                serie.observations, serie._strict
            ),
            (None, None, 0, None, False)
        )

    def test_error_01(self):
        """Entite error."""
        s = sitehydro.Stationhydro(code='A044581001', strict=False)
        o = obshydro.Observations(obshydro.Observation('2012-10-03 06:00', 33))
        obshydro.Serie(**{'entite': s, 'grandeur': 'H', 'observations': o})
        self.assertRaises(
            TypeError,
            obshydro.Serie,
            **{'entite': 'X', 'grandeur': 'H', 'observations': o}
        )

    def test_error_02(self):
        """Grandeur error."""
        s = sitehydro.Stationhydro(code='A044581001', strict=False)
        o = obshydro.Observations(obshydro.Observation('2012-10-03 06:00', 33))
        obshydro.Serie(**{'entite': s, 'grandeur': 'H', 'observations': o})
        self.assertRaises(
            ValueError,
            obshydro.Serie,
            **{'entite': s, 'grandeur': None, 'observations': o}
        )
        self.assertRaises(
            ValueError,
            obshydro.Serie,
            **{'entite': s, 'grandeur': 'X', 'observations': o}
        )

    def test_error_03(self):
        """Statut error."""
        s = sitehydro.Stationhydro(code='A044581001', strict=False)
        o = obshydro.Observations(obshydro.Observation('2012-10-03 06:00', 33))
        obshydro.Serie(
            **{'entite': s, 'grandeur': 'H', 'statut': 12, 'observations': o}
        )
        self.assertRaises(
            ValueError,
            obshydro.Serie,
            **{'entite': s, 'grandeur': 'H', 'statut': None, 'observations': o}
        )
        self.assertRaises(
            ValueError,
            obshydro.Serie,
            **{'entite': s, 'grandeur': 'H', 'statut': 124, 'observations': o}
        )

    def test_error_04(self):
        """Test Observations error."""
        s = sitehydro.Stationhydro(code='A044581001', strict=False)
        obshydro.Serie(
            **{
                'entite': s, 'grandeur': 'H', 'observations': 12,
                'strict': False
            }
        )
        self.assertRaises(
            TypeError,
            obshydro.Serie,
            **{
                'entite': s, 'grandeur': 'H', 'observations': 12,
                'strict': True
            }
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

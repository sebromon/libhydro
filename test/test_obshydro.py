#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function
"""Test program for obshydro.

To run all tests just type:
    './test_obshydro.py' or 'python test_obshydro.py'

To run only a class test:
    python -m unittest test_obshydro.TestClass

To run only a specific test:
    python -m unittest test_obshydro.TestClass
    python -m unittest test_obshydro.TestClass.test_method

"""

#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """Version 0.1a"""
__date__ = """2013-07-26"""

#HISTORY
#V0.1 - 2013-07-15
#    first shot

#-- todos ---------------------------------------------------------------------
# TODO - nothing
# FIXME - nothing

#-- imports -------------------------------------------------------------------
import unittest
import os
import sys
import datetime

sys.path.extend([os.path.join('..', '..'), os.path.join('..', 'core')])

import obshydro


#-- config --------------------------------------------------------------------

#-- class TestObservation -----------------------------------------------------
class TestObservation(unittest.TestCase):
    """Observation class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base(self):
        """Base case tests."""
        # test 01
        obs = obshydro.Observation('2000-01-01 10:33:01+0000', 20.5, 4, 8, False)
        self.assertEqual(
            obs['dte'].item(),
            datetime.datetime(2000, 1, 1, 10, 33, 1),
            'erreur %s, wrong dte' % (self.__class__.__name__)
        )
        self.assertEqual(
            obs['res'].item(),
            20.5,
            'erreur %s, wrong res' % (self.__class__.__name__)
        )
        self.assertEqual(
            obs['mth'].item(),
            4,
            'erreur %s, wrong mth' % (self.__class__.__name__)
        )
        self.assertEqual(
            obs['qal'].item(),
            8,
            'erreur %s, wrong qal' % (self.__class__.__name__)
        )
        self.assertEqual(
            obs['cnt'].item(),
            False,
            'erreur %s, wrong cnt' % (self.__class__.__name__)
        )

        # test 02
        obs = obshydro.Observation('2000-01-01 10:33:01', 20)
        obs = obshydro.Observation('2000-01-01 10:33', 0, 4)
        obs = obshydro.Observation('2000-01-01 00:00+0100', 10, 4, 8, True)
        obs = obshydro.Observation(datetime.datetime(2000, 1, 1, 10), 10, mth=4, qal=8)
        obs = obshydro.Observation(datetime.datetime(2000, 1, 1), '20', cnt=True)

    def test_errors(self):
        """Errors tests."""

        # test 01
        self.assertRaises(
            TypeError,
            obshydro.Observation,
            # *('2000-10-10 10:00', 10)
            *('2000', 10)
        )

        # test 02
        self.assertRaises(
            ValueError,
            obshydro.Observation,
            # *('2000-10-05 10:00', 10)
            *('2000-10-05 10:00', 'aaa')
        )

        # test 03
        self.assertRaises(
            ValueError,
            obshydro.Observation,
            *('2000-10-05 10:00', 20),
            # **{'mth': 4}
            **{'mth': 1000}
        )

        # test 04
        self.assertRaises(
            ValueError,
            obshydro.Observation,
            *('2000-10-05 10:00', 20),
            # **{'qal': 16}
            **{'qal': 1000}
        )


#-- class TestObservations ----------------------------------------------------
class TestObservations(unittest.TestCase):
    """Observations class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

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
            obshydro.Observation('2012-10-03 06:00', 33, mth=4, qal=0, cnt=True),
            obshydro.Observation('2012-10-03 07:00', 37, mth=0, qal=12, cnt=False),
            obshydro.Observation('2012-10-03 08:00', 42, mth=12, qal=20, cnt=True)
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
        o = obshydro.Observation('2012-10-03 06:00', 33, mth=4, qal=0, cnt=True)
        obshydro.Observations(*[o, o])
        # ...and fails otherwise
        self.assertRaises(
            TypeError,
            obshydro.Observations,
            # *[o, o]  # is good !
            *[o, 33]  # is wrong !!
        )


#-- class TestSerie -----------------------------------------------------------
class TestSerie(unittest.TestCase):
    """Serie class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base_01(self):
        """Serie on a site."""
        s = obshydro.sitehydro.Sitehydro(code='A0445810', libelle='Le Rhône à Marseille')
        g = 'Q'
        t = 16
        o = obshydro.Observations(
            obshydro.Observation('2012-10-03 06:00', 33),
            obshydro.Observation('2012-10-03 07:00', 37),
            obshydro.Observation('2012-10-03 08:00', 42)
        )
        i = True
        serie = obshydro.Serie(
            entite=s, grandeur=g, statut=t, observations=o, strict=i
        )
        self.assertEqual(
            (
                serie.entite, serie.grandeur, serie.statut,
                serie.observations, serie._strict
            ),
            (s, g, t, o, i)
        )

    def test_base_02(self):
        """Serie on a station with no statut."""
        s = obshydro.sitehydro.Stationhydro(code='A044581001')
        o = obshydro.Observations(
            obshydro.Observation('2012-10-03 06:00', 33),
            obshydro.Observation('2012-10-03 08:00', 42)
        )
        serie = obshydro.Serie(entite=s, observations=o)
        self.assertEqual(
            (
                serie.entite, serie.grandeur, serie.statut,
                serie.observations, serie._strict
            ),
            (s, None, 0, o, True)
        )

    def test_base_03(self):
        """Serie should accept bad observations in strict mode."""
        s = obshydro.sitehydro.Stationhydro()
        o = 44  # no control on observations
        serie = obshydro.Serie(entite=s, observations=o)
        self.assertEqual(
            (
                serie.entite, serie.grandeur, serie.statut,
                serie.observations, serie._strict
            ),
            (s, None, 0, o, True)
        )

    def test_lazy_mode_01(self):
        """Base case test."""
        s = 4
        g = 'RR'
        t = 123
        o = [10, 13, 25, 8]
        i = False
        serie = obshydro.Serie(
            entite=s, grandeur=g, statut=t, observations=o, strict=i
        )
        self.assertEqual(
            (
                serie.entite, serie.grandeur, serie.statut,
                serie.observations, serie._strict
            ),
            (s, g, 0, o, i)
        )

    def test_error_01(self):
        """Entite error."""
        # s = obshydro.sitehydro.Stationhydro(code='A044581001')
        self.assertRaises(
            TypeError,
            obshydro.Serie,
            # **{'entite': s}  # good !
            **{'entite': 'X'}  # bad !!
        )

    def test_error_02(self):
        """Grandeur error."""
        self.assertRaises(
            ValueError,
            obshydro.Serie,
            # **{'grandeur': 'H'}  # good !
            **{'grandeur': 'X'}  # bad !!
        )

    def test_error_03(self):
        """Statut error."""
        self.assertRaises(
            ValueError,
            obshydro.Serie,
            # **{'statut': 12}  # good !
            **{'statut': 124}  # bad !!
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function
"""Test program for sitehydro.

To run all tests just type:
    './test_sitehydro.py' or 'python test_sitehydro.py'

To run only a class test:
    python -m unittest test_sitehydro.TestClass

To run only a specific test:
    python -m unittest test_sitehydro.TestClass
    python -m unittest test_sitehydro.TestClass.test_method

"""

#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """Version 0.1a"""
__date__ = """2013-07-15"""

#HISTORY
#V0.1 - 2013-07-15
#    first shot

#-- todos ---------------------------------------------------------------------
# TODO - nothing
# FIXME - nothing

#-- imports -------------------------------------------------------------------
import unittest

import sys
sys.path.extend(['..', './core', '../..', '../core'])
from sitehydro import Sitehydro, Stationhydro


#-- config --------------------------------------------------------------------

#-- class ---------------------------------------------------------------------
class TestSiteHydro(unittest.TestCase):
    """"""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base(self):
        """."""
        # test 01
        typesite = code = libelle = None
        stations = []
        s = Sitehydro()
        self.assertEqual(
            (s.typesite, s.code, s.libelle, s.stations),
            (typesite, code, libelle, stations),
            'erreur %s' % (self.__class__.__name__)
        )

        # test 02 - 1 station
        typesite = 'REEL'
        code = 'A3334550'
        libelle = 'La Saône [après la crue] à Montélimar [hé oui]'
        stations = Stationhydro()
        s = Sitehydro(
            typesite=typesite, code=code, libelle=libelle, stations=stations
        )
        self.assertEqual(
            (s.typesite, s.code, s.libelle, s.stations),
            (typesite, code, libelle, [stations]),
            'erreur %s' % (self.__class__.__name__)
        )

        # test 03 - n stations
        typesite = 'REEL'
        code = 'A3334550'
        libelle = 'La Saône [après la crue] à Montélimar [hé oui]'
        stations = (Stationhydro(), Stationhydro())
        s = Sitehydro(
            typesite=typesite, code=code, libelle=libelle, stations=stations
        )
        self.assertEqual(
            (s.typesite, s.code, s.libelle, s.stations),
            (typesite, code, libelle, [s for s in stations]),
            'erreur %s' % (self.__class__.__name__)
        )

    def test_errors(self):
        """Errors tests."""
        self.assertRaises(
            ValueError,
            Sitehydro,
            {'typesite': 'REEEL'}
        )
        self.assertRaises(
            ValueError,
            Sitehydro,
            {'code': 'B4400000'}
        )
        self.assertRaises(
            ValueError,
            Sitehydro,
            {'libelle': [3, 2]}
        )
        self.assertRaises(
            ValueError,
            Sitehydro,
            {'stations': ['station']}
        )


class TestStationHydro(unittest.TestCase):
    """"""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base(self):
        """Base case tests."""
        # test 01
        typestation = code = libelle = None
        s = Stationhydro()
        self.assertEqual(
            (s.typestation, s.code, s.libelle),
            (typestation, code, libelle),
            'erreur %s' % (self.__class__.__name__)
        )

        # test 02
        typestation = 'LIMNI'
        code = 'A033465001'
        libelle = 'La Seine à Paris - rive droite'
        s = Stationhydro(typestation=typestation, code=code, libelle=libelle)
        self.assertEqual(
            (s.typestation, s.code, s.libelle),
            (typestation, code, libelle),
            'erreur %s' % (self.__class__.__name__)
        )

    def test_errors(self):
        """Errors tests."""
        self.assertRaises(
            ValueError,
            Stationhydro,
            {'typestation': 'LIMMMMNI'}
        )
        self.assertRaises(
            ValueError,
            Stationhydro,
            {'code': 'B440000'}
        )
        self.assertRaises(
            ValueError,
            Stationhydro,
            {'libelle': [3, 2]}
        )

#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

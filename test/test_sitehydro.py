# -*- coding: utf-8 -*-
"""Test program for sitehydro.

To run all tests just type:
    './test_sitehydro.py' or 'python test_sitehydro.py'

To run only a class test:
    python -m unittest test_sitehydro.TestClass

To run only a specific test:
    python -m unittest test_sitehydro.TestClass
    python -m unittest test_sitehydro.TestClass.test_method

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

from libhydro.core.sitehydro import Sitehydro, Stationhydro, Capteur


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """Version 0.1d"""
__date__ = """2013-08-07"""

#HISTORY
#V0.1 - 2013-07-15
#    first shot


#-- todos ---------------------------------------------------------------------


#-- config --------------------------------------------------------------------


#-- class TestSiteHydro -------------------------------------------------------
class TestSiteHydro(unittest.TestCase):
    """Sitehydro class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base_01(self):
        """Empty site."""
        typesite = code = libelle = None
        stations = []
        s = Sitehydro()
        self.assertEqual(
            (s.typesite, s.code, s.libelle, s.stations),
            (typesite, code, libelle, stations)
        )

    def test_base_02(self):
        """Site with 1 station."""
        typesite = 'REEL'
        code = 'A3334550'
        libelle = 'La Saône [apres la crue] a Montelimar [he oui]'
        stations = Stationhydro()
        s = Sitehydro(
            typesite=typesite, code=code, libelle=libelle, stations=stations
        )
        self.assertEqual(
            (s.typesite, s.code, s.libelle, s.stations),
            (typesite, code, libelle, [stations])
        )

    def test_base_03(self):
        """Site with n station."""
        typesite = 'REEL'
        code = 'A3334550'
        libelle = 'La Saône [apres la crue] a Montelimar [hé oui]'
        stations = (Stationhydro(), Stationhydro())
        s = Sitehydro(
            typesite=typesite, code=code, libelle=libelle, stations=stations
        )
        self.assertEqual(
            (s.typesite, s.code, s.libelle, s.stations),
            (typesite, code, libelle, [s for s in stations])
        )

    def test_dim_mode_01(self):
        """Dim mode test."""
        typesite = '6'
        code = '3'
        stations = [1, 2, 3]
        s = Sitehydro(
            typesite=typesite, code=code,  stations=stations, strict=False
        )
        self.assertEqual(
            (s.typesite, s.code, s.stations),
            (typesite, code, stations)
        )

    def test_error_01(self):
        """Typesite error."""
        Sitehydro(**{'typesite': 'REEL'})
        self.assertRaises(
            ValueError,
            Sitehydro,
            **{'typesite': 'REEEL'}
        )

    def test_error_02(self):
        """Code error."""
        Sitehydro(**{'code': 'B4401122'})
        self.assertRaises(
            ValueError,
            Sitehydro,
            **{'code': 'B440112201'}
        )
        Sitehydro(**{'code': 'B4401122'})
        self.assertRaises(
            ValueError,
            Sitehydro,
            **{'code': 'B44011'}
        )

    def test_error_03(self):
        """Stations error."""
        stations = (Stationhydro(), Stationhydro())
        Sitehydro(**{'stations': stations})
        self.assertRaises(
            TypeError,
            Sitehydro,
            **{'stations': ['station']}
        )


#-- class TestStationHydro ----------------------------------------------------
class TestStationHydro(unittest.TestCase):
    """Stationhydro class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base_01(self):
        """Base case with empty station."""
        typestation = code = libelle = None
        s = Stationhydro()
        self.assertEqual(
            (s.typestation, s.code, s.libelle),
            (typestation, code, libelle)
        )

    def test_base_02(self):
        """Base case test."""
        typestation = 'LIMNI'
        code = 'A033465001'
        libelle = 'La Seine a Paris - rive droite'
        s = Stationhydro(typestation=typestation, code=code, libelle=libelle)
        self.assertEqual(
            (s.typestation, s.code, s.libelle),
            (typestation, code, libelle)
        )

    def test_dim_mode_01(self):
        """Dim mode test."""
        typestation = '6'
        code = '3'
        s = Stationhydro(typestation=typestation, code=code, strict=False)
        self.assertEqual(
            (s.typestation, s.code),
            (typestation, code)
        )

    def test_error_01(self):
        """Typestation error."""
        Stationhydro(**{'typestation': 'LIMNI'})
        self.assertRaises(
            ValueError,
            Stationhydro,
            **{'typestation': 'LIMMMMNI'}
        )

    def test_error_02(self):
        """Code error."""
        Stationhydro(**{'code': 'B440112201'})
        self.assertRaises(
            ValueError,
            Stationhydro,
            **{'code': 'B4401122'}
        )
        self.assertRaises(
            ValueError,
            Stationhydro,
            **{'code': 'B44011220101'}
        )


#-- class TestCapteur ----------------------------------------------------
class TestCapteur(unittest.TestCase):
    """Capteur class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base_01(self):
        """Base case with empty capteur."""
        typemesure = code = libelle = None
        c = Capteur()
        self.assertEqual(
            (c.typemesure, c.code, c.libelle),
            (typemesure, code, libelle)
        )

    def test_base_02(self):
        """Base case test."""
        typemesure = 'H'
        code = 'A03346500101'
        libelle = 'Capteur de secours'
        c = Capteur(typemesure=typemesure, code=code, libelle=libelle)
        self.assertEqual(
            (c.typemesure, c.code, c.libelle),
            (typemesure, code, libelle)
        )

    def test_dim_mode_01(self):
        """Dim mode test."""
        typemesure = 'RR'
        code = 'C1'
        c = Capteur(typemesure=typemesure, code=code, strict=False)
        self.assertEqual(
            (c.typemesure, c.code),
            (typemesure, code)
        )

    def test_error_01(self):
        """Typemesure error."""
        Capteur(**{'typemesure': 'H'})
        self.assertRaises(
            ValueError,
            Capteur,
            **{'typemesure': 'RR'}
        )

    def test_error_02(self):
        """Code error."""
        Capteur(**{'code': 'B44011220101'})
        self.assertRaises(
            ValueError,
            Capteur,
            **{'code': 'B440112201'}
        )
        self.assertRaises(
            ValueError,
            Capteur,
            **{'code': 'B4401122010133'}
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

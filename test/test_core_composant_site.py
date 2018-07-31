# coding: utf-8
"""Test program for composant_site.

To run all tests just type:
    python -m unittest test_core_composant_site

To run only a class test:
    python -m unittest test_core_composant_site.TestClass

To run only a specific test:
    python -m unittest test_core_composant_site.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import unittest

from libhydro.core import _composant_site as composant_site


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.3b"""
__date__ = """2014-07-18"""

# HISTORY
# V0.3 - 2014-07-16
#   remove the composant part
# V0.2 - 2014-03-01
#   add the descriptor tests
# V0.1 - 2013-11-07
#   first shot


# -- class TestCoord ----------------------------------------------------------
class TestCoord(unittest.TestCase):

    """Coord class tests."""

    # def setUp(self):
    # """Hook method for setting up the test fixture before exercising it."""
    # pass

    # def tearDown(self):
    # """Hook method for deconstructing the test fixture after testing it."""
    # pass

    def test_base_01(self):
        """Base test."""
        x = 5.9
        y = 10
        p = 22
        c = composant_site.Coord(x, y, p)
        self.assertEqual(
            (c.x, c.y, c.proj),
            (float(x), float(y), p)
        )

    def test_base_02(self):
        """Base test with strongs."""
        x = '5'
        y = '11.3'
        p = 3
        c = composant_site.Coord(x, y, p)
        self.assertEqual(
            (c.x, c.y, c.proj),
            (float(x), float(y), p)
        )

    def test_equal_01(self):
        """Test __equal__ method."""
        self.assertEqual(
            composant_site.Coord(5, 10, 26),
            composant_site.Coord(5, 10, 26),
        )
        self.assertNotEqual(
            composant_site.Coord(5, 10, 26),
            composant_site.Coord(6, 10, 26),
        )

    def test_str_01(self):
        """Test __str__ method."""
        x = 5.9
        y = 10
        p = 22
        c = composant_site.Coord(x, y, p)
        self.assertTrue(c.__str__().rfind(str(x)) > -1)
        self.assertTrue(c.__str__().rfind(str(y)) > -1)
        self.assertTrue(c.__str__().rfind('proj') > -1)
        c = composant_site.Coord(x, y, strict=False)
        self.assertTrue(c.__str__().rfind('proj') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        x = 5.9
        y = 10
        p = None
        c = composant_site.Coord(x, y, p, strict=False)
        self.assertEqual(
            (c.x, c.y, c.proj),
            (float(x), float(y), p)
        )

    def test_error_01(self):
        """X error."""
        composant_site.Coord(**{'x': 1, 'y': 2.3, 'proj': 22})
        self.assertRaises(
            TypeError,
            composant_site.Coord,
            **{'x': 'a', 'y': 2.3, 'proj': 22}
        )

    def test_error_02(self):
        """Y error."""
        composant_site.Coord(**{'x': 1, 'y': 2.3, 'proj': 22})
        self.assertRaises(
            TypeError,
            composant_site.Coord,
            **{'x': '1', 'y': None, 'proj': 22}
        )

    def test_error_03(self):
        """Proj error."""
        composant_site.Coord(**{'x': 1, 'y': 2.3, 'proj': 22})
        self.assertRaises(
            ValueError,
            composant_site.Coord,
            **{'x': '1', 'y': 8156941.2368, 'proj': None}
        )
        self.assertRaises(
            ValueError,
            composant_site.Coord,
            **{'x': '1', 'y': 8156941.2368, 'proj': 8591674}
        )


# -- class TestAltitude -------------------------------------------------------
class TestAltitude(unittest.TestCase):

    """Altitude class tests."""

    # def setUp(self):
    # """Hook method for setting up the test fixture before exercising it."""
    # pass

    # def tearDown(self):
    # """Hook method for deconstructing the test fixture after testing it."""
    # pass

    def test_base_01(self):
        """Base test."""
        altitude = 158.4
        sysalti = 1
        alt = composant_site.Altitude(altitude=altitude,
                                      sysalti=sysalti)
        self.assertEqual(
            (alt.altitude, alt.sysalti),
            (altitude, sysalti)
        )

    def test_altitude(self):
        """Altitude test"""
        altitudes = ['15.4', 1, 156.4, -18.4]
        expected = [15.4, 1, 156.4, -18.4]
        sysalti = 5
        for index, altitude in enumerate(altitudes):
            alt = composant_site.Altitude(altitude=altitude,
                                          sysalti=sysalti)
            self.assertEqual(alt.altitude, expected[index])

    def test_sysalti(self):
        """Sysalti test"""
        sysaltis = [0, 1, 31]
        altitude = 147.3
        alt = composant_site.Altitude(altitude=altitude)
        self.assertEqual(alt.sysalti, 31)
        for sysalti in sysaltis:
            alt = composant_site.Altitude(altitude=altitude,
                                          sysalti=sysalti)
            self.assertEqual(alt.sysalti, sysalti)

    def test_error_altitude(self):
        """Altitude error test"""
        altitude = 13.4
        sysalti = 1
        composant_site.Altitude(altitude=altitude,
                                sysalti=sysalti)
        for altitude in [None, 'toto']:
            with self.assertRaises(Exception):
                composant_site.Altitude(altitude=altitude,
                                        sysalti=sysalti)

    def test_error_sysalti(self):
        """Sysalti error test"""
        altitude = 13.4
        sysalti = 1
        composant_site.Altitude(altitude=altitude,
                                sysalti=sysalti)
        for sysalti in [None, -5, 32]:
            with self.assertRaises(Exception):
                composant_site.Altitude(altitude=altitude,
                                        sysalti=sysalti)

    def test_strict(self):
        """Altitude witout altitude and sysalti"""
        strict = False
        composant_site.Altitude(strict=strict)

    def test_str(self):
        """Representation test"""
        sysalti = 1
        altitude = '84.1'
        alt = composant_site.Altitude(altitude=altitude, sysalti=sysalti)
        str_alt = alt.__str__()
        self.assertTrue(str_alt.find('Bourdeloue') > -1)
        self.assertTrue(str_alt.find(altitude) > -1)


# -- class TestLoiStat -------------------------------------------------------
class TestLoiStat(unittest.TestCase):
    """LoiStat class tests."""
    def test_01(self):
        """simple test"""
        contexte = 3
        loi = 2
        loistat = composant_site.LoiStat(contexte=contexte, loi=loi)
        self.assertEqual((loistat.contexte, loistat.loi),
                         (contexte, loi))

    def test_error_contexte(self):
        """contexte error"""
        contexte = 3
        loi = 2
        for contexte in [1, 3]:
            composant_site.LoiStat(contexte=contexte, loi=loi)
        for contexte in [None, -5, 0, 4, 'toto']:
            with self.assertRaises(Exception):
                composant_site.LoiStat(contexte=contexte, loi=loi)

    def test_error_loi(self):
        """loi error"""
        contexte = 3
        loi = 2
        for loi in [0, 3]:
            composant_site.LoiStat(contexte=contexte, loi=loi)
        for loi in [None, -5, 4, 'toto']:
            with self.assertRaises(Exception):
                composant_site.LoiStat(contexte=contexte, loi=loi)

    def test_str(self):
        """Representation test"""
        contexte = 3
        loi = 2
        loistat = composant_site.LoiStat(contexte=contexte, loi=loi)
        self.assertTrue(loistat.__str__().find('Gauss') > -1)
        self.assertTrue(loistat.__str__().find('Etiage') > -1)


# -- class TestEntiteVigiCrues -----------------------------------------------
class TestEntiteVigiCrues(unittest.TestCase):
    """EntiteVigiCrues class tests."""

    def test_01(self):
        """ simple test"""
        code = 'LA215'
        entite = composant_site.EntiteVigiCrues(code=code)
        self.assertEqual((entite.code, entite.nom),
                         (code, None))

    def test_02(self):
        """Full EntiteVigiCrues"""
        code = 'LA215'
        nom = 'entité'
        entite = composant_site.EntiteVigiCrues(code=code, nom=nom)
        self.assertEqual((entite.code, entite.nom),
                         (code, nom))

    def test_str(self):
        """Representation test"""
        code = 'LA215'
        nom = 'entité'
        entite = composant_site.EntiteVigiCrues(code=code, nom=nom)
        self.assertTrue(entite.__str__().find(code) > -1)
        self.assertTrue(entite.__str__().find(nom) > -1)

# -*- coding: utf-8 -*-
"""Test program for composant.

To run all tests just type:
    './test_core_composant.py' or 'python test_core_composant.py'

To run only a class test:
    python -m unittest test_core_composant.TestClass

To run only a specific test:
    python -m unittest test_core_composant.TestClass
    python -m unittest test_core_composant.TestClass.test_method

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

from libhydro.core import _composant as composant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2013-11-07"""

#HISTORY
#V0.1 - 2013-11-07
#    first shot


#-- class TestCoord -----------------------------------------------------------
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
        c = composant.Coord(x, y, p)
        self.assertEqual(
            (c.x, c.y, c.proj),
            (float(x), float(y), p)
        )

    def test_base_02(self):
        """Base test with strongs."""
        x = '5'
        y = '11.3'
        p = 3
        c = composant.Coord(x, y, p)
        self.assertEqual(
            (c.x, c.y, c.proj),
            (float(x), float(y), p)
        )

    def test_equal_01(self):
        """Test __equal__ method."""
        self.assertEqual(
            composant.Coord(5, 10, 26),
            composant.Coord(5, 10, 26),
        )

    def test_str_01(self):
        """Test __str__ method."""
        x = 5.9
        y = 10
        p = 22
        c = composant.Coord(x, y, p)
        self.assertTrue(c.__str__().rfind(str(x)) > -1)
        self.assertTrue(c.__str__().rfind(str(y)) > -1)
        self.assertTrue(c.__str__().rfind('proj') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        x = 5.9
        y = 10
        p = None
        c = composant.Coord(x, y, p, strict=False)
        self.assertEqual(
            (c.x, c.y, c.proj),
            (float(x), float(y), p)
        )

    def test_error_01(self):
        """X error."""
        composant.Coord(**{'x': 1, 'y': 2.3, 'proj': 22})
        self.assertRaises(
            TypeError,
            composant.Coord,
            **{'x': 'a', 'y': 2.3, 'proj': 22}
        )

    def test_error_02(self):
        """Y error."""
        composant.Coord(**{'x': 1, 'y': 2.3, 'proj': 22})
        self.assertRaises(
            TypeError,
            composant.Coord,
            **{'x': '1', 'y': None, 'proj': 22}
        )

    def test_error_03(self):
        """Proj error."""
        composant.Coord(**{'x': 1, 'y': 2.3, 'proj': 22})
        self.assertRaises(
            TypeError,
            composant.Coord,
            **{'x': '1', 'y': 8156941.2368, 'proj': None}
        )
        self.assertRaises(
            ValueError,
            composant.Coord,
            **{'x': '1', 'y': 8156941.2368, 'proj': 8591674}
        )


#-- class TestIsCodeHydro -----------------------------------------------------
class TestIsCodeHydro(unittest.TestCase):

    """Function is_code_hydro class tests."""

    def test_bool_true(self):
        """True test."""
        self.assertTrue(composant.is_code_hydro('A3330510', raises=False))
        self.assertTrue(composant.is_code_hydro('A3330510', raises=True))
        self.assertTrue(
            composant.is_code_hydro('A333051002', 10, raises=False)
        )
        self.assertTrue(
            composant.is_code_hydro('A333051002', 10, raises=True)
        )
        self.assertTrue(
            composant.is_code_hydro('A33305100101', 12, raises=False)
        )
        self.assertTrue(
            composant.is_code_hydro('A33305100101', 12, raises=True)
        )

    def test_bool_false(self):
        """False test."""
        # TypeError
        self.assertFalse(composant.is_code_hydro(33, raises=False))
        # too short
        self.assertFalse(composant.is_code_hydro('A330010', raises=False))
        # too long
        self.assertFalse(
            composant.is_code_hydro('A2233305100101', 12, raises=False)
        )
        # wrong chars
        self.assertFalse(
            composant.is_code_hydro('3330051002', 10, raises=False)
        )
        self.assertFalse(
            composant.is_code_hydro('A330C5100201', 12, raises=False)
        )

    def test_raises(self):
        """Error test."""
        # TypeError
        self.assertRaises(
            TypeError,
            composant.is_code_hydro,
            **{'code': 33, 'raises': True}
        )
        # too short
        self.assertRaises(
            ValueError,
            composant.is_code_hydro,
            **{'code': 'A330010', 'raises': True}
        )
        # too long
        self.assertRaises(
            ValueError,
            composant.is_code_hydro,
            **{'code': 'A2233305100101', 'length': 12, 'raises': True}
        )
        # wrong first char
        self.assertRaises(
            ValueError,
            composant.is_code_hydro,
            **{'code': '33001000', 'raises': True}
        )


#-- class TestIsCodeCommune ---------------------------------------------------
class TestIsCodecommune(unittest.TestCase):

    """Function is_code_commune class tests."""

    def test_bool_true(self):
        """True test."""
        self.assertTrue(composant.is_code_commune('32150', raises=False))
        self.assertTrue(composant.is_code_commune(32150, raises=False))
        self.assertTrue(composant.is_code_commune('02531', raises=True))
        self.assertTrue(composant.is_code_commune('2A531', raises=False))
        self.assertTrue(composant.is_code_commune('2A531', raises=True))
        self.assertTrue(composant.is_code_commune('2B531', raises=False))
        self.assertTrue(composant.is_code_commune('2B531', raises=True))

    def test_bool_false(self):
        """False test."""
        # TypeError
        self.assertFalse(composant.is_code_commune([], raises=False))
        # too short
        self.assertFalse(composant.is_code_commune('3310', raises=False))
        # too long
        self.assertFalse(composant.is_code_commune('333051', raises=False))
        # wrong chars
        self.assertFalse(composant.is_code_commune('3A250', raises=False))
        self.assertFalse(composant.is_code_commune('2C201', raises=False))

    def test_raises(self):
        """Error test."""
        # TypeError (ValueError because code is cast in unicode)
        self.assertRaises(
            ValueError,
            composant.is_code_commune,
            **{'code': [], 'raises': True}
        )
        # too short
        self.assertRaises(
            ValueError,
            composant.is_code_commune,
            **{'code': '3310', 'raises': True}
        )
        # too long
        self.assertRaises(
            ValueError,
            composant.is_code_commune,
            **{'code': '233305', 'raises': True}
        )
        # wrong chars
        self.assertRaises(
            ValueError,
            composant.is_code_commune,
            **{'code': '2D100', 'raises': True}
        )
        self.assertRaises(
            ValueError,
            composant.is_code_commune,
            **{'code': '2A10W', 'raises': True}
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

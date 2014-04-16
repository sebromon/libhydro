#!/usr/bin/env python
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
import datetime
import numpy


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2c"""
__date__ = """2014-03-25"""

#HISTORY
#V0.2 - 2014-03-01
#    add the descriptor tests
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
        self.assertNotEqual(
            composant.Coord(5, 10, 26),
            composant.Coord(6, 10, 26),
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
            ValueError,
            composant.Coord,
            **{'x': '1', 'y': 8156941.2368, 'proj': None}
        )
        self.assertRaises(
            ValueError,
            composant.Coord,
            **{'x': '1', 'y': 8156941.2368, 'proj': 8591674}
        )


#-- class TestDatefromeverything ----------------------------------------------
class TestDatefromeverything(unittest.TestCase):

    """Datefromeverything class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # define a class with value required
        class VR(object):
            dt = composant.Datefromeverything(required=True)

            def __init__(self, dt=None):
                self.dt = dt

        self.VR = VR

        # define a class with value not required
        class VNR(object):
            dt = composant.Datefromeverything(required=False)

            def __init__(self, dt=None):
                self.dt = dt

        self.VNR = VNR

    def test_value_required_init(self):
        """Test the setters and getters when value is required."""
        # init
        dt = datetime.datetime(2008, 10, 10, 9, 33)
        vrs = []
        # build various objects
        vrs.append(self.VR(
            numpy.datetime64('2008-10-10T09:33+00:00')
        ))
        vrs.append(self.VR('2008-10-10T09:33+00:00'))
        vrs.append(self.VR(dt))
        vrs.append(self.VR([2008, 10, 10, 9, 33]))
        vrs.append(self.VR(
            {'year': 2008, 'month': 10, 'day': 10, 'hour': 9, 'minute': 33}
        ))
        for vr in vrs:
            self.assertEqual(vr.dt, dt)

    def test_value_required_error(self):
        """The value required error."""
        self.assertRaises(
            TypeError,
            self.VR,
            None
        )
        self.assertRaises(
            ValueError,
            self.VR,
            '2014-10-08'
        )
        self.assertRaises(
            ValueError,
            self.VR,
            2014
        )
        self.assertRaises(
            ValueError,
            self.VR,
            [2014]
        )

    def test_value_not_required_init(self):
        """Test the setters and getters when value is not required."""
        # init
        dt = datetime.datetime(2010, 1, 5)
        vnrs = []
        # build various objects
        vnrs.append(self.VNR(
            numpy.datetime64('2010-01-05T02:00+02:00')
        ))
        vnrs.append(self.VNR('2010-01-05T02:00+02:00'))
        vnrs.append(self.VNR(dt))
        vnrs.append(self.VNR([2010, 1, 5, 0, 0]))
        vnrs.append(self.VNR([2010, 1, 5]))
        vnrs.append(self.VNR(
            {'year': 2010, 'month': 1, 'day': 5, 'minute': 0}
        ))
        vnrs.append(self.VNR(
            {'year': 2010, 'month': 1, 'day': 5}
        ))
        for vnr in vnrs:
            self.assertEqual(vnr.dt, dt)

    def test_value_not_required_error(self):
        vnr = self.VNR()
        self.assertEqual(vnr.dt, None)
        vnr.dt = None


#-- class TestNomenclatureitem ------------------------------------------------
class TestNomenclatureitem(unittest.TestCase):

    """Nomenclatureitem class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # define a default class
        class NI_strict_required(object):
            ni = composant.Nomenclatureitem(nomenclature=509)

            def __init__(self, ni):
                self.ni = ni

        self.NI_strict_required = NI_strict_required

        # define a class with strict=False
        class NI_required(object):
            ni = composant.Nomenclatureitem(nomenclature=509, strict=False)

            def __init__(self, ni='default value not in nomenclature'):
                self.ni = ni

        self.NI_required = NI_required

        # define a class with required=False
        class NI_strict(object):
            ni = composant.Nomenclatureitem(nomenclature=509, required=False)

            def __init__(self, ni='H'):
                self.ni = ni

        self.NI_strict = NI_strict

    def test_NI_strict_required(self):
        """NI_strict_required test.

        Test the setters and getters when a value is required and has to
        match the nomenclature.

        """
        ni = self.NI_strict_required('H')
        self.assertEqual(ni.ni, 'H')
        ni = self.NI_strict_required('Q')
        self.assertEqual(ni.ni, 'Q')
        ni.ni = 'H'
        self.assertEqual(ni.ni, 'H')

    def test_NI_strict_required_error(self):
        """NI_strict_required error."""
        self.assertRaises(
            ValueError,
            self.NI_strict_required,
            None
        )
        self.assertRaises(
            ValueError,
            self.NI_strict_required,
            'Z'
        )
        ni = self.NI_strict_required('H')
        self.assertRaises(
            ValueError,
            ni.__setattr__,
            *('ni', 'Z')
        )
        self.assertRaises(
            ValueError,
            ni.__setattr__,
            *('ni', None)
        )

    def test_NI_required(self):
        """NI_required test.

        Test the setters and getters when a value is required.

        """
        ni = self.NI_required('H')
        self.assertEqual(ni.ni, 'H')
        ni = self.NI_required('Q')
        self.assertEqual(ni.ni, 'Q')
        ni = self.NI_required('Z')
        self.assertEqual(ni.ni, 'Z')
        ni = self.NI_required(3)
        self.assertEqual(ni.ni, '3')
        ni = self.NI_required()
        self.assertEqual(ni.ni, 'default value not in nomenclature')
        ni.ni = 5
        self.assertEqual(ni.ni, '5')

    def test_NI_required_error(self):
        """NI_required error."""
        self.assertRaises(
            ValueError,
            self.NI_required,
            None
        )
        ni = self.NI_required('H')
        self.assertRaises(
            ValueError,
            ni.__setattr__,
            *('ni', None)
        )

    def test_NI_strict(self):
        """NI_strict test.

        Test the setters and getters whith a strict property.

        """
        ni = self.NI_strict('H')
        self.assertEqual(ni.ni, 'H')
        ni = self.NI_strict('Q')
        self.assertEqual(ni.ni, 'Q')
        ni = self.NI_strict(None)
        self.assertEqual(ni.ni, None)
        # default value
        ni = self.NI_strict()
        self.assertEqual(ni.ni, 'H')
        ni.ni = None
        self.assertEqual(ni.ni, None)
        ni.ni = 'Q'
        self.assertEqual(ni.ni, 'Q')

    def test_NI_strict_error(self):
        """NI_strict error."""
        self.assertRaises(
            ValueError,
            self.NI_strict,
            3
        )
        self.assertRaises(
            ValueError,
            self.NI_strict,
            'Z'
        )
        ni = self.NI_strict('H')
        self.assertRaises(
            ValueError,
            ni.__setattr__,
            *('ni', '333')
        )

    def test_error_01(self):
        """Nomenclature error."""
        self.assertRaises(
            ValueError,
            composant.Nomenclatureitem,
            **{'nomenclature': 0}
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
        # a bastard code Hydro2 !
        self.assertTrue(composant.is_code_hydro('A842020C', raises=True))
        self.assertTrue(composant.is_code_hydro('A842020C', raises=False))

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
        self.assertFalse(
            composant.is_code_hydro('A33051CC', raises=False)
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
        # wrong last char
        self.assertRaises(
            ValueError,
            composant.is_code_hydro,
            **{'code': 'A333101a', 'raises': True}
        )
        # wrong chars
        self.assertRaises(
            ValueError,
            composant.is_code_hydro,
            **{'code': 'A33001CC', 'raises': True}
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
# -*- coding: utf-8 -*-
"""Test program for rolecontact.

To run all tests just type:
    python -m unittest test_core_zonehydro

To run only a class test:
    python -m unittest test_core_zonehydro.TestClass

To run only a specific test:
    python -m unittest test_core_zonehydro.TestClass.test_method

"""

# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import unittest

import libhydro.core.zonehydro as _zonehydro


class TestZonehydro(unittest.TestCase):
    """Zonehydro class tests."""

    def test_base_01(self):
        """Simple zone"""
        code = '1234'
        zone = _zonehydro.Zonehydro(code=code)
        self.assertEqual((zone.code, zone.libelle),
                         (code, None))

    def test_base_02(self):
        """Full zone"""
        code = 'A000'
        libelle = 'Libellé'
        zone = _zonehydro.Zonehydro(code=code, libelle=libelle)
        self.assertEqual((zone.code, zone.libelle),
                         (code, libelle))

    def test_str_01(self):
        """Test representation simple role"""
        code = 'A100'
        libelle = 'Libellé'
        zone = _zonehydro.Zonehydro(code=code, libelle=libelle)
        zone_str = zone.__unicode__()
        self.assertTrue(zone_str.find(code) != -1)
        self.assertTrue(zone_str.find(libelle) != -1)
        # without libelle
        zone = _zonehydro.Zonehydro(code=code)
        zone_str = zone.__unicode__()
        self.assertTrue(zone_str.find(code) != -1)

    def test_error_code(self):
        """Test error code"""
        code = 'Z987'
        _zonehydro.Zonehydro(code=code)
        with self.assertRaises(TypeError):
            _zonehydro.Zonehydro()
        for code in ['A', 'A1000']:
            with self.assertRaises(ValueError):
                _zonehydro.Zonehydro(code=code)

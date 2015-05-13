# coding: utf-8
"""Test program for composant_obs.

To run all tests just type:
    python -m unittest test_core_composant_obs

To run only a class test:
    python -m unittest test_core_composant_obs.TestClass

To run only a specific test:
    python -m unittest test_core_composant_obs.TestClass.test_method

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

from libhydro.core import _composant_obs as composant_obs

# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-07-25"""

# HISTORY
# V0.1 - 2014-07-16
#   first shot


# -- class TestObservations ---------------------------------------------------
class TestObservations(unittest.TestCase):

    """Observations class tests."""

    def test_none(self):
        """None test."""
        obs = composant_obs.Observations(int, None)
        self.assertEqual(obs, None)


# -- class TestSerie ----------------------------------------------------------
class TestSerie(unittest.TestCase):

    """Serie class tests."""

    def test_base(self):
        """Base test."""
        with self.assertRaises(TypeError):
            composant_obs.Serie(contact='my')

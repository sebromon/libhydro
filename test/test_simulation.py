# -*- coding: utf-8 -*-
"""Test program for simulation.

To run all tests just type:
    './test_ simulation.py' or 'python test_ simulation.py'

To run only a class test:
    python -m unittest test_ simulation.TestClass

To run only a specific test:
    python -m unittest test_ simulation.TestClass
    python -m unittest test_ simulation.TestClass.test_method

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

from libhydro.core.simulation import Prevision


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """Version 0.1a"""
__date__ = """2013-08-07"""

#HISTORY
#V0.1 - 2013-08-07
#    first shot


#-- todos ---------------------------------------------------------------------


#-- config --------------------------------------------------------------------


#-- class TestPrevision -------------------------------------------------------
class TestPrevision(unittest.TestCase):
    """Prevision class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base_01(self):
        """Simple prevision."""
        dte = '2012-05-18 18:36+00'
        res = 33.5
        p = Prevision(dte, res)
        self.assertEqual(
            p.item(),
            (datetime.datetime(2012, 5, 18, 18, 36), res, 50)
        )

    def test_base_02(self):
        """Prevision with probability."""
        dte = '2012-05-18 00:00+00'
        res = 33.5
        prb = 22.3
        p = Prevision(dte=dte, res=res, prb=prb)
        self.assertEqual(
            p.item(),
            (datetime.datetime(2012, 5, 18), res, int(prb))
        )
        self.assertEqual(
            (p['dte'].item(), p['res'].item(), p['prb'].item()),
            (datetime.datetime(2012, 5, 18), res, int(prb))
        )

    def test_error_01(self):
        """Date error."""
        Prevision(**{'dte': '2012-10-10 10', 'res': 25.8})
        self.assertRaises(
            TypeError,
            Prevision,
            **{'dte': '2012-10-10', 'res': 25.8}
        )

    def test_error_02(self):
        """Res error."""
        Prevision(**{'dte': '2012-10-10 10:10', 'res': 10})
        self.assertRaises(
            ValueError,
            Prevision,
            **{'dte': '2012-10-10 10:10', 'res': 'xxx'}
        )

    def test_error_03(self):
        """Prb error."""
        Prevision(**{'dte': '2012-10-10 10:10', 'res': 25.8, 'prb': 22.3})
        self.assertRaises(
            ValueError,
            Prevision,
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'prb': -1}
        )
        self.assertRaises(
            ValueError,
            Prevision,
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'prb': 111}
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

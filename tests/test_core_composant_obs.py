# -*- coding: utf-8 -*-
"""Test program for composant_obs.

To run all tests just type:
    python -m unittest test_core_composant_obs

To run only a class test:
    python -m unittest test_core_composant_obs.TestClass

To run only a specific test:
    python -m unittest test_core_composant_obs.TestClass.test_method

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


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-07-16"""

#HISTORY
#V0.1 - 2014-07-16
#    first shot


#-- class TestObservations ----------------------------------------------------
class TestObservations(unittest.TestCase):

    raise NotImplementedError


#-- class TestSerie -----------------------------------------------------------
class TestSerie(unittest.TestCase):

    raise NotImplementedError

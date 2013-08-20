# -*- coding: utf-8 -*-
"""Test program for modeleprevision.

To run all tests just type:
    './test_modeleprevision.py' or 'python test_modeleprevision.py'

To run only a class test:
    python -m unittest test_modeleprevision.TestClass

To run only a specific test:
    python -m unittest test_modeleprevision.TestClass
    python -m unittest test_modeleprevision.TestClass.test_method

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

from libhydro.core import modeleprevision


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """Version 0.1b"""
__date__ = """2013-08-20"""

#HISTORY
#V0.1 - 2013-08-06
#    first shot


#-- todos ---------------------------------------------------------------------


#-- config --------------------------------------------------------------------


#-- class TestModeleprevision -------------------------------------------------
class TestModeleprevision(unittest.TestCase):
    """Modeleprevision class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base_01(self):
        """Empty Modeleprevision."""
        code = libelle = description = None
        typemodele = 0
        m = modeleprevision.Modeleprevision()
        self.assertEqual(
            (m.code, m.libelle, m.typemodele, m.description),
            (code, libelle, typemodele, description)
        )

    def test_base_02(self):
        """Basic modele SHOM."""
        code = 'SCnMERshom'
        libelle = 'Maree SHOM'
        typemodele = 5
        description = 'Les predictions de maree du SHOM.'
        m = modeleprevision.Modeleprevision(
            code=code, libelle=libelle,
            typemodele=typemodele, description=description
        )
        self.assertEqual(
            (m.code, m.libelle, m.typemodele, m.description),
            (code, libelle, typemodele, description)
        )

    def test_base_03(self):
        """Basic modele Arpege."""
        code = 'SCyMERarp'
        libelle = 'Surcote Arpege'
        typemodele = 4
        description = 'Surcote MF.'
        m = modeleprevision.Modeleprevision(
            code=code, libelle=libelle,
            typemodele=typemodele, description=description
        )
        self.assertEqual(
            (m.code, m.libelle, m.typemodele, m.description),
            (code, libelle, typemodele, description)
        )

    def test_str_01(self):
        """Test __str__ method with None values."""
        m = modeleprevision.Modeleprevision()
        self.assertTrue(m.__str__().rfind('Modele') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        code = 'SCyMERarp this one is too long !'
        typemodele = 8545
        m = modeleprevision.Modeleprevision(
            code=code, typemodele=typemodele, strict=False
        )
        self.assertEqual(
            (m.code, m.typemodele),
            (code, typemodele)
        )

    def test_error_01(self):
        """Code error."""
        modeleprevision.Modeleprevision(**{'code': '0123456789'})
        self.assertRaises(
            ValueError,
            modeleprevision.Modeleprevision,
            **{'code': '0123456789x'}
        )

    def test_error_02(self):
        """Typemodele error."""
        modeleprevision.Modeleprevision(**{'typemodele': 1})
        self.assertRaises(
            ValueError,
            modeleprevision.Modeleprevision,
            **{'typemodele': 1000}
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

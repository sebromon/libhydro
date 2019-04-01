# coding: utf-8
"""Test program for modeleprevision.

To run all tests just type:
    python -m unittest test_core_modeleprevision

To run only a class test:
    python -m unittest test_core_modeleprevision.TestClass

To run only a specific test:
    python -m unittest test_core_modeleprevision.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import unittest
import datetime as _datetime

from libhydro.core import (modeleprevision, intervenant as _intervenant,
                           sitehydro as _sitehydro)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1b"""
__date__ = """2013-08-20"""

# HISTORY
# V0.1 - 2013-08-06
#   first shot


# -- class TestModeleprevision ------------------------------------------------
class TestModeleprevision(unittest.TestCase):
    """Modeleprevision class tests."""

    def test_base_01(self):
        """Empty Modeleprevision."""
        code = libelle = description = None
        typemodele = 0
        m = modeleprevision.Modeleprevision()
        self.assertEqual(
            (m.code, m.libelle, m.typemodele, m.description, m.contact,
             m.dtmaj, m.siteshydro),
            (code, libelle, typemodele, description, None, None, [])
        )

    def test_base_02(self):
        """Basic modele SHOM."""
        code = 'SCnMERshom'
        libelle = 'Maree SHOM'
        typemodele = 5
        description = 'Les predictions de maree du SHOM.'
        contact = _intervenant.Contact(code='125')
        dtmaj = _datetime.datetime(2014, 10, 3, 11, 17, 54)
        siteshydro = [_sitehydro.Sitehydro(code='A1234567'),
                      _sitehydro.Sitehydro(code='Z7654321')]
        m = modeleprevision.Modeleprevision(
            code=code, libelle=libelle,
            typemodele=typemodele, description=description, contact=contact,
            dtmaj=dtmaj, siteshydro=siteshydro
        )
        self.assertEqual(
            (m.code, m.libelle, m.typemodele, m.description, m.contact,
             m.dtmaj, m.siteshydro),
            (code, libelle, typemodele, description, contact,
             dtmaj, siteshydro)
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

    def test_error_03(self):
        """Contact error."""
        code = '0123456789'
        for contact in [None, _intervenant.Contact(code='9999')]:
            modeleprevision.Modeleprevision(code=code, contact=contact)
        for contact in ['4321', 'toto']:
            with self.assertRaises(TypeError):
                modeleprevision.Modeleprevision(code=code, contact=contact)

    def test_error_04(self):
        """Siteshydro error."""
        code = '0123456789'
        site0 = _sitehydro.Sitehydro(code='A1234567')
        site1 = _sitehydro.Sitehydro(code='Z7654321')
        for siteshydro in [None, [], site0, [site0], [site0, site1]]:
            modeleprevision.Modeleprevision(code=code, siteshydro=siteshydro)
        for siteshydro in ['A1234567', [site0, 'Z7654321']]:
            with self.assertRaises(TypeError):
                modeleprevision.Modeleprevision(code=code,
                                                siteshydro=siteshydro)

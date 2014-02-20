# -*- coding: utf-8 -*-
"""Test program for intervenant.

To run all tests just type:
    './test_core_intervenant.py' or 'python test_core_intervenant.py'

To run only a class test:
    python -m unittest test_core_intervenant.TestClass

To run only a specific test:
    python -m unittest test_core_intervenant.TestClass
    python -m unittest test_core_intervenant.TestClass.test_method

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

from libhydro.core import intervenant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin""" \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1c"""
__date__ = """2014-02-20"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


#-- class TestIntervenant -----------------------------------------------------
class TestIntervenant(unittest.TestCase):

    """Intervenant class tests."""

    def test_base_01(self):
        """Empty Intervenant."""
        i = intervenant.Intervenant()
        self.assertEqual(
            (i.code, i.origine, i.nom, i.mnemo, i.contacts),
            (0, 'SANDRE', None, None, [])
        )

    def test_base_02(self):
        """SIRET auto Intervenant."""
        code = 12345678901234
        i = intervenant.Intervenant(code=code)
        self.assertEqual(
            (i.code, i.origine),
            (code, 'SIRET')
        )

    def test_base_03(self):
        """SIRET Intervenant."""
        code = 12345678901234
        origine = 'SIRET'
        nom = 'Service Central de la Pluie'
        mnemo = 'SCHAPI'
        contacts = [
            intervenant.Contact(code=0), intervenant.Contact(code=1)
        ]
        it = intervenant.Intervenant(
            code=code, origine='I', nom=nom, mnemo=mnemo, contacts=contacts
        )
        self.assertEqual(
            (it.code, it.origine, it.nom, it.mnemo, it.contacts),
            (code, origine, nom, mnemo, contacts)
        )
        for ct in it.contacts:
            self.assertEqual(ct.intervenant, it)

    def test_base_04(self):
        """SANDRE auto Intervenant."""
        code = 33
        i = intervenant.Intervenant(code=code)
        self.assertEqual(
            (i.code, i.origine),
            (code, 'SANDRE')
        )

    def test_base_05(self):
        """SANDRE Intervenant."""
        code = 123
        origine = 'SANDRE'
        nom = 'Service Central de la Pluie'
        mnemo = 'SCHAPI'
        contacts = [intervenant.Contact()]
        it = intervenant.Intervenant(
            code=code, origine='A', nom=nom, mnemo=mnemo, contacts=contacts[0]
        )
        self.assertEqual(
            (it.code, it.origine, it.nom, it.mnemo, it.contacts),
            (code, origine, nom, mnemo, contacts)
        )
        for ct in it.contacts:
            self.assertEqual(ct.intervenant, it)
        it.code = 12345678901234
        it.origine = 'SIRET'
        it.contacts = None

    def test_str_01(self):
        """Test __str__ method with None values."""
        i = intervenant.Intervenant()
        self.assertTrue(i.__str__().rfind('Intervenant') > -1)
        self.assertTrue(i.__str__().rfind('contact') > -1)

    def test_error_01(self):
        """Code error."""
        it = intervenant.Intervenant(origine='SANDRE')
        self.assertRaises(
            TypeError,
            it.__setattr__,
            *('code', None)
        )

    def test_error_02(self):
        """Origine error."""
        it = intervenant.Intervenant(origine='SANDRE')
        self.assertRaises(
            ValueError,
            intervenant.Intervenant,
            **{'origine': 'SIRET'}
        )
        self.assertRaises(
            ValueError,
            intervenant.Intervenant,
            **{'origine': 'S'}
        )
        self.assertRaises(
            ValueError,
            it.__setattr__,
            *('origine', None)
        )

    def test_error_03(self):
        """SIRET error."""
        code = 12345678901234
        intervenant.Intervenant(code=code, origine='SANDRE')
        it = intervenant.Intervenant(code=code, origine='SIRET')
        self.assertRaises(
            ValueError,
            intervenant.Intervenant,
            **{'origine': 'SIRET'}
        )
        self.assertRaises(
            ValueError,
            it.__setattr__,
            *('code', 123)
        )
        self.assertRaises(
            ValueError,
            intervenant.Intervenant,
            **{'code': 123, 'origine': 'SIRET'}
        )

    def test_error_04(self):
        """Contact error."""
        contacts = [intervenant.Contact()]
        intervenant.Intervenant(contacts=contacts)
        self.assertRaises(
            TypeError,
            intervenant.Intervenant,
            **{'contacts': '---'}
        )

    def test_error_05(self):
        """Contact link error."""
        it1 = intervenant.Intervenant(code=1)
        it2 = intervenant.Intervenant(code=2)
        contacts = [
            intervenant.Contact(code=10, intervenant=it1),
            intervenant.Contact(code=20, intervenant=it2)
        ]
        it1.contacts = contacts[0]
        it2.contacts = contacts[1]
        self.assertRaises(
            ValueError,
            it1.__setattr__,
            *('contacts', contacts[1])
        )
        self.assertRaises(
            ValueError,
            it2.__setattr__,
            *('contacts', contacts[0])
        )


#-- class TestContact ---------------------------------------------------------
class TestContact(unittest.TestCase):

    """Contact class tests."""

    def test_base_01(self):
        """Empty Contact."""
        c = intervenant.Contact()
        self.assertEqual(
            (c.code, c.nom, c.prenom, c.civilite, c.intervenant),
            (None, None, None, None, None)
        )

    def test_base_02(self):
        """Base Contact."""
        code = 99
        nom = 'Toto'
        prenom = 'Robert'
        civilite = 3
        i = intervenant.Intervenant(code=5)
        c = intervenant.Contact(
            code=code, nom=nom, prenom=prenom,
            civilite=civilite, intervenant=i
        )
        self.assertEqual(
            (c.code, c.nom, c.prenom, c.civilite, c.intervenant),
            (code, nom, prenom, civilite, i)
        )

    def test_str_01(self):
        """Test __str__ method with None values."""
        c = intervenant.Contact()
        self.assertTrue(c.__str__().rfind('Contact') > -1)

    def test_error_01(self):
        """Code error."""
        it = intervenant.Contact(code=99)
        self.assertRaises(
            ValueError,
            it.__setattr__,
            *('code', 'abcd')
        )
        self.assertRaises(
            ValueError,
            intervenant.Contact,
            **{'code': -1}
        )
        self.assertRaises(
            ValueError,
            intervenant.Contact,
            **{'code': 10000}
        )

    def test_error_02(self):
        """Civilite error."""
        intervenant.Contact(civilite=1)
        self.assertRaises(
            ValueError,
            intervenant.Contact,
            **{'civilite': 0}
        )

    def test_error_03(self):
        """Intervenant error."""
        i = intervenant.Intervenant(code=5)
        intervenant.Contact(intervenant=i)
        self.assertRaises(
            TypeError,
            intervenant.Contact,
            **{'intervenant': 5}
        )

#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

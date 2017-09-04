# coding: utf-8
"""Test program for intervenant.

To run all tests just type:
    python -m unittest test_core_intervenant

To run only a class test:
    python -m unittest test_core_intervenant.TestClass

To run only a specific test:
    python -m unittest test_core_intervenant.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import unittest

from libhydro.core import intervenant


# -- strings ------------------------------------------------------------------
__version__ = '0.2.2'
__date__ = '2017-05-04'

# HISTORY
# V0.2 - 2017-04-20
#   tests propriete Contact.profil
#   update tests to new Contact.code type
#   some refactoring
# V0.1 - 2013-08-20
#   first shot


# -- class TestIntervenant ----------------------------------------------------
class TestIntervenant(unittest.TestCase):

    """Intervenant class tests."""

    def test_base_01(self):
        """Empty Intervenant."""
        i = intervenant.Intervenant()
        self.assertEqual(
            (i.code, i.origine, i.nom, i.mnemo, i.contacts),
            (0, 'SANDRE', None, None, []))

    def test_base_02(self):
        """SIRET auto Intervenant."""
        code = 12345678901234
        i = intervenant.Intervenant(code=code)
        self.assertEqual((i.code, i.origine), (code, 'SIRET'))

    def test_base_03(self):
        """SIRET Intervenant."""
        code = 12345678901234
        origine = 'SIRET'
        nom = 'Service Central de la Pluie'
        mnemo = 'SCHAPI'
        contacts = [intervenant.Contact(code=0), intervenant.Contact(code=1)]
        it = intervenant.Intervenant(
            code=code, origine='I', nom=nom, mnemo=mnemo, contacts=contacts)
        self.assertEqual(
            (it.code, it.origine, it.nom, it.mnemo, it.contacts),
            (code, origine, nom, mnemo, contacts))
        for ct in it.contacts:
            self.assertEqual(ct.intervenant, it)

    def test_base_04(self):
        """SANDRE auto Intervenant."""
        code = 33
        i = intervenant.Intervenant(code=code)
        self.assertEqual((i.code, i.origine), (code, 'SANDRE'))

    def test_base_05(self):
        """SANDRE Intervenant."""
        code = 123
        origine = 'SANDRE'
        nom = 'Service Central de la Pluie'
        mnemo = 'SCHAPI'
        contacts = [intervenant.Contact(code='99')]
        it = intervenant.Intervenant(
            code=code, origine='A', nom=nom, mnemo=mnemo, contacts=contacts[0])
        self.assertEqual(
            (it.code, it.origine, it.nom, it.mnemo, it.contacts),
            (code, origine, nom, mnemo, contacts))
        for ct in it.contacts:
            self.assertEqual(ct.intervenant, it)
        it.code = 12345678901234
        it.origine = 'SIRET'
        it.contacts = None

    def test_str_01(self):
        """Test __str__ method with None values."""
        i = intervenant.Intervenant(nom='toto')
        self.assertTrue(i.__str__().rfind('Intervenant') > -1)
        self.assertTrue(i.__str__().rfind('contact') > -1)
        i = intervenant.Intervenant(33, mnemo='toto')
        self.assertTrue(i.__str__().rfind('Intervenant') > -1)
        self.assertTrue(i.__str__().rfind('contact') > -1)
        i = intervenant.Intervenant()
        self.assertTrue(i.__str__().rfind('Intervenant') > -1)
        self.assertTrue(i.__str__().rfind('contact') > -1)
        self.assertTrue(i.__str__().rfind('<sans nom>') > -1)

    def test_error_01(self):
        """Code error."""
        it = intervenant.Intervenant(origine='SANDRE')
        self.assertRaises(TypeError, it.__setattr__, *('code', None))

    def test_error_02(self):
        """Origine error."""
        it = intervenant.Intervenant(origine='SANDRE')
        self.assertRaises(
            ValueError, intervenant.Intervenant, **{'origine': 'SIRET'})
        self.assertRaises(
            ValueError, intervenant.Intervenant, **{'origine': 'S'})
        self.assertRaises(ValueError, it.__setattr__, *('origine', None))

    def test_error_03(self):
        """SIRET error."""
        code = 12345678901234
        intervenant.Intervenant(code=code, origine='SANDRE')
        it = intervenant.Intervenant(code=code, origine='SIRET')
        self.assertRaises(
            ValueError, intervenant.Intervenant, **{'origine': 'SIRET'})
        self.assertRaises(
            ValueError, it.__setattr__, *('code', 123))
        self.assertRaises(
            ValueError, intervenant.Intervenant,
            **{'code': 123, 'origine': 'SIRET'})

    def test_error_04(self):
        """Contact error."""
        contacts = [intervenant.Contact(code='5')]
        intervenant.Intervenant(contacts=contacts)
        self.assertRaises(
            TypeError, intervenant.Intervenant, **{'contacts': '---'})

    def test_error_05(self):
        """Contact link error."""
        it1 = intervenant.Intervenant(code=1)
        it2 = intervenant.Intervenant(code=2)
        contacts = [
            intervenant.Contact(code=10, intervenant=it1),
            intervenant.Contact(code=20, intervenant=it2)]
        it1.contacts = contacts[0]
        it2.contacts = contacts[1]
        self.assertRaises(
            ValueError, it1.__setattr__, *('contacts', contacts[1]))
        self.assertRaises(
            ValueError, it2.__setattr__, *('contacts', contacts[0]))


# -- class TestContact --------------------------------------------------------
class TestContact(unittest.TestCase):

    """Contact class tests."""

    def test_base_01(self):
        """Empty Contact."""
        code = '99'
        c = intervenant.Contact(code=code)
        self.assertEqual(
            (c.code, c.nom, c.prenom, c.civilite, c.intervenant,
             c.profil, c.motdepasse),
            (code, None, None, None, None, 0, None))

    def test_base_02(self):
        """Base Contact."""
        code = '99'
        nom = 'Toto'
        prenom = 'Robert'
        civilite = 3
        profil = 7  # 0b111
        motdepasse = 'mdp'
        i = intervenant.Intervenant(code=5)
        c = intervenant.Contact(
            code=code, nom=nom, prenom=prenom, civilite=civilite,
            intervenant=i, profil=profil, motdepasse=motdepasse)
        self.assertEqual(
            (c.code, c.nom, c.prenom, c.civilite, c.intervenant,
             c.profil, c.motdepasse),
            (code, nom, prenom, civilite, i, 7, motdepasse))

    def test_profil(self):
        """Test profil."""
        # base case
        c = intervenant.Contact(code=0)
        self.assertEqual(c.profil, 0)
        c.profil = 5
        self.assertEqual(c.profil, 5)
        # errors
        with self.assertRaises(ValueError):
            c.profil = -1
        with self.assertRaises(ValueError):
            c.profil = 8
        with self.assertRaises(ValueError):
            c.profil = 'r'

    def test_profiladminnat(self):
        """Test profiladminnat."""
        code = '99'
        nom = 'Toto'
        prenom = 'Robert'
        civilite = 3
        profil = 3  # 0b011
        i = intervenant.Intervenant(code=5)
        c = intervenant.Contact(
            code=code, nom=nom, prenom=prenom, civilite=civilite,
            intervenant=i, profil=profil)
        self.assertFalse(c.profiladminnat)
        c.profiladminnat = True
        self.assertTrue(c.profiladminnat)
        for profil in ('100', '101', '110', '111'):
            c.profil = profil
            self.assertTrue(c.profiladminnat)
        for profil in ('000', '001', '010', '011'):
            c.profil = profil
            self.assertFalse(c.profiladminnat)

    def test_profilmodel(self):
        """Test profilmodel."""
        code = '99'
        nom = 'Toto'
        prenom = 'Robert'
        civilite = 3
        profil = 3  # 0b011
        i = intervenant.Intervenant(code=5)
        c = intervenant.Contact(
            code=code, nom=nom, prenom=prenom, civilite=civilite,
            intervenant=i)
        self.assertFalse(c.profilmodel)
        c.profilmodel = profil
        self.assertTrue(c.profilmodel)
        for profil in ('010', '011', '110', '111'):
            c.profil = profil
            self.assertTrue(c.profilmodel)
        for profil in ('000', '001', '100', '101'):
            c.profil = profil
            self.assertFalse(c.profilmodel)

    def test_profilinst(self):
        """Test profilinst."""
        code = 'xxx'
        profil = 1  # 0b001
        i = intervenant.Intervenant(code=5)
        c = intervenant.Contact(
            code=code, intervenant=i, profil=profil)
        self.assertTrue(c.profilinst)
        c.profilinst = 0
        self.assertFalse(c.profilinst)
        for profil in ('001', '011', '101', '111'):
            c.profil = profil
            self.assertTrue(c.profilinst)
        for profil in ('000', '010', '100', '110'):
            c.profil = profil
            self.assertFalse(c.profilinst)

    def test_profilpublic(self):
        """Test profilpublic."""
        code = '!!'
        profil = 7  # 0b111
        i = intervenant.Intervenant(code=5)
        c = intervenant.Contact(
            code=code, intervenant=i, profil=profil)
        self.assertFalse(c.profilpublic)
        c.profilpublic = True
        self.assertTrue(c.profilpublic)
        for profil in ('000',):
            c.profil = profil
            self.assertTrue(c.profilpublic)
        for profil in ('001', '010', '011', '100', '101', '110', '111'):
            c.profil = profil
            self.assertFalse(c.profilpublic)

    def test_str_01(self):
        """Test __str__ method with None values."""
        c = intervenant.Contact(code='99')
        self.assertTrue(c.__str__().rfind('Contact') > -1)

    def test_error_01(self):
        """Code error."""
        c = intervenant.Contact(code=99999)
        c = intervenant.Contact(code='abcde')
        c = intervenant.Contact(code='-1')
        self.assertRaises(
            ValueError, c.__setattr__, *('code', 'abcdefgh'))  # too long
        self.assertRaises(
            ValueError, intervenant.Contact, **{'code': 100000})  # too long

    def test_error_02(self):
        """Civilite error."""
        intervenant.Contact(code='99', civilite=1)
        self.assertRaises(
            ValueError, intervenant.Contact, **{'code': '99', 'civilite': 0})

    def test_error_03(self):
        """Intervenant error."""
        i = intervenant.Intervenant(code=5)
        intervenant.Contact(code=5, intervenant=i)
        self.assertRaises(
            TypeError, intervenant.Contact, **{'code': '99', 'intervenant': 5})

    def test_error_04(self):
        """profil error."""
        for profil in ('88', '5', '200'):
            with self.assertRaises(ValueError):
                intervenant.Contact(code='1', profil=profil)

    def test_error_05(self):
        """absence de code contact."""
        with self.assertRaises(TypeError):
            intervenant.Contact()
        with self.assertRaises(TypeError):
            intervenant.Contact(code=None)

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
from datetime import datetime

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
             c.profil, c.adresse, c.fonction, c.telephone, c.portable, c.fax,
             c.mel, c.dtmaj, c.profilsadmin, c.alias, c.motdepasse,
             c.dtactivation, c.dtdesactivation),
            (code, None, None, None, None, 0, None, None, None, None, None,
             None, None, [], None, None, None, None))

    def test_base_02(self):
        """Base Contact."""
        code = '99'
        nom = 'Toto'
        prenom = 'Robert'
        civilite = 3
        profil = 7  # 0b111
        motdepasse = 'mdp'
        adresse = intervenant.Adresse(ville='Paris',
                                      adresse1='18 rue toto',
                                      codepostal='31000',
                                      pays='FR')
        telephone = '00000'
        portable = '060000'
        fax = '99'
        mel = 'toto@tata.fr'
        alias = 'ALIAS'
        dtactivation = datetime(2012, 7, 2, 10, 30, 50)
        dtdesactivation = datetime(2015, 3, 22, 18, 15, 25)
        i = intervenant.Intervenant(code=5)
        fonction = 'Hydromètre'
        dtmaj = datetime(2017, 12, 15, 10, 54, 37)
        profil1 = intervenant.ProfilAdminLocal(profil='GEST', zoneshydro='A123')
        profil2 = intervenant.ProfilAdminLocal(profil='JAU', zoneshydro='R444')
        profilsadmin = [profil1, profil2]
        c = intervenant.Contact(
            code=code, nom=nom, prenom=prenom, civilite=civilite,
            intervenant=i, profil=profil, adresse=adresse, fonction=fonction,
            telephone=telephone, portable=portable, fax=fax, mel=mel,
            dtmaj=dtmaj, profilsadmin=profilsadmin, alias=alias,
            motdepasse=motdepasse, dtactivation=dtactivation,
            dtdesactivation=dtdesactivation)
        self.assertEqual(
            (c.code, c.nom, c.prenom, c.civilite, c.intervenant,
             c.profil, c.adresse, c.fonction, c.telephone, c.portable, c.fax,
             c.mel, c.dtmaj, c.profilsadmin, c.alias, c.motdepasse,
             c.dtactivation, c.dtdesactivation),
            (code, nom, prenom, civilite, i, profil, adresse, fonction,
             telephone, portable, fax, mel, dtmaj, profilsadmin, alias,
             motdepasse, dtactivation, dtdesactivation))

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

    def test_adresse(self):
        adr = intervenant.Adresse('Toulouse')
        for adresse in [None, adr]:
            intervenant.Contact(code='9999', adresse=adresse)
        for adresse in ['Toulouse', 5]:
            with self.assertRaises(Exception):
                intervenant.Contact(code='9999', adresse=adresse)

    def test_profilsadmin(self):
        profil1 = intervenant.ProfilAdminLocal(profil='GEST', zoneshydro='A123')
        profil2 = intervenant.ProfilAdminLocal(profil='JAU', zoneshydro='R444')
        for profilsadmin in [None, [], profil1, [profil1, profil2]]:
            intervenant.Contact(code='9999', profilsadmin=profilsadmin)
        for profilsadmin in ['JAU', [profil1, 'GEST']]:
            with self.assertRaises(Exception):
                intervenant.Contact(code='9999', profilsadmin=profilsadmin)

# -- class TestContact --------------------------------------------------------
class TestAdresse(unittest.TestCase):

    """Contact class tests."""

    def test_simple(self):
        ville = 'Toulouse'
        adr = intervenant.Adresse(ville=ville)
        self.assertEqual(adr.ville, ville)

    def test_full_adresse(self):
        ville = 'Bordeaux'
        adresse1 = '17 rue toto'
        adresse2 = '134 avenue tata'
        codepostal = '33000'
        boitepostale = 'boîte postale'
        pays = 'FR'
        adr = intervenant.Adresse(ville=ville, adresse1=adresse1,
                                  adresse2=adresse2, boitepostale=boitepostale,
                                  codepostal=codepostal, pays=pays)
        self.assertEqual((adr.ville, adr.adresse1, adr.adresse2,
                          adr.boitepostale, adr.codepostal, adr.pays),
                         (ville, adresse1, adresse2,
                          boitepostale, codepostal, pays))

    def test_str_01(self):
        ville = 'Agen'
        adresse1 = '5 rue toto'
        codepostal = '12345'
        pays = 'FR'
        adr = intervenant.Adresse(ville=ville, adresse1=adresse1,
                                  codepostal=codepostal, pays=pays)
        adrstr = adr.__str__()
        self.assertTrue(adrstr.find(ville) > -1)
        self.assertTrue(adrstr.find(adresse1) > -1)
        self.assertTrue(adrstr.find(codepostal) > -1)
        self.assertTrue(adrstr.find(pays) > -1)

    def test_str_02(self):
        ville = None
        adr = intervenant.Adresse(ville=ville)
        adrstr = adr.__str__()
        self.assertTrue(adrstr.find('sans ville') > -1)

    def test_pays(self):
        ville = 'Madrid'
        pays = 'ES'
        intervenant.Adresse(ville=ville, pays=pays)
        for pays in ['Espagne', 'E', 5]:
            with self.assertRaises(Exception):
                intervenant.Adresse(ville=ville, pays=pays)


# -- class TestProfilAdminLocal -----------------------------------------------
class TestProfilAdminLocal(unittest.TestCase):

    """Contact class tests."""
    def test_simple(self):
        profil = 'GEST'
        zoneshydro = ['A123']
        pal = intervenant.ProfilAdminLocal(profil=profil,
                                           zoneshydro=zoneshydro)
        self.assertEqual((pal.profil, pal.zoneshydro, pal.dtactivation,
                          pal.dtdesactivation),
                         (profil, zoneshydro, None, None))

    def test_full(self):
        profil = 'JAU'
        zoneshydro = ['A123', 'Z987']
        dtactivation = datetime(2015, 10, 14, 10, 20, 30)
        dtdesactivation = datetime(2017, 1, 17, 18, 19, 15)
        pal = intervenant.ProfilAdminLocal(profil=profil,
                                           zoneshydro=zoneshydro,
                                           dtactivation=dtactivation,
                                           dtdesactivation=dtdesactivation)
        self.assertEqual((pal.profil, pal.zoneshydro, pal.dtactivation,
                          pal.dtdesactivation),
                         (profil, zoneshydro, dtactivation, dtdesactivation))

    def test_profil(self):
        zoneshydro = 'B000'
        for profil in ['JAU', 'GEST']:
            intervenant.ProfilAdminLocal(profil=profil, zoneshydro=zoneshydro)
        for profil in [None, 'Gestionnaire']:
            with self.assertRaises(Exception):
                intervenant.ProfilAdminLocal(profil=profil,
                                             zoneshydro=zoneshydro)

    def test_zonehydro(self):
        profil = 'GEST'
        for zoneshydro in ['A123', ['A123'], ['A123', 'B456']]:
            intervenant.ProfilAdminLocal(profil=profil, zoneshydro=zoneshydro)
        for zoneshydro in [None, [], ['A'], ['A12345'], ['A123', 'B12']]:
            with self.assertRaises(Exception):
                intervenant.ProfilAdminLocal(profil=profil,
                                             zoneshydro=zoneshydro)

    def test_str_01(self):
        profil = 'GEST'
        zoneshydro = 'A123'
        pal = intervenant.ProfilAdminLocal(profil=profil, zoneshydro=zoneshydro)
        palstr = pal.__str__()
        self.assertTrue(palstr.find(zoneshydro) > -1)
        self.assertTrue(palstr.find(profil) > -1)

    def test_str_02(self):
        profil = 'GEST'
        zoneshydro = ['A123', 'Z999']
        dtactivation = datetime(2015, 10, 14, 10, 20, 30)
        dtdesactivation = datetime(2017, 1, 17, 18, 19, 15)
        pal = intervenant.ProfilAdminLocal(profil=profil, zoneshydro=zoneshydro,
                                           dtactivation=dtactivation,
                                           dtdesactivation=dtdesactivation)
        palstr = pal.__unicode__()
        for zonehydro in zoneshydro:
            self.assertTrue(palstr.find(zonehydro) > -1)
        self.assertTrue(palstr.find(profil) > -1)
        self.assertTrue(palstr.find(str(dtactivation)) > -1)
        self.assertTrue(palstr.find(str(dtdesactivation)) > -1)

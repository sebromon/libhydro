# coding: utf-8
"""Test program for seuil.

To run all tests just type:
    python -m unittest test_core_seuil

To run only a class test:
    python -m unittest test_core_seuil.TestClass

To run only a specific test:
    python -m unittest test_core_seuil.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime
import unittest

from libhydro.core.seuil import Seuilhydro, Seuilmeteo, Valeurseuil
from libhydro.core import sitehydro, sitemeteo


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1e"""
__date__ = """2014-12-17"""

# HISTORY
# V0.1 - 2014-02-12
#   first shot


# -- class TestSeuilhydro -----------------------------------------------------
class TestSeuilhydro(unittest.TestCase):

    """Seuilhydro class tests."""

    def test_base_01(self):
        """Minimum Seuilhydro."""
        code = 'seuil 1'
        seuil = Seuilhydro(code)
        self.assertEqual(
            (
                seuil.code, seuil.sitehydro, seuil.typeseuil,
                seuil.duree, seuil.nature, seuil.libelle,
                seuil.mnemo, seuil.gravite, seuil.commentaire,
                seuil.publication, seuil.valeurforcee,
                seuil.dtmaj, seuil.valeurs
            ),
            (
                code, None, None, None, None, None, None, None, None,
                None, None, None, []
            )
        )

    def test_base_02(self):
        """Full Seuilhydro."""
        site = sitehydro.Sitehydro('R5330001')
        capteur = sitehydro.Capteur('R53300010101')
        code = 175896
        typeseuil = 2
        duree = 25
        nature = 11
        libelle = 'Libellé du çeuil'
        mnemo = None
        gravite = 54
        commentaire = 'Ce seuil ne sera jamais dépassé'
        publication = 20
        valeurforcee = True
        dtmaj = datetime.datetime(1953, 12, 31, 8)
        valeurs = [
            Valeurseuil(valeur=10, entite=capteur),
            Valeurseuil(valeur=11, entite=capteur),
            Valeurseuil(valeur=12, entite=capteur)
        ]
        seuil = Seuilhydro(
            code=code,
            sitehydro=site,
            typeseuil=typeseuil,
            duree=duree,
            nature=nature,
            libelle=libelle,
            mnemo=mnemo,
            gravite=gravite,
            commentaire=commentaire,
            publication=publication,
            valeurforcee=valeurforcee,
            dtmaj=dtmaj,
            valeurs=valeurs
        )
        self.assertEqual(
            (
                seuil.code, seuil.sitehydro, seuil.typeseuil, seuil.duree,
                seuil.nature, seuil.libelle, seuil.mnemo, seuil.gravite,
                seuil.commentaire, seuil.publication, seuil.valeurforcee,
                seuil.dtmaj, seuil.valeurs
            ),
            (
                str(code), site, typeseuil, duree, nature, libelle,
                mnemo, gravite, commentaire, publication, valeurforcee,
                dtmaj, valeurs
            )
        )

    def test_publication(self):
        code = 999
        site = sitehydro.Sitehydro('A1234567')
        for publication in [None, 0, 10, 30, 32]:
            Seuilhydro(code=code, sitehydro=site, publication=publication)
        for publication in ['toto', -5, 5, 100]:
            with self.assertRaises(Exception):
                Seuilhydro(code=code, sitehydro=site, publication=publication)

    def test_valeurforcee(self):
        code = 999
        site = sitehydro.Sitehydro('A1234567')
        for valeurforcee in [None, False, True]:
            s = Seuilhydro(code=code, sitehydro=site,
                           valeurforcee=valeurforcee)
            self.assertEqual(s.valeurforcee, valeurforcee)
        s.valeurforcee = 1
        self.assertEqual(s.valeurforcee, True)

    def test_str_01(self):
        """Test __str__ method."""
        site = sitehydro.Sitehydro('R5330001')
        code = 175896
        typeseuil = 1
        duree = 0
        seuil = Seuilhydro(
            sitehydro=site, code=code, typeseuil=typeseuil, duree=duree
        )
        self.assertTrue(seuil.__str__().rfind(str(code)) > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode."""
        code = 175896
        typeseuil = None
        duree = None
        seuil = Seuilhydro(
            sitehydro='site', code=code, typeseuil=typeseuil, duree=duree,
            strict=False
        )
        self.assertTrue(seuil.__str__().rfind(str(code)) > -1)
        self.assertTrue(seuil.__str__().rfind(str('sans duree')) > -1)

    def test_equality_01(self):
        """Test equality and inequality with metadata only."""
        # prepare
        site = sitehydro.Sitehydro('R5330001')
        code = 175896
        typeseuil = 1
        duree = 0
        seuil = Seuilhydro(
            sitehydro=site, code=code, typeseuil=typeseuil, duree=duree
        )
        other = Seuilhydro(
            sitehydro=site, code=code, typeseuil=typeseuil, duree=duree
        )
        # equality
        self.assertEqual(seuil, seuil)
        self.assertEqual(seuil, other)
        # inequality
        other.sitehydro = None
        self.assertNotEqual(seuil, other)
        other.sitehydro, other.code = site, 2
        self.assertNotEqual(seuil, other)
        # lazy mode
        other = Seuilhydro(
            sitehydro=site, code=code, typeseuil=2, duree=10
        )
        self.assertNotEqual(seuil, other)
        other.typeseuil = other.duree = None
        self.assertTrue(seuil.__eq__(other, lazzy=True))

    def test_equality_02(self):
        """Test equality and inequality with valeurs."""
        # assert equality
        station = sitehydro.Station('Z987654321')
        valeurs = [Valeurseuil(valeur=i, entite=station) for i in range(10)]
        seuil = Seuilhydro(code=1, valeurs=valeurs[:])
        other = Seuilhydro(code=1, valeurs=valeurs[:])
        self.assertEqual(seuil, other)
        self.assertTrue(seuil.__eq__(other, ignore=['valeurs']))
        self.assertTrue(seuil.__eq__(other, ignore=['code']))
        # a shorter list of values
        other.valeurs = valeurs[1:]
        self.assertNotEqual(seuil, other)
        self.assertTrue(seuil.__eq__(other, ignore=['valeurs']))
        self.assertTrue(seuil.__eq__(other, ignore=['code', 'valeurs']))
        self.assertFalse(seuil.__ne__(other, ignore=['valeurs']))
        self.assertTrue(seuil.__ne__(other, ignore=['code']))
        # a different value
        seuil.valeurs = other.valeurs = [Valeurseuil(0, entite=station)]
        self.assertEqual(seuil, other)
        other.valeurs = [Valeurseuil(899.3, entite=station)]
        self.assertNotEqual(seuil, other)
        # None case
        seuil.valeurs = other.valeurs = None
        self.assertEqual(seuil, other)
        # non iterable values
        seuil._strict = other._strict = False
        self.assertEqual(seuil, other)
        seuil.valeurs, other.valeurs = [5], [7]
        self.assertNotEqual(seuil, other)

    def test_error_01(self):
        """Code error."""
        code = '175896'
        seuil = Seuilhydro(code=code)
        self.assertEqual(seuil.code, code)
        self.assertRaises(
            TypeError,
            Seuilhydro,
            **{'code': None}
        )

    def test_error_02(self):
        """Typeseuil error."""
        typeseuil = 1
        seuil = Seuilhydro(code=1, typeseuil=typeseuil)
        self.assertEqual(seuil.typeseuil, typeseuil)
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'code': 1, 'typeseuil': 'xxx'}
        )
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'code': 1, 'typeseuil': 999}
            # **{'code': 1, 'typeseuil': 1}
        )

    def test_error_03(self):
        """Duree error."""
        # not an integer
        duree = 10
        seuil = Seuilhydro(code=1, duree=duree)
        self.assertEqual(seuil.duree, duree)
        self.assertRaises(
            TypeError,
            Seuilhydro,
            **{'code': 1, 'duree': 'not a integer'}
        )
        # default value is 0 for absolute seuil
        seuil = Seuilhydro(code=1, typeseuil=1)
        self.assertEqual(seuil.duree, 0)
        # absolute seuil duree must be 0
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'code': 1, 'typeseuil': 1, 'duree': 5}
        )
        # gradient seuil must have a duree
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'code': 1, 'typeseuil': 2, 'duree': None}
        )
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'code': 1, 'typeseuil': 2, 'duree': 0}
        )

    def test_error_04(self):
        """Nature error."""
        nature = 101
        seuil = Seuilhydro(code=0, nature=nature)
        self.assertEqual(seuil.nature, nature)
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'code': 0, 'nature': 49}
        )

    def test_error_05(self):
        """Gravite error."""
        gravite = 100
        seuil = Seuilhydro(code='aaa', gravite=gravite)
        self.assertEqual(seuil.gravite, gravite)
        gravite = 0
        seuil = Seuilhydro(code='aaa', gravite=gravite)
        self.assertEqual(seuil.gravite, gravite)
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'code': 'aaa', 'gravite': 101}
        )
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'code': 'aaa', 'gravite': -1}
        )
        self.assertRaises(
            TypeError,
            Seuilhydro,
            **{'code': 'aaa', 'gravite': 'xx'}
        )

    def test_error_06(self):
        """Valeurs error."""
        station = sitehydro.Station('P121236541')
        valeurs = [Valeurseuil(10, entite=station)]
        seuil = Seuilhydro(code='A22', valeurs=valeurs)
        self.assertEqual(seuil.code, 'A22')
        self.assertRaises(
            TypeError,
            Seuilhydro,
            **{'code': 0, 'valeurs': [9, 10]}
        )


# -- class TestSeuilmeteo -----------------------------------------------------
class TestSeuilmeteo(unittest.TestCase):

    """Seuilhydro class tests."""

    def test_base_01(self):
        """Minimum Seuilhydro."""
        code = 'seuil 1'
        site = sitemeteo.Sitemeteo(code='010000000')
        grandeurmeteo = sitemeteo.Grandeur(typemesure='RR', sitemeteo=site)
        seuil = Seuilmeteo(code, grandeurmeteo=grandeurmeteo)
        self.assertEqual(
            (
                seuil.code, seuil.grandeurmeteo, seuil.typeseuil,
                seuil.duree, seuil.nature, seuil.libelle,
                seuil.mnemo, seuil.gravite, seuil.commentaire,
                seuil.dtmaj, seuil.valeurs
            ),
            (
                code, grandeurmeteo, None, None, None, None, None, None, None,
                None, []
            )
        )

    def test_base_02(self):
        """Full Seuilhydro."""
        code = 'seuil 1'
        typeseuil = 2
        duree = 60
        nature = 24
        libelle = 'Seuil météo'
        mnemo = 'Météo'
        gravite = 51
        commentaire = 'Commentaire du seuil'
        dtmaj = datetime.datetime(2016, 10, 11, 12, 13, 14)
        site = sitemeteo.Sitemeteo(code='010000000')
        grandeurmeteo = sitemeteo.Grandeur(typemesure='RR', sitemeteo=site)
        valeurs = [Valeurseuil(valeur=150, entite=grandeurmeteo,
                               tolerance=1.5)]
        seuil = Seuilmeteo(code=code, grandeurmeteo=grandeurmeteo,
                           typeseuil=typeseuil, duree=duree, nature=nature,
                           libelle=libelle, mnemo=mnemo, gravite=gravite,
                           commentaire=commentaire, dtmaj=dtmaj,
                           valeurs=valeurs)

        self.assertEqual(
            (
                seuil.code, seuil.grandeurmeteo, seuil.typeseuil,
                seuil.duree, seuil.nature, seuil.libelle,
                seuil.mnemo, seuil.gravite, seuil.commentaire,
                seuil.dtmaj, seuil.valeurs
            ),
            (
                code, grandeurmeteo, typeseuil, duree, nature, libelle, mnemo,
                gravite, commentaire,
                dtmaj, valeurs
            )
        )

    def test_valeurs(self):
        code = '555'
        site = sitemeteo.Sitemeteo(code='010000000')
        grandeurmeteo = sitemeteo.Grandeur(typemesure='RR', sitemeteo=site)
        seuil = Seuilmeteo(code, grandeurmeteo=grandeurmeteo)
        val0 = Valeurseuil(valeur=150, entite=grandeurmeteo, tolerance=1.5)
        val1 = Valeurseuil(valeur=180, entite=grandeurmeteo, tolerance=3)
        tabvaleurs = [None, [], val0, [val1], [val0, val1]]
        expected = [[], [], [val0], [val1], [val0, val1]]
        for index, valeurs in enumerate(tabvaleurs):
            seuil.valeurs = valeurs
            self.assertEqual(seuil.valeurs, expected[index])

    def test_grandeurmeteo(self):
        """test property grandeurmeteo"""
        code = '156'
        site = sitemeteo.Sitemeteo(code='010000000')
        grandeurmeteo = sitemeteo.Grandeur(typemesure='RR', sitemeteo=site)
        Seuilmeteo(code=code, grandeurmeteo=grandeurmeteo)
        for grandeurmeteo in ['4321', 'toto', site]:
            with self.assertRaises(TypeError):
                Seuilmeteo(code=code, grandeurmeteo=grandeurmeteo)


# -- class TestValeurseuil ----------------------------------------------------
class TestValeurseuil(unittest.TestCase):

    """Valeurseuil class tests."""

    def test_base_01(self):
        """Minimum Valeurseuil."""
        site = sitehydro.Sitehydro('A1234567')
        valeur = 33.0
        valseuil = Valeurseuil(valeur=valeur, entite=site)
        self.assertEqual((valseuil.valeur, valseuil.entite),
                         (valeur, site))

    def test_base_02(self):
        """Full Valeurseuil."""
        seuil = Seuilhydro(code=1, strict=False)
        entite = sitehydro.Sitehydro(code='Z8250001')
        tolerance = '10.3'
        valeur = '253.42'
        dtactivation = datetime.datetime(2012, 1, 5, 8, 33)
        dtdesactivation = datetime.datetime(2012, 10, 8, 8, 33)
        valseuil = Valeurseuil(
            valeur=valeur,
            seuil=seuil,
            entite=entite,
            tolerance=tolerance,
            dtactivation=dtactivation,
            dtdesactivation=dtdesactivation
        )
        self.assertEqual(
            (
                valseuil.valeur, valseuil.seuil, valseuil.entite,
                valseuil.tolerance, valseuil.dtactivation,
                valseuil.dtdesactivation
            ),
            (
                float(valeur), seuil, entite, float(tolerance),
                dtactivation, dtdesactivation
            )
        )

    def test_fuzzy_01(self):
        """test fuzzy mode"""
        entite = sitehydro.Sitehydro(code='Z8250001')
        valseuil = Valeurseuil(valeur=None, entite=entite, strict=False)
        self.assertIsNone(valseuil.valeur)

    def test_str_01(self):
        """Test __str__ method."""
        valeur = 8
        tolerance = 5
        entite = sitehydro.Station('R533010110')
        valseuil = Valeurseuil(
            entite=entite, valeur=valeur, tolerance=tolerance
        )
        self.assertTrue(valseuil.__str__().rfind(str(valeur)) > -1)
        self.assertTrue(valseuil.__str__().rfind(str(tolerance)) > -1)

    # def test_fuzzy_mode_01(self):  # TODO
    #     """Fuzzy mode."""
    #     entite = sitehydro.Station('R533010110')
    #     descriptif = 'some texte here'
    #     publication = 9999
    #     e = seuil.seuil(
    #         entite=entite, contact=None, descriptif=descriptif,
    #         publication=publication, strict=False
    #     )
    #     self.assertEqual(
    #         (e.contact, e.publication), (None, publication)
    #     )

    def test_equality(self):
        """Test equality and inequality."""
        valeur = 8
        tolerance = 5
        entite = sitehydro.Station('R533010110')
        valseuil = Valeurseuil(
            entite=entite, valeur=valeur, tolerance=tolerance
        )
        other = Valeurseuil(
            entite=entite, valeur=valeur, tolerance=tolerance
        )
        self.assertEqual(valseuil, other)
        other = Valeurseuil(
            entite=entite, valeur=10, tolerance=tolerance
        )
        self.assertNotEqual(valseuil, other)

    def test_error_01(self):
        """Valeur error."""
        valeur = 8
        station = sitehydro.Station('A123456789')
        valseuil = Valeurseuil(valeur=valeur, entite=station)
        self.assertEqual(valseuil.valeur, valeur)
        self.assertRaises(
            TypeError,
            Valeurseuil,
            **{'valeur': None,
               'entite': station}
        )
        self.assertRaises(
            ValueError,
            Valeurseuil,
            **{'valeur': 'not a number'}
        )

    def test_entite(self):
        """Entite test"""
        valeur = 15.5
        smeteo = sitemeteo.Sitemeteo('123456789')
        entites = [sitehydro.Sitehydro('A1234567'),
                   sitehydro.Station('A123456789'),
                   sitehydro.Capteur('A12345678901'),
                   sitemeteo.Grandeur(typemesure='RR', sitemeteo=smeteo)]
        for entite in entites:
            Valeurseuil(valeur=valeur, entite=entite)
        for entite in [None, 'A1234567', smeteo]:
            with self.assertRaises(Exception):
                Valeurseuil(valeur=valeur, entite=entite)

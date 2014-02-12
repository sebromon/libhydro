# -*- coding: utf-8 -*-
"""Test program for seuil.

To run all tests just type:
    './test_core_seuil.py' or 'python test_core_seuil.py'

To run only a class test:
    python -m unittest test_core_seuil.TestClass

To run only a specific test:
    python -m unittest test_core_seuil.TestClass
    python -m unittest test_core_seuil.TestClass.test_method

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

import datetime
import unittest

from libhydro.core.seuil import Seuilhydro, Valeurseuil
from libhydro.core import sitehydro


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-02-12"""

#HISTORY
#V0.1 - 2014-02-12
#    first shot


#-- class Testseuilhydro ------------------------------------------------------
class Testseuilhydro(unittest.TestCase):

    """Seuilhydro class tests."""

    def test_base_01(self):
        """Minimum Seuilhydro."""
        seuil = Seuilhydro()
        self.assertEqual(
            (
                seuil.sitehydro, seuil.code, seuil.typeseuil,
                seuil.duree, seuil.nature, seuil.libelle,
                seuil.mnemo, seuil.gravite, seuil.commentaire,
                seuil.publication, seuil.valeurforcee,
                seuil.valeurs
            ),
            (
                None, 0, 1, 0, None, None, None, None, None,
                False, False, None
            )
        )

    def test_base_02(self):
        """Full Seuilhydro."""
        site = sitehydro.Sitehydro('R5330001')
        code = 175896
        typeseuil = 2
        duree = 25.8
        nature = 11
        libelle = 'Libellé du çeuil'
        mnemo = None
        gravite = 54
        commentaire = 'Ce seuil ne sera jamais dépassé'
        publication = True
        valeurforcee = True
        dtmaj = datetime.datetime.utcnow()
        valeurs = [
            Valeurseuil(10), Valeurseuil(11), Valeurseuil(12)
        ]
        seuil = Seuilhydro(
            sitehydro=site,
            code=code,
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
                seuil.sitehydro, seuil.code, seuil.typeseuil, seuil.duree,
                seuil.nature, seuil.libelle, seuil.mnemo, seuil.gravite,
                seuil.commentaire, seuil.publication, seuil.valeurforcee,
                seuil.dtmaj, seuil.valeurs
            ),
            (
                site, code, typeseuil, duree, nature, libelle, mnemo, gravite,
                commentaire, publication, valeurforcee, dtmaj, valeurs
            )
        )

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

    # def test_fuzzy_mode_01(self):
    #     """Fuzzy mode."""
    #     entite = sitehydro.Stationhydro('R533010110')
    #     descriptif = 'some texte here'
    #     publication = 9999
    #     e = seuil.seuil(
    #         entite=entite, contact=None, descriptif=descriptif,
    #         publication=publication, strict=False
    #     )
    #     self.assertEqual(
    #         (e.contact, e.publication), (None, publication)
    #     )

    def test_error_01(self):
        """Code error."""
        code = 175896
        seuil = Seuilhydro(code=code)
        self.assertEqual(seuil.code, code)
        self.assertRaises(
            TypeError,
            Seuilhydro,
            **{'code': None}
        )
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'code': 'not a integer'}
        )

    def test_error_02(self):
        """Typeseuil error."""
        typeseuil = 1
        seuil = Seuilhydro(typeseuil=typeseuil)
        self.assertEqual(seuil.typeseuil, typeseuil)
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'typeseuil': 'xxx'}
        )
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'typeseuil': 999}
            # **{'typeseuil': 1}
        )

    def test_error_03(self):
        """Duree error."""
        duree = 10.5
        seuil = Seuilhydro(duree=duree)
        self.assertEqual(seuil.duree, duree)
        self.assertRaises(
            TypeError,
            Seuilhydro,
            **{'duree': None}
        )
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'duree': 'not a integer'}
        )

    def test_error_04(self):
        """Nature error."""
        nature = 101
        seuil = Seuilhydro(nature=nature)
        self.assertEqual(seuil.nature, nature)
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'nature': 49}
        )

    def test_error_05(self):
        """Gravite error."""
        gravite = 100
        seuil = Seuilhydro(gravite=gravite)
        self.assertEqual(seuil.gravite, gravite)
        gravite = 0
        seuil = Seuilhydro(gravite=gravite)
        self.assertEqual(seuil.gravite, gravite)
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'gravite': 101}
        )
        self.assertRaises(
            ValueError,
            Seuilhydro,
            **{'gravite': -1}
        )


#-- class Testvaleurseuil -----------------------------------------------------
class Testvaleurseuil(unittest.TestCase):

    """Valeurseuil class tests."""

    def test_base_01(self):
        """Minimum Valeurseuil."""
        valseuil = Valeurseuil(33)
        self.assertEqual(valseuil.valeur, 33)

    def test_base_02(self):
        """Full Valeurseuil."""
        seuil = Seuilhydro(strict=False)
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

    def test_str_01(self):
        """Test __str__ method."""
        valeur = 8
        tolerance = 5
        entite = sitehydro.Stationhydro('R533010110')
        valseuil = Valeurseuil(
            entite=entite, valeur=valeur, tolerance=tolerance
        )
        self.assertTrue(valseuil.__str__().rfind(str(valeur)) > -1)
        self.assertTrue(valseuil.__str__().rfind(str(tolerance)) > -1)

    # def test_fuzzy_mode_01(self):  # TODO
    #     """Fuzzy mode."""
    #     entite = sitehydro.Stationhydro('R533010110')
    #     descriptif = 'some texte here'
    #     publication = 9999
    #     e = seuil.seuil(
    #         entite=entite, contact=None, descriptif=descriptif,
    #         publication=publication, strict=False
    #     )
    #     self.assertEqual(
    #         (e.contact, e.publication), (None, publication)
    #     )

    def test_error_01(self):
        """Valeur error."""
        valeur = 8
        valseuil = Valeurseuil(valeur=valeur)
        self.assertEqual(valseuil.valeur, valeur)
        self.assertRaises(
            TypeError,
            Valeurseuil,
            **{'valeur': None}
        )
        self.assertRaises(
            ValueError,
            Valeurseuil,
            **{'valeur': 'not a number'}
        )

#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

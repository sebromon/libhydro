# -*- coding: utf-8 -*-
"""Test program for sitemeteo.

To run all tests just type:
    python -m unittest test_core_sitemeteo

To run only a class test:
    python -m unittest test_core_sitemeteo.TestClass

To run only a specific test:
    python -m unittest test_core_sitemeteo.TestClass.test_method

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

from libhydro.core import sitemeteo
from libhydro.core import _composant as composant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-07-11"""

#HISTORY
#V0.1 - 2014-07-11
#    first shot


#-- class TestSitemeteo -------------------------------------------------------
class TestSitemeteo(unittest.TestCase):

    """Sitemeteo class tests."""

    def test_base_01(self):
        """Empty site."""
        # init
        code = '021301001'
        m = sitemeteo.Sitemeteo(code=code)
        # test
        self.assertEqual(
            (
                m.code, m.libelle, m.libelleusuel,
                m.coord, m.commune, m.grandeurs
            ),
            (code, None, None, None, None, [])
        )

    def test_base_02(self):
        """Site with 1 grandeur."""
        # init
        code = '033345510'
        libelle = 'MONTÉLIMAR'
        libelleusuel = 'Montélimar SPC'
        coord = (482000, 1897556.5, 26)
        commune = 32150
        grandeur = sitemeteo.Grandeurmeteo('RR')
        m = sitemeteo.Sitemeteo(
            code=code, libelle=libelle, libelleusuel=libelleusuel,
            coord=coord, commune=commune, grandeurs=grandeur
        )
        # test
        self.assertEqual(
            (
                m.code, m.libelle, m.libelleusuel,
                m.coord, m.commune, m.grandeurs
            ),
            (
                code, libelle, libelleusuel,
                composant.Coord(*coord), unicode(commune),
                [grandeur]
            )
        )

    def test_base_03(self):
        """Sitemeteo with n grandeurs."""
        # init
        code = '033345502'
        libelle = 'MONTÉLIMAR'
        libelleusuel = 'Montélimar SPC'
        coord = (482000, 1897556.5, 26)
        commune = 32150
        grandeurs = (
            sitemeteo.Grandeurmeteo('RR'),
            sitemeteo.Grandeurmeteo('EP'),
            sitemeteo.Grandeurmeteo('DV'),
            sitemeteo.Grandeurmeteo('RR'),
        )
        m = sitemeteo.Sitemeteo(
            code=code, libelle=libelle, libelleusuel=libelleusuel,
            coord=coord, commune=commune, grandeurs=grandeurs
        )
        # test
        self.assertEqual(
            (
                m.code, m.libelle, m.libelleusuel,
                m.coord, m.commune, m.grandeurs
            ),
            (
                code, libelle, libelleusuel,
                composant.Coord(*coord), unicode(commune),
                list(grandeurs)
            )
        )

    def test_base_04(self):
        """Update some attributes."""
        # init
        code = '033345502'
        libelle = 'MONTÉLIMAR'
        libelleusuel = 'Montélimar SPC'
        coord = (482000, 1897556.5, 26)
        commune = 32150
        grandeurs = [
            sitemeteo.Grandeurmeteo('RR'),
            sitemeteo.Grandeurmeteo('EP'),
            sitemeteo.Grandeurmeteo('DV'),
            sitemeteo.Grandeurmeteo('RR'),
        ]
        m = sitemeteo.Sitemeteo(
            code=code, libelle=libelle, libelleusuel=libelleusuel,
            coord=coord, commune=commune, grandeurs=grandeurs
        )
        # test
        self.assertEqual(m.grandeurs, grandeurs)
        m.grandeurs = None
        self.assertEqual(m.grandeurs, [])
        m.grandeurs = grandeurs[0]
        self.assertEqual(m.grandeurs, [grandeurs[0]])
        m.grandeurs = grandeurs
        self.assertEqual(m.grandeurs, grandeurs)
        self.assertEqual(m.coord, composant.Coord(*coord))
        m.coord = (10, 20, 25)
        m.coord = composant.Coord(*coord)
        self.assertEqual(m.commune, unicode(commune))
        m.commune = 32150
        m.commune = None

    def test_str_01(self):
        """Test __str__ method with None values."""
        m = sitemeteo.Sitemeteo(code=0, strict=False)
        self.assertTrue(m.__str__().rfind('Sitemeteo') > -1)

    def test_str_02(self):
        """Test __str__ with unicode."""
        m = sitemeteo.Sitemeteo(code='044553301')
        m.libelle = 'ℓα gαяσηηє à тσυℓσυѕє'
        m.__unicode__()
        m.__str__()

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test with None values."""
        code = 1
        grandeurs = ['rouge', 'vert']
        m = sitemeteo.Sitemeteo(code=code,  grandeurs=grandeurs, strict=False)
        self.assertEqual(
            (m.code, m.grandeurs),
            (unicode(code), grandeurs)
        )

    def test_error_01(self):
        """Code error."""
        code = '044011221'
        sitemeteo.Sitemeteo(**{'code': code})
        self.assertRaises(
            TypeError,
            sitemeteo.Sitemeteo,
            **{'code': None}
        )
        self.assertRaises(
            ValueError,
            sitemeteo.Sitemeteo,
            **{'code': '%s1' % code}
        )
        self.assertRaises(
            ValueError,
            sitemeteo.Sitemeteo,
            **{'code': code[:-1]}
        )

    def test_error_02(self):
        """Coord error."""
        code = '044011221'
        coord = (33022, 5846, 26)
        sitemeteo.Sitemeteo(**{'code': code, 'coord': coord})
        self.assertRaises(
            TypeError,
            sitemeteo.Sitemeteo,
            **{'code': code, 'coord': coord[0]}
        )

    def test_error_03(self):
        """Commune error."""
        code = '044011221'
        commune = '33022'
        sitemeteo.Sitemeteo(**{'code': code, 'commune': commune})
        self.assertRaises(
            ValueError,
            sitemeteo.Sitemeteo,
            **{'code': code, 'commune': commune[:-1]}
        )
        self.assertRaises(
            ValueError,
            sitemeteo.Sitemeteo,
            **{'code': code, 'commune': '%s1' % commune}
        )

    def test_error_04(self):
        """Grandeurs error."""
        code = '023510101'
        grandeurs = (
            sitemeteo.Grandeurmeteo('RR'),
            sitemeteo.Grandeurmeteo('EP'),
        )
        sitemeteo.Sitemeteo(
            **{
                'code': code,
                'grandeurs': grandeurs
            }
        )
        self.assertRaises(
            TypeError,
            sitemeteo.Sitemeteo,
            **{'code': code, 'grandeurs': ['I am not a troncon']}
        )


#-- class TestGrandeurmeteo ---------------------------------------------------
class TestGrandeurmeteo(unittest.TestCase):

    """Grandeurmeteo class tests."""

    def test_base(self):
    # def test_base_01(self):
        """Base case test."""
        typegrandeur = 'EP'
        g = sitemeteo.Grandeurmeteo(typegrandeur=typegrandeur)
        self.assertEqual(g.typegrandeur, typegrandeur)

    def test_str(self):
        """Test __str__ method with None values."""
        g = sitemeteo.Grandeurmeteo(typegrandeur='', strict=False)
        self.assertTrue(g.__str__().rfind('Grandeurmeteo') > -1)
        g = sitemeteo.Grandeurmeteo(typegrandeur=None, strict=False)
        self.assertTrue(g.__str__().rfind('Grandeurmeteo') > -1)

    def test_fuzzy_mode(self):
        """Fuzzy mode test."""
        typegrandeur = 'a fake one'
        g = sitemeteo.Grandeurmeteo(typegrandeur=typegrandeur, strict=False)
        self.assertEqual(g.typegrandeur, typegrandeur)

    def test_error(self):
    # def test_error_01(self):
        """Typegrandeur error."""
        g = sitemeteo.Grandeurmeteo(**{'typegrandeur': 'RR'})
        self.assertRaises(
            ValueError,
            g.__setattr__,
            *('typegrandeur', None)
        )
        self.assertRaises(
            ValueError,
            g.__setattr__,
            *('typegrandeur', 'xxxx')
        )

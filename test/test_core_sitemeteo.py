# coding: utf-8
"""Test program for sitemeteo.

To run all tests just type:
    python -m unittest test_core_sitemeteo

To run only a class test:
    python -m unittest test_core_sitemeteo.TestClass

To run only a specific test:
    python -m unittest test_core_sitemeteo.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import unittest

from libhydro.core import sitemeteo
from libhydro.core import _composant_site as composant_site


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1d"""
__date__ = """2014-08-01"""

# HISTORY
# V0.1 - 2014-07-11
#   first shot


# -- class TestSitemeteo ------------------------------------------------------
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
        # same with 8 chars code
        shortcode = '21301001'
        m = sitemeteo.Sitemeteo(code=shortcode)
        self.assertEqual(m.code, code)

    def test_base_02(self):
        """Site with 1 grandeur."""
        # init
        code = '033345510'
        libelle = 'MONTÉLIMAR'
        libelleusuel = 'Montélimar SPC'
        coord = (482000, 1897556.5, 26)
        commune = 32150
        grandeur = sitemeteo.Grandeur('RR')
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
                composant_site.Coord(*coord), str(commune),
                [grandeur]
            )
        )
        grandeur.sitemeteo = m
        self.assertEqual(grandeur.sitemeteo, m)

    def test_base_03(self):
        """Sitemeteo with n grandeurs."""
        # init
        code = '033345502'
        libelle = 'MONTÉLIMAR'
        libelleusuel = 'Montélimar SPC'
        coord = (482000, 1897556.5, 26)
        commune = 32150
        grandeurs = (
            sitemeteo.Grandeur('RR'),
            sitemeteo.Grandeur('EP'),
            sitemeteo.Grandeur('DV'),
            sitemeteo.Grandeur('RR'),
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
                composant_site.Coord(*coord), str(commune),
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
            sitemeteo.Grandeur('RR'),
            sitemeteo.Grandeur('EP'),
            sitemeteo.Grandeur('DV'),
            sitemeteo.Grandeur('RR'),
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
        self.assertEqual(m.coord, composant_site.Coord(*coord))
        m.coord = (10, 20, 25)
        m.coord = composant_site.Coord(*coord)
        self.assertEqual(m.commune, str(commune))
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
            (str(code), grandeurs)
        )

    def test_error_01(self):
        """Code error."""
        code = '044011221'
        sitemeteo.Sitemeteo(code=code)
        with self.assertRaises(TypeError):
            sitemeteo.Sitemeteo(code=None)
        with self.assertRaises(ValueError):
            sitemeteo.Sitemeteo(code='%s1' % code)
        with self.assertRaises(ValueError):
            sitemeteo.Sitemeteo(code=code[:-2])

    def test_error_02(self):
        """Coord error."""
        code = '044011221'
        coord = (33022, 5846, 26)
        sitemeteo.Sitemeteo(code=code, coord=coord)
        with self.assertRaises(TypeError):
            sitemeteo.Sitemeteo(code=code, coord=coord[0])

    def test_error_03(self):
        """Commune error."""
        code = '044011221'
        commune = '33022'
        sitemeteo.Sitemeteo(code=code, commune=commune)
        with self.assertRaises(ValueError):
            sitemeteo.Sitemeteo(code=code, commune=commune[:-1])
        with self.assertRaises(ValueError):
            sitemeteo.Sitemeteo(code=code, commune='%s1' % commune)

    def test_error_04(self):
        """Grandeurs error."""
        code = '023510101'
        grandeurs = (
            sitemeteo.Grandeur('RR'),
            sitemeteo.Grandeur('EP'),
        )
        sitemeteo.Sitemeteo(
            code=code,
            grandeurs=grandeurs
        )
        with self.assertRaises(TypeError):
            sitemeteo.Sitemeteo(code=code, grandeurs=['I am not a troncon'])


# -- class TestGrandeur -------------------------------------------------------
class TestGrandeur(unittest.TestCase):

    """Grandeur class tests."""

    def test_base_01(self):
        """Base case test."""
        codeinsee = '013008110'
        s = sitemeteo.Sitemeteo(codeinsee)
        typemesure = 'EP'
        g = sitemeteo.Grandeur(
            typemesure=typemesure,
            sitemeteo=s
        )
        self.assertEqual(g.typemesure, typemesure)
        self.assertEqual(g.sitemeteo.code, codeinsee)
        self.assertIsNone(g.pdt)

    def test_base_02(self):
        """Test pdt"""
        codeinsee = '013008110'
        s = sitemeteo.Sitemeteo(codeinsee)
        typemesure = 'RR'
        pdt = 5
        g = sitemeteo.Grandeur(
            typemesure=typemesure,
            sitemeteo=s,
            pdt=pdt
        )
        self.assertEqual(g.typemesure, typemesure)
        self.assertEqual(g.sitemeteo.code, codeinsee)
        self.assertEqual(g.pdt, pdt)

    def test_str(self):
        """Test __str__ method with None values."""
        g = sitemeteo.Grandeur(typemesure='', strict=False)
        self.assertTrue(g.__str__().rfind('Grandeur') > -1)
        g = sitemeteo.Grandeur(typemesure=None, strict=False)
        self.assertTrue(g.__str__().rfind('Grandeur') > -1)

    def test_fuzzy_mode(self):
        """Fuzzy mode test."""
        typemesure = 'a fake one'
        site = 'anything can fit in fuzzy mode!'
        g = sitemeteo.Grandeur(
            typemesure=typemesure,
            sitemeteo=site,
            strict=False
        )
        self.assertEqual(g.typemesure, typemesure)
        self.assertEqual(g.sitemeteo, site)

    def test_error_01(self):
        """typemesure error."""
        g = sitemeteo.Grandeur(typemesure='RR')
        with self.assertRaises(ValueError):
            g.__setattr__('typemesure', None)
        with self.assertRaises(ValueError):
            g.__setattr__('typemesure', 'xxxx')

    def test_error_02(self):
        """Sitemeteo error."""
        s = sitemeteo.Sitemeteo('266012001')
        g = sitemeteo.Grandeur(
            typemesure='RR',
            sitemeteo=s
        )
        with self.assertRaises(TypeError):
            g.__setattr__('sitemeteo', 'junk site !')


# -- class TestSitemeteoPondere --------------------------------------------
class TestSitemeteoPondere(unittest.TestCase):
    """SitemeteoPondere class tests."""

    def test_01(self):
        """ Test simple SitemeteoPondere"""
        code = '987654321'
        ponderation = 0.54
        sitepondere = sitemeteo.SitemeteoPondere(
            code=code, ponderation=ponderation)
        self.assertEqual((sitepondere.code, sitepondere.ponderation),
                         (code, ponderation))

    def test_sitemeteo(self):
        """Test property sitemeteo"""
        code = '987654321'
        ponderation = 0.54
        sitemeteo.SitemeteoPondere(code=code,
                                   ponderation=ponderation)

        for code in [None, '1245']:
            with self.assertRaises(Exception):
                sitemeteo.SitemeteoPondere(
                    code=code, ponderation=ponderation)

    def test_ponderation(self):
        """Test property ponderation"""
        code = '987654321'
        ponderation = 0.54
        sitemeteo.SitemeteoPondere(code=code,
                                   ponderation=ponderation)

        for ponderation in ['toto', None]:
            with self.assertRaises(TypeError):
                sitemeteo.SitemeteoPondere(
                    code=code, ponderation=ponderation)

    def test_str(self):
        """Test representation"""
        code = '987654321'
        ponderation = '0.54'
        site_pond = sitemeteo.SitemeteoPondere(code=code,
                                               ponderation=ponderation)
        site_str = site_pond.__str__()
        self.assertTrue(site_str.find(code) != -1)
        self.assertTrue(site_str.find(ponderation) != -1)

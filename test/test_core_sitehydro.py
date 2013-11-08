# -*- coding: utf-8 -*-
"""Test program for sitehydro.

To run all tests just type:
    './test_core_sitehydro.py' or 'python test_core_sitehydro.py'

To run only a class test:
    python -m unittest test_core_sitehydro.TestClass

To run only a specific test:
    python -m unittest test_core_sitehydro.TestClass
    python -m unittest test_core_sitehydro.TestClass.test_method

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

from libhydro.core import sitehydro
from libhydro.core import composant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1g"""
__date__ = """2013-11-07"""

#HISTORY
#V0.1 - 2013-07-15
#    first shot


#-- class TestSitehydro -------------------------------------------------------
class TestSitehydro(unittest.TestCase):

    """Sitehydro class tests."""

    # def setUp(self):
    # """Hook method for setting up the test fixture before exercising it."""
    # pass

    # def tearDown(self):
    # """Hook method for deconstructing the test fixture after testing it."""
    # pass

    def test_base_01(self):
        """Empty site."""
        code = 'R5330101'
        s = sitehydro.Sitehydro(code=code)
        self.assertEqual(
            (s.code, s.typesite, s.libelle, s.codeh2, s.stations, s.communes),
            (code, 'REEL', None, None, [], [])
        )

    def test_base_02(self):
        """Site with 1 station."""
        code = 'A3334550'
        codeh2 = 'A3334550'
        typesite = 'MAREGRAPHE'
        libelle = 'La Saône [apres la crue] a Montelimar'
        coord = (482000, 1897556.5, 26)
        stations = sitehydro.Stationhydro(
            code='%s01' % code, typestation='LIMNI'
        )
        communes = 32150
        s = sitehydro.Sitehydro(
            code=code, codeh2=codeh2, typesite=typesite, libelle=libelle,
            coord=coord, stations=stations, communes=communes
        )

        self.assertEqual(
            (
                s.code, s.codeh2, s.typesite, s.libelle, s.coord,
                s.stations, s.communes
            ),
            (
                code, codeh2, typesite, libelle, composant.Coord(*coord),
                [stations], [unicode(communes)]
            )
        )

    def test_base_03(self):
        """Site with n station."""
        code = 'A3334550'
        typesite = 'REEL'
        libelle = 'La Saône [apres la crue] a Montelimar [hé oui]'
        coord = {'x': 482000, 'y': 1897556.5, 'proj': 26}
        stations = (
            sitehydro.Stationhydro(
                code='%s01' % code, typestation='DEB'
            ),
            sitehydro.Stationhydro(
                code='%s02' % code, typestation='LIMNIMERE'
            ),
            sitehydro.Stationhydro(
                code='%s03' % code, typestation='LIMNIFILLE'
            )
        )
        communes = [32150, 31100]
        s = sitehydro.Sitehydro(
            code=code, typesite=typesite, libelle=libelle,
            coord=coord, stations=stations, communes=communes
        )
        self.assertEqual(
            (
                s.code, s.typesite, s.libelle, s.coord,
                s.stations, s.communes
            ),
            (
                code, typesite, libelle, composant.Coord(**coord),
                [st for st in stations],
                [unicode(commune) for commune in communes]
            )
        )

    def test_base_04(self):
        """Update stations attribute."""
        code = 'A3334550'
        typesite = 'REEL'
        libelle = 'La Saône [apres la crue] a Montelimar [hé oui]'
        coord = composant.Coord(**{'x': 482000, 'y': 1897556.5, 'proj': 26})
        stations = [
            sitehydro.Stationhydro(code='%s01' % code, typestation='DEB')
        ]
        s = sitehydro.Sitehydro(
            code=code, typesite=typesite, libelle=libelle,
            coord=coord, stations=stations
        )
        self.assertEqual(s.stations, stations)
        s.stations = None
        self.assertEqual(s.stations, [])
        s.stations = stations[0]
        self.assertEqual(s.stations, stations)
        s.stations = stations
        self.assertEqual(s.stations, stations)
        self.assertEqual(s.coord, coord)
        self.assertEqual(s.communes, [])
        s.communes = 32150
        s.communes = '2B810'
        s.communes = ['2A001', 33810, 44056, '2B033']
        s.communes = None

    def test_str_01(self):
        """Test __str__ method with None values."""
        s = sitehydro.Sitehydro(code=0, strict=False)
        self.assertTrue(s.__str__().rfind('Site') > -1)

    @unittest.skipIf(
        (sys.stdout.encoding == 'cp850'),
        "windows console can't deal with these characters"
    )
    def test_str_02(self):
        """Test __str__ with unicode."""
        s = sitehydro.Sitehydro(code='A0445533')
        s.libelle = 'ℓα gαяσηηє à тσυℓσυѕє'
        s.__unicode__()
        s.__str__()

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test with None values."""
        code = stations = None
        s = sitehydro.Sitehydro(
            code=code,  stations=stations, strict=False
        )
        self.assertEqual(
            (s.typesite, s.code, s.stations),
            ('REEL', code, [])
        )

    def test_fuzzy_mode_02(self):
        """Fuzzy mode test."""
        code = '3'
        typesite = '6'
        stations = [1, 2, 3]
        s = sitehydro.Sitehydro(
            typesite=typesite, code=code,  stations=stations, strict=False
        )
        self.assertEqual(
            (s.typesite, s.code, s.stations),
            (typesite, code, stations)
        )

    def test_error_01(self):
        """Typesite error."""
        code = 'H0001010'
        s = sitehydro.Sitehydro(**{'code': code, 'typesite': 'REEL'})
        self.assertRaises(
            TypeError,
            s.__setattr__,
            *('typesite', None)
        )
        self.assertRaises(
            ValueError,
            sitehydro.Sitehydro,
            **{'code': code, 'typesite': 'REEEL'}
        )

    def test_error_02(self):
        """Code error."""
        code = 'B4401122'
        sitehydro.Sitehydro(**{'code': code})
        self.assertRaises(
            TypeError,
            sitehydro.Sitehydro,
            **{'code': None}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Sitehydro,
            **{'code': '%s01' % code}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Sitehydro,
            **{'code': code[:-1]}
        )

    def test_error_03(self):
        """Code hydro2 error."""
        code = 'B4401122'
        sitehydro.Sitehydro(**{'code': code, 'codeh2': code})
        self.assertRaises(
            ValueError,
            sitehydro.Sitehydro,
            **{'code': code, 'codeh2': '{}01'.format(code)}
        )

    def test_error_04(self):
        """Station error."""
        code = 'B4401122'
        stations = (
            sitehydro.Stationhydro(code='%s01' % code),
            sitehydro.Stationhydro(code='%s02' % code)
        )
        sitehydro.Sitehydro(**{'code': code, 'stations': stations})
        self.assertRaises(
            TypeError,
            sitehydro.Sitehydro,
            **{'code': code, 'stations': ['station']}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Sitehydro,
            **{'code': code, 'typesite': 'PONCTUEL', 'stations': stations}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Sitehydro,
            **{'code': code, 'typesite': 'FICTIF', 'stations': stations}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Sitehydro,
            **{'code': code, 'typesite': 'VIRTUEL', 'stations': stations}
        )

    def test_error_05(self):
        """Coord error."""
        code = 'B4401122'
        coord = (33022, 5846, 26)
        sitehydro.Sitehydro(**{'code': code, 'coord': coord})
        self.assertRaises(
            TypeError,
            sitehydro.Sitehydro,
            **{'code': code, 'coord': coord[0]}
        )


#-- class TestStationhydro ----------------------------------------------------
class TestStationhydro(unittest.TestCase):

    """Stationhydro class tests."""

    # def setUp(self):
    # """Hook method for setting up the test fixture before exercising it."""
    # pass

    # def tearDown(self):
    # """Hook method for deconstructing the test fixture after testing it."""
    # pass

    def test_base_01(self):
        """Base case with empty station."""
        code = 'O033401101'
        s = sitehydro.Stationhydro(code=code)
        self.assertEqual(
            (s.code, s.typestation, s.libelle, s.commune),
            (code, 'LIMNI', None, None)
        )

    def test_base_02(self):
        """Base case test."""
        code = 'A033465001'
        typestation = 'LIMNI'
        libelle = 'La Seine a Paris - rive droite'
        capteurs = [sitehydro.Capteur(code='V83310100101')]
        commune = '03150'
        s = sitehydro.Stationhydro(
            code=code, typestation=typestation, libelle=libelle,
            capteurs=capteurs, commune=commune
        )
        self.assertEqual(
            (s.code, s.typestation, s.libelle, s.capteurs, s.commune),
            (code, typestation, libelle, capteurs, commune)
        )

    def test_base_03(self):
        """Update capteurs attribute."""
        code = 'A033465001'
        typestation = 'LIMNI'
        libelle = 'La Seine a Paris - rive droite'
        capteurs = [sitehydro.Capteur(code='V83310100101')]
        commune = '2B201'
        s = sitehydro.Stationhydro(
            code=code, typestation=typestation, libelle=libelle,
            capteurs=capteurs, commune=commune
        )
        self.assertEqual(
            (s.code, s.typestation, s.libelle, s.commune),
            (code, typestation, libelle, commune)
        )
        s.capteurs = None
        self.assertEqual(s.capteurs, [])
        s.capteurs = capteurs[0]
        self.assertEqual(s.capteurs, capteurs)
        s.capteurs = capteurs
        self.assertEqual(s.capteurs, capteurs)

    def test_str_01(self):
        """Test __str__ method with None values."""
        s = sitehydro.Stationhydro(code=0, strict=False)
        self.assertTrue(s.__str__().rfind('Station') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        code = '3'
        typestation = '6'
        s = sitehydro.Stationhydro(
            code=code, typestation=typestation, strict=False
        )
        self.assertEqual(
            (s.code, s.typestation),
            (code, typestation)
        )

    def test_error_01(self):
        """Typestation error."""
        code = 'A033465001'
        s = sitehydro.Stationhydro(**{'code': code, 'typestation': 'LIMNI'})
        self.assertRaises(
            TypeError,
            s.__setattr__,
            *('typestation', None)
        )
        self.assertRaises(
            TypeError,
            sitehydro.Stationhydro,
            **{'code': None}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Stationhydro,
            **{'code': code, 'typestation': 'LIMMMMNI'}
        )

    def test_error_02(self):
        """Code error."""
        code = 'B440112201'
        sitehydro.Stationhydro(**{'code': code})
        self.assertRaises(
            ValueError,
            sitehydro.Stationhydro,
            **{'code': code[:-1]}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Stationhydro,
            **{'code': '%s0' % code}
        )

    def test_error_03(self):
        """Capteur error."""
        code = 'B440112201'
        capteurs = (
            sitehydro.Capteur(code='%s01' % code, typemesure='Q'),
            sitehydro.Capteur(code='%s02' % code, typemesure='H'),
        )
        sitehydro.Stationhydro(**{
            'code': code, 'typestation': 'DEB', 'capteurs': capteurs
        })
        self.assertRaises(
            TypeError,
            sitehydro.Stationhydro,
            **{'code': code, 'capteurs': 'c'}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Stationhydro,
            **{'code': code, 'capteurs': capteurs}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Stationhydro,
            **{'code': code, 'typestation': 'LIMNI', 'capteurs': capteurs}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Stationhydro,
            **{'code': code, 'typestation': 'HC', 'capteurs': capteurs}
        )


#-- class TestCapteur ----------------------------------------------------
class TestCapteur(unittest.TestCase):

    """Capteur class tests."""

    # def setUp(self):
    # """Hook method for setting up the test fixture before exercising it."""
    # pass

    # def tearDown(self):
    # """Hook method for deconstructing the test fixture after testing it."""
    # pass

    def test_base_01(self):
        """Base case with empty capteur."""
        code = 'V83310100101'
        c = sitehydro.Capteur(code=code)
        self.assertEqual(
            (c.code, c.typemesure, c.libelle),
            (code, 'H', None)
        )

    def test_base_02(self):
        """Base case test."""
        typemesure = 'Q'
        code = 'A03346500101'
        libelle = 'Capteur de secours'
        c = sitehydro.Capteur(
            code=code, typemesure=typemesure, libelle=libelle
        )
        self.assertEqual(
            (c.code, c.typemesure, c.libelle),
            (code, typemesure, libelle)
        )

    def test_str_01(self):
        """Test __str__ method with None values."""
        c = sitehydro.Capteur(code=0, strict=False)
        self.assertTrue(c.__str__().rfind('Capteur') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        typemesure = 'RR'
        code = 'C1'
        c = sitehydro.Capteur(
            code=code, typemesure=typemesure, strict=False
        )
        self.assertEqual(
            (c.code, c.typemesure),
            (code, typemesure)
        )

    def test_error_01(self):
        """Typemesure error."""
        c = sitehydro.Capteur(**{'code': 'A14410010201', 'typemesure': 'H'})
        self.assertRaises(
            TypeError,
            c.__setattr__,
            *('typemesure', None)
        )
        self.assertRaises(
            ValueError,
            sitehydro.Capteur,
            **{'code': 'A14410010201', 'typemesure': 'RR'}
        )

    def test_error_02(self):
        """Code error."""
        sitehydro.Capteur(**{'code': 'B44011220101'})
        self.assertRaises(
            TypeError,
            sitehydro.Capteur,
            **{'code': None}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Capteur,
            **{'code': 'B440112201'}
        )
        self.assertRaises(
            ValueError,
            sitehydro.Capteur,
            **{'code': 'B4401122010133'}
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

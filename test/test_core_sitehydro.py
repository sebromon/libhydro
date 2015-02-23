# -*- coding: utf-8 -*-
"""Test program for sitehydro.

To run all tests just type:
    python -m unittest test_core_sitehydro

To run only a class test:
    python -m unittest test_core_sitehydro.TestClass

To run only a specific test:
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
from libhydro.core import _composant_site as composant_site


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2a"""
__date__ = """2014-12-17"""

#HISTORY
#V0.2 - 2014-12-17
#   replace Stationhydro with Station
#V0.1 - 2013-07-15
#    first shot


#-- class TestSitehydro -------------------------------------------------------
class TestSitehydro(unittest.TestCase):

    """Sitehydro class tests."""

    def test_base_01(self):
        """Empty site."""
        code = 'R5330101'
        s = sitehydro.Sitehydro(code=code)
        self.assertEqual(
            (
                s.code, s.codeh2, s.typesite, s.libelle, s.libelleusuel,
                s.stations, s.communes, s.tronconsvigilance
            ),
            (code, None, 'REEL', None, None, [], [], [])
        )

    def test_base_02(self):
        """Site with 1 station."""
        code = 'A3334550'
        codeh2 = 'A3334550'
        typesite = 'MAREGRAPHE'
        libelle = 'La Saône [apres la crue] a Montélimar'
        libelleusuel = 'Montélimar'
        coord = (482000, 1897556.5, 26)
        station = sitehydro.Station(
            code='%s01' % code, typestation='LIMNI'
        )
        commune = 32150
        tronconvigilance = sitehydro.Tronconvigilance(
            code='AC1', libelle='La Liane'
        )
        s = sitehydro.Sitehydro(
            code=code, codeh2=codeh2, typesite=typesite,
            libelle=libelle, libelleusuel=libelleusuel,
            coord=coord, stations=station, communes=commune,
            tronconsvigilance=tronconvigilance
        )

        self.assertEqual(
            (
                s.code, s.codeh2, s.typesite, s.libelle, s.libelleusuel,
                s.coord, s.stations, s.communes, s.tronconsvigilance
            ),
            (
                code, codeh2, typesite, libelle, libelleusuel,
                composant_site.Coord(*coord), [station], [unicode(commune)],
                [tronconvigilance]
            )
        )

    def test_base_03(self):
        """Site with n station."""
        code = 'A3334550'
        typesite = 'REEL'
        libelle = 'La Saône [apres la crue] a Montelimar [hé oui]'
        coord = {'x': 482000, 'y': 1897556.5, 'proj': 26}
        stations = (
            sitehydro.Station(
                code='%s01' % code, typestation='DEB'
            ),
            sitehydro.Station(
                code='%s02' % code, typestation='LIMNIMERE'
            ),
            sitehydro.Station(
                code='%s03' % code, typestation='LIMNIFILLE'
            )
        )
        communes = [32150, 31100]
        tronconsvigilance = (
            sitehydro.Tronconvigilance(
                code='AC1', libelle='La Liane 1'
            ),
            sitehydro.Tronconvigilance(
                code='AC2', libelle='La Liane 2'
            ),
            sitehydro.Tronconvigilance(
                code='AC3', libelle='La Liane 3'
            )
        )
        s = sitehydro.Sitehydro(
            code=code, typesite=typesite, libelle=libelle,
            coord=coord, stations=stations, communes=communes,
            tronconsvigilance=tronconsvigilance
        )
        self.assertEqual(
            (
                s.code, s.typesite, s.libelle, s.coord,
                s.stations, s.communes, s.tronconsvigilance
            ),
            (
                code, typesite, libelle, composant_site.Coord(**coord),
                [st for st in stations],
                [unicode(commune) for commune in communes],
                [tronconvigilance for tronconvigilance in tronconsvigilance]
            )
        )

    def test_equality(self):
        """Equality test."""
        # strict mode
        code = 'O0334011'
        site = sitehydro.Sitehydro(code=code)
        other = sitehydro.Sitehydro(code=code)
        self.assertEqual(site, other)
        other.libelle = 'A label here...'
        self.assertNotEqual(site, other)
        # lazzy mode: None attributes are ignored
        self.assertTrue(site.__eq__(other, lazzy=True))
        # ignore some attrs
        other.libelle = None
        self.assertEqual(site, other)
        other.stations = sitehydro.Station('A456102001')
        self.assertNotEqual(site, other)
        self.assertTrue(site.__eq__(other, ignore=['stations']))

    def test_base_04(self):
        """Update some attributes."""
        code = 'A3334550'
        typesite = 'REEL'
        libelle = 'La Saône [apres la crue] a Montelimar [hé oui]'
        coord = composant_site.Coord(
            x=482000, y=1897556.5, proj=26
        )
        stations = [
            sitehydro.Station(code='%s01' % code, typestation='DEB')
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
        self.assertEqual(s.tronconsvigilance, [])
        t = sitehydro.Tronconvigilance(
            code='XX33',
            libelle='Le Târtémpion'
        )
        s.tronconsvigilance = t
        self.assertEqual(s.tronconsvigilance, [t])
        s.tronconsvigilance = (t, t, t)
        self.assertEqual(s.tronconsvigilance, [t, t, t])

    def test_str_01(self):
        """Test __str__ method with None values."""
        s = sitehydro.Sitehydro(code=0, strict=False)
        self.assertTrue(s.__str__().rfind('Site') > -1)

    def test_str_02(self):
        """Test __str__ with unicode."""
        s = sitehydro.Sitehydro(code='A0445533')
        s.libelle = 'ℓα gαяσηηє à тσυℓσυѕє'
        s.__unicode__()
        s.__str__()

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test with None values."""
        code = stations = None
        trv = ['tr1']
        s = sitehydro.Sitehydro(
            code=code,  stations=stations, tronconsvigilance=trv,
            strict=False
        )
        self.assertEqual(
            (s.typesite, s.code, s.stations, s.tronconsvigilance),
            ('REEL', code, [], trv)
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
        s = sitehydro.Sitehydro(code=code, typesite='REEL')
        with self.assertRaises(ValueError):
            s.__setattr__('typesite', None)
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(code=code, typesite='REEEL')

    def test_error_02(self):
        """Code error."""
        code = 'B4401122'
        sitehydro.Sitehydro(code=code)
        with self.assertRaises(TypeError):
            sitehydro.Sitehydro(code=None)
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(code='%s01' % code)
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(code=code[:-1])

    def test_error_03(self):
        """Code hydro2 error."""
        code = 'B4401122'
        sitehydro.Sitehydro(code=code, codeh2=code)
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(code=code, codeh2='{}01'.format(code))

    def test_error_04(self):
        """Station error."""
        code = 'B4401122'
        stations = (
            sitehydro.Station(code='%s01' % code),
            sitehydro.Station(code='%s02' % code)
        )
        sitehydro.Sitehydro(code=code, stations=stations)
        with self.assertRaises(TypeError):
            sitehydro.Sitehydro(code=code, stations=['station'])
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(
                code=code, typesite='PONCTUEL', stations=stations
            )
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(
                code=code, typesite='FICTIF', stations=stations
            )
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(
                code=code, typesite='VIRTUEL', stations=stations
            )

    def test_error_05(self):
        """Coord error."""
        code = 'B4401122'
        coord = (33022, 5846, 26)
        sitehydro.Sitehydro(code=code, coord=coord)
        with self.assertRaises(TypeError):
            sitehydro.Sitehydro(code=code, coord=coord[0])

    def test_error_06(self):
        """Tronconsvigilance error."""
        code = 'A2351010'
        sitehydro.Sitehydro(
            code=code,
            tronconsvigilance=sitehydro.Tronconvigilance()
        )
        with self.assertRaises(TypeError):
            sitehydro.Sitehydro(
                code=code, tronconsvigilance='I am not a troncon'
            )


#-- class TestStation ---------------------------------------------------------
class TestStation(unittest.TestCase):

    """Station class tests."""

    def test_base_01(self):
        """Base case with empty station."""
        code = 'O033401101'
        s = sitehydro.Station(code=code)
        self.assertEqual(
            (
                s.code, s.typestation, s.libelle, s.libellecomplement,
                s.commune, s.ddcs
            ),
            (code, 'LIMNI', None, None, None, [])
        )

    def test_base_02(self):
        """Base case test."""
        code = 'A033465001'
        typestation = 'LIMNI'
        libelle = 'La Seine a Paris - rive droite'
        libellecomplement = 'rive droite'
        capteurs = [sitehydro.Capteur(code='V83310100101')]
        commune = '03150'
        ddcs = 33  # a numeric rezo
        s = sitehydro.Station(
            code=code, typestation=typestation,
            libelle=libelle, libellecomplement=libellecomplement,
            capteurs=capteurs, commune=commune, ddcs=ddcs
        )
        self.assertEqual(
            (
                s.code, s.typestation, s.libelle, s.libellecomplement,
                s.capteurs, s.commune, s.ddcs
            ),
            (
                code, typestation, libelle, libellecomplement,
                capteurs, commune, [unicode(ddcs)]
            )
        )

    def test_base_03(self):
        """Update capteurs attribute."""
        code = 'A033465001'
        typestation = 'LIMNI'
        libelle = 'La Seine a Paris - rive droite'
        capteurs = [sitehydro.Capteur(code='V83310100101')]
        commune = '2B201'
        ddcs = ['33', 'the rezo']
        s = sitehydro.Station(
            code=code, typestation=typestation, libelle=libelle,
            capteurs=capteurs, commune=commune, ddcs=ddcs
        )
        self.assertEqual(
            (s.code, s.typestation, s.libelle, s.commune, s.ddcs),
            (code, typestation, libelle, commune, ddcs)
        )
        s.capteurs = None
        self.assertEqual(s.capteurs, [])
        s.capteurs = capteurs[0]
        self.assertEqual(s.capteurs, capteurs)
        s.capteurs = capteurs
        self.assertEqual(s.capteurs, capteurs)

    def test_equality(self):
        """Equality test."""
        # strict mode
        code = 'O033401101'
        station = sitehydro.Station(code=code)
        other = sitehydro.Station(code=code)
        self.assertEqual(station, other)
        other.libelle = 'A label here...'
        self.assertNotEqual(station, other)
        # lazzy mode: None attributes are ignored
        self.assertTrue(station.__eq__(other, lazzy=True))
        # ignore some attrs
        self.assertNotEqual(station, other)
        self.assertTrue(station.__eq__(other, ignore=['libelle']))

    def test_str_01(self):
        """Test __str__ method with None values."""
        s = sitehydro.Station(code=0, strict=False)
        self.assertTrue(s.__str__().rfind('Station') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        code = '3'
        typestation = '6'
        s = sitehydro.Station(
            code=code, typestation=typestation, strict=False
        )
        self.assertEqual(
            (s.code, s.typestation),
            (code, typestation)
        )

    def test_error_01(self):
        """Typestation error."""
        code = 'A033465001'
        s = sitehydro.Station(code=code, typestation='LIMNI')
        with self.assertRaises(ValueError):
            s.__setattr__('typestation', None)
        with self.assertRaises(TypeError):
            sitehydro.Station(code=None)
        with self.assertRaises(ValueError):
            sitehydro.Station(code=code, typestation='LIMMMMNI')

    def test_error_02(self):
        """Code error."""
        code = 'B440112201'
        sitehydro.Station(code=code)
        with self.assertRaises(ValueError):
            sitehydro.Station(code=code[:-1])
        with self.assertRaises(ValueError):
            sitehydro.Station(code='%s0' % code)

    def test_error_03(self):
        """Capteur error."""
        code = 'B440112201'
        capteurs = (
            sitehydro.Capteur(code='%s01' % code, typemesure='Q'),
            sitehydro.Capteur(code='%s02' % code, typemesure='H'),
        )
        sitehydro.Station(
            code=code, typestation='DEB', capteurs=capteurs
        )
        with self.assertRaises(TypeError):
            sitehydro.Station(code=code, capteurs='c')
        with self.assertRaises(ValueError):
            sitehydro.Station(code=code, capteurs=capteurs)
        with self.assertRaises(ValueError):
            sitehydro.Station(
                code=code, typestation='LIMNI', capteurs=capteurs
            )
        with self.assertRaises(ValueError):
            sitehydro.Station(
                code=code, typestation='HC', capteurs=capteurs
            )

    def test_error_05(self):
        """Disceau error."""
        code = 'B440112201'
        ddcs = 'code rezo'
        sitehydro.Station(code=code, ddcs=ddcs)
        with self.assertRaises(ValueError):
            sitehydro.Station(code=code, ddcs=ddcs * 2)


#-- class TestCapteur ----------------------------------------------------
class TestCapteur(unittest.TestCase):

    """Capteur class tests."""

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

    def test_equality(self):
        """Equality test."""
        # strict mode
        typemesure = 'Q'
        code = 'A03346500101'
        libelle = 'Capteur de secours'
        capteur = sitehydro.Capteur(
            code=code, typemesure=typemesure, libelle=libelle
        )
        other = sitehydro.Capteur(
            code=code, typemesure=typemesure, libelle=libelle
        )
        self.assertEqual(capteur, other)
        other.libelle = None
        self.assertNotEqual(capteur, other)
        # lazzy mode: None attributes are ignored
        self.assertTrue(capteur.__eq__(other, lazzy=True))

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
        c = sitehydro.Capteur(code='A14410010201', typemesure='H')
        with self.assertRaises(ValueError):
            c.__setattr__('typemesure', None)
        with self.assertRaises(ValueError):
            sitehydro.Capteur(code='A14410010201', typemesure='RR')

    def test_error_02(self):
        """Code error."""
        sitehydro.Capteur(code='B44011220101')
        with self.assertRaises(TypeError):
            sitehydro.Capteur(code=None)
        with self.assertRaises(ValueError):
            sitehydro.Capteur(code='B440112201')
        with self.assertRaises(ValueError):
            sitehydro.Capteur(code='B4401122010133')


#-- class TestTronconvigilance ------------------------------------------------
class TestTronconvigilance(unittest.TestCase):

    """Tronconvigilance class tests."""

    def test_base_01(self):
        """Base case with empty troncon."""
        t = sitehydro.Tronconvigilance()
        self.assertEqual(
            (t.code, t.libelle),
            (None, None)
        )

    def test_base_02(self):
        """Base case test."""
        code = 'LO18'
        libelle = 'Loire amont'
        t = sitehydro.Tronconvigilance(code=code, libelle=libelle)
        self.assertEqual(
            (t.code, t.libelle),
            (code, libelle)
        )

    def test_equality(self):
        """Equality test."""
        code = 'LO18'
        libelle = 'Loire amont'
        troncon = sitehydro.Tronconvigilance(code=code, libelle=libelle)
        other = sitehydro.Tronconvigilance(code=code, libelle=libelle)
        self.assertEqual(troncon, other)
        other.libelle = 'Seine'
        self.assertNotEqual(troncon, other)

    def test_str_01(self):
        """Test __str__ method with None values."""
        t = sitehydro.Tronconvigilance()
        self.assertTrue(t.__str__().rfind('Troncon') > -1)

    def test_str_02(self):
        """Test __str__ method."""
        code = 'LO18'
        libelle = 'Loire amont'
        t = sitehydro.Tronconvigilance(code=code, libelle=libelle)
        self.assertTrue(t.__str__().rfind('Troncon') > -1)

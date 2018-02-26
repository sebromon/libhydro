# coding: utf-8
"""Test program for courbetarage.

To run all tests just type:
    python -m unittest test_core_courbecorrection

To run only a class test:
    python -m unittest test_core_courbecorrection.TestClass

To run only a specific test:
    python -m unittest test_core_courbecorrection.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import unittest
from datetime import datetime

from libhydro.core.jaugeage import (HauteurJaugeage, Jaugeage)
import libhydro.core.sitehydro as _sitehydro

# -- strings ------------------------------------------------------------------
__version__ = '0.1'
__date__ = '2017-05-04'

# HISTORY
# V0.1 - SR - 2017-05-04
#   first shot


class TestHauteurJaugeage(unittest.TestCase):
    """PivotCT class tests."""

    def test_base_01(self):
        """Simple HauteurJaugeage"""
        station = _sitehydro.Station(code='O123456789')
        sysalti = 0
        coteretenue = 100.8
        hjaug = HauteurJaugeage(station=station, sysalti=sysalti,
                                coteretenue=coteretenue)
        self.assertEqual((hjaug.station, hjaug.sysalti, hjaug.coteretenue),
                         (station, sysalti, coteretenue))

    def test_base_02(self):
        """Full HauteurJaugeage"""
        station = _sitehydro.Station(code='O123456789')
        sysalti = 0
        coteretenue = 100.8
        cotedeb = 987.4
        cotefin = 1000.54
        denivele = 14.4
        distancestation = 456.12
        stationfille = _sitehydro.Station(code='A123456789')
        dtdeb_refalti = datetime(2015, 1, 5, 10, 14, 56)
        hjaug = HauteurJaugeage(station=station, sysalti=sysalti,
                                coteretenue=coteretenue, cotedeb=cotedeb,
                                cotefin=cotefin, denivele=denivele,
                                distancestation=distancestation,
                                stationfille=stationfille,
                                dtdeb_refalti=dtdeb_refalti)
        self.assertEqual(
            (hjaug.station, hjaug.sysalti, hjaug.coteretenue, hjaug.cotedeb,
             hjaug.cotefin, hjaug.denivele, hjaug.distancestation,
             hjaug.stationfille, hjaug.dtdeb_refalti),
            (station, sysalti, coteretenue, cotedeb, cotefin, denivele,
             distancestation, stationfille, dtdeb_refalti))

    def test_base_03(self):
        """check string conversion of properties"""
        station = _sitehydro.Station(code='O123456789')
        sysalti = '31'
        coteretenue = '100.8'
        cotedeb = '987.4'
        cotefin = '1000.54'
        denivele = '14.4'
        distancestation = '456.12'
        stationfille = _sitehydro.Station(code='A123456789')
        dtdeb_refalti = '2015-01-05T10:14:56'
        hjaug = HauteurJaugeage(station=station, sysalti=sysalti,
                                coteretenue=coteretenue, cotedeb=cotedeb,
                                cotefin=cotefin, denivele=denivele,
                                distancestation=distancestation,
                                stationfille=stationfille,
                                dtdeb_refalti=dtdeb_refalti)
        self.assertEqual(
            (hjaug.station, hjaug.sysalti, hjaug.coteretenue, hjaug.cotedeb,
             hjaug.cotefin, hjaug.denivele, hjaug.distancestation,
             hjaug.stationfille, hjaug.dtdeb_refalti),
            (station, int(sysalti), float(coteretenue), float(cotedeb),
             float(cotefin), float(denivele),
             float(distancestation), stationfille,
             datetime(2015, 1, 5, 10, 14, 56)))

    def test_cmp_01(self):
        """check __lt__ and __gt__ methods"""
        station = _sitehydro.Station(code='O123456789')
        coteretenue1 = 100.8
        coteretenue2 = 103.45
        hjaug1 = HauteurJaugeage(station=station, coteretenue=coteretenue1)
        hjaug2 = HauteurJaugeage(station=station, coteretenue=coteretenue2)

        self.assertTrue(hjaug1 < hjaug2)
        self.assertFalse(hjaug1 > hjaug2)

        hjaug2.coteretenue = 54.12
        self.assertTrue(hjaug1 > hjaug2)
        self.assertFalse(hjaug1 < hjaug2)

    def test_str_01(self):
        """check str"""
        codestation = 'O123456789'
        station = _sitehydro.Station(code=codestation)
        sysalti = 0
        coteretenue = 100.8
        hjaug = HauteurJaugeage(station=station, sysalti=sysalti,
                                coteretenue=coteretenue)
        hjaug_str = hjaug.__str__()
        self.assertTrue(hjaug_str.find(codestation) > -1)
        self.assertTrue(hjaug_str.find(str(coteretenue)) > -1)

    def test_str_02(self):
        """check str fuzzy mode"""
        codestation = 'O123456789'
        station = codestation
        coteretenue = 100.8
        hjaug = HauteurJaugeage(station=station, coteretenue=coteretenue,
                                strict=False)
        hjaug_str = hjaug.__str__()
        self.assertTrue(hjaug_str.find(codestation) > -1)
        self.assertTrue(hjaug_str.find(str(coteretenue)) > -1)

        hjaug = HauteurJaugeage(station=None, coteretenue=coteretenue,
                                strict=False)
        hjaug_str = hjaug.__str__()
        self.assertTrue(hjaug_str.find('<sans station>') > -1)

    def test_error_01(self):
        """station error"""
        station = _sitehydro.Station(code='O123456789')
        sysalti = 0
        coteretenue = 100.8
        HauteurJaugeage(station=station, sysalti=sysalti,
                        coteretenue=coteretenue)

        station = 'O123456789'
        with self.assertRaises(TypeError) as context:
            HauteurJaugeage(station=station, sysalti=sysalti,
                            coteretenue=coteretenue)
        self.assertEqual(str(context.exception),
                         'station is not a sitehydro.Station')

        station = None
        with self.assertRaises(TypeError) as context:
            HauteurJaugeage(station=station, sysalti=sysalti,
                            coteretenue=coteretenue)
        self.assertEqual(str(context.exception),
                         'station is required')

    def test_error_02(self):
        """sysalti error"""
        station = _sitehydro.Station(code='O123456789')
        sysalti = 0
        coteretenue = 100.8
        HauteurJaugeage(station=station, sysalti=sysalti,
                        coteretenue=coteretenue)

        sysalti = 'AA'
        with self.assertRaises(ValueError):
            HauteurJaugeage(station=station, sysalti=sysalti,
                            coteretenue=coteretenue)

        sysalti = None
        with self.assertRaises(ValueError):
            HauteurJaugeage(station=station, sysalti=sysalti,
                            coteretenue=coteretenue)

        sysalti = 999
        with self.assertRaises(ValueError):
            HauteurJaugeage(station=station, sysalti=sysalti,
                            coteretenue=coteretenue)

    def test_error_03(self):
        """coteretenue error"""
        station = _sitehydro.Station(code='O123456789')
        sysalti = 0
        coteretenue = 100.8
        HauteurJaugeage(station=station, sysalti=sysalti,
                        coteretenue=coteretenue)

        coteretenue = None
        with self.assertRaises(ValueError) as context:
            HauteurJaugeage(station=station, sysalti=sysalti,
                            coteretenue=coteretenue)
        self.assertEqual(str(context.exception),
                         'coteretenue is required')

        coteretenue = 'AA'
        with self.assertRaises(ValueError):
            HauteurJaugeage(station=station, sysalti=sysalti,
                            coteretenue=coteretenue)

    def test_error_04(self):
        """cotedeb cotefin denivelle distancestation error"""
        properties_to_check = ['cotedeb', 'cotefin',
                               'denivele', 'distancestation']

        for prop in properties_to_check:
            args = {}
            args['station'] = _sitehydro.Station(code='O123456789')
            args['sysalti'] = 0
            args['coteretenue'] = 100.8
            args[prop] = 105.45
            HauteurJaugeage(**args)
            args[prop] = 'AB'
            with self.assertRaises(ValueError):
                HauteurJaugeage(**args)

    def test_error_05(self):
        """stationfille check"""
        args = {}
        args['station'] = _sitehydro.Station(code='O123456789')
        args['sysalti'] = 0
        args['coteretenue'] = 100.8
        args['stationfille'] = _sitehydro.Station(code='A123456789')
        HauteurJaugeage(**args)
        args['stationfille'] = 'A123456789'
        with self.assertRaises(TypeError) as context:
            HauteurJaugeage(**args)
        self.assertEqual(str(context.exception),
                         'stationfille is not a sitehydro.Station')

    def test_error_06(self):
        """dtdeb_refalti error"""
        args = {}
        args['station'] = _sitehydro.Station(code='O123456789')
        args['sysalti'] = 0
        args['coteretenue'] = 100.8
        args['dtdeb_refalti'] = datetime(2015, 1, 17, 14, 15, 19)
        HauteurJaugeage(**args)
        args['dtdeb_refalti'] = 'AA'
        with self.assertRaises(ValueError) as context:
            HauteurJaugeage(**args)
        self.assertEqual(str(context.exception),
                         'could not convert object to datetime.datetime')


class TestJaugeage(unittest.TestCase):
    """Jaugeage class tests."""

    def test_base_01(self):
        """simple jaugeage"""
        code = '156'
        site = _sitehydro.Sitehydro(code='O1234567')
        jaug = Jaugeage(code=code, site=site)
        self.assertEqual((jaug.code, jaug.site),
                         (code, site))

    def test_base_02(self):
        """full jaugeage"""
        # un jaugeage
        station = _sitehydro.Station(code='O123456789')
        sysalti = 0
        coteretenue = 100.8
        hjaug = HauteurJaugeage(station=station, sysalti=sysalti,
                                coteretenue=coteretenue)

        code = '156'
        dte = datetime(2017, 6, 30, 16, 35, 43)
        debit = 10556.12
        dtdeb = datetime(2017, 6, 29, 14, 29, 35)
        dtfin = datetime(2017, 6, 29, 15, 42, 31)
        section_mouillee = 1478.25
        perimetre_mouille = 9854.12
        largeur_miroir = 841.21
        mode = 10
        commentaire = 'un jaugeage'
        vitessemoy = 16.45
        vitessemax = 19.87
        vitessemoy_surface = 17.14
        site = _sitehydro.Sitehydro(code='O1234567')
        hauteurs = [hjaug]

        dtmaj = datetime(2017, 6, 30, 16, 37, 10)
        jaug = Jaugeage(code=code, dte=dte, debit=debit, dtdeb=dtdeb,
                        dtfin=dtfin, section_mouillee=section_mouillee,
                        perimetre_mouille=perimetre_mouille,
                        largeur_miroir=largeur_miroir,
                        mode=mode, commentaire=commentaire,
                        vitessemoy=vitessemoy, vitessemax=vitessemax,
                        vitessemoy_surface=vitessemoy_surface, site=site,
                        hauteurs=hauteurs, dtmaj=dtmaj)
        self.assertEqual(
            (jaug.code, jaug.dte, jaug.debit, jaug.dtdeb, jaug.dtfin,
             jaug.section_mouillee, jaug.perimetre_mouille,
             jaug.largeur_miroir, jaug.mode, jaug.commentaire, jaug.vitessemoy,
             jaug.vitessemax, jaug.vitessemoy_surface, jaug.site,
             jaug.hauteurs, jaug.dtmaj),
            (code, dte, debit, dtdeb, dtfin, section_mouillee,
             perimetre_mouille, largeur_miroir, mode, commentaire, vitessemoy,
             vitessemax, vitessemoy_surface, site, hauteurs, dtmaj)
            )

    def test_base_04(self):
        """check hauteurs"""
        # make hauteur
        station = _sitehydro.Station(code='O123456789')
        sysalti = 0
        coteretenue1 = 100.8
        coteretenue2 = 106.42
        hjaug1 = HauteurJaugeage(station=station, sysalti=sysalti,
                                 coteretenue=coteretenue1)
        hjaug2 = HauteurJaugeage(station=station, sysalti=sysalti,
                                 coteretenue=coteretenue2)

        code = '156'
        site = _sitehydro.Sitehydro(code='O1234567')

        hauteurs = None
        jaug = Jaugeage(code=code, site=site, hauteurs=hauteurs)
        self.assertEqual(jaug.hauteurs, [])

        hauteurs = []
        jaug = Jaugeage(code=code, site=site, hauteurs=hauteurs)
        self.assertEqual(jaug.hauteurs, [])

        hauteurs = hjaug1
        jaug = Jaugeage(code=code, site=site, hauteurs=hauteurs)
        self.assertEqual(jaug.hauteurs, [hjaug1])

        hauteurs = [hjaug1, hjaug2]
        jaug = Jaugeage(code=code, site=site, hauteurs=hauteurs)
        self.assertEqual(jaug.hauteurs, hauteurs)

    def test_fuzzy_01(self):
        """fuzzy mode"""
        code = '875'
        site = 'O1234567'
        hauteurs = [100.45, 100.86, 101.54]
        jaug = Jaugeage(code=code, site=site, hauteurs=hauteurs, strict=False)
        self.assertEqual((jaug.code, jaug.site, jaug.hauteurs),
                         (code, site, hauteurs))

    def test_sorting_01(self):
        """check sorting hauteurs"""
        station = _sitehydro.Station(code='O123456789')
        sysalti = 0
        coteretenue1 = 159.81
        coteretenue2 = 106.42
        hjaug1 = HauteurJaugeage(station=station, sysalti=sysalti,
                                 coteretenue=coteretenue1)
        hjaug2 = HauteurJaugeage(station=station, sysalti=sysalti,
                                 coteretenue=coteretenue2)

        code = '156'
        site = _sitehydro.Sitehydro(code='O1234567')
        hauteurs = [hjaug1, hjaug2]
        jaug = Jaugeage(code=code, site=site, hauteurs=hauteurs,
                        tri_hauteurs=False)
        self.assertEqual(jaug.hauteurs, hauteurs)
        jaug = Jaugeage(code=code, site=site, hauteurs=hauteurs,
                        tri_hauteurs=True)
        self.assertNotEqual(jaug.hauteurs, hauteurs)
        self.assertEqual(jaug.hauteurs[0], hjaug2)
        self.assertEqual(jaug.hauteurs[1], hjaug1)

        def test_order_hauteurs_01(self):
            """check soritng hauteurs fuzzy mode"""
            hjaug1 = HauteurJaugeage(station=station, sysalti=sysalti,
                                     coteretenue=coteretenue1)
            hjaug2 = None
            hjaug3 = 154.2
            hjaug4 = '187.4'

            hauteurs = [hjaug1, hjaug2, hjaug3, hjaug4]

            code = '156'
            site = _sitehydro.Sitehydro(code='O1234567')
            jaug = Jaugeage(code=code, site=site, hauteurs=hauteurs,
                            tri_hauteurs=True, strict=False)
            # just chack that each hauteur is in hauteurs
            # no sorting check
            self.assertEqual(len(jaug.hauteurs), len(hauteurs))
            for hauteur in hauteurs:
                self.assertIn(hauteur, jaug.hauteurs)

    def test_str_01(self):
        """check str"""
        code = '156'
        codesite = 'O1234567'
        site = _sitehydro.Sitehydro(code=codesite)
        jaug = Jaugeage(code=code, site=site)
        jaug_str = jaug.__str__()
        self.assertTrue(jaug_str.find(code) > -1)
        self.assertTrue(jaug_str.find(codesite) > -1)

    def test_str_02(self):
        """check str fuzzy mode"""
        code = '156'
        codesite = 'O1234567'
        site = codesite
        #site = _sitehydro.Sitehydro(code=codesite)
        jaug = Jaugeage(code=code, site=site, strict=False)
        jaug_str = jaug.__str__()

        self.assertTrue(jaug_str.find(code) > -1)
        self.assertTrue(jaug_str.find(codesite) > -1)

        jaug = Jaugeage(code=code, site=None, strict=False)
        jaug_str = jaug.__str__()
        self.assertTrue(jaug_str.find('<sans site>') > -1)

    def test_str_03(self):
        """check str with dte"""
        code = '156'
        codesite = 'O1234567'
        site = _sitehydro.Sitehydro(code=codesite)
        dte = datetime(2015, 4, 7, 0, 17, 23)
        jaug = Jaugeage(code=code, site=site, dte=dte)
        jaug_str = jaug.__str__()

        self.assertTrue(jaug_str.find(code) > -1)
        self.assertTrue(jaug_str.find(codesite) > -1)
        self.assertTrue(jaug_str.find('2015-04-07') > -1)
        self.assertTrue(jaug_str.find('00:17:23') > -1)

    def test_error_01(self):
        """code error"""
        code = '156'
        site = _sitehydro.Sitehydro(code='O1234567')
        Jaugeage(code=code, site=site)

        code = None
        with self.assertRaises(TypeError) as context:
            Jaugeage(code=code, site=site)
        self.assertEqual(str(context.exception),
                         'code is required')

    def test_error_02(self):
        """site error"""
        code = '156'
        site = _sitehydro.Sitehydro(code='O1234567')
        Jaugeage(code=code, site=site)

        site = None
        with self.assertRaises(TypeError) as context:
            Jaugeage(code=code, site=site)
        self.assertEqual(str(context.exception),
                         'site is required')

        site = 'O1234567'
        with self.assertRaises(TypeError) as context:
            Jaugeage(code=code, site=site)
        self.assertEqual(str(context.exception),
                         'site is not a sitehydro.Sitehydro')

    def test_error_03(self):
        """ float properties error"""
        properties_to_check = ['section_mouillee',
                               'perimetre_mouille',
                               'largeur_miroir',
                               'vitessemoy', 'vitessemax',
                               'vitessemoy_surface']

        for prop in properties_to_check:
            args = {}
            args['code'] = '156'
            args['site'] = _sitehydro.Sitehydro(code='A1234567')
            args[prop] = 147.45
            Jaugeage(**args)

            args[prop] = 'AA'
            with self.assertRaises(ValueError):
                Jaugeage(**args)

    def test_error_04(self):
        """hauteurs error"""
        code = '156'
        site = _sitehydro.Sitehydro(code='A1234567')

        station = _sitehydro.Station(code='O123456789')
        sysalti = 0
        coteretenue1 = 100.8
        coteretenue2 = 105.8
        hjaug1 = HauteurJaugeage(station=station, sysalti=sysalti,
                                 coteretenue=coteretenue1)
        hjaug2 = HauteurJaugeage(station=station, sysalti=sysalti,
                                 coteretenue=coteretenue2)

        hauteurs = [hjaug1, hjaug2]

        Jaugeage(code=code, site=site, hauteurs=hauteurs)

        hauteurs = [hjaug1, 'AA']
        with self.assertRaises(TypeError) as context:
            Jaugeage(code=code, site=site, hauteurs=hauteurs)
        self.assertEqual(str(context.exception),
                         'hauteurs is not an iterable of HauteurJaugeage')

    def test_error_05(self):
        """check dte dtdeb, dtfin and dtmaj"""
        code = '156'
        site = _sitehydro.Sitehydro(code='O1234567')
        dte = datetime(2016, 10, 3, 10, 45, 12)
        dtdeb = datetime(2016, 10, 3, 9, 4, 15)
        dtfin = datetime(2016, 10, 3, 11, 17, 54)
        dtmaj = datetime(2017, 7, 3, 5, 54, 1)
        jaug = Jaugeage(code=code, site=site, dte=dte, dtdeb=dtdeb,
                        dtfin=dtfin, dtmaj=dtmaj)
        self.assertEqual((jaug.dte, jaug.dtdeb, jaug.dtfin, jaug.dtmaj),
                         (dte, dtdeb, dtfin, dtmaj))
        jaug.dte = '2015-06-07T05:04:03'
        with self.assertRaises(Exception):
            jaug.dte = 'AA'
        with self.assertRaises(Exception):
            jaug.dtdeb = 'AA'
        with self.assertRaises(Exception):
            jaug.dtfin = 'AA'
        with self.assertRaises(Exception):
            jaug.dtmaj = 'AA'

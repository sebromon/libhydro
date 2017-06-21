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
from datetime import datetime, timedelta

from libhydro.core.courbecorrection import (CourbeCorrection, PivotCC)

import libhydro.core.intervenant as _intervenant
import libhydro.core.sitehydro as _sitehydro

# -- strings ------------------------------------------------------------------
__version__ = '0.1'
__date__ = '2017-05-04'

# HISTORY
# V0.1 - SR - 2017-05-04
#   first shot

class TestPivotCC(unittest.TestCase):
    """PivotCT class tests."""

    def test_base_01(self):
        """PivotCC with dte and deltah"""
        dte = datetime(2015, 1, 2, 3, 4, 5)
        deltah = 10.5
        pivot = PivotCC(dte=dte, deltah=deltah)
        self.assertEqual((pivot.dte, pivot.deltah,
                          pivot.dtactivation, pivot.dtdesactivation),
                         (dte, deltah, None, None))

    def test_base_02(self):
        """PivotCTPoly with all properties not None"""
        dte = datetime(2015, 1, 2, 3, 4, 5)
        deltah = -14.6
        dtactivation = datetime(2016, 10, 2, 9, 47, 3)
        dtdesactivation = datetime(2016, 11, 6, 22, 6, 9)
        pivot = PivotCC(dte=dte, deltah=deltah, dtactivation=dtactivation,
                        dtdesactivation=dtdesactivation)
        self.assertEqual((pivot.dte, pivot.deltah,
                          pivot.dtactivation, pivot.dtdesactivation),
                         (dte, deltah, dtactivation, dtdesactivation))

    def test_base_03(self):
        """ test __lt__ and __gt__ functions """
        pivot1 = PivotCC(dte=datetime(2010, 1, 2, 3, 4, 5),
                         deltah = -10.5)
        pivot2 = PivotCC(dte=datetime(2015, 10, 6, 11, 9, 54),
                         deltah = 56.2)

        self.assertTrue(pivot1 < pivot2)
        self.assertFalse(pivot1 > pivot2)
        
        self.assertFalse(pivot2 < pivot1)
        self.assertTrue(pivot2 > pivot1)
        

    def test_base_04(self):
        """fuzzy mode"""
        dte = datetime(2010, 4, 9, 10, 41, 32)
        pivot = PivotCC(dte=dte, strict=False)
        self.assertEqual((pivot.dte, pivot.deltah,
                          pivot.dtactivation, pivot.dtdesactivation),
                         (dte, None, None, None))

    def test_str_01(self):
        """Test __str__ method."""
        dte = datetime(2010, 4, 9, 10, 41, 32)
        deltah = 18.4
        pivot = PivotCC(dte=dte, deltah=deltah)
        str_expected = "Point pivot dte : {0} deltah : {1}".format(dte,deltah)
        self.assertEqual(pivot.__str__(),str_expected)


    def test_error_01(self):
        """dte error."""
        dte = datetime(2015, 1, 2, 3, 4, 5)
        deltah = 18.4
        
        PivotCC(dte=dte, deltah=deltah)

        dte = None
        with self.assertRaises(TypeError) as context:
            PivotCC(dte=dte, deltah=deltah)
        self.assertEqual(context.exception.message,
                         'a value other than None is required')
        
        dte = 'ABC'
        with self.assertRaises(ValueError) as context:
            PivotCC(dte=dte, deltah=deltah)
        self.assertEqual(context.exception.message,
                         'could not convert object to datetime.datetime')
    
    def test_error_02(self):
        """deltah error."""
        dte = datetime(2015, 1, 2, 3, 4, 5)
        deltah = 18.4
        
        PivotCC(dte=dte, deltah=deltah)

        deltah = None
        with self.assertRaises(TypeError) as context:
            PivotCC(dte=dte, deltah=deltah)
        self.assertEqual(context.exception.message,
                         'deltah is required')
        
        deltah = 'ABC'
        with self.assertRaises(ValueError) as context:
            PivotCC(dte=dte, deltah=deltah)
        pos = context.exception.message.rfind('could not convert')
        self.assertTrue( pos > -1)
        
#
#    def test_error_02(self):
#        """Debit error."""
#        hauteur = 1.5
#        debit = 3.6
#        PivotCTPoly(hauteur=hauteur, debit=debit)
#        debit = None
#        with self.assertRaises(TypeError) as context:
#            PivotCTPoly(hauteur=hauteur, debit=debit)
#        self.assertEqual(context.exception.message,
#                         'debit is required') 
#        
#        debit = 'ab'
#        with self.assertRaises(ValueError):
#            PivotCTPoly(hauteur=hauteur, debit=debit)
#
#    def test_error_03(self):
#        """qualif not in nomenclature."""
#        hauteur = 1.5
#        debit = 3.4
#
#        qualif = 12
#        PivotCTPoly(hauteur=hauteur, qualif=qualif, debit=debit)
#
#        qualif = 0
#        with self.assertRaises(ValueError):
#            PivotCTPoly(hauteur=hauteur, qualif=qualif, debit=debit)


# -- class TestCourbeCorrection ----------------------------------------------------
class TestCourbeCorrection(unittest.TestCase):

    """CourbeCorrection class tests."""

    def test_base_01(self):
        """Empty CourbeCorrection."""

        station = _sitehydro.Station(code='O123456789')
        cc = CourbeCorrection(station=station)
        self.assertEqual(
            (cc.station, cc.libelle, cc.commentaire, cc.pivots
             , cc.dtmaj),
            (station, None, None, [], None))
    
    def test_base_02(self):
        """CourbeCorrection with all properties not None"""

        station = _sitehydro.Station(code='O123456789')
        commentaire = 'no comment'
        libelle = 'courbe bidon'
        pivot1 = PivotCC(dte=datetime(2010, 1, 2, 3, 4, 5),
                         deltah = -10.5)
        pivot2 = PivotCC(dte=datetime(2015, 10, 6, 11, 9, 54),
                         deltah = 56.2)
        pivots = [pivot1, pivot2]
        dtmaj = datetime(2017, 6, 21, 8, 37, 15)        
        
        cc = CourbeCorrection(station=station,commentaire=commentaire,
                              libelle=libelle, pivots = pivots, dtmaj=dtmaj)
        self.assertEqual(
            (cc.station, cc.libelle, cc.commentaire, cc.pivots
             , cc.dtmaj),
            (station, libelle, commentaire, pivots, dtmaj))
    
    def test_base_03(self):
        """Sorting pivots"""
        
        station = _sitehydro.Station(code='O123456789')
        commentaire = 'no comment'
        libelle = 'courbe bidon'
        pivot1 = PivotCC(dte=datetime(2015, 1, 2, 3, 4, 5),
                         deltah = -10.5)
        pivot2 = PivotCC(dte=datetime(2001, 10, 6, 11, 9, 54),
                         deltah = 56.2)
        pivots = [pivot1, pivot2]
        dtmaj = datetime(2017, 6, 21, 8, 37, 15)        
        
        cc = CourbeCorrection(station=station,commentaire=commentaire,
                              libelle=libelle, pivots = pivots, dtmaj=dtmaj,
                              tri_pivots=False)
        self.assertEqual(
            (cc.station, cc.libelle, cc.commentaire, cc.pivots
             , cc.dtmaj),
            (station, libelle, commentaire, pivots, dtmaj))
        
        cc = CourbeCorrection(station=station,commentaire=commentaire,
                              libelle=libelle, pivots = pivots, dtmaj=dtmaj,
                              tri_pivots=True)
        self.assertNotEqual(cc.pivots, pivots)
        self.assertEqual(len(cc.pivots), len(pivots))
        self.assertEqual(cc.pivots[0], pivot2)
        self.assertEqual(cc.pivots[1], pivot1)
    
    def test_base_04(self):
        """ fuzzy mode 1 point pivot"""
        station = _sitehydro.Station(code='O123456789')
        pivot1 = PivotCC(dte=datetime(2010, 1, 2, 3, 4, 5),
                         deltah = -10.5)
        pivots = pivot1
        CourbeCorrection(station=station)
        with self.assertRaises(TypeError):
            CourbeCorrection(station=station, pivots=pivots)

        ct = CourbeCorrection(station=station, pivots=pivots,strict=False)
        self.assertEqual(ct.pivots, [pivots])
    
    def test_base_05(self):
        """ fuzzy mode station and pivots"""
        
        station = 'O123456789'
        pivots = [datetime(2015, 1, 9, 14, 21, 41),
                  'ABC']
        ct = CourbeCorrection(station=station, pivots=pivots,strict=False)
        self.assertEqual((ct.station,ct.pivots), (station,pivots))

    def test_str_01(self):
        """ test __str__ method without pivots and libelle """
        code = 'O123456789'
        station = _sitehydro.Station(code=code)
        cc = CourbeCorrection(station=station)
        str_cc = cc.__str__()
        self.assertTrue(str_cc.rfind('0 pivot') > -1)
        self.assertTrue(str_cc.rfind(code) > -1)
        self.assertTrue(str_cc.rfind('<sans libelle>') > -1)

    def test_str_02(self):
        """ test __str__ method with pivots and libelle """
        code = 'O123456789'
        station = _sitehydro.Station(code=code)
        libelle = 'toto'
        pivot1 = PivotCC(dte=datetime(2010, 1, 2, 3, 4, 5),
                         deltah = -10.5)
        pivot2 = PivotCC(dte=datetime(2015, 10, 6, 11, 9, 54),
                         deltah = 56.2)
        pivots = [pivot1, pivot2]
        cc = CourbeCorrection(station=station, libelle=libelle, pivots=pivots)
        str_cc = cc.__str__()
        self.assertTrue(str_cc.rfind('2 pivots') > -1)
        self.assertTrue(str_cc.rfind(code) > -1)
        self.assertTrue(str_cc.rfind(libelle) > -1)

    def test_str_03(self):
        """ test __str__ method fuzzy mode """
        code = 'O123456789'
        station = code
        cc = CourbeCorrection(station=station, strict=False)
        str_cc = cc.__str__()
        self.assertTrue(str_cc.rfind('0 pivot') > -1)
        self.assertTrue(str_cc.rfind(code) > -1)
        self.assertTrue(str_cc.rfind('<sans libelle>') > -1)
        
        station = None
        cc = CourbeCorrection(station=station, strict=False)
        str_cc = cc.__str__()
        self.assertTrue(str_cc.rfind('0 pivot') > -1)
        self.assertTrue(str_cc.rfind('<sans codestation>') > -1)
        self.assertTrue(str_cc.rfind('<sans libelle>') > -1)

    def test_error_01(self):
        """station error"""
        station = _sitehydro.Station(code='O123456789')
        CourbeCorrection(station=station)
        
        station = None
        with self.assertRaises(TypeError) as context:
            CourbeCorrection(station=station)
        self.assertEqual(context.exception.message, 'station is required')
        
        station = 'O123456789'
        with self.assertRaises(TypeError) as context:
            CourbeCorrection(station=station)
        self.assertEqual(context.exception.message,
                         'station is not a sitehydro.Station')
        
    def test_error_02(self):
        """pivots error"""
        station = _sitehydro.Station(code='O123456789')
        pivot1 = PivotCC(dte=datetime(2010, 1, 2, 3, 4, 5),
                         deltah = -10.5)
        pivot2 = PivotCC(dte=datetime(2015, 10, 6, 11, 9, 54),
                         deltah = 56.2)
        pivots = [pivot1, pivot2]
        CourbeCorrection(station=station, pivots=pivots)

        pivots = [pivot1]
        with self.assertRaises(TypeError) as context:
            CourbeCorrection(station=station, pivots=pivots)
        self.assertEqual(context.exception.message,
                         'pivots must be an iterable of minimum 2 PivotCC')
        
        pivots = [pivot1, 'pivot2']
        with self.assertRaises(TypeError) as context:
            CourbeCorrection(station=station, pivots=pivots)
        self.assertEqual(context.exception.message,
                         'pivots must be a PivotCC or an iterable of PivotCC')

#    def test_base_02(self):
#        """CourbeTarage with 2 pivots"""
#        
#        hauteur1 = 1.5
#        debit1 = 2.3
#        pivot1 = PivotCTPoly(hauteur=hauteur1, debit=debit1)
#
#        hauteur2 = 14.2
#        debit2 = 3.4
#        pivot2 = PivotCTPoly(hauteur=hauteur2, debit=debit2)
#
#        pivots = [pivot1, pivot2]
#        code = 'tre'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, pivots=pivots)
#
#        self.assertEqual(len(ct.pivots), len(pivots))
#        self.assertEqual(ct.pivots[0], pivots[0])
#        self.assertEqual(ct.pivots[1], pivots[1])
#
#    def test_base_03(self):
#        """ Pivots sorted """
#        hauteur1 = 100.6
#        debit1 = 2.3
#        pivot1 = PivotCTPoly(hauteur=hauteur1, debit=debit1)
#
#        hauteur2 = 14.2
#        debit2 = 3.4
#        pivot2 = PivotCTPoly(hauteur=hauteur2, debit=debit2)
#
#        pivots = [pivot1, pivot2]
#        code = 'tre'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, pivots=pivots)
#
#        self.assertEqual(len(ct.pivots), len(pivots))
#        self.assertTrue(ct.pivots[0].hauteur <= ct.pivots[1].hauteur)
#        self.assertEqual(ct.pivots[0], pivots[1])
#        self.assertEqual(ct.pivots[1], pivots[0])
#    
#    def test_base_04(self):
#        """CourbeTarge de type puissance without points"""
#        code = 'tre'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        typect = 4
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)
#        self.assertEqual((ct.code, ct.station, ct.typect),
#                         (code, station, typect))
#
#    def test_base_05(self):
#        """CourbeTarge de type puissance with 2 points"""
#        code = 'tre'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        typect = 4
#        
#        hauteur = (10.5, 16.4)
#        vara = (0.5, 0.8)
#        varb = (1.5, 1.4)
#        varh = (15.4,19.4)
#        pivots = [PivotCTPuissance(hauteur=hauteur[i], vara=vara[i],
#                                   varb=varb[i], varh=varh[i])
#                  for i in xrange(0,2)]
#        self.assertEqual(len(pivots),2)
#
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect, pivots=pivots)
#        self.assertEqual((ct.code,ct.station,ct.typect),
#                         (code,station,typect))
#        self.assertEqual(len(ct.pivots), len(pivots))
#        self.assertEqual(ct.pivots[0], pivots[0])
#        self.assertEqual(ct.pivots[1], pivots[1])
#    
#    def test_base_06(self):
#        """CourbeTarge de type puissance with 2 unsorted points"""
#        code = 'tre'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        typect = 4
#        
#        hauteur = (16.4, 10.8)
#        vara = (0.5, 0.8)
#        varb = (1.5, 1.4)
#        varh = (15.4,19.4)
#        pivots = [PivotCTPuissance(hauteur=hauteur[i], vara=vara[i],
#                                   varb=varb[i], varh=varh[i])
#                  for i in xrange(0, 2)]
#        self.assertEqual(len(pivots), 2)
#
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect, pivots=pivots)
#        self.assertEqual((ct.code,ct.station,ct.typect),
#                         (code,station,typect))
#        self.assertEqual(len(ct.pivots), len(pivots))
#        self.assertEqual(ct.pivots[0], pivots[1])
#        self.assertEqual(ct.pivots[1], pivots[0])
#    
#    def test_base_07(self):
#        """courbeTarage with periodes"""
#        code = 'tre'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        periode1 = PeriodeCT(dtdeb=datetime(2015, 1, 1),
#                             dtfin=datetime(2016, 1, 1))
#        periode2 = PeriodeCT(dtdeb=datetime(2016, 2, 1),
#                             dtfin=datetime(2017, 1, 1))
#        periodes = [periode1, periode2]
#        ct = CourbeTarage(code=code, libelle=libelle,station=station, periodes=periodes)
#        self.assertEqual(len(ct.periodes),len(periodes))
#        self.assertEqual(ct.periodes[0],periodes[0])
#        self.assertEqual(ct.periodes[1], periodes[1])
#        
#
#    def test_base_08(self):
#        """CourbeTarage"""
#        code = 'code'
#        station = _sitehydro.Station(code='O123456789')
#        libelle = 'courbé de tarage'
#        typect = 0
#        limiteinf = 50
#        limitesup = 1000
#        dn = 1.1
#        alpha = 0.9
#        beta = 1.2
#        commentaire = 'courbe test'
#        contact = _intervenant.Contact('159')
#        
#        pivots = [PivotCTPoly(hauteur=189.6, debit=103254.2),
#                  PivotCTPoly(hauteur=1110.4, debit=1151543.9)]
#        periodes = [PeriodeCT(dtdeb=datetime(2015,1,1),
#                             dtfin=datetime(2016,1,1))]
#        
#        dtmaj = datetime.utcnow()
#        ct = CourbeTarage(code=code, station=station, libelle=libelle,
#                          typect=typect, limiteinf=limiteinf,
#                          limitesup=limitesup, dn=dn, alpha=alpha, beta=beta,
#                          commentaire=commentaire, contact=contact,
#                          pivots=pivots, periodes=periodes, dtmaj=dtmaj)
#        self.assertEqual((ct.code, ct.station, ct.libelle, ct.typect,
#                         ct.limiteinf, ct.limitesup, ct.dn, ct.alpha, ct.beta,
#                         ct.commentaire, ct.contact, ct.pivots, ct.periodes, ct.dtmaj),
#                         (code, station, libelle, typect,
#                         limiteinf, limitesup, dn, alpha, beta,
#                         commentaire, contact, pivots, periodes, dtmaj))
#
#    def test_str_01(self):
#        code = 'courbe 123'
#        libelle = 'libelle'
#        station = _sitehydro.Station(code='O123456789')
#        typect = 0
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)
#        self.assertTrue(ct.__str__().rfind('polyligne') > -1)
#        typect = 4
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)
#        self.assertTrue(ct.__str__().rfind('fonction puissance') > -1)
#
#    def test_str_02(self):
#        code = 'courbe 123'
#        libelle = 'libelle'
#        station = _sitehydro.Station(code='O123456789')
#        typect = 16
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect, strict=False)
#        self.assertTrue(ct.__str__().rfind('polyligne') == -1)
#        self.assertTrue(ct.__str__().rfind('<sans type>') > -1)
#        typect = 4
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)
#        self.assertTrue(ct.__str__().rfind('fonction puissance') > -1)
#
#
#    def test_error_01(self):
#        """code error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        CourbeTarage(code=code, libelle=libelle, station=station)
#
#        with self.assertRaises(TypeError) as context:
#            CourbeTarage(libelle=libelle, station=station)
#        self.assertEqual(context.exception.message,
#                         'code is required')
#    
#    def test_error_011(self):
#        """libelle error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        CourbeTarage(code=code, libelle=libelle, station=station)
#
#        with self.assertRaises(TypeError) as context:
#            CourbeTarage(code=code, station=station)
#        self.assertEqual(context.exception.message,
#                         'libelle is required')
#
#    def test_error_02(self):
#        """station error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        CourbeTarage(code=code, libelle=libelle, station=station)
#
#        station = 'O123456789'
#        with self.assertRaises(TypeError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station)
#        self.assertEqual(context.exception.message,
#                         'station is not a sitehydro.Station')
#        
#        with self.assertRaises(TypeError) as context:
#            CourbeTarage(code=code, libelle=libelle)
#        self.assertEqual(context.exception.message,
#                         'station is required')
#
#    def test_error_03(self):
#        """type courbe error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        typect = 0
#        CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)
#
#        typect = 2
#        with self.assertRaises(ValueError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)
#
#        self.assertEqual(context.exception.message,
#                         'value should be in nomenclature 503')
#
#    def test_error_04(self):
#        """one point pivot error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        pivot = PivotCTPoly(hauteur=1.5, qualif=20, debit=2.3)
#        with self.assertRaises(ValueError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station, pivots=[pivot])
#        self.assertEqual(context.exception.message,
#                         'pivots must not contain only one pivot')
#
#    def test_error_041(self):
#        """limiteinf error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        limiteinf = 15.5
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, limiteinf=limiteinf)
#        
#        ct.limitesup = 30.1
#        with self.assertRaises(ValueError) as context:
#            ct.limiteinf = 35.2
#        self.assertEqual(context.exception.message,
#                         'limiteinf must be smaller than limitesup')
#        
#        limiteinf = 156.4
#        limitesup = 155.1
#        with self.assertRaises(ValueError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station,
#                         limiteinf=limiteinf, limitesup=limitesup)
#        self.assertEqual(context.exception.message,
#                         'limiteinf must be smaller than limitesup')
#
#    def test_error_042(self):
#        """limitesup error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        limitesup = 15.5
#        ct = CourbeTarage(code=code, libelle=libelle, station=station, limitesup=limitesup)
#        
#        ct.limiteinf = 10.0
#        with self.assertRaises(ValueError) as context:
#            ct.limitesup = 5.6
#        self.assertEqual(context.exception.message,
#                         'limiteinf must be smaller than limitesup')
#        
#        limiteinf = 156.4
#        limitesup = 155.1
#        with self.assertRaises(ValueError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station,
#                         limiteinf=limiteinf, limitesup=limitesup)
#        self.assertEqual(context.exception.message,
#                         'limiteinf must be smaller than limitesup')
#        
#    def test_error_05(self):
#        """beta error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        alpha = 1
#        beta = 1
#        dn = 1
#        CourbeTarage(code=code, libelle=libelle, station=station,
#                          dn=dn, alpha=alpha, beta=beta)
#
#        beta = -0.5
#
#        with self.assertRaises(ValueError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station,
#                         dn=dn, alpha=alpha, beta=beta)
#        self.assertEqual(context.exception.message,
#                         'beta must be positive')
#
#    def test_error_06(self):
#        """contact error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        contact = _intervenant.Contact(code='156')
#        CourbeTarage(code=code, libelle=libelle, station=station,
#                          contact = contact)
#
#        contact = '156'
#
#        with self.assertRaises(TypeError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station,
#                          contact = contact)
#        self.assertEqual(context.exception.message,
#                         'contact incorrect')
#
#
#    def test_error_07(self):
#        """pivots error"""
#        code='jjff'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        pivotpuissance1 = PivotCTPuissance(hauteur=15.6,
#                                           vara = 1.1,
#                                           varb = 1.2,
#                                           varh= 19.5)
#        pivotpuissance2 = PivotCTPuissance(hauteur=115.6,
#                                           vara = 0.8,
#                                           varb = 0.9,
#                                           varh= 119.5)
#        pivotpoly1 = PivotCTPoly(hauteur=15.6,
#                                 debit=1598.23)
#        pivotpoly2 = PivotCTPoly(hauteur=19.6,
#                                 debit=1142.3)
#        pivots = [pivotpoly1, pivotpoly2]
#        CourbeTarage(code=code, libelle=libelle, station=station,typect=0,
#                     pivots=pivots)
#        pivots = pivotpoly1
#        CourbeTarage(code=code, libelle=libelle, station=station,typect=0,
#                     pivots=pivots)
#        
#        pivots = [pivotpoly1, pivotpuissance2]
#        with self.assertRaises(TypeError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station, typect=0,
#                         pivots=pivots)
#        self.assertEqual(context.exception.message,
#                         'pivots must be a PivotCTPoly or an iterable of PivotCTPoly')
#        
#        pivots = pivotpuissance1
#        
#        # CourbeTarage kaunch ValueError instead of TypeError
#        with self.assertRaises(Exception) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station, typect=0,
#                         pivots=pivots)
##        self.assertEqual(context.exception.message,
##                         'pivots must be a PivotCTPoly or an iterable of PivotCTPoly')
#        
#        
#        pivots = [pivotpuissance1, pivotpuissance2]
#        CourbeTarage(code=code, libelle=libelle, station=station,typect=4,
#                     pivots=pivots)
#        
#        pivots = [pivotpuissance1, pivotpoly1]
#        with self.assertRaises(TypeError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station, typect=4,
#                         pivots=pivots)
#        self.assertEqual(context.exception.message,
#                         'pivots must be a PivotCTPuissance or an iterable of PivotCTPuissance')
#
#        pivots = pivotpoly1
#        # CourbeTarage kaunch ValueError instead of TypeError
#        with self.assertRaises(Exception) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station, typect=4,
#                         pivots=pivots)
##        self.assertEqual(context.exception.message,
##                         'pivots must be a PivotCTPuissance or an iterable of PivotCTPuissance')
#        
#
#    def test_error_08(self):
#        """periodes error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        periodes = PeriodeCT(dtdeb=datetime(2015, 1, 1),
#                             dtfin=datetime(2016, 1, 1))
#        
#        CourbeTarage(code=code, libelle=libelle, station=station,
#                     periodes = periodes)
#
#        periodes = 'periode'
#
#        with self.assertRaises(TypeError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station,
#                         periodes = periodes)
#        self.assertEqual(context.exception.message,
#                         'periodes is not a PeriodeCT or an iterable of PeriodeCT')
#
#        periodes = ['a', 'b']
#        with self.assertRaises(TypeError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station,
#                         periodes = periodes)
#        self.assertEqual(context.exception.message,
#                         'periodes is not a PeriodeCT or an iterable of PeriodeCT')
#
#    def test_error_09(self):
#        """dtmaj error"""
#        code = 'courbe 123'
#        libelle = 'libellé'
#        station = _sitehydro.Station(code='O123456789')
#        dtmaj = datetime(2017,1,1)
#        ct = CourbeTarage(code=code, libelle=libelle, station=station,
#                          dtmaj=dtmaj)
#        self.assertEqual(dtmaj,ct.dtmaj)
#        
#        dtmaj='ab'
#        with self.assertRaises(ValueError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station, dtmaj=dtmaj)
#        self.assertEqual(context.exception.message,
#                         'could not convert object to datetime.datetime')
#        
#        dtmaj = datetime.utcnow() + timedelta(minutes=1)
#        with self.assertRaises(ValueError) as context:
#            CourbeTarage(code=code, libelle=libelle, station=station, dtmaj=dtmaj)
#        self.assertEqual(context.exception.message,
#                         'dtmaj cannot be in the future')
#
#        with self.assertRaises(ValueError) as context:
#            ct.dtmaj = datetime.utcnow() + timedelta(minutes=1)
#        self.assertEqual(context.exception.message,
#                         'dtmaj cannot be in the future')
#        
#
#class TestHistoActivePeriode(unittest.TestCase):
#    
#    def test_base_01(self):
#        """HistoActivePeriode with only dtactivation"""
#        dtactivation = datetime(2017, 1, 1)
#        histo = HistoActivePeriode(dtactivation = dtactivation)
#        self.assertEqual((histo.dtactivation, histo.dtdesactivation),
#                         (dtactivation, None))
#
#    def test_base_02(self):
#        """HistoActivePeriode with only dtactivation"""
#        dtactivation = datetime(2017, 1, 1)
#        dtdesactivation = datetime(2017, 3, 1)
#        histo = HistoActivePeriode(dtactivation=dtactivation, dtdesactivation=dtdesactivation)
#        self.assertEqual((histo.dtactivation, histo.dtdesactivation),
#                         (dtactivation, dtdesactivation))
#
#    def test_error_01(self):
#        """dtactivation error"""
#        dtactivation = datetime(2017, 1, 1)
#        HistoActivePeriode(dtactivation=dtactivation)
#        
#        dtactivation = None
#        with self.assertRaises(TypeError) as context:
#            HistoActivePeriode(dtactivation=dtactivation)
#        self.assertEqual(context.exception.message,
#                         'a value other than None is required')
#        
#        dtactivation = 'aa'
#        with self.assertRaises(ValueError) as context:
#            HistoActivePeriode(dtactivation=dtactivation)
#        self.assertEqual(context.exception.message,
#                         'could not convert object to datetime.datetime')
#
#    def test_error_02(self):
#        dtactivation = datetime(2017, 1, 1)
#        dtdesactivation = '2017-05-01'
#        HistoActivePeriode(dtactivation=dtactivation, dtdesactivation=dtdesactivation)
#        
#        dtdesactivation = '2016-05-01'
#        with self.assertRaises(ValueError) as context:
#            HistoActivePeriode(dtactivation=dtactivation, dtdesactivation=dtdesactivation)
#        self.assertEqual(context.exception.message,
#                         'deactivation date must be later than activation date')
#
#class TestPeriodeCT(unittest.TestCase):
#
#    def test_base_01(self):
#        """simple PeriodeCT"""
#        dtdeb = datetime(2015, 1, 1)
#        dtfin = datetime(2016, 1, 1)
#        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin)
#        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
#                         (dtdeb, dtfin, 8, []))
#
#    def test_base_02(self):
#        """PeriodeCT with etat"""
#        dtdeb = datetime(2015, 1, 1)
#        dtfin = datetime(2016, 1, 1)
#        etat = 0
#        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat)
#        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat),
#                         (dtdeb, dtfin, etat))
#
#    def test_base_03(self):
#        """PeriodeCT with histos"""
#        dtdeb = datetime(2015, 1, 1)
#        dtfin = datetime(2016, 1, 1)
#        etat = 12
#
#        histo1 = HistoActivePeriode(dtactivation=datetime(2015, 1, 1),
#                                    dtdesactivation=datetime(2016, 1, 1))
#                                    
#        histo2 = HistoActivePeriode(dtactivation=datetime(2016, 2, 1),
#                                    dtdesactivation=datetime(2017, 1, 1))
#        
#        histos = histo1
#        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
#        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
#                         (dtdeb, dtfin, etat, [histos]))
#        
#        histos = [histo1, histo2]
#        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
#        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
#                         (dtdeb, dtfin, etat, histos))
#        
#
#    def test_error_01(self):
#        """dtfin error"""
#        dtdeb = datetime(2015, 1, 1)
#        dtfin = datetime(2014, 1, 1)
#        with self.assertRaises(ValueError) as context:
#            PeriodeCT(dtdeb=dtdeb, dtfin=dtfin)
#        self.assertEqual(context.exception.message,
#                         'dtfin must be later than dtdeb')
#
#    def test_error_02(self):
#        """ etat error"""
#        dtdeb = datetime(2015, 1, 1)
#        dtfin = datetime(2016, 1, 1)
#        etat = 0
#        PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat)
#
#        etat = 1
#        with self.assertRaises(ValueError) as context:
#            PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat)
#        self.assertEqual(context.exception.message,
#                         'value should be in nomenclature 504')
#
#    def test_error_03(self):
#        """ histos error"""
#        dtdeb = datetime(2015, 1, 1)
#        dtfin = datetime(2016, 1, 1)
#        etat = 12
#
#        histo1 = HistoActivePeriode(dtactivation=datetime(2015, 1, 1),
#                                    dtdesactivation=datetime(2016, 1, 1))
#                                    
#        histo2 = HistoActivePeriode(dtactivation=datetime(2016, 2, 1),
#                                    dtdesactivation=datetime(2017, 1, 1))
#        
#        histos = histo1
#        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
#        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
#                         (dtdeb, dtfin, etat, [histos]))
#        
#        histos = datetime(2015, 1 ,1)
#        
#        with self.assertRaises(Exception):
#            PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
#        
#        histos = [histo1, histo2]
#        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
#        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
#                         (dtdeb, dtfin, etat, histos))
#        
#        histos = [histo1, 2017]
#        with self.assertRaises(TypeError) as context:
#            PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
#        self.assertEqual(context.exception.message,
#                         'histos is not a HistoActivePeriode or an iterable of HistoActivePeriode')

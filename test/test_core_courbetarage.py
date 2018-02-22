# coding: utf-8
"""Test program for courbetarage.

To run all tests just type:
    python -m unittest test_core_courbetarage

To run only a class test:
    python -m unittest test_core_courbetarage.TestClass

To run only a specific test:
    python -m unittest test_core_courbetarage.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import unittest
from datetime import datetime, timedelta

from libhydro.core.courbetarage import (CourbeTarage, PivotCT,
                                        PivotCTPoly, PivotCTPuissance,
                                        HistoActivePeriode, PeriodeCT)
import libhydro.core.intervenant as _intervenant
import libhydro.core.sitehydro as _sitehydro

# -- strings ------------------------------------------------------------------
__version__ = '0.1'
__date__ = '2017-05-04'

# HISTORY
# V0.1 - SR - 2017-05-04
#   first shot

class TestPivotCT(unittest.TestCase):
    """PivotCT class tests."""

    def test_base_01(self):
        """PivotCC with hauteur"""
        hauteur = 158.9
        pivot = PivotCT(hauteur=hauteur)
        self.assertEqual((pivot.hauteur, pivot.qualif),
                         (hauteur, 16))


    def test_base_02(self):
        """ operators < and > """
        hauteur1 = 15.5
        pivot1 = PivotCT(hauteur=hauteur1)
        hauteur2 = 18.4
        pivot2 = PivotCT(hauteur=hauteur2)
        self.assertTrue(pivot1 < pivot2)
        self.assertFalse(pivot2 < pivot1)

        self.assertFalse(pivot1 > pivot2)
        self.assertTrue(pivot2 > pivot1)


class TestPivotCTPoly(unittest.TestCase):
    """PivotCTPoly class tests."""

    def test_base_01(self):
        """PivotCTPoly whit hauteur and debit."""
        hauteur = 1.5
        debit = 3.4
        pivot = PivotCTPoly(hauteur=hauteur, debit=debit)
        self.assertEqual(
            (pivot.hauteur, pivot.qualif, pivot.debit),
            (hauteur, 16, debit))

    def test_base_02(self):
        """PivotCTPoly whit hauteur and debit and qualif."""
        hauteur = 1.5
        debit = 3.4
        qualif = 20
        pivot = PivotCTPoly(hauteur=hauteur, qualif=qualif, debit=debit)
        self.assertEqual(
            (pivot.hauteur, pivot.qualif, pivot.debit),
            (hauteur, qualif, debit))

    def test_str_01(self):
        """Test __str__ method."""
        hauteur = 1.5
        debit = 3.4
        pivot = PivotCTPoly(hauteur=hauteur, debit=debit)
        str_expected = "Point pivot de hauteur {0} et de debit {1}".format(hauteur, debit)
        self.assertEqual(pivot.__str__(), str_expected)
#        self.assertTrue(obs.__str__().rfind('UTC') > -1)
#        self.assertTrue(obs.__str__().rfind('continue') > -1)

    def test_error_01(self):
        """Hauteur error."""
        hauteur = 1.5
        debit = 3.4
        PivotCTPoly(hauteur=hauteur, debit=debit)

        hauteur = None
        with self.assertRaises(TypeError) as context:
            PivotCTPoly(hauteur=hauteur, debit=debit)
        self.assertEqual(str(context.exception),
                         'hauteur is required')

        hauteur = 'ab'
        with self.assertRaises(ValueError):
            PivotCTPoly(hauteur=hauteur, debit=debit)

    def test_error_02(self):
        """Debit error."""
        hauteur = 1.5
        debit = 3.6
        PivotCTPoly(hauteur=hauteur, debit=debit)
        debit = None
        with self.assertRaises(TypeError) as context:
            PivotCTPoly(hauteur=hauteur, debit=debit)
        self.assertEqual(str(context.exception),
                         'debit is required')

        debit = 'ab'
        with self.assertRaises(ValueError):
            PivotCTPoly(hauteur=hauteur, debit=debit)

    def test_error_03(self):
        """qualif not in nomenclature."""
        hauteur = 1.5
        debit = 3.4

        qualif = 12
        PivotCTPoly(hauteur=hauteur, qualif=qualif, debit=debit)

        qualif = 0
        with self.assertRaises(ValueError):
            PivotCTPoly(hauteur=hauteur, qualif=qualif, debit=debit)

class TestPivotCTPuissance(unittest.TestCase):
    """PivotCTPuissance class tests."""

    def test_base_01(self):
        """PivotCTPuissance with hauteur,vara,varb,varh"""
        hauteur = 1.5
        vara = 3.4
        varb = 4.5
        varh = 154.3
        pivot = PivotCTPuissance(hauteur=hauteur, vara=vara, varb=varb, varh=varh)
        self.assertEqual(
            (pivot.hauteur, pivot.qualif, pivot.vara, pivot.varb, pivot.varh),
            (hauteur, 16, vara, varb, varh))

    def test_base_02(self):
        """PivotCTPuissance with hauteur, vara, varb, varh and qualif"""
        hauteur = 1.5
        vara = 3.4
        varb = 4.5
        varh = 154.3
        qualif = 20
        pivot = PivotCTPuissance(hauteur=hauteur, qualif=qualif, vara=vara, varb=varb, varh=varh)
        self.assertEqual((pivot.hauteur, pivot.qualif,
                          pivot.vara, pivot.varb, pivot.varh),
                         (hauteur, qualif, vara, varb, varh))


    def test_str_02(self):
        """Test __str__ method"""
        hauteur = 15.6
        vara = 0.5
        varb = 0.7
        varh = 1.1
        pivot = PivotCTPuissance(hauteur=hauteur,
                                 vara=vara, varb=varb, varh=varh)

        expected = 'Point pivot de hauteur {}'\
                   ' et de coefficients a={} b={} et h0={}'.format(hauteur, vara, varb, varh)
        self.assertEqual(pivot.__str__(), expected)

    def test_str_01(self):
        """Test __str__ method with None values."""
        pivot = PivotCTPuissance(strict=False)
        str_pivot = pivot.__str__()
        self.assertTrue(str_pivot.rfind('Point pivot') > -1)
        self.assertTrue(str_pivot.rfind('sans hauteur') > -1)
        self.assertTrue(str_pivot.rfind('sans coef a') > -1)
        self.assertTrue(str_pivot.rfind('sans coef b') > -1)
        self.assertTrue(str_pivot.rfind('sans coef h0') > -1)

    def test_error_01(self):
        """Hauteur error"""
        hauteur = 99.9
        vara = 3.4
        varb = 4.5
        varh = 154.3
        qualif = 20
        PivotCTPuissance(hauteur=hauteur, qualif=qualif, vara=vara, varb=varb, varh=varh)

        hauteur = None
        with self.assertRaises(TypeError) as context:
            PivotCTPuissance(hauteur=hauteur, qualif=qualif, vara=vara, varb=varb, varh=varh)
        self.assertEqual(str(context.exception), 'hauteur is required')

        hauteur = 'ab'
        with self.assertRaises(ValueError) as context:
            PivotCTPuissance(hauteur=hauteur, qualif=qualif, vara=vara, varb=varb, varh=varh)

    def test_error_02(self):
        """vara error"""
        hauteur = 1.5
        vara = 3.6
        varb = 4.5
        varh = 154.3
        qualif = 20
        PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                         vara=vara, varb=varb, varh=varh)
        vara = None
        with self.assertRaises(TypeError) as context:
            PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                             vara=vara, varb=varb, varh=varh)

        self.assertEqual(str(context.exception),
                         'vara is required')
        vara = 'ab'
        with self.assertRaises(ValueError):
            PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                             vara=vara, varb=varb, varh=varh)

    def test_error_03(self):
        """varb error"""
        hauteur = 1.5
        vara = 3.6
        varb = 4.5
        varh = 154.3
        qualif = 20
        PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                         vara=vara, varb=varb, varh=varh)
        varb = None
        with self.assertRaises(TypeError) as context:
            PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                             vara=vara, varb=varb, varh=varh)

        self.assertEqual(str(context.exception),
                         'varb is required')
        varb = 'ab'
        with self.assertRaises(ValueError):
            PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                             vara=vara, varb=varb, varh=varh)

    def test_error_04(self):
        """varh error"""
        hauteur = 1.5
        vara = 3.6
        varb = 4.5
        varh = 154.3
        qualif = 20
        PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                         vara=vara, varb=varb, varh=varh)
        varh = None
        with self.assertRaises(TypeError) as context:
            PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                             vara=vara, varb=varb, varh=varh)

        self.assertEqual(str(context.exception),
                         'varh is required')
        varh = 'ab'
        with self.assertRaises(ValueError):
            PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                             vara=vara, varb=varb, varh=varh)

    def test_error_05(self):
        """qualif not in nomenclature"""
        hauteur = 1.5
        vara = 3.4
        varb = 4.5
        varh = 154.3

        qualif = 12
        PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                         vara=vara, varb=varb, varh=varh)

        qualif = 0
        with self.assertRaises(ValueError) as context:
            PivotCTPuissance(hauteur=hauteur, qualif=qualif,
                             vara=vara, varb=varb, varh=varh)
        self.assertEqual(str(context.exception),
                         'value should be in nomenclature 505')

# -- class TestCourbeTarage ----------------------------------------------------
class TestCourbeTarage(unittest.TestCase):
    """CourbeTarage class tests."""

    def test_base_01(self):
        """Empty CourbeTarage."""
        code = 'tre'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'libellé'
        ct = CourbeTarage(code=code, libelle=libelle, station=station)
        self.assertEqual(
            (ct.code, ct.station, ct.libelle, ct.typect,
             ct.limiteinf, ct.limitesup,
             ct.dn, ct.alpha, ct.beta,
             ct.commentaire, ct.contact, ct.pivots, ct.periodes, ct.dtmaj),
            (code, station, libelle, 0,
             None, None,
             None, None, None,
             None, None, [], [], None))

    def test_base_02(self):
        """CourbeTarage with 2 pivots"""

        hauteur1 = 1.5
        debit1 = 2.3
        pivot1 = PivotCTPoly(hauteur=hauteur1, debit=debit1)

        hauteur2 = 14.2
        debit2 = 3.4
        pivot2 = PivotCTPoly(hauteur=hauteur2, debit=debit2)

        pivots = [pivot1, pivot2]
        code = 'tre'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        ct = CourbeTarage(code=code, libelle=libelle, station=station, pivots=pivots)

        self.assertEqual(len(ct.pivots), len(pivots))
        self.assertEqual(ct.pivots[0], pivots[0])
        self.assertEqual(ct.pivots[1], pivots[1])

    def test_base_03(self):
        """ Pivots sorted """
        hauteur1 = 100.6
        debit1 = 2.3
        pivot1 = PivotCTPoly(hauteur=hauteur1, debit=debit1)

        hauteur2 = 14.2
        debit2 = 3.4
        pivot2 = PivotCTPoly(hauteur=hauteur2, debit=debit2)

        pivots = [pivot1, pivot2]
        code = 'tre'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')

        ct = CourbeTarage(code=code, libelle=libelle, station=station, pivots=pivots)

        self.assertEqual(len(ct.pivots), len(pivots))
        self.assertTrue(ct.pivots[0].hauteur <= ct.pivots[1].hauteur)
        self.assertEqual(ct.pivots[0], pivots[1])
        self.assertEqual(ct.pivots[1], pivots[0])

    def test_base_04(self):
        """CourbeTarge de type puissance without points"""
        code = 'tre'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        typect = 4
        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)
        self.assertEqual((ct.code, ct.station, ct.typect),
                         (code, station, typect))

    def test_base_05(self):
        """CourbeTarge de type puissance with 2 points"""
        code = 'tre'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        typect = 4

        hauteur = (10.5, 16.4)
        vara = (0.5, 0.8)
        varb = (1.5, 1.4)
        varh = (15.4, 19.4)
        pivots = [PivotCTPuissance(hauteur=hauteur[i], vara=vara[i],
                                   varb=varb[i], varh=varh[i])
                  for i in range(0, 2)]
        self.assertEqual(len(pivots), 2)

        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect, pivots=pivots)
        self.assertEqual((ct.code, ct.station, ct.typect),
                         (code, station, typect))
        self.assertEqual(len(ct.pivots), len(pivots))
        self.assertEqual(ct.pivots[0], pivots[0])
        self.assertEqual(ct.pivots[1], pivots[1])

    def test_base_06(self):
        """CourbeTarge de type puissance with 2 unsorted points"""
        code = 'tre'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        typect = 4

        hauteur = (16.4, 10.8)
        vara = (0.5, 0.8)
        varb = (1.5, 1.4)
        varh = (15.4, 19.4)
        pivots = [PivotCTPuissance(hauteur=hauteur[i], vara=vara[i],
                                   varb=varb[i], varh=varh[i])
                  for i in range(0, 2)]
        self.assertEqual(len(pivots), 2)

        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect, pivots=pivots)
        self.assertEqual((ct.code, ct.station, ct.typect),
                         (code, station, typect))
        self.assertEqual(len(ct.pivots), len(pivots))
        self.assertEqual(ct.pivots[0], pivots[1])
        self.assertEqual(ct.pivots[1], pivots[0])

    def test_base_07(self):
        """courbeTarage with periodes"""
        code = 'tre'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        periode1 = PeriodeCT(dtdeb=datetime(2015, 1, 1),
                             dtfin=datetime(2016, 1, 1))
        periode2 = PeriodeCT(dtdeb=datetime(2016, 2, 1),
                             dtfin=datetime(2017, 1, 1))
        periodes = [periode1, periode2]
        ct = CourbeTarage(code=code, libelle=libelle, station=station, periodes=periodes)
        self.assertEqual(len(ct.periodes), len(periodes))
        self.assertEqual(ct.periodes[0], periodes[0])
        self.assertEqual(ct.periodes[1], periodes[1])


    def test_base_08(self):
        """CourbeTarage"""
        code = 'code'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'courbé de tarage'
        typect = 0
        limiteinf = 50
        limitesup = 1000
        dn = 1.1
        alpha = 0.9
        beta = 1.2
        commentaire = 'courbe test'
        contact = _intervenant.Contact('159')

        pivots = [PivotCTPoly(hauteur=189.6, debit=103254.2),
                  PivotCTPoly(hauteur=1110.4, debit=1151543.9)]
        periodes = [PeriodeCT(dtdeb=datetime(2015, 1, 1),
                              dtfin=datetime(2016, 1, 1))]

        dtmaj = datetime.utcnow()
        ct = CourbeTarage(code=code, station=station, libelle=libelle,
                          typect=typect, limiteinf=limiteinf,
                          limitesup=limitesup, dn=dn, alpha=alpha, beta=beta,
                          commentaire=commentaire, contact=contact,
                          pivots=pivots, periodes=periodes, dtmaj=dtmaj)
        self.assertEqual((ct.code, ct.station, ct.libelle, ct.typect,
                          ct.limiteinf, ct.limitesup, ct.dn, ct.alpha, ct.beta,
                          ct.commentaire, ct.contact, ct.pivots, ct.periodes, ct.dtmaj),
                         (code, station, libelle, typect,
                          limiteinf, limitesup, dn, alpha, beta,
                          commentaire, contact, pivots, periodes, dtmaj))

    def test_base_09(self):
        """test function get_used_actived_periodes"""
        code = 'code'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'libelle'

        histo1 = HistoActivePeriode(dtactivation=datetime(2015, 1, 1),
                                    dtdesactivation=datetime(2016, 1, 1))

        histo2 = HistoActivePeriode(dtactivation=datetime(2016, 2, 1),
                                    dtdesactivation=datetime(2017, 1, 1))

        histos = [histo1, histo2]

        periode1 = PeriodeCT(dtdeb=datetime(2014, 1, 1),
                             dtfin=datetime(2014, 2, 1),
                             etat=8)

        periode2 = PeriodeCT(dtdeb=datetime(2015, 1, 1),
                             dtfin=datetime(2016, 1, 1),
                             etat=8)
        periode3 = PeriodeCT(dtdeb=datetime(2016, 2, 1),
                             dtfin=datetime(2017, 1, 1))

        # par défaut periodes utilisées
        periodes = [periode1, periode2, periode3]
        ctar = CourbeTarage(code=code, station=station, libelle=libelle,
                            periodes=periodes)
        self.assertEqual(ctar.get_used_actived_periodes(),
                         periodes)

        # periode non utilisée
        periode2.etat = 0
        ctar = CourbeTarage(code=code, station=station, libelle=libelle,
                            periodes=periodes)
        self.assertEqual(ctar.get_used_actived_periodes(),
                         [periode1, periode3])

        # periode3 non active
        periode3.histos = histos
        ctar = CourbeTarage(code=code, station=station, libelle=libelle,
                            periodes=periodes)
        self.assertEqual(ctar.get_used_actived_periodes(),
                         [periode1])

        # periode3 active
        periode3.histos[1].dtdesactivation = None
        ctar = CourbeTarage(code=code, station=station, libelle=libelle,
                            periodes=periodes)
        self.assertEqual(ctar.get_used_actived_periodes(),
                         [periode1, periode3])

    def test_base_10(self):
        """test function is_used"""
        code = 'code'
        station = _sitehydro.Station(code='O123456789')
        libelle = 'libelle'

        histo1 = HistoActivePeriode(dtactivation=datetime(2015, 1, 1),
                                    dtdesactivation=datetime(2016, 1, 1))

        histo2 = HistoActivePeriode(dtactivation=datetime(2016, 2, 1),
                                    dtdesactivation=datetime(2017, 1, 1))

        histos = [histo1, histo2]

        periode1 = PeriodeCT(dtdeb=datetime(2014, 1, 1),
                             dtfin=datetime(2014, 2, 1),
                             etat=8)

        periode2 = PeriodeCT(dtdeb=datetime(2015, 1, 1),
                             dtfin=datetime(2016, 1, 1),
                             etat=8)
        periode3 = PeriodeCT(dtdeb=datetime(2016, 2, 1),
                             dtfin=datetime(2017, 1, 1))

        periode4 = PeriodeCT(dtdeb=datetime(2017, 6, 3, 1, 11, 4))

        periodes = [periode1, periode2, periode3, periode4]
        ctar = CourbeTarage(code=code, station=station, libelle=libelle,
                            periodes=periodes)
        self.assertFalse(ctar.is_active(dte=datetime(2013, 1, 1)))
        self.assertTrue(ctar.is_active(dte=datetime(2014, 1, 1)))
        self.assertTrue(ctar.is_active(dte=datetime(2014, 1, 1)))
        self.assertFalse(ctar.is_active(dte=datetime(2014, 3, 1)))

        self.assertTrue(ctar.is_active(dte=datetime(2015, 4, 14, 14, 15, 17)))
        self.assertTrue(ctar.is_active(dte=datetime(2016, 1, 1)))

        self.assertFalse(ctar.is_active(dte=datetime(2016, 1, 10, 2, 4, 5)))
        self.assertTrue(ctar.is_active(dte=datetime(2016, 4, 14, 14, 15, 17)))
        self.assertTrue(ctar.is_active(dte=datetime(2017, 1, 1)))
        self.assertFalse(ctar.is_active(dte=datetime(2017, 1, 1, 0, 0, 1)))

        self.assertTrue(ctar.is_active(dte=datetime(2017, 6, 4, 0, 0, 1)))
        self.assertTrue(ctar.is_active(dte=datetime(2050, 1, 1)))

        periode2.etat = 0
        self.assertFalse(ctar.is_active(dte=datetime(2015, 4, 14, 14, 15, 17)))

        periode3.histos = histos
        self.assertFalse(ctar.is_active(dte=datetime(2016, 4, 14, 14, 15, 17)))

        histo2.dtdesactivation = None
        self.assertTrue(ctar.is_active(dte=datetime(2016, 4, 14, 14, 15, 17)))

    def test_base_11(self):
        """fuzzy mode"""
        code = 'code'
        station = 'O123456789'
        libelle = 'libelle'
        pivots = PivotCTPoly(hauteur=1, debit=2)
        CourbeTarage(code=code, station=station, libelle=libelle,
                     pivots=pivots, strict=False)


    def test_str_01(self):
        """test __str__ strict mode"""
        code = 'courbe 123'
        libelle = 'libelle'
        station = _sitehydro.Station(code='O123456789')
        typect = 0
        ct = CourbeTarage(code=code, libelle=libelle, station=station,
                          typect=typect)
        self.assertTrue(ct.__str__().rfind('polyligne') > -1)
        typect = 4
        ct = CourbeTarage(code=code, libelle=libelle, station=station,
                          typect=typect)
        self.assertTrue(ct.__str__().rfind('fonction puissance') > -1)

    def test_str_02(self):
        """test __str__ fuzzy mode"""
        code = 'courbe 123'
        libelle = 'libelle'
        station = _sitehydro.Station(code='O123456789')
        typect = 16
        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect, strict=False)
        self.assertTrue(ct.__str__().rfind('polyligne') == -1)
        self.assertTrue(ct.__str__().rfind('<sans type>') > -1)
        typect = 4
        ct = CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)
        self.assertTrue(ct.__str__().rfind('fonction puissance') > -1)


    def test_error_01(self):
        """code error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        CourbeTarage(code=code, libelle=libelle, station=station)

        with self.assertRaises(TypeError) as context:
            CourbeTarage(libelle=libelle, station=station)
        self.assertEqual(str(context.exception),
                         'code is required')

    def test_error_011(self):
        """libelle error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        CourbeTarage(code=code, libelle=libelle, station=station)

        with self.assertRaises(TypeError) as context:
            CourbeTarage(code=code, station=station)
        self.assertEqual(str(context.exception),
                         'libelle is required')

    def test_error_02(self):
        """station error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        CourbeTarage(code=code, libelle=libelle, station=station)

        station = 'O123456789'
        with self.assertRaises(TypeError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station)
        self.assertEqual(str(context.exception),
                         'station is not a sitehydro.Station')

        with self.assertRaises(TypeError) as context:
            CourbeTarage(code=code, libelle=libelle)
        self.assertEqual(str(context.exception),
                         'station is required')

    def test_error_03(self):
        """type courbe error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        typect = 0
        CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)

        typect = 2
        with self.assertRaises(ValueError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station, typect=typect)

        self.assertEqual(str(context.exception),
                         'value should be in nomenclature 503')

    def test_error_04(self):
        """one point pivot error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        pivot = PivotCTPoly(hauteur=1.5, qualif=20, debit=2.3)

        pivots = pivot
        with self.assertRaises(TypeError):
            CourbeTarage(code=code, libelle=libelle, station=station,
                         pivots=pivots)

        pivots = [pivot]
        with self.assertRaises(TypeError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station,
                         pivots=[pivot])
        self.assertEqual(str(context.exception),
                         'pivots must not contain only one pivot')

    def test_error_041(self):
        """limiteinf error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        limiteinf = 15.5
        ct = CourbeTarage(code=code, libelle=libelle, station=station, limiteinf=limiteinf)

        ct.limitesup = 30.1
        with self.assertRaises(ValueError) as context:
            ct.limiteinf = 35.2
        self.assertEqual(str(context.exception),
                         'limiteinf must be smaller than limitesup')

        limiteinf = 156.4
        limitesup = 155.1
        with self.assertRaises(ValueError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station,
                         limiteinf=limiteinf, limitesup=limitesup)
        self.assertEqual(str(context.exception),
                         'limiteinf must be smaller than limitesup')

    def test_error_042(self):
        """limitesup error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        limitesup = 15.5
        ct = CourbeTarage(code=code, libelle=libelle, station=station, limitesup=limitesup)

        ct.limiteinf = 10.0
        with self.assertRaises(ValueError) as context:
            ct.limitesup = 5.6
        self.assertEqual(str(context.exception),
                         'limiteinf must be smaller than limitesup')

        limiteinf = 156.4
        limitesup = 155.1
        with self.assertRaises(ValueError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station,
                         limiteinf=limiteinf, limitesup=limitesup)
        self.assertEqual(str(context.exception),
                         'limiteinf must be smaller than limitesup')

    def test_error_05(self):
        """beta error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        alpha = 1
        beta = 1
        dn = 1
        CourbeTarage(code=code, libelle=libelle, station=station,
                     dn=dn, alpha=alpha, beta=beta)

        beta = -0.5

        with self.assertRaises(ValueError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station,
                         dn=dn, alpha=alpha, beta=beta)
        self.assertEqual(str(context.exception),
                         'beta must be positive')

    def test_error_06(self):
        """contact error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        contact = _intervenant.Contact(code='156')
        CourbeTarage(code=code, libelle=libelle, station=station,
                     contact=contact)

        contact = '156'

        with self.assertRaises(TypeError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station,
                         contact=contact)
        self.assertEqual(str(context.exception),
                         'contact incorrect')


    def test_error_07(self):
        """pivots error"""
        code = 'jjff'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        pivotpuissance1 = PivotCTPuissance(hauteur=15.6,
                                           vara=1.1,
                                           varb=1.2,
                                           varh=19.5)
        pivotpuissance2 = PivotCTPuissance(hauteur=115.6,
                                           vara=0.8,
                                           varb=0.9,
                                           varh=119.5)
        pivotpoly1 = PivotCTPoly(hauteur=15.6,
                                 debit=1598.23)
        pivotpoly2 = PivotCTPoly(hauteur=19.6,
                                 debit=1142.3)
        pivots = [pivotpoly1, pivotpoly2]
        CourbeTarage(code=code, libelle=libelle, station=station, typect=0,
                     pivots=pivots)

        pivots = [pivotpoly1, pivotpuissance2]
        with self.assertRaises(TypeError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station, typect=0,
                         pivots=pivots)
        self.assertEqual(str(context.exception),
                         'pivots must be a PivotCTPoly or an iterable of PivotCTPoly')

        pivots = [pivotpuissance1, pivotpuissance2]
        CourbeTarage(code=code, libelle=libelle, station=station, typect=4,
                     pivots=pivots)

        pivots = [pivotpuissance1, pivotpoly1]
        with self.assertRaises(TypeError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station, typect=4,
                         pivots=pivots)
        self.assertEqual(str(context.exception),
                         'pivots must be a PivotCTPuissance or an iterable of PivotCTPuissance')

    def test_error_08(self):
        """periodes error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        periodes = PeriodeCT(dtdeb=datetime(2015, 1, 1),
                             dtfin=datetime(2016, 1, 1))

        CourbeTarage(code=code, libelle=libelle, station=station,
                     periodes=periodes)

        periodes = 'periode'

        with self.assertRaises(TypeError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station,
                         periodes=periodes)
        self.assertEqual(str(context.exception),
                         'periodes is not a PeriodeCT or an iterable of PeriodeCT')

        periodes = ['a', 'b']
        with self.assertRaises(TypeError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station,
                         periodes=periodes)
        self.assertEqual(str(context.exception),
                         'periodes is not a PeriodeCT or an iterable of PeriodeCT')

    def test_error_09(self):
        """dtmaj error"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        dtmaj = datetime(2017, 1, 1)
        ct = CourbeTarage(code=code, libelle=libelle, station=station,
                          dtmaj=dtmaj)
        self.assertEqual(dtmaj, ct.dtmaj)

        dtmaj = 'ab'
        with self.assertRaises(ValueError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station, dtmaj=dtmaj)
        self.assertEqual(str(context.exception),
                         'could not convert object to datetime.datetime')

        dtmaj = datetime.utcnow() + timedelta(minutes=1)
        with self.assertRaises(ValueError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station, dtmaj=dtmaj)
        self.assertEqual(str(context.exception),
                         'dtmaj cannot be in the future')

        with self.assertRaises(ValueError) as context:
            ct.dtmaj = datetime.utcnow() + timedelta(minutes=1)
        self.assertEqual(str(context.exception),
                         'dtmaj cannot be in the future')

    def test_error_10(self):
        """pivots with same hauteur"""
        code = 'courbe 123'
        libelle = 'libellé'
        station = _sitehydro.Station(code='O123456789')
        typect = 0
        pivot1 = PivotCTPoly(hauteur=150.65, debit=14789.2)
        pivot2 = PivotCTPoly(hauteur=178.12, debit=15473.8)
        pivots = [pivot1, pivot2]
        CourbeTarage(code=code, libelle=libelle, station=station,
                     typect=typect, pivots=pivots)

        pivot2.hauteur = pivot1.hauteur
        with self.assertRaises(ValueError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station,
                         typect=typect, pivots=pivots)
        self.assertEqual(str(context.exception),
                         'pivots contains pivots with same hauteur')

        pivots = [pivot1, pivot1]
        with self.assertRaises(ValueError) as context:
            CourbeTarage(code=code, libelle=libelle, station=station,
                         typect=typect, pivots=pivots)
        self.assertEqual(str(context.exception),
                         'pivots contains pivots with same hauteur')

class TestHistoActivePeriode(unittest.TestCase):
    """HistoActivePeriode class tests."""

    def test_base_01(self):
        """HistoActivePeriode with only dtactivation"""
        dtactivation = datetime(2017, 1, 1)
        histo = HistoActivePeriode(dtactivation=dtactivation)
        self.assertEqual((histo.dtactivation, histo.dtdesactivation),
                         (dtactivation, None))

    def test_base_02(self):
        """HistoActivePeriode with only dtactivation"""
        dtactivation = datetime(2017, 1, 1)
        dtdesactivation = datetime(2017, 3, 1)
        histo = HistoActivePeriode(dtactivation=dtactivation, dtdesactivation=dtdesactivation)
        self.assertEqual((histo.dtactivation, histo.dtdesactivation),
                         (dtactivation, dtdesactivation))

    def test_error_01(self):
        """dtactivation error"""
        dtactivation = datetime(2017, 1, 1)
        HistoActivePeriode(dtactivation=dtactivation)

        dtactivation = None
        with self.assertRaises(TypeError) as context:
            HistoActivePeriode(dtactivation=dtactivation)
        self.assertEqual(str(context.exception),
                         'a value other than None is required')

        dtactivation = 'aa'
        with self.assertRaises(ValueError) as context:
            HistoActivePeriode(dtactivation=dtactivation)
        self.assertEqual(str(context.exception),
                         'could not convert object to datetime.datetime')

    def test_error_02(self):
        """dtdesactivation < dtactivation error"""
        dtactivation = datetime(2017, 1, 1)
        dtdesactivation = '2017-05-01'
        HistoActivePeriode(dtactivation=dtactivation, dtdesactivation=dtdesactivation)

        dtdesactivation = '2016-05-01'
        with self.assertRaises(ValueError) as context:
            HistoActivePeriode(dtactivation=dtactivation, dtdesactivation=dtdesactivation)
        self.assertEqual(str(context.exception),
                         'deactivation date must be later than activation date')

class TestPeriodeCT(unittest.TestCase):
    """PeriodeCT class tests."""

    def test_base_01(self):
        """simple PeriodeCT"""
        dtdeb = datetime(2015, 1, 1)
        dtfin = datetime(2016, 1, 1)
        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin)
        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
                         (dtdeb, dtfin, 8, []))

    def test_base_02(self):
        """PeriodeCT with etat"""
        dtdeb = datetime(2015, 1, 1)
        dtfin = datetime(2016, 1, 1)
        etat = 0
        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat)
        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat),
                         (dtdeb, dtfin, etat))

    def test_base_03(self):
        """PeriodeCT with histos"""
        dtdeb = datetime(2015, 1, 1)
        dtfin = datetime(2016, 1, 1)
        etat = 12

        histo1 = HistoActivePeriode(dtactivation=datetime(2015, 1, 1),
                                    dtdesactivation=datetime(2016, 1, 1))

        histo2 = HistoActivePeriode(dtactivation=datetime(2016, 2, 1),
                                    dtdesactivation=datetime(2017, 1, 1))

        histos = histo1
        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
                         (dtdeb, dtfin, etat, [histos]))

        histos = [histo1, histo2]
        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
                         (dtdeb, dtfin, etat, histos))


    def test_error_01(self):
        """dtfin error"""
        dtdeb = datetime(2015, 1, 1)
        dtfin = datetime(2014, 1, 1)
        with self.assertRaises(ValueError) as context:
            PeriodeCT(dtdeb=dtdeb, dtfin=dtfin)
        self.assertEqual(str(context.exception),
                         'dtfin must be later than dtdeb')

    def test_error_02(self):
        """ etat error"""
        dtdeb = datetime(2015, 1, 1)
        dtfin = datetime(2016, 1, 1)
        etat = 0
        PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat)

        etat = 1
        with self.assertRaises(ValueError) as context:
            PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat)
        self.assertEqual(str(context.exception),
                         'value should be in nomenclature 504')

    def test_error_03(self):
        """ histos error"""
        dtdeb = datetime(2015, 1, 1)
        dtfin = datetime(2016, 1, 1)
        etat = 12

        histo1 = HistoActivePeriode(dtactivation=datetime(2015, 1, 1),
                                    dtdesactivation=datetime(2016, 1, 1))

        histo2 = HistoActivePeriode(dtactivation=datetime(2016, 2, 1),
                                    dtdesactivation=datetime(2017, 1, 1))

        histos = histo1
        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
                         (dtdeb, dtfin, etat, [histos]))

        histos = datetime(2015, 1, 1)

        with self.assertRaises(Exception):
            PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)

        histos = [histo1, histo2]
        periode = PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
        self.assertEqual((periode.dtdeb, periode.dtfin, periode.etat, periode.histos),
                         (dtdeb, dtfin, etat, histos))

        histos = [histo1, 2017]
        with self.assertRaises(TypeError) as context:
            PeriodeCT(dtdeb=dtdeb, dtfin=dtfin, etat=etat, histos=histos)
        self.assertEqual(str(context.exception),
                         'histos is not a HistoActivePeriode or an iterable of HistoActivePeriode')

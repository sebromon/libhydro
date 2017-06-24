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

from libhydro.core.courbecorrection import (CourbeCorrection, PivotCC)
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
                         deltah=-10.5)
        pivot2 = PivotCC(dte=datetime(2015, 10, 6, 11, 9, 54),
                         deltah=56.2)

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
        str_expected = "Point pivot dte : {0} deltah : {1}".format(dte, deltah)
        self.assertEqual(pivot.__str__(), str_expected)


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
        self.assertTrue(pos > -1)

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
                         deltah=-10.5)
        pivot2 = PivotCC(dte=datetime(2015, 10, 6, 11, 9, 54),
                         deltah=56.2)
        pivots = [pivot1, pivot2]
        dtmaj = datetime(2017, 6, 21, 8, 37, 15)

        cc = CourbeCorrection(station=station, commentaire=commentaire,
                              libelle=libelle, pivots=pivots, dtmaj=dtmaj)
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
                         deltah=-10.5)
        pivot2 = PivotCC(dte=datetime(2001, 10, 6, 11, 9, 54),
                         deltah=56.2)
        pivots = [pivot1, pivot2]
        dtmaj = datetime(2017, 6, 21, 8, 37, 15)

        cc = CourbeCorrection(station=station, commentaire=commentaire,
                              libelle=libelle, pivots=pivots, dtmaj=dtmaj,
                              tri_pivots=False)
        self.assertEqual(
            (cc.station, cc.libelle, cc.commentaire, cc.pivots
             , cc.dtmaj),
            (station, libelle, commentaire, pivots, dtmaj))

        cc = CourbeCorrection(station=station, commentaire=commentaire,
                              libelle=libelle, pivots=pivots, dtmaj=dtmaj,
                              tri_pivots=True)
        self.assertNotEqual(cc.pivots, pivots)
        self.assertEqual(len(cc.pivots), len(pivots))
        self.assertEqual(cc.pivots[0], pivot2)
        self.assertEqual(cc.pivots[1], pivot1)

    def test_base_04(self):
        """ fuzzy mode 1 point pivot"""
        station = _sitehydro.Station(code='O123456789')
        pivot1 = PivotCC(dte=datetime(2010, 1, 2, 3, 4, 5),
                         deltah=-10.5)
        pivots = pivot1
        CourbeCorrection(station=station)
        with self.assertRaises(TypeError):
            CourbeCorrection(station=station, pivots=pivots)

        ct = CourbeCorrection(station=station, pivots=pivots, strict=False)
        self.assertEqual(ct.pivots, [pivots])

    def test_base_05(self):
        """ fuzzy mode station and pivots"""

        station = 'O123456789'
        pivots = [datetime(2015, 1, 9, 14, 21, 41),
                  'ABC']
        ct = CourbeCorrection(station=station, pivots=pivots, strict=False)
        self.assertEqual((ct.station, ct.pivots), (station, pivots))

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
                         deltah=-10.5)
        pivot2 = PivotCC(dte=datetime(2015, 10, 6, 11, 9, 54),
                         deltah=56.2)
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
                         deltah=-10.5)
        pivot2 = PivotCC(dte=datetime(2015, 10, 6, 11, 9, 54),
                         deltah=56.2)
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

    def test_error_03(self):
        """ pivots with same hauteur"""

        station = _sitehydro.Station(code='O123456789')
        pivot1 = PivotCC(dte=datetime(2010, 1, 2, 3, 4, 5),
                         deltah=-10.5)
        pivot2 = PivotCC(dte=datetime(2015, 10, 6, 11, 9, 54),
                         deltah=56.2)
        pivots = [pivot1, pivot2]
        CourbeCorrection(station=station, pivots=pivots)

        pivots = [pivot1, pivot1]
        with self.assertRaises(ValueError) as context:
            CourbeCorrection(station=station, pivots=pivots)
            self.assertEqual(context.exception.message,
                             'pivots contains 2 pivots with same date')

        pivot2.dte = pivot1.dte
        pivots = [pivot1, pivot1]
        with self.assertRaises(ValueError) as context:
            CourbeCorrection(station=station, pivots=pivots)
        self.assertEqual(context.exception.message,
                         'pivots contains 2 pivots with same date')

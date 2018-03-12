# coding: utf-8
"""Test program for xml.from_xml.

To run all tests just type:
    python -m unittest test_conv_xml_from_xml

To run only a class test:
    python -m unittest test_conv_xml_from_xml.TestClass

To run only a specific test:
    python -m unittest test_conv_xml_from_xml.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import os
import unittest
import datetime
import math

from libhydro.conv.xml import _from_xml as from_xml
from libhydro.core import (sitehydro, sitemeteo, _composant)


# -- strings ------------------------------------------------------------------
# contributor Sébastien ROMON
__version__ = '0.5.3'
__date__ = '2017-09-05'

# HISTORY
# V0.5.3 - SR - 2017-07-18
# Add tests on plages utilisation of Station and Capteur
# V0.5.2 - SR - 2017-07-18
# Add tests on new properties of Station
# V0.5.1 - SR - 2017-07-05
# Add test <Jaugeages>
# V0.5 SR - 2017-06-20
#  Add tests <CourbesCorrection>
# V0.4 SR - 2017-06-20
#  Add tests <CourbesTarage>
# V0.3 - 2017-04-20
#   update tests to new Contact.code type
#   some refactoring
# V0.2 - 2014-08-03
#   add the modelesprevision tests
# V0.1 - 2013-08-24
#   first shot


# -- class TestFromXmlSeriesMeteo ---------------------------------------------
class TestFromXmlSeriesMeteo(unittest.TestCase):

    """FromXmlSeriesMeteo class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '2', 'seriesmeteo.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'seriesobselab',
                 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['sitesmeteo'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertNotEqual(self.data['seriesmeteo'], [])
        self.assertEqual(self.data['simulations'], [])
        # self.assertEqual(len(self.data['sitesmeteo']), 1)
        self.assertEqual(len(self.data['seriesmeteo']), 3)

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '2')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod,
                         datetime.datetime(2010, 2, 26, 23, 55, 30))
        self.assertEqual(scenario.emetteur.contact.code, '1')
        self.assertEqual(scenario.emetteur.intervenant.code, 1537)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_serie_RR(self):
        """Serie RR test."""
        for serie in self.data['seriesmeteo']:
            if serie.grandeur.typemesure == 'RR':
                break
        self.assertEqual(serie.grandeur.sitemeteo.code, '987654321')
        self.assertEqual(serie.duree, datetime.timedelta(minutes=10))
        self.assertEqual(serie.dtdeb,
                         datetime.datetime(2015, 1, 2, 14, 18, 19))
        self.assertEqual(serie.dtfin,
                         datetime.datetime(2015, 1, 5, 10, 21, 54))
        self.assertEqual(serie.dtprod,
                         datetime.datetime(2015, 2, 6, 23, 54, 25))
        # (dte) res mth qal qua ctxt statut
        self.assertEqual(serie.observations.iloc[0].tolist(),
                         [15.2, 14, 20, 90, 1, 8])
        self.assertEqual(serie.observations.loc['2015-01-02 16:00'].tolist(),
                         [13.9, 10, 16, 100, 0, 4])
        self.assertEqual(serie.observations['statut'].tolist(),
                         [8, 4, 0, 16])

    def test_serie_TA(self):
        """Serie TA test."""
        for serie in self.data['seriesmeteo']:
            if serie.grandeur.typemesure == 'TA':
                break
        self.assertEqual(serie.grandeur.sitemeteo.code, '123456789')
        self.assertEqual(serie.duree, datetime.timedelta(minutes=0))
        self.assertEqual(serie.dtdeb, None)
        self.assertEqual(serie.dtfin, None)
        self.assertEqual(serie.dtprod, None)
        # (dte) res mth qal qua
        self.assertEqual(serie.observations.iloc[0].tolist()[:3],
                         [23.1, 0, 16])
        self.assertTrue(math.isnan(serie.observations.iloc[0]['qua'].item()))
        # self.assertEqual(serie.observations.loc['2010-02-26 13:00'].tolist(),
        #                  [8, 0, 16, 75])

    def test_without_obs(self):
        """Serie without obs test."""
        serie = self.data['seriesmeteo'][2]
        self.assertIsNone(serie.observations)

    @unittest.skip("todo: obs without res")
    def test_without_res(self):
        """Serie with one obs but without res ."""
        serie = self.data['seriesmeteo'][3]
        self.assertIsNotNone(serie.observations)

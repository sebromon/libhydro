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


# -- class TestFromXmlSeriesHydro ---------------------------------------------
class TestFromXmlSeriesHydro(unittest.TestCase):
    """FromXmlSeriesMeteo class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '2', 'serieshydro.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'seriesobselab',
                 'seriesobselabmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['sitesmeteo'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertNotEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['seriesmeteo'], [])
        self.assertEqual(self.data['simulations'], [])

    def test_full_serie(self):
        """Test serie with all tags"""
        serie = self.data['serieshydro'][0]
        dtdeb = datetime.datetime(2014, 11, 4, 10, 56, 41)
        dtfin = datetime.datetime(2014, 12, 2, 8, 15, 27)
        dtprod = datetime.datetime(2015, 9, 17, 9, 11, 47)

        self.assertEqual((serie.entite.code, serie.grandeur, serie.dtdeb,
                          serie.dtfin, serie.dtprod, serie.contact.code,
                          serie.sysalti, serie.perime),
                         ('A1234567', 'Q', dtdeb, dtfin, dtprod, '247',
                          1, True))
        self.assertEqual(serie.pdt.to_int(), 5)
        self.assertEqual(len(serie.observations), 1)
        self.assertEqual(serie.observations.loc['2014-11-04 11:05:00'].tolist(),
                         [1547.1, 14, 20, 1, 8])

    def test_minimal_serie(self):
        """Serie and obs with only mandatory tags"""
        serie = self.data['serieshydro'][1]
        self.assertEqual((serie.entite.code, serie.grandeur, serie.dtdeb,
                          serie.dtfin, serie.dtprod, serie.contact,
                          serie.sysalti, serie.perime),
                         ('B234567890', 'H', None, None, None, None,
                          31, None))
        self.assertEqual(serie.pdt, None)
        self.assertEqual(len(serie.observations), 1)
        self.assertEqual(serie.observations.loc['2014-11-04 11:05:00'].tolist(),
                         [1547.1, 0, 16, 0, 0])

    def test_serie_without_obs(self):
        """Serie without obs"""
        serie = self.data['serieshydro'][2]
        dtdeb = datetime.datetime(2017, 9, 8, 6, 49, 26)
        dtfin = datetime.datetime(2017, 9, 13, 17, 18, 37)
        dtprod = datetime.datetime(2018, 2, 5, 11, 48, 59)
        self.assertEqual((serie.entite.code, serie.grandeur, serie.dtdeb,
                          serie.dtfin, serie.dtprod, serie.contact,
                          serie.sysalti, serie.perime),
                         ('C98765432101', 'H', dtdeb, dtfin, dtprod, None,
                          31, True))
        self.assertIsNone(serie.observations)

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
                 'seriesobselabmeteo', 'simulations')))
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
        self.assertEqual(serie.observations.iloc[0]['statut'].item(), 0)
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


# -- class TestFromXmlSeriesMeteo ---------------------------------------------
class TestFromXmlSeriesObsElab(unittest.TestCase):

    """FromXmlSeriesObsElab( class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '2', 'obsselab.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'seriesobselab',
                 'seriesobselabmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['sitesmeteo'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['seriesmeteo'], [])
        self.assertEqual(self.data['simulations'], [])
        self.assertNotEqual(self.data['seriesobselab'], [])

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

    def test_serie_qmnj(self):
        """Serie QMNJ test."""
        serie = self.data['seriesobselab'][0]
        self.assertEqual(serie.entite.code, 'K1234567')
        self.assertEqual(serie.pdt.to_int(), 3)
        self.assertEqual(serie.dtdeb,
                         datetime.datetime(2011, 12, 9, 17, 11, 23))
        self.assertEqual(serie.dtfin,
                         datetime.datetime(2012, 2, 4, 15, 9, 37))
        self.assertEqual(serie.dtprod,
                         datetime.datetime(2013, 4, 17, 8, 27, 48))
        self.assertEqual(serie.dtdesactivation,
                         datetime.datetime(2015, 8, 11, 13, 4, 12))
        self.assertEqual(serie.dtactivation,
                         datetime.datetime(2010, 11, 3, 14, 51, 40))

        self.assertEqual(serie.sysalti, 1)
        self.assertEqual(serie.glissante, False)

        self.assertEqual(serie.dtdebrefalti,
                         datetime.datetime(2008, 3, 24, 6, 11, 27))
        self.assertEqual(serie.contact.code, '54')

        # (dte) res mth qal qua ctxt statut
        self.assertEqual(serie.observations.iloc[0].tolist(),
                         [873.1, 4, 20, 1, 8])
#         self.assertEqual(serie.observations.loc['2015-01-02 16:00'].tolist(),
#                          [13.9, 10, 16, 100, 0, 4])
#         self.assertEqual(serie.observations['statut'].tolist(),
#                          [8, 4, 0, 16])

    @unittest.skip("todo: obs without res")
    def test_serie_TA(self):
        """Serie TA test."""
        pass
        # self.assertEqual(serie.observations.loc['2010-02-26 13:00'].tolist(),
        #                  [8, 0, 16, 75])

    @unittest.skip("todo: obs without res")
    def test_without_obs(self):
        """Serie without obs test."""
        serie = self.data['seriesmeteo'][2]
        self.assertIsNone(serie.observations)

    @unittest.skip("todo: obs without res")
    def test_without_res(self):
        """Serie with one obs but without res ."""
        serie = self.data['seriesmeteo'][3]
        self.assertIsNotNone(serie.observations)


# -- class TestFromXmlSeriesObsElabMeteo --------------------------------------
class TestFromXmlSeriesObsElabMeteo(unittest.TestCase):

    """XmlSeriesObsElabMeteo class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '2', 'obsselabmeteo.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'seriesobselab',
                 'seriesobselabmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['sitesmeteo'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['seriesmeteo'], [])
        self.assertEqual(self.data['simulations'], [])
        self.assertEqual(self.data['seriesobselab'], [])
        self.assertNotEqual(self.data['seriesobselabmeteo'], [])

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

    def test_serie_ipa(self):
        serie = self.data['seriesobselabmeteo'][0]
        self.assertEqual(serie.site.sitemeteo.code, '012345678')
        self.assertEqual(serie.site.ponderation, 0.51)
        self.assertEqual(serie.grandeur, 'RR')
        self.assertEqual(serie.typeserie, 2)
        self.assertEqual(serie.dtdeb,
                         datetime.datetime(2017, 4, 18, 15, 16, 14))
        self.assertEqual(serie.dtfin,
                         datetime.datetime(2017, 5, 2, 8, 51, 43))
        self.assertEqual(serie.duree, datetime.timedelta(seconds=3600))

        self.assertEqual(serie.ipa.coefk, 0.21)
        self.assertEqual(serie.ipa.npdt, 5)
        self.assertEqual(len(serie.observations), 2)
        self.assertEqual(serie.observations.iloc[0].tolist(),
                         [10.4, 12.0, 20.0, 88.4, 16.0])
        obs = serie.observations.loc['2017-04-20 13:21:08'].iloc[0].tolist()
        self.assertEqual(obs[0:3], [11.9, 0.0, 16.0])
        self.assertTrue(math.isnan(obs[3]))
        self.assertEqual(obs[4], 0.0)

    def test_serie_lamedeau(self):
        serie = self.data['seriesobselabmeteo'][1]
        self.assertEqual(serie.site.code, 'Z7654321')
        self.assertEqual(serie.grandeur, 'RR')
        self.assertEqual(serie.typeserie, 1)
        self.assertEqual(serie.dtdeb,
                         datetime.datetime(2011, 8, 17, 19, 24, 16))
        self.assertEqual(serie.dtfin,
                         datetime.datetime(2012, 2, 8, 15, 29, 31))
        self.assertEqual(serie.duree, datetime.timedelta(seconds=1800))

        self.assertIsNone(serie.ipa)

        self.assertEqual(len(serie.observations), 2)
        self.assertEqual(serie.observations.iloc[0].tolist(),
                         [28.8, 12.0, 0.0, 33.1, 12.0])
        obs = serie.observations.loc['2011-12-15 08:09:10'].iloc[0].tolist()
        self.assertEqual(obs[0:3], [38.1, 0.0, 16.0])
        self.assertTrue(math.isnan(obs[3]))
        self.assertEqual(obs[4], 0.0)

    def test_minimal_serie(self):
        serie = self.data['seriesobselabmeteo'][2]
        self.assertEqual(serie.site.code, 'F3214321')
        self.assertEqual(serie.grandeur, 'RR')
        self.assertEqual(serie.typeserie, 1)
        self.assertIsNone(serie.dtdeb)
        self.assertIsNone(serie.dtfin)
        self.assertIsNone(serie.duree)

        self.assertIsNone(serie.ipa)

        self.assertEqual(len(serie.observations), 1)
        obs = serie.observations.loc['2013-05-04 13:11:26'].iloc[0].tolist()
        self.assertEqual(obs[0:3], [55.8, 0.0, 16.0])
        self.assertTrue(math.isnan(obs[3]))
        self.assertEqual(obs[4], 0.0)


# -- class TestFromXmlCourbesTarage --------------------------------------
class TestFromXmlCourbesTarage(unittest.TestCase):
    """XmlSeriesObsElabMeteo class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '2', 'courbestarage.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'seriesobselab',
                 'seriesobselabmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['sitesmeteo'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['seriesmeteo'], [])
        self.assertEqual(self.data['simulations'], [])
        self.assertEqual(self.data['seriesobselab'], [])
        self.assertEqual(self.data['seriesobselabmeteo'], [])
        self.assertNotEqual(self.data['courbestarage'], [])

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

    def test_full_courbetarage(self):
        courbe = self.data['courbestarage'][0]
        self.assertEqual(courbe.code, '1514')
        self.assertEqual(courbe.libelle, 'Libellé courbe')
        self.assertEqual(courbe.typect, 0)
        self.assertEqual(courbe.dtcreation, datetime.datetime(2015, 5, 4,
                                                              11, 16, 49))
        self.assertEqual(courbe.limiteinf, 136.5)
        self.assertEqual(courbe.limitesup, 289.4)
        self.assertEqual(courbe.limiteinfpub, 138.4)
        self.assertEqual(courbe.limitesuppub, 256.7)
        self.assertEqual(courbe.dn, 1.4)
        self.assertEqual(courbe.alpha, 1.1)
        self.assertEqual(courbe.beta, 1.3)
        self.assertEqual(courbe.commentaire, 'Commentaire')
        self.assertEqual(courbe.station.code, 'A123456789')
        self.assertEqual(courbe.contact.code, '144')

        self.assertEqual(len(courbe.pivots), 2)
        pivot1 = courbe.pivots[0]
        self.assertEqual(pivot1.hauteur, 58.4)
        self.assertEqual(pivot1.debit, 1547.1)
        pivot2 = courbe.pivots[1]
        self.assertEqual(pivot2.hauteur, 300.4)
        self.assertEqual(pivot2.debit, 3541.3)

        self.assertEqual(len(courbe.periodes), 2)
        periode = courbe.periodes[0]
        self.assertEqual(periode.dtdeb, datetime.datetime(2010, 9, 23,
                                                          8, 15, 41))
        self.assertEqual(periode.dtfin, datetime.datetime(2018, 4, 14,
                                                          17, 54, 49))
        self.assertEqual(periode.etat, 12)
        self.assertEqual(len(periode.histos), 2)
        histo1 = periode.histos[0]
        self.assertEqual(histo1.dtactivation, datetime.datetime(2015, 2, 22,
                                                                11, 12, 4))
        self.assertEqual(histo1.dtdesactivation, datetime.datetime(2016, 10, 2,
                                                                   16, 50, 11))

        histo2 = periode.histos[1]
        self.assertEqual(histo2.dtactivation, datetime.datetime(2017, 1, 17,
                                                                12, 10, 33))
        self.assertEqual(histo2.dtdesactivation, datetime.datetime(2018, 3, 15,
                                                                   14, 13, 8))

        # période2
        periode2 = courbe.periodes[1]
        self.assertEqual(periode2.dtdeb, datetime.datetime(2018, 5, 1,
                                                           7, 19, 51))
        self.assertIsNone(periode2.dtfin)
        self.assertEqual(periode2.etat, 4)
        self.assertEqual(len(periode2.histos), 1)
        histo = periode2.histos[0]
        self.assertEqual(histo.dtactivation, datetime.datetime(2018, 5, 2,
                                                               17, 18, 37))
        self.assertIsNone(histo.dtdesactivation)

        self.assertEqual(courbe.dtmaj, datetime.datetime(2018, 4, 16,
                                                         7, 9, 3))
        self.assertEqual(courbe.commentaireprive, 'Commentaire privé')

    def test_min_courbetarage(self):
        courbe = self.data['courbestarage'][1]
        self.assertEqual(courbe.code, '159874')
        self.assertEqual(courbe.libelle, 'Lb')
        self.assertEqual(courbe.typect, 4)
        self.assertIsNone(courbe.dtcreation)
        self.assertIsNone(courbe.limiteinf)
        self.assertIsNone(courbe.limitesup)
        self.assertIsNone(courbe.limiteinfpub)
        self.assertIsNone(courbe.limitesuppub)
        self.assertIsNone(courbe.dn)
        self.assertIsNone(courbe.alpha)
        self.assertIsNone(courbe.beta)
        self.assertIsNone(courbe.commentaire)
        self.assertEqual(courbe.station.code, 'Z987654321')
        self.assertIsNone(courbe.contact)

        self.assertEqual(len(courbe.pivots), 0)

        self.assertEqual(len(courbe.periodes), 0)

        self.assertIsNone(courbe.dtmaj)
        self.assertIsNone(courbe.commentaireprive)

    def test_courbetarage_puissance(self):
        courbe = self.data['courbestarage'][2]
        self.assertEqual(courbe.code, '4321')
        self.assertEqual(courbe.libelle, 'Courbe puissance')
        self.assertEqual(courbe.typect, 4)
        self.assertIsNone(courbe.dtcreation)
        self.assertIsNone(courbe.limiteinf)
        self.assertIsNone(courbe.limitesup)
        self.assertIsNone(courbe.limiteinfpub)
        self.assertIsNone(courbe.limitesuppub)
        self.assertIsNone(courbe.dn)
        self.assertIsNone(courbe.alpha)
        self.assertIsNone(courbe.beta)
        self.assertIsNone(courbe.commentaire)
        self.assertEqual(courbe.station.code, 'C123454321')
        self.assertEqual(courbe.contact.code, '22')

        self.assertEqual(len(courbe.pivots), 2)
        pivot1 = courbe.pivots[0]
        self.assertEqual(pivot1.hauteur, 76.4)
        self.assertEqual(pivot1.vara, 1)
        self.assertEqual(pivot1.varb, 1)
        self.assertEqual(pivot1.varh, 1)
        pivot2 = courbe.pivots[1]
        self.assertEqual(pivot2.hauteur, 541.3)
        self.assertEqual(pivot2.vara, 1.3)
        self.assertEqual(pivot2.varb, 1.1)
        self.assertEqual(pivot2.varh, 512.9)

        self.assertEqual(len(courbe.periodes), 1)
        periode = courbe.periodes[0]
        self.assertEqual(periode.dtdeb, datetime.datetime(2016, 7, 11,
                                                          15, 8, 34))
        self.assertEqual(periode.dtfin, datetime.datetime(2050, 2, 1,
                                                          10, 0, 0))
        self.assertEqual(periode.etat, 8)
        self.assertEqual(len(periode.histos), 1)
        histo1 = periode.histos[0]
        self.assertEqual(histo1.dtactivation, datetime.datetime(2017, 1, 17,
                                                                12, 10, 33))
        self.assertIsNone(histo1.dtdesactivation)

        self.assertEqual(courbe.dtmaj, datetime.datetime(2017, 12, 9,
                                                         11, 51, 50))
        self.assertIsNone(courbe.commentaireprive)

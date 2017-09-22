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
from libhydro.core import (sitehydro, sitemeteo)


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


# -- class TestFromXmlIntervenants --------------------------------------------
class TestFromXmlIntervenants(unittest.TestCase):

    """FromXmlIntervenants class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'intervenants.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertNotEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['simulations'], [])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(
            scenario.dtprod, datetime.datetime(2001, 12, 17, 4, 30, 47))
        self.assertEqual(scenario.emetteur.intervenant.code, 1537)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.emetteur.contact.code, '525')
        self.assertEqual(
            scenario.destinataire.intervenant.code, 12345671234567)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SIRET')
        self.assertEqual(scenario.destinataire.contact.code, '2')

    def test_intervenant_0(self):
        """intervenant 0 test."""
        # intervenant
        i = self.data['intervenants'][0]
        self.assertEqual(i.code, 11)
        self.assertEqual(i.origine, 'SANDRE')
        self.assertEqual(i.nom, 'Nom')
        self.assertEqual(i.mnemo, 'Mnemo')
        # contacts
        self.assertEqual(len(i.contacts), 2)
        c = i.contacts[0]
        self.assertEqual(c.code, '1')
        self.assertEqual(c.nom, 'Nom')
        self.assertEqual(c.prenom, 'Prenom')
        self.assertEqual(c.civilite, 1)
        self.assertEqual(c.intervenant, i)
        self.assertEqual(c.profilasstr, '001')
        c = i.contacts[1]
        self.assertEqual(c.code, '2')
        self.assertEqual(c.nom, 'Nom2')
        self.assertEqual(c.prenom, 'Prenom2')
        self.assertEqual(c.civilite, 2)
        self.assertEqual(c.intervenant, i)
        self.assertEqual(c.profilasstr, '010')

    def test_intervenant_1(self):
        """intervenant 1 test."""
        # intervenant
        i = self.data['intervenants'][1]
        self.assertEqual(i.code, 12345671234567)
        self.assertEqual(i.origine, 'SIRET')
        self.assertEqual(i.nom, 'Nom Sirét')
        self.assertEqual(i.mnemo, 'Captâîn Mnémo')
        # contacts
        self.assertEqual(len(i.contacts), 1)
        c = i.contacts[0]
        self.assertEqual(c.code, '5')
        self.assertEqual(c.nom, 'Nom Contaçt')
        self.assertEqual(c.prenom, 'Prenom Contaçt')
        self.assertEqual(c.civilite, 3)
        self.assertEqual(c.intervenant, i)
        self.assertEqual(c.profilasstr, '100')


# -- class TestFromXmlSitesHydro ----------------------------------------------
class TestFromXmlSitesHydros(unittest.TestCase):

    """FromXmlSitesHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'siteshydro.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertNotEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['simulations'], [])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(
            scenario.dtprod, datetime.datetime(2010, 2, 26, 12, 53, 10))
        self.assertEqual(scenario.emetteur.contact.code, '1069')
        self.assertEqual(scenario.emetteur.intervenant.code, 25)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_sitehydro_0(self):
        """Sitehydro 0 test."""
        sh = self.data['siteshydro'][0]
        self.assertEqual(sh.code, 'A1984310')
        self.assertEqual(sh.typesite, 'REEL')

    def test_sitehydro_1(self):
        """Sitehydro 1 test."""
        # check site
        sh = self.data['siteshydro'][1]
        self.assertEqual(sh.code, 'O1984310')
        self.assertEqual(
            sh.libelle, 'Le Touch à Toulouse [Saint-Martin-du-Touch]')
        self.assertEqual(sh.libelleusuel, 'St-Martin-du-Touch')
        self.assertEqual(sh.typesite, 'SOURCE')
        self.assertEqual(sh.code, 'O1984310')
        self.assertEqual(sh.communes, ['11354', '11355', '2B021'])
        self.assertEqual(len(sh.stations), 3)
        # check stations
        for i in range(1, 3):
            self.assertEqual(sh.stations[i - 1].code, 'O19843100%i' % i)
            self.assertEqual(sh.stations[i - 1].libelle,
                             '%s - station %i' % (sh.libelle, i))
            self.assertEqual(sh.stations[i - 1].typestation, 'LIMNI')
            self.assertEqual(sh.stations[i - 1].libellecomplement,
                             'station %i' % i)

        # check plages d'utilisation
        self.assertEqual(len(sh.stations[0].plages_utilisation), 2)
        plage = sh.stations[0].plages_utilisation[0]
        self.assertEqual(plage.dtdeb,
                         datetime.datetime(2015, 2, 14, 11, 54, 6))
        self.assertEqual(plage.dtfin,
                         datetime.datetime(2016, 9, 21, 6, 19, 31))
        self.assertEqual(plage.dtactivation,
                         datetime.datetime(2017, 3, 17, 17, 38, 21))
        self.assertEqual(plage.dtdesactivation,
                         datetime.datetime(2017, 4, 29, 19, 51, 48))
        self.assertEqual(plage.active, False)

        plage = sh.stations[0].plages_utilisation[1]
        self.assertEqual(plage.dtdeb,
                         datetime.datetime(2020, 11, 3, 15, 2, 3))
        self.assertIsNone(plage.dtfin)
        self.assertIsNone(plage.dtactivation)
        self.assertIsNone(plage.dtdesactivation)
        self.assertIsNone(plage.active)

        self.assertEqual(sh.stations[0].niveauaffichage, 911)
        self.assertEqual(sh.stations[1].niveauaffichage, 0)

    def test_sitehydro_2(self):
        """Sitehydro 2 test."""
        # check site
        sh = self.data['siteshydro'][2]
        self.assertEqual(sh.code, 'O2000040')
        self.assertEqual(sh.typesite, 'REEL')
        # check station
        station = sh.stations[0]
        self.assertEqual(station.libellecomplement, 'échelle principale')
        self.assertEqual(station.coord.x, 15)
        self.assertEqual(station.coord.y, 16)
        self.assertEqual(station.coord.proj, 26)

    def test_sitehydro_3(self):
        """Sitehydro 3 test."""
        # check site
        site = self.data['siteshydro'][3]
        self.assertEqual(site.coord.x, 618766)
        self.assertEqual(site.coord.y, 1781803)
        self.assertEqual(site.coord.proj, 26)
        self.assertEqual(site.codeh2, 'O1235401')
        self.assertEqual(len(site.tronconsvigilance), 2)
        self.assertEqual(site.tronconsvigilance[0].code, 'AG3')
        self.assertEqual(site.tronconsvigilance[1].code, 'AG5')
        self.assertEqual(
            site.tronconsvigilance[1].libelle, 'Troncon Adour àvâl')
        self.assertEqual(site.entitehydro, 'Y1524018')
        self.assertEqual(site.tronconhydro, 'O0011532')
        self.assertEqual(site.zonehydro, 'H420')
        self.assertEqual(site.precisioncoursdeau, 'bras principal')
        # check station
        station = site.stations[0]
        self.assertEqual(station.ddcs, ['10', '1000000001'])
        self.assertEqual(station.commune, '11354')
        self.assertEqual(station.codeh2, 'O1712510')
        self.assertEqual(station.niveauaffichage, 1)
        self.assertEqual(station.libellecomplement, 'Complément du libellé')
        self.assertEqual(station.descriptif, 'Station située à Auterive')
        self.assertEqual(station.dtmaj,
                         datetime.datetime(2017, 7, 17, 11, 23, 34))
        self.assertEqual(station.pointk, 153.71)
        self.assertEqual(station.dtmiseservice,
                         datetime.datetime(1991, 10, 7, 14, 15, 16))
        self.assertEqual(station.dtfermeture,
                         datetime.datetime(2012, 4, 21, 19, 58, 3))
        self.assertEqual(station.surveillance, True)
        # checkcapteurs
        capteurs = station.capteurs
        self.assertEqual(len(capteurs), 2)
        self.assertEqual(capteurs[0].code, 'O17125100102')
        self.assertEqual(capteurs[0].typemesure, 'H')
        self.assertEqual(capteurs[1].code, 'O17125100101')
        self.assertEqual(capteurs[1].typemesure, 'H')
        self.assertEqual(capteurs[1].codeh2, 'O1712510')

        # check plages utilisatino capteurs
        self.assertEqual(len(capteurs[0].plages_utilisation), 0)
        self.assertEqual(len(capteurs[1].plages_utilisation), 2)
        plage = capteurs[1].plages_utilisation[0]
        self.assertEqual(plage.dtdeb,
                         datetime.datetime(2009, 11, 3, 15, 19, 18))
        self.assertEqual(plage.dtfin,
                         datetime.datetime(2015, 3, 21, 11, 14, 47))
        self.assertEqual(plage.dtactivation,
                         datetime.datetime(2014, 12, 14, 18, 27, 32))
        self.assertEqual(plage.dtdesactivation,
                         datetime.datetime(2015, 10, 25, 19, 13, 4))
        self.assertEqual(plage.active, True)

        plage = capteurs[1].plages_utilisation[1]
        self.assertEqual(plage.dtdeb,
                         datetime.datetime(2016, 1, 15, 12, 14, 13))
        self.assertIsNone(plage.dtfin)
        self.assertIsNone(plage.dtactivation)
        self.assertIsNone(plage.dtdesactivation)
        self.assertIsNone(plage.active)

    def test_error_1(self):
        """Xml file with namespace error test."""
        with self.assertRaises(ValueError):
            # *([os.path.join('data', 'xml', '1.1', 'siteshydro.xml')])
            from_xml._parse(*([os.path.join(
                'data', 'xml', '1.1', 'siteshydro_with_namespace.xml')]))


# -- class TestFromXmlSeuilsHydro ---------------------------------------------
class TestFromXmlSeuilsHydros(unittest.TestCase):

    """FromXmlSeuilsHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'seuilshydro.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertNotEqual(self.data['siteshydro'], [])
        self.assertNotEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['simulations'], [])
        self.assertEqual(len(self.data['siteshydro']), 5)
        self.assertEqual(len(self.data['seuilshydro']), 9)

    def test_seuils_sitehydro_0(self):
        """Test seuils sitehydro 0."""
        # check the sitehydro
        sh = self.data['siteshydro'][0]
        self.assertEqual(sh.code, 'U2655010')

        # find the seuil
        for seuil in self.data['seuilshydro']:
            if seuil.sitehydro.code == 'U2655010' and seuil.code == '2214':
                break

        # check the seuil
        # self.assertEqual(seuil.sh, sh)  # FIXME
        self.assertEqual(seuil.typeseuil, 1)
        self.assertEqual(seuil.duree, 0)
        self.assertEqual(seuil.nature, 32)
        self.assertEqual(seuil.libelle, 'Crue du 24/11/2003')
        self.assertEqual(seuil.mnemo, 'Mnemonique')
        self.assertEqual(seuil.gravite, 65)
        self.assertEqual(seuil.commentaire, 'Commentaire du seuil')
        self.assertEqual(seuil.publication, True)
        self.assertEqual(seuil.valeurforcee, True)
        self.assertEqual(seuil.dtmaj, datetime.datetime(2012, 2, 19, 8, 25))
        self.assertEqual(seuil._strict, True)

        # check the values
        self.assertEqual(len(seuil.valeurs), 1)
        self.assertEqual(seuil.valeurs[0].valeur, 7000465)
        # self.assertEqual(seuil.valeurs[0].seuil, seuil)  # FIXME
        self.assertEqual(seuil.valeurs[0].entite, seuil.sitehydro)
        self.assertEqual(seuil.valeurs[0].tolerance, 0)
        self.assertEqual(seuil.valeurs[0].dtactivation,
                         datetime.datetime(2010, 5, 17, 13, 40, 2))
        self.assertEqual(seuil.valeurs[0].dtdesactivation,
                         datetime.datetime(2012, 2, 19, 9, 28))
        self.assertEqual(seuil.valeurs[0]._strict, True)

    def test_seuils_sitehydro_1(self):
        """Test seuils sitehydro 1."""
        # check the sitehydro
        sh = self.data['siteshydro'][1]
        self.assertEqual(sh.code, 'O2000040')

        # find the seuil
        for seuil in self.data['seuilshydro']:
            if seuil.sitehydro.code == 'O2000040' and seuil.code == '82':
                break

        # check the seuil
        # self.assertEqual(seuil.sitehydro, sitehydro)  # FIXME
        self.assertEqual(seuil.typeseuil, 2)
        self.assertEqual(seuil.duree, 60)
        self.assertEqual(seuil.nature, 32)
        self.assertEqual(seuil.libelle, 'Gradient durée 60')
        self.assertEqual(seuil.mnemo, None)
        self.assertEqual(seuil.gravite, None)
        self.assertEqual(seuil.commentaire, None)
        self.assertEqual(seuil.publication, False)
        self.assertEqual(seuil.valeurforcee, None)
        self.assertEqual(seuil.dtmaj,
                         datetime.datetime(2014, 3, 23, 9, 51, 56))

        # check the values
        self.assertEqual(len(seuil.valeurs), 4)
        self.assertEqual(seuil.valeurs[0].valeur, 85)
        self.assertEqual(seuil.valeurs[1].valeur, 4380)
        self.assertEqual(seuil.valeurs[2].valeur, 3520)
        self.assertEqual(seuil.valeurs[3].valeur, 8320)
        self.assertEqual(seuil.valeurs[0].seuil, seuil)
        self.assertEqual(seuil.valeurs[0].entite.code, 'O2000040')
        self.assertEqual(seuil.valeurs[1].entite.code, 'O200004001')
        self.assertEqual(seuil.valeurs[2].entite.code, 'O200004002')
        self.assertEqual(seuil.valeurs[3].entite.code, 'O200004003')
        self.assertEqual(seuil.valeurs[0].tolerance, 5)
        self.assertEqual(seuil.valeurs[1].tolerance, 0)
        self.assertEqual(seuil.valeurs[2].tolerance, None)
        self.assertEqual(seuil.valeurs[3].tolerance, 10)
        self.assertEqual(seuil.valeurs[0].dtactivation, None)
        self.assertEqual(seuil.valeurs[1].dtactivation,
                         datetime.datetime(2010, 6, 10, 10, 52, 57))
        self.assertEqual(seuil.valeurs[2].dtactivation,
                         datetime.datetime(2010, 6, 10, 11, 32, 57))
        self.assertEqual(seuil.valeurs[3].dtactivation,
                         datetime.datetime(2010, 6, 10, 11, 52, 57))
        self.assertEqual(seuil.valeurs[0].dtdesactivation, None)
        self.assertEqual(seuil.valeurs[1].dtdesactivation, None)
        self.assertEqual(seuil.valeurs[2].dtdesactivation,
                         datetime.datetime(2013, 10, 5, 5, 59, 29))
        self.assertEqual(seuil.valeurs[3].dtdesactivation, None)

    def test_seuils_sitehydro_2(self):
        """Test seuils sitehydro 2."""
        # find 4 seuils
        seuils = []
        for seuil in self.data['seuilshydro']:
            if seuil.sitehydro.code == 'O0144020' and \
                    seuil.code in [str(i) for i in range(1, 5)]:
                seuils.append(seuil)

        # check the seuils
        for i in range(4):
            self.assertEqual(seuils[i].sitehydro.code, 'O0144020')
            self.assertEqual(len(seuils[i].valeurs), 0)

    def test_seuils_sitehydro_3(self):
        """Test seuils sitehydro 3."""
        # find 2 seuils
        seuils = []
        for seuil in self.data['seuilshydro']:
            if seuil.sitehydro.code == 'O6793330' and \
                    seuil.code in ('338', '341'):
                seuils.append(seuil)

        # sort the seuils list
        seuils = sorted(seuils, key=lambda s: getattr(s, 'code'))

        # check the seuils
        for i in range(1):
            self.assertEqual(seuils[i].sitehydro.code, 'O6793330')
        self.assertEqual(seuils[0].mnemo, 'Seuil de vigilance JAUNE')
        self.assertEqual(len(seuils[0].valeurs), 2)
        # print(seuils[0].valeurs)
        self.assertEqual(seuils[0].valeurs[0].valeur, 100)
        self.assertEqual(seuils[0].valeurs[1].valeur, 3200)
        self.assertEqual(seuils[1].libelle, 'Crue du 08/04/1994')
        self.assertEqual(len(seuils[1].valeurs), 1)
        self.assertEqual(seuils[1].valeurs[0].valeur, 3500)

    def test_seuils_sitehydro_4(self):
        """Test seuils sitehydro 4."""
        # find the seuil
        seuils = []
        for seuil in self.data['seuilshydro']:
            if (seuil.sitehydro.code == 'O3334020'):
                seuils.append(seuil)

        # check we have only the seuil number 19
        self.assertEqual(len(seuils), 1)
        self.assertEqual(seuils[0].code, '19')
        self.assertEqual(seuils[0].libelle, 'Crue du 24/11/2003')
        seuil = seuils[0]

        # check the 4 seuil values
        for i in range(4):
            self.assertEqual(seuil.valeurs[i].valeur, i + 1)
            self.assertEqual(seuil.valeurs[i].entite, seuil.sitehydro)
            self.assertEqual(seuil.valeurs[i].seuil, seuil)

    def test_seuils_sitehydro_5(self):
        """Test seuils with a bad xml."""
        with self.assertRaises(ValueError):
            from_xml._parse(os.path.join(
                    'data', 'xml', '1.1', 'seuilshydro_inconsistent.xml'))


# -- class TestFromXmlSitesMeteo ----------------------------------------------
class TestFromXmlSitesMeteo(unittest.TestCase):

    """FromXmlSitesMeteo class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'sitesmeteo.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertNotEqual(self.data['sitesmeteo'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['seriesmeteo'], [])
        self.assertEqual(self.data['simulations'], [])
        # len
        self.assertEqual(len(self.data['sitesmeteo']), 1)

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod,
                         datetime.datetime(2010, 2, 26, 8, 5, 56))
        self.assertEqual(scenario.emetteur.contact.code, '26')
        self.assertEqual(scenario.emetteur.intervenant.code, 1520)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_sitemeteo_0(self):
        """Sitemeteo 0 test."""
        sm = self.data['sitesmeteo'][0]
        self.assertEqual(sm.code, '001072001')
        self.assertEqual(sm.libelle, 'CEYZERIAT_PTC')
        self.assertEqual(sm.libelleusuel, 'CEYZERIAT')
        self.assertEqual(sm.coord.x, 827652)
        self.assertEqual(sm.coord.y, 2112880)
        self.assertEqual(sm.coord.proj, 26)
        self.assertEqual(sm.commune, '35281')
        self.assertEqual(sm._strict, True)
        self.assertEqual(len(sm.grandeurs), 2)
        for grandeur in sm.grandeurs:
            self.assertEqual(grandeur.sitemeteo, sm)
        self.assertEqual(sm.grandeurs[0].typemesure, 'RR')
        self.assertEqual(sm.grandeurs[0].pdt, 4)
        self.assertEqual(sm.grandeurs[1].typemesure, 'VV')
        self.assertIsNone(sm.grandeurs[1].pdt)


# -- class TestFromXmlModelesPrevision ----------------------------------------
class TestFromXmlModelesPrevision(unittest.TestCase):

    """FromXmlModelesPrevision class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'modelesprevision.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['sitesmeteo'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertNotEqual(self.data['modelesprevision'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['seriesmeteo'], [])
        self.assertEqual(self.data['simulations'], [])
        # len
        self.assertEqual(len(self.data['modelesprevision']), 2)

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod,
                         datetime.datetime(2001, 12, 17, 4, 30, 47))
        self.assertEqual(scenario.emetteur.intervenant.code, 825)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.emetteur.contact.code, '222')
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.contact.code, '2')

    def test_modeleprevision_0(self):
        """Modeleprevision 0 test."""
        modeleprevision = self.data['modelesprevision'][0]
        self.assertEqual(modeleprevision.code, 'token')
        self.assertEqual(modeleprevision.libelle, 'String')
        self.assertEqual(modeleprevision.typemodele, 0)
        self.assertEqual(modeleprevision.description, 'String')

    def test_modeleprevision_1(self):
        """Modeleprevision 1 test."""
        modeleprevision = self.data['modelesprevision'][1]
        self.assertEqual(modeleprevision.code, 'token')
        self.assertEqual(modeleprevision.libelle, 'String')
        self.assertEqual(modeleprevision.typemodele, 0)
        self.assertEqual(modeleprevision.description, 'String')


# -- class TestFromXmlEvenements ----------------------------------------------
class TestFromXmlEvenements(unittest.TestCase):

    """FromXmlEvenements class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'evenements.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertNotEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['simulations'], [])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod,
                         datetime.datetime(2010, 2, 26, 7, 5))
        self.assertEqual(scenario.emetteur.contact.code, '26')
        self.assertEqual(scenario.emetteur.intervenant.code, 1520)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_evenement_0(self):
        """Evenement 0 test."""
        evenement = self.data['evenements'][0]
        self.assertTrue(isinstance(evenement.entite, sitehydro.Sitehydro))
        self.assertEqual(evenement.entite.code, 'A0010101')
        self.assertEqual(evenement.contact.code, '1')
        self.assertEqual(evenement.dt, datetime.datetime(1999, 8, 12, 0, 5))
        self.assertEqual(evenement.descriptif, "Arrachement de l'échelle")
        self.assertEqual(evenement.publication, 1)
        self.assertEqual(evenement.dtmaj,
                         datetime.datetime(2000, 5, 10, 22, 5))

    def test_evenement_1(self):
        """Evenement 1 test."""
        evenement = self.data['evenements'][1]
        self.assertTrue(isinstance(evenement.entite, sitehydro.Station))
        self.assertEqual(evenement.entite.code, 'Z853010101')
        self.assertEqual(evenement.contact.code, '8563')
        self.assertEqual(evenement.dt, datetime.datetime(2010, 2, 26, 9, 5))
        self.assertEqual(evenement.descriptif,
                         'Déplacement de la station de 22.5m')
        self.assertEqual(evenement.publication, 20)
        self.assertEqual(evenement.dtmaj,
                         datetime.datetime(2011, 1, 13, 10, 5))

    def test_evenement_2(self):
        """Evenement 2 test."""
        evenement = self.data['evenements'][2]
        self.assertTrue(isinstance(evenement.entite, sitemeteo.Sitemeteo))
        self.assertEqual(evenement.entite.code, '008530001')
        self.assertEqual(evenement.contact.code, '1')
        self.assertEqual(evenement.dt, datetime.datetime(1968, 2, 2, 23, 0))
        self.assertEqual(evenement.descriptif,
                         'Débouchage de la sonde de température')
        self.assertEqual(evenement.publication, 100)
        self.assertEqual(evenement.dtmaj,
                         datetime.datetime(2000, 1, 1, 22, 0))


# -- class TestFromXmlJaugeages ----------------------------------------------
class TestFromXmlJaugeages(unittest.TestCase):

    """FromXmlJaugeages class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'jaugeages.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements', 'jaugeages',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['simulations'], [])
        self.assertNotEqual(self.data['jaugeages'], [])

    def test_jaugeage_01(self):
        """check simple jaugeage"""
        jaugeage = self.data['jaugeages'][0]
        self.assertEqual(jaugeage.code, '184')

        self.assertIsNone(jaugeage.dte)
        self.assertIsNone(jaugeage.dtdeb)
        self.assertIsNone(jaugeage.debit)
        self.assertIsNone(jaugeage.dtfin)

        self.assertIsNone(jaugeage.section_mouillee)
        self.assertIsNone(jaugeage.perimetre_mouille)
        self.assertIsNone(jaugeage.largeur_miroir)
        self.assertIsNone(jaugeage.mode)
        self.assertIsNone(jaugeage.commentaire)
        self.assertIsNone(jaugeage.vitessemoy)
        self.assertIsNone(jaugeage.vitessemax)
        self.assertIsNone(jaugeage.vitessemoy_surface)

        self.assertEqual(jaugeage.site.code, 'K0101010')
        self.assertEqual(len(jaugeage.hauteurs), 0)
        self.assertIsNone(jaugeage.dtmaj)

    def test_jaugeage_02(self):
        """check full jaugeage"""
        jaugeage = self.data['jaugeages'][1]
        self.assertEqual(jaugeage.code, '159')
        self.assertEqual(jaugeage.dte, datetime.datetime(2015, 8, 3, 4, 5, 17))
        self.assertEqual(jaugeage.dtdeb,
                         datetime.datetime(2015, 8, 2, 6, 13, 34))
        self.assertEqual(jaugeage.debit, 1034.56)
        self.assertEqual(jaugeage.dtfin,
                         datetime.datetime(2015, 8, 3, 11, 39, 8))
        self.assertEqual(jaugeage.section_mouillee, 341.25)
        self.assertEqual(jaugeage.perimetre_mouille, 987.54)
        self.assertEqual(jaugeage.largeur_miroir, 156423.12)
        self.assertEqual(jaugeage.mode, 5)
        self.assertEqual(jaugeage.commentaire, 'Commentaire')
        self.assertEqual(jaugeage.vitessemoy, 17.54)
        self.assertEqual(jaugeage.vitessemax, 19.43)
        self.assertEqual(jaugeage.vitessemoy_surface, 18.87)
        self.assertEqual(jaugeage.site.code, 'A1234567')

        self.assertEqual(len(jaugeage.hauteurs), 3)
        hjaug1 = jaugeage.hauteurs[0]
        self.assertEqual(hjaug1.station.code, 'Z123456789')
        self.assertEqual(hjaug1.sysalti, 0)
        self.assertEqual(hjaug1.coteretenue, 149.17)
        self.assertEqual(hjaug1.cotedeb, 148.62)
        self.assertEqual(hjaug1.cotefin, 150.23)
        self.assertEqual(hjaug1.denivele, 1.51)
        self.assertEqual(hjaug1.distancestation, 1543.13)
        self.assertEqual(hjaug1.stationfille.code, 'B123456789')
        self.assertEqual(hjaug1.dtdeb_refalti,
                         datetime.datetime(2010, 11, 24, 5, 42, 31))
        hjaug2 = jaugeage.hauteurs[1]
        self.assertEqual(hjaug2.station.code, 'K987654321')
        self.assertEqual(hjaug2.sysalti, 31)
        self.assertEqual(hjaug2.coteretenue, 214.15)
        self.assertEqual(hjaug2.cotedeb, 212.67)
        self.assertEqual(hjaug2.cotefin, 216.99)
        self.assertEqual(hjaug2.distancestation, 846.21)
        self.assertEqual(hjaug2.stationfille.code, 'L987654321')
        self.assertEqual(hjaug2.dtdeb_refalti,
                         datetime.datetime(2015, 3, 26, 16, 14, 15))

        hjaug3 = jaugeage.hauteurs[2]
        self.assertEqual(hjaug3.station.code, 'V195436574')
        self.assertEqual(hjaug3.sysalti, 25)
        self.assertEqual(hjaug3.coteretenue, 214.15)
        self.assertIsNone(hjaug3.cotedeb)
        self.assertIsNone(hjaug3.cotefin)
        self.assertIsNone(hjaug3.distancestation)
        self.assertIsNone(hjaug3.stationfille)
        self.assertIsNone(hjaug3.dtdeb_refalti)

        self.assertEqual(jaugeage.dtmaj,
                         datetime.datetime(2017, 7, 4, 6, 20, 47))


# -- class TestFromXmlEvenements ----------------------------------------------
class TestFromXmlCourbesTarage(unittest.TestCase):

    """FromXmlCourbesTarage class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'courbestarage.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertNotEqual(self.data['courbestarage'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['simulations'], [])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod,
                         datetime.datetime(2017, 6, 20, 7, 47, 48))
        self.assertEqual(scenario.emetteur.contact.code, '74')
        self.assertEqual(scenario.emetteur.intervenant.code, 1178)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_courbetarage_0(self):
        """CourbeTarage 0 test."""
        ct = self.data['courbestarage'][0]
        self.assertEqual(ct.code, 'courbe tarage')
        self.assertEqual(ct.libelle, 'libellé')
        self.assertEqual(ct.typect, 0)
        self.assertEqual(ct.limiteinf, 156.12)
        self.assertEqual(ct.limitesup, 854.01)
        self.assertEqual(ct.dn, 1.15)
        self.assertEqual(ct.alpha, 1.23)
        self.assertEqual(ct.beta, 2.56)
        self.assertEqual(ct.commentaire, 'no comment')
        self.assertEqual(ct.station.code, 'A123456789')
        self.assertEqual(len(ct.pivots), 2)

        pivot1 = ct.pivots[0]
        self.assertEqual(pivot1.hauteur, 198.26)
        self.assertEqual(pivot1.qualif, 16)
        self.assertEqual(pivot1.debit, 20021.36)

        pivot2 = ct.pivots[1]
        self.assertEqual(pivot2.hauteur, 209.12)
        self.assertEqual(pivot2.qualif, 20)
        self.assertEqual(pivot2.debit, 30156.12)

        self.assertEqual(len(ct.periodes), 2)

        periode1 = ct.periodes[0]
        self.assertEqual(periode1.dtdeb, datetime.datetime(2015, 1, 2,
                                                           3, 4, 5))
        self.assertEqual(periode1.dtfin, datetime.datetime(2016, 10, 11,
                                                           12, 13, 14))
        self.assertEqual(periode1.etat, 0)
        self.assertEqual(len(periode1.histos), 2)
        histo1 = periode1.histos[0]
        self.assertEqual(histo1.dtactivation, datetime.datetime(2017, 5, 20,
                                                                6, 44, 23))
        self.assertEqual(histo1.dtdesactivation, datetime.datetime(2017, 6, 1,
                                                                   7, 57, 12))

        periode2 = ct.periodes[1]
        self.assertEqual(periode2.dtdeb, datetime.datetime(2017, 5, 9,
                                                           11, 56, 47))
        self.assertEqual(periode2.dtfin, datetime.datetime(2017, 6, 15,
                                                           23, 11, 18))
        self.assertEqual(periode2.etat, 8)

        self.assertEqual(ct.dtmaj, datetime.datetime(2017, 6, 19, 8, 1, 21))

    def test_courbetarage_1(self):
        """CourbeTarage puissance test."""
        ct = self.data['courbestarage'][1]
        self.assertEqual(ct.code, 'Courbe 1564')
        self.assertEqual(ct.libelle, 'Courbe puissance')
        self.assertEqual(ct.typect, 4)
        self.assertEqual(ct.limiteinf, 10.56)
        self.assertEqual(ct.limitesup, 987.12)
        self.assertIsNone(ct.dn)
        self.assertIsNone(ct.alpha)
        self.assertIsNone(ct.beta)
        self.assertEqual(ct.commentaire, 'commentaire')
        self.assertEqual(ct.station.code, 'W987654321')
        self.assertEqual(len(ct.pivots), 2)

        pivot1 = ct.pivots[0]
        self.assertEqual(pivot1.hauteur, 123.456)
        self.assertEqual(pivot1.qualif, 12)
        self.assertEqual(pivot1.vara, 1.06)
        self.assertEqual(pivot1.varb, 0.98)
        self.assertEqual(pivot1.varh, 2.31)

        pivot2 = ct.pivots[1]
        self.assertEqual(pivot2.hauteur, 198.64)
        self.assertEqual(pivot2.qualif, 20)
        self.assertEqual(pivot2.vara, 5.14)
        self.assertEqual(pivot2.varb, 2.35e-6)
        self.assertEqual(pivot2.varh, 45.14)

        self.assertEqual(len(ct.periodes), 1)

        periode1 = ct.periodes[0]
        self.assertEqual(periode1.dtdeb, datetime.datetime(2010, 3, 4,
                                                           15, 6, 20))
        self.assertEqual(periode1.dtfin, datetime.datetime(2011, 10, 24,
                                                           5, 19, 24))
        self.assertEqual(periode1.etat, 8)
        self.assertEqual(len(periode1.histos), 0)
        self.assertEqual(ct.dtmaj, datetime.datetime(2015, 9, 3, 1, 41, 34))

    def test_courbetarage_2(self):
        """CourbeTarage avec seulement les champs obligatoires"""
        ct = self.data['courbestarage'][2]
        self.assertEqual(ct.code, 'ct 987')
        self.assertEqual(ct.libelle, 'éàéà')
        self.assertEqual(ct.typect, 0)
        self.assertIsNone(ct.limiteinf)
        self.assertIsNone(ct.limitesup)
        self.assertIsNone(ct.dn)
        self.assertIsNone(ct.alpha)
        self.assertIsNone(ct.beta)
        self.assertIsNone(ct.commentaire)
        self.assertEqual(ct.station.code, 'B198524123')
        self.assertEqual(len(ct.pivots), 0)

        self.assertEqual(len(ct.periodes), 0)

        self.assertIsNone(ct.dtmaj)


# -- class TestFromXmlCourbesCorrection ----------------------------------------------
class TestFromXmlCourbesCorrection(unittest.TestCase):

    """FromXmlCourbesCorrection class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'courbescorrection.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['courbestarage'], [])
        self.assertNotEqual(self.data['courbescorrection'], [])
        self.assertEqual(len(self.data['courbescorrection']), 2)
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['simulations'], [])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod,
                         datetime.datetime(2017, 6, 20, 7, 47, 48))
        self.assertEqual(scenario.emetteur.contact.code, '74')
        self.assertEqual(scenario.emetteur.intervenant.code, 1178)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_courbecorrection_0(self):
        """CourbeTarage 0 test."""
        cc = self.data['courbescorrection'][0]
        self.assertEqual(cc.station.code, 'A123456789')
        self.assertEqual(cc.libelle, 'libellé courbe correction')
        self.assertEqual(cc.commentaire, 'commentaire cc')
        
        self.assertEqual(len(cc.pivots), 2)

        pivot1 = cc.pivots[0]
        self.assertEqual(pivot1.dte, datetime.datetime(2007, 3, 4, 12, 25, 34))
        self.assertEqual(pivot1.deltah, 10.56)
        self.assertEqual(pivot1.dtactivation,
                         datetime.datetime(2007, 4, 5, 11, 12, 13))
        self.assertEqual(pivot1.dtdesactivation,
                         datetime.datetime(2008, 5, 1, 22, 14, 54))

        pivot2 = cc.pivots[1]
        self.assertEqual(pivot2.dte, datetime.datetime(2008, 11, 20, 5, 41, 12))
        self.assertEqual(pivot2.deltah, -189.12)
        self.assertEqual(pivot2.dtactivation,
                         datetime.datetime(2009, 2, 27, 1, 55, 33))
        self.assertEqual(pivot2.dtdesactivation, None)
        
        
        self.assertEqual(cc.dtmaj, datetime.datetime(2017, 6, 21, 15, 3, 31))

    def test_courbecorrection_1(self):
        """CourbeTarage 1 test."""
        cc = self.data['courbescorrection'][1]
        self.assertEqual(cc.station.code, 'Z987654321')
        self.assertIsNone(cc.libelle)
        self.assertIsNone(cc.commentaire)
        self.assertEqual(len(cc.pivots), 0)
        self.assertIsNone(cc.dtmaj, None)

# -- class TestFromXmlSeriesHydro ---------------------------------------------
class TestFromXmlSeriesHydro(unittest.TestCase):

    """FromXmlSeriesHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'serieshydro.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertNotEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['simulations'], [])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod, datetime.datetime(2010, 2, 26, 7, 5))
        self.assertEqual(scenario.emetteur.contact.code, '26')
        self.assertEqual(scenario.emetteur.intervenant.code, 1520)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_serie_0(self):
        """Serie 0 test."""
        serie = self.data['serieshydro'][0]
        self.assertEqual(serie.entite.code, 'V7144010')
        self.assertEqual(serie.grandeur, 'Q')
        self.assertEqual(serie.statut, 4)
        self.assertEqual(serie.observations.iloc[0].tolist(),
                         [20992, 0, 16, True])
        self.assertEqual(serie.observations.loc['2010-02-26 11:15'].tolist(),
                         [21176, 0, 16, True])

    def test_serie_1(self):
        """Serie 1 test."""
        serie = self.data['serieshydro'][1]
        self.assertEqual(serie.entite.code, 'V714401001')
        self.assertEqual(serie.grandeur, 'Q')
        self.assertEqual(serie.statut, 4)
        self.assertEqual(serie.observations.iloc[0].tolist(),
                         [20, 12, 12, False])
        self.assertEqual(serie.observations.loc['2010-02-26 13:15'].tolist(),
                         [21, 12, 8, False])

    def test_serie_2(self):
        """Serie 2 test."""
        serie = self.data['serieshydro'][2]
        self.assertEqual(serie.entite.code, 'V71440100103')
        self.assertEqual(serie.grandeur, 'H')
        self.assertEqual(serie.statut, 4)
        self.assertEqual(serie.observations.loc['2010-02-26 13:10'].tolist(),
                         [680, 4, 20, True])
        self.assertEqual(serie.observations.loc['2010-02-26 13:15'].tolist(),
                         [684, 0, 20, True])
        self.assertEqual(serie.observations.loc['2010-02-26 14:55'].tolist(),
                         [670, 12, 20, True])

    def test_seriehydro_without_observation(self):
        """Test a unconventionnal seriehydro from bdhydro."""
        data = from_xml._parse(os.path.join(
                'data', 'xml', '1.1', 'serieshydro_without_observations.xml'))
        self.assertEqual(len(data['serieshydro']), 34)


# -- class TestFromXmlSeriesMeteo ---------------------------------------------
class TestFromXmlSeriesMeteo(unittest.TestCase):

    """FromXmlSeriesMeteo class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'seriesmeteo.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
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
        self.assertEqual(len(self.data['seriesmeteo']), 2)

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
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
        self.assertEqual(serie.grandeur.sitemeteo.code, '001033002')
        self.assertEqual(serie.duree, datetime.timedelta(minutes=60))
        self.assertEqual(serie.statut, 4)
        self.assertEqual(serie.dtdeb, datetime.datetime(2010, 2, 26, 12))
        self.assertEqual(serie.dtfin, datetime.datetime(2010, 2, 26, 13))
        self.assertEqual(serie.dtprod,
                         datetime.datetime(2010, 2, 26, 15, 13, 37))
        # (dte) res mth qal qua
        self.assertEqual(serie.observations.iloc[0].tolist(), [2, 0, 16, 100])
        self.assertEqual(serie.observations.loc['2010-02-26 13:00'].tolist(),
                         [8, 0, 16, 75])

    def test_serie_TA(self):
        """Serie TA test."""
        for serie in self.data['seriesmeteo']:
            if serie.grandeur.typemesure == 'TA':
                break
        self.assertEqual(serie.grandeur.sitemeteo.code, '02B033002')
        self.assertEqual(serie.duree, datetime.timedelta(minutes=0))
        self.assertEqual(serie.statut, 4)
        self.assertEqual(serie.dtdeb, datetime.datetime(2010, 2, 26, 14))
        self.assertEqual(serie.dtfin, datetime.datetime(2010, 2, 26, 14))
        self.assertEqual(serie.dtprod,
                         datetime.datetime(2010, 2, 26, 15, 13, 37))
        # (dte) res mth qal qua
        self.assertEqual(serie.observations.iloc[0].tolist()[:3], [4, 0, 16])
        self.assertTrue(math.isnan(serie.observations.iloc[0]['qua'].item()))
        # self.assertEqual(serie.observations.loc['2010-02-26 13:00'].tolist(),
        #                  [8, 0, 16, 75])

    def test_POM(self):
        """Serie POM test."""
        pom = from_xml._parse(os.path.join(
            'data', 'xml', '1.1', 'seriesmeteo_POM.xml'))['seriesmeteo']
        # 280 observations
        self.assertEqual(sum([len(s.observations) for s in pom]), 280)
        # 4 sitesmeteo and therefore 4 series
        self.assertEqual(len(pom), 4)

    def test_without_obs(self):
        """Serie without obs test."""
        serie = from_xml._parse(os.path.join(
            'data', 'xml', '1.1', 'seriesmeteo_without_observations.xml'))[
                'seriesmeteo'][0]
        self.assertEqual(serie.observations['res'].values.tolist(),
                         [5.8, 23.0, 45.8])
        serie.resample(datetime.timedelta(hours=1))
        l = serie.observations['res'].values.tolist()
        self.assertTrue(math.isnan(l[2]))
        l.pop(2)
        self.assertEqual(l, [5.8, 23.0, 45.8])


# -- class TestFromXmlSimulations ---------------------------------------------
class TestFromXmlSimulations(unittest.TestCase):

    """FromXmlSimulations class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'simulations.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'courbestarage', 'jaugeages', 'courbescorrection',
                 'serieshydro', 'seriesmeteo', 'simulations')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertNotEqual(self.data['simulations'], [])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod,
                         datetime.datetime(2010, 2, 26, 9, 30))
        self.assertEqual(scenario.emetteur.contact.code, '41')
        self.assertEqual(scenario.emetteur.intervenant.code, 1537)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, 14)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_simulation_0(self):
        """Simulation 0 test."""
        simulation = self.data['simulations'][0]
        # check simulation
        self.assertEqual(simulation.entite.code, 'Y1612020')
        self.assertEqual(simulation.modeleprevision.code, '13_08')
        self.assertEqual(simulation.grandeur, 'Q')
        self.assertEqual(simulation.statut, 4)
        self.assertEqual(simulation.qualite, 36)
        self.assertEqual(simulation.public, False)
        self.assertEqual(simulation.commentaire,
                         'Biais=-14.91 Précision=36.00')
        self.assertEqual(simulation.dtprod,
                         datetime.datetime(2010, 2, 26, 14, 45))
        # check previsions => res
        # FIXME  #1 - restore the full list when the duplicate pandas index is
        #   fixed. Restore also lines 52-55 in test/data/xml/1.1/simulation.xml
        #self.assertEqual(set(simulation.previsions.tolist()),
        #                 set([30, 10, 50, 25, 75, 90, 23, 25]))
        self.assertEqual(set(simulation.previsions_prb.tolist()),
                         set([25, 75, 90, 95]))
        self.assertEqual(set(simulation.previsions_tend.tolist()),
                         set([30, 10, 50, 23, 25]))
        # self.assertEqual(set(simulation.previsions.tolist()),
        #                  set([30, 10, 50, 25, 75, 90, 95, 23, 25]))
        self.assertEqual(simulation.previsions_prb.iloc[0], 25)
        self.assertEqual(
            simulation.previsions_tend['2010-02-26 15:00'].tolist(), [23, 25])
        self.assertEqual(
            # FIXME #1
            # simulation.previsions.swaplevel(0, 1)[50].tolist(), [30, 95, 23])
            simulation.previsions_prb.swaplevel(0, 1)[50].tolist(), [95])
        self.assertEqual(
            simulation.previsions_prb.swaplevel(0, 1)[40].tolist(), [75])
        # check previsions => index
        # FIXME #1
        # self.assertEqual(len(simulation.previsions.index), 9)
        self.assertEqual(len(simulation.previsions_prb.index), 4)
        self.assertEqual(len(simulation.previsions_tend.index), 5)
        self.assertEqual(
            set([x[0] for x in simulation.previsions_prb.swaplevel(0, 1).index]),
            set([20, 40, 49, 50]))
        self.assertEqual(
            set([x[0] for x in simulation.previsions_tend.swaplevel(0, 1).index]),
            set(['moy', 'min', 'max', 'moy', 'max']))
        # check previsions_tend et previsions_prb
        self.assertEqual(
            simulation.previsions_prb.swaplevel(0, 1)[40].tolist(), [75])
        self.assertEqual(
            simulation.previsions_tend.swaplevel(0, 1)['moy'].tolist(),
            [30, 23])
        self.assertEqual(
            simulation.previsions_tend.swaplevel(0, 1)['min'].tolist(), [10])
        self.assertEqual(
            simulation.previsions_tend.swaplevel(0, 1)['max'].tolist(),
            [50, 25])

    def test_simulation_1(self):
        """Simulation 1 test."""
        simulation = self.data['simulations'][1]
        # check simulation
        self.assertEqual(simulation.entite.code, 'Y161202001')
        self.assertEqual(simulation.modeleprevision.code, 'ScMerSHOM')
        self.assertEqual(simulation.grandeur, 'H')
        self.assertEqual(simulation.statut, 4)
        self.assertEqual(simulation.qualite, 21)
        self.assertEqual(simulation.public, True)
        self.assertEqual(simulation.dtprod,
                         datetime.datetime(2010, 2, 26, 14, 45))
        # check previsions => res
        self.assertEqual(len(simulation.previsions_tend), 8)
        self.assertEqual(simulation.previsions_tend.tolist()[0], 371.774)
        self.assertEqual(simulation.previsions_tend.tolist()[3], 422.280)
        self.assertEqual(simulation.previsions_tend.tolist()[7], 358.71)
        # check previsions => index
        self.assertEqual(len(simulation.previsions_tend.index), 8)
        self.assertEqual(len(simulation.previsions_tend.swaplevel(0, 1)['moy']), 8)

    def test_simulation_2(self):
        """Simulation 2 test."""
        simulation = self.data['simulations'][2]
        # check simulation
        self.assertEqual(simulation.entite.code, 'Y1612020')
        self.assertEqual(simulation.modeleprevision.code, '13_09')
        self.assertEqual(simulation.grandeur, 'Q')
        self.assertEqual(simulation.statut, 16)
        self.assertEqual(simulation.qualite, None)
        self.assertEqual(simulation.public, False)
        self.assertEqual(simulation.dtprod,
                         datetime.datetime(2010, 2, 26, 9, 45))
        # check previsions => res
        self.assertEqual(len(simulation.previsions_tend), 4)
        self.assertEqual(simulation.previsions_tend.tolist(), [22, 33, 44, 55])
        # check previsions => index
        self.assertEqual(len(simulation.previsions_tend.index), 4)
        self.assertEqual(len(simulation.previsions_tend.swaplevel(0, 1)['min']), 2)
        self.assertEqual(len(simulation.previsions_tend.swaplevel(0, 1)['max']), 2)

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
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import os
import unittest
import datetime
import math

from libhydro.conv.xml import _from_xml as from_xml
from libhydro.core import (sitehydro, sitemeteo)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin""" \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2c"""
__date__ = """2014-12-17"""

# HISTORY
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
            os.path.join('data', 'xml', '1.1', 'intervenants.xml')
        )

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'serieshydro', 'seriesmeteo', 'simulations'))
        )
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
            scenario.dtprod, datetime.datetime(2001, 12, 17, 4, 30, 47)
        )
        self.assertEqual(scenario.emetteur.intervenant.code, 1537)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.emetteur.contact.code, 525)
        self.assertEqual(
            scenario.destinataire.intervenant.code, 12345671234567
        )
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SIRET')
        self.assertEqual(scenario.destinataire.contact.code, 2)

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
        self.assertEqual(c.code, 1)
        self.assertEqual(c.nom, 'Nom')
        self.assertEqual(c.prenom, 'Prenom')
        self.assertEqual(c.civilite, 1)
        self.assertEqual(c.intervenant, i)
        c = i.contacts[1]
        self.assertEqual(c.code, 2)
        self.assertEqual(c.nom, 'Nom2')
        self.assertEqual(c.prenom, 'Prenom2')
        self.assertEqual(c.civilite, 2)
        self.assertEqual(c.intervenant, i)

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
        self.assertEqual(c.code, 5)
        self.assertEqual(c.nom, 'Nom Contaçt')
        self.assertEqual(c.prenom, 'Prenom Contaçt')
        self.assertEqual(c.civilite, 3)
        self.assertEqual(c.intervenant, i)


# -- class TestFromXmlSitesHydro ----------------------------------------------
class TestFromXmlSitesHydros(unittest.TestCase):

    """FromXmlSitesHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'siteshydro.xml')
        )

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'serieshydro', 'seriesmeteo', 'simulations'))
        )
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
            scenario.dtprod, datetime.datetime(2010, 2, 26, 12, 53, 10)
        )
        self.assertEqual(scenario.emetteur.contact.code, 1069)
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
            sh.libelle, 'Le Touch à Toulouse [Saint-Martin-du-Touch]'
        )
        self.assertEqual(
            sh.libelleusuel, 'St-Martin-du-Touch'
        )
        self.assertEqual(sh.typesite, 'SOURCE')
        self.assertEqual(sh.code, 'O1984310')
        self.assertEqual(sh.communes, ['11354', '11355', '2B021'])
        self.assertEqual(len(sh.stations), 3)
        # check stations
        for i in range(1, 3):
            self.assertEqual(sh.stations[i - 1].code, 'O19843100%i' % i)
            self.assertEqual(
                sh.stations[i - 1].libelle, '%s - station %i' % (
                    sh.libelle, i
                )
            )
            self.assertEqual(sh.stations[i - 1].typestation, 'LIMNI')
            self.assertEqual(
                sh.stations[i - 1].libellecomplement, 'station %i' % i
            )
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
            site.tronconsvigilance[1].libelle, 'Troncon Adour àvâl'
        )
        # check station
        station = site.stations[0]
        self.assertEqual(station.ddcs, ['10', '1000000001'])
        self.assertEqual(station.commune, '11354')
        self.assertEqual(station.codeh2, 'O1712510')
        self.assertEqual(station.niveauaffichage, 1)
        # checkcapteurs
        capteurs = station.capteurs
        self.assertEqual(len(capteurs), 2)
        self.assertEqual(capteurs[0].code, 'O17125100102')
        self.assertEqual(capteurs[0].typemesure, 'H')
        self.assertEqual(capteurs[1].code, 'O17125100101')
        self.assertEqual(capteurs[1].typemesure, 'H')
        self.assertEqual(capteurs[1].codeh2, 'O1712510')

    def test_error_1(self):
        """Xml file with namespace error test."""
        with self.assertRaises(ValueError):
            from_xml._parse(
                # *([os.path.join('data', 'xml', '1.1', 'siteshydro.xml')])
                *([os.path.join(
                    'data', 'xml', '1.1', 'siteshydro_with_namespace.xml'
                )])
            )


# -- class TestFromXmlSeuilsHydro ---------------------------------------------
class TestFromXmlSeuilsHydros(unittest.TestCase):

    """FromXmlSeuilsHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'seuilshydro.xml')
        )

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'serieshydro', 'seriesmeteo', 'simulations'))
        )
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
            if (
                (seuil.sitehydro.code == 'U2655010')
                and (seuil.code == '2214')
            ):
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
        self.assertEqual(
            seuil.valeurs[0].dtactivation,
            datetime.datetime(2010, 5, 17, 13, 40, 2)
        )
        self.assertEqual(
            seuil.valeurs[0].dtdesactivation,
            datetime.datetime(2012, 2, 19, 9, 28)
        )
        self.assertEqual(seuil.valeurs[0]._strict, True)

    def test_seuils_sitehydro_1(self):
        """Test seuils sitehydro 1."""
        # check the sitehydro
        sh = self.data['siteshydro'][1]
        self.assertEqual(sh.code, 'O2000040')

        # find the seuil
        for seuil in self.data['seuilshydro']:
            if (
                (seuil.sitehydro.code == 'O2000040')
                and (seuil.code == '82')
            ):
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
        self.assertEqual(
            seuil.dtmaj, datetime.datetime(2014, 3, 23, 9, 51, 56)
        )

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
        self.assertEqual(
            seuil.valeurs[1].dtactivation,
            datetime.datetime(2010, 6, 10, 10, 52, 57)
        )
        self.assertEqual(
            seuil.valeurs[2].dtactivation,
            datetime.datetime(2010, 6, 10, 11, 32, 57)
        )
        self.assertEqual(
            seuil.valeurs[3].dtactivation,
            datetime.datetime(2010, 6, 10, 11, 52, 57)
        )
        self.assertEqual(
            seuil.valeurs[0].dtdesactivation, None
        )
        self.assertEqual(
            seuil.valeurs[1].dtdesactivation, None
        )
        self.assertEqual(
            seuil.valeurs[2].dtdesactivation,
            datetime.datetime(2013, 10, 5, 5, 59, 29)
        )
        self.assertEqual(
            seuil.valeurs[3].dtdesactivation, None
        )

    def test_seuils_sitehydro_2(self):
        """Test seuils sitehydro 2."""
        # find 4 seuils
        seuils = []
        for seuil in self.data['seuilshydro']:
            if (
                (seuil.sitehydro.code == 'O0144020')
                and (seuil.code in [unicode(i) for i in range(1, 5)])
            ):
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
            if (
                (seuil.sitehydro.code == 'O6793330')
                and (seuil.code in ('338', '341'))
            ):
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
            from_xml._parse(
                os.path.join(
                    'data', 'xml', '1.1', 'seuilshydro_inconsistent.xml'
                )
            )


# -- class TestFromXmlSitesMeteo ----------------------------------------------
class TestFromXmlSitesMeteo(unittest.TestCase):

    """FromXmlSitesMeteo class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'sitesmeteo.xml')
        )

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'serieshydro', 'seriesmeteo', 'simulations'))
        )
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
        self.assertEqual(
            scenario.dtprod, datetime.datetime(2010, 2, 26, 8, 5, 56)
        )
        self.assertEqual(scenario.emetteur.contact.code, 26)
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
        self.assertEqual(sm.grandeurs[1].typemesure, 'VV')


# -- class TestFromXmlModelesPrevision ----------------------------------------
class TestFromXmlModelesPrevision(unittest.TestCase):

    """FromXmlModelesPrevision class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'modelesprevision.xml')
        )

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'serieshydro', 'seriesmeteo', 'simulations'))
        )
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
        self.assertEqual(
            scenario.dtprod, datetime.datetime(2001, 12, 17, 4, 30, 47)
        )
        self.assertEqual(scenario.emetteur.intervenant.code, 825)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.emetteur.contact.code, 222)
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.contact.code, 2)

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
            os.path.join('data', 'xml', '1.1', 'evenements.xml')
        )

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'serieshydro', 'seriesmeteo', 'simulations'))
        )
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
        self.assertEqual(
            scenario.dtprod, datetime.datetime(2010, 2, 26, 7, 5)
        )
        self.assertEqual(scenario.emetteur.contact.code, 26)
        self.assertEqual(scenario.emetteur.intervenant.code, 1520)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, 1537)
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_evenement_0(self):
        """Evenement 0 test."""
        evenement = self.data['evenements'][0]
        self.assertTrue(isinstance(evenement.entite, sitehydro.Sitehydro))
        self.assertEqual(evenement.entite.code, 'A0010101')
        self.assertEqual(evenement.contact.code, 1)
        self.assertEqual(evenement.dt, datetime.datetime(1999, 8, 12, 0, 5))
        self.assertEqual(evenement.descriptif, "Arrachement de l'échelle")
        self.assertEqual(evenement.publication, 1)
        self.assertEqual(
            evenement.dtmaj, datetime.datetime(2000, 5, 10, 22, 5)
        )

    def test_evenement_1(self):
        """Evenement 1 test."""
        evenement = self.data['evenements'][1]
        self.assertTrue(isinstance(evenement.entite, sitehydro.Station))
        self.assertEqual(evenement.entite.code, 'Z853010101')
        self.assertEqual(evenement.contact.code, 8563)
        self.assertEqual(evenement.dt, datetime.datetime(2010, 2, 26, 9, 5))
        self.assertEqual(
            evenement.descriptif, 'Déplacement de la station de 22.5m'
        )
        self.assertEqual(evenement.publication, 20)
        self.assertEqual(
            evenement.dtmaj, datetime.datetime(2011, 1, 13, 10, 5)
        )

    def test_evenement_2(self):
        """Evenement 2 test."""
        evenement = self.data['evenements'][2]
        self.assertTrue(isinstance(evenement.entite, sitemeteo.Sitemeteo))
        self.assertEqual(evenement.entite.code, '008530001')
        self.assertEqual(evenement.contact.code, 1)
        self.assertEqual(evenement.dt, datetime.datetime(1968, 2, 2, 23, 0))
        self.assertEqual(
            evenement.descriptif, 'Débouchage de la sonde de température'
        )
        self.assertEqual(evenement.publication, 100)
        self.assertEqual(
            evenement.dtmaj, datetime.datetime(2000, 1, 1, 22, 0)
        )


# -- class TestFromXmlSeriesHydro ---------------------------------------------
class TestFromXmlSeriesHydro(unittest.TestCase):

    """FromXmlSeriesHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'serieshydro.xml')
        )

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'serieshydro', 'seriesmeteo', 'simulations'))
        )
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
        self.assertEqual(scenario.emetteur.contact.code, 26)
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
        self.assertEqual(
            serie.observations.iloc[0].tolist(), [20992, 0, 16, True]
        )
        self.assertEqual(
            serie.observations.loc['2010-02-26 11:15'].tolist(),
            [21176, 0, 16, True]
        )

    def test_serie_1(self):
        """Serie 1 test."""
        serie = self.data['serieshydro'][1]
        self.assertEqual(serie.entite.code, 'V714401001')
        self.assertEqual(serie.grandeur, 'Q')
        self.assertEqual(serie.statut, 4)
        self.assertEqual(
            serie.observations.iloc[0].tolist(), [20, 12, 12, False]
        )
        self.assertEqual(
            serie.observations.loc['2010-02-26 13:15'].tolist(),
            [21, 12, 8, False]
        )

    def test_serie_2(self):
        """Serie 2 test."""
        serie = self.data['serieshydro'][2]
        self.assertEqual(serie.entite.code, 'V71440100103')
        self.assertEqual(serie.grandeur, 'H')
        self.assertEqual(serie.statut, 4)
        self.assertEqual(
            serie.observations.loc['2010-02-26 13:10'].tolist(),
            [680, 4, 20, True]
        )
        self.assertEqual(
            serie.observations.loc['2010-02-26 13:15'].tolist(),
            [684, 0, 20, True]
        )
        self.assertEqual(
            serie.observations.loc['2010-02-26 14:55'].tolist(),
            [670, 12, 20, True]
        )

    def test_seriehydro_without_observation(self):
        """Test a unconventionnal seriehydro from bdhydro."""
        data = from_xml._parse(
            os.path.join(
                'data', 'xml', '1.1', 'serieshydro_without_observations.xml'
            )
        )
        self.assertEqual(len(data['serieshydro']), 34)


# -- class TestFromXmlSeriesMeteo ---------------------------------------------
class TestFromXmlSeriesMeteo(unittest.TestCase):

    """FromXmlSeriesMeteo class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'seriesmeteo.xml')
        )

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'serieshydro', 'seriesmeteo', 'simulations'))
        )
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
        self.assertEqual(
            scenario.dtprod, datetime.datetime(2010, 2, 26, 23, 55, 30)
        )
        self.assertEqual(scenario.emetteur.contact.code, 1)
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
        self.assertEqual(
            serie.dtprod, datetime.datetime(2010, 2, 26, 15, 13, 37)
        )
        self.assertEqual(
            # (dte) res mth qal qua
            serie.observations.iloc[0].tolist(), [2, 0, 16, 100]
        )
        self.assertEqual(
            serie.observations.loc['2010-02-26 13:00'].tolist(),
            [8, 0, 16, 75]
        )

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
        self.assertEqual(
            serie.dtprod, datetime.datetime(2010, 2, 26, 15, 13, 37)
        )
        self.assertEqual(
            # (dte) res mth qal qua
            serie.observations.iloc[0].tolist()[:3], [4, 0, 16]
        )
        self.assertTrue(
            math.isnan(serie.observations.iloc[0]['qua'].item())
        )

        # self.assertEqual(
        #     serie.observations.loc['2010-02-26 13:00'].tolist(),
        #     [8, 0, 16, 75]
        # )

    def test_POM(self):
        """Serie POM test."""
        pom = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'seriesmeteo_POM.xml')
        )['seriesmeteo']
        # 280 observations
        self.assertEqual(sum([len(s.observations) for s in pom]), 280)
        # 4 sitesmeteo and therefore 4 series
        self.assertEqual(len(pom), 4)

    def test_without_obs(self):
        """Serie without obs test."""
        serie = from_xml._parse(
            os.path.join(
                'data', 'xml', '1.1', 'seriesmeteo_without_observations.xml'
            )
        )['seriesmeteo'][0]
        self.assertEqual(
            serie.observations['res'].values.tolist(),
            [5.8, 23.0, 45.8]
        )
        serie.resample(datetime.timedelta(hours=1))
        l = serie.observations['res'].values.tolist()
        self.assertTrue(math.isnan(l[2]))
        l.pop(2)
        self.assertEqual(
            l,
            [5.8, 23.0, 45.8]
        )


# -- class TestFromXmlSimulations ---------------------------------------------
class TestFromXmlSimulations(unittest.TestCase):

    """FromXmlSimulations class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'simulations.xml')
        )

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'modelesprevision', 'evenements',
                 'serieshydro', 'seriesmeteo', 'simulations'))
        )
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
        self.assertEqual(
            scenario.dtprod, datetime.datetime(2010, 2, 26, 9, 30)
        )
        self.assertEqual(scenario.emetteur.contact.code, 41)
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
        self.assertEqual(
            simulation.commentaire, 'Biais=-14.91 Précision=36.00'
        )
        self.assertEqual(
            simulation.dtprod, datetime.datetime(2010, 2, 26, 14, 45)
        )
        # check previsions => res
        self.assertEqual(
            set(simulation.previsions.tolist()),
            set([30, 10, 50, 25, 75, 90, 23, 25])
        )
        self.assertEqual(simulation.previsions.iloc[3], 25)
        self.assertEqual(
            simulation.previsions.loc['2010-02-26 15:00'].tolist(), [23, 25]
        )
        self.assertEqual(
            simulation.previsions.swaplevel(0, 1)[50].tolist(),
            [30, 23]
        )
        self.assertEqual(
            simulation.previsions.swaplevel(0, 1)[40].tolist(),
            [75]
        )
        # check previsions => index
        self.assertEqual(len(simulation.previsions.index), 8)
        self.assertEqual(
            set([x[0] for x in simulation.previsions.swaplevel(0, 1).index]),
            set([50, 0, 100, 20, 40, 49, 50, 100])
        )

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
        self.assertEqual(
            simulation.dtprod, datetime.datetime(2010, 2, 26, 14, 45)
        )
        # check previsions => res
        self.assertEqual(len(simulation.previsions), 8)
        self.assertEqual(simulation.previsions.tolist()[0], 371.774)
        self.assertEqual(simulation.previsions.tolist()[3], 422.280)
        self.assertEqual(simulation.previsions.tolist()[7], 358.71)
        # check previsions => index
        self.assertEqual(len(simulation.previsions.index), 8)
        self.assertEqual(len(simulation.previsions.swaplevel(0, 1)[50]), 8)

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
        self.assertEqual(
            simulation.dtprod, datetime.datetime(2010, 2, 26, 9, 45)
        )
        # check previsions => res
        self.assertEqual(len(simulation.previsions), 4)
        self.assertEqual(simulation.previsions.tolist(), [22, 33, 44, 55])
        # check previsions => index
        self.assertEqual(len(simulation.previsions.index), 4)
        self.assertEqual(len(simulation.previsions.swaplevel(0, 1)[0]), 2)
        self.assertEqual(len(simulation.previsions.swaplevel(0, 1)[100]), 2)

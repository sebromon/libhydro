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
from libhydro.core import (sitehydro, sitemeteo, _composant, _composant_site)


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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '1537')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.emetteur.contact.code, '525')
        self.assertEqual(
            scenario.destinataire.intervenant.code, '12345671234567')
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SIRET')
        self.assertEqual(scenario.destinataire.contact.code, '2')

    def test_intervenant_0(self):
        """intervenant 0 test."""
        # intervenant
        i = self.data['intervenants'][0]
        i_adr = i.adresse
        self.assertEqual(i.code, '11')
        self.assertEqual(i.origine, 'SANDRE')
        self.assertEqual(i.nom, 'Nom')
        self.assertEqual(i.statut, 'Gelé')
        self.assertEqual(i.dtcreation, datetime.datetime(1967, 8, 13, 0, 0, 0))
        self.assertEqual(i.dtmaj, datetime.datetime(2001, 12, 17, 4, 30, 47))
        self.assertEqual(i.auteur, 'Auteur')
        self.assertEqual(i.mnemo, 'Mnemo')
        self.assertEqual(i_adr.boitepostale, 'Boite postale')
        self.assertEqual(i_adr.adresse1_cplt, 'complément')
        self.assertEqual(i_adr.adresse1, '1 rue toto')
        self.assertEqual(i_adr.lieudit, 'Lieu-dit')
        self.assertEqual(i_adr.ville, 'Ville')
        self.assertEqual(i_adr.dep, '31')
        self.assertEqual(i.commentaire, 'Commentaire')
        self.assertEqual(i.activite, 'Activités')
        self.assertEqual(i_adr.codepostal, 'Code postal')
        self.assertEqual(i.nominternational, 'International')
        self.assertEqual(i.siret, 12345678901234)
        self.assertEqual(i.commune.code, '32001')
        self.assertEqual(i_adr.pays, 'FR')
        self.assertEqual(i_adr.adresse2, 'Adresse étrangère')
        self.assertEqual(i.telephone, '0600')
        self.assertEqual(i.fax, '0000')
        self.assertEqual(i.siteweb, 'http://toto.fr')
        self.assertEqual(i.pere.code, '33')
        self.assertEqual(i.pere.origine, 'SANDRE')
        # contacts
        self.assertEqual(len(i.contacts), 3)
        c = i.contacts[0]
        self.assertEqual(c.code, '1')
        self.assertEqual(c.nom, 'Nom')
        self.assertEqual(c.prenom, 'Prenom')
        self.assertEqual(c.civilite, 1)
        self.assertEqual(c.intervenant, i)
        self.assertEqual(c.profilasstr, '001')
        self.assertIsNotNone(c.adresse)
        adr = c.adresse
        self.assertEqual(adr.adresse1, 'Adresse')
        self.assertEqual(adr.adresse2, 'Adresse étrangère')
        self.assertEqual(adr.codepostal, '31000')
        self.assertEqual(adr.ville, 'Toulouse')
        self.assertEqual(adr.pays, 'FR')
        self.assertEqual(c.fonction, 'Hydromètre')
        self.assertEqual(c.telephone, '0000')
        self.assertEqual(c.portable, '0600')
        self.assertEqual(c.fax, 'Fax')
        self.assertEqual(c.mel, 'Mail')
        self.assertEqual(c.dtmaj, datetime.datetime(2015, 2, 3, 12, 10, 38))
        self.assertEqual(len(c.profilsadmin), 2)
        profil0 = c.profilsadmin[0]
        self.assertEqual(profil0.profil, 'GEST')
        self.assertEqual(len(profil0.zoneshydro), 2)
        self.assertEqual(
            (profil0.zoneshydro[0].code, profil0.zoneshydro[1].code),
            ('A123', 'Z987'))
        self.assertEqual(profil0.dtactivation,
                         datetime.datetime(2004, 4, 15, 17, 18, 19))
        self.assertEqual(profil0.dtdesactivation,
                         datetime.datetime(2005, 8, 10, 13, 36, 43))
        profil1 = c.profilsadmin[1]
        self.assertEqual(profil1.profil, 'JAU')
        self.assertEqual(len(profil1.zoneshydro), 2)
        self.assertEqual(
            (profil1.zoneshydro[0].code, profil1.zoneshydro[1].code),
            ('L000', 'K444'))
        self.assertIsNone(profil1.dtactivation)
        self.assertIsNone(profil1.dtdesactivation)
        self.assertEqual(c.alias, 'ALIAS')
        self.assertEqual(c.motdepasse, 'mot de passe')
        self.assertEqual(c.dtactivation,
                         datetime.datetime(2001, 12, 17, 9, 30, 47))
        self.assertEqual(c.dtdesactivation,
                         datetime.datetime(2013, 10, 25, 11, 45, 36))
        c = i.contacts[1]
        self.assertEqual(c.code, '2')
        self.assertEqual(c.nom, 'Nom2')
        self.assertEqual(c.prenom, 'Prenom2')
        self.assertEqual(c.civilite, 2)
        self.assertEqual(c.intervenant, i)
        self.assertEqual(c.profilasstr, '010')
        c = i.contacts[2]
        self.assertEqual(c.code, '999')
        self.assertIsNone(c.nom)
        self.assertIsNone(c.prenom)
        self.assertIsNone(c.civilite)
        self.assertEqual(c.intervenant, i)
        self.assertEqual(c.profilasstr, '000')

    def test_intervenant_1(self):
        """intervenant 1 test."""
        # intervenant
        i = self.data['intervenants'][1]
        self.assertEqual(i.code, '12345671234567')
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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '25')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, '1537')
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
        self.assertEqual(sh.communes, [_composant_site.Commune(code='11354'),
                                       _composant_site.Commune(code='11355'),
                                       _composant_site.Commune(code='2B021')])
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
        self.assertEqual(len(sh.stations[0].plages), 2)
        plage = sh.stations[0].plages[0]
        self.assertEqual(plage.dtdeb,
                         datetime.datetime(2015, 2, 14, 11, 54, 6))
        self.assertEqual(plage.dtfin,
                         datetime.datetime(2016, 9, 21, 6, 19, 31))
        self.assertEqual(plage.dtactivation,
                         datetime.datetime(2017, 3, 17, 17, 38, 21))
        self.assertEqual(plage.dtdesactivation,
                         datetime.datetime(2017, 4, 29, 19, 51, 48))
        self.assertEqual(plage.active, False)

        plage = sh.stations[0].plages[1]
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
        self.assertEqual(len(site.entitesvigicrues), 2)
        self.assertEqual(site.entitesvigicrues[0].code, 'AG3')
        self.assertEqual(site.entitesvigicrues[1].code, 'AG5')
        self.assertEqual(
            site.entitesvigicrues[1].libelle, 'Troncon Adour àvâl')
        self.assertEqual(site.entitehydro, 'Y1524018')

        self.assertEqual(len(site.images), 2)
        image0 = site.images[0]
        self.assertEqual((image0.adresse, image0.typeill,
                          image0.formatimg, image0.commentaire),
                         ('http://image1.jpeg', 1,
                          'image/jpeg', 'Commentaire'))
        image1 = site.images[1]
        self.assertEqual((image1.adresse, image1.typeill,
                          image1.formatimg, image1.commentaire),
                         ('http://image2.bmp', 2,
                          'image/bmp', None))


        self.assertEqual(len(site.roles), 2)
        role1 = site.roles[0]
        self.assertEqual(role1.contact.code, '2')
        self.assertEqual(role1.role, 'ADM')
        self.assertIsNone(role1.dtdeb)
        self.assertIsNone(role1.dtfin)
        self.assertIsNone(role1.dtmaj)

        role2 = site.roles[1]
        self.assertEqual(role2.contact.code, '1234')
        self.assertEqual(role2.role, 'REF')
        self.assertEqual(role2.dtdeb,
                         datetime.datetime(2010, 5, 17, 11, 26, 39))
        self.assertEqual(role2.dtfin,
                         datetime.datetime(2038, 1, 19, 20, 55, 30))
        self.assertEqual(role2.dtmaj,
                         datetime.datetime(2017, 11, 4, 9, 23, 31))

        self.assertEqual(site.tronconhydro, 'O0011532')
        self.assertEqual(site.zonehydro, 'H420')
        self.assertEqual(site.precisioncoursdeau, 'bras principal')
        # check station
        station = site.stations[0]
        self.assertEqual(station.code, 'O171251001')
        self.assertEqual(station.libelle,
                         'L\'Ariège à Auterive - station de secours')
        self.assertEqual(station.typestation, 'DEB')
        self.assertEqual(station.libellecomplement, 'Complément du libellé')
        self.assertEqual(station.commentaireprive, 'Station située à Auterive')
        self.assertEqual(station.dtmaj,
                         datetime.datetime(2017, 7, 17, 11, 23, 34))
        self.assertEqual(station.coord.x, 15.0)
        self.assertEqual(station.coord.y, 16.0)
        self.assertEqual(station.coord.proj, 26)
        self.assertEqual(station.pointk, 153.71)
        self.assertEqual(station.dtmiseservice,
                         datetime.datetime(1991, 10, 7, 14, 15, 16))
        self.assertEqual(station.dtfermeture,
                         datetime.datetime(2012, 4, 21, 19, 58, 3))
        self.assertEqual(station.surveillance, True)
        self.assertEqual(station.niveauaffichage, 991)
        self.assertEqual(station.droitpublication, 20)
        self.assertEqual(station.essai, False)
        self.assertEqual(station.influence, 2)
        self.assertEqual(station.influencecommentaire, 'Libellé influence')
        self.assertEqual(station.commentaire,
                         'commentaire1 création station hydro')
        self.assertEqual(len(station.stationsanterieures), 1)
        self.assertEqual(station.stationsanterieures[0].code, 'G876542134')
        self.assertEqual(len(station.stationsposterieures), 0)

        self.assertEqual(len(station.plagesstationsfille), 1)
        self.assertEqual(station.plagesstationsfille[0].code,
                         'L854795216')
        self.assertEqual(len(station.plagesstationsmere), 0)

        self.assertEqual(len(station.qualifsdonnees), 2)
        qualif0 = station.qualifsdonnees[0]
        self.assertEqual(qualif0.coderegime, 1)
        self.assertEqual(qualif0.qualification, 12)
        self.assertEqual(qualif0.commentaire, 'Commentaire qualif')
        qualif1 = station.qualifsdonnees[1]
        self.assertEqual(qualif1.coderegime, 2)
        self.assertEqual(qualif1.qualification, 16)
        self.assertIsNone(qualif1.commentaire)
        self.assertEqual(station.finalites, [1, 2])
        self.assertEqual(len(station.loisstat), 3)
        loi0 = station.loisstat[0]
        self.assertEqual((loi0.contexte, loi0.loi),
                         (1, 1))
        loi1 = station.loisstat[1]
        self.assertEqual((loi1.contexte, loi1.loi),
                         (3, 2))
        loi2 = station.loisstat[2]
        self.assertEqual((loi2.contexte, loi2.loi),
                         (2, 3))

        self.assertEqual(len(station.images), 2)
        image0 = station.images[0]
        self.assertEqual((image0.adresse, image0.typeill, image0.formatimg,
                          image0.commentaire),
                         ('http://toto.fr/station.png', 2, 'png',
                          'Image de la station'))
        image1 = station.images[1]
        self.assertEqual((image1.adresse, image1.typeill, image1.formatimg,
                          image1.commentaire),
                         ('http://tata.fr/station2.bmp', None, None, None))

        self.assertEqual(len(station.roles), 2)
        role0 = station.roles[0]
        self.assertEqual((role0.contact.code, role0.role, role0.dtdeb,
                          role0.dtfin, role0.dtmaj),
                         ('2', 'ADM',
                          datetime.datetime(2005, 11, 18, 14, 56, 54),
                          datetime.datetime(2007, 5, 4, 14, 12, 28),
                          datetime.datetime(2012, 10, 4, 11, 35, 21)))
        role1 = station.roles[1]
        self.assertEqual((role1.contact.code, role1.role, role1.dtdeb,
                          role1.dtfin, role1.dtmaj),
                         ('999', 'REF', None, None, None))

        self.assertEqual(len(station.plages), 2)
        plage0 = station.plages[0]
        self.assertEqual((plage0.dtdeb, plage0.dtfin, plage0.dtactivation,
                          plage0.dtdesactivation, plage0.active),
                         (datetime.datetime(2006, 4, 25, 16, 0, 0),
                          datetime.datetime(2006, 4, 30, 17, 0, 0),
                          datetime.datetime(2007, 1, 18, 15, 10, 5),
                          datetime.datetime(2014, 10, 11, 9, 47, 44),
                          True
                          ))
        plage1 = station.plages[1]
        self.assertEqual((plage1.dtdeb, plage1.dtfin, plage1.dtactivation,
                          plage1.dtdesactivation, plage1.active),
                         (datetime.datetime(2006, 5, 25, 16, 0, 0),
                          datetime.datetime(2006, 5, 30, 17, 0, 0),
                          None, None, False))

        self.assertEqual([reseau.code for reseau in station.reseaux],
                         ['10', '1000000001'])

        # checkcapteurs
        capteurs = station.capteurs
        self.assertEqual(len(capteurs), 2)
        self.assertEqual(capteurs[0].code, 'O17125100102')
        self.assertEqual(capteurs[0].typemesure, 'H')
        self.assertEqual(capteurs[0].typecapteur, 0)  # default type
        self.assertEqual(capteurs[1].code, 'O17125100101')
        self.assertEqual(capteurs[1].libelle, 'Ultrasons principal')
        self.assertEqual(capteurs[1].mnemo, 'UP')
        self.assertEqual(capteurs[1].typemesure, 'H')
        self.assertEqual(capteurs[1].codeh2, 'O1712510')
        self.assertEqual(capteurs[1].typecapteur, 3)
        self.assertEqual(capteurs[1].surveillance, False)
        self.assertEqual(capteurs[1].dtmaj,
                         datetime.datetime(2016, 5, 18, 14, 5, 35))
        self.assertEqual(capteurs[1].pdt, 6)
        self.assertEqual(capteurs[1].essai, True)
        self.assertEqual(capteurs[1].commentaire, 'Capteur jaune')
        self.assertEqual(capteurs[1].observateur.code, '3')

        # check plages utilisatino capteurs
        self.assertEqual(len(capteurs[0].plages), 0)
        self.assertEqual(len(capteurs[1].plages), 2)

        plage = capteurs[1].plages[0]
        self.assertEqual(plage.dtdeb,
                         datetime.datetime(2009, 11, 3, 15, 19, 18))
        self.assertEqual(plage.dtfin,
                         datetime.datetime(2015, 3, 21, 11, 14, 47))
        self.assertEqual(plage.dtactivation,
                         datetime.datetime(2014, 12, 14, 18, 27, 32))
        self.assertEqual(plage.dtdesactivation,
                         datetime.datetime(2015, 10, 25, 19, 13, 4))
        self.assertEqual(plage.active, True)

        plage = capteurs[1].plages[1]
        self.assertEqual(plage.dtdeb,
                         datetime.datetime(2016, 1, 15, 12, 14, 13))
        self.assertIsNone(plage.dtfin)
        self.assertIsNone(plage.dtactivation)
        self.assertIsNone(plage.dtdesactivation)
        self.assertIsNone(plage.active)
        # Fin capteurs

        self.assertEqual(len(station.refsalti), 2)
        refalti0 = station.refsalti[0]
        self.assertEqual((refalti0.dtdeb, refalti0.dtfin,
                          refalti0.dtactivation, refalti0.dtdesactivation,
                          refalti0.altitude.altitude,
                          refalti0.altitude.sysalti, refalti0.dtmaj),
                         (datetime.datetime(2006, 1, 1, 8, 0, 0),
                          datetime.datetime(2006, 1, 31, 10, 0, 0),
                          datetime.datetime(2009, 12, 4, 11, 32, 4),
                          datetime.datetime(2013, 7, 28, 8, 10, 57),
                          999.0, 4,
                          datetime.datetime(2014, 4, 24, 16, 54, 21)
                          ))

        refalti1 = station.refsalti[1]
        self.assertEqual((refalti1.dtdeb, refalti1.dtfin,
                          refalti1.dtactivation, refalti1.dtdesactivation,
                          refalti1.altitude.altitude,
                          refalti1.altitude.sysalti, refalti1.dtmaj),
                         (datetime.datetime(2007, 2, 1, 8, 0, 0),
                          datetime.datetime(2007, 2, 28, 10, 0, 0),
                          None, None,
                          777.0, 7, None
                          ))
        self.assertEqual(station.codeh2, 'O1712510')
        self.assertEqual(station.commune, '11354')

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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(seuil.publication, 12)
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
        self.assertEqual(seuil.publication, 22)
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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '1520')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, '1537')
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_sitemeteo_0(self):
        """Sitemeteo 0 test."""
        sm = self.data['sitesmeteo'][0]
        self.assertEqual(sm.code, '001072001')
        self.assertEqual(sm.libelle, 'CEYZERIAT_PTC')
        self.assertEqual(sm.libelleusuel, 'CEYZERIAT')
        self.assertEqual(sm.mnemo, 'Mnémo')
        self.assertEqual(sm.lieudit, 'Aérodrome de bourg Ceyzeriat')
        self.assertEqual(sm.coord.x, 827652)
        self.assertEqual(sm.coord.y, 2112880)
        self.assertEqual(sm.coord.proj, 26)
        self.assertEqual(sm.altitude.altitude, 53.0)
        self.assertEqual(sm.altitude.sysalti, 7)
        self.assertEqual(sm.fuseau, 2)
        self.assertEqual(sm.dtmaj, datetime.datetime(2015, 3, 17, 11, 54, 47))
        self.assertEqual(sm.dtouverture,
                         datetime.datetime(1950, 1, 1, 0, 0, 0))
        self.assertEqual(sm.dtfermeture,
                         datetime.datetime(2007, 10, 24, 9, 8, 1))
        self.assertTrue(sm.droitpublication)
        self.assertFalse(sm.essai)
        self.assertEqual(sm.commentaire, 'Commentaire')

        self.assertEqual(len(sm.images), 2)
        image0 = sm.images[0]
        self.assertEqual((image0.adresse, image0.typeill, image0.formatimg,
                          image0.commentaire),
                         ('http://xxxxxxx', 3, 'image/jpeg ',
                          'Photo d\'ensemble depuis le nord'))
        image1 = sm.images[1]
        self.assertEqual((image1.adresse, image1.typeill, image1.formatimg,
                          image1.commentaire),
                         ('http://toto.fr/img.png', None, None, None))

        self.assertEqual(len(sm.reseaux), 2)
        self.assertEqual(sm.reseaux[0].code, '10')
        self.assertEqual(sm.reseaux[1].code, '100000003')
        self.assertEqual(len(sm.roles), 1)
        role = sm.roles[0]
        self.assertEqual(role.contact.code, '2')
        self.assertEqual(role.role, 'ADM')
        self.assertEqual(role.dtdeb, datetime.datetime(2008, 4, 19, 11, 10, 9))
        self.assertEqual(role.dtfin, datetime.datetime(2015, 10, 4, 7, 20, 30))
        self.assertEqual(role.dtmaj,
                         datetime.datetime(2016, 12, 9, 17, 58, 16))
        self.assertEqual(sm.commune, '35281')
        self.assertEqual(sm._strict, True)
        self.assertEqual(len(sm.grandeurs), 2)
        for grandeur in sm.grandeurs:
            self.assertEqual(grandeur.sitemeteo, sm)

        grd0 = sm.grandeurs[0]
        self.assertEqual(grd0.typemesure, 'RR')
        self.assertEqual(grd0.dtmiseservice,
                         datetime.datetime(1994, 4, 5, 16, 0, 0))
        self.assertEqual(grd0.dtfermeture,
                         datetime.datetime(2011, 4, 5, 16, 0, 0))
        self.assertEqual(grd0.essai, True)
        self.assertEqual(grd0.pdt, 4)
        self.assertEqual(len(grd0.classesqualite), 1)
        cl0 = grd0.classesqualite[0]
        self.assertEqual(cl0.classe, 3)
        self.assertEqual(cl0.visite.dtvisite,
                         datetime.datetime(1994, 4, 5, 8, 23, 0))
        self.assertEqual(cl0.dtdeb, datetime.datetime(1994, 4, 5, 8, 21, 0))
        self.assertEqual(cl0.dtfin, datetime.datetime(2010, 4, 5, 8, 28, 0))
        self.assertEqual(grd0.dtmaj, datetime.datetime(2012, 9, 4, 12, 54, 17))

        self.assertEqual(sm.grandeurs[1].typemesure, 'VV')
        self.assertIsNone(sm.grandeurs[1].pdt)

        self.assertEqual(len(sm.visites), 2)
        visite = sm.visites[0]
        self.assertEqual(visite.dtvisite,
                         datetime.datetime(2003, 10, 15, 11, 28, 34))
        self.assertIsNone(visite.contact)
        self.assertIsNone(visite.methode)
        self.assertIsNone(visite.modeop)

        
        visite = sm.visites[1]
        self.assertEqual(visite.dtvisite,
                         datetime.datetime(2004, 4, 5, 19, 36, 0))
        self.assertEqual(visite.contact.code, '4')
        self.assertEqual(visite.methode, 'Méthode à préciser')
        self.assertEqual(visite.modeop, 'Libellé libre')


# -- class TestFromXmlSeuilsMeteo ---------------------------------------------
class TestFromXmlSeuilsMeteos(unittest.TestCase):

    """FromXmlSeuilsHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'seuilsmeteo.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['simulations'], [])
        self.assertEqual(len(self.data['siteshydro']), 0)
        self.assertEqual(len(self.data['seuilshydro']), 0)
        self.assertEqual(len(self.data['sitesmeteo']), 3)
        self.assertEqual(len(self.data['seuilsmeteo']), 3)

    def test_seuils_sitemeteo_0(self):
        """Test seuils sitemeteo 0."""
        # check the sitehydro
        seuil = self.data['seuilsmeteo'][0]
        grandeur = seuil.grandeurmeteo
        self.assertEqual(grandeur.typemesure, 'VV')
        self.assertEqual(grandeur.dtmiseservice,
                         datetime.datetime(1998, 4, 5, 16, 0, 0))
        self.assertEqual(grandeur.sitemeteo.code, '001072001')
        self.assertEqual(grandeur.sitemeteo.libelle, 'CEYZERIAT_PTC')
        self.assertEqual(seuil.code, '28')
        self.assertEqual(seuil.typeseuil, 1)
        self.assertEqual(seuil.nature, 11)
        self.assertEqual(seuil.duree, 0)
        self.assertEqual(seuil.libelle, 'Vitesse maximale avant arrachement')
        self.assertEqual(seuil.mnemo, 'V max')
        self.assertEqual(seuil.gravite, 85)
        self.assertEqual(seuil.commentaire, 'Commentaire seuil')
        self.assertEqual(len(seuil.valeurs), 1)
        valeur = seuil.valeurs[0]
        self.assertEqual(valeur.valeur, 25.03)
        self.assertEqual(valeur.dtdesactivation,
                         datetime.datetime(2016, 3, 10, 9, 11, 12))
        self.assertEqual(valeur.dtactivation,
                         datetime.datetime(2015, 6, 27, 11, 37, 41))
        self.assertEqual(valeur.tolerance, 1.2,)
        self.assertEqual(seuil.dtmaj,
                         datetime.datetime(2017, 12, 3, 15, 24, 13))

    def test_seuils_sitemeteo_1(self):
        """Test seuils sitemeteo 0."""
        # check the sitehydro
        seuil = self.data['seuilsmeteo'][1]

        grandeur = seuil.grandeurmeteo
        self.assertEqual(grandeur.typemesure, 'VV')
        self.assertEqual(grandeur.dtmiseservice,
                         datetime.datetime(1998, 4, 5, 16, 0, 0))
        self.assertEqual(grandeur.sitemeteo.code, '001072001')
        self.assertEqual(grandeur.sitemeteo.libelle, 'CEYZERIAT_PTC')

        self.assertEqual(seuil.code, '29')
        self.assertEqual(seuil.typeseuil, 2)
        self.assertEqual(seuil.nature, 31)
        self.assertEqual(seuil.duree, 60)
        self.assertEqual(seuil.libelle, 'Vitesse gradient')
        self.assertEqual(seuil.mnemo, 'V grad')
        self.assertEqual(seuil.gravite, 50)
        self.assertEqual(seuil.commentaire, 'Commentaire')
        self.assertEqual(len(seuil.valeurs), 1)
        valeur = seuil.valeurs[0]
        self.assertEqual(valeur.valeur, 10)
        self.assertIsNone(valeur.dtdesactivation)
        self.assertEqual(valeur.dtactivation,
                         datetime.datetime(2018, 10, 15, 13, 25, 14))
        self.assertIsNone(valeur.tolerance)
        self.assertEqual(seuil.dtmaj,
                         datetime.datetime(2019, 3, 1, 18, 56, 37))

    def test_seuils_sitemeteo_2(self):
        """Test seuils sitemeteo 0."""
        # check the sitehydro
        seuil = self.data['seuilsmeteo'][2]

        grandeur = seuil.grandeurmeteo
        self.assertEqual(grandeur.typemesure, 'RR')
        self.assertIsNone(grandeur.dtmiseservice)
        self.assertEqual(grandeur.sitemeteo.code, '123456789')
        self.assertIsNone(grandeur.sitemeteo.libelle)

        self.assertEqual(seuil.code, '1234')
        self.assertIsNone(seuil.typeseuil)
        self.assertIsNone(seuil.nature)
        self.assertIsNone(seuil.duree)
        self.assertIsNone(seuil.libelle)
        self.assertIsNone(seuil.mnemo)
        self.assertIsNone(seuil.gravite)
        self.assertIsNone(seuil.commentaire)
        self.assertEqual(len(seuil.valeurs), 0)
        self.assertIsNone(seuil.dtmaj)




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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '825')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.emetteur.contact.code, '222')
        self.assertEqual(scenario.destinataire.intervenant.code, '1537')
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.contact.code, '2')

    def test_modeleprevision_0(self):
        """Modeleprevision 0 test."""
        modeleprevision = self.data['modelesprevision'][0]
        self.assertEqual(modeleprevision.contact.code, '1234')
        self.assertEqual(modeleprevision.code, '9876543210')
        self.assertEqual(modeleprevision.libelle, 'Libellé du modèle')
        self.assertEqual(modeleprevision.typemodele, 1)
        self.assertEqual(modeleprevision.description, 'Description du modèle')
        self.assertEqual(modeleprevision.dtmaj,
                         datetime.datetime(2001, 12, 17, 4, 30, 47))
        self.assertEqual(modeleprevision.siteshydro, [])

    def test_modeleprevision_1(self):
        """Modeleprevision 1 test."""
        modeleprevision = self.data['modelesprevision'][1]
        self.assertIsNone(modeleprevision.contact)
        self.assertEqual(modeleprevision.code, '0123456789')
        self.assertIsNone(modeleprevision.libelle)
        self.assertEqual(modeleprevision.typemodele, 0)
        self.assertIsNone(modeleprevision.description)
        self.assertIsNone(modeleprevision.dtmaj)
        self.assertEqual(modeleprevision.siteshydro, [])


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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '1520')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, '1537')
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_evenement_0(self):
        """Evenement 0 test."""
        evenement = self.data['evenements'][0]
        self.assertTrue(isinstance(evenement.entite, sitehydro.Sitehydro))
        self.assertEqual(evenement.entite.code, 'A0010101')
        self.assertEqual(evenement.contact.code, '1')
        self.assertEqual(evenement.dt, datetime.datetime(1999, 8, 12, 0, 5))
        self.assertEqual(evenement.descriptif, "Arrachement de l'échelle")
        self.assertEqual(evenement.publication, 12)
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
        self.assertEqual(evenement.publication, 12)
        self.assertEqual(evenement.typeevt, 7)
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
        self.assertEqual(evenement.publication, 22)
        self.assertEqual(evenement.dtmaj,
                         datetime.datetime(2000, 1, 1, 22, 0))

    def test_evenement_3(self):
        """Evenement 3 test."""
        evenement = self.data['evenements'][3]
        self.assertEqual(evenement.entite.code, 'Z853011234')
        self.assertEqual(evenement.contact.code, '1234')
        self.assertEqual(evenement.dt,
                         datetime.datetime(2018, 3, 27, 10, 6, 1))
        self.assertEqual(evenement.descriptif,
                         'Déplacement de la station de 34.5m')
        self.assertEqual(evenement.publication, 12)
        self.assertEqual(evenement.typeevt, 7)
        self.assertEqual(evenement.dtmaj,
                         datetime.datetime(2018, 6, 26, 11, 7, 34))

    def test_evenement_4(self):
        """Evenement 4 test."""
        evenement = self.data['evenements'][4]
        self.assertEqual(evenement.entite.code, 'Z853014321')
        self.assertEqual(evenement.contact.code, '4321')
        self.assertEqual(evenement.dt,
                         datetime.datetime(2017, 1, 25, 8, 4, 59))
        self.assertEqual(evenement.descriptif,
                         'Déplacement de la station de 59.5m')
        self.assertEqual(evenement.publication, 12)
        self.assertEqual(evenement.dtmaj,
                         datetime.datetime(2017, 7, 11, 9, 11, 17))

    def test_evenement_5(self):
        """Evènement archivé"""
        evt = self.data['evenements'][5]
        dtmaj = datetime.datetime(2016, 11, 2, 7, 15, 53)
        self.assertEqual(evt.dtmaj, dtmaj)
        self.assertEqual(evt.dtfin, dtmaj)

    def test_evenement_6(self):
        """Evènement archivé sans dtmaj"""
        evt = self.data['evenements'][6]
        self.assertIsNone(evt.dtmaj)
        self.assertIsNotNone(evt.dtfin)

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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(jaugeage.code, 184)

        self.assertIsNone(jaugeage.dte)
        self.assertIsNone(jaugeage.dtdeb)
        self.assertIsNone(jaugeage.debit)
        self.assertIsNone(jaugeage.dtfin)

        self.assertIsNone(jaugeage.section_mouillee)
        self.assertIsNone(jaugeage.perimetre_mouille)
        self.assertIsNone(jaugeage.largeur_miroir)
        self.assertEqual(jaugeage.mode, 0)
        self.assertIsNone(jaugeage.commentaire)
        self.assertIsNone(jaugeage.vitessemoy)
        self.assertIsNone(jaugeage.vitessemax)
        self.assertIsNone(jaugeage.vitessemax_surface)

        self.assertEqual(jaugeage.site.code, 'K0101010')
        self.assertEqual(len(jaugeage.hauteurs), 0)
        self.assertIsNone(jaugeage.dtmaj)

    def test_jaugeage_02(self):
        """check full jaugeage"""
        jaugeage = self.data['jaugeages'][1]
        self.assertEqual(jaugeage.code, 159)
        self.assertEqual(jaugeage.dte, datetime.datetime(2015, 8, 3, 4, 5, 17))
        self.assertEqual(jaugeage.dtdeb,
                         datetime.datetime(2015, 8, 2, 6, 13, 34))
        self.assertEqual(jaugeage.debit, 1034.56)
        self.assertEqual(jaugeage.dtfin,
                         datetime.datetime(2015, 8, 3, 11, 39, 8))
        self.assertEqual(jaugeage.section_mouillee, 341.25)
        self.assertEqual(jaugeage.perimetre_mouille, 987.54)
        self.assertEqual(jaugeage.largeur_miroir, 156423.12)
        self.assertEqual(jaugeage.mode, 3)
        self.assertEqual(jaugeage.commentaire, 'Commentaire')
        self.assertEqual(jaugeage.vitessemoy, 17.54)
        self.assertEqual(jaugeage.vitessemax, 19.43)
        self.assertEqual(jaugeage.vitessemax_surface, 18.87)
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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '1178')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, '1537')
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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '1178')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, '1537')
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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '1520')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, '1537')
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_serie_0(self):
        """Serie 0 test."""
        serie = self.data['serieshydro'][0]
        self.assertEqual(serie.entite.code, 'V7144010')
        self.assertEqual(serie.grandeur, 'Q')
        self.assertEqual(serie.observations.iloc[0].tolist(),
                         [20992, 0, 16, 0, 4])
        self.assertEqual(serie.observations.loc['2010-02-26 11:15'].tolist(),
                         [21176, 0, 16, 0, 4])

    def test_serie_1(self):
        """Serie 1 test."""
        serie = self.data['serieshydro'][1]
        self.assertEqual(serie.entite.code, 'V714401001')
        self.assertEqual(serie.grandeur, 'Q')
        self.assertEqual(serie.observations.iloc[0].tolist(),
                         [20, 8, 12, 1, 4])
        self.assertEqual(serie.observations.loc['2010-02-26 13:15'].tolist(),
                         [21, 8, 8, 1, 4])

    def test_serie_2(self):
        """Serie 2 test."""
        serie = self.data['serieshydro'][2]
        self.assertEqual(serie.entite.code, 'V71440100103')
        self.assertEqual(serie.grandeur, 'H')
        self.assertEqual(serie.observations.loc['2010-02-26 13:10'].tolist(),
                         [680, 4, 20, 0, 4])
        self.assertEqual(serie.observations.loc['2010-02-26 13:15'].tolist(),
                         [684, 0, 20, 0, 4])
        self.assertEqual(serie.observations.loc['2010-02-26 14:55'].tolist(),
                         [670, 8, 20, 0, 4])

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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '1537')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, '1537')
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_serie_RR(self):
        """Serie RR test."""
        for serie in self.data['seriesmeteo']:
            if serie.grandeur.typemesure == 'RR':
                break
        self.assertEqual(serie.grandeur.sitemeteo.code, '001033002')
        self.assertEqual(serie.duree, datetime.timedelta(minutes=60))
        self.assertEqual(serie.dtdeb, datetime.datetime(2010, 2, 26, 12))
        self.assertEqual(serie.dtfin, datetime.datetime(2010, 2, 26, 13))
        self.assertEqual(serie.dtprod,
                         datetime.datetime(2010, 2, 26, 15, 13, 37))
        # (dte) res mth qal qua
        self.assertEqual(serie.observations.iloc[0].tolist(),
                         [2, 0, 16, 100, 0, 4])
        self.assertEqual(serie.observations.loc['2010-02-26 13:00'].tolist(),
                         [8, 0, 16, 75, 0, 4])

    def test_serie_TA(self):
        """Serie TA test."""
        for serie in self.data['seriesmeteo']:
            if serie.grandeur.typemesure == 'TA':
                break
        self.assertEqual(serie.grandeur.sitemeteo.code, '02B033002')
        self.assertEqual(serie.duree, datetime.timedelta(minutes=0))
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
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
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
        self.assertEqual(scenario.emetteur.intervenant.code, '1537')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, '14')
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


# -- class TestFromXmlObssElab ---------------------------------------------
class TestFromXmlObssElab(unittest.TestCase):

    """FromXmlObssElab class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'obsselaboree.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertNotEqual(self.data['seriesobselab'], [])
        self.assertEqual(self.data['simulations'], [])

    def test_series(self):
        series = self.data['seriesobselab']

        self.assertEqual(series[0].entite.code, 'O005002001')
        self.assertEqual(series[0].typegrd, 'QmnJ')
        self.assertEqual(series[0].pdt.duree, datetime.timedelta(days=1))
        self.assertEqual(series[0].pdt.unite, _composant.PasDeTemps.JOURS)
        self.assertEqual(len(series[0].observations), 9)
        self.assertEqual(series[0].dtprod,
                         datetime.datetime(2013, 6, 23, 0, 21, 34))

        self.assertEqual(series[1].entite.code, 'H040002001')
        self.assertEqual(series[1].typegrd, 'QmnJ')
        self.assertEqual(len(series[1].observations), 3)
        self.assertEqual(series[1].dtprod,
                         datetime.datetime(2013, 6, 23, 1, 47, 8))

        self.assertEqual(series[2].entite.code, 'H620101001')
        self.assertEqual(series[2].typegrd, 'QmnJ')
        self.assertEqual(len(series[2].observations), 2)
        self.assertEqual(series[2].dtprod,
                         datetime.datetime(2013, 6, 29, 2, 45, 54))

        self.assertEqual(series[3].entite.code, 'H622101001')
        self.assertEqual(series[3].typegrd, 'QmnJ')
        self.assertEqual(len(series[3].observations), 11)

        self.assertEqual(series[4].entite.code, 'Q142001001')
        self.assertEqual(series[4].typegrd, 'QmnJ')
        self.assertEqual(len(series[4].observations), 1)
        self.assertEqual(series[4].dtprod,
                         datetime.datetime(2013, 6, 14, 7, 4, 29))


# -- class TestFromXmlObssElab ---------------------------------------------
class TestFromXmlObssElabMeteo(unittest.TestCase):

    """FromXmlObssElab class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'obsselaboreemeteo.xml'))

    def test_base(self):
        """Check keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['seriesobselab'], [])
        self.assertEqual(self.data['simulations'], [])
        self.assertNotEqual(self.data['seriesmeteo'], [])
        self.assertNotEqual(self.data['seriesobselabmeteo'], [])

    def test_series(self):
        series = self.data['seriesobselabmeteo']
        self.assertEqual(series[0].site.code, 'A0010330')
        self.assertEqual(series[0].grandeur, 'RR')
        self.assertEqual(series[0].typeserie, 1)
        self.assertEqual(len(series[0].observations), 2)

        self.assertEqual(series[1].site.code, 'A0010331')
        self.assertEqual(series[1].typeserie, 1)
        self.assertEqual(len(series[1].observations), 1)



# -- class TestFromXmlGradients ----------------------------------------
class TestFromXmlGradients(unittest.TestCase):

    """FromXmlGradients class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'gradients.xml'))

    def test_base(self):
        """Check Keys test."""
        self.assertEqual(
            set(self.data.keys()),
   
         set(('scenario', 'intervenants', 'siteshydro', 'sitesmeteo',
                 'seuilshydro', 'seuilsmeteo', 'modelesprevision',
                 'evenements', 'courbestarage', 'jaugeages',
                 'courbescorrection', 'serieshydro', 'seriesmeteo',
                 'seriesobselab', 'seriesobselabmeteo', 'simulations',
                 'seriesgradients')))
        self.assertNotEqual(self.data['scenario'], [])
        self.assertEqual(self.data['intervenants'], [])
        self.assertEqual(self.data['siteshydro'], [])
        self.assertEqual(self.data['sitesmeteo'], [])
        self.assertEqual(self.data['seuilshydro'], [])
        self.assertEqual(self.data['modelesprevision'], [])
        self.assertEqual(self.data['evenements'], [])
        self.assertEqual(self.data['serieshydro'], [])
        self.assertEqual(self.data['seriesmeteo'], [])
        self.assertEqual(self.data['simulations'], [])

        self.assertEqual(len(self.data['seriesgradients']), 3)

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod,
                         datetime.datetime(2010, 2, 26, 23, 55, 30))
        self.assertEqual(scenario.emetteur.contact.code, '1')
        self.assertEqual(scenario.emetteur.intervenant.code, '1537')
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.intervenant.code, '1537')
        self.assertEqual(scenario.destinataire.intervenant.origine, 'SANDRE')

    def test_gradients_0(self):
        """Gradients 0 test."""
        serie = self.data['seriesgradients'][0]
        self.assertEqual(serie.duree, 60)
        self.assertEqual(serie.entite.code, 'A1234567')
        self.assertEqual(serie.grd, 'Q')
        self.assertEqual(serie.contact.code, '158')
        self.assertEqual(serie.dtprod,
                         datetime.datetime(2008, 12, 15, 11, 7, 54))
        self.assertEqual(len(serie.gradients), 2)
        self.assertEqual(serie.gradients['res'].to_list(), [150.8, 130.2])
        self.assertEqual(serie.gradients['mth'].to_list(), [8, 4])
        self.assertEqual(serie.gradients['qal'].to_list(), [16, 12])
        self.assertEqual(serie.gradients['statut'].to_list(), [4, 8])
        self.assertEqual(serie.gradients.index.to_list(),
                         [datetime.datetime(2008, 12, 15, 9, 0, 0),
                          datetime.datetime(2008, 12, 15, 10, 0, 0)])

    def test_gradients_1(self):
        """Gradients 1 test."""
        serie = self.data['seriesgradients'][1]
        self.assertEqual(serie.duree, 30)
        self.assertEqual(serie.entite.code, 'A123456789')
        self.assertEqual(serie.grd, 'H')
        self.assertEqual(serie.contact.code, '130')
        self.assertEqual(serie.dtprod,
                         datetime.datetime(2009, 12, 15, 11, 7, 54))
        self.assertEqual(len(serie.gradients), 1)
        self.assertEqual(serie.gradients['res'].to_list(), [15.8])
        self.assertEqual(serie.gradients['mth'].to_list(), [0])
        self.assertEqual(serie.gradients['qal'].to_list(), [20])
        self.assertEqual(serie.gradients['statut'].to_list(), [12])
        self.assertEqual(serie.gradients.index.to_list(),
                         [datetime.datetime(2009, 12, 15, 9, 0, 0)])

    def test_gradients_2(self):
        """Gradients 2 test."""
        serie = self.data['seriesgradients'][2]
        self.assertEqual(serie.duree, 30)
        self.assertEqual(serie.entite.code, 'A12345678901')
        self.assertEqual(serie.grd, 'H')
        self.assertEqual(serie.contact.code, '130')
        self.assertEqual(serie.dtprod,
                         datetime.datetime(2009, 12, 15, 11, 7, 54))
        self.assertEqual(len(serie.gradients), 1)
        self.assertEqual(serie.gradients['res'].to_list(), [13.2])
        self.assertEqual(serie.gradients['mth'].to_list(), [14])
        self.assertEqual(serie.gradients['qal'].to_list(), [16])
        self.assertEqual(serie.gradients['statut'].to_list(), [16])
        self.assertEqual(serie.gradients.index.to_list(),
                         [datetime.datetime(2009, 12, 15, 10, 30, 0)])


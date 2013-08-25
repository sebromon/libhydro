# -*- coding: utf-8 -*-
"""Test program for xml.from_xml.

To run all tests just type:
    './test_xml_from_xml.py' or 'python test_xml_from_xml.py'

To run only a class test:
    python -m unittest test_xml_from_xml.TestClass

To run only a specific test:
    python -m unittest test_xml_from_xml.TestClass
    python -m unittest test_xml_from_xml.TestClass.test_method

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

import datetime

import libhydro.conv.xml as xml
# from libhydro.core import intervenant

#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """Version 0.1b"""
__date__ = """2013-08-25"""

#HISTORY
#V0.1 - 2013-08-24
#    first shot


#-- class TestFromXmlSiteshydro ----------------------------------------------
class TestFromXmlSitesHyros(unittest.TestCase):
    """FromXmlSitesHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = xml.parse('data/xml/1.1/siteshydro.xml')

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base(self):
        """Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'siteshydro', 'series', 'simulations'))
        )
        self.assertIsNotNone(self.data['scenario'])
        self.assertIsNotNone(self.data['siteshydro'])
        self.assertIsNone(self.data['series'])
        self.assertIsNone(self.data['simulations'])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(
            scenario.dtprod, datetime.datetime(2010, 2, 26, 12, 53, 10)
        )
        self.assertEqual(scenario.emetteur.code, 1069)
        self.assertEqual(scenario.emetteur.intervenant.code, 25)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.code, 1537)
        self.assertEqual(scenario.destinataire.origine, 'SANDRE')

    def test_sitehydro_0(self):
        """Sitehydro 0 test."""
        sitehydro = self.data['siteshydro'][0]
        self.assertEqual(sitehydro.code, 'A1984310')
        self.assertEqual(sitehydro.typesite, 'REEL')

    def test_sitehydro_1(self):
        """Sitehydro 1 test."""
        # check site
        sitehydro = self.data['siteshydro'][1]
        self.assertEqual(sitehydro.code, 'O1984310')
        self.assertEqual(
            sitehydro.libelle, 'Le Touch à Toulouse [Saint-Martin-du-Touch]'
        )
        self.assertEqual(sitehydro.typesite, 'SOURCE')
        self.assertEqual(sitehydro.code, 'O1984310')
        self.assertEqual(len(sitehydro.stations), 3)
        # check stations
        for  i in range(1, 3):
            self.assertEqual(sitehydro.stations[i - 1].code, 'O19843100%i' % i)
            self.assertEqual(sitehydro.stations[i - 1].libelle, 'station %i' % i)
            self.assertEqual(sitehydro.stations[i - 1].typestation, 'LIMNI')

    def test_sitehydro_2(self):
        """Sitehydro 2 test."""
        sitehydro = self.data['siteshydro'][2]
        self.assertEqual(sitehydro.code, 'O2000040')
        self.assertEqual(sitehydro.typesite, 'REEL')

    def test_sitehydro_3(self):
        """Sitehydro 3 test."""
        capteurs = self.data['siteshydro'][3].stations[0].capteurs
        self.assertEqual(len(capteurs), 2)
        self.assertEqual(capteurs[0].code, 'O17125100102')
        self.assertEqual(capteurs[0].typemesure, 'H')
        self.assertEqual(capteurs[1].code, 'O17125100101')
        self.assertEqual(capteurs[1].typemesure, 'H')

    def test_error_1(self):
        """Xml file with namespace error test."""
        self.assertRaises(
            ValueError,
            xml.parse,
            # *(['data/xml/1.1/siteshydro.xml'])
            *(['data/xml/1.1/siteshydro_with_namespace.xml'])
        )


#-- class TestFromXmlSitesMeteo ----------------------------------------------
#TODO

#-- class TestFromXmlObssHydro -----------------------------------------------
class TestFromXmlObssHydro(unittest.TestCase):
    """FromXmlObssHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = xml.parse('data/xml/1.1/obsshydro.xml')

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base(self):
        """Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'siteshydro', 'series', 'simulations'))
        )
        self.assertIsNotNone(self.data['scenario'])
        self.assertIsNone(self.data['siteshydro'])
        self.assertIsNotNone(self.data['series'])
        self.assertIsNone(self.data['simulations'])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod, datetime.datetime(2010, 2, 26, 7, 5))
        self.assertEqual(scenario.emetteur.code, 26)
        self.assertEqual(scenario.emetteur.intervenant.code, 1520)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.code, 1537)
        self.assertEqual(scenario.destinataire.origine, 'SANDRE')

    def test_serie_0(self):
        """Serie 0 test."""
        serie = self.data['series'][0]
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
        serie = self.data['series'][1]
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
        serie = self.data['series'][2]
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


#-- class TestFromXmlObssMeteo -----------------------------------------------
#TODO


#-- class TestFromXmlSimulations ---------------------------------------------
class TestFromXmlSimulations(unittest.TestCase):
    """FromXmlSimulations class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.data = xml.parse('data/xml/1.1/simulations.xml')

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base(self):
        """Keys test."""
        self.assertEqual(
            set(self.data.keys()),
            set(('scenario', 'siteshydro', 'series', 'simulations'))
        )
        self.assertIsNotNone(self.data['scenario'])
        self.assertIsNone(self.data['siteshydro'])
        self.assertIsNone(self.data['series'])
        self.assertIsNotNone(self.data['simulations'])

    def test_scenario(self):
        """Scenario test."""
        scenario = self.data['scenario']
        self.assertEqual(scenario.code, 'hydrometrie')
        self.assertEqual(scenario.version, '1.1')
        self.assertEqual(scenario.nom, 'Echange de données hydrométriques')
        self.assertEqual(scenario.dtprod, datetime.datetime(2010, 2, 26, 9, 30))
        self.assertEqual(scenario.emetteur.code, 41)
        self.assertEqual(scenario.emetteur.intervenant.code, 1537)
        self.assertEqual(scenario.emetteur.intervenant.origine, 'SANDRE')
        self.assertEqual(scenario.destinataire.code, 14)
        self.assertEqual(scenario.destinataire.origine, 'SANDRE')

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
            simulation.previsions.tolist(), [30, 10, 50, 25, 75, 90, 23, 25]
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
            [x[0] for x in simulation.previsions.swaplevel(0, 1).index],
            [50, 0, 100, 20, 40, 49, 50, 100]
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
        self.assertEqual(simulation.qualite, 29)
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


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

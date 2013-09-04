# -*- coding: utf-8 -*-
"""Test program for xml.xml.

To run all tests just type:
    './test_xml_xml.py' or 'python test_xml_xml.py'

To run only a class test:
    python -m unittest test_xml_xml.TestClass

To run only a specific test:
    python -m unittest test_xml_xml.TestClass
    python -m unittest test_xml_xml.TestClass.test_method

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
import numpy

from libhydro.core import intervenant
from libhydro.conv.xml import (Scenario, Message)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1c"""
__date__ = """2013-09-04"""

#HISTORY
#V0.1 - 2013-08-22
#    first shot


#-- class TestScenario --------------------------------------------------------
class TestScenario(unittest.TestCase):
    """Scenario class tests."""

    def test_base_01(self):
        """Base case scenario."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        sce = Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertEqual(
            (sce.code, sce.version, sce.nom,
             sce.emetteur, sce.destinataire),
            ('hydrometrie', '1.1', 'Echange de données hydrométriques',
             emetteur, destinataire)
        )

    def test_base_02(self):
        """Dtprod tests."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        # default dtprod is utcnow()
        sce = Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertTrue(isinstance(sce.dtprod, datetime.datetime))
        # stringt dtprod
        dtprod = '2012-12-12T05:33+00'
        sce = Scenario(
            emetteur=emetteur, destinataire=destinataire,
            dtprod=dtprod
        )
        self.assertEqual(sce.dtprod, datetime.datetime(2012, 12, 12, 5, 33))
        # datetime dtprod
        sce = Scenario(
            emetteur=emetteur, destinataire=destinataire,
            dtprod=datetime.datetime(2012, 12, 12, 5, 33)
        )
        self.assertEqual(sce.dtprod, datetime.datetime(2012, 12, 12, 5, 33))
        # datetime64 dtprod
        sce = Scenario(
            emetteur=emetteur, destinataire=destinataire,
            dtprod=numpy.datetime64(dtprod)
        )
        self.assertEqual(sce.dtprod, datetime.datetime(2012, 12, 12, 5, 33))

    def test_str_01(self):
        """Test __str__ method."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        sce = Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertTrue(sce.__str__().rfind('Message') > -1)

    def test_error_01(self):
        """Emetteur error."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertRaises(
            TypeError,
            Scenario,
            **{'emetteur': None, 'destinataire': destinataire}
        )
        self.assertRaises(
            TypeError,
            Scenario,
            **{'emetteur': 'emetteur', 'destinataire': destinataire}
        )

    def test_error_02(self):
        """Destinataire error."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertRaises(
            TypeError,
            Scenario,
            **{'emetteur': emetteur, 'destinataire': None}
        )
        self.assertRaises(
            TypeError,
            Scenario,
            **{'emetteur': emetteur, 'destinataire': 'destinataire'}
        )

    def test_error_03(self):
        """Dtprod error."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        Scenario(emetteur=emetteur, destinataire=destinataire, dtprod=None)
        self.assertRaises(
            TypeError,
            Scenario,
            **{'emetteur': emetteur, 'destinataire': destinataire, 'dtprod': {}}
        )
        self.assertRaises(
            ValueError,
            Scenario,
            **{'emetteur': emetteur, 'destinataire': destinataire, 'dtprod': 'ff'}
        )


#-- class TestMessage --------------------------------------------------------
class TestMessage(unittest.TestCase):
    """Message class tests."""

    SKIP_WRITE = (
        (not os.path.isdir(os.path.join(os.path.sep, 'tmp'))),
        'no destination for xml file writing test'
    )

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.fsit = os.path.join('data', 'xml', '1.1', 'siteshydro.xml')
        self.fobs = os.path.join('data', 'xml', '1.1', 'obsshydro.xml')
        self.fsim = os.path.join('data', 'xml', '1.1', 'simulations.xml')
        self.ftmp = os.path.join(os.path.sep, 'tmp', 'libhydro_test_file.xml')

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base_01(self):
        """Simple message."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        msg = Message(scenario=scenario, strict=False)
        self.assertEqual(msg.scenario, scenario)

    @unittest.skipIf(*SKIP_WRITE)
    def test_base_02(self):
        """Message from file siteshydro."""
        msg = Message.from_file(self.fsit)
        msg.show()
        msg.write(self.ftmp, force=True)
        msg.siteshydro = msg.siteshydro[0]

    @unittest.skipIf(*SKIP_WRITE)
    def test_base_03(self):
        """Message from file obsshydro."""
        msg = Message.from_file(self.fobs)
        msg.write(self.ftmp, force=True)
        msg.series = msg.series[0]

    @unittest.skipIf(*SKIP_WRITE)
    def test_base_04(self):
        """Message from file simulations."""
        msg = Message.from_file(self.fsim)
        msg.write(self.ftmp, force=True)
        msg.simulations = msg.simulations[0]

    def test_error_01(self):
        """Scenario error."""
        # emetteur = intervenant.Contact()
        # destinataire = intervenant.Intervenant()
        # scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        # msg = Message(scenario=scenario, strict=False)
        self.assertRaises(
            TypeError,
            Message,
            # **{'scenario': scenario, 'strict': False}
            **{'scenario': None, 'strict': False}
        )
        self.assertRaises(
            TypeError,
            Message,
            **{'scenario': 'scenario'}
        )

    def test_error_02(self):
        """Siteshydro error."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertRaises(
            TypeError,
            Message,
            **{'scenario': scenario, 'siteshydro': 'siteshydro'}
        )

    def test_error_03(self):
        """Series error."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertRaises(
            TypeError,
            Message,
            **{'scenario': scenario, 'series': 'series'}
        )

    def test_error_04(self):
        """Simulations error."""
        emetteur = intervenant.Contact()
        destinataire = intervenant.Intervenant()
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertRaises(
            TypeError,
            Message,
            **{'scenario': scenario, 'simulations': 'simulations'}
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

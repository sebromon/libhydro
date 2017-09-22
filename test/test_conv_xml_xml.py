# coding: utf-8
"""Test program for xml.xml.

To run all tests just type:
    python -m unittest test_conv_xml_xml

To run only a class test:
    python -m unittest test_conv_xml_xml.TestClass

To run only a specific test:
    python -m unittest test_conv_xml_xml.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import os
import tempfile
import shutil

import unittest

import datetime
import numpy

from libhydro.core import intervenant
from libhydro.conv.xml import (Scenario, Message)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin""" \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2.1"""
__date__ = """2017-07-05"""

# HISTORY
# V0.2.1 - SR - 2017-07-05
# Ajout tests jaugeages
# V0.2 - SR - 2017-06-22
# Ajout tests courbes de correction et de tarage
# V0.1 - 2013-08-22
#   first shot

# -- config -------------------------------------------------------------------
FILES_PATH = os.path.join('data', 'xml', '1.1')


# -- class TestScenario -------------------------------------------------------
class TestScenario(unittest.TestCase):

    """Scenario class tests."""

    def test_base_01(self):
        """Base case scenario."""
        destinataire = intervenant.Intervenant(
            contacts=[intervenant.Contact(code='99')]
        )
        emetteur = intervenant.Contact(code='98', intervenant=intervenant.Intervenant())
        sce = Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertEqual(
            (
                sce.code, sce.version, sce.nom,
                sce.emetteur.intervenant, sce.emetteur.contact,
                sce.destinataire.intervenant, sce.destinataire.contact),
            (
                'hydrometrie', '1.1', 'Echange de données hydrométriques',
                emetteur.intervenant, emetteur,
                destinataire, destinataire.contacts[0]
            )
        )

    def test_base_02(self):
        """Dtprod tests."""
        emetteur = intervenant.Intervenant()
        destinataire = intervenant.Contact(
            code=55,
            intervenant=intervenant.Intervenant(code=1537)
        )
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
        emetteur = intervenant.Intervenant()
        destinataire = intervenant.Intervenant()
        sce = Scenario(emetteur=emetteur, destinataire=destinataire)
        self.assertTrue(sce.__str__().rfind('Message') > -1)

    def test_error_01(self):
        """Emetteur error."""
        destinataire = intervenant.Intervenant()
        emetteur = intervenant.Contact(code='99', intervenant=intervenant.Intervenant())
        Scenario(emetteur=emetteur, destinataire=destinataire)
        with self.assertRaises(TypeError):
            Scenario(emetteur=None, destinataire=destinataire)
        with self.assertRaises(TypeError):
            Scenario(emetteur='emetteur', destinataire=destinataire)
        # a Contact without Intervenant emetteur
        emetteur.intervenant = None
        with self.assertRaises(TypeError):
            Scenario(emetteur=emetteur, destinataire=destinataire)

    def test_error_02(self):
        """Destinataire error."""
        destinataire = intervenant.Intervenant()
        emetteur = intervenant.Intervenant()
        Scenario(emetteur=emetteur, destinataire=destinataire)
        with self.assertRaises(TypeError):
            Scenario(emetteur=emetteur, destinataire=None)
        with self.assertRaises(TypeError):
            Scenario(emetteur=emetteur, destinataire='destinataire')
        # a Contact without an Intervenant
        destinataire = intervenant.Contact(
            code=5, intervenant=intervenant.Intervenant()
        )
        Scenario(emetteur=emetteur, destinataire=destinataire)
        destinataire.intervenant = None
        with self.assertRaises(TypeError):
            Scenario(emetteur=emetteur, destinataire=destinataire)

    def test_error_03(self):
        """Dtprod error."""
        emetteur = intervenant.Intervenant(code=5)
        destinataire = intervenant.Intervenant(code=8, nom='toto')
        Scenario(emetteur=emetteur, destinataire=destinataire, dtprod=None)
        with self.assertRaises(ValueError):
            Scenario(
                emetteur=emetteur,
                destinataire=destinataire,
                dtprod=2012
            )
        with self.assertRaises(ValueError):
            Scenario(
                emetteur=emetteur,
                destinataire=destinataire,
                dtprod='2012-13-24'
            )


# -- class TestMessage --------------------------------------------------------
class TestMessage(unittest.TestCase):

    """Message class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        self.file_sith = os.path.join(FILES_PATH, 'siteshydro.xml')
        self.file_sitm = os.path.join(FILES_PATH, 'sitesmeteo.xml')
        self.file_seu = os.path.join(FILES_PATH, 'seuilshydro.xml')
        self.file_eve = os.path.join(FILES_PATH, 'evenements.xml')
        self.file_ct = os.path.join(FILES_PATH, 'courbestarage.xml')
        self.file_jaug = os.path.join(FILES_PATH, 'jaugeages.xml')
        self.file_cc = os.path.join(FILES_PATH, 'courbescorrection.xml')
        self.file_serh = os.path.join(FILES_PATH, 'serieshydro.xml')
        self.file_serm = os.path.join(FILES_PATH, 'seriesmeteo.xml')
        self.file_sim = os.path.join(FILES_PATH, 'simulations.xml')
        self.tmp_dir = tempfile.mkdtemp(prefix='test_xml_')
        self.tmp_file = tempfile.mktemp(dir=self.tmp_dir)

    def tearDown(self):
        """Hook method for deconstructing the test fixture after testing it."""
        shutil.rmtree(self.tmp_dir)

    def test_base_01(self):
        """Simple message."""
        emetteur = intervenant.Contact(10)
        emetteur.intervenant = intervenant.Intervenant(1537, mnemo='SCHAPI')
        destinataire = intervenant.Intervenant()
        destinataire.contacts = [
            intervenant.Contact(5),
            intervenant.Contact(15),
            intervenant.Contact(555)
        ]
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        msg = Message(scenario=scenario, strict=False)
        self.assertEqual(msg.scenario, scenario)
        self.assertEqual(scenario.emetteur.intervenant, emetteur.intervenant)
        self.assertEqual(scenario.emetteur.contact, emetteur)
        self.assertEqual(scenario.destinataire.intervenant, destinataire)
        self.assertEqual(
            scenario.destinataire.contact, destinataire.contacts[0]
        )

    def test_base_02(self):
        """Message from file siteshydro."""
        msg = Message.from_file(self.file_sith)
        msg.show()
        msg.write(self.tmp_file, force=True)
        msg.siteshydro = [msg.siteshydro[0]]

    def test_base_03(self):
        """Message from file sitesmeteo."""
        msg = Message.from_file(self.file_sitm)
        msg.show()
        msg.write(self.tmp_file, force=True)
        msg.sitesmeteo = [msg.sitesmeteo[0]]

    def test_base_04(self):
        """Message from file seuilshydro."""
        msg = Message.from_file(self.file_seu)
        msg.show()
        msg.write(self.tmp_file, force=True)
        msg.seuilshydro.append(msg.seuilshydro[0])
        msg.seuilshydro[1] = msg.seuilshydro[0]

    def test_base_05(self):
        """Message from file evenements."""
        msg = Message.from_file(self.file_eve)
        msg.show()
        msg.write(self.tmp_file, force=True)
        msg.evenements.extend([msg.evenements[0]])

    def test_base_06(self):
        """Message from file serieshydro."""
        msg = Message.from_file(self.file_serh)
        msg.write(self.tmp_file, force=True)
        msg.serieshydro[:] = (msg.serieshydro[0],)

    def test_base_07(self):
        """Message from file seriesmeteo."""
        msg = Message.from_file(self.file_serm)
        msg.write(self.tmp_file, force=True)
        msg.seriesmeteo[:] = (msg.seriesmeteo[0],)

    def test_base_08(self):
        """Message from file simulations."""
        msg = Message.from_file(self.file_sim)
        msg.write(self.tmp_file, force=True)
        msg.simulations.insert(0, msg.simulations[0])

    def test_base_09(self):
        """Message from a file with namespaces."""
        fname = os.path.join(FILES_PATH, 'siteshydro_with_namespace.xml')
        msg = Message.from_file(fname)
        msg.write(self.tmp_file, force=True)

    def test_base_10(self):
        """Message from file courbestarage."""
        msg = Message.from_file(self.file_ct)
        msg.write(self.tmp_file, force=True)
        msg.courbestarage.insert(0, msg.courbestarage[0])

    def test_base_11(self):
        """Message from file courbescorrection."""
        msg = Message.from_file(self.file_cc)
        msg.write(self.tmp_file, force=True)
        msg.courbescorrection.insert(0, msg.courbescorrection[0])

    def test_base_12(self):
        """Message from file jaugeages."""
        msg = Message.from_file(self.file_jaug)
        self.assertTrue(len(msg.jaugeages) > 0)
        msg.write(self.tmp_file, force=True)
        msg.jaugeages.insert(0, msg.jaugeages[0])

    def test_base_13(self):
        """Message from string (str) serieshydro"""
        with open(self.file_serh, 'r') as f:
            content = f.read()
        self.assertTrue(isinstance(content, str))
        msg = Message.from_string(content)
        msg.write(self.tmp_file, force=True)
        msg.serieshydro[:] = (msg.serieshydro[0],)

    def test_base_14(self):
        """Message from string (bytes) serieshydro"""
        with open(self.file_serh, 'r') as f:
            content = f.read().encode('utf8')
        self.assertTrue(isinstance(content, bytes))
        msg = Message.from_string(content)
        msg.write(self.tmp_file, force=True)
        msg.serieshydro[:] = (msg.serieshydro[0],)

    def test_base_15(self):
        """test Message.to_string"""
        msg = Message.from_file(self.file_serh)
        content = msg.to_string()
        self.assertTrue(isinstance(content, str))
        msg2 = Message.from_string(content)
        for i in range(0, len(msg.serieshydro)):
            self.assertEqual(msg.serieshydro[i], msg2.serieshydro[i])

    def test_str_01(self):
        """Test __str__ method with basic values."""
        emetteur = intervenant.Contact(
            5,
            intervenant=intervenant.Intervenant(1537)
        )
        destinataire = intervenant.Intervenant()
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        msg = Message(scenario=scenario, strict=False)
        self.assertTrue(msg.__str__().rfind('Message') > -1)

    def test_str_02(self):
        """Test __str__ method without scenario."""
        msg = Message(scenario='', strict=False)
        self.assertTrue(msg.__str__().rfind('Message') > -1)
        self.assertTrue(msg.__str__().rfind('sans scenario') > -1)

    def test_error_01(self):
        """Scenario error."""
        emetteur = intervenant.Contact(
            53, intervenant=intervenant.Intervenant(4589)
        )
        destinataire = intervenant.Intervenant(code=248, nom='The Boss')
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        assert Message(scenario=scenario, strict=False)
        with self.assertRaises(TypeError):
            Message(scenario=None, strict=False)
        with self.assertRaises(TypeError):
            Message(scenario='scenario')

    def test_error_02(self):
        """Siteshydro error."""
        emetteur = intervenant.Intervenant()
        destinataire = intervenant.Intervenant()
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        with self.assertRaises(TypeError):
            Message(scenario=scenario, siteshydro='siteshydro')

    def test_error_03(self):
        """Seuilshydro error."""
        emetteur = intervenant.Intervenant()
        destinataire = intervenant.Intervenant()
        destinataire.contacts = [
            intervenant.Contact(code='99'),
            intervenant.Contact(code='5'),
            intervenant.Contact(code='999'),
            intervenant.Contact(code='123')
        ]
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        with self.assertRaises(TypeError):
            Message(scenario=scenario, seuilshydro='seuilshydro')

    def test_error_04(self):
        """Evenements error."""
        emetteur = intervenant.Intervenant()
        destinataire = intervenant.Intervenant()
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        with self.assertRaises(TypeError):
            Message(scenario=scenario, evenements='evenements')

    def test_error_05(self):
        """Series error."""
        emetteur = intervenant.Contact(code='99')
        emetteur.intervenant = intervenant.Intervenant(1845)
        destinataire = intervenant.Intervenant()
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        with self.assertRaises(TypeError):
            Message(scenario=scenario, series='series')

    def test_error_06(self):
        """Simulations error."""
        emetteur = intervenant.Intervenant(1623, nom='GAD')
        destinataire = intervenant.Intervenant(mnemo='nemo')
        scenario = Scenario(emetteur=emetteur, destinataire=destinataire)
        with self.assertRaises(TypeError):
            Message(scenario=scenario, simulations='simulations')

    def test_add_01(self):
        """Add elements to message."""
        msg = Message.from_file(self.file_sith)
        msg2 = Message.from_file(self.file_serh)
        msg3 = Message.from_file(self.file_sim)
        msg.add(serieshydro=msg2.serieshydro, simulations=msg3.simulations)
        self.assertEqual(msg.serieshydro, msg2.serieshydro)
        self.assertEqual(msg.simulations, msg3.simulations)

    def test_add_error_01(self):
        """Add error."""
        msg = Message.from_file(self.file_sith)
        with self.assertRaises(TypeError):
            msg.add(blurp='')
        with self.assertRaises(ValueError):
            msg.add(serieshydro='eee')

    def test_write_error_01(self):
        """Write existing file."""
        msg = Message.from_file(self.file_sith)
        msg.write(self.tmp_file, force=True)
        with self.assertRaises(IOError):
            msg.write(self.tmp_file)

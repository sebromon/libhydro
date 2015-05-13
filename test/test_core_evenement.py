# coding: utf-8
"""Test program for evenement.

To run all tests just type:
    python -m unittest test_core_evenement

To run only a class test:
    python -m unittest test_core_evenement.TestClass

To run only a specific test:
    python -m unittest test_core_evenement.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys
sys.path.append('..')

import datetime
import unittest

from libhydro.core import evenement
from libhydro.core import sitehydro
from libhydro.core import intervenant


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1d"""
__date__ = """2014-12-17"""

# HISTORY
# V0.1 - 2013-11-26
#   first shot


# -- class Testevenement ------------------------------------------------------
class Testevenement(unittest.TestCase):

    """Evenement class tests."""

    def test_base_01(self):
        """Minimum evenement."""
        entite = sitehydro.Sitehydro('R5330101')
        descriptif = 'some texte here'
        contact = intervenant.Contact(nom='moi')
        e = evenement.Evenement(
            entite=entite, descriptif=descriptif, contact=contact
        )
        self.assertEqual(
            (e.entite, e.descriptif, e.contact, e.publication),
            (entite, descriptif, contact, 100)
        )

    def test_base_02(self):
        """Full evenement."""
        entite = sitehydro.Station('R533010110')
        descriptif = 'some texte here'
        contact = intervenant.Contact(nom='moi')
        dt = datetime.datetime(1852, 2, 8, 5, 10, 8)
        publication = 10
        e = evenement.Evenement(
            entite=entite, descriptif=descriptif, contact=contact,
            dt=dt, publication=publication, dtmaj=dt
        )
        self.assertEqual(
            (e.entite, e.descriptif, e.contact, e.publication, e.dt, e.dtmaj),
            (entite, descriptif, contact, publication, dt, dt)
        )

    def test_str_01(self):
        """Test __str__ method."""
        entite = sitehydro.Station('R533010110')
        descriptif = 'some texte here'
        contact = intervenant.Contact(nom='moi')
        e = evenement.Evenement(
            entite=entite, contact=contact, descriptif=descriptif
        )
        self.assertTrue(e.__str__().rfind('Evenement') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode."""
        entite = sitehydro.Station('R533010110')
        descriptif = 'some texte here'
        publication = 9999
        e = evenement.Evenement(
            entite=entite, contact=None, descriptif=descriptif,
            publication=publication, strict=False
        )
        self.assertEqual(
            (e.contact, e.publication), (None, publication)
        )

    def test_error_01(self):
        """Entite error."""
        entite = sitehydro.Station('R533010110')
        descriptif = 'some texte here'
        contact = intervenant.Contact(nom='moi')
        e = evenement.Evenement(
            entite=entite, contact=contact, descriptif=descriptif
        )
        self.assertEqual(e.entite, entite)
        self.assertRaises(
            TypeError,
            evenement.Evenement,
            **{'entite': None, 'contact': contact, 'descriptif': descriptif}
        )
        self.assertRaises(
            TypeError,
            evenement.Evenement,
            **{'entite': 3, 'contact': contact, 'descriptif': descriptif}
        )

    def test_error_02(self):
        """Descriptif error."""
        entite = sitehydro.Station('R533010110')
        descriptif = 'some texte here'
        contact = intervenant.Contact(nom='moi')
        e = evenement.Evenement(
            entite=entite, contact=contact, descriptif=descriptif
        )
        self.assertEqual(e.descriptif, descriptif)
        self.assertRaises(
            TypeError,
            evenement.Evenement,
            **{'entite': entite, 'contact': contact, 'descriptif': None}
        )

    def test_error_03(self):
        """Contact error."""
        entite = sitehydro.Station('R533010110')
        descriptif = 'some texte here'
        contact = intervenant.Contact(nom='moi')
        e = evenement.Evenement(
            entite=entite, contact=contact, descriptif=descriptif
        )
        self.assertEqual(e.contact, contact)
        self.assertRaises(
            TypeError,
            evenement.Evenement,
            **{'entite': entite, 'contact': None, 'descriptif': descriptif}
        )

    def test_error_04(self):
        """Publication error."""
        entite = sitehydro.Station('R533010110')
        descriptif = 'some texte here'
        contact = intervenant.Contact(nom='moi')
        e = evenement.Evenement(
            entite=entite, contact=contact, descriptif=descriptif,
            publication=10
        )
        self.assertRaises(
            ValueError,
            e.__setattr__,
            *('publication', None)
        )
        self.assertRaises(
            ValueError,
            e.__setattr__,
            *('publication', 9999)
        )

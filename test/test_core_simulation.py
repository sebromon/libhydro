# coding: utf-8
"""Test program for simulation.

To run all tests just type:
    python -m unittest test_core_simulation

To run only a class test:
    python -m unittest test_core_simulation.TestClass

To run only a specific test:
    python -m unittest test_core_simulation.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import unittest
import datetime

from libhydro.core import (simulation, modeleprevision, sitehydro)


# -- strings ------------------------------------------------------------------
__version__ = '0.1.8'
__date__ = '2015-05-24'

# HISTORY
# V0.1 - 2013-08-07
#   first shot


# -- class TestPrevisionTendance ----------------------------------------------
class TestPrevisionTendance(unittest.TestCase):

    """PrevisionTendance class tests."""

    def test_base_01(self):
        """Simple prevision."""
        dte = '2012-05-18 18:36+00'
        res = 33.5
        p = simulation.PrevisionTendance(dte, res)
        self.assertEqual(
            p.item(),
            (datetime.datetime(2012, 5, 18, 18, 36), res, 'moy'))

    def test_base_02(self):
        """Prevision with tendency."""
        dte = '2012-05-18 00:00+00'
        res = 33.5
        tend = 'min'
        p = simulation.PrevisionTendance(dte=dte, res=res, tend=tend)
        self.assertEqual(
            p.item(),
            (datetime.datetime(2012, 5, 18), res, tend))
        self.assertEqual(
            (p['dte'].item(), p['res'].item(), p['tend'].item()),
            (datetime.datetime(2012, 5, 18), res, tend))

    def test_str_01(self):
        """Test __str__ method with minimum values."""
        dte = '2012-05-18 00:00+00'
        res = 33
        p = simulation.PrevisionTendance(dte=dte, res=res)
        self.assertTrue(p.__str__().rfind('de tendance') > -1)
        self.assertTrue(p.__str__().rfind('UTC') > -1)

    def test_error_01(self):
        """Date error."""
        simulation.PrevisionTendance(**{'dte': '2012-10-10 10', 'res': 25.8})
        self.assertRaises(
            ValueError,
            simulation.PrevisionTendance,
            **{'dte': '2012-10-55', 'res': 25.8})

    def test_error_02(self):
        """Test res error."""
        simulation.PrevisionTendance(**{'dte': '2012-10-10 10:10', 'res': 10})
        self.assertRaises(
            ValueError,
            simulation.PrevisionTendance,
            **{'dte': '2012-10-10 10:10', 'res': 'xxx'})

    def test_error_03(self):
        """tendance error."""
        simulation.PrevisionTendance(
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'tend': 'moy'})
        self.assertRaises(
            ValueError,
            simulation.PrevisionTendance,
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'tend': 'median'})
        self.assertRaises(
            ValueError,
            simulation.PrevisionTendance,
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'tend': 'mediane'})


# -- class TestPrevisionPrb ---------------------------------------------------
class TestPrevisionPrb(unittest.TestCase):

    """PrevisionPrb class tests."""

    def test_base_01(self):
        """Simple prevision."""
        dte = '2012-05-18 18:36+00'
        res = 33.5
        p = simulation.PrevisionPrb(dte, res)
        self.assertEqual(
            p.item(),
            (datetime.datetime(2012, 5, 18, 18, 36), res, 50))

    def test_base_02(self):
        """Prevision with probability."""
        dte = '2012-05-18 00:00+00'
        res = 33.5
        prb = 22.3
        p = simulation.PrevisionPrb(dte=dte, res=res, prb=prb)
        self.assertEqual(
            p.item(),
            (datetime.datetime(2012, 5, 18), res, int(prb)))
        self.assertEqual(
            (p['dte'].item(), p['res'].item(), p['prb'].item()),
            (datetime.datetime(2012, 5, 18), res, int(prb)))

    def test_str_01(self):
        """Test __str__ method with minimum values."""
        dte = '2012-05-18 00:00+00'
        res = 33
        p = simulation.PrevisionPrb(dte=dte, res=res)
        self.assertTrue(p.__str__().rfind('avec une probabilite') > -1)
        self.assertTrue(p.__str__().rfind('UTC') > -1)

    def test_error_01(self):
        """Date error."""
        simulation.PrevisionPrb(**{'dte': '2012-10-10 10', 'res': 25.8})
        self.assertRaises(
            ValueError,
            simulation.PrevisionPrb,
            **{'dte': '2012-10-55', 'res': 25.8})

    def test_error_02(self):
        """Test res error."""
        simulation.PrevisionPrb(**{'dte': '2012-10-10 10:10', 'res': 10})
        self.assertRaises(
            ValueError,
            simulation.PrevisionPrb,
            **{'dte': '2012-10-10 10:10', 'res': 'xxx'})

    def test_error_03(self):
        """Prb error."""
        simulation.PrevisionPrb(
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'prb': 22.3})
        self.assertRaises(
            ValueError,
            simulation.PrevisionPrb,
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'prb': -1})
        self.assertRaises(
            ValueError,
            simulation.PrevisionPrb,
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'prb': 111})


# -- class TestPrevisionsPrb --------------------------------------------------
class TestPrevisionsPrb(unittest.TestCase):

    """PrevisionsPrb class tests."""

    def test_base_01(self):
        """Test previsions with one prevision."""
        dte = datetime.datetime(1953, 5, 18, 18, 5, 33)
        res = 8956321.2569
        prb = 75
        prvs = simulation.PrevisionsPrb(
            simulation.PrevisionPrb(dte=dte, res=res, prb=prb))
        self.assertEqual(prvs.tolist(), [res])
        self.assertEqual(prvs.index.tolist(), [(dte, prb), ])

    def test_base_02(self):
        """Base previsions."""
        d = [datetime.datetime(2012, 5, 18, 18, 0),
             datetime.datetime(2012, 5, 18, 18, 5),
             datetime.datetime(2012, 5, 18, 18, 10)]
        r = [33.5, 35, 40]
        p = simulation.PrevisionsPrb(
            simulation.PrevisionPrb(d[0], r[0]),
            simulation.PrevisionPrb(d[1], r[1]),
            simulation.PrevisionPrb(d[2], r[2]))
        self.assertEqual(p.tolist(), r)
        self.assertEqual([t[0] for t in p.index.tolist()], d)
        self.assertEqual(
            [t[1] for t in p.index.tolist()], [50, 50, 50])

    def test_error_01(self):
        """Prevision error."""
        prv = simulation.PrevisionPrb(
            **{'dte': '2012-10-10 10', 'res': 25.8, 'prb': 3})
        simulation.PrevisionsPrb(prv)
        simulation.PrevisionsPrb(*[prv, prv, prv])
        self.assertRaises(TypeError, simulation.PrevisionsPrb, 44)


# -- class TestSimulation -----------------------------------------------------
class TestSimulation(unittest.TestCase):

    """Simulation class tests."""

    def test_base_01(self):
        """Empty simulation."""
        sim = simulation.Simulation()
        self.assertEqual(sim.entite, None)
        self.assertEqual(sim.modeleprevision, None)
        self.assertEqual(sim.grandeur, None)
        self.assertEqual(sim.statut, 4)
        self.assertEqual(sim.qualite, None)
        self.assertEqual(sim.public, False)
        self.assertEqual(sim.commentaire, None)
        self.assertEqual(sim.dtprod, None)
        self.assertEqual(sim.previsions_tend, None)
        self.assertEqual(sim.previsions_prb, None)

    def test_base_02(self):
        """Full simulation."""
        entite = sitehydro.Sitehydro(code=44, strict=False)
        modele = modeleprevision.Modeleprevision(code=3)
        grandeur = 'Q'
        statut = 16
        qualite = 53
        public = False
        commentaire = 'The Ultimate Question of Life, the Universe and' \
                      'Everything'
        dtprod = datetime.datetime(2012, 5, 18, 18, 36)
        previsions_prb = simulation.PrevisionsPrb(
            simulation.PrevisionPrb(
                **{'dte': '2012-10-10 10', 'res': 25.8, 'prb': 3}))
        sim = simulation.Simulation(
            entite=entite,
            modeleprevision=modele,
            grandeur=grandeur,
            statut=statut,
            qualite=qualite,
            public=public,
            commentaire=commentaire,
            dtprod=dtprod,
            previsions_prb=previsions_prb)
        self.assertEqual(sim.entite, entite)
        self.assertEqual(sim.modeleprevision, modele)
        self.assertEqual(sim.grandeur, grandeur)
        self.assertEqual(sim.statut, statut)
        self.assertEqual(sim.qualite, qualite)
        self.assertEqual(sim.public, public)
        self.assertEqual(sim.commentaire, commentaire)
        self.assertEqual(sim.dtprod, dtprod)
        self.assertEqual(sim.previsions_prb.all(), previsions_prb.all())

    def test_base_03(self):
        """Dtprod can be a string."""
        sim = simulation.Simulation(dtprod='2012-05-18T18:36Z')
        self.assertEqual(sim.dtprod, datetime.datetime(2012, 5, 18, 18, 36))
        sim = simulation.Simulation(dtprod='2012-05-18 18:36+02')
        self.assertEqual(sim.dtprod, datetime.datetime(2012, 5, 18, 16, 36))

    def test_str_01(self):
        """Test __str__ method with minimum values."""
        # None values
        sim = simulation.Simulation()
        self.assertTrue(sim.__str__().rfind('Simulation') > -1)
        self.assertTrue(sim.__str__().rfind('Date de production') > -1)
        self.assertTrue(sim.__str__().rfind('Commentaire') > -1)
        self.assertTrue(sim.__str__().rfind('Previsions') > -1)
        # a junk entite
        sim = simulation.Simulation(entite='station 33', strict=False)
        self.assertTrue(sim.__str__().rfind('entite inconnue') > -1)
        # a junk statut
        sim = simulation.Simulation(statut=999, strict=False)
        self.assertTrue(sim.__str__().rfind('sans statut') > -1)

    def test_str_02(self):
        """Test __str__ method with basic values."""
        previsions_prb = simulation.PrevisionsPrb(
            simulation.PrevisionPrb(
                **{'dte': '2012-10-10 10', 'res': 25.8, 'prb': 3}))
        sim = simulation.Simulation(
            dtprod='2012-05-18T18:36Z',
            entite=sitehydro.Station(
                code=0, libelle='Toulouse', strict=False),
            previsions_prb=previsions_prb)
        self.assertTrue(sim.__str__().rfind('Simulation') > -1)
        self.assertTrue(sim.__str__().rfind('Date de production') > -1)
        self.assertTrue(sim.__str__().rfind('Commentaire') > -1)
        self.assertTrue(sim.__str__().rfind('Previsions') > -1)

    def test_str_03(self):
        """Test __str__ method with big Previsions."""
        previsions_prb = simulation.PrevisionsPrb(
            *[simulation.PrevisionPrb(dte='20%i-10-10 10' % x, res=x)
              for x in range(10, 50)])
        sim = simulation.Simulation(
            dtprod='2012-05-18T18:36Z',
            entite=sitehydro.Station(code=0, strict=False),
            previsions_prb=previsions_prb)
        self.assertTrue(sim.__str__().rfind('Simulation') > -1)
        self.assertTrue(sim.__str__().rfind('Date de production') > -1)
        self.assertTrue(sim.__str__().rfind('Commentaire') > -1)
        self.assertTrue(sim.__str__().rfind('Previsions') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        entite = 'station'
        modele = 'modele'
        grandeur = 'RR'
        statut = 333333
        public = True
        commentaire = 'Nong'
        dtprod = datetime.datetime(2012, 5, 18, 18, 36)
        qualite = 100
        previsions_prb = [10, 20, 30]
        sim = simulation.Simulation(
            entite=entite,
            modeleprevision=modele,
            grandeur=grandeur,
            statut=statut,
            qualite=qualite,
            public=public,
            commentaire=commentaire,
            dtprod=dtprod,
            previsions_prb=previsions_prb,
            strict=False)
        self.assertEqual(sim.entite, entite)
        self.assertEqual(sim.modeleprevision, modele)
        self.assertEqual(sim.grandeur, grandeur)
        self.assertEqual(sim.statut, statut)
        self.assertEqual(sim.qualite, qualite)
        self.assertEqual(sim.public, public)
        self.assertEqual(sim.commentaire, commentaire)
        self.assertEqual(sim.dtprod, dtprod)
        self.assertEqual(sim.previsions_prb, previsions_prb)

    def test_error_01(self):
        """Entite error."""
        # init
        site = sitehydro.Sitehydro(code='A0440101')
        station = sitehydro.Station(code='A044010101')
        simul = simulation.Simulation(
            **{'entite': station, 'grandeur': 'H'})
        self.assertEqual(simul.grandeur, 'H')
        # wrong entite
        self.assertRaises(
            TypeError,
            simulation.Simulation,
            # **{'entite': entite}
            **{'entite': 25})
        # site with a H simulation
        self.assertRaises(
            TypeError,
            simulation.Simulation,
            **{'entite': site, 'grandeur': 'H'})
        # station with a Q simulation
        self.assertRaises(
            TypeError,
            simulation.Simulation,
            **{'entite': station, 'grandeur': 'Q'})

    def test_error_02(self):
        """Modeleprevision error."""
        modele = modeleprevision.Modeleprevision()
        simulation.Simulation(**{'modeleprevision': modele})
        self.assertRaises(
            TypeError,
            simulation.Simulation,
            # **{'modeleprevision': modele}
            **{'modeleprevision': 'gloup !'})

    def test_error_03(self):
        """Grandeur error."""
        simulation.Simulation(**{'grandeur': 'Q'})
        simulation.Simulation(**{'grandeur': None})
        self.assertRaises(
            ValueError,
            simulation.Simulation,
            # **{'grandeur': 'H'}
            **{'grandeur': 'RR'})

    def test_error_04(self):
        """Statut error."""
        simulation.Simulation(**{'statut': 16})
        self.assertRaises(
            ValueError,
            simulation.Simulation,
            # **{'statut': 16}
            **{'statut': None})
        self.assertRaises(
            ValueError,
            simulation.Simulation,
            # **{'statut': 16}
            **{'statut': 111111})

    def test_error_05(self):
        """Qualite error."""
        simulation.Simulation(**{'qualite': 45})
        self.assertRaises(
            ValueError,
            simulation.Simulation,
            # **{'qualite': 45}
            **{'qualite': -1})

    def test_error_06(self):
        """Dtprod error."""
        dtprod = datetime.datetime(2020, 1, 1, 10, 0)
        simulation.Simulation(**{'dtprod': dtprod})
        dtprod = '2020-01-01 10:00'
        simulation.Simulation(**{'dtprod': dtprod})
        self.assertRaises(
            (TypeError, ValueError),
            simulation.Simulation,
            # **{'dtprod': dtprod}
            **{'dtprod': '2020-10 10:00'})

    def test_error_07(self):
        """Test previsions error."""
        prvs = simulation.PrevisionsPrb(
            simulation.PrevisionPrb(
                **{'dte': '2012-10-10 10', 'res': 25.8, 'prb': 3}))
        simulation.Simulation(**{'previsions_prb': prvs})
        self.assertRaises(
            TypeError,
            simulation.Simulation,
            # **{'previsions': prvs}
            **{'previsions_prb': [110, 20, 30]})

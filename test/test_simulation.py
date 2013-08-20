# -*- coding: utf-8 -*-
"""Test program for simulation.

To run all tests just type:
    './test_ simulation.py' or 'python test_ simulation.py'

To run only a class test:
    python -m unittest test_ simulation.TestClass

To run only a specific test:
    python -m unittest test_ simulation.TestClass
    python -m unittest test_ simulation.TestClass.test_method

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

from libhydro.core import (simulation, modeleprevision, sitehydro)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """Version 0.1c"""
__date__ = """2013-08-20"""

#HISTORY
#V0.1 - 2013-08-07
#    first shot


#-- todos ---------------------------------------------------------------------


#-- config --------------------------------------------------------------------


#-- class TestPrevision -------------------------------------------------------
class TestPrevision(unittest.TestCase):
    """Prevision class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base_01(self):
        """Simple prevision."""
        dte = '2012-05-18 18:36+00'
        res = 33.5
        p = simulation.Prevision(dte, res)
        self.assertEqual(
            p.item(),
            (datetime.datetime(2012, 5, 18, 18, 36), res, 50)
        )

    def test_base_02(self):
        """Prevision with probability."""
        dte = '2012-05-18 00:00+00'
        res = 33.5
        prb = 22.3
        p = simulation.Prevision(dte=dte, res=res, prb=prb)
        self.assertEqual(
            p.item(),
            (datetime.datetime(2012, 5, 18), res, int(prb))
        )
        self.assertEqual(
            (p['dte'].item(), p['res'].item(), p['prb'].item()),
            (datetime.datetime(2012, 5, 18), res, int(prb))
        )

    def test_str_01(self):
        """Test __str__ method with minimum values."""
        dte = '2012-05-18 00:00+00'
        res = 33
        p = simulation.Prevision(dte=dte, res=res)
        self.assertTrue(p.__str__().rfind('avec une probabilite') > -1)
        self.assertTrue(p.__str__().rfind('UTC') > -1)

    def test_error_01(self):
        """Date error."""
        simulation.Prevision(**{'dte': '2012-10-10 10', 'res': 25.8})
        self.assertRaises(
            TypeError,
            simulation.Prevision,
            **{'dte': '2012-10-10', 'res': 25.8}
        )

    def test_error_02(self):
        """Res error."""
        simulation.Prevision(**{'dte': '2012-10-10 10:10', 'res': 10})
        self.assertRaises(
            ValueError,
            simulation.Prevision,
            **{'dte': '2012-10-10 10:10', 'res': 'xxx'}
        )

    def test_error_03(self):
        """Prb error."""
        simulation.Prevision(**{'dte': '2012-10-10 10:10', 'res': 25.8, 'prb': 22.3})
        self.assertRaises(
            ValueError,
            simulation.Prevision,
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'prb': -1}
        )
        self.assertRaises(
            ValueError,
            simulation.Prevision,
            **{'dte': '2012-10-10 10:10', 'res': 25.8, 'prb': 111}
        )


#-- class TestPrevisions ------------------------------------------------------
class TestPrevisions(unittest.TestCase):
    """Previsions class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

    def test_base_01(self):
        """Previsions with one prevision."""
        dte = datetime.datetime(1953, 5, 18, 18, 5, 33)
        res = 8956321.2569
        prb = 75
        prvs = simulation.Previsions(
            simulation.Prevision(dte=dte, res=res, prb=prb)
        )
        self.assertEqual(prvs.tolist(), [res])
        self.assertEqual(
            prvs.index.tolist(),
            [(dte, prb), ]
        )

    def test_base_02(self):
        """Base previsions."""
        d = [
            datetime.datetime(2012, 5, 18, 18, 0),
            datetime.datetime(2012, 5, 18, 18, 5),
            datetime.datetime(2012, 5, 18, 18, 10)
        ]
        r = [33.5, 35, 40]
        p = simulation.Previsions(
            simulation.Prevision(d[0], r[0]),
            simulation.Prevision(d[1], r[1]),
            simulation.Prevision(d[2], r[2])
        )
        self.assertEqual(p.tolist(), r)
        self.assertEqual(
            [t[0] for t in p.index.tolist()],
            d
        )
        self.assertEqual(
            [t[1] for t in p.index.tolist()],
            [50, 50, 50]
        )

    def test_error_01(self):
        """Prevision error."""
        prv = simulation.Prevision(
            **{'dte': '2012-10-10 10', 'res': 25.8, 'prb': 3}
        )
        simulation.Previsions(prv)
        simulation.Previsions(*[prv, prv, prv])
        self.assertRaises(
            TypeError,
            simulation.Previsions,
            44
        )


#-- class TestSimulation ------------------------------------------------------
class TestSimulation(unittest.TestCase):
    """Simulation class tests."""

    # def setUp(self):
    #     """Hook method for setting up the test fixture before exercising it."""
    #     pass

    # def tearDown(self):
    #     """Hook method for deconstructing the test fixture after testing it."""
    #     pass

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
        self.assertEqual(sim.previsions, None)

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
        previsions = simulation.Previsions(
            simulation.Prevision(
                **{'dte': '2012-10-10 10', 'res': 25.8, 'prb': 3}
            )
        )
        sim = simulation.Simulation(
            entite=entite,
            modeleprevision=modele,
            grandeur=grandeur,
            statut=statut,
            qualite=qualite,
            public=public,
            commentaire=commentaire,
            dtprod=dtprod,
            previsions=previsions
        )
        self.assertEqual(sim.entite, entite)
        self.assertEqual(sim.modeleprevision, modele)
        self.assertEqual(sim.grandeur, grandeur)
        self.assertEqual(sim.statut, statut)
        self.assertEqual(sim.qualite, qualite)
        self.assertEqual(sim.public, public)
        self.assertEqual(sim.commentaire, commentaire)
        self.assertEqual(sim.dtprod, dtprod)
        self.assertEqual(sim.previsions, previsions)

    def test_base_03(self):
        """Dtprod can be a string."""
        sim = simulation.Simulation(dtprod='2012-05-18T18:36Z')
        self.assertEqual(sim.dtprod, datetime.datetime(2012, 5, 18, 18, 36))
        sim = simulation.Simulation(dtprod='2012-05-18 18:36+02')
        self.assertEqual(sim.dtprod, datetime.datetime(2012, 5, 18, 16, 36))

    def test_str_01(self):
        """Test __str__ method with None values."""
        sim = simulation.Simulation()
        self.assertTrue(sim.__str__().rfind('Simulation') > -1)
        self.assertTrue(sim.__str__().rfind('Date de production') > -1)
        self.assertTrue(sim.__str__().rfind('Commentaire') > -1)
        self.assertTrue(sim.__str__().rfind('Previsions') > -1)

    def test_str_02(self):
        """Test __str__ method with basic values."""
        previsions = simulation.Previsions(
            simulation.Prevision(
                **{'dte': '2012-10-10 10', 'res': 25.8, 'prb': 3}
            )
        )
        sim = simulation.Simulation(
            dtprod='2012-05-18T18:36Z',
            entite=sitehydro.Stationhydro(
                code=0, libelle='Toulouse', strict=False
            ),
            previsions=previsions
        )
        self.assertTrue(sim.__str__().rfind('Simulation') > -1)
        self.assertTrue(sim.__str__().rfind('Date de production') > -1)
        self.assertTrue(sim.__str__().rfind('Commentaire') > -1)
        self.assertTrue(sim.__str__().rfind('Previsions') > -1)

    def test_str_03(self):
        """Test __str__ method with big Previsions."""
        previsions = simulation.Previsions(
            *[simulation.Prevision(dte='20%i-10-10 10' % x, res=x)
              for x in range(10, 50)]
        )
        sim = simulation.Simulation(
            dtprod='2012-05-18T18:36Z',
            entite=sitehydro.Stationhydro(code=0, strict=False),
            previsions=previsions
        )
        self.assertTrue(sim.__str__().rfind('Simulation') > -1)
        self.assertTrue(sim.__str__().rfind('Date de production') > -1)
        self.assertTrue(sim.__str__().rfind('Commentaire') > -1)
        self.assertTrue(sim.__str__().rfind('Previsions') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        entite = 'station'
        modeleprevision = 'modele'
        grandeur = 'RR'
        statut = 333333
        public = True
        commentaire = 'Nong'
        dtprod = datetime.datetime(2012, 5, 18, 18, 36)
        qualite = 100
        previsions = [10, 20, 30]
        sim = simulation.Simulation(
            entite=entite,
            modeleprevision=modeleprevision,
            grandeur=grandeur,
            statut=statut,
            qualite=qualite,
            public=public,
            commentaire=commentaire,
            dtprod=dtprod,
            previsions=previsions,
            strict=False
        )
        self.assertEqual(sim.entite, entite)
        self.assertEqual(sim.modeleprevision, modeleprevision)
        self.assertEqual(sim.grandeur, grandeur)
        self.assertEqual(sim.statut, statut)
        self.assertEqual(sim.qualite, qualite)
        self.assertEqual(sim.public, public)
        self.assertEqual(sim.commentaire, commentaire)
        self.assertEqual(sim.dtprod, dtprod)
        self.assertEqual(sim.previsions, previsions)

    def test_error_01(self):
        """Entite error."""
        entite = sitehydro.Stationhydro(code='A044010101')
        simulation.Simulation(**{'entite': entite})
        self.assertRaises(
            TypeError,
            simulation.Simulation,
            # **{'entite': entite}
            **{'entite': 25}
        )

    def test_error_02(self):
        """Modeleprevision error."""
        modele = modeleprevision.Modeleprevision()
        simulation.Simulation(**{'modeleprevision': modele})
        self.assertRaises(
            TypeError,
            simulation.Simulation,
            # **{'modeleprevision': modele}
            **{'modeleprevision': 'gloup !'}
        )

    def test_error_03(self):
        """Grandeur error."""
        simulation.Simulation(**{'grandeur': 'Q'})
        self.assertRaises(
            ValueError,
            simulation.Simulation,
            # **{'grandeur': 'H'}
            **{'grandeur': 'RR'}
        )

    def test_error_04(self):
        """Statut error."""
        simulation.Simulation(**{'statut': 16})
        self.assertRaises(
            ValueError,
            simulation.Simulation,
            # **{'statut': 16}
            **{'statut': 111111}
        )

    def test_error_05(self):
        """Qualite error."""
        simulation.Simulation(**{'qualite': 45})
        self.assertRaises(
            ValueError,
            simulation.Simulation,
            # **{'qualite': 45}
            **{'qualite': -1}
        )

    def test_error_06(self):
        """Dtprod error."""
        dtprod = datetime.datetime(2020, 1, 1, 10, 0)
        simulation.Simulation(**{'dtprod': dtprod})
        dtprod = '2020-01-01 10:00'
        simulation.Simulation(**{'dtprod': dtprod})
        self.assertRaises(
            TypeError,
            simulation.Simulation,
            # **{'dtprod': dtprod}
            **{'dtprod': '2020-10 10:00'}
        )

    def test_error_07(self):
        """Previsions error."""
        prvs = simulation.Previsions(
            simulation.Prevision(
                **{'dte': '2012-10-10 10', 'res': 25.8, 'prb': 3}
            )
        )
        simulation.Simulation(**{'previsions': prvs})
        self.assertRaises(
            TypeError,
            simulation.Simulation,
            # **{'previsions': prvs}
            **{'previsions': [110, 20, 30]}
        )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

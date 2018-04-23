# -*- coding: utf-8 -*-
"""Test program for obselaboreemeteo.

To run all tests just type:
    python -m unittest test_core_obselaboreemeteo

To run only a class test:
    python -m unittest test_core_obselaboreemeteo.TestClass

To run only a specific test:
    python -m unittest test_core_obselaboreemeteo.TestClass.test_method

"""

# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import unittest
import datetime as _datetime
import numpy as _numpy

from libhydro.core import (obselaboreemeteo as _obselaboreemeteo,
                           sitehydro as _sitehydro,
                           sitemeteo as _sitemeteo)

# -- strings ------------------------------------------------------------------
__author__ = """Sébastien ROMON""" \
             """<sebastien.romon@developpement-durable.gouv.fr>"""
__version__ = """0.1"""
__date__ = """2018-04-17"""


# -- class TestObsElab --------------------------------------------
class TestObsElabMeteo(unittest.TestCase):
    """"ObservationElaboree class tests."""

    def test_base_01(self):
        """Test full obs elab meteo"""
        dte = _datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        qua = 66.7
        statut = 8
        obs = _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                             res=res,
                                             mth=mth,
                                             qal=qal,
                                             qua=qua,
                                             statut=statut)
        self.assertEqual(obs.item(),
                         (dte, res, mth, qal, qua, statut))

    def test_base_02(self):
        """Test minimal obs elab meteo"""
        dte = _datetime.datetime(2018, 3, 15, 11, 23, 48)
        res = 265.43
        obs = _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                             res=res)
        self.assertEqual((obs['dte'], obs['res'], obs['mth'], obs['qal'],
                          obs['statut']),
                         (dte, res, 0, 16, 0))
        self.assertTrue(_numpy.isnan(obs['qua'].item()))

    def test_str_01(self):
        """Test representation"""
        dte = _datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        qua = 98
        statut = 8
        obs = _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                             res=res,
                                             mth=mth,
                                             qal=qal,
                                             qua=qua,
                                             statut=statut)
        self.assertEqual(obs.item(),
                         (dte, res, mth, qal, qua, statut))

    def test_dte(self):
        """Test property dte"""
        dte = '2015-07-15T11:45:56'
        res = 100.5
        qal = 20
        mth = 8
        qua = 98
        statut = 8
        for dte in ['2015-07-15T11:45:56',
                    _numpy.datetime64('2015-07-15T11:45:56'),
                    _datetime.datetime(2015, 7, 15, 11, 45, 56)]:
            obs = _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                                 res=res,
                                                 mth=mth,
                                                 qal=qal,
                                                 qua=qua,
                                                 statut=statut)
            self.assertEqual(obs['dte'].item(),
                             _datetime.datetime(2015, 7, 15, 11, 45, 56))
        dte = ' abc'
        with self.assertRaises(Exception) as cm:
            _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                           res=res,
                                           mth=mth,
                                           qal=qal,
                                           qua=qua,
                                           statut=statut)

    def test_res(self):
        """Test property res"""
        dte = _datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        qua = 98
        statut = 8
        _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                       res=res,
                                       mth=mth,
                                       qal=qal,
                                       qua=qua,
                                       statut=statut)
        for res in ['abc']:
            with self.assertRaises(Exception) as cm:
                _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                               res=res,
                                               mth=mth,
                                               qal=qal,
                                               qua=qua,
                                               statut=statut)

    def test_mth(self):
        """Test property mth"""
        dte = _datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        qua = 98
        statut = 8
        for mth in [0, 4, 8, 10, 14]:
            _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                           res=res,
                                           mth=mth,
                                           qal=qal,
                                           qua=qua,
                                           statut=statut)

        for mth in ['abc', -1, 6, 100]:
            with self.assertRaises(Exception) as cm:
                _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                               res=res,
                                               mth=mth,
                                               qal=qal,
                                               qua=qua,
                                               statut=statut)

    def test_statut(self):
        """Test property statut"""
        dte = _datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        qua = 98
        statut = 8
        for statut in [0, 4, 8, 12, 16]:
            _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                           res=res,
                                           mth=mth,
                                           qal=qal,
                                           qua=qua,
                                           statut=statut)

        for statut in ['abc', -1, 6, 100]:
            with self.assertRaises(Exception) as cm:
                _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                               res=res,
                                               mth=mth,
                                               qal=qal,
                                               qua=qua,
                                               statut=statut)

    def test_qal(self):
        """Test property qal"""
        dte = _datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        qua = 98
        statut = 8
        _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                       res=res,
                                       mth=mth,
                                       qal=qal,
                                       qua=qua,
                                       statut=statut)

        for qal in ['abc', -1, 100]:
            with self.assertRaises(Exception) as cm:
                _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                               res=res,
                                               mth=mth,
                                               qal=qal,
                                               qua=qua,
                                               statut=statut)

    def test_qua(self):
        """Test property qal"""
        dte = _datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        qua = 98
        statut = 8
        _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                       res=res,
                                       mth=mth,
                                       qal=qal,
                                       qua=qua,
                                       statut=statut)

        for qua in [_numpy.nan, 56.2, 97.4, 0, 100]:
            _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                           res=res,
                                           mth=mth,
                                           qal=qal,
                                           qua=qua,
                                           statut=statut)
        for qua in [-1.4, 101.3, 'abc']:
            with self.assertRaises(Exception) as cm:
                _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                               res=res,
                                               mth=mth,
                                               qal=qal,
                                               qua=qua,
                                               statut=statut)


# -- class TestObservationElaboree --------------------------------------------
class TestObssElabMeteo(unittest.TestCase):
    """ObssElabMeteo class tests."""

    def test_base_01(self):
        """Test witout observations"""
        obss = _obselaboreemeteo.ObssElabMeteo()
        self.assertEqual(len(obss), 0)

    def test_base_02(self):
        """Test with one observation"""
        dte = _datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        qua = 98
        statut = 8
        obs = _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                             res=res,
                                             mth=mth,
                                             qal=qal,
                                             qua=qua,
                                             statut=statut)

        obss = _obselaboreemeteo.ObssElabMeteo(obs)
        self.assertEqual(len(obss), 1)
        # self.assertEqual(obss.iloc[0], )

    def test_base_03(self):
        """Test with two observations"""
        dte = _datetime.datetime(2016, 2, 10, 9, 17, 43)
        res = 100.5
        qal = 20
        mth = 8
        qua = 98
        statut = 8
        obs1 = _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                              res=res,
                                              mth=mth,
                                              qal=qal,
                                              qua=qua,
                                              statut=statut)
        dte = _datetime.datetime(2016, 2, 10, 9, 18, 56)
        res = 138.4
        qal = 12
        mth = 0
        qua = 56
        statut = 12
        obs2 = _obselaboreemeteo.ObsElabMeteo(dte=dte,
                                              res=res,
                                              mth=mth,
                                              qal=qal,
                                              qua=qua,
                                              statut=statut)
        obss = _obselaboreemeteo.ObssElabMeteo(obs1, obs2)
        self.assertEqual(len(obss), 2)

    def test_concat(self):
        """Test static methoc concat"""
        dte1 = _datetime.datetime(2015, 3, 11, 23, 14, 54)
        obs1 = _obselaboreemeteo.ObsElabMeteo(dte=dte1,
                                              res=138.4)
        obss1 = _obselaboreemeteo.ObssElabMeteo(obs1)

        dte2 = _datetime.datetime(2015, 3, 11, 23, 14, 54)
        obs2 = _obselaboreemeteo.ObsElabMeteo(dte=dte2,
                                              res=168.1)
        obss2 = _obselaboreemeteo.ObssElabMeteo(obs2)

        obss = _obselaboreemeteo.ObssElabMeteo.concat(obss1, obss2)
        self.assertEqual(len(obss), 2)

    def test_concat_error(self):
        """Test concat error"""
        dte1 = _datetime.datetime(2015, 3, 11, 23, 14, 54)
        obs1 = _obselaboreemeteo.ObsElabMeteo(dte=dte1,
                                              res=138.4)
        obss1 = _obselaboreemeteo.ObssElabMeteo(obs1)

        dte2 = _datetime.datetime(2015, 3, 11, 23, 14, 54)
        obs2 = _obselaboreemeteo.ObsElabMeteo(dte=dte2,
                                              res=168.1)
        obss2 = _obselaboreemeteo.ObssElabMeteo(obs2)

        _obselaboreemeteo.ObssElabMeteo.concat(obss1, obss2)
        with self.assertRaises(Exception) as cm:
            _obselaboreemeteo.ObssElabMeteo.concat(obss1, 17.4)

    def test_error(self):
        """Test error"""
        dte1 = _datetime.datetime(2015, 3, 11, 23, 14, 54)
        obs1 = _obselaboreemeteo.ObsElabMeteo(dte=dte1,
                                              res=138.4)

        dte2 = _datetime.datetime(2015, 3, 11, 23, 14, 54)
        obs2 = _obselaboreemeteo.ObsElabMeteo(dte=dte2,
                                              res=168.1)
        obss = [obs1, obs2]
        _obselaboreemeteo.ObssElabMeteo(*obss)

        obss = [obs1, 14.2]
        with self.assertRaises(TypeError) as cm:
            _obselaboreemeteo.ObssElabMeteo(*obss)


# -- class TestIpa --------------------------------------------
class TestIpa(unittest.TestCase):
    """Ipa class tests."""
    def test_01(self):
        """Test minimal Ipa"""
        coefk = 0.34
        ipa = _obselaboreemeteo.Ipa(coefk=coefk)
        self.assertEqual((ipa.coefk, ipa.npdt),
                         (coefk, None))

    def test_02(self):
        """Test full Ipa"""
        coefk = 0.57
        npdt = 8
        ipa = _obselaboreemeteo.Ipa(coefk=coefk, npdt=npdt)
        self.assertEqual((ipa.coefk, ipa.npdt),
                         (coefk, npdt))

    def test_coefk(self):
        """Test coefk"""
        coefs = [0.12, 0.58]
        npdt = 4
        for coefk in coefs:
            ipa = _obselaboreemeteo.Ipa(coefk=coefk, npdt=npdt)
            self.assertEqual((ipa.coefk, ipa.npdt),
                             (coefk, npdt))
        coefs = [-0.2, 1.05, '1.6']
        for coefk in coefs:
            with self.assertRaises(ValueError) as cm:
                _obselaboreemeteo.Ipa(coefk=coefk, npdt=npdt)

        coefs = [None, 'toto']
        for coefk in coefs:
            with self.assertRaises(TypeError) as cm:
                _obselaboreemeteo.Ipa(coefk=coefk, npdt=npdt)

    def test_npdt(self):
        """Test coefk"""
        coefk = 0.5
        npdts = [0, 3, 8]
        for npdt in npdts:
            ipa = _obselaboreemeteo.Ipa(coefk=coefk, npdt=npdt)
            self.assertEqual((ipa.coefk, ipa.npdt),
                             (coefk, npdt))

        npdts = [-8, -1]
        for npdt in npdts:
            with self.assertRaises(ValueError) as cm:
                _obselaboreemeteo.Ipa(coefk=coefk, npdt=npdt)

        npdts = ['tata', 'toto']
        for npdt in npdts:
            with self.assertRaises(TypeError) as cm:
                _obselaboreemeteo.Ipa(coefk=coefk, npdt=npdt)

    def test_str_01(self):
        """Test representation simple ipa"""
        coefk = '0.5'
        ipa = _obselaboreemeteo.Ipa(coefk=coefk)
        self.assertTrue(ipa.__str__().find(coefk) != -1)
        self.assertTrue(ipa.__str__().find('inconnu') != -1)

    def test_str_02(self):
        """Test representation full ipa"""
        coefk = '0.8'
        npdt = '9'
        ipa = _obselaboreemeteo.Ipa(coefk=coefk, npdt=npdt)
        self.assertTrue(ipa.__unicode__().find(coefk) != -1)
        self.assertTrue(ipa.__unicode__().find(npdt) != -1)


# -- class TestObservationElaboree --------------------------------------------
class TestSerieObsElabMeteo(unittest.TestCase):
    """SerieObsElabMeteo class tests."""
    def test_01(self):
        """Test minimal serie obs elab meteo"""
        sitehydro = _sitehydro.Sitehydro(code='A1234567')
        grandeur = 'RR'
        typeserie = 1
        # dtprod = _datetime.datetime(2017, 11, 4, 7, 54, 34)

        serie = _obselaboreemeteo.SerieObsElabMeteo(site=sitehydro,
                                                    grandeur=grandeur,
                                                    typeserie=typeserie)
        self.assertEqual((serie.site, serie.grandeur, serie.typeserie),
                         (sitehydro, grandeur, typeserie))

    def test_02(self):
        """test full serie obs elab meteo"""
        sitemeteo = _sitemeteo.Sitemeteo(code='123456789')
        ponderation = 0.58
        sitepondere = _sitemeteo.SitemeteoPondere(sitemeteo=sitemeteo,
                                                         ponderation=ponderation)
        grandeur = 'RR'
        dtprod = _datetime.datetime(2016, 10, 8, 14, 23, 29)
        dtdeb = _datetime.datetime(2016, 3, 4, 11, 28, 50)
        dtfin = _datetime.datetime(2016, 4, 2, 14, 33, 42)
        typeserie = 2
        duree = 3600
        ipa = _obselaboreemeteo.Ipa(coefk=0.14, npdt=5)
        obss = [_obselaboreemeteo.ObsElabMeteo(
                    dte=_datetime.datetime(2015, 8, 1, 11, 0, 0), res=157.4),
                _obselaboreemeteo.ObsElabMeteo(
                    dte=_datetime.datetime(2015, 8, 1, 12, 0, 0), res=168.6)]
        observations = _obselaboreemeteo.ObssElabMeteo(*obss)
        serie = _obselaboreemeteo.SerieObsElabMeteo(site=sitepondere,
                                                    grandeur=grandeur,
                                                    typeserie=typeserie,
                                                    dtprod=dtprod,
                                                    dtdeb=dtdeb,
                                                    dtfin=dtfin,
                                                    duree=duree,
                                                    ipa=ipa,
                                                    observations=observations)

        self.assertEqual((serie.site, serie.grandeur, serie.typeserie,
                          serie.dtprod, serie.dtdeb, serie.dtfin, serie.ipa),
                         (sitepondere, grandeur, typeserie, dtprod, dtdeb,
                          dtfin, ipa))
        self.assertEqual(len(serie.observations), 2)
        self.assertEqual(serie.observations.iloc[0, 0], 157.4)
        self.assertEqual(serie.observations.loc['2015-08-01 12:00:00', 'res'],
                         168.6)

    def test_site(self):
        """Test property site"""
        code = '123456789'
        sitemeteo = _sitemeteo.Sitemeteo(code=code)
        ponderation = 0.58
        sites = [_sitehydro.Sitehydro(code='A1234567'),
                 _sitemeteo.SitemeteoPondere(sitemeteo=sitemeteo,
                                                    ponderation=ponderation)]
        grandeur = 'RR'
        typeserie = 1
        for site in sites:
            _obselaboreemeteo.SerieObsElabMeteo(site=site,
                                                grandeur=grandeur,
                                                typeserie=typeserie)
        for site in [None, sitemeteo, 'toto', code]:
            with self.assertRaises(TypeError) as cm:
                _obselaboreemeteo.SerieObsElabMeteo(site=site,
                                                    grandeur=grandeur,
                                                    typeserie=typeserie)

    def test_duree(self):
        """Test property duree"""
        site = _sitehydro.Sitehydro(code='A1234567')
        grandeur = 'RR'
        typeserie = 1
        durees = [None, 60, _datetime.timedelta(minutes=60)]
        # dtprod = _datetime.datetime(2017, 11, 4, 7, 54, 34)
        for duree in durees:
            _obselaboreemeteo.SerieObsElabMeteo(site=site,
                                                grandeur=grandeur,
                                                typeserie=typeserie,
                                                duree=duree)

        for duree in [-5, 'toto']:
            with self.assertRaises(Exception) as cm:
                _obselaboreemeteo.SerieObsElabMeteo(site=site,
                                                    grandeur=grandeur,
                                                    typeserie=typeserie,
                                                    duree=duree)

    def test_ipa(self):
        """Test property ipa"""
        code = '123456789'
        sitemeteo = _sitemeteo.Sitemeteo(code=code)
        ponderation = 0.58
        site = _sitemeteo.SitemeteoPondere(sitemeteo=sitemeteo,
                                                  ponderation=ponderation)
        grandeur = 'RR'
        typeserie = 2

        for ipa in [None, _obselaboreemeteo.Ipa(coefk=0.14, npdt=5)]:
            _obselaboreemeteo.SerieObsElabMeteo(site=site,
                                                grandeur=grandeur,
                                                typeserie=typeserie,
                                                ipa=ipa)
        for ipa in ['toto', 0.8]:
            with self.assertRaises(TypeError) as cm:
                _obselaboreemeteo.SerieObsElabMeteo(site=site,
                                                    grandeur=grandeur,
                                                    typeserie=typeserie,
                                                    ipa=ipa)

    def test_observations(self):
        """Test property observations"""
        site = _sitehydro.Sitehydro(code='A1234567')
        grandeur = 'RR'
        typeserie = 1
        obss = [_obselaboreemeteo.ObsElabMeteo(
                    dte=_datetime.datetime(2015, 8, 1, 11, 0, 0), res=157.4),
                _obselaboreemeteo.ObsElabMeteo(
                    dte=_datetime.datetime(2015, 8, 1, 12, 0, 0), res=168.6)]
        # observations = _obselaboreemeteo.ObssElabMeteo(*obss)
        for observations in [None, _obselaboreemeteo.ObssElabMeteo(*obss)]:
            _obselaboreemeteo.SerieObsElabMeteo(site=site,
                                                grandeur=grandeur,
                                                typeserie=typeserie,
                                                observations=observations)
        for observations in [obss, 115.2]:
            with self.assertRaises(TypeError) as cm:
                _obselaboreemeteo.SerieObsElabMeteo(site=site,
                                                    grandeur=grandeur,
                                                    typeserie=typeserie,
                                                    observations=observations)

    def test_strict(self):
        """Test strict=False"""
        cdsitemeteo = '123456789'
        grandeur = 'RR'
        dtprod = _datetime.datetime(2016, 10, 8, 14, 23, 29)
        dtdeb = _datetime.datetime(2016, 3, 4, 11, 28, 50)
        dtfin = _datetime.datetime(2016, 4, 2, 14, 33, 42)
        typeserie = 2
        duree = 3600
        ipa = 0.14
        observations = [154.6, 159.4]
        serie = _obselaboreemeteo.SerieObsElabMeteo(site=cdsitemeteo,
                                                    grandeur=grandeur,
                                                    typeserie=typeserie,
                                                    dtprod=dtprod,
                                                    dtdeb=dtdeb,
                                                    dtfin=dtfin,
                                                    duree=duree,
                                                    ipa=ipa,
                                                    observations=observations,
                                                    strict=False)

        self.assertEqual((serie.site, serie.grandeur, serie.typeserie,
                          serie.dtprod, serie.dtdeb, serie.dtfin, serie.ipa),
                         (cdsitemeteo, grandeur, typeserie, dtprod, dtdeb,
                          dtfin, ipa))
        self.assertEqual(serie.duree, _datetime.timedelta(minutes=60))

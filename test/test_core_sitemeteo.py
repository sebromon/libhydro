# coding: utf-8
"""Test program for sitemeteo.

To run all tests just type:
    python -m unittest test_core_sitemeteo

To run only a class test:
    python -m unittest test_core_sitemeteo.TestClass

To run only a specific test:
    python -m unittest test_core_sitemeteo.TestClass.test_method

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

from libhydro.core import (sitemeteo, intervenant as _intervenant,
                           rolecontact as _rolecontact)
from libhydro.core import _composant_site as composant_site


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1d"""
__date__ = """2014-08-01"""

# HISTORY
# V0.1 - 2014-07-11
#   first shot


# -- class TestSitemeteo ------------------------------------------------------
class TestSitemeteo(unittest.TestCase):

    """Sitemeteo class tests."""

    def test_base_01(self):
        """Empty site."""
        # init
        code = '021301001'
        m = sitemeteo.Sitemeteo(code=code)
        # test
        self.assertEqual(
            (
                m.code, m.libelle, m.libelleusuel,
                m.mnemo, m.lieudit, m.coord, m.altitude, m.fuseau, m.dtmaj,
                m.dtouverture, m.dtfermeture, m.droitpublication, m.essai,
                m.commentaire, m.images, m.reseaux, m.roles, m.zonehydro,
                m.commune, m.grandeurs, m.visites
            ),
            (code, None, None, None, None, None, None, None, None, None, None,
             None, None, None, [], [], [], None, None, [], [])
        )
        # same with 8 chars code
        shortcode = '21301001'
        m = sitemeteo.Sitemeteo(code=shortcode)
        self.assertEqual(m.code, code)

    def test_base_02(self):
        """Site with 1 grandeur."""
        # init
        code = '033345510'
        libelle = 'MONTÉLIMAR'
        libelleusuel = 'Montélimar SPC'
        mnemo = 'Mnémo'
        lieudit = 'lieu-dit'
        coord = (482000, 1897556.5, 26)
        altitude = composant_site.Altitude(altitude=131.6, sysalti=0)
        fuseau = 1
        dtmaj = _datetime.datetime(2015, 3, 17, 18, 14, 42)
        dtouverture = _datetime.datetime(2010, 11, 20, 9, 45, 6)
        dtfermeture = _datetime.datetime(2014, 2, 3, 12, 10, 20)
        droitpublication = False
        essai = True
        commentaire = 'Commentaire'

        images = [composant_site.Image(adresse='http://www.toto.fr'),
                  composant_site.Image(adresse='http://www.tata.fr',
                                       typeill=2)]
        
        reseaux = [composant_site.ReseauMesure(code='RESEAU',
                                               libelle='Libellé réseau')]
        roles = [_rolecontact.RoleContact(contact=_intervenant.Contact('134'),
                                          role='REF')]
        zonehydro = 'A123'
        commune = 32150
        grandeur = sitemeteo.Grandeur('RR')
        visites = [sitemeteo.Visite(
                    dtvisite=_datetime.datetime(2011, 5, 17, 9, 50, 15),
                    contact=_intervenant.Contact('987'),
                    methode='Méthode',
                    modeop='Mode opératoire'),
                   sitemeteo.Visite(
                    dtvisite=_datetime.datetime(2013, 8, 15, 14, 36, 23)),
                   ]

        m = sitemeteo.Sitemeteo(
            code=code, libelle=libelle, libelleusuel=libelleusuel, mnemo=mnemo,
            lieudit=lieudit, coord=coord, altitude=altitude, fuseau=fuseau,
            dtmaj=dtmaj, dtouverture=dtouverture, dtfermeture=dtfermeture,
            droitpublication=droitpublication, essai=essai,
            commentaire=commentaire, images=images, reseaux=reseaux, roles=roles,
            zonehydro=zonehydro, commune=commune, grandeurs=grandeur,
            visites=visites)

        # test
        self.assertEqual(
            (
                m.code, m.libelle, m.libelleusuel,
                m.mnemo, m.lieudit, m.coord, m.altitude, m.fuseau, m.dtmaj,
                m.dtouverture, m.dtfermeture, m.droitpublication, m.essai,
                m.commentaire, m.images, m.reseaux, m.roles, m.zonehydro, m.commune,
                m.grandeurs, m.visites
            ),
            (
                code, libelle, libelleusuel, mnemo, lieudit,
                composant_site.Coord(*coord), altitude, fuseau, dtmaj,
                dtouverture, dtfermeture, droitpublication, essai,
                commentaire, images, reseaux, roles, zonehydro,
                str(commune), [grandeur], visites
            )
        )
        grandeur.sitemeteo = m
        self.assertEqual(grandeur.sitemeteo, m)

    def test_base_03(self):
        """Sitemeteo with n grandeurs."""
        # init
        code = '033345502'
        libelle = 'MONTÉLIMAR'
        libelleusuel = 'Montélimar SPC'
        coord = (482000, 1897556.5, 26)
        commune = 32150
        grandeurs = (
            sitemeteo.Grandeur('RR'),
            sitemeteo.Grandeur('EP'),
            sitemeteo.Grandeur('DV'),
            sitemeteo.Grandeur('RR'),
        )
        m = sitemeteo.Sitemeteo(
            code=code, libelle=libelle, libelleusuel=libelleusuel,
            coord=coord, commune=commune, grandeurs=grandeurs
        )
        # test
        self.assertEqual(
            (
                m.code, m.libelle, m.libelleusuel,
                m.coord, m.commune, m.grandeurs
            ),
            (
                code, libelle, libelleusuel,
                composant_site.Coord(*coord), str(commune),
                list(grandeurs)
            )
        )

    def test_base_04(self):
        """Update some attributes."""
        # init
        code = '033345502'
        libelle = 'MONTÉLIMAR'
        libelleusuel = 'Montélimar SPC'
        coord = (482000, 1897556.5, 26)
        commune = 32150
        grandeurs = [
            sitemeteo.Grandeur('RR'),
            sitemeteo.Grandeur('EP'),
            sitemeteo.Grandeur('DV'),
            sitemeteo.Grandeur('RR'),
        ]
        m = sitemeteo.Sitemeteo(
            code=code, libelle=libelle, libelleusuel=libelleusuel,
            coord=coord, commune=commune, grandeurs=grandeurs
        )
        # test
        self.assertEqual(m.grandeurs, grandeurs)
        m.grandeurs = None
        self.assertEqual(m.grandeurs, [])
        m.grandeurs = grandeurs[0]
        self.assertEqual(m.grandeurs, [grandeurs[0]])
        m.grandeurs = grandeurs
        self.assertEqual(m.grandeurs, grandeurs)
        self.assertEqual(m.coord, composant_site.Coord(*coord))
        m.coord = (10, 20, 25)
        m.coord = composant_site.Coord(*coord)
        self.assertEqual(m.commune, str(commune))
        m.commune = 32150
        m.commune = None

    def test_str_01(self):
        """Test __str__ method with None values."""
        m = sitemeteo.Sitemeteo(code=0, strict=False)
        self.assertTrue(m.__str__().rfind('Sitemeteo') > -1)

    def test_str_02(self):
        """Test __str__ with unicode."""
        m = sitemeteo.Sitemeteo(code='044553301')
        m.libelle = 'ℓα gαяσηηє à тσυℓσυѕє'
        m.__unicode__()
        m.__str__()

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test with None values."""
        code = 1
        grandeurs = ['rouge', 'vert']
        m = sitemeteo.Sitemeteo(code=code,  grandeurs=grandeurs, strict=False)
        self.assertEqual(
            (m.code, m.grandeurs),
            (str(code), grandeurs)
        )

    def test_error_01(self):
        """Code error."""
        code = '044011221'
        sitemeteo.Sitemeteo(code=code)
        with self.assertRaises(TypeError):
            sitemeteo.Sitemeteo(code=None)
        with self.assertRaises(ValueError):
            sitemeteo.Sitemeteo(code='%s1' % code)
        with self.assertRaises(ValueError):
            sitemeteo.Sitemeteo(code=code[:-2])

    def test_error_02(self):
        """Coord error."""
        code = '044011221'
        coord = (33022, 5846, 26)
        sitemeteo.Sitemeteo(code=code, coord=coord)
        with self.assertRaises(TypeError):
            sitemeteo.Sitemeteo(code=code, coord=coord[0])

    def test_error_03(self):
        """Commune error."""
        code = '044011221'
        commune = '33022'
        sitemeteo.Sitemeteo(code=code, commune=commune)
        with self.assertRaises(ValueError):
            sitemeteo.Sitemeteo(code=code, commune=commune[:-1])
        with self.assertRaises(ValueError):
            sitemeteo.Sitemeteo(code=code, commune='%s1' % commune)

    def test_error_04(self):
        """Grandeurs error."""
        code = '023510101'
        grandeurs = (
            sitemeteo.Grandeur('RR'),
            sitemeteo.Grandeur('EP'),
        )
        sitemeteo.Sitemeteo(
            code=code,
            grandeurs=grandeurs
        )
        with self.assertRaises(TypeError):
            sitemeteo.Sitemeteo(code=code, grandeurs=['I am not a troncon'])

    def test_error_reseaux(self):
        """Reseaux error."""
        code = '023510101'
        reseau1 = composant_site.ReseauMesure(code='RESEAU',
                                              libelle='Libellé réseau')
        reseau2 = composant_site.ReseauMesure(code='RESEAU2',
                                              libelle='Libellé réseau2')
        for reseaux in [None, [], reseau1, [reseau1], [reseau1, reseau2]]:
            sitemeteo.Sitemeteo(code=code, reseaux=reseaux)

        for reseaux in ['RESEAU', ['RESEAU'], [reseau1, 'RESEAU']]:
            with self.assertRaises(TypeError):
                sitemeteo.Sitemeteo(code=code, reseaux=reseaux)

    def test_error_roles(self):
        """Roles error."""
        code = '023510101'
        role1 = _rolecontact.RoleContact(contact=_intervenant.Contact('134'),
                                         role='REF')
        role2 = _rolecontact.RoleContact(contact=_intervenant.Contact('999'),
                                         role='ADM')
        for roles in [None, [], role1, [role1], [role1, role2]]:
            sitemeteo.Sitemeteo(code=code, roles=roles)

        for roles in ['REF', ['REF'], [role1, 'REF']]:
            with self.assertRaises(TypeError):
                sitemeteo.Sitemeteo(code=code, roles=roles)

    def test_error_visites(self):
        """visites error."""
        code = '023510101'
        visite1 = sitemeteo.Visite(
                dtvisite=_datetime.datetime(2011, 5, 17, 9, 50, 15),
                contact=_intervenant.Contact('987'),
                methode='Méthode',
                modeop='Mode opératoire')
        visite2 = sitemeteo.Visite(
                dtvisite=_datetime.datetime(2013, 8, 15, 14, 36, 23))

        for visites in [None, [], visite1, [visite1], [visite1, visite2]]:
            sitemeteo.Sitemeteo(code=code, visites=visites)

        for visites in ['1990-01-01T00:00:00', ['2015-01-01T00:00:00'],
                        [visite1, _datetime.datetime(2016, 10, 15, 5, 6, 7)]]:
            with self.assertRaises(TypeError):
                sitemeteo.Sitemeteo(code=code, visites=visites)

    def test_altitude(self):
        """Altitude error."""
        code = '023510101'
        alt = composant_site.Altitude(altitude=131.6, sysalti=0)

        for altitude in [None, alt]:
            sitemeteo.Sitemeteo(code=code, altitude=altitude)

        for altitude in [151.8, '151.5']:
            with self.assertRaises(TypeError):
                sitemeteo.Sitemeteo(code=code, altitude=altitude)

    def test_zonehydro(self):
        """Zonehydro error."""
        code = '023510101'
        for zonehydro in [None, 'A123']:
            sitemeteo.Sitemeteo(code=code, zonehydro=zonehydro)
        for zonehydro in [151.8, 'A1234567']:
            with self.assertRaises(Exception):
                sitemeteo.Sitemeteo(code=code, zonehydro=zonehydro)

    def test_images(self):
        """images test"""
        code = '023510101'
        img1 = composant_site.Image(adresse='http://www.toto.fr')
        img2 = composant_site.Image(adresse='http://www.tata.fr',
                                    typeill=2)
        for images in [None, [], img1, [img2], [img1, img2]]:
            sitemeteo.Sitemeteo(code=code, images=images)
        for images in ['www.toto.fr', ['www.toto.fr'], [img1, 'toto']]:
            with self.assertRaises(Exception):
                sitemeteo.Sitemeteo(code=code, images=images)


# -- class TestGrandeur -------------------------------------------------------
class TestGrandeur(unittest.TestCase):

    """Grandeur class tests."""

    def test_base_01(self):
        """Simple Grandeur test"""
        typemesure = 'RR'
        grd = sitemeteo.Grandeur(typemesure=typemesure)
        self.assertEqual((grd.typemesure, grd.sitemeteo, grd.dtmiseservice,
                          grd.dtfermeture, grd.essai, grd.surveillance,
                          grd.delaiabsence, grd.pdt, grd.classesqualite,
                          grd.dtmaj),
                         (typemesure, None, None, None, None, None, None, None,
                          [], None))

    def test_base_02(self):
        """Full grandeur test"""
        codeinsee = '013008110'
        s = sitemeteo.Sitemeteo(codeinsee)
        typemesure = 'EP'
        dtmiseservice = _datetime.datetime(2012, 9, 4, 16, 14, 26)
        dtfermeture = _datetime.datetime(2016, 2, 10, 13, 27, 31)
        essai = False
        surveillance = True
        delaiabsence = 30
        pdt = 5

        classe = 3
        dtvisite = _datetime.datetime(2015, 10, 5, 14, 16, 51)
        dtdeb = _datetime.datetime(2015, 11, 3, 9, 10, 20)
        dtfin = _datetime.datetime(2017, 4, 17, 13, 47, 57)
        visite = sitemeteo.Visite(dtvisite=dtvisite)
        clq1 = sitemeteo.ClasseQualite(classe=classe, visite=visite,
                                       dtdeb=dtdeb, dtfin=dtfin)
        clq2 = sitemeteo.ClasseQualite(classe=4)
        classesqualite = [clq1, clq2]
        dtmaj = _datetime.datetime(2015, 6, 25, 7, 8, 11)
        grd = sitemeteo.Grandeur(
            typemesure=typemesure, sitemeteo=s, dtmiseservice=dtmiseservice,
            dtfermeture=dtfermeture, essai=essai, surveillance=surveillance,
            delaiabsence=delaiabsence, pdt=pdt, classesqualite=classesqualite,
            dtmaj=dtmaj)
        self.assertEqual((grd.typemesure, grd.sitemeteo, grd.dtmiseservice,
                          grd.dtfermeture, grd.essai, grd.surveillance,
                          grd.delaiabsence, grd.pdt, grd.classesqualite,
                          grd.dtmaj),
                         (typemesure, s, dtmiseservice, dtfermeture, essai,
                          surveillance, delaiabsence, pdt, classesqualite,
                          dtmaj))

    def test_pdt(self):
        """Test pdt"""
        typemesure = 'RR'
        for pdt in [None, 0, '1', 60]:
            sitemeteo.Grandeur(typemesure=typemesure, pdt=pdt)
        for pdt in [-1, 'toto']:
            with self.assertRaises(Exception):
                sitemeteo.Grandeur(typemesure=typemesure, pdt=pdt)

    def test_delaiabsence(self):
        """Test delaiabsence"""
        typemesure = 'RR'
        for delaiabsence in [None, 0, '1', 60]:
            sitemeteo.Grandeur(typemesure=typemesure,
                               delaiabsence=delaiabsence)
        for delaiabsence in [-1, 'toto']:
            with self.assertRaises(Exception):
                sitemeteo.Grandeur(typemesure=typemesure,
                                   delaiabsence=delaiabsence)

    def test_sitemeteo(self):
        """sitemeteo test"""
        typemesure = 'TA'
        codeinsee = '013008110'
        sim = sitemeteo.Sitemeteo(codeinsee)
        for site in [None, sim]:
            sitemeteo.Grandeur(typemesure=typemesure, sitemeteo=site)
        for site in [codeinsee, 'toto']:
            with self.assertRaises(Exception):
                sitemeteo.Grandeur(typemesure=typemesure, sitemeteo=site)

    def test_classesqualite(self):
        """classesqualite test"""

        classe = 3
        dtvisite = _datetime.datetime(2015, 10, 5, 14, 16, 51)
        dtdeb = _datetime.datetime(2015, 11, 3, 9, 10, 20)
        dtfin = _datetime.datetime(2017, 4, 17, 13, 47, 57)
        visite = sitemeteo.Visite(dtvisite=dtvisite)
        clq1 = sitemeteo.ClasseQualite(classe=classe, visite=visite,
                                       dtdeb=dtdeb, dtfin=dtfin)
        clq2 = sitemeteo.ClasseQualite(classe=4)
        typemesure = 'HN'
        for classesqualite in [None, [], clq1, [clq1, clq2]]:
            sitemeteo.Grandeur(typemesure=typemesure,
                               classesqualite=classesqualite)
        for classesqualite in ['toto', [clq1, 'toto']]:
            with self.assertRaises(Exception):
                sitemeteo.Grandeur(typemesure=typemesure,
                                   classesqualite=classesqualite)

    def test_str(self):
        """Test __str__ method with None values."""
        g = sitemeteo.Grandeur(typemesure='', strict=False)
        self.assertTrue(g.__str__().rfind('Grandeur') > -1)
        g = sitemeteo.Grandeur(typemesure=None, strict=False)
        self.assertTrue(g.__str__().rfind('Grandeur') > -1)

    def test_fuzzy_mode(self):
        """Fuzzy mode test."""
        typemesure = 'a fake one'
        site = 'anything can fit in fuzzy mode!'
        g = sitemeteo.Grandeur(
            typemesure=typemesure,
            sitemeteo=site,
            strict=False
        )
        self.assertEqual(g.typemesure, typemesure)
        self.assertEqual(g.sitemeteo, site)

    def test_error_01(self):
        """typemesure error."""
        g = sitemeteo.Grandeur(typemesure='RR')
        with self.assertRaises(ValueError):
            g.__setattr__('typemesure', None)
        with self.assertRaises(ValueError):
            g.__setattr__('typemesure', 'xxxx')

    def test_error_02(self):
        """Sitemeteo error."""
        s = sitemeteo.Sitemeteo('266012001')
        g = sitemeteo.Grandeur(
            typemesure='RR',
            sitemeteo=s
        )
        with self.assertRaises(TypeError):
            g.__setattr__('sitemeteo', 'junk site !')


# -- class TestSitemeteoPondere --------------------------------------------
class TestSitemeteoPondere(unittest.TestCase):
    """SitemeteoPondere class tests."""

    def test_01(self):
        """ Test simple SitemeteoPondere"""
        code = '987654321'
        ponderation = 0.54
        sitepondere = sitemeteo.SitemeteoPondere(
            code=code, ponderation=ponderation)
        self.assertEqual((sitepondere.code, sitepondere.ponderation),
                         (code, ponderation))

    def test_sitemeteo(self):
        """Test property sitemeteo"""
        code = '987654321'
        ponderation = 0.54
        sitemeteo.SitemeteoPondere(code=code,
                                   ponderation=ponderation)

        for code in [None, '1245']:
            with self.assertRaises(Exception):
                sitemeteo.SitemeteoPondere(
                    code=code, ponderation=ponderation)

    def test_ponderation(self):
        """Test property ponderation"""
        code = '987654321'
        ponderation = 0.54
        sitemeteo.SitemeteoPondere(code=code,
                                   ponderation=ponderation)

        for ponderation in ['toto', None]:
            with self.assertRaises(TypeError):
                sitemeteo.SitemeteoPondere(
                    code=code, ponderation=ponderation)

    def test_str(self):
        """Test representation"""
        code = '987654321'
        ponderation = '0.54'
        site_pond = sitemeteo.SitemeteoPondere(code=code,
                                               ponderation=ponderation)
        site_str = site_pond.__str__()
        self.assertTrue(site_str.find(code) != -1)
        self.assertTrue(site_str.find(ponderation) != -1)

# -- class TestVisite --------------------------------------------
class TestVisite(unittest.TestCase):
    """Visite class tests."""

    def test_01(self):
        """Simple visite test."""
        dtvisite = _datetime.datetime(2015, 9, 17, 10, 31, 28)
        visite = sitemeteo.Visite(dtvisite=dtvisite)
        self.assertEqual((visite.dtvisite, visite.contact, visite.methode,
                          visite.modeop),
                         (dtvisite, None, None, None))

    def test_02(self):
        """Full Visite test."""
        dtvisite = _datetime.datetime(2015, 9, 17, 10, 31, 28)
        contact = _intervenant.Contact('654')
        methode = 'Méthode'
        modeop = 'Mode opératoire'
        visite = sitemeteo.Visite(dtvisite=dtvisite, contact=contact,
                                  methode=methode, modeop=modeop)
        self.assertEqual((visite.dtvisite, visite.contact, visite.methode,
                          visite.modeop),
                         (dtvisite, contact, methode, modeop))

    def test_str_01(self):
        """representation of visite with dtvisite and contact"""
        dtvisite = _datetime.datetime(2015, 9, 17, 10, 31, 28)
        contact = _intervenant.Contact('654')
        visite = sitemeteo.Visite(dtvisite=dtvisite, contact=contact)
        strvisite = visite.__str__()
        self.assertTrue(strvisite.find(contact.code) > -1)
        self.assertTrue(
            strvisite.find(dtvisite.strftime('%Y-%m-%d %H:%M:%S')) > -1)

    def test_str_02(self):
        """representation of visite with dtvisite and contact"""
        dtvisite = _datetime.datetime(2015, 9, 17, 10, 31, 28)
        visite = sitemeteo.Visite(dtvisite=dtvisite)
        strvisite = visite.__str__()
        self.assertTrue(
            strvisite.find(dtvisite.strftime('%Y-%m-%d %H:%M:%S')) > -1)

    def test_contact(self):
        dtvisite = _datetime.datetime(2015, 9, 17, 10, 31, 28)
        for contact in (None, _intervenant.Contact('156')):
            sitemeteo.Visite(dtvisite=dtvisite, contact=contact)
        for contact in ['156', 847]:
            with self.assertRaises(Exception):
                sitemeteo.Visite(dtvisite=dtvisite, contact=contact)

# -- class TestVisite --------------------------------------------
class TestClasseQualite(unittest.TestCase):
    """ClasseQualite class tests."""

    def test_01(self):
        """Simple ClasseQualite test"""
        classe = 4
        clq = sitemeteo.ClasseQualite(classe=classe)
        self.assertEqual((clq.classe, clq.visite, clq.dtdeb, clq.dtfin),
                         (classe, None, None, None))

    def test_02(self):
        """Full ClasseQualite test"""
        classe = 1
        dtvisite = _datetime.datetime(2015, 10, 5, 14, 16, 51)
        dtdeb = _datetime.datetime(2015, 11, 3, 9, 10, 20)
        dtfin = _datetime.datetime(2017, 4, 17, 13, 47, 57)
        visite = sitemeteo.Visite(dtvisite=dtvisite)
        clq = sitemeteo.ClasseQualite(classe=classe, visite=visite,
                                      dtdeb=dtdeb, dtfin=dtfin)
        self.assertEqual((clq.classe, clq.visite.dtvisite, clq.dtdeb,
                          clq.dtfin),
                         (classe, dtvisite, dtdeb, dtfin))

    def test_classe(self):
        for classe in [1, '3', 5]:
            sitemeteo.ClasseQualite(classe=classe)
        for classe in [0, 'toto', 6]:
            with self.assertRaises(Exception):
                sitemeteo.ClasseQualite(classe=classe)

    def test_visite(self):
        classe = 1
        dtvisite = _datetime.datetime(2013, 6, 3, 15, 44, 31)
        for visite in [None, sitemeteo.Visite(dtvisite=dtvisite)]:
            sitemeteo.ClasseQualite(classe=classe, visite=visite)
        for visite in [dtvisite, 'toto', 6]:
            with self.assertRaises(Exception):
                sitemeteo.ClasseQualite(classe=classe, visite=visite)

    def test_str01(self):
        classe = '2'
        clq = sitemeteo.ClasseQualite(classe=classe)
        strclq = clq.__unicode__()
        self.assertTrue(strclq.find(classe) > -1)

    def test_str02(self):
        classe = '2'
        dtvisite = _datetime.datetime(2015, 10, 5, 14, 16, 51)
        dtdeb = _datetime.datetime(2015, 11, 3, 9, 10, 20)
        dtfin = _datetime.datetime(2017, 4, 17, 13, 47, 57)
        visite = sitemeteo.Visite(dtvisite=dtvisite)
        clq = sitemeteo.ClasseQualite(classe=classe, visite=visite,
                                      dtdeb=dtdeb, dtfin=dtfin)

        strclq = clq.__str__()
        self.assertTrue(strclq.find(classe) > -1)
        self.assertTrue(strclq.find('2015-10-05 14:16:51') > -1)
        self.assertTrue(strclq.find('2015-11-03 09:10:20') > -1)
        self.assertTrue(strclq.find('2017-04-17 13:47:57') > -1)

# coding: utf-8
"""Test program for sitehydro.

To run all tests just type:
    python -m unittest test_core_sitehydro

To run only a class test:
    python -m unittest test_core_sitehydro.TestClass

To run only a specific test:
    python -m unittest test_core_sitehydro.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime
import unittest

from libhydro.core import sitehydro, sitemeteo as _sitemeteo
from libhydro.core import (_composant_site as composant_site,
                           rolecontact as _rolecontact,
                           intervenant as _intervenant)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.3.2"""
__date__ = """2017-09-22"""
# contributor Sébastien ROMON

# HISTORY
# V0.3.2 - SR - 2017-07-18
# Tests entitehydro, tronconhydro, zonehydro precisioncoursdeaun of class Site
# V0.3.1 - SR - 2017-07-18
# Tests on plages of classes Station and Capteur
# V0.3 - SR - 2017-07-18
# Tests on properies of class Station
# V0.2 - 2014-12-17
#  replace Stationhydro with Station
# V0.1 - 2013-07-15
#   first shot


# -- class TestSitehydro ------------------------------------------------------
class TestSitehydro(unittest.TestCase):

    """Sitehydro class tests."""

    def test_base_01(self):
        """Empty site."""
        code = 'R5330101'
        s = sitehydro.Sitehydro(code=code)
        self.assertEqual(
            (
                s.code, s.codeh2, s.typesite, s.libelle, s.libelleusuel,
                s.stations, s.communes, s.entitehydro,
                s.zonehydro, s.tronconhydro, s.precisioncoursdeau,
                s.pkamont, s.pkaval, s.dtmaj, s.bvtopo,
                s.bvhydro, s.altitude, s.fuseau, s.statut, s.dtpremieredonnee,
                s.moisetiage, s.moisanneehydro, s.dureecrues, s.publication,
                s.essai, s.influence, s.influencecommentaire, s.commentaire,
                s.siteassocie, s.sitesattaches, s.loisstat, s.images, s.roles,
                s.entitesvigicrues, s.lamesdeau, s.sitesamont, s.sitesaval
            ),
            (code, None, 'REEL', None, None,
             [], [], None,
             None, None,  None,
             None, None, None, None,
             None, None, None, None, None,
             None, None, None, None,
             None, None, None, None,
             None, [], [], [], [], [],
             [], [], [])
        )

    def test_base_02(self):
        """Site with 1 station."""
        code = 'A3334550'
        codeh2 = 'A3334550'
        typesite = 'MAREGRAPHE'
        libelle = 'La Saône [apres la crue] a Montélimar'
        libelleusuel = 'Montélimar'
        coord = (482000, 1897556.5, 26)
        station = sitehydro.Station(
            code='%s01' % code, typestation='LIMNI'
        )
        commune = composant_site.Commune(code=32150)
        entitehydro = 'O---0000'
        tronconhydro = 'O0240430'
        zonehydro = 'O987'
        precisioncoursdeau = 'totale'
        pkamont = 31.5
        pkaval = 54.2
        dtmaj = _datetime.datetime(2017, 3, 9, 14, 16, 24)
        bvtopo = 1516.3
        bvhydro = 1432.7
        altitude = composant_site.Altitude(altitude=98.2, sysalti=2)
        fuseau = 9
        statut = 3
        dtpremieredonnee = _datetime.datetime(2010, 4, 13)
        moisetiage = 5
        moisanneehydro = 7
        dureecrues = 15
        publication = 30
        essai = True
        influence = 4
        influencecommentaire = 'Commentaire sur l\'influence'
        commentaire = 'Commentaire du site'
        siteassocie = sitehydro.Sitehydro(code='A7654321')

        siteattache1 = sitehydro.Sitehydroattache(
            code='C1212121', ponderation=0.4,
            decalage=15)
        siteattache2 = sitehydro.Sitehydroattache(
            code='C1212121', ponderation=0.6,
            decalage=28)
        sitesattaches = [siteattache1, siteattache2]

        loi1 = composant_site.LoiStat(contexte=1, loi=2)
        loi2 = composant_site.LoiStat(contexte=2, loi=1)
        loisstat = [loi1, loi2]

        images = [composant_site.Image(adresse='http://www.toto.fr'),
                  composant_site.Image(adresse='http://www.tata.fr',
                                       typeill=2)]

        role1 = _rolecontact.RoleContact(contact=_intervenant.Contact('1234'),
                                         role='PRV')
        role2 = _rolecontact.RoleContact(
            contact=_intervenant.Contact('4321'),
            role='EXP',
            dtdeb=_datetime.datetime(2010, 4, 17, 11, 12, 13),
            dtfin=_datetime.datetime(2038, 10, 4, 17, 18, 19),
            dtmaj=_datetime.datetime(2018, 9, 3, 15, 54, 35))
        roles = [role1, role2]

        entitevigicrues1 = composant_site.EntiteVigiCrues(code='LA1',
                                                          libelle='entité')
        entitevigicrues2 = composant_site.EntiteVigiCrues(code='Z98')
        entitesvigicrues = [entitevigicrues1, entitevigicrues2]

        lamedeau1 = _sitemeteo.SitemeteoPondere(
            code='01234567',
            ponderation=0.6
            )
        lamedeau2 = _sitemeteo.SitemeteoPondere(
            code='12345678',
            ponderation=0.4
            )
        lamesdeau = [lamedeau1, lamedeau2]

        siteamont1 = sitehydro.Sitehydro(code='C9412683')
        siteamont2 = sitehydro.Sitehydro(code='K1123321')
        sitesamont = [siteamont1, siteamont2]

        siteaval1 = sitehydro.Sitehydro(code='J8754921')
        siteaval2 = sitehydro.Sitehydro(code='K2659170')
        sitesaval = [siteaval1, siteaval2]

        s = sitehydro.Sitehydro(
            code=code, codeh2=codeh2, typesite=typesite,
            libelle=libelle, libelleusuel=libelleusuel,
            coord=coord, stations=station, communes=commune,
            entitehydro=entitehydro,
            tronconhydro=tronconhydro,
            zonehydro=zonehydro,
            precisioncoursdeau=precisioncoursdeau,
            pkamont=pkamont,
            pkaval=pkaval,
            altitude=altitude,
            dtmaj=dtmaj,
            bvtopo=bvtopo,
            bvhydro=bvhydro,
            fuseau=fuseau,
            statut=statut,
            dtpremieredonnee=dtpremieredonnee,
            moisetiage=moisetiage,
            moisanneehydro=moisanneehydro,
            dureecrues=dureecrues,
            publication=publication,
            essai=essai,
            influence=influence,
            influencecommentaire=influencecommentaire,
            commentaire=commentaire,
            siteassocie=siteassocie,
            sitesattaches=sitesattaches,
            loisstat=loisstat, images=images,
            roles=roles,
            entitesvigicrues=entitesvigicrues,
            lamesdeau=lamesdeau,
            sitesamont=sitesamont,
            sitesaval=sitesaval
        )

        self.assertEqual(
            (
                s.code, s.codeh2, s.typesite, s.libelle, s.libelleusuel,
                s.coord, s.stations, s.communes,
                s.entitehydro, s.zonehydro, s.tronconhydro,
                s.precisioncoursdeau, s.pkamont, s.pkaval, s.dtmaj, s.bvtopo,
                s.bvhydro, s.altitude, s.fuseau, s.statut, s.dtpremieredonnee,
                s.moisetiage, s.moisanneehydro, s.dureecrues, s.publication,
                s.essai, s.influence, s.influencecommentaire, s.commentaire,
                s.siteassocie, s.sitesattaches, s.loisstat, s.images, s.roles,
                s.entitesvigicrues, s.lamesdeau, s.sitesamont, s.sitesaval
            ),
            (
                code, codeh2, typesite, libelle, libelleusuel,
                composant_site.Coord(*coord), [station], [commune],
                entitehydro, zonehydro, tronconhydro,
                precisioncoursdeau, pkamont, pkaval, dtmaj, bvtopo,
                bvhydro, altitude, fuseau, statut, dtpremieredonnee,
                moisetiage, moisanneehydro, dureecrues, publication,
                essai, influence, influencecommentaire, commentaire,
                siteassocie, sitesattaches, loisstat, images, roles,
                entitesvigicrues, lamesdeau, sitesamont, sitesaval
            )
        )

    def test_base_03(self):
        """Site with n station."""
        code = 'A3334550'
        typesite = 'REEL'
        libelle = 'La Saône [apres la crue] a Montelimar [hé oui]'
        coord = {'x': 482000, 'y': 1897556.5, 'proj': 26}
        stations = (
            sitehydro.Station(
                code='%s01' % code, typestation='DEB'
            ),
            sitehydro.Station(
                code='%s02' % code, typestation='LIMNIMERE'
            ),
            sitehydro.Station(
                code='%s03' % code, typestation='LIMNIFILLE'
            )
        )
        communes = [composant_site.Commune(32150),
                    composant_site.Commune(31100)]
        entitesvigicrues = (
            composant_site.EntiteVigiCrues(
                code='AC1', libelle='La Liane 1'
            ),
            composant_site.EntiteVigiCrues(
                code='AC2', libelle='La Liane 2'
            ),
            composant_site.EntiteVigiCrues(
                code='AC3', libelle='La Liane 3'
            )
        )
        s = sitehydro.Sitehydro(
            code=code, typesite=typesite, libelle=libelle,
            coord=coord, stations=stations, communes=communes,
            entitesvigicrues=entitesvigicrues
        )
        self.assertEqual(
            (
                s.code, s.typesite, s.libelle, s.coord,
                s.stations, s.communes, s.entitesvigicrues
            ),
            (
                code, typesite, libelle, composant_site.Coord(**coord),
                [st for st in stations],
                communes,
                [entitevigicrues for entitevigicrues in entitesvigicrues]
            )
        )

    def test_equality(self):
        """Equality test."""
        # strict mode
        code = 'O0334011'
        site = sitehydro.Sitehydro(code=code)
        other = sitehydro.Sitehydro(code=code)
        self.assertEqual(site, other)
        other.libelle = 'A label here...'
        self.assertNotEqual(site, other)
        # lazzy mode: None attributes are ignored
        self.assertTrue(site.__eq__(other, lazzy=True))
        # ignore some attrs
        other.libelle = None
        self.assertEqual(site, other)
        other.stations = sitehydro.Station('A456102001')
        self.assertNotEqual(site, other)
        self.assertTrue(site.__eq__(other, ignore=['stations']))

    def test_base_04(self):
        """Update some attributes."""
        code = 'A3334550'
        typesite = 'REEL'
        libelle = 'La Saône [apres la crue] a Montelimar [hé oui]'
        coord = composant_site.Coord(
            x=482000, y=1897556.5, proj=26
        )
        stations = [
            sitehydro.Station(code='%s01' % code, typestation='DEB')
        ]
        s = sitehydro.Sitehydro(
            code=code, typesite=typesite, libelle=libelle,
            coord=coord, stations=stations
        )
        self.assertEqual(s.stations, stations)
        s.stations = None
        self.assertEqual(s.stations, [])
        s.stations = stations[0]
        self.assertEqual(s.stations, stations)
        s.stations = stations
        self.assertEqual(s.stations, stations)
        self.assertEqual(s.coord, coord)
        self.assertEqual(s.communes, [])
        s.communes = composant_site.Commune(32150)
        s.communes = composant_site.Commune('2B810')
        s.communes = [composant_site.Commune('2A001'),
                      composant_site.Commune(33810),
                      composant_site.Commune(44056),
                      composant_site.Commune('2B033')]
        s.communes = None
        self.assertEqual(s.entitesvigicrues, [])
        entite = composant_site.EntiteVigiCrues(
            code='XX33',
            libelle='Le Târtémpion'
        )
        s.entitesvigicrues = entite
        self.assertEqual(s.entitesvigicrues, [entite])
        s.entitesvigicrues = (entite, entite, entite)
        self.assertEqual(s.entitesvigicrues, [entite, entite, entite])

    def test_str_01(self):
        """Test __str__ method with None values."""
        s = sitehydro.Sitehydro(code=0, strict=False)
        self.assertTrue(s.__str__().rfind('Site') > -1)

    def test_str_02(self):
        """Test __str__ with unicode."""
        s = sitehydro.Sitehydro(code='A0445533')
        s.libelle = 'ℓα gαяσηηє à тσυℓσυѕє'
        s.__unicode__()
        s.__str__()

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test with None values."""
        code = stations = None
        trv = ['tr1']
        s = sitehydro.Sitehydro(
            code=code,  stations=stations, entitesvigicrues=trv,
            strict=False
        )
        self.assertEqual(
            (s.typesite, s.code, s.stations, s.entitesvigicrues),
            ('REEL', code, [], trv)
        )

    def test_fuzzy_mode_02(self):
        """Fuzzy mode test."""
        code = '3'
        typesite = '6'
        stations = [1, 2, 3]
        s = sitehydro.Sitehydro(
            typesite=typesite, code=code,  stations=stations, strict=False
        )
        self.assertEqual(
            (s.typesite, s.code, s.stations),
            (typesite, code, stations)
        )

    def test_error_01(self):
        """Typesite error."""
        code = 'H0001010'
        s = sitehydro.Sitehydro(code=code, typesite='REEL')
        with self.assertRaises(ValueError):
            s.__setattr__('typesite', None)
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(code=code, typesite='REEEL')

    def test_error_02(self):
        """Code error."""
        code = 'B4401122'
        sitehydro.Sitehydro(code=code)
        with self.assertRaises(TypeError):
            sitehydro.Sitehydro(code=None)
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(code='%s01' % code)
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(code=code[:-1])

    def test_error_03(self):
        """Code hydro2 error."""
        code = 'B4401122'
        sitehydro.Sitehydro(code=code, codeh2=code)
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(code=code, codeh2='{}01'.format(code))

    def test_error_04(self):
        """Station error."""
        code = 'B4401122'
        stations = (
            sitehydro.Station(code='%s01' % code),
            sitehydro.Station(code='%s02' % code)
        )
        sitehydro.Sitehydro(code=code, stations=stations)
        with self.assertRaises(TypeError):
            sitehydro.Sitehydro(code=code, stations=['station'])
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(
                code=code, typesite='PONCTUEL', stations=stations
            )
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(
                code=code, typesite='FICTIF', stations=stations
            )
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(
                code=code, typesite='VIRTUEL', stations=stations
            )

    def test_error_05(self):
        """Coord error."""
        code = 'B4401122'
        coord = (33022, 5846, 26)
        sitehydro.Sitehydro(code=code, coord=coord)
        with self.assertRaises(TypeError):
            sitehydro.Sitehydro(code=code, coord=coord[0])

    def test_error_06(self):
        """Entitesvigicrues error."""
        code = 'A2351010'
        sitehydro.Sitehydro(
            code=code,
            entitesvigicrues=composant_site.EntiteVigiCrues()
        )
        with self.assertRaises(TypeError):
            sitehydro.Sitehydro(
                code=code, entitesvigicrues='I am not a troncon'
            )

    def test_error_07(self):
        """Zonehydro error."""
        code = 'A2351010'
        zonehydro = 'A012'
        sitehydro.Sitehydro(
            code=code,
            zonehydro=zonehydro)
        zonehydro = 'A0123'
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(
                code=code, zonehydro=zonehydro
            )

    def test_error_08(self):
        """Tronconhydro error."""
        code = 'A2351010'
        tronconhydro = 'A1234567'
        sitehydro.Sitehydro(
            code=code,
            tronconhydro=tronconhydro)
        tronconhydro = 'A0123'
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(
                code=code, tronconhydro=tronconhydro
            )

    def test_error_09(self):
        """Entitehydro error."""
        code = 'A2351010'
        entitehydro = 'A1234567'
        sitehydro.Sitehydro(
            code=code,
            entitehydro=entitehydro)
        entitehydro = 'A0123456789'
        with self.assertRaises(ValueError):
            sitehydro.Sitehydro(
                code=code, entitehydro=entitehydro
            )

    def test_error_10(self):
        """pkamont pkaval error"""
        code = 'A2351010'
        for pk in ['1.8', 165.4, None]:
            sitehydro.Sitehydro(
                code=code,
                pkamont=pk)
            sitehydro.Sitehydro(
                code=code,
                pkaval=pk)
        pk = 'toto'
        with self.assertRaises(Exception):
            sitehydro.Sitehydro(
                code=code, pkamont=pk
            )
        with self.assertRaises(Exception):
            sitehydro.Sitehydro(
                code=code, pkaval=pk
            )

    def test_error_11_altitude(self):
        """altitude error"""
        code = 'A2351010'
        altitude = composant_site.Altitude(altitude=98.2, sysalti=2)
        sitehydro.Sitehydro(
            code=code, altitude=altitude
        )
        for altitude in [189.4, 'toto']:
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(
                    code=code, altitude=altitude
                )

    def test_error_12_bv(self):
        """bvhydro et bvtopo error"""
        code = 'A2351010'
        for bv in [1578989.4, None]:
            sitehydro.Sitehydro(
                code=code, bvhydro=bv
            )
            sitehydro.Sitehydro(
                code=code, bvtopo=bv
            )
        bv = 'tata'
        with self.assertRaises(Exception):
            sitehydro.Sitehydro(
                code=code, bvhydro=bv
            )
        with self.assertRaises(Exception):
            sitehydro.Sitehydro(
                code=code, bvtopo=bv
            )

    def test_error_13_fuseau(self):
        """fuseau error"""
        code = 'A2351010'
        for fuseau in [1, '5', None]:
            sitehydro.Sitehydro(
                code=code, fuseau=fuseau
            )
        for fuseau in ['toto']:
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(code=code, fuseau=fuseau)

    def test_error_xx_siteassocie(self):
        siteassocie = sitehydro.Sitehydro(code='K5463981')
        sitehydro.Sitehydro(code='L4545456',
                            siteassocie=siteassocie)
        siteassocie = 'A12234567'
        with self.assertRaises(Exception):
            sitehydro.Sitehydro(code='L4545456', siteassocie=siteassocie)

    def test_error_xx_sitesattaches(self):
        siteattache1 = sitehydro.Sitehydroattache(code='K5463981')
        siteattache2 = sitehydro.Sitehydroattache(code='L1239546')
        for sites in [[siteattache1, siteattache2], [], None, siteattache1]:
            sitehydro.Sitehydro(code='L4545456',
                                sitesattaches=sites)
        for sites in ['toto', ['toto'], [siteattache1, 'tata']]:
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(code='L4545456', sitesattaches=sites)

    def test_error_xx_loisstat(self):
        loi1 = composant_site.LoiStat(contexte=1, loi=2)
        loi2 = composant_site.LoiStat(contexte=2, loi=1)
        for lois in [[loi1, loi2], [], None, loi1]:
            sitehydro.Sitehydro(code='L4545456',
                                loisstat=lois)
        for lois in [1, 'toto', ['toto'], [loi1, 1]]:
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(code='L4545456', loisstat=lois)

    def test_images(self):
        """images test"""
        code = 'A1234567'
        img1 = composant_site.Image(adresse='http://www.toto.fr')
        img2 = composant_site.Image(adresse='http://www.tata.fr',
                                    typeill=2)
        for images in [None, [], img1, [img2], [img1, img2]]:
            sitehydro.Sitehydro(code=code, images=images)
        for images in ['www.toto.fr', ['www.toto.fr'], [img1, 'toto']]:
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(code=code, images=images)

    def test_error_xx_roles(self):
        role1 = _rolecontact.RoleContact(contact=_intervenant.Contact('1234'),
                                         role='PRV')
        role2 = _rolecontact.RoleContact(
            contact=_intervenant.Contact('4321'),
            role='EXP',
            dtdeb=_datetime.datetime(2010, 4, 17, 11, 12, 13),
            dtfin=_datetime.datetime(2038, 10, 4, 17, 18, 19),
            dtmaj=_datetime.datetime(2018, 9, 3, 15, 54, 35))
        for roles in [[role1, role2], [], None, role1]:
            sitehydro.Sitehydro(code='L4545456',
                                roles=roles)
        for roles in [1, 'toto', ['toto'], [roles, '1']]:
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(code='L4545456', roles=roles)

    def test_error_xx_entitesvigicrues(self):
        entitevigicrues1 = composant_site.EntiteVigiCrues(code='LA1',
                                                          libelle='entité')
        entitevigicrues2 = composant_site.EntiteVigiCrues(code='Z98')
        for entites in [None, [], entitevigicrues1,
                        [entitevigicrues1, entitevigicrues2]]:
            sitehydro.Sitehydro(code='L4545456', entitesvigicrues=entites)
        for entites in ['LA1', [entitevigicrues1, 'LA1']]:
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(code='L4545456', entitesvigicrues=entites)

    def test_error_xx_lamesdeau(self):
        lamedeau1 = _sitemeteo.SitemeteoPondere(
            code='01234567',
            ponderation=0.6
            )
        lamedeau2 = _sitemeteo.SitemeteoPondere(
            code='12345678',
            ponderation=0.4
            )
        for lames in [None, [], lamedeau1, [lamedeau1, lamedeau2]]:
            sitehydro.Sitehydro(code='L4545456', lamesdeau=lames)
        for lames in ['01234567', [lamedeau1, '01234567']]:
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(code='L4545456', lamesdeau=lames)

    def test_error_xx__sitesmontaval(self):
        site1 = sitehydro.Sitehydro(code='Z4564564')
        site2 = sitehydro.Sitehydro(code='Z4564564')
        for sites in [None, [], site1, [site1, site2]]:
            sitehydro.Sitehydro(code='L4545456', sitesamont=sites)
            sitehydro.Sitehydro(code='L4545456', sitesaval=sites)
        for sites in ['Z4564564', [site1, 'Z4564564']]:
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(code='L4545456', sitesamont=sites)
            with self.assertRaises(Exception):
                sitehydro.Sitehydro(code='L4545456', sitesaval=sites)

    def test_inheritance(self):
        """Test inheritance."""
        class Sitehydro(sitehydro.Sitehydro):
            def __init__(self, code, prop, *args, **kwargs):
                super(Sitehydro, self).__init__(code, *args, **kwargs)
                self.prop = prop

        code = 'A3331020'
        prop = 10
        commune = composant_site.Commune('32001')
        x = Sitehydro(code=code, prop=prop, communes=commune)
        self.assertEqual(x.code, code)
        self.assertEqual(x.prop, prop)
        self.assertEqual(x.communes, [commune])


# -- class TestSitehydroattache -----------------------------------------------
class TestSitehydroattache(unittest.TestCase):
    def test_01(self):
        code = 'A1234567'
        site = sitehydro.Sitehydroattache(code=code)
        self.assertEqual((site.code, site.ponderation, site.decalage,
                          site.dtdeb, site.dtfin, site.dtdebactivation,
                          site.dtfinactivation),
                         (code, None, None, None, None, None, None))

    def test_02(self):
        code = 'Z7654321'
        ponderation = 0.7
        decalage = 30
        dtdeb = _datetime.datetime(2013, 4, 9, 10, 54, 31)
        dtfin = _datetime.datetime(2015, 8, 17, 21, 17, 5)
        dtdebactivation = _datetime.datetime(2014, 3, 25, 12, 20, 43)
        dtfinactivation = _datetime.datetime(2014, 3, 25, 12, 20, 43)
        site = sitehydro.Sitehydroattache(code=code,
                                          ponderation=ponderation,
                                          decalage=decalage, dtdeb=dtdeb,
                                          dtfin=dtfin,
                                          dtdebactivation=dtdebactivation,
                                          dtfinactivation=dtfinactivation)
        self.assertEqual((code, site.ponderation, site.decalage,
                          site.dtdeb, site.dtfin, site.dtdebactivation,
                          site.dtfinactivation),
                         (code, ponderation, decalage, dtdeb, dtfin,
                          dtdebactivation, dtfinactivation))

    def test_str(self):
        code = 'Z7654321'
        ponderation = '0.7'
        decalage = '38'
        site = sitehydro.Sitehydroattache(code=code,
                                          ponderation=ponderation,
                                          decalage=decalage)
        self.assertTrue(site.__unicode__().find(code) > -1)
        self.assertTrue(site.__unicode__().find(ponderation) > -1)
        self.assertTrue(site.__unicode__().find(decalage) > -1)

    def test_error_code(self):
        code = 'A1234567'
        sitehydro.Sitehydroattache(code=code)
        code = None
        with self.assertRaises(TypeError):
            sitehydro.Sitehydroattache(code=code)

        code = 'A123456789'
        with self.assertRaises(ValueError):
            sitehydro.Sitehydroattache(code=code)

    def test_error_ponderation(self):
        code = 'A1234567'
        ponderation = 0.4
        sitehydro.Sitehydroattache(code=code, ponderation=ponderation)

        ponderation = 'toto'
        with self.assertRaises(Exception):
            sitehydro.Sitehydroattache(code=code, ponderation=ponderation)

    def test_error_decalage(self):
        code = 'A1234567'
        ponderation = 0.4
        decalage = 30
        sitehydro.Sitehydroattache(code=code, ponderation=ponderation,
                                   decalage=decalage)

        decalage = 'toto'
        with self.assertRaises(Exception):
            sitehydro.Sitehydroattache(code=code, ponderation=ponderation,
                                       decalage=decalage)


# -- class TestStation --------------------------------------------------------
class TestStation(unittest.TestCase):

    """Station class tests."""

    def test_base_01(self):
        """Base case with empty station."""
        code = 'O033401101'
        s = sitehydro.Station(code=code)
        self.assertEqual(
            (
                s.code, s.codeh2, s.typestation,
                s.libelle, s.libellecomplement,
                s.commentaireprive, s.dtmaj, s.pointk,
                s.dtmiseservice, s.dtfermeture,
                s.surveillance, s.niveauaffichage, s.coord,
                s.droitpublication, s.delaidiscontinuite,
                s.delaiabsence, s.essai, s.influence,
                s.influencecommentaire, s.commentaire,
                s.stationsanterieures, s.stationsposterieures,
                s.qualifsdonnees, s.finalites, s.loisstat, s.images,
                s.roles, s.capteurs, s.refsalti, s.commune,
                s.reseaux, s.plages, s.stationsamont, s.stationsaval,
                s.plagesstationsfille, s.plagesstationsmere),
            (
                code, None, 'LIMNI',
                None, None,
                None, None, None,
                None, None,
                None, 0, None,
                10, None,
                None, None, None,
                None, None,
                [], [],
                [], [], [], [],
                [], [], [], None,
                [], [], [], [],
                [], []))

    def test_base_02(self):
        """Base case test."""
        code = 'A033465001'
        codeh2 = 'A1234567'
        typestation = 'LIMNI'
        libelle = 'La Seine a Paris - rive droite'
        # libelleusuel = 'La Seine'
        libellecomplement = 'rive droite'
        coord = composant_site.Coord(x=15.6, y=19.4, proj=26)
        commentaireprive = 'commentaire privé'
        dtmaj = _datetime.datetime(2017, 7, 17, 9, 31, 15)
        dtmiseservice = _datetime.datetime(1990, 4, 5, 11, 45, 21)
        dtfermeture = _datetime.datetime(2007, 10, 1, 9, 36, 58)
        pointk = 35.68
        surveillance = True
        niveauaffichage = 991
        droitpublication = 20
        delaidiscontinuite = 38
        delaiabsence = 27
        essai = False
        influence = 3
        influencecommentaire = 'Influence com'
        commentaire = 'Commentaire'
        stationsanterieures = [sitehydro.Station(code='A123456789'),
                               sitehydro.Station(code='Z987654321')]
        stationsposterieures = [sitehydro.Station(code='B123456789'),
                                sitehydro.Station(code='C987654321')]
        qualifsdonnees = [composant_site.QualifDonnees(coderegime=1,
                                                       qualification=12),
                          composant_site.QualifDonnees(coderegime=2,
                                                       qualification=16)]
        finalites = [2, 5, 7]

        loi1 = composant_site.LoiStat(contexte=1, loi=2)
        loi2 = composant_site.LoiStat(contexte=2, loi=1)
        loisstat = [loi1, loi2]

        images = [composant_site.Image(adresse='http://www.toto.fr'),
                  composant_site.Image(adresse='http://www.tata.fr',
                                       typeill=2)]

        role1 = _rolecontact.RoleContact(contact=_intervenant.Contact('1234'),
                                         role='PRV')
        role2 = _rolecontact.RoleContact(
            contact=_intervenant.Contact('4321'),
            role='EXP',
            dtdeb=_datetime.datetime(2010, 4, 17, 11, 12, 13),
            dtfin=_datetime.datetime(2038, 10, 4, 17, 18, 19),
            dtmaj=_datetime.datetime(2018, 9, 3, 15, 54, 35))
        roles = [role1, role2]
        dtdeb = _datetime.datetime(2015, 5, 18, 11, 54, 34)
        alt = 154.2
        altitude = composant_site.Altitude(altitude=alt)
        refalti1 = composant_site.RefAlti(dtdeb=dtdeb, altitude=altitude)
        dtdeb = _datetime.datetime(2017, 6, 15, 13, 38, 1)
        alt = 189.1
        altitude = composant_site.Altitude(altitude=alt)
        refalti2 = composant_site.RefAlti(dtdeb=dtdeb, altitude=altitude)
        refsalti = [refalti1, refalti2]
        capteurs = [sitehydro.Capteur(code='V83310100101')]
        commune = '03150'
        reseaux = composant_site.ReseauMesure(code='33')
        stationsamont = [sitehydro.Station(code='K123495124'),
                         sitehydro.Station(code='L123495124')]
        stationsaval = [sitehydro.Station(code='M123495124'),
                        sitehydro.Station(code='O123495124')]
        plages = [
            sitehydro.PlageUtil(
                dtdeb=_datetime.datetime(2017, 9, 1, 12, 3, 19)),
            sitehydro.PlageUtil(
                dtdeb=_datetime.datetime(2017, 9, 1, 12, 3, 19),
                dtfin=_datetime.datetime(2020, 2, 15, 10, 11, 56),
                dtactivation=_datetime.datetime(2017, 8, 23, 9, 43, 32),
                dtdesactivation=_datetime.datetime(2017, 9, 4, 19, 41, 27),
                active=True)]
        ps1 = sitehydro.PlageStation(
            code='A010129840',
            dtdeb=_datetime.datetime(2010, 11, 4, 10, 52, 47),
            dtfin=_datetime.datetime(2011, 3, 27, 15, 14, 3))
        ps2 = sitehydro.PlageStation(
            code='K710129844',
            dtdeb=_datetime.datetime(2014, 10, 8, 11, 50, 32),
            dtfin=_datetime.datetime(2015, 6, 11, 17, 23, 14))
        plagesstationsfille = [ps1, ps2]
        ps3 = sitehydro.PlageStation(
            code='W354875674',
            dtdeb=_datetime.datetime(2000, 2, 10, 7, 10, 23),
            dtfin=_datetime.datetime(2005, 11, 3, 18, 15, 23))
        ps4 = sitehydro.PlageStation(
            code='K556854188',
            dtdeb=_datetime.datetime(2007, 6, 4, 11, 50, 37),
            dtfin=_datetime.datetime(2008, 9, 25, 13, 37, 43))
        plagesstationsmere = [ps3, ps4]
        s = sitehydro.Station(
            code=code, codeh2=codeh2, typestation=typestation,
            libelle=libelle, libellecomplement=libellecomplement,
            # libelleusuel=libelleusuel,
            commentaireprive=commentaireprive, dtmaj=dtmaj, pointk=pointk,
            dtmiseservice=dtmiseservice, dtfermeture=dtfermeture,
            surveillance=surveillance, niveauaffichage=niveauaffichage,
            coord=coord, droitpublication=droitpublication,
            delaidiscontinuite=delaidiscontinuite, delaiabsence=delaiabsence,
            essai=essai, influence=influence,
            influencecommentaire=influencecommentaire, commentaire=commentaire,
            stationsanterieures=stationsanterieures,
            stationsposterieures=stationsposterieures,
            qualifsdonnees=qualifsdonnees, finalites=finalites,
            loisstat=loisstat, images=images, roles=roles, capteurs=capteurs,
            refsalti=refsalti, commune=commune, reseaux=reseaux, plages=plages,
            stationsamont=stationsamont, stationsaval=stationsaval,
            plagesstationsfille=plagesstationsfille,
            plagesstationsmere=plagesstationsmere
        )
        self.assertEqual(
            (
                s.code, s.codeh2, s.typestation,
                s.libelle, s.libellecomplement,
                s.commentaireprive, s.dtmaj, s.pointk,
                s.dtmiseservice, s.dtfermeture,
                s.surveillance, s.niveauaffichage, s.coord,
                s.droitpublication, s.delaidiscontinuite,
                s.delaiabsence, s.essai, s.influence,
                s.influencecommentaire, s.commentaire,
                s.stationsanterieures, s.stationsposterieures,
                s.qualifsdonnees, s.finalites, s.loisstat, s.images,
                s.roles, s.capteurs, s.refsalti, s.commune,
                s.reseaux, s.plages, s.stationsamont, s.stationsaval,
                s.plagesstationsfille, s.plagesstationsmere),
            (
                code, codeh2, typestation,
                libelle, libellecomplement,
                commentaireprive, dtmaj, pointk,
                dtmiseservice, dtfermeture,
                surveillance, niveauaffichage, coord,
                droitpublication, delaidiscontinuite,
                delaiabsence, essai, influence,
                influencecommentaire, commentaire,
                stationsanterieures, stationsposterieures,
                qualifsdonnees, finalites, loisstat, images,
                roles, capteurs, refsalti, commune,
                [reseaux], plages, stationsamont, stationsaval,
                plagesstationsfille, plagesstationsmere))

    def test_base_03(self):
        """Update capteurs attribute."""
        code = 'A033465001'
        typestation = 'LIMNI'
        libelle = 'La Seine a Paris - rive droite'
        capteurs = [sitehydro.Capteur(code='V83310100101')]
        commune = '2B201'
        reseaux = [composant_site.ReseauMesure(code='33', libelle='Réseau'),
                   composant_site.ReseauMesure(code='the rezo')]
        s = sitehydro.Station(
            code=code, typestation=typestation, libelle=libelle,
            capteurs=capteurs, commune=commune, reseaux=reseaux
        )
        self.assertEqual(
            (s.code, s.typestation, s.libelle, s.commune, s.reseaux),
            (code, typestation, libelle, commune, reseaux)
        )
        s.capteurs = None
        self.assertEqual(s.capteurs, [])
        s.capteurs = capteurs[0]
        self.assertEqual(s.capteurs, capteurs)
        s.capteurs = capteurs
        self.assertEqual(s.capteurs, capteurs)

    def test_equality(self):
        """Equality test."""
        # strict mode
        code = 'O033401101'
        station = sitehydro.Station(code=code)
        other = sitehydro.Station(code=code)
        self.assertEqual(station, other)
        other.libelle = 'A label here...'
        self.assertNotEqual(station, other)
        # lazzy mode: None attributes are ignored
        self.assertTrue(station.__eq__(other, lazzy=True))
        # ignore some attrs
        self.assertNotEqual(station, other)
        self.assertTrue(station.__eq__(other, ignore=['libelle']))

    def test_str_01(self):
        """Test __str__ method with None values."""
        s = sitehydro.Station(code=0, strict=False)
        self.assertTrue(s.__str__().rfind('Station') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        code = '3'
        typestation = '6'
        s = sitehydro.Station(
            code=code, typestation=typestation, strict=False
        )
        self.assertEqual(
            (s.code, s.typestation),
            (code, typestation)
        )

    def test_error_01(self):
        """Typestation error."""
        code = 'A033465001'
        s = sitehydro.Station(code=code, typestation='LIMNI')
        with self.assertRaises(ValueError):
            s.__setattr__('typestation', None)
        with self.assertRaises(TypeError):
            sitehydro.Station(code=None)
        with self.assertRaises(ValueError):
            sitehydro.Station(code=code, typestation='LIMMMMNI')

    def test_error_02(self):
        """Code error."""
        code = 'B440112201'
        sitehydro.Station(code=code)
        with self.assertRaises(ValueError):
            sitehydro.Station(code=code[:-1])
        with self.assertRaises(ValueError):
            sitehydro.Station(code='%s0' % code)

    def test_error_03(self):
        """Capteur error."""
        code = 'B440112201'
        capteurs = (
            sitehydro.Capteur(code='%s01' % code, typemesure='Q'),
            sitehydro.Capteur(code='%s02' % code, typemesure='H'),
        )
        sitehydro.Station(
            code=code, typestation='DEB', capteurs=capteurs
        )
        with self.assertRaises(TypeError):
            sitehydro.Station(code=code, capteurs='c')
        with self.assertRaises(ValueError):
            sitehydro.Station(code=code, capteurs=capteurs)
        with self.assertRaises(ValueError):
            sitehydro.Station(
                code=code, typestation='LIMNI', capteurs=capteurs
            )
        with self.assertRaises(ValueError):
            sitehydro.Station(
                code=code, typestation='HC', capteurs=capteurs
            )

    def test_error_05(self):
        """Disceau error."""
        code = 'B440112201'
        reseau0 = composant_site.ReseauMesure(10)
        reseau1 = composant_site.ReseauMesure(code='10145', libelle='Réseau')
        for reseaux in [None, [], reseau0, reseau1, [reseau0, reseau1]]:
            sitehydro.Station(code=code, reseaux=reseaux)
        for reseaux in [10, [reseau0, 10], [10]]:
            with self.assertRaises(Exception):
                sitehydro.Station(code=code, reseaux=reseaux)

    def test_error_stations(self):
        """stationsanterieures,stationsposterieures
        stationsamont aval error."""
        stations = [sitehydro.Station(code='A123456789'),
                    sitehydro.Station(code='Z987654321')]
        for arg in ['stationsanterieures', 'stationsposterieures',
                    'stationsamont', 'stationsaval']:
            args = {}
            args['code'] = 'B440112201'
            for value in [None, stations, stations[0]]:
                args[arg] = value
                sitehydro.Station(**args)
            for value in ['toto', 'A123456789', ['A123456789'],
                          [stations[0], 'A123456789']]:
                args[arg] = value
                with self.assertRaises(Exception):
                    sitehydro.Station(**args)

    def test_error_qualifsdonnees(self):
        """Test qualifsdonnees error"""
        code = 'B440112201'
        qualifsdonnees = [composant_site.QualifDonnees(coderegime=1,
                                                       qualification=12),
                          composant_site.QualifDonnees(coderegime=2,
                                                       qualification=16)]
        for qualifs in [None, [], qualifsdonnees, qualifsdonnees[0]]:
            sitehydro.Station(code=code, qualifsdonnees=qualifs)
        for qualifs in ['toto', [qualifsdonnees[0], 'toto']]:
            with self.assertRaises(Exception):
                sitehydro.Station(code=code, qualifsdonnees=qualifs)

    def test_error_finalites(self):
        code = 'B440112201'
        finalites = [1, 3, '7']
        for fin in [None, [], finalites, finalites[0], finalites[2]]:
            sitehydro.Station(code=code, finalites=fin)
        for fin in [9, ['15'], [0, 'toto']]:
            with self.assertRaises(Exception):
                sitehydro.Station(code=code, finalites=fin)

    def test_error_refsalti(self):
        code = 'B440112201'
        dtdeb = _datetime.datetime(2015, 5, 18, 11, 54, 34)
        alt = 154.2
        altitude = composant_site.Altitude(altitude=alt)
        refalti1 = composant_site.RefAlti(dtdeb=dtdeb, altitude=altitude)
        dtdeb = _datetime.datetime(2017, 6, 15, 13, 38, 1)
        alt = 189.1
        altitude = composant_site.Altitude(altitude=alt)
        refalti2 = composant_site.RefAlti(dtdeb=dtdeb, altitude=altitude)
        refsalti = [refalti1, refalti2]
        for refs in [None, [], refsalti, refsalti[0]]:
            sitehydro.Station(code=code, refsalti=refs)
        for refs in [[refalti1, 'toto'], 'toto']:
            with self.assertRaises(Exception):
                sitehydro.Station(code=code, refsalti=refs)

    def test_error_plages(self):
        code = 'B440112201'
        plage1 = sitehydro.PlageUtil(
                    dtdeb=_datetime.datetime(2017, 9, 1, 12, 3, 19))
        plage2 = sitehydro.PlageUtil(
            dtdeb=_datetime.datetime(2017, 9, 1, 12, 3, 19),
            dtfin=_datetime.datetime(2020, 2, 15, 10, 11, 56),
            dtactivation=_datetime.datetime(2017, 8, 23, 9, 43, 32),
            dtdesactivation=_datetime.datetime(2017, 9, 4, 19, 41, 27),
            active=True)
        for plages in [None, [], plage1, [plage1], [plage1, plage2]]:
            sitehydro.Station(code=code, plages=plages)
        for plages in [5, ['tata'], [plage1, 5]]:
            with self.assertRaises(Exception):
                sitehydro.Station(code=code, plages=plages)

    def test_error_plagesstations(self):
        code = 'B440112201'
        ps1 = sitehydro.PlageStation(
            code='A010129840',
            dtdeb=_datetime.datetime(2010, 11, 4, 10, 52, 47),
            dtfin=_datetime.datetime(2011, 3, 27, 15, 14, 3))
        ps2 = sitehydro.PlageStation(
            code='K710129844',
            dtdeb=_datetime.datetime(2014, 10, 8, 11, 50, 32),
            dtfin=_datetime.datetime(2015, 6, 11, 17, 23, 14))
        for arg in ['plagesstationsfille', 'plagesstationsmere']:
            args = {}
            args['code'] = code
            for value in [None, [], ps1, [ps1], [ps1, ps2]]:
                args[arg] = value
                sitehydro.Station(**args)
            for value in ['toto', [5], [ps1, 5]]:
                args[arg] = value
                with self.assertRaises(Exception):
                    sitehydro.Station(**args)

    def test_images(self):
        """images test"""
        code = 'Z987654321'
        img1 = composant_site.Image(adresse='http://www.toto.fr')
        img2 = composant_site.Image(adresse='http://www.tata.fr',
                                    typeill=2)
        for images in [None, [], img1, [img2], [img1, img2]]:
            sitehydro.Station(code=code, images=images)
        for images in ['www.toto.fr', ['www.toto.fr'], [img1, 'toto']]:
            with self.assertRaises(Exception):
                sitehydro.Station(code=code, images=images)


# -- class TestCapteur --------------------------------------------------------
class TestCapteur(unittest.TestCase):

    """Capteur class tests."""

    def test_base_01(self):
        """Base case with empty capteur."""
        code = 'V83310100101'
        c = sitehydro.Capteur(code=code)
        self.assertEqual(
            (c.code, c.typemesure, c.libelle, c.typecapteur, c.codeh2,
             c.mnemo,c.surveillance, c.dtmaj, c.pdt, c.essai, c.commentaire,
             c.observateur, c.plages),
            (code, 'H', None, 0, None, None, None, None, None, None, None,
             None, [])
        )

    def test_base_02(self):
        """Base case test."""
        typemesure = 'Q'
        code = 'A03346500101'
        libelle = 'Capteur de secours'
        typecapteur = 5
        codeh2 = 'A0334650'
        mnemo = 'Mnémo capteur'
        surveillance = False
        dtmaj = _datetime.datetime(2016, 8, 3, 11, 16, 54)
        pdt = 17
        essai = True
        commentaire = 'Capteur secondaire'
        observateur = _intervenant.Contact(code='1549')

        plages = [
            sitehydro.PlageUtil(
                dtdeb=_datetime.datetime(2017, 9, 1, 12, 3, 19)),
            sitehydro.PlageUtil(
                dtdeb=_datetime.datetime(2017, 9, 1, 12, 3, 19),
                dtfin=_datetime.datetime(2020, 2, 15, 10, 11, 56),
                dtactivation=_datetime.datetime(2017, 8, 23, 9, 43, 32),
                dtdesactivation=_datetime.datetime(2017, 9, 4, 19, 41, 27),
                active=True)]
        c = sitehydro.Capteur(
            code=code, codeh2=codeh2, typemesure=typemesure, libelle=libelle,
            typecapteur=typecapteur, mnemo=mnemo, surveillance=surveillance,
            dtmaj=dtmaj, pdt=pdt, essai=essai, commentaire=commentaire,
            observateur=observateur, plages=plages
        )
        self.assertEqual(
            (c.code, c.codeh2, c.typemesure, c.libelle, c.typecapteur,
             c.mnemo, c.surveillance, c. dtmaj, c.pdt, c.essai, c.commentaire,
             c.observateur, c.plages),
            (code, codeh2, typemesure, libelle, typecapteur, mnemo,
             surveillance, dtmaj, pdt, essai, commentaire, observateur, plages)
        )

    def test_equality(self):
        """Equality test."""
        # strict mode
        typemesure = 'Q'
        code = 'A03346500101'
        libelle = 'Capteur de secours'
        capteur = sitehydro.Capteur(
            code=code, typemesure=typemesure, libelle=libelle
        )
        other = sitehydro.Capteur(
            code=code, typemesure=typemesure, libelle=libelle
        )
        self.assertEqual(capteur, other)
        other.libelle = None
        self.assertNotEqual(capteur, other)
        # lazzy mode: None attributes are ignored
        self.assertTrue(capteur.__eq__(other, lazzy=True))

    def test_str_01(self):
        """Test __str__ method with None values."""
        c = sitehydro.Capteur(code=0, strict=False)
        self.assertTrue(c.__str__().rfind('Capteur') > -1)
        self.assertTrue(c.__str__().rfind('type inconnu') > -1)

    def test_str_02(self):
        """Test __str__ method with None values."""
        typecapteur = 1
        c = sitehydro.Capteur(code=0, typecapteur=typecapteur, strict=False)
        self.assertTrue(c.__str__().rfind('Capteur') > -1)
        self.assertTrue(c.__str__().rfind('type observateur') > -1)

    def test_fuzzy_mode_01(self):
        """Fuzzy mode test."""
        typemesure = 'RR'
        code = 'C1'
        c = sitehydro.Capteur(
            code=code, typemesure=typemesure, strict=False
        )
        self.assertEqual(
            (c.code, c.typemesure),
            (code, typemesure)
        )

    def test_error_01(self):
        """Typemesure error."""
        c = sitehydro.Capteur(code='A14410010201', typemesure='H')
        with self.assertRaises(ValueError):
            c.__setattr__('typemesure', None)
        with self.assertRaises(ValueError):
            sitehydro.Capteur(code='A14410010201', typemesure='RR')

    def test_error_02(self):
        """Code error."""
        sitehydro.Capteur(code='B44011220101')
        with self.assertRaises(TypeError):
            sitehydro.Capteur(code=None)
        with self.assertRaises(ValueError):
            sitehydro.Capteur(code='B440112201')
        with self.assertRaises(ValueError):
            sitehydro.Capteur(code='B4401122010133')

    def test_error_03(self):
        """typecapteur error."""
        typecapteur = 6
        code = 'Z00123456789'
        sitehydro.Capteur(code=code,
                          typecapteur=typecapteur)
        typecapteur = 56
        with self.assertRaises(ValueError):
            sitehydro.Capteur(code=code,
                              typecapteur=typecapteur)

    def test_error_04(self):
        """dtmaj error"""
        dtmaj = _datetime.datetime(2014, 1, 9, 18, 14, 31)
        code = 'Z00123456789'
        sitehydro.Capteur(code=code,
                          dtmaj=dtmaj)
        for dtmaj in [5, 'toto']:
            with self.assertRaises(ValueError):
                sitehydro.Capteur(code=code,
                                  dtmaj=dtmaj)

    def test_surveillance(self):
        """surveillance error"""
        code = 'Z00123456789'
        for surveillance in [True, 1]:
            capteur = sitehydro.Capteur(code=code,
                                        surveillance=surveillance)
            self.assertTrue(capteur.surveillance)
        for surveillance in [False, 0]:
            capteur = sitehydro.Capteur(code=code,
                                        surveillance=surveillance)
            self.assertFalse(capteur.surveillance)

    def test_essai(self):
        """essai error"""
        code = 'Z00123456789'
        for essai in [True, 1]:
            capteur = sitehydro.Capteur(code=code,
                                        essai=essai)
            self.assertTrue(capteur.essai)
        for essai in [False, 0]:
            capteur = sitehydro.Capteur(code=code,
                                        essai=essai)
            self.assertFalse(capteur.essai)

    def test_error_pdt(self):
        """pdt error"""
        pdt = 5
        code = 'Z00123456789'
        sitehydro.Capteur(code=code,
                          pdt=pdt)
        for pdt in [-5, 'toto']:
            with self.assertRaises(Exception):
                sitehydro.Capteur(code=code,
                                  pdt=pdt)

    def test_error_observateur(self):
        """observateur error"""
        observateur = _intervenant.Contact(code='99')
        code = 'Z00123456789'
        sitehydro.Capteur(code=code,
                          observateur=observateur)
        for observateur in [18, '5', 'toto']:
            with self.assertRaises(TypeError):
                sitehydro.Capteur(code=code,
                                  observateur=observateur)

# -- class TestTronconvigilance -----------------------------------------------
class TestTronconvigilance(unittest.TestCase):

    """Tronconvigilance class tests."""

    def test_base_01(self):
        """Base case with empty troncon."""
        t = sitehydro.Tronconvigilance()
        self.assertEqual(
            (t.code, t.libelle),
            (None, None)
        )

    def test_base_02(self):
        """Base case test."""
        code = 'LO18'
        libelle = 'Loire amont'
        t = sitehydro.Tronconvigilance(code=code, libelle=libelle)
        self.assertEqual(
            (t.code, t.libelle),
            (code, libelle)
        )

    def test_equality(self):
        """Equality test."""
        code = 'LO18'
        libelle = 'Loire amont'
        troncon = sitehydro.Tronconvigilance(code=code, libelle=libelle)
        other = sitehydro.Tronconvigilance(code=code, libelle=libelle)
        self.assertEqual(troncon, other)
        other.libelle = 'Seine'
        self.assertNotEqual(troncon, other)

    def test_str_01(self):
        """Test __str__ method with None values."""
        t = sitehydro.Tronconvigilance()
        self.assertTrue(t.__str__().rfind('Troncon') > -1)

    def test_str_02(self):
        """Test __str__ method."""
        code = 'LO18'
        libelle = 'Loire amont'
        t = sitehydro.Tronconvigilance(code=code, libelle=libelle)
        self.assertTrue(t.__str__().rfind('Troncon') > -1)


# -- class TestPlageUtil -----------------------------------------------
class TestPlageUtil(unittest.TestCase):
    """PlageUtil class tests."""

    def test_base_01(self):
        """Base case with ."""
        dtdeb = _datetime.datetime(2016, 2, 3, 4, 5, 6)
        plage = sitehydro.PlageUtil(dtdeb=dtdeb)
        self.assertEqual(
            (plage.dtdeb, plage.dtfin, plage.dtactivation,
             plage.dtdesactivation, plage.active),
            (dtdeb, None, None, None, True)
        )

    def test_base_02(self):
        """Base case test."""
        dtdeb = _datetime.datetime(2016, 2, 3, 4, 5, 6)
        dtfin = _datetime.datetime(2016, 9, 1, 13, 15, 26)
        dtactivation = _datetime.datetime(2017, 8, 9, 11, 43, 56)
        dtdesactivation = _datetime.datetime(2017, 10, 18, 14, 24, 12)
        active = False
        plage = sitehydro.PlageUtil(dtdeb=dtdeb,
                                    dtfin=dtfin,
                                    dtactivation=dtactivation,
                                    dtdesactivation=dtdesactivation,
                                    active=active)
        self.assertEqual(
            (plage.dtdeb, plage.dtfin, plage.dtactivation,
             plage.dtdesactivation, plage.active),
            (dtdeb, dtfin, dtactivation, dtdesactivation, active)
        )

    def test_equality(self):
        """Equality test."""
        dtdeb = _datetime.datetime(2016, 2, 3, 4, 5, 6)
        dtfin = _datetime.datetime(2016, 9, 1, 13, 15, 26)
        dtactivation = _datetime.datetime(2017, 8, 9, 11, 43, 56)
        dtdesactivation = _datetime.datetime(2017, 10, 18, 14, 24, 12)
        active = False
        plage = sitehydro.PlageUtil(dtdeb=dtdeb,
                                    dtfin=dtfin,
                                    dtactivation=dtactivation,
                                    dtdesactivation=dtdesactivation,
                                    active=active)

        other = sitehydro.PlageUtil(dtdeb=dtdeb,
                                    dtfin=dtfin,
                                    dtactivation=dtactivation,
                                    dtdesactivation=dtdesactivation,
                                    active=active)
        self.assertEqual(plage, other)
        plage.dtdesactivation = _datetime.datetime(2017, 10, 18, 14, 25, 12)
        self.assertNotEqual(plage, other)

    def test_str_01(self):
        """Test __str__ method with only dtdeb."""
        dtdeb = _datetime.datetime(2016, 2, 3, 4, 5, 6)
        plage = sitehydro.PlageUtil(dtdeb=dtdeb)
        self.assertTrue(plage.__str__().rfind('active') > -1)
        self.assertTrue(plage.__str__().rfind('[2016-02-03 04:05:06') > -1)
        self.assertTrue(plage.__str__().rfind('sans date de fin') > -1)

    def test_str_02(self):
        """Test __str__ method."""
        dtdeb = _datetime.datetime(2016, 2, 3, 4, 5, 6)
        dtfin = _datetime.datetime(2030, 4, 9, 11, 15, 26)
        active = False
        plage = sitehydro.PlageUtil(dtdeb=dtdeb,
                                    dtfin=dtfin,
                                    active=active)
        self.assertTrue(plage.__str__().rfind('[2016-02-03 04:05:06') > -1)
        self.assertTrue(plage.__str__().rfind('2030-04-09 11:15:26]') > -1)
        self.assertTrue(plage.__str__().rfind('inactive') > -1)


# -- class TestPlageStation -----------------------------------------------
class TestPlageStation(unittest.TestCase):
    """PlageStation class tests."""

    def test_base_01(self):
        """simple test"""
        dtdeb = _datetime.datetime(2015, 4, 11, 13, 58, 23)
        code = 'A123456789'
        pst = sitehydro.PlageStation(code=code, dtdeb=dtdeb)
        self.assertEqual((pst.code, pst.dtdeb, pst.dtfin),
                         (code, dtdeb, None))

    def test_base_full_plagestation(self):
        """Test full PlageStation"""
        dtdeb = _datetime.datetime(2015, 4, 11, 13, 58, 23)
        dtfin = _datetime.datetime(2019, 10, 28, 10, 14, 3)
        code = 'A123456789'
        libelle = 'libellé'
        pst = sitehydro.PlageStation(code=code, libelle=libelle,
                                     dtdeb=dtdeb, dtfin=dtfin)
        self.assertEqual((pst.code, pst.libelle, pst.dtdeb, pst.dtfin),
                         (code, libelle, dtdeb, dtfin))

    def test_str(self):
        dtdeb = _datetime.datetime(2015, 4, 11, 13, 58, 23)
        dtfin = _datetime.datetime(2019, 10, 28, 10, 14, 3)
        code = 'A123456789'
        pst = sitehydro.PlageStation(code=code, dtdeb=dtdeb, dtfin=dtfin)
        pst_str = pst.__str__()
        self.assertTrue(pst_str.find(dtdeb.__str__()) > -1)
        self.assertTrue(pst_str.find(dtfin.__str__()) > -1)
        self.assertTrue(pst_str.find(code) > -1)
        pst.dtfin = None
        pst_str = pst.__str__()
        self.assertTrue(pst_str.find('sans date de fin') > -1)

    def test_error_station(self):
        dtdeb = _datetime.datetime(2015, 4, 11, 13, 58, 23)
        code = 'A123456789'
        sitehydro.PlageStation(code=code, dtdeb=dtdeb)
        for code in [None, 5, 'A123456']:
            with self.assertRaises(Exception):
                sitehydro.PlageStation(code=code, dtdeb=dtdeb)

    def test_error_dtdeb(self):
        dtdeb = _datetime.datetime(2015, 4, 11, 13, 58, 23)
        code = 'A123456789'
        sitehydro.PlageStation(code=code, dtdeb=dtdeb)
        for dtdeb in [None, 5]:
            with self.assertRaises(Exception):
                sitehydro.PlageStation(code=code, dtdeb=dtdeb)

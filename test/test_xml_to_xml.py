# -*- coding: utf-8 -*-
"""Test program for xml.to_xml.

To run all tests just type:
    './test_xml_to_xml.py' or 'python test_xml_to_xml.py'

To run only a class test:
    python -m unittest test_xml_to_xml.TestClass

To run only a specific test:
    python -m unittest test_xml_to_xml.TestClass
    python -m unittest test_xml_to_xml.TestClass.test_method

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

from lxml import etree

from libhydro.conv.xml import (
    _to_xml as to_xml,
    _from_xml as from_xml
)

#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin""" \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1b"""
__date__ = """2013-11-23"""

#HISTORY
#V0.1 - 2013-08-30
#    first shot


# -- config -------------------------------------------------------------------
COMPARE = 17


#-- class TestFunctions -------------------------------------------------------
class TestFunctions(unittest.TestCase):

    """Functions class tests."""

    def test_factory_single_element_01(self):
        """Factory single element base test."""
        root = etree.Element('Root')
        story = {
            'SubRoot': {'value': 'toto'}
        }
        element = to_xml._factory(root=root, story=story)
        firstpass = True
        for child in element.find(story.keys()[0]):
            self.assertTrue(firstpass)
            firstpass = False
            self.assertEqual(child.tag, story.keys()[0])
            self.assertEqual(child.text, story.values()[0]['value'])
            self.asserEqual(child.attrib, None)

    def test_factory_single_element_02(self):
        """Factory single element with attributes test."""
        root = etree.Element('Root')
        story = {
            'SubRoot': {'value': 'toto', 'attr': {'a': '1', 'b': '2'}}
        }
        element = to_xml._factory(root=root, story=story)
        firstpass = True
        for child in element.find(story.keys()[0]):
            self.assertTrue(firstpass)
            firstpass = False
            self.assertEqual(child.tag, story.keys()[0])
            self.assertEqual(child.text, story.values()[0]['value'])
            self.assertEqual(child.attrib, story.values()[0]['attr'])

    def test_factory_single_element_03(self):
        """Factory single element with force test."""
        root = etree.Element('Root')
        # force is False, element should not be appended
        story = {
            'SubRoot': {'value': None}
        }
        element = to_xml._factory(root=root, story=story)
        self.assertIsNone(element.find(story.keys()[0]))
        # force is True, element should be appended
        story = {
            'SubRoot': {'value': None, 'force': True}
        }
        element = to_xml._factory(root=root, story=story)
        firstpass = True
        for child in element.find(story.keys()[0]):
            self.assertTrue(firstpass)
            firstpass = False
            self.assertEqual(child.tag, story.keys()[0])
            self.assertEqual(child.text, None)

    def test_factory_multi_element(self):
        """Factory multi element test."""
        root = etree.Element('Root')
        story = {
            'SubRoot': {'value': ('toto', 'tata', 'titi')}
        }
        element = to_xml._factory(root=root, story=story)
        passes = 0
        for child in element.findall(story.keys()[0]):
            passes += 1
            self.assertEqual(child.tag, story.keys()[0])
            self.assertTrue(child.text in story.values()[0]['value'])
        self.assertEqual(passes, 3)

    def test_factory_sub_story(self):
        """Factory sub story test."""
        root = etree.Element('Root')
        story = {
            'SubRoot': {'value': 'toto'}
        }
        element = to_xml._factory(root=root, story=story)
        firstpass = True
        for child in element:
            self.assertTrue(firstpass)
            firstpass = False
            self.assertEqual(child.tag, story.keys()[0])
            self.assertEqual(child.text, story.values()[0]['value'])

    def test_make_element(self):
        """Make element base test."""
        args = ('TagName', 'text', {'attr1': '1', 'attr2': '2'})
        element = to_xml._make_element(*args)
        self.assertEqual(element.tag, args[0])
        self.assertEqual(element.text, args[1])
        self.assertEqual(element.attrib, args[2])


#-- class TestToXmlSiteshydro -------------------------------------------------
class TestToXmlSitesHydros(unittest.TestCase):

    """ToXmlSitesHydro class tests."""

    def test_base(self):
        """Base test."""

        expected = """<hydrometrie>"""\
            """<Scenario>"""\
            """<CodeScenario>hydrometrie</CodeScenario>"""\
            """<VersionScenario>1.1</VersionScenario>"""\
            """<NomScenario>Echange de données hydrométriques</NomScenario>"""\
            """<DateHeureCreationFichier>2010-02-26T12:53:10"""\
            """</DateHeureCreationFichier>"""\
            """<Emetteur>"""\
            """<CdIntervenant schemaAgencyID="SANDRE">25</CdIntervenant>"""\
            """<CdContact schemaAgencyID="SANDRE">1069</CdContact>"""\
            """</Emetteur>"""\
            """<Destinataire>"""\
            """<CdIntervenant schemaAgencyID="SANDRE">1537</CdIntervenant>"""\
            """</Destinataire>"""\
            """</Scenario>"""\
            """<RefHyd>"""\
            """<SitesHydro>"""\
            """<SiteHydro>"""\
            """<CdSiteHydro>A1984310</CdSiteHydro>"""\
            """<TypSiteHydro>REEL</TypSiteHydro>"""\
            """</SiteHydro>"""\
            """<SiteHydro>"""\
            """<CdSiteHydro>O1984310</CdSiteHydro>"""\
            """<LbSiteHydro>Le Touch à Toulouse [Saint-Martin-du-Touch]"""\
            """</LbSiteHydro>"""\
            """<TypSiteHydro>SOURCE</TypSiteHydro>"""\
            """<CdCommune>11354</CdCommune>"""\
            """<CdCommune>11355</CdCommune>"""\
            """<CdCommune>2B021</CdCommune>"""\
            """<StationsHydro>"""\
            """<StationHydro>"""\
            """<CdStationHydro>O198431001</CdStationHydro>"""\
            """<LbStationHydro>station 1</LbStationHydro>"""\
            """<TypStationHydro>LIMNI</TypStationHydro>"""\
            """</StationHydro>"""\
            """<StationHydro>"""\
            """<CdStationHydro>O198431002</CdStationHydro>"""\
            """<LbStationHydro>station 2</LbStationHydro>"""\
            """<TypStationHydro>LIMNI</TypStationHydro>"""\
            """</StationHydro>"""\
            """<StationHydro>"""\
            """<CdStationHydro>O198431003</CdStationHydro>"""\
            """<LbStationHydro>station 3</LbStationHydro>"""\
            """<TypStationHydro>LIMNI</TypStationHydro>"""\
            """</StationHydro>"""\
            """</StationsHydro>"""\
            """</SiteHydro>"""\
            """<SiteHydro>"""\
            """<CdSiteHydro>O2000040</CdSiteHydro>"""\
            """<LbSiteHydro>La Garonne à Toulouse</LbSiteHydro>"""\
            """<TypSiteHydro>REEL</TypSiteHydro>"""\
            """<StationsHydro>"""\
            """<StationHydro>"""\
            """<CdStationHydro>O200004001</CdStationHydro>"""\
            """<LbStationHydro>La Garonne à Toulouse</LbStationHydro>"""\
            """<TypStationHydro>LIMNI</TypStationHydro>"""\
            """</StationHydro>"""\
            """</StationsHydro>"""\
            """</SiteHydro>"""\
            """<SiteHydro>"""\
            """<CdSiteHydro>O1712510</CdSiteHydro>"""\
            """<LbSiteHydro>L'Ariège à Auterive</LbSiteHydro>"""\
            """<TypSiteHydro>REEL</TypSiteHydro>"""\
            """<CdSiteHydroAncienRef>O1235401</CdSiteHydroAncienRef>"""\
            """<StationsHydro>"""\
            """<StationHydro>"""\
            """<CdStationHydro>O171251001</CdStationHydro>"""\
            """<LbStationHydro>L'Ariège à Auterive - station de secours"""\
            """</LbStationHydro>"""\
            """<TypStationHydro>LIMNI</TypStationHydro>"""\
            """<Capteurs>"""\
            """<Capteur>"""\
            """<CdCapteur>O17125100102</CdCapteur>"""\
            """<LbCapteur>Radar</LbCapteur>"""\
            """<TypMesureCapteur>H</TypMesureCapteur>"""\
            """</Capteur>"""\
            """<Capteur>"""\
            """<CdCapteur>O17125100101</CdCapteur>"""\
            """<LbCapteur>Ultrasons principal</LbCapteur>"""\
            """<TypMesureCapteur>H</TypMesureCapteur>"""\
            """<CdCapteurAncienRef>O1712510</CdCapteurAncienRef>"""\
            """</Capteur>"""\
            """</Capteurs>"""\
            """<CdStationHydroAncienRef>O1712510</CdStationHydroAncienRef>"""\
            """<CdCommune>11354</CdCommune>"""\
            """</StationHydro>"""\
            """</StationsHydro>"""\
            """</SiteHydro>"""\
            """</SitesHydro>"""\
            """</RefHyd>"""\
            """</hydrometrie>"""

        # read xml
        data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'siteshydro.xml')
        )
        xml = etree.tostring(
            to_xml._to_xml(
                scenario=data['scenario'],
                siteshydro=data['siteshydro']
            ),
            encoding='utf-8'
        ).decode('utf-8')

        # test
        assert_unicode_equal(xml, expected)


#-- class TestToXmlSitesMeteo -------------------------------------------------
#TODO


#-- class TestToXmlObssHydro --------------------------------------------------
class TestToXmlObssHydro(unittest.TestCase):

    """ToXmlObssHydro class tests."""

    def test_base(self):
        """Base test."""

        expected = """<hydrometrie>"""\
            """<Scenario>"""\
            """<CodeScenario>hydrometrie</CodeScenario>"""\
            """<VersionScenario>1.1</VersionScenario>"""\
            """<NomScenario>Echange de données hydrométriques</NomScenario>"""\
            """<DateHeureCreationFichier>2010-02-26T07:05:00</DateHeureCreationFichier>"""\
            """<Emetteur>"""\
            """<CdIntervenant schemaAgencyID="SANDRE">1520</CdIntervenant>"""\
            """<CdContact schemaAgencyID="SANDRE">26</CdContact>"""\
            """</Emetteur>"""\
            """<Destinataire>"""\
            """<CdIntervenant schemaAgencyID="SANDRE">1537</CdIntervenant>"""\
            """</Destinataire>"""\
            """</Scenario>"""\
            """<Donnees>"""\
            """<Series>"""\
            """<Serie>"""\
            """<CdSiteHydro>V7144010</CdSiteHydro>"""\
            """<GrdSerie>Q</GrdSerie>"""\
            """<StatutSerie>4</StatutSerie>"""\
            """<ObssHydro>"""\
            """<ObsHydro>"""\
            """<DtObsHydro>2010-02-26T11:10:00</DtObsHydro>"""\
            """<ResObsHydro>20992.0</ResObsHydro>"""\
            """<MethObsHydro>0</MethObsHydro>"""\
            """<QualifObsHydro>16</QualifObsHydro>"""\
            """<ContObsHydro>True</ContObsHydro>"""\
            """</ObsHydro>"""\
            """<ObsHydro>"""\
            """<DtObsHydro>2010-02-26T11:15:00</DtObsHydro>"""\
            """<ResObsHydro>21176.0</ResObsHydro>"""\
            """<MethObsHydro>0</MethObsHydro>"""\
            """<QualifObsHydro>16</QualifObsHydro>"""\
            """<ContObsHydro>True</ContObsHydro>"""\
            """</ObsHydro>"""\
            """</ObssHydro>"""\
            """</Serie>"""\
            """<Serie>"""\
            """<CdStationHydro>V714401001</CdStationHydro>"""\
            """<GrdSerie>Q</GrdSerie>"""\
            """<StatutSerie>4</StatutSerie>"""\
            """<ObssHydro>"""\
            """<ObsHydro>"""\
            """<DtObsHydro>2010-02-26T13:10:00</DtObsHydro>"""\
            """<ResObsHydro>20.0</ResObsHydro>"""\
            """<MethObsHydro>12</MethObsHydro>"""\
            """<QualifObsHydro>12</QualifObsHydro>"""\
            """<ContObsHydro>False</ContObsHydro>"""\
            """</ObsHydro>"""\
            """<ObsHydro>"""\
            """<DtObsHydro>2010-02-26T13:15:00</DtObsHydro>"""\
            """<ResObsHydro>21.0</ResObsHydro>"""\
            """<MethObsHydro>12</MethObsHydro>"""\
            """<QualifObsHydro>8</QualifObsHydro>"""\
            """<ContObsHydro>False</ContObsHydro>"""\
            """</ObsHydro>"""\
            """</ObssHydro>"""\
            """</Serie>"""\
            """<Serie>"""\
            """<CdCapteur>V71440100103</CdCapteur>"""\
            """<GrdSerie>H</GrdSerie>"""\
            """<StatutSerie>4</StatutSerie>"""\
            """<ObssHydro>"""\
            """<ObsHydro>"""\
            """<DtObsHydro>2010-02-26T13:10:00</DtObsHydro>"""\
            """<ResObsHydro>680.0</ResObsHydro>"""\
            """<MethObsHydro>4</MethObsHydro>"""\
            """<QualifObsHydro>20</QualifObsHydro>"""\
            """<ContObsHydro>True</ContObsHydro>"""\
            """</ObsHydro>"""\
            """<ObsHydro>"""\
            """<DtObsHydro>2010-02-26T13:15:00</DtObsHydro>"""\
            """<ResObsHydro>684.0</ResObsHydro>"""\
            """<MethObsHydro>0</MethObsHydro>"""\
            """<QualifObsHydro>20</QualifObsHydro>"""\
            """<ContObsHydro>True</ContObsHydro>"""\
            """</ObsHydro>"""\
            """<ObsHydro>"""\
            """<DtObsHydro>2010-02-26T14:55:00</DtObsHydro>"""\
            """<ResObsHydro>670.0</ResObsHydro>"""\
            """<MethObsHydro>12</MethObsHydro>"""\
            """<QualifObsHydro>20</QualifObsHydro>"""\
            """<ContObsHydro>True</ContObsHydro>"""\
            """</ObsHydro>"""\
            """</ObssHydro>"""\
            """</Serie>"""\
            """</Series>"""\
            """</Donnees>"""\
            """</hydrometrie>"""

        # read xml
        data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'obsshydro.xml')
        )
        xml = etree.tostring(
            to_xml._to_xml(
                scenario=data['scenario'],
                series=data['series']
            ),
            encoding='utf-8'
        ).decode('utf-8')

        # test
        assert_unicode_equal(xml, expected)


#-- class TestToXmlObssMeteo --------------------------------------------------
#TODO


#-- class TestToXmlSimulations ------------------------------------------------
class TestToXmlSimulations(unittest.TestCase):

    """ToXmlSimulations class tests."""

    def test_base(self):
        """Base test."""

        expected = """<hydrometrie>"""\
            """<Scenario>"""\
            """<CodeScenario>hydrometrie</CodeScenario>"""\
            """<VersionScenario>1.1</VersionScenario>"""\
            """<NomScenario>Echange de données hydrométriques</NomScenario>"""\
            """<DateHeureCreationFichier>2010-02-26T09:30:00</DateHeureCreationFichier>"""\
            """<Emetteur>"""\
            """<CdIntervenant schemaAgencyID="SANDRE">1537</CdIntervenant>"""\
            """<CdContact schemaAgencyID="SANDRE">41</CdContact>"""\
            """</Emetteur>"""\
            """<Destinataire>"""\
            """<CdIntervenant schemaAgencyID="SANDRE">14</CdIntervenant>"""\
            """</Destinataire>"""\
            """</Scenario>"""\
            """<Donnees>"""\
            """<Simuls>"""\
            """<Simul>"""\
            """<GrdSimul>Q</GrdSimul>"""\
            """<DtProdSimul>2010-02-26T14:45:00</DtProdSimul>"""\
            """<IndiceQualiteSimul>36</IndiceQualiteSimul>"""\
            """<StatutSimul>4</StatutSimul>"""\
            """<PubliSimul>False</PubliSimul>"""\
            """<ComSimul>Biais=-14.91 Précision=36.00</ComSimul>"""\
            """<CdSiteHydro>Y1612020</CdSiteHydro>"""\
            """<CdModelePrevision>13_08</CdModelePrevision>"""\
            """<Prevs>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T14:00:00</DtPrev>"""\
            """<ResMinPrev>10.0</ResMinPrev>"""\
            """<ResMoyPrev>30.0</ResMoyPrev>"""\
            """<ResMaxPrev>50.0</ResMaxPrev>"""\
            """<ProbsPrev>"""\
            """<ProbPrev>"""\
            """<PProbPrev>20</PProbPrev>"""\
            """<ResProbPrev>25.0</ResProbPrev>"""\
            """</ProbPrev>"""\
            """<ProbPrev>"""\
            """<PProbPrev>40</PProbPrev>"""\
            """<ResProbPrev>75.0</ResProbPrev>"""\
            """</ProbPrev>"""\
            """<ProbPrev>"""\
            """<PProbPrev>49</PProbPrev>"""\
            """<ResProbPrev>90.0</ResProbPrev>"""\
            """</ProbPrev>"""\
            """</ProbsPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T15:00:00</DtPrev>"""\
            """<ResMoyPrev>23.0</ResMoyPrev>"""\
            """<ResMaxPrev>25.0</ResMaxPrev>"""\
            """</Prev>"""\
            """</Prevs>"""\
            """</Simul>"""\
            """<Simul>"""\
            """<GrdSimul>H</GrdSimul>"""\
            """<DtProdSimul>2010-02-26T14:45:00</DtProdSimul>"""\
            """<IndiceQualiteSimul>21</IndiceQualiteSimul>"""\
            """<StatutSimul>4</StatutSimul>"""\
            """<PubliSimul>True</PubliSimul>"""\
            """<CdStationHydro>Y161202001</CdStationHydro>"""\
            """<CdModelePrevision>ScMerSHOM</CdModelePrevision>"""\
            """<Prevs>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T14:00:00</DtPrev>"""\
            """<ResMoyPrev>371.774</ResMoyPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T15:00:00</DtPrev>"""\
            """<ResMoyPrev>271.374</ResMoyPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T16:00:00</DtPrev>"""\
            """<ResMoyPrev>267.747</ResMoyPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T17:00:00</DtPrev>"""\
            """<ResMoyPrev>422.28</ResMoyPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T18:00:00</DtPrev>"""\
            """<ResMoyPrev>218.297</ResMoyPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T19:00:00</DtPrev>"""\
            """<ResMoyPrev>264.121</ResMoyPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T20:00:00</DtPrev>"""\
            """<ResMoyPrev>280.604</ResMoyPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T21:00:00</DtPrev>"""\
            """<ResMoyPrev>358.71</ResMoyPrev>"""\
            """</Prev>"""\
            """</Prevs>"""\
            """</Simul>"""\
            """<Simul>"""\
            """<GrdSimul>Q</GrdSimul>"""\
            """<DtProdSimul>2010-02-26T09:45:00</DtProdSimul>"""\
            """<IndiceQualiteSimul>29</IndiceQualiteSimul>"""\
            """<StatutSimul>16</StatutSimul>"""\
            """<PubliSimul>False</PubliSimul>"""\
            """<CdSiteHydro>Y1612020</CdSiteHydro>"""\
            """<CdModelePrevision>13_09</CdModelePrevision>"""\
            """<Prevs>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T09:00:00</DtPrev>"""\
            """<ResMinPrev>22.0</ResMinPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T10:00:00</DtPrev>"""\
            """<ResMaxPrev>33.0</ResMaxPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T11:00:00</DtPrev>"""\
            """<ResMinPrev>44.0</ResMinPrev>"""\
            """</Prev>"""\
            """<Prev>"""\
            """<DtPrev>2010-02-26T12:00:00</DtPrev>"""\
            """<ResMaxPrev>55.0</ResMaxPrev>"""\
            """</Prev>"""\
            """</Prevs>"""\
            """</Simul>"""\
            """</Simuls>"""\
            """</Donnees>"""\
            """</hydrometrie>"""

        # read xml
        data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'simulations.xml')
        )
        xml = etree.tostring(
            to_xml._to_xml(
                scenario=data['scenario'],
                simulations=data['simulations']
            ),
            encoding='utf-8'
        ).decode('utf-8')

        # test
        assert_unicode_equal(xml, expected)


# -- functions ----------------------------------------------------------------
def assert_unicode_equal(xml, expected):
    """Raise personnal AssertionError on failure."""
    for (i, c) in enumerate(expected):
        try:
            assert(xml[i] == c)

        except AssertionError:
            raise AssertionError(
                'error character %i\n'
                '%s\n%s%sv%s%s\n%s' % (
                    i,
                    xml[i - (2 * COMPARE):i + (2 * COMPARE)],
                    ' ' * COMPARE, '-' * COMPARE,
                    '-' * COMPARE, ' ' * COMPARE,
                    expected[i - (2 * COMPARE):i + (2 * COMPARE)]
                )
            )


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

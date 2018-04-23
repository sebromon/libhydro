# coding: utf-8
"""Test program for xml.to_xml.

To run all tests just type:
    python -m unittest test_conv_xml_to_xml

To run only a class test:
    python -m unittest test_conv_xml_to_xml.TestClass

To run only a specific test:
    python -m unittest test_conv_xml_to_xml.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import os
import unittest

from lxml import etree

from libhydro.conv.xml import _to_xml as to_xml, _from_xml as from_xml
from libhydro.core import sitehydro, seuil


# -- strings ------------------------------------------------------------------
__version__ = '0.6.1'
__date__ = '2017-07-05'

# HISTORY
# V0.6.1 - SR - 2017-07-05
# Add xml fim with jaugeages
# V0.6 - SR - 2017-06-22
# Ajout xml contenant des courbes de correction
# V0.5 - SR - 2017-06-20
# Ajout xml contenant des courbes de tarage
# V0.4 - 2014-08-04
#   fix some pandas failures
#   temporarily escape some unstable tests (FIXME)
#   separate the sandre and bdhydro tests
# V0.3 - 2014-08-01
#   update the ToXmlBaseTest to write all tags
# V0.2 - 2014-03-22
#   factorize all the base tests in a suite
# V0.1 - 2013-08-30
#   first shot

# -- config -------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# assert_unicode_equal function parameter
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# number of chars printed on screen to compare the 2 xml strings
# half of the value is before the error (left), the other is after (right)
# change this value if on screen comparison is to short or too long
COMPARE = 35


# -- functions ----------------------------------------------------------------
def xml_to_unicode(fname):
    """Return unicode."""
    with open(fname, 'r') as f:

        # remove XML declaration line and  get the file encoding
        f.readline()
        encoding = 'utf-8'

        # make the string and return
        lines = [
            #l.decode(encoding).strip()
            l.strip()
            for l in f.readlines()
            if not l.lstrip().startswith('<!--')]
            #if not l.decode(encoding).lstrip().startswith('<!--')]
        return ''.join(lines)


def assert_unicode_equal(xml, expected, msg=None):
    """Raise personnal AssertionError on failure.

    Compare the 2 xml strings char by char and returns the exact place where
    it doesn't match, with 2 * COMPARE lenght char context.

    Example:
        HeureCreationFichier><Emetteur><CdIntervenant schemeAgencyID="SANDRE
                    ----------------------v----------------------
        HeureCreationFichier><Emetteur><CdContact>26</CdContact></Emetteur><

    """
    for (i, c) in enumerate(expected):
        try:
            assert(xml[i] == c)

        except AssertionError:
            raise AssertionError(
                '{msg} => error character {place:d}\n\n'
                '{xml}\n'
                '{fill1}{fill2}v{fill2}\n'
                '{expected}'.format(
                    fill1=' ' * COMPARE,
                    fill2='-' * COMPARE,
                    msg=msg or '',
                    place=i,
                    xml=xml[i - (2 * COMPARE):i + (2 * COMPARE)],
                    expected=expected[i - (2 * COMPARE):i + (2 * COMPARE)]))


# -- class TestToXmlSeuilsHydro -----------------------------------------------
class TestToXmlSeuilsHydro(unittest.TestCase):

    """ToXmlSeuilsHydro class tests, with some specific tests for seuils."""

    def test_error_01(self):
        """More than one site valeurseuil."""
        site = sitehydro.Sitehydro('X2221010')
        seuilhydro = seuil.Seuilhydro('33', sitehydro=site)
        seuilhydro.valeurs = [
            seuil.Valeurseuil(2, entite=site),
            seuil.Valeurseuil(5, entite=site)]
        with self.assertRaises(ValueError):
            to_xml._seuilhydro_to_element(seuilhydro)

    def test_error_02(self):
        """Valeurseuil entite is not a station."""
        site = sitehydro.Sitehydro('X2221010')
        seuilhydro = seuil.Seuilhydro('33', sitehydro=site)
        valeurseuil = seuil.Valeurseuil(
            valeur=2, seuil=seuilhydro, entite=site)
        with self.assertRaises(TypeError):
            to_xml._valeurseuilstation_to_element(valeurseuil)


# -- class ParametrizedTestCase -----------------------------------------------
class ParametrizedTestCase(unittest.TestCase):

    """TestCase classes that want to be parametrized should inherit from this
    class."""

    # it works but lack of a precise error message.

    # source: http://eli.thegreenplace.net/2011/08/02/
    #         python-unit-testing-parametrized-test-cases/
    # see also:  https://pypi.python.org/pypi/testscenarios/

    def __init__(self, methodName='runTest', param=None, version=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param
        self.version = version

    @staticmethod
    def parametrize(testcase_class, param, version):
        """ Create a suite containing all tests taken from the given subclass,
        passing them the parameter 'param'."""
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        for testname in testnames:
            suite.addTest(testcase_class(testname, param=param,
                                         version=version))
        return suite


# -- class ToXmlBaseTest ------------------------------------------------------
class ToXmlBaseTest(ParametrizedTestCase):

    """ToXmlBaseTest class.

    A basic test for a unit asserts that reading the (param).xml file and
    re-writing it, gives the same string as in the (param)_expected.xml.

    Note that the file name (param) MUST be the Scenario attribute for this
    unit.

    """
    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # build the expected string
        if self.param is not None and self.version is not None:
            self.expected = xml_to_unicode(os.path.join(
                'data', 'xml', self.version, '%s_expected.xml' % self.param))
            self.expected_bdhydro = xml_to_unicode(os.path.join(
                'data', 'xml', self.version, '%s_expected_bdhydro.xml' % (
                    self.param)))
        # set our own assertEqual function, more verbose
        self.assertEqual = assert_unicode_equal

    def test_base(self):
        """Sandre format test."""

        # TODO discover hack - we do not want unittest.discover to run this
        #                      test directly. But it count as a real test :-(
        if self.param is None:
            self.skipTest('this test runs in a separated TestSuite')

        # build object from xml
        data = from_xml._parse(
            os.path.join('data', 'xml', self.version, '%s.xml' % self.param))
        data['ordered'] = True
        # build xml string from objects
        xml = etree.tostring(to_xml._to_xml(
            bdhydro=False, version=self.version, **data), encoding='utf-8').decode('utf-8')
        # test
#         if self.param == 'seriesmeteo':  # FIXME
#             self.skipTest(
#                 "the 'seriesmeteo' test can fail for ordering problems...")
        self.assertEqual(
            xml, self.expected,
            msg='To XML SANDRE format test for unit <%s>' % self.param)

    def test_bdhydro(self):
        """Bdhydro format test."""

        # TODO discover hack - we do not want unittest.discover to run this
        #                      test directly. But it count as a real test :-(
        if self.param is None:
            self.skipTest('this test runs in a separated TestSuite')

        # build object from xml
        data = from_xml._parse(
            os.path.join('data', 'xml', self.version, '%s.xml' % self.param))
        data['ordered'] = True
        # build xml string from objects
        xml = etree.tostring(to_xml._to_xml(
            bdhydro=True, version=self.version, **data), encoding='utf-8').decode('utf-8')
        # test
#         if self.param == 'seriesmeteo':  # FIXME
#             self.skipTest(
#                 "the 'seriesmeteo' test can fail for ordering problems...")
        self.assertEqual(
            xml, self.expected_bdhydro,
            msg='To XML BDHYDRO format test for unit <%s>' % self.param)


# -- class TestAllXmlBaseTests ------------------------------------------------
class TestAllXmlBaseTests(unittest.TestCase):
    """Run All base tests in a TestSuite.

    Required by unittest.discover.

    """
    suite = unittest.TestSuite()
    version_units = {}
    version_units['1.1'] = ('intervenants', 'siteshydro', 'sitesmeteo',
                            'seuilshydro', 'modelesprevision', 'evenements',
                            'courbestarage', 'jaugeages', 'courbescorrection',
                            'serieshydro', 'seriesmeteo', 'obsselaboree',
                            'obsselaboreemeteo', 'simulations')
    version_units['2'] = ('serieshydro', 'seriesmeteo', 'obsselab',
                          'obsselabmeteo')
    for version, units in version_units.items():
        for unit in units:
            suite.addTest(
                ParametrizedTestCase.parametrize(ToXmlBaseTest, param=unit,
                                                 version=version))
    unittest.TextTestRunner(verbosity=1).run(suite)


# -- class TestFunctions ------------------------------------------------------
class TestFunctions(unittest.TestCase):

    """Functions class tests."""

    def test_factory_single_element_01(self):
        """Factory single element base test."""
        root = etree.Element('Root')
        story = {'SubRoot': {'value': 'toto'}}
        element = to_xml._factory(root=root, story=story)
        firstpass = True
        for child in element.find(list(story.keys())[0]):
            self.assertTrue(firstpass)
            firstpass = False
            self.assertEqual(child.tag, list(story.keys())[0])
            self.assertEqual(child.text, list(story.values())[0]['value'])
            self.asserEqual(child.attrib, None)

    def test_factory_single_element_02(self):
        """Factory single element with attributes test."""
        root = etree.Element('Root')
        story = {'SubRoot': {'value': 'toto', 'attr': {'a': '1', 'b': '2'}}}
        element = to_xml._factory(root=root, story=story)
        firstpass = True
        for child in element.find(list(story.keys())[0]):
            self.assertTrue(firstpass)
            firstpass = False
            self.assertEqual(child.tag, list(story.keys())[0])
            self.assertEqual(child.text, list(story.values())[0]['value'])
            self.assertEqual(child.attrib, list(story.values())[0]['attr'])

    def test_factory_single_element_03(self):
        """Factory single element with force test."""
        root = etree.Element('Root')
        # force is False, element should not be appended
        story = {'SubRoot': {'value': None}}
        element = to_xml._factory(root=root, story=story)
        self.assertIsNone(element.find(list(story.keys())[0]))
        # force is True, element should be appended
        story = {'SubRoot': {'value': None, 'force': True}}
        element = to_xml._factory(root=root, story=story)
        firstpass = True
        for child in element.find(list(story.keys())[0]):
            self.assertTrue(firstpass)
            firstpass = False
            self.assertEqual(child.tag, list(story.keys())[0])
            self.assertEqual(child.text, None)

    def test_factory_multi_element(self):
        """Factory multi element test."""
        root = etree.Element('Root')
        story = {'SubRoot': {'value': ('toto', 'tata', 'titi')}}
        element = to_xml._factory(root=root, story=story)
        passes = 0
        for child in element.findall(list(story.keys())[0]):
            passes += 1
            self.assertEqual(child.tag, list(story.keys())[0])
            self.assertTrue(child.text in list(story.values())[0]['value'])
        self.assertEqual(passes, 3)

    def test_factory_sub_story(self):
        """Factory sub story test."""
        root = etree.Element('Root')
        story = {'SubRoot': {'value': 'toto'}}
        element = to_xml._factory(root=root, story=story)
        firstpass = True
        for child in element:
            self.assertTrue(firstpass)
            firstpass = False
            self.assertEqual(child.tag, list(story.keys())[0])
            self.assertEqual(child.text, list(story.values())[0]['value'])

    def test_make_element(self):
        """Make element base test."""
        args = ('TagName', 'text', {'attr1': '1', 'attr2': '2'})
        element = to_xml._make_element(*args)
        self.assertEqual(element.tag, args[0])
        self.assertEqual(element.text, args[1])
        self.assertEqual(element.attrib, args[2])

    def test_required(self):
        """Required test."""
        obj_str = 'aaa'
        assert to_xml._required(obj_str, ['lower', 'join', 'split'])
        with self.assertRaises(ValueError):
            to_xml._required(obj_str, ['xxx'])

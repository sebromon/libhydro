# -*- coding: utf-8 -*-
"""Test program for xml.to_xml.

To run all tests just type:
    './test_conv_xml_to_xml.py' or 'python test_conv_xml_to_xml.py'

To run only a class test:
    python -m unittest test_conv_xml_to_xml.TestClass

To run only a specific test:
    python -m unittest test_conv_xml_to_xml.TestClass
    python -m unittest test_conv_xml_to_xml.TestClass.test_method

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
__version__ = """0.2a"""
__date__ = """2014-03-22"""

#HISTORY
#V0.2 - 2014-03-22
#    factorize all the base tests in a suite
#V0.1 - 2013-08-30
#    first shot

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
            l.decode(encoding).strip()
            for l in f.readlines()
            if not l.decode(encoding).lstrip().startswith('<!--')
        ]
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
                    expected=expected[i - (2 * COMPARE):i + (2 * COMPARE)]
                )
            )


#-- class TestToXmlSeuilsHydro ------------------------------------------------
# class TestToXmlSeuilsHydro(unittest.TestCase):
#
#     """ToXmlSeuilsHydro class tests."""
#
#     def setUp(self):
#"""Hook method for setting up the test fixture before exercising it."""
#         # build expected string
#         self.expected = xml_to_unicode(
#             os.path.join('data', 'xml', '1.1', 'seuilshydro_expected.xml')
#         )
#         # we have our own assertEqual function, more verbose
#         self.assertEqual = assert_unicode_equal
#
#     def test_base(self):
#         """Base test."""
#         # build objects from xml
#         # data = from_xml._parse(
#         #     os.path.join('data', 'xml', '1.1', 'seuilshydro.xml')
#         # )
#
#         # for this one we can't compare the whole 2 xmls because the seuils
#         # manipulations change their order
#
#         # for seuil in data['seuilshydro']:
#         #     if seuil.sitehydro.code =='O2000040':
#         #     # here we need to sort the seuils from 1 to 4
#
#         # ordered_seuils = []
#         # # sort the sites
#         # for codesite in (
#         #     'U2655010', 'O2000040', 'O0144020', 'O6793330', 'O3334020'
#         # ):
#         #     for seuil in data['seuilshydro']:
#         #         if seuil.sitehydro.code == codesite:
#
#         #             # here we need to sort the seuils after
#         #             # sort the seuil 1 to 4 for codesite == 'O0144020':
#         #             # here we need to sort the seuils from 1 to 4
#         #             if codesite == 'O2000040':
#         #                 break
#
#         #             # here we need to sort the stations
#         #             if codesite == 'O2000040':
#         #                 ordered_valeurs = []
#         #                 for codestation in (
#         #                     'O2000040',
#         #                     'O200004001', 'O200004002', 'O200004003'
#         #                 ):
#         #                     for valeurseuil in seuil.valeurs:
#         #                         if valeurseuil.entite.code == codestation:
#         #                             ordered_valeurs.append(valeurseuil)
#         #                             break
#         #                 seuil.valeurs = ordered_valeurs
#
#         #             ordered_seuils.append(seuil)
#         #             break
#
#         return
#         # build xml string from objects
#         # xml = etree.tostring(
#         #     to_xml._to_xml(
#         #         scenario=data['scenario'],
#         #         seuilshydro=ordered_seuils
#         #     ),
#         #     encoding='utf-8'
#         # ).decode('utf-8')
#         # # test
#         # # print(xml)
#         # self.assertEqual(xml, self.expected)


# -- class ParametrizedTestCase -----------------------------------------------
class ParametrizedTestCase(unittest.TestCase):

    """TestCase classes that want to be parametrized should inherit from this
    class."""

    # it works but lack of a precise error message.

    # source: http://eli.thegreenplace.net/2011/08/02/
    #         python-unit-testing-parametrized-test-cases/
    # see also:  https://pypi.python.org/pypi/testscenarios/

    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_class, param):
        """ Create a suite containing all tests taken from the given subclass,
        passing them the parameter 'param'."""
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        for testname in testnames:
            suite.addTest(testcase_class(testname, param=param))
        return suite


#-- class ToXmlBaseTest -------------------------------------------------------
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
        if self.param is not None:
            self.expected = xml_to_unicode(
                os.path.join(
                    'data', 'xml', '1.1', '%s_expected.xml' % self.param
                )
            )
        # set our own assertEqual function, more verbose
        self.assertEqual = assert_unicode_equal

    def test_base(self):
        """Base test."""

        # TODO discover hack - we do not want unittest.discover to run this
        #                      test directly. But it count as a real test :-(
        if self.param is None:
            self.skipTest('this test runs in a separated TestSuite')

        # build object from xml
        data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', '%s.xml' % self.param)
        )
        # build xml string from objects
        xml = etree.tostring(
            to_xml._to_xml(**{
                'scenario': data['scenario'],
                self.param: data[self.param],
                'ordered': True
            }),
            encoding='utf-8'
        ).decode('utf-8')
        # test
        # DEBUG - if self.param == 'seuilshydro': print(xml)
        self.assertEqual(
            xml,
            self.expected,
            msg='ToXMLBaseTest for unit <%s>' % self.param
        )


#-- class TestAllXmlBaseTests -------------------------------------------------
class TestAllXmlBaseTests(unittest.TestCase):
    """Run All base tests in a TestSuite.

    Required by unittest.discover.

    """
    # TODO sitesmeteo, obssmeteo, modelesprevision
    suite = unittest.TestSuite()
    for unit in (
        'siteshydro', 'seuilshydro', 'evenements', 'series', 'simulations'
    ):
        suite.addTest(
            ParametrizedTestCase.parametrize(ToXmlBaseTest, param=unit)
        )
    unittest.TextTestRunner(verbosity=1).run(suite)


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


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

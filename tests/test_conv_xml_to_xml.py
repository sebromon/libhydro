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
__version__ = """0.1c"""
__date__ = """2014-02-23"""

#HISTORY
#V0.1 - 2013-08-30
#    first shot


#-- todos ---------------------------------------------------------------------
# FIXME - factorize TestToXmlSitesHydros, ToXmlObssHydro, ToXmlSimulations


# -- config -------------------------------------------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# assert_unicode_equal function parameter
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# number of chars printed on screen to compare the 2 xml strings
# half of the value is before the error (left), the other is after (right)
# change this value if on screen comparison is to short or too long
COMPARE = 35


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

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # build expected string
        self.expected = xml_to_unicode(
            os.path.join('data', 'xml', '1.1', 'siteshydro_expected.xml')
        )
        # we have our own assertEqual function, more verbose
        self.assertEqual = assert_unicode_equal

    def test_base(self):
        """Base test."""
        # build objects from xml
        data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'siteshydro.xml')
        )
        # build xml string from objects
        xml = etree.tostring(
            to_xml._to_xml(
                scenario=data['scenario'],
                siteshydro=data['siteshydro']
            ),
            encoding='utf-8'
        ).decode('utf-8')
        # test
        self.assertEqual(xml, self.expected)


#-- class TestToXmlSitesMeteo -------------------------------------------------
#TODO


#-- class TestToXmlEvenements -------------------------------------------------
class TestToXmlEvenements(unittest.TestCase):

    """ToXmlEvenements class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # build expected string
        self.expected = xml_to_unicode(
            os.path.join('data', 'xml', '1.1', 'evenements_expected.xml')
        )
        # we have our own assertEqual function, more verbose
        self.assertEqual = assert_unicode_equal

    def test_base(self):
        """Base test."""
        # build objects from xml
        data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'evenements.xml')
        )
        # build xml string from objects
        xml = etree.tostring(
            to_xml._to_xml(
                scenario=data['scenario'],
                evenements=data['evenements']
            ),
            encoding='utf-8'
        ).decode('utf-8')
        # test
        self.assertEqual(xml, self.expected)


#-- class TestToXmlObssHydro --------------------------------------------------
class TestToXmlObssHydro(unittest.TestCase):

    """ToXmlObssHydro class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # build expected string
        self.expected = xml_to_unicode(
            os.path.join('data', 'xml', '1.1', 'obsshydro_expected.xml')
        )
        # we have our own assertEqual function, more verbose
        self.assertEqual = assert_unicode_equal

    def test_base(self):
        """Base test."""
        # build objects from xml
        data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'obsshydro.xml')
        )
        # build xml string from objects
        xml = etree.tostring(
            to_xml._to_xml(
                scenario=data['scenario'],
                series=data['series']
            ),
            encoding='utf-8'
        ).decode('utf-8')
        # test
        self.assertEqual(xml, self.expected)


#-- class TestToXmlObssMeteo --------------------------------------------------
#TODO


#-- class TestToXmlSimulations ------------------------------------------------
class TestToXmlSimulations(unittest.TestCase):

    """ToXmlSimulations class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # build expected string
        self.expected = xml_to_unicode(
            os.path.join('data', 'xml', '1.1', 'simulations_expected.xml')
        )
        # we have our own assertEqual function, more verbose
        self.assertEqual = assert_unicode_equal

    def test_base(self):
        """Base test."""
        # build object from xml
        data = from_xml._parse(
            os.path.join('data', 'xml', '1.1', 'simulations.xml')
        )
        # build xml string from objects
        xml = etree.tostring(
            to_xml._to_xml(
                scenario=data['scenario'],
                simulations=data['simulations']
            ),
            encoding='utf-8'
        ).decode('utf-8')
        # test
        self.assertEqual(xml, self.expected)


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

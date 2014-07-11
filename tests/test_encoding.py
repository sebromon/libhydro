#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test program for encoding problems.

To run all tests just type:
    './test_encoding.py' or 'python test_encoding.py'

To run only a class test:
    python -m unittest test_encoding.TestClass

To run only a specific test:
    python -m unittest test_encoding.TestClass
    python -m unittest test_encoding.TestClass.test_method

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    # !!! WE DO NOT USE the defautl unicode here !!!
    # unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys
import os
sys.path.append(os.path.join('..', '..'))

import unittest

import codecs


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin \
             <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-07-10"""

#HISTORY
#V0.1 - 2014-07-10
#    first shot


#-- class TestWrite2tty -------------------------------------------------------
class TestWrite2tty(unittest.TestCase):

    """TestWrite2tty class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # init
        self.libelle = u'Essaye ça: ℓα gαяσηηє à тσυℓσυѕє'
        self.fname = '~written_test_file_for_encoding_tests.tmp'

        # DEBUG - give some context
        # print('sys.stdout.encoding: %s' % sys.stdout.encoding)
        # import locale
        # print(
        #     'locale.getpreferredencoding: %s\n' % (
        #         locale.getpreferredencoding()
        #     )
        # )

    def tearDown(self):
        """Hook method for deconstructing the test fixture after testing it."""
        try:
            os.remove(self.fname)
        except:
            pass

    def test_regular_tty(self):
        """Print to the TTY."""
        print('\n%s' % self.libelle)

    def test_redirected_tty(self):
        """Emulate a print to a file redirected TTY."""
        #With a shell redirection, sys.stdout.encoding is None.
        #the __str__ method switch to locale.getpreferredencoding
        #and if it'd None again to 'ascii'
        with codecs.open(
            self.fname, mode='wt', encoding='ascii', errors='replace'
        ) as f:
            f.write(self.libelle)

    def test_win_tty(self):
        """Print to a windows TTY."""
        with codecs.open(
            self.fname, mode='wt', encoding='cp850', errors='replace'
        ) as f:
            f.write(self.libelle)


#-- main ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

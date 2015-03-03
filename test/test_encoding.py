# -*- coding: utf-8 -*-
"""Test program for encoding problems.

To run all tests just type:
    python -m unittest test_encoding

To run only a class test:
    python -m unittest test_encoding.TestClass

To run only a specific test:
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
sys.path.append('..')

import os
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
        # print('\n%s' % self.libelle)
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

    def test_unix_tty(self):
        """Print to a unix TTY."""
        with codecs.open(
            self.fname, mode='w', encoding='utf-8', errors='replace'
        ) as f:
            f.write(self.libelle)

    def test_windows_tty(self):
        """Print to a windows TTY."""
        with codecs.open(
            self.fname, mode='w', encoding='cp852', errors='replace'
        ) as f:
            f.write(self.libelle)

    def test_redirected_tty(self):
        """Emulate a print to a file redirected TTY."""
        #With a shell redirection, sys.stdout.encoding is None and
        #the __str__ method switch to locale.getpreferredencoding and
        #if it's None it switches again to 'ascii'
        with codecs.open(
            self.fname, mode='w', encoding='ascii', errors='replace'
        ) as f:
            f.write(self.libelle)

    def test_win_gui(self):
        """Print to a windows gui."""
        with codecs.open(
            self.fname, mode='w', encoding='cp1252', errors='replace'
        ) as f:
            f.write(self.libelle)

# -*- coding: utf-8 -*-
"""Test program for csv._to_csv converter.

To run all tests just type:
    python -m unittest test_conv_csv_to_csv

To run only a class test:
    python -m unittest test_conv_csv_to_csv.TestClass

To run only a specific test:
    python -m unittest test_conv_csv_to_csv.TestClass.test_method

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

# import csv
import unittest

from libhydro.conv import csv as lhcsv


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-12-18"""

#HISTORY
#V0.1 - 2014-12-18
#    first shot

#-- config --------------------------------------------------------------------
CSV_DIR = os.path.join('data', 'csv')


#-- class TestFromCsv ---------------------------------------------------------
class TestFromCsv(unittest.TestCase):

    """FromCsv class tests."""

    # TODO to be replaced by read and write

    def test_base(self):
        """Quick read all hydrometrie files test."""
        files = (
            # fname,            data,         encoding
            ('siteshydro_full', 'sitehydro', 'utf-8'),
            ('siteshydro_full_8859-1', 'sitehydro', 'latin1'),
            ('siteshydro_minimum', 'sitehydro', 'utf-8'),
            ('siteshydro_partial', 'sitehydro', 'utf-8'),
            # TODO sitemeteo, seriehydro, seriemeteo
        )
        for f in files:
            fname = os.path.join(CSV_DIR, '{}.csv'.format(f[0]))
            lhcsv.from_csv(fname=fname, dtype=f[1], encoding=f[2])

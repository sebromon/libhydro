# coding: utf-8
"""Module libhydro.conv._to_csv."""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import csv as _csv
import codecs as _codecs
import cStringIO as _cStringIO

# from ._config import (DIALECT, MAPPING)
# from libhydro.core import sitehydro as _sitehydro
# from libhydro.core import (sitehydro, sitemeteo, obshydro, obsmeteo)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-12-15"""

# HISTORY¬
# V0.1 - 2014-12-15¬
#   first shot¬


# -- todos --------------------------------------------------------------------
# PROGRESS - 0%


# -- init ---------------------------------------------------------------------
# the csv register_dialect deals only wtih strings :-(
# _csv.register_dialect(
#     'hydrometrie',
#     **DIALECT
# )

# TODO - reverse the mapping
#    for python 2.7+ / 3+:
#        inv_map = {v: k for k, v in map.items()}
#    in python2.7+, using map.iteritems() would be more efficient


# remove the ;
# decimal separator ,

# -- CSV encoding classes -----------------------------------------------------
class _UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=_csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = _cStringIO.StringIO()
        self.writer = _csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = _codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# -- functions ----------------------------------------------------------------
# to CSV
# write(objects, fname)
# write_siteshydro(fname)
# write_sitesmeteo(fname)
# write_serieshydro(fname)
# write_seriesmeteo(fname)

# to CSV with Pandas
# df = None
# for s in serieshydro:
#     s.observations['cdstation'] = s.entite.code
#     if df is None:
#         df = s.observations
#     else:
#         df = df.append(s.observations)
# df.to_csv('/tmp/toto')

# -*- coding: utf-8 -*-
"""Module libhydro.conv.csv.

TODO

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import csv as _csv

from ._config import (DIALECT, MAPPING)
from libhydro.core import sitehydro as _sitehydro
# from libhydro.core import (sitehydro, sitemeteo, obshydro, obsmeteo)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-12-15"""

#HISTORY¬
 #V0.1 - 2014-12-15¬
 #    first shot¬


#-- todos ---------------------------------------------------------------------
# PROGRESS - 10%


#-- init ----------------------------------------------------------------------
# the csv register_dialect deals only wtih strings :-(
_csv.register_dialect(
    'hydrometrie',
    **DIALECT
    # **{str(k): str(v) for (k, v) in DIALECT.items()}
)


#-- functions -----------------------------------------------------------------
# from CSV
# read(object, fname)

def siteshydro_from_file(
    fname,
    merge=True,
    dialect='hydrometrie',
    mappings=(MAPPING['sitehydro'], MAPPING['stationhydro']),
    *args, **kwds
):
    """TODO."""
    with open(fname, 'rb') as csvfile:
        # init the reader
        csvreader = _csv.DictReader(csvfile, dialect=dialect, *args, **kwds)

        # check fieldnames against the mapping keys
        # DEBUG - print(csvreader.fieldnames, mapping.keys())
        all_keys = set(mappings[0].keys() + mappings[1].keys())
        if not set(csvreader.fieldnames).issubset(all_keys):
            diff = set(csvreader.fieldnames) - all_keys
            raise _csv.Error(
                'unknown field{0} name{0} {1}'.format(
                    's' if len(diff) > 1 else '',
                    ', '.join(diff)
                )
            )

        # action !
        siteshydro = []
        for row in csvreader:
            # DEBUG -
            # print(
            #     {
            #         mappings[1][k]: v for k, v in row.items()
            #         if k in mappings[1].keys()
            #         if mappings[1][k] is not None
            #     }
            # )
            sitehydro = _sitehydro.Sitehydro(
                **{
                    mappings[0][k]: v for k, v in row.items()
                    if k in mappings[0].keys()
                    if mappings[0][k] is not None
                }
            )
            stationhydro = None
            if not set(csvreader.fieldnames).issubset(mappings[0].keys()):
                stationhydro = _sitehydro.Stationhydro(  # FIXME factorize
                    **{
                        mappings[1][k]: v for k, v in row.items()
                        if k in mappings[1].keys()
                        if mappings[1][k] is not None
                    }
                )
            found = False
            if merge:
                # o exp(n) !!
                for s in siteshydro:
                    if s == sitehydro:
                        found = True
                        if stationhydro is not None:
                            s.stationshydro.append(stationhydro)
                        break
            if not merge or not found:
                if stationhydro is not None:
                    sitehydro.stationshydro = [stationhydro]
                siteshydro.append(sitehydro)

        # ending
        return siteshydro

# sitesmeteo_from_file(fname)
# serieshydro_from_file(fname)
# seriesmeteo_from_file(fname)


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

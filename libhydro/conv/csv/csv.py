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
import codecs as _codecs
import cStringIO as _cStringIO

from ._config import (DIALECT, MAPPING)
from libhydro.core import sitehydro as _sitehydro
# from libhydro.core import (sitehydro, sitemeteo, obshydro, obsmeteo)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1b"""
__date__ = """2014-12-16"""

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


#-- CSV encoding decoding classes ---------------------------------------------
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = _codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=_csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = _csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter:
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


#-- functions -----------------------------------------------------------------
# from CSV
# read(object, fname)

def siteshydro_from_csv(
    fname, encoding='utf-8', dialect='hydrometrie',
    merge=True, mapping=MAPPING, **kwds
):
    """TODO."""  # TODO
    with open(fname, 'rb') as f:
        # init the reader
        csv = UnicodeReader(f=f, dialect=dialect, encoding=encoding, **kwds)
        fieldnames = csv.next()

        # parse the csv file
        siteshydro = []
        for i, row in enumerate(csv):

            # emulate the csv.DictReader
            row = dict(zip(fieldnames, row))

            # sitehydro is mandatory...
            try:
                sitehydro = _sitehydro.Sitehydro(
                    **_map_keys(row, mapping['sitehydro'], strict=False)
                )
                sitehydro.coord = _map_keys(
                    row, mapping['sitehydro.coord'], strict=False
                ) or None

            except Exception as e:
                raise _csv.Error(
                    'error line {} reading '
                    'the sitehydro, {}'.format(i + 1, e)
                )

            # ... but stationhydro is optional
            dstation = _map_keys(
                row, mapping['stationhydro'], strict=False
            ) or None
            # DEBUG -
            # print(
            # 'Line: {}\nRow: {}\nStation: {}\n'.format(i, row, dstation)
            # )
            if dstation:
                try:
                    stationhydro = _sitehydro.Stationhydro(**dstation)
                    stationhydro.coord = _map_keys(
                        row, mapping['stationhydro.coord'], strict=False
                    ) or None
                    sitehydro.stations = [stationhydro]

                except Exception as e:
                    raise _csv.Error(
                        'error line {} reading '
                        'the stationhydro, {}'.format(i + 1, e)
                    )

            siteshydro.append(sitehydro)

            # merge
            # found = False
            # if merge:
            #     # o exp(n) !!
            #     for s in siteshydro:
            #         if s == sitehydro:
            #             found = True
            #             if stationhydro is not None:
            #                 s.stationshydro.append(stationhydro)
            #             break
            # if not merge or not found:
            #     if stationhydro is not None:
            #         sitehydro.stationshydro = [stationhydro]
            #     siteshydro.append(sitehydro)

        # ending
        return siteshydro

# sitesmeteo_from_file(fname)
# serieshydro_from_file(fname)
# seriesmeteo_from_file(fname)


def _map_keys(base, mapper, strict=True, iterator='items'):
    """Return the base dictionary with mapped keys.

    Example:
        with base = {k1: v1, k2: v2, k3: '', ...}
        and mapper = {k1: kk1, k2: None, ...}
        the function returns {Kk1: v1, ...}

    If mapper[k] is None or if v is an empty string, the entry (k: v) is poped
    from the returned dict.

    Arguments:
        base (dict) = the dict to update
        mapper (dict) = a key mapping dict
        strict (bool, default True) = if mapper[k] is not found, an error is
            raised in strict mode, otherwise the entry is erased from the
            returned dict
        iterator (str in 'items', 'iteritems') = iter method

    """
    if strict:
        # strict is True
        try:
            return {
                mapper[k]: v for k, v in getattr(base, iterator)()
                if v != ''
                if mapper[k] is not None
            }
        except KeyError:
            # a fully documented error :)
            diff = set(base.keys()) - set(mapper.keys())
            raise _csv.Error(
                'unknown field{0} name{0} {1}'.format(
                    's' if len(diff) > 1 else '',
                    ', '.join(diff)
                )
            )
    else:
        # strict is False, should never raise
        return {
            mapper[k]: v for k, v in getattr(base, iterator)()
            if v != ''
            if k in mapper.keys()
            if mapper[k] is not None
        }


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

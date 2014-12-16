# -*- coding: utf-8 -*-
"""Module libhydro.conv._from_csv."""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import csv as _csv
import codecs as _codecs

from ._config import (DIALECT, MAPPING)
from libhydro.core import (sitehydro as _sitehydro, _composant_site)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1b"""
__date__ = """2014-12-16"""

#HISTORY¬
 #V0.1 - 2014-12-15¬
 #    first shot¬


#-- todos ---------------------------------------------------------------------
# PROGRESS - 25%
# TODO - read by column number


#-- init ----------------------------------------------------------------------
# CAREFUL, the csv.register_dialect deals only with strings :-( in Python2
_csv.register_dialect('hydrometrie', **DIALECT)


#-- CSV decoding classes ------------------------------------------------------
class _UTF8Recoder:

    """Iterator that reads an encoded stream and reencodes """
    """the input to UTF-8."""

    def __init__(self, f, encoding):
        self.reader = _codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class _UnicodeReader:

    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.

    """

    def __init__(self, f, dialect=_csv.excel, encoding="utf-8", **kwds):
        f = _UTF8Recoder(f, encoding)
        self.reader = _csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


#-- exposed functions ---------------------------------------------------------
def from_csv(data, fname, encoding='utf-8'):
    """Retourne les objets de type <data> contenus dans le fichier <fname>.

   Une fonction generique pour lire les CSV au format Hydrometrie. Pour decoder
   des fichiers ne respectant pas le format Hydrometrie, utiliser les fonctions
   dediees.

    Arguments:
        data (string) = siteshydro, sitesmeteo, serieshydro, seriesmeteo
        fname (string) = nom du fichier
        encoding (string, defaut 'utf-8')

     """
    return eval(
        '{}_from_csv(fname="{}", encoding="{}")'.format(
            data, fname, encoding
        )
    )


def siteshydro_from_csv(fname, encoding='utf-8', dialect='hydrometrie',
                        merge=True, mapping=MAPPING, **kwds):
    """Retourne la liste des sites hydrometriques contenus dans le fichier
    <fname>.

   Cette fonction est completement parametrable et permet de decoder facilement
   des fichiers ne respectant pas le format Hydrometrie.

    Arguments:
        fname (string) = nom du fichier
        encoding (string, defaut 'utf-8')
        dialect (csv.Dialect, defaut DIALECT) = format du CSV
        merge (bool, defaut True) = par defaut les sites identiques sont
            regroupes dans une seule entite
        mapping (dict, defaut MAPPING) = mapping header => attribut. Les
            dictionnaires de second niveau sont configurables
        **kwds = autres argument passes au csv.Reader

    """
    # parse the CSV file
    with open(fname, 'rb') as f:

        # init
        csv = _UnicodeReader(f=f, dialect=dialect, encoding=encoding, **kwds)
        fieldnames = csv.next()
        siteshydro = []

        # main loop
        for i, row in enumerate(csv):

            # emulate the csv.DictReader
            row = dict(zip(fieldnames, row))

            # DEBUG - print('\nLine: {}\nRow: {}\n'.format(i, row))

            try:
                # read the sitehydro
                # if 'sitehydro' in mapping: mandatory !
                sitehydro = _get_entity_from_row(
                    cls=_sitehydro.Sitehydro,
                    row=row,
                    mapper=mapping['sitehydro']
                )
                if 'sitehydro.coord' in mapping:
                    sitehydro.coord = _get_entity_from_row(
                        cls=_composant_site.Coord,
                        row=row,
                        mapper=mapping['sitehydro.coord']
                    )

                # read the stationhydro
                if 'stationhydro' in mapping:
                    stationhydro = _get_entity_from_row(
                        cls=_sitehydro.Stationhydro,
                        row=row,
                        mapper=mapping['stationhydro']
                    )
                    if stationhydro and 'stationhydro.coord' in mapping:
                        stationhydro.coord = _get_entity_from_row(
                            cls=_composant_site.Coord,
                            row=row,
                            mapper=mapping['stationhydro.coord']
                        )
                    sitehydro.stations = stationhydro

            except Exception as e:
                raise _csv.Error(
                    'error in line {}, {}'.format(i + 1, e)
                )

            # add the sitehydro to the list
            siteshydro.append(sitehydro)

    # ending
    if not merge:
        return siteshydro
    else:
        return _merge_siteshydro(siteshydro)


def sitesmeteo_from_csv(fname):
    raise NotImplementedError


def serieshydro_from_csv(fname):
    raise NotImplementedError


def seriesmeteo_from_csv(fname):
    raise NotImplementedError


#-- private functions ---------------------------------------------------------
def _merge_siteshydro(siteshydro):
    """Merge site siteshydro.

    This merge is O(n2) !!.

    """
    mergedsites = []
    for sitehydro in siteshydro:
        for mergedsite in mergedsites:
            if sitehydro.__eq__(mergedsite, ignore=['_stations']):
                mergedsite.stations.extend(sitehydro.stations)
                break
        else:  # we have a new sitehydro here
            mergedsites.append(sitehydro)
    return mergedsites


def _get_entity_from_row(cls, row, mapper):
    """.
    """
    try:
        args = _map_keys(base=row, mapper=mapper, strict=False)
        if args:
            return cls(**args)
        # else (args is None): return None

    except Exception:
        raise _csv.Error(
            # "can't find a suitable {}, {}".format(cls.__name__.lower(), e)
            "can't find a suitable {}".format(cls.__name__.lower())
        )


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

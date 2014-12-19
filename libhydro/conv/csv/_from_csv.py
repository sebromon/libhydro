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
import functools as _functools

from ._config import (FLAG, SECOND_LINE, DECIMAL_POINT, MAPPER)
import libhydro.core


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2a"""
__date__ = """2014-12-19"""

#HISTORY¬
 #V0.1 - 2014-12-15¬
 #    first shot¬


#-- todos ---------------------------------------------------------------------
# PROGRESS - 50%
# TODO - read by column number
# TODO - write a Reader class and a Sniffer


#-- config --------------------------------------------------------------------
# datatype: (class, child class)
DTYPE = {
    'sitehydro': (
        libhydro.core.sitehydro.Sitehydro, libhydro.core.sitehydro.Station
    ),
    'sitemeteo': (
        libhydro.core.sitemeteo.Sitemeteo,  libhydro.core.sitemeteo.Grandeur
    )

}
# Sort of ugly but we need to cast numbers using a locale DECIMAL separator,
# and it's not easy to find which
FLOAT_ATTRS = ('x', 'y')


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


#-- main functions ------------------------------------------------------------
def from_csv(dtype, fname, encoding='utf-8'):
    """Retourne les objets de type <dtype> contenus dans le fichier CSV
    <fname>.

   C'est une fonction generique pour lire les fichier au format Hydrometrie.

   Pour decoder des fichiers ne respectant pas ce format, utiliser les
   fonctions specifiques a chaque type de donnees.

    Arguments:
        dtype (string) = sitehydro, sitemeteo, seriehydro, seriemeteo
        fname (string) = nom du fichier
        encoding (string, defaut 'utf-8')

     """
    # TODO - could be a sniffer
    return eval(
        '{}_from_csv(fname="{}", encoding="{}")'.format(
            dtype.replace('site', 'sites').replace('serie', 'series'),
            fname,
            encoding
        )
    )


FROM_CSV_DOC = """\
Retourne la liste des {} contenus dans le fichier CSV <fname>.

Cette fonction est completement parametrable et permet de decoder des fichiers
ne respectant pas le format Hydrometrie, en lui passant la configuration
appropriee.

Arguments:
    fname (string) = nom du fichier
    encoding (string, defaut 'utf-8')
    merge (bool, defaut True) = par defaut les sites identiques sont
        regroupes dans une seule entite
    dialect (csv.Dialect, defaut 'hydrometrie') = format du CSV
    flag (dict, defaut FLAG)
    second_line (bool, defaut SECOND_LINE)
    decimal (char, defaut DECIMAL_POINT)
    mapper (dict, defaut MAPPER) = mapping header => attribut. Les
        dictionnaires de second niveau sont configurables
    **kwds = autres argument passes au csv.Reader

"""


def sites_from_csv(fname, dtype, merge=True, encoding='utf-8',
                   dialect='hydrometrie',
                   flag=FLAG, second_line=SECOND_LINE, decimal=DECIMAL_POINT,
                   mapper=MAPPER, **kwds):
    """Return the <dtype> entities in the CSV file <fname>.

    Generic function for 'siteshydro' and 'sitesmeteo'.

    Args:
        dtype (string in 'sitehydro', 'sitemeteo')

    The other args are described in the _FROM_CSV_DOCSTRING

    """
    # init
    if dtype not in DTYPE:
        raise ValueError('dtype should be in {}'.format(DTYPE.keys()))
    # parse the CSV file
    with open(fname, 'rb') as f:

        # init
        csv = _UnicodeReader(f=f, dialect=dialect, encoding=encoding, **kwds)
        sites = []

        # fieldnames
        fieldnames = csv.next()
        if flag and not flag['header'] == fieldnames.pop():
            raise _csv.Error('header flag not found')

        # second line
        if second_line:
            csv.next()

        # main loop
        for i, row in enumerate(csv):
            # DEBUG - print('\nLine: {}\nRow: {}\n'.format(i, row))
            try:
                # check the flag
                if flag and not flag['row'] == row.pop():
                    raise _csv.Error('flag not found')
                # emulate the csv.DictReader
                row = dict(zip(fieldnames, row))
                # append the site
                sites.append(
                    site_from_row(
                        dtype=dtype, row=row, mapper=mapper, decimal=decimal
                    )
                )
            except Exception as e:
                raise _csv.Error(
                    'error in line {}, {}'.format(i + 1, e)
                )

    # ending
    if not merge or sites is None or sites == []:
        return sites
    else:
        return merge_sites(sites=sites)


siteshydro_from_csv = _functools.partial(sites_from_csv, dtype='sitehydro')
siteshydro_from_csv.__doc__ = FROM_CSV_DOC.format('sites hydrometriques')
sitesmeteo_from_csv = _functools.partial(sites_from_csv, dtype='sitemeteo')
sitesmeteo_from_csv.__doc__ = FROM_CSV_DOC.format('sites meteorologiques')


def serieshydro_from_csv(fname):
    raise NotImplementedError


def seriesmeteo_from_csv(fname):
    raise NotImplementedError


#-- secondary functions -------------------------------------------------------
def merge_sites(sites):
    """Merge a list of sites.

    This merge is O(n2) !!.

    """
    # pre-condition
    if sites is None:
        return

    # init
    # dtype is 'sitehydro' or 'sitemeteo'
    dtype = sites[0].__class__.__name__.lower()
    # childtype is 'stations' or 'grandeurs'
    childtype = '{}s'.format(DTYPE[dtype][1].__name__.lower())
    mergedsites = []

    # action
    for site in sites:
        for mergedsite in mergedsites:
            if site.__eq__(mergedsite, ignore=[childtype]):
                getattr(mergedsite, childtype).extend(
                    getattr(site, childtype)
                )
                break
        else:  # we have a new site here
            mergedsites.append(site)

    # return
    return mergedsites


def site_from_row(dtype, row, mapper, decimal=None):
    """Return a Site object from a row.

    Arguments:
        dtype (string in 'sitehydro', 'sitemeteo')
        row (dict) = {fieldname: value, ...}
        mapper (dict, defaut MAPPER) = mapping header => attribut. Les
            dictionnaires de second niveau sont configurables
        decimal (char, defaut DECIMAL_POINT)

    """
    # map the string dtype in a class
    try:
        site_cls = DTYPE[dtype][0]
        site_cls_name = '{}.{}'.format(
            site_cls.__module__, site_cls.__name__
        )
        child_cls = DTYPE[dtype][1]
        child_cls_name = '{}.{}'.format(
            child_cls.__module__, child_cls.__name__
        )
    except Exception as e:
        raise ValueError(
            "error while computing class names, {}".format(e)
        )

    # read the mandatory parent entity (site)
    site = entity_from_row(
        cls=site_cls,
        row=row,
        mapper=mapper[site_cls_name],
        decimal=decimal
    )
    if '{}.coord'.format(site_cls_name) in mapper:
        site.coord = entity_from_row(
            cls=libhydro.core._composant_site.Coord,
            row=row,
            mapper=mapper['{}.coord'.format(site_cls_name)],
            decimal=decimal
        )

    # read the child entity (station or grandeur)
    if child_cls_name in mapper:
        child = entity_from_row(
            cls=child_cls,
            row=row,
            mapper=mapper[child_cls_name],
            decimal=decimal
        )
        if child and '{}.coord'.format(child_cls_name) in mapper:
            child.coord = entity_from_row(
                cls=libhydro.core._composant_site.Coord,
                row=row,
                mapper=mapper['{}.coord'.format(child_cls_name)],
                decimal=decimal
            )
        # join the child to his father
        setattr(site, '{}s'.format(child_cls.__name__.lower()), child)

    # get out
    return site


def entity_from_row(cls, row, mapper, strict=False,
                    decimal=None, floats_attrs=FLOAT_ATTRS):
    """Return an object of class 'cls" from the 'row' values 'mapped' with the
    mapper.

    Arguments:
        cls (cls)
        row (dict)    |
        mapper (dict) | passed to the map_keys function
        strict (bool) |
        decimal (char) = decimal point |
        floats_attrs (list of strings) | = attributes to cast in float

    """
    try:
        args = map_keys(base=row, mapper=mapper, strict=strict)
        if args:
            # cast float_attrs to float
            if decimal and floats_attrs:
                for arg in set(args).intersection(set(floats_attrs)):
                    args[arg] = float(args[arg].replace(decimal, '.'))
            # instantiate and return the object
            return cls(**args)
        # else (args is None): return None

    except Exception as e:
        raise _csv.Error(
            "can't find a suitable {} ({})".format(
                cls.__name__.capitalize(),
                e
            )
        )


def map_keys(base, mapper, strict=True, iterator='items'):
    """Return the base dictionary with mapped keys.

    Example:
        with base = {k1: v1, k2: v2, k3: '', ...}
        and mapper = {k1: kk1, k2: None, ...}
        the function returns {Kk1: v1, ...}

    If mapper[k] is None or if v is an empty string, the entry (k: v) is popped
    from the returned dict, which can be empty.

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

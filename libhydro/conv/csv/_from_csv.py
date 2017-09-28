# coding: utf-8
"""Module libhydro.conv._from_csv."""
# -- imports ------------------------------------------------------------------
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


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.5a"""
__date__ = """2015-06-11"""

# HISTORY¬
# V0.5 - 2014-12-29¬
#   add the seriesmeteo reader
# V0.4 - 2014-12-20¬
#   add the serieshydro reader
# V0.1 - 2014-12-15¬
#   first shot¬


# -- todos --------------------------------------------------------------------
# PROGRESS - 80% - working but needs a big refactoring
# TODO - write a Reader class and a Sniffer
# TODO - read by column number
# TODO - write an __iter__ method


# -- config -------------------------------------------------------------------
# datatype: (class, child class)
DTYPE = {
    'sitehydro': (
        libhydro.core.sitehydro.Sitehydro,
        libhydro.core.sitehydro.Station
    ),
    'sitemeteo': (
        libhydro.core.sitemeteo.Sitemeteo,
        libhydro.core.sitemeteo.Grandeur
    ),
    'seriehydro': (
        libhydro.core.obshydro.Serie,
        libhydro.core.obshydro.Observation
    ),
    'seriemeteo': (
        libhydro.core.obsmeteo.Serie,
        libhydro.core.obsmeteo.Observation
    ),
}


# -- CSV decoding classes -----------------------------------------------------
class _UTF8Recoder:

    """Iterator that reads an encoded stream and reencodes """
    """the input to UTF-8."""

    def __init__(self, f, encoding):
        self.reader = _codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def __next__(self):
        line = self.reader.readline()
        if len(line) == 0:
            raise StopIteration
        return line
        #return self.reader.next().encode("utf-8")


class _UnicodeReader:

    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.

    """

    def __init__(self, f, dialect=_csv.excel, encoding="utf-8", **kwds):
        f = _UTF8Recoder(f, encoding)
        self.reader = _csv.reader(f, dialect=dialect, **kwds)

    def __next__(self):
        row = next(self.reader)
        return row
        #return [str(s, "utf-8") for s in row]

    def __iter__(self):
        return self


# -- main functions -----------------------------------------------------------
# FIXME - this one should be a sniffer
# class Sniffer(fname, encoding='utf-8'):
#     pass
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
    return eval(
        '{}_from_csv(fname="{}", encoding="{}")'.format(
            dtype.replace('site', 'sites').replace('serie', 'series'),
            fname,
            encoding
        )
    )


# FIXME  update docstring
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

# FIXME - this one should be the Reader and exposed with the dtype arg
#   class Reader():
#       pass


def parse_csv(fname, encoding='utf-8', dialect='hydrometrie',
              merge=True, mapper=MAPPER, flag=FLAG, second_line=SECOND_LINE,
              decimal=DECIMAL_POINT, dtype=None, **kwds):
    """Parse the CSV <fname> and return a collection of <dtype> entities.

    It is a generic function to encapsulate the file logic.

    Args:
        dtype (string in 'sitehydro', 'sitemeteo')

    The other args are described in the _FROM_CSV_DOCSTRING

    """
    # init
    if dtype not in DTYPE:
        raise ValueError('dtype should be in {}'.format(list(DTYPE.keys())))

    # parse the CSV file
    with open(fname, 'rb') as f:
    #with open(fname, newline='') as f:
        # init
        csv = _UnicodeReader(f=f, dialect=dialect, encoding=encoding, **kwds)
        collection = []

        # fieldnames
        fieldnames = next(csv)
        if flag and not flag['header'] == fieldnames.pop():
            raise _csv.Error('header flag not found')

        # second line
        if second_line:
            next(csv)

        # main loop
        for i, row in enumerate(csv):
            # DEBUG - print('\nLine: {}\nRow: {}\n'.format(i, row))
            try:
                # check the flag
                if flag and not flag['row'] == row.pop():
                    raise _csv.Error('flag not found')
                # emulate the csv.DictReader
                row = dict(list(zip(fieldnames, row)))
                # append the row item
                # calling 'site_from_row' or 'serie_from_row'
                collection.append(
                    eval(
                        '{}_from_row('
                        'dtype=dtype, row=row, mapper=mapper,'
                        'decimal=decimal'
                        ')'.format(
                            dtype.replace('hydro', '').replace('meteo', '')
                        )
                    )
                )
            except Exception as e:
                raise _csv.Error(
                    'error in line {}, {}'.format(i + 1, e)
                )

    # ending
    if not merge or collection is None or collection == []:
        return collection
    else:
        return merge_collection(collection=collection, dtype=dtype)


# FIXME - not useful. We could expose only a SimpleReader, a sniffer for sandre
# csv and a full Reader(dtype, ...)
siteshydro_from_csv = _functools.partial(parse_csv, dtype='sitehydro')
siteshydro_from_csv.__doc__ = FROM_CSV_DOC.format('sites hydrometriques')
sitesmeteo_from_csv = _functools.partial(parse_csv, dtype='sitemeteo')
sitesmeteo_from_csv.__doc__ = FROM_CSV_DOC.format('sites meteorologiques')
serieshydro_from_csv = _functools.partial(parse_csv, dtype='seriehydro')
serieshydro_from_csv.__doc__ = FROM_CSV_DOC.format('series hydrometriques')
seriesmeteo_from_csv = _functools.partial(parse_csv, dtype='seriemeteo')
seriesmeteo_from_csv.__doc__ = FROM_CSV_DOC.format('series meteorologiques')


# -- secondary functions ------------------------------------------------------
def merge_collection(collection, dtype):
    """Merge a collection of dtype objects.

    This merge is O(n2) !!.

    """
    # pre-condition
    if collection is None:
        return

    # childtype is 'stations' or 'grandeurs'
    child_name = '{}s'.format(DTYPE[dtype][1].__name__.lower())
    mergedcollection = []

    # action
    for item in collection:
        for mergeditem in mergedcollection:
            if item.__eq__(mergeditem, ignore=[child_name]):
                if dtype[:4] == 'site':
                    # we have a list to extend
                    getattr(mergeditem, child_name).extend(
                        getattr(item, child_name)
                    )
                else:
                    # we have a DataFrame to concat
                    setattr(
                        mergeditem,
                        child_name,
                        libhydro.core.obshydro.Observations.concat((
                            getattr(mergeditem, child_name),
                            getattr(item, child_name)
                        ))
                    )
                break
        else:  # we have a new item here
            mergedcollection.append(item)

    # return
    return mergedcollection


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
            "error while computing class name, {}".format(e)
        )

    # read the mandatory parent entity (site)
    site = object_from_row(
        cls=site_cls,
        row=row,
        mapper=mapper[site_cls_name],
        decimal=decimal
    )
    if '{}.coord'.format(site_cls_name) in mapper:
        site.coord = object_from_row(
            cls=libhydro.core._composant_site.Coord,
            row=row,
            mapper=mapper['{}.coord'.format(site_cls_name)],
            decimal=decimal
        )

    # read the child entity (station or grandeur)
    if child_cls_name in mapper:
        child = object_from_row(
            cls=child_cls,
            row=row,
            mapper=mapper[child_cls_name],
            decimal=decimal
        )
        if child and '{}.coord'.format(child_cls_name) in mapper:
            child.coord = object_from_row(
                cls=libhydro.core._composant_site.Coord,
                row=row,
                mapper=mapper['{}.coord'.format(child_cls_name)],
                decimal=decimal
            )
        # join the child to his father
        setattr(site, '{}s'.format(child_cls.__name__.lower()), child)

    # get out
    return site


def serie_from_row(dtype, row, mapper, decimal=None):
    """Return a Serie object from a row.

    Arguments:
        dtype (string in 'seriehydro', 'seriemeteo')
        row (dict) = {fieldname: value, ...}
        mapper (dict, defaut MAPPER) = mapping header => attribut. Les
            dictionnaires de second niveau sont configurables
        decimal (char, defaut DECIMAL_POINT)

    """
    # map the string dtype in a class
    try:
        serie_cls = DTYPE[dtype][0]
        serie_cls_name = '{}.{}'.format(
            serie_cls.__module__, serie_cls.__name__
        )
        obs_cls = DTYPE[dtype][1]
        obs_cls_name = '{}.{}'.format(
            obs_cls.__module__, obs_cls.__name__
        )
        obss_cls_name = '{}s'.format(obs_cls_name)
    except Exception as e:
        raise ValueError(
            "error while computing class name, {}".format(e)
        )

    # get the entity and add it to the row and the mapper
    if dtype == 'seriehydro':
        try:
            entity = object_from_row(
                cls=libhydro.core.sitehydro.Station,
                row=row,
                mapper=mapper['{}.entite_station'.format(serie_cls_name)],
                decimal=decimal
            )
            if entity is None:
                raise Exception
        except Exception:
            entity = object_from_row(
                cls=libhydro.core.sitehydro.Sitehydro,
                row=row,
                mapper=mapper['{}.entite_sitehydro'.format(serie_cls_name)],
                decimal=decimal
            )
        row['entite'] = entity  # FIXME - check if key exists already
        serie_mapper = mapper[serie_cls_name].copy()
        serie_mapper.update({'entite': 'entite'})  # FIXME check too

    else:  # seriemeteo
        sitemeteo = object_from_row(
            cls=libhydro.core.sitemeteo.Sitemeteo,
            row=row,
            mapper=mapper['{}.grandeur.sitemeteo'.format(serie_cls_name)]
        )
        row['sitemeteo'] = sitemeteo
        grandeur_mapper = mapper['{}.grandeur'.format(serie_cls_name)].copy()
        grandeur_mapper.update({'sitemeteo': 'sitemeteo'})
        grandeur = object_from_row(
            cls=libhydro.core.sitemeteo.Grandeur,
            row=row,
            mapper=grandeur_mapper,
            decimal=decimal
        )
        row['grandeur'] = grandeur  # FIXME - check if key exists already
        serie_mapper = mapper[serie_cls_name].copy()
        serie_mapper.update({'grandeur': 'grandeur'})  # FIXME check too

    # build the serie
    serie = object_from_row(
        cls=serie_cls,
        row=row,
        mapper=serie_mapper,
        decimal=decimal
    )

    # build and add the obs
    obs = object_from_row(
        cls=obs_cls,
        row=row,
        mapper=mapper[obs_cls_name],
        decimal=decimal
    )
    serie.observations = eval('{}'.format(obss_cls_name))(obs)

    # return
    return serie


def object_from_row(cls, row, mapper, strict=False, decimal=None):
    """Return an object of class 'cls" from the 'row' values 'mapped' with the
    mapper.

    Arguments:
        cls (cls)
        row (dict)    |
        mapper (dict) | passed to the map_keys function
        strict (bool) |
        decimal (char) = decimal point

    """
    # ugly but we need to cast dates or numbers using a locale DECIMAL
    # separator, and it's not easy to find which
    FLOAT_ATTRS = set(['x', 'y', 'res'])
    DATE_ATTRS = set(['dte'])

    try:
        args = map_keys(base=row, mapper=mapper, strict=strict)
        if args:
            # cast float_attrs to floats
            if decimal:
                for arg in set(args).intersection(FLOAT_ATTRS):
                    args[arg] = float(args[arg].replace(decimal, '.'))
            # cast date_attrs to dates
            for arg in set(args).intersection(DATE_ATTRS):
                args[arg] = datefstr(args[arg])
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
        iterator (str = 'items') = iter method
                                   python2 iterator can be iteritems 
    """
    # Python3  object has no attribute 'iteritem
    # so iterator = 'items'
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
            if k in list(mapper.keys())
            if mapper[k] is not None
        }


def datefstr(date):
    """Return 'AAAA-MM-JJ hh:mm:ss' from 'JJ/MM/AAAA hh:mm:ss'."""
    if '/' not in date:
        return date
    try:
        d, h = date.split()
        return '{} {}'.format('-'.join(d.split('/')[::-1]), h)
    except Exception as e:
        raise ValueError("'{}' is not a valid date, {} ".format(date, e))

# -*- coding: utf-8 -*-
"""Module simulation.

Ce module contient les classes:
    # Prevision
    # Simulation

On peux aussi utiliser directement les classes de la librairie Pandas, les
Series ou les DataFrame.

Exemple pour instancier une Series:
    datas = pandas.Series(
        data = [100, 110, 120],
        index = [
            datetime.datetime(2012, 5, 1),
            datetime.datetime(2012, 5, 2),
            datetime.datetime(2012, 5, 3)
        ]
        dtype = None,
        name='previsions de debit'
)

Exemple pour instancier un DataFrame:
    hauteurs = pandas.DataFrame({
        'H2354310': Series_de_hauteurs_1,
        'H4238907': Series_de_hauteurs_2,
        ...
    })

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import numpy as _np
# import pandas as _pd

# from .nomenclature import NOMENCLATURE as _NOMENCLATURE
# from . import sitehydro as _sitehydro


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1a"""
__date__ = """2013-08-07"""

#HISTORY
#V0.1 - 2013-08-07
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - many properties


#-- class Simulation ----------------------------------------------------------
class Simulation(object):
    """
    grandeur
    dtprod
    qualite
    statut
    publication
    commentaire
    modeleprevision
    entite

    previsions

    """

    # sysalti
    # responsable
    # refalti
    # courbetarage

    # TODO
    pass


#-- class Prevision -----------------------------------------------------------
class Prevision(_np.ndarray):
    """Classe prevision.

    Classe pour manipuler une prevision elementaire.

    Subclasse de numpy.array('dte', 'res', 'prb'), les elements etant du
    type DTYPE.

    Date et resultat sont obligatoires, la probabilite vaut 50 par defaut.

    L'implementation differe de celle du modele de donnees car on utilise une
    seule classe pour les previsions deterministes (min ,moy et max) et les
    previsions probabilistes (probabilite + valeur) en applicant la regle:
        # la valeur min est celle de probabilite 0
        # la valeur moyenne est celle de probabilite 50
        # la valeur maximum est celle de probabilite 100

    Proprietes:
        dte (numpy.datetime64 ou string) = date UTC de la prevision au format
            ISO 8601, arrondie a la seconde. A l'initialisation si le fuseau
            horaire n'est pas precise, la date est consideree en heure locale.
            Pour forcer la sasie d'une date UTC utiliser le fuseau +00:
                np.datetime64('2000-01-01T09:28:00+00')
        res (numpy.float) = resultat
        prb (numpy.int entre 0 et 100, defaut 50) = probabilite du resultat

    """

    DTYPE = _np.dtype([
        (str('dte'), _np.datetime64(None, str('s'))),
        (str('res'), _np.float),
        (str('prb'), _np.int8)
    ])

    def __new__(cls, dte, res, prb=50):
        if not isinstance(dte, _np.datetime64):
            dte = _np.datetime64(dte)
        try:
            prb = int(prb)
            if (prb < 0) or (prb > 100):
                raise ValueError('probabilite incorrecte')
        except Exception:
            raise
        obj = _np.array(
            (dte, res, prb),
            dtype=Prevision.DTYPE
        ).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

    def __str__(self):
        """String representation."""
        return '{0} avec une probabilite de {1}% pour le {2} a {3} UTC'.format(
            self['res'].item(),
            self['prb'].item(),
            *self['dte'].item().isoformat().split('T')
        ).encode('utf-8')

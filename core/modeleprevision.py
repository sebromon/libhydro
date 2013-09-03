# -*- coding: utf-8 -*-
"""Module modeleprevision.

Ce module contient une seule classe:
    #Modeleprevision

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys as _sys

from .nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1c"""
__date__ = """2013-09-03"""

#HISTORY
#V0.1 - 2013-08-06
#    first shot


#-- todos ---------------------------------------------------------------------


# -- config -------------------------------------------------------------------


#-- class Sitehydro -----------------------------------------------------------
class Modeleprevision(object):
    """Class Modeleprevision.

    Classe pour manipuler les modeles numeriques de prevision.

    Proprietes:
        code (string <= 10) =
        libelle (string)
        typemodele (integer parmi NOMENCLATURE[525])
        description (string)

    """

    #dtmaj
    #auteur

    def __init__(
        self, code=None, libelle=None, typemodele=0, description=None,
        strict=True
    ):
        """Initialisation.

        Arguments:
            code (string <= 10)
            libelle (string)
            typemodele (integer parmi NOMENCLATURE[525], defaut 0)
            description (string)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du code et du type de modele

        """

        # -- simple properties --
        self._strict = strict
        self.libelle = unicode(libelle) if (libelle is not None) else None
        self.description = unicode(description) if \
            (description is not None) else None

        # -- full properties --
        self.code = code
        self.typemodele = typemodele

    # -- property code --
    @property
    def code(self):
        """Code hydro."""
        return self._code

    @code.setter
    def code(self, code):
        try:
            if code is not None:
                code = unicode(code)
                if (self._strict and (len(code) > 10)):
                    raise ValueError('code incorrect')
            self._code = code
        except:
            raise

    # -- property typemodele --
    @property
    def typemodele(self):
        """Type de modele."""
        return self._typemodele

    @typemodele.setter
    def typemodele(self, typemodele):
        try:
            if typemodele is not None:
                typemodele = int(typemodele)
                if (self._strict) and (typemodele not in _NOMENCLATURE[525]):
                    raise ValueError('typemodele incorrect')
            self._typemodele = typemodele
        except:
            raise

    # -- other methods --
    def __unicode__(self):
        """Unicode representation."""
        return 'Modele de type {0} {1}::{2}\nDescription: {3}'.format(
            self.typemodele or '<inconnu>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            self.description or '<sans description>'
        )

    def __str__(self):
        """String representation."""
        if _sys.version_info[0] >= 3:  # Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode('utf8')

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

from . import _composant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.8d"""
__date__ = """2014-12-17"""

#HISTORY
#V0.8 - 2014-03-02
#    use descriptors
#V0.1 - 2013-08-06
#    first shot


#-- todos ---------------------------------------------------------------------
# PROGRESS - Modeleprevision 80%


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

    # Modeleprevision other properties

    #dtmaj
    #auteur

    typemodele = _composant.Nomenclatureitem(nomenclature=525, required=False)

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
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(self.__class__)['typemodele'].strict = self._strict
        self.libelle = unicode(libelle) if (libelle is not None) else None
        self.description = unicode(description) if \
            (description is not None) else None

        # -- descriptors --
        self.typemodele = typemodele

        # -- full properties --
        self._code = None
        self.code = code

    # -- property code --
    @property
    def code(self):
        """Return code hydro."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code hydro."""
        try:
            if code is not None:
                code = unicode(code)
                if (self._strict and (len(code) > 10)):
                    raise ValueError('code incorrect')
            self._code = code
        except:
            raise

    # -- special methods --
    __all__attrs__ = (
        'code', 'libelle', 'typemodel', 'description'
    )
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__

    def __unicode__(self):
        """Return unicode representation."""
        return 'Modele de type {0} {1}::{2}\nDescription: {3}'.format(
            self.typemodele or '<inconnu>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            self.description or '<sans description>'
        )

    __str__ = _composant.__str__

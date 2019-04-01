# coding: utf-8
"""Module modeleprevision.

Ce module contient une seule classe:
    #Modeleprevision

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from . import _composant
from libhydro.core import intervenant as _intervenant, sitehydro as _sitehydro

# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.8d"""
__date__ = """2015-10-30"""

# HISTORY
# V0.8 - 2014-03-02
#   use descriptors
# V0.1 - 2013-08-06
#   first shot

# -- todos --------------------------------------------------------------------
# PROGRESS - Modeleprevision 80%


# -- class Sitehydro ----------------------------------------------------------
class Modeleprevision(object):

    """Class Modeleprevision.

    Classe pour manipuler les modeles numeriques de prevision.

    Proprietes:
        code (string <= 10) = code modèle
        libelle (string) = libellé du modèle
        typemodele (integer parmi NOMENCLATURE[525]) = type de modèle
        description (string) = description
        contact (_intervenant.Contact or None) = contact
        dtmaj (datetime.datetime or None) = date de mise à jour
        siteshydro (iterable of _sitehydro.Sitehydro) = sites hydro

    """

    typemodele = _composant.Nomenclatureitem(nomenclature=525, required=False)
    dtmaj = _composant.Datefromeverything(required=False)

    def __init__(
        self, code=None, libelle=None, typemodele=0, description=None,
        contact=None, dtmaj=None, siteshydro=None, strict=True
    ):
        """Initialisation.

        Arguments:
            code (string <= 10) = code modèle
            libelle (string) = libellé du modèle
            typemodele (integer parmi NOMENCLATURE[525]) = type de modèle
            description (string) = description
            contact (_intervenant.Contact or None) = contact
            dtmaj (datetime.datetime or None) = date de mise à jour
            siteshydro (iterable of _sitehydro.Sitehydro) = sites hydro
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite du code et du type de modele

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(Modeleprevision)['typemodele'].strict = self._strict
        self.libelle = str(libelle) if (libelle is not None) else None
        self.description = str(description) if \
            (description is not None) else None

        # -- descriptors --
        self.typemodele = typemodele
        self.dtmaj = dtmaj

        # -- full properties --
        self._code = None
        self.code = code
        self._contact = None
        self.contact = contact
        self._siteshydro = []
        self.siteshydro=siteshydro


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
                code = str(code)
                if (self._strict and (len(code) > 10)):
                    raise ValueError('code incorrect')
            self._code = code
        except:
            raise

    # -- property contact --
    @property
    def contact(self):
        """Return contact hydro."""
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Set contact hydro."""
        if contact is not None:
            if not isinstance(contact, _intervenant.Contact):
                raise TypeError(
                    'contact must be an instance of intervenant.Contact')
        self._contact = contact

    # -- property siteshydro --
    @property
    def siteshydro(self):
        """Return siteshydro hydro."""
        return self._siteshydro

    @siteshydro.setter
    def siteshydro(self, siteshydro):
        """Set siteshydro hydro."""
        self._siteshydro = []
        if siteshydro is None:
            return
        if isinstance(siteshydro, _sitehydro.Sitehydro):
            siteshydro = [siteshydro]
        for sitehydro in siteshydro:
            if not isinstance(sitehydro, _sitehydro.Sitehydro):
                raise TypeError(
                    'siteshydro must be a _sitehydro.Sitehydro'
                    ' or an iterable of _sitehydro.Sitehydro')
            self._siteshydro.append(sitehydro)

    # -- special methods --
    __all__attrs__ = (
        'code', 'libelle', 'typemodele', 'description', 'contact', 'dtmaj',
        'siteshydro'
    )
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        return 'Modele de type {0} {1}::{2}\nDescription: {3}'.format(
            self.typemodele or '<inconnu>',
            self.code or '<sans code>',
            self.libelle or '<sans libelle>',
            self.description or '<sans description>'
        )

    __str__ = _composant.__str__

# coding: utf-8
"""Module evenement.

Ce module contient la classe:
    # Evenement

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime
import collections as _collections

from . import (_composant, sitehydro as _sitehydro, sitemeteo as _sitemeteo)


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """1.0f"""
__date__ = """2015-10-30"""

# HISTORY
# V1.0 - 2014-03-02
#   use descriptors
# V0.1 - 2013-11-26
#   first shot

# -- todos --------------------------------------------------------------------
# PROGRESS - Evenement 100%

# Namedtuple permettant de manipuler des ressources
# associées à un évènement
Ressource = _collections.namedtuple('Ressource', ['url', 'libelle'])


# -- class Evenement ----------------------------------------------------------
class Evenement(object):

    """Classe Evenement.

    Classe pour manipuler des evenements.

    Proprietes:
        entite (sitehydro.Sitehydro ou sitehydro.Station ou
            sitemeteo.Sitemeteo) = entite concernee par l'evenement
        descriptif (string)
        contact (intervenant.Contact) = contact proprietaire de l'evenement
        dt (datetime.datetime) = date de l'evenement
        publication (entier parmi NOMENCLATURE[534]) = type de publication
        dtmaj (datetime.datetime ou None) = date de mise a jour
        typeevt (entier parmi NOMENCLATURE[891]) = type de l'évènement
        ressources (iterable of evenement.Ressource) = ressources associées
            à l'évènement
        dtfin (datetime.datetime ou None) = date de fin
    """

    dt = _composant.Datefromeverything(required=False)
    # publication = _composant.Nomenclatureitem(nomenclature=534)
    publication = _composant.Nomenclatureitem(nomenclature=874)
    typeevt = _composant.Nomenclatureitem(nomenclature=891)
    dtmaj = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)

    def __init__(
        self, entite, descriptif, contact,
        dt=_datetime.datetime.utcnow(), publication=0,
        dtmaj=_datetime.datetime.utcnow(), typeevt=0, ressources=None,
        dtfin=None, strict=True
    ):
        """Initialisation.

        Arguments:
            entite (sitehydro.Sitehydro ou sitehydro.Station ou
                sitemeteo.Sitemeteo) = entite concernee par l'evenement
            descriptif (string)
            contact (intervenant.Contact) = contact proprietaire de l'evenement
            dt (numpy.datetime64 string, datetime.datetime...) =
                date de l'evenement
            publication (entier parmi NOMENCLATURE[534]) = type de publication
            dtmaj (numpy.datetime64 string, datetime.datetime...) =
                date de mise a jour
            typeevt (entier parmi NOMENCLATURE[891]) = type de l'évènement
            ressources (iterable of evenement.Ressource) = ressources associées
                à l'évènement
            dtfin (datetime.datetime ou None) = date de fin
            strict (bool, defaut True) = en mode permissif le type de
                publication n'est pas controle et les proprietes obligatoires
                sont facultatives

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(Evenement)['publication'].strict = self._strict

        # -- descriptors --
        self.dt = dt
        self.publication = publication
        self.dtmaj = dtmaj
        self.typeevt = typeevt
        self.dtfin = dtfin

        # -- full properties --
        self._entite = self._descriptif = self._contact = None
        self.entite = entite
        self.descriptif = descriptif
        self.contact = contact

        self._ressources = None
        self.ressources = ressources

    # -- property entite --
    @property
    def entite(self):
        """Return entite."""
        return self._entite

    @entite.setter
    def entite(self, entite):
        """Set entite."""
        if self._strict:
            if entite is None:
                raise TypeError('entite is required')
            if not isinstance(
                entite,
                (_sitehydro.Sitehydro, _sitehydro.Station,
                 _sitemeteo.Sitemeteo)
            ):
                raise TypeError(
                    'entite must be a Sitehydro, a Station or a Sitemeteo'
                )
        self._entite = entite

    # -- property descriptif --
    @property
    def descriptif(self):
        """Return descriptif."""
        return self._descriptif

    @descriptif.setter
    def descriptif(self, descriptif):
        """Set descriptif."""
        if descriptif is None:
            if self._strict:
                raise TypeError('descriptif is required')
        self._descriptif = str(descriptif)

    # -- property contact --
    @property
    def contact(self):
        """Return contact."""
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Set contact."""
        if contact is None:
            if self._strict:
                raise TypeError('contact is required')
        self._contact = contact

    # -- property ressources --
    @property
    def ressources(self):
        """Return ressources."""
        return self._ressources

    @ressources.setter
    def ressources(self, ressources):
        """Set ressources."""
        self._ressources = []
        if ressources is None:
            return
        if isinstance(ressources, Ressource):
            self._ressources = [ressources]
            return
        for ressource in ressources:
            if not isinstance(ressource, Ressource):
                raise TypeError('ressources must be an iterable'
                                ' of evenement.Ressource')
            self._ressources.append(ressource)

    # -- special methods --
    __all__attrs__ = (
        'entite', 'descriptif', 'contact', 'dt', 'publication', 'dtmaj',
        'typeevt', 'ressources', 'dtfin'
    )
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        return '''Evenement de l'entite {entite} ''' \
               '''redige par {contact}'''.format(
                   entite=self.entite,
                   contact=self.contact if self.contact is not None
                   else '<sans contact>',
               )

    __str__ = _composant.__str__

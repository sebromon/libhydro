# -*- coding: utf-8 -*-
"""Module evenement.

Ce module contient la classe:
    # Evenement

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime

from . import _composant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """1.0c"""
__date__ = """2014-07-16"""

#HISTORY
#V1.0 - 2014-03-02
#    use descriptors
#V0.1 - 2013-11-26
#    first shot


#-- todos ---------------------------------------------------------------------
# PROGRESS - Evenement 100%

#-- class Evenement -----------------------------------------------------------
class Evenement(object):

    """Classe Evenement.

    Classe pour manipuler des evenements.

    Proprietes:
        entite (sitehydro.Sitehydro ou sitehydro.Stationhydro ou
            sitemeteo.Sitemeteo) = entite concernee par l'evenement
        descriptif (string)
        contact (intervenant.Contact) = contact proprietaire de l'evenement
        dt (datetime.datetime) = date de l'evenement
        publication (entier parmi NOMENCLATURE[534]) = type de publication
        dtmaj (datetime.datetime) = date de mise a jour

    """

    dt = _composant.Datefromeverything(required=False)
    publication = _composant.Nomenclatureitem(nomenclature=534)
    dtmaj = _composant.Datefromeverything(required=False)

    def __init__(
        self, entite, descriptif, contact,
        dt=_datetime.datetime.utcnow(), publication=100,
        dtmaj=_datetime.datetime.utcnow(), strict=True
    ):
        """Initialisation.

        Arguments:
            entite (sitehydro.Sitehydro ou sitehydro.Stationhydro ou
                sitemeteo.Sitemeteo) = entite concernee par l'evenement
            descriptif (string)
            contact (intervenant.Contact) = contact proprietaire de l'evenement
            dt (numpy.datetime64 string, datetime.datetime...) =
                date de l'evenement
            publication (entier parmi NOMENCLATURE[534]) = type de publication
            dtmaj (numpy.datetime64 string, datetime.datetime...) =
                date de mise a jour
            strict (bool, defaut True) = en mode permissif le type de
                publication n'est pas controle et les proprietes obligatoires
                sont facultatives

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(self.__class__)['publication'].strict = self._strict

        # -- descriptors --
        self.dt = dt
        self.publication = publication
        self.dtmaj = dtmaj

        # -- full properties --
        self._entite = self._descriptif = self._contact = None
        self.entite = entite
        self.descriptif = descriptif
        self.contact = contact

    # -- property entite --
    @property
    def entite(self):
        """Return entite."""
        return self._entite

    @entite.setter
    def entite(self, entite):
        """Set entite."""
        if entite is None:
            if self._strict:
                raise TypeError('entite is required')
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
        self._descriptif = unicode(descriptif)

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

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return '''Evenement de l'entite {entite} ''' \
               '''redige par {contact}'''.format(
                   entite=self.entite,
                   contact=self.contact or '<sans contact>',
               )

    __str__ = _composant.__str__

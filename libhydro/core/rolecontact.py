# -*- coding: utf-8 -*-
"""Module role.

Ce module contient la classe:
    # Role

"""

# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

from libhydro.core import (_composant, intervenant as _intervenant)
from libhydro.core.nomenclature import NOMENCLATURE as _NOMENCLATURE

class RoleContact(object):
    """Classe RoleContact.

    Classe pour manipuler des roles d'une entité hydro ou d'un site météo.
    Propriétés:
        contact (intervenant.Contact) = contact associé au role
        role (int parmi NOMENCLATURE[527]) = role du contact
        dtdeb (datetime.datetime or None) : date de début du role
        dtfin (datetime.datetime or None) : date de fin du role
        dtmaj (datetime.datetime or None) : date de mise à jour
    """

    role = _composant.Nomenclatureitem(nomenclature=527)
    dtdeb = _composant.Datefromeverything(required=False)
    dtfin = _composant.Datefromeverything(required=False)
    dtmaj = _composant.Datefromeverything(required=False)

    def __init__(self, contact=None, role=None, dtdeb=None, dtfin=None,
                 dtmaj=None):

        self.role = role
        self.dtdeb = dtdeb
        self.dtfin = dtfin
        self.dtmaj = dtmaj

        self._contact = None
        self.contact = contact

    # -- property contact --
    @property
    def contact(self):
        """Return contact."""
        return self._contact

    @contact.setter
    def contact(self, contact):
        """Set contact."""
        self._contact = None
        # None case
        if contact is None:
            raise TypeError('contact is required')
        if not isinstance(contact, _intervenant.Contact):
            raise TypeError(
                'contact must be an instance of _intervenant.Contact')
        self._contact = contact

    def __unicode__(self):
        dtdeb = self.dtdeb if self.dtdeb is not None \
            else '<sans date de début>'
        dtfin = self.dtfin if self.dtfin is not None else '<sans date de fin>'
        return "Contact {} ayant le role {} ({}) entre {} et {}".format(
            self.contact.code, self.role, _NOMENCLATURE[527][self.role],
            dtdeb, dtfin)

    __str__ = _composant.__str__

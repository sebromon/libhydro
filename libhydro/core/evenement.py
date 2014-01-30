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

import sys as _sys
import datetime as _datetime

from libhydro.core.nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2013-11-26"""

#HISTORY
#V0.1 - 2013-11-26
#    first shot


#-- todos ---------------------------------------------------------------------

# -- config -------------------------------------------------------------------

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
            dt (datetime.datetime) = date de l'evenement
            publication (entier parmi NOMENCLATURE[534]) = type de publication
            dtmaj (datetime.datetime) = date de mise a jour
            strict (bool, defaut True) = en mode permissif le contact est
                facultatif et le type de publication n'est pas controle

        """

        # -- simple properties --
        self.entite = entite
        self.descriptif = unicode(descriptif) \
            if (descriptif is not None) else None
        self.contact = contact
        self.dt = dt
        self.dtmaj = dtmaj
        self._strict = bool(strict)

        # -- full properties --
        self._publication = None
        self.publication = publication

    # -- property publication --
    @property
    def publication(self):
        """Return type publication."""
        return self._publication

    @publication.setter
    def publication(self, publication):
        """Set type publication."""
        try:

            # None case
            if publication is None:
                raise TypeError('publication is required')

            # other cases
            publication = int(publication)
            if (self._strict) and (publication not in _NOMENCLATURE[534]):
                raise ValueError('publication incorrect')

            # all is well
            self._publication = publication

        except:
            raise

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return '''Evenement de l'entite {entite} ''' \
               '''redige par {contact}'''.format(
                   entite=self.entite,
                   contact=self.contact or '<sans contact>',
               )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)

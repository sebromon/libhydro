# -*- coding: utf-8 -*-
"""Module xml.scenario.

Ce module contient la classe:
    # Scenario

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime

from . import intervenant as _intervenant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1a"""
__date__ = """2013-08-20"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


#-- todos ---------------------------------------------------------------------


# -- class Scenario -----------------------------------------------------------
class Scenario(object):
    """Classe Scenario.

    Classe pour manipuler les scenarios des messages SANDRE.

    Proprietes:
        code = hydrometrie
        version = 1.1
        nom = 'Echange de donnees hydrometriques'
        dtprod (datetime.datetime)
        emetteur (intervenant.Contact)
        destinataire (intervenant.Intervenant)

    """

    # TODO - Scenario other properties

    # reference
    # envoi
    # contexte

    def __init__(self, emetteur, destinataire):
        """Constructeur.

        Arguments:
            emetteur (intervenant.Contact)
            destinataire (intervenant.Intervenant)

        """

        # -- simple properties --
        self.code = 'hydrometrie'
        self.version = 1.1
        self.nom = 'Echange de données hydrométriques'
        self.dtprod = _datetime.datetime.utcnow()

        # -- full properties --
        self.emetteur = emetteur
        self.destinataire = destinataire

    # -- property emetteur --
    @property
    def emetteur(self):
        """Emetteur du message."""
        return self._emetteur

    @emetteur.setter
    def emetteur(self, emetteur):
        try:
            if emetteur is None:
                raise ValueError('emetteur is required')
            if not isinstance(emetteur, _intervenant.Contact):
                raise ValueError('emetteur incorrect')
            self._emetteur = emetteur
        except:
            raise

    # -- property destinataire --
    @property
    def destinataire(self):
        """Destinataire du message."""
        return self._destinataire

    @destinataire.setter
    def destinataire(self, destinataire):
        try:
            if destinataire is None:
                raise ValueError('destinataire is required')
            if not isinstance(destinataire, _intervenant.Intervenant):
                raise ValueError('destinataire incorrect')
            self._destinataire = destinataire
        except:
            raise

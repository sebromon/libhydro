# -*- coding: utf-8 -*-
"""Module xml.classes.

Ce module contient les classes:
    # Message
    # Scenario

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
import numpy as _numpy

from libhydro.core import (intervenant as _intervenant)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1e"""
__date__ = """2013-09-03"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


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

    # class attributes
    code = 'hydrometrie'
    version = '1.1'
    nom = 'Echange de données hydrométriques'

    def __init__(self, emetteur, destinataire, dtprod=None):
        """Constructeur.

        Arguments:
            emetteur (intervenant.Contact)
            destinataire (intervenant.Intervenant)
            dtprod (datetime ou isoformat, defaut utcnow())

        """

        # -- full properties --
        self.emetteur = emetteur
        self.destinataire = destinataire
        self.dtprod = dtprod

    # -- property emetteur --
    @property
    def emetteur(self):
        """Emetteur du message."""
        return self._emetteur

    @emetteur.setter
    def emetteur(self, emetteur):
        try:
            # None case
            if emetteur is None:
                raise TypeError('emetteur is required')
            # other cases
            if not isinstance(emetteur, _intervenant.Contact):
                raise TypeError('emetteur incorrect')
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
            # None case
            if destinataire is None:
                raise TypeError('destinataire is required')
            # other cases
            if not isinstance(destinataire, _intervenant.Intervenant):
                raise TypeError('destinataire incorrect')
            self._destinataire = destinataire
        except:
            raise

    # -- property dtprod --
    @property
    def dtprod(self):
        """Date de production du message."""
        return self._dtprod

    @dtprod.setter
    def dtprod(self, dtprod):
        try:
            # None case
            if dtprod is None:
                dtprod = _datetime.datetime.utcnow()

            # other cases
            if isinstance(dtprod, (str, unicode)):
                dtprod = _numpy.datetime64(dtprod)
            if isinstance(dtprod, _numpy.datetime64):
                dtprod = dtprod.item()
            if not isinstance(dtprod, _datetime.datetime):
                raise TypeError('dtprod must be a datetime')

            # all is well
            self._dtprod = dtprod

        except:
            raise

    # -- other methods --
    def __unicode__(self):
        """Unicode representation."""
        return "Message du {0}\nEmis par le {1} pour l'{2}".format(
            self.dtprod,
            self.emetteur,
            self.destinataire
        )

    def __str__(self):
        """String representation."""
        if _sys.version_info[0] >= 3:  # Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode('utf8')


# -- class Message ------------------------------------------------------------
class Message(object):

    def __init__(self):
        # TODO
        pass

        # 'scenario': _scenario_from_element(tree.find('Scenario')),
        # # 'intervenants':
        # 'siteshydro': _siteshydro_from_element(tree.find('RefHyd/SitesHydro')),
        # # 'sitesmeteo'
        # # 'modelesprevision': 'TODOS',
        # # 'evenements'
        # # 'courbestarage'
        # # 'jaugeages'
        # # 'courbescorrection'
        # 'series': _series_from_element(tree.find('Donnees/Series')),
        # # 'obssmeteo'
        # # 'obsselab'
        # # 'gradshydro'
        # # 'qualifsannee'
        # 'simulations': _simulations_from_element(tree.find('Donnees/Simuls'))
        # # 'alarmes'

    @classmethod
    def from_file(src):
        # TODO
        pass

#     """Parse le fichier src, instancie et retourne les objets qu'il contient.
#
#     Arguments:
#         src (nom de fichier, url, objet fichier...) = source de donnee. Les
#             type de src acceptes sont ceux de lxml.etree.parse
#
#     Retourne un dictionnaire avec les cles:
#             # scenario: xml.Scenario
#             # siteshydro: liste de sitehydro.Siteshydro ou None
#             # series: liste de obshydro.Serie ou None
#             # simulation: liste de simulation.Simulation ou None
#
#     """
#
#     # read the file
#     parser = _etree.XMLParser(
#         remove_blank_text=True, remove_comments=True, ns_clean=True
#     )
#     tree = _etree.parse(src, parser=parser)
#
#     # deal with namespaces
#     # TODO - we could certainly do better with namespaces
#     if tree.getroot().nsmap != {}:
#         raise ValueError("can't parse xml file with namespaces")
#
#     return {
#         'scenario': _scenario_from_element(tree.find('Scenario')),
#         # 'intervenants':
#         'siteshydro': _siteshydro_from_element(tree.find('RefHyd/SitesHydro')),
#         # 'sitesmeteo'
#         # 'modelesprevision': 'TODOS',
#         # 'evenements'
#         # 'courbestarage'
#         # 'jaugeages'
#         # 'courbescorrection'
#         'series': _series_from_element(tree.find('Donnees/Series')),
#         # 'obssmeteo'
#         # 'obsselab'
#         # 'gradshydro'
#         # 'qualifsannee'
#         'simulations': _simulations_from_element(tree.find('Donnees/Simuls'))
#         # 'alarmes'
#     }

    def add(self, *args):
        """Add some elements."""
        # TODO
        pass

    def write(self, dst):
        # TODO
        pass

    def __str__(self):
        # TODO
        pass

# -*- coding: utf-8 -*-
"""Module seuil.

Ce module contient les classes:
    # Seuilhydro
    # Valeurseuil

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime

from libhydro.core.nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1a"""
__date__ = """2014-02-10"""

#HISTORY
#V0.1 - 2014-02-10
#    first shot


#-- todos ---------------------------------------------------------------------
# class Seuilmeteo - TODO


#-- config --------------------------------------------------------------------

#-- class _Seuil --------------------------------------------------------------
class _Seuil(object):

    """Abstract base class for seuils.

    Properties:
        code (entier) = code seuil
        typeseuil (entier parmi NOMENCLATURE[528]) = type du seuil
        duree (entier) = duree du seuil en minutes
        nature (entier parmi NOMENCLATURE[529]) = nature du seuil
        libelle (string[255]) = libelle du seuil
        mnemo (string[50]) = mnemonique
        gravite (entier < 100)
        commentaire (texte)
        dtmaj (datetime.datetime) = date de mise a jour

        La duree n'est pertinente que pour les seuils de type gradient.
        Le libelle et le mnemonique sont exclusifs.

    """

    def __init__(
        self, code, typeseuil, duree=0,
        nature=None, libelle=None, mnemo=None, gravite=None, commentaire=None,
        dtmaj=_datetime.datetime.utcnow(), strict=True
    ):
        """Initialisation.

        Arguments:
            code (entier) = code seuil
            typeseuil (entier parmi NOMENCLATURE[528]) = type du seuil
            duree (entier, defaut 0) = duree du seuil en minutes
            nature (entier parmi NOMENCLATURE[529]) = nature du seuil
            libelle (string[255]) = libelle du seuil
            mnemo (string[50]) = mnemonique
            gravite (entier < 100)
            commentaire (texte)
            dtmaj (datetime.datetime) = date de mise a jour
            strict (bool, defaut True) = strict or fuzzy mode

        """
        # -- simple properties --
        self.libelle = unicode(libelle) if libelle else None
        self.mnemo = unicode(mnemo) if mnemo else None
        self.commentaire = unicode(commentaire) if commentaire else None
        self.dtmaj = dtmaj
        self._strict = bool(strict)

        # -- full properties --
        self._code = 0
        self.code = code
        self._typeseuil = None
        self.typeseuil = typeseuil
        self._duree = 0
        self.duree = duree
        self._nature = None
        self.nature = nature
        self._gravite = 0
        self.gravite = gravite

    # -- property code --
#     @property
#     def publication(self):
#         """Return type publication."""
#         return self._publication
#
#     @publication.setter
#     def publication(self, publication):
#         """Set type publication."""
#         try:
#
#             # None case
#             if publication is None:
#                 raise TypeError('publication is required')
#
#             # other cases
#             publication = int(publication)
#             if (self._strict) and (publication not in _NOMENCLATURE[534]):
#                 raise ValueError('publication incorrect')
#
#             # all is well
#             self._publication = publication
#
#         except:
#             raise

    # -- property typeseuil --

    # -- property duree --

    # -- property nature --

    # -- property gravite --


#-- class Seuilhydro ----------------------------------------------------------
class Seuilhydro(_Seuil):

    """Classe Seuilhydro.

    Proprietes:
        code (entier) = code seuil
        typeseuil (entier parmi NOMENCLATURE[528]) = type du seuil
        duree (entier) = duree du seuil en minutes
        nature (entier parmi NOMENCLATURE[529]) = nature du seuil
        libelle (string[255]) = libelle du seuil
        mnemo (string[50]) = mnemonique
        gravite (entier < 100)
        commentaire (texte)
        publication (bool)
        valeurforcee (bool)
        dtmaj (datetime.datetime) = date de mise a jour

        La duree n'est pertinente que pour les seuils de type gradient.
        Le libelle et le mnemonique sont exclusifs.

    """

    def __init__(
        self, code, typeseuil, duree=0,
        nature=None, libelle=None, mnemo=None, gravite=None, commentaire=None,
        publication=False, valeurforcee=False,
        dtmaj=_datetime.datetime.utcnow(), strict=True
    ):
        """Initialisation.

        Arguments:
            code (entier) = code seuil
            typeseuil (entier parmi NOMENCLATURE[528]) = type du seuil
            duree (entier, defaut 0) = duree du seuil en minutes
            nature (entier parmi NOMENCLATURE[529]) = nature du seuil
            libelle (string[255]) = libelle du seuil
            mnemo (string[50]) = mnemonique
            gravite (entier < 100)
            commentaire (texte)
            publication (bool, defaut False)
            valeurforcee (bool, defaut False)
            dtmaj (datetime.datetime) = date de mise a jour
            strict (bool, defaut True) = strict or fuzzy mode

        """
        # -- super --
        super(Seuilhydro, self).__init__(
            code=code, typeseuil=typeseuil, duree=duree,
            nature=nature, libelle=libelle, mnemo=mnemo, gravite=gravite,
            commentaire=commentaire, dtmaj=dtmaj, strict=strict
        )

        # -- simple properties --
        self.publication = bool(publication)
        self.valeurforcee = bool(valeurforcee)

#     # -- other methods --
#     def __unicode__(self):
#         """Return unicode representation."""
#         return '''Evenement de l'entite {entite} ''' \
#                '''redige par {contact}'''.format(
#                    entite=self.entite,
#                    contact=self.contact or '<sans contact>',
#                )
#
#     def __str__(self):
#         """Return string representation."""
#         if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
#             return self.__unicode__()
#         else:  # Python 2
#             return self.__unicode__().encode(_sys.stdout.encoding)

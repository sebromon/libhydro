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

import sys as _sys
import datetime as _datetime

from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from . import _composant


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1f"""
__date__ = """2014-03-19"""

#HISTORY
#V0.1 - 2014-02-10
#    first shot


#-- todos ---------------------------------------------------------------------
# PROGRESS - Seuilhydro 100% - Valeurseuil 60% - Seuilmeteo 0%
# TODO - write Class Seuilmeteo
# TODO - in Class Seuilhydro: add ctrl 'duree is required only for grad type'
# TODO - in Class Seuilhydro: add ctrl 'libelle and mnemo are exclusive'
# TODO - in Class Valseuil: move all properties in full properties
# TODO - write __unicode__ method for Seuilhydro


#-- class _Seuil --------------------------------------------------------------
class _Seuil(object):

    """Abstract base class for seuils.

    Properties:
        code (entier) = code seuil
        typeseuil (entier parmi NOMENCLATURE[528]) = type du seuil
        duree (numerique) = duree du seuil en minutes
        nature (entier parmi NOMENCLATURE[529]) = nature du seuil
        libelle (string[255]) = libelle du seuil
        mnemo (string[50]) = mnemonique
        gravite (0 < entier < 100)
        commentaire (texte)
        dtmaj (datetime.datetime) = date de mise a jour
        valeurs (liste de Valeurseuil)

        La duree n'est pertinente que pour les seuils de type gradient.
        Le libelle et le mnemonique sont exclusifs.

    """

    dtmaj = _composant.Datefromeverything(required=False)
    typeseuil = _composant.Nomenclatureitem(nomenclature=528)
    nature = _composant.Nomenclatureitem(nomenclature=529, required=False)

    def __init__(
        self, code=0, typeseuil=1, duree=0,
        nature=None, libelle=None, mnemo=None, gravite=None, commentaire=None,
        dtmaj=_datetime.datetime.utcnow(), valeurs=None, strict=True
    ):
        """Initialisation.

        Arguments:
            code (entier) = code seuil
            typeseuil (entier parmi NOMENCLATURE[528]) = type du seuil
            duree (numerique) = duree du seuil en minutes
            nature (entier parmi NOMENCLATURE[529]) = nature du seuil
            libelle (string[255]) = libelle du seuil
            mnemo (string[50]) = mnemonique
            gravite (0 < entier < 100)
            commentaire (texte)
            dtmaj (numpy.datetime64 string, datetime.datetime...) =
                date de mise a jour
            valeurs (liste de Valeurseuil)
            strict (bool, defaut True) = strict or fuzzy mode

        La navigabilite des valeurs vers le seuil est assuree par le
        constructeur.

        """
        # -- simple properties --
        self.libelle = unicode(libelle) if libelle else None
        self.mnemo = unicode(mnemo) if mnemo else None
        self.commentaire = unicode(commentaire) if commentaire else None
        self._strict = bool(strict)

        # -- descriptors --
        self.dtmaj = dtmaj
        self.typeseuil = typeseuil
        self.nature = nature

        # -- full properties --
        self._code = self._duree = 0
        self.code = code
        self.duree = duree
        self._gravite = self._valeurs = None
        self.gravite = gravite
        self.valeurs = valeurs

    # -- property code --
    @property
    def code(self):
        """Return code."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code."""
        try:

            # None case
            if code is None:
                raise TypeError('code is required')

            # other cases
            self._code = int(code)

        except:
            raise

    # -- property duree --
    @property
    def duree(self):
        """Return duree."""
        return self._duree

    @duree.setter
    def duree(self, duree):
        """Set duree."""
        try:

            # None case
            if duree is None:
                raise TypeError('duree is required')

            # other cases
            self._duree = float(duree)

        except:
            raise

    # -- property gravite --
    @property
    def gravite(self):
        """Return gravite."""
        return self._gravite

    @gravite.setter
    def gravite(self, gravite):
        """Set gravite."""
        try:

            # None case
            if gravite is not None:
                gravite = int(gravite)
                if not (0 <= gravite <= 100):
                    raise ValueError('gravite out of range')

            # all is well
            self._gravite = gravite

        except:
            raise

    @property
    def valeurs(self):
        """Return valeurs."""
        return self._valeurs

    @valeurs.setter
    def valeurs(self, valeurs):
        """Set valeurs."""
        # assert the navigability from valeur to seuil
        if valeurs is not None:
            for valeur in valeurs:
                valeur.seuil = self

        # all is well
        self._valeurs = valeurs

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return '''Seuil {code} de type {typeseuil} ''' \
               '''et de duree {duree} mn\n''' \
               '''{nature}\n''' \
               '''Intitule: {intitule}\n''' \
               '''Gravite: {gravite}\n''' \
               '''Valeurs:\n{valeurs}\n'''.format(
                   code=self.code,
                   typeseuil=_NOMENCLATURE[528][self.typeseuil],
                   duree=self.duree,
                   nature=(
                       _NOMENCLATURE[529][self.nature]
                       if self.nature is not None
                       else '<nature inconnue>'
                   ),
                   intitule=self.libelle or self.mnemo or '<sans intitule>',
                   gravite=self.gravite or '<gravite inconnue>',
                   valeurs='\n'.join(
                       ['  %s' % v.__unicode__() for v in self.valeurs]
                   ) if (self.valeurs not in (None, []))
                   else '    <sans valeurs>'
               )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


#-- class Seuilhydro ----------------------------------------------------------
class Seuilhydro(_Seuil):

    """Classe Seuilhydro.

    Proprietes:
        sitehydro (sitehydro.Sitehydro) = site hydro du seuil
        code (entier) = code seuil
        typeseuil (entier parmi NOMENCLATURE[528]) = type du seuil
        duree (numerique) = duree du seuil en minutes
        nature (entier parmi NOMENCLATURE[529]) = nature du seuil
        libelle (string[255]) = libelle du seuil
        mnemo (string[50]) = mnemonique
        gravite (0 < entier < 100)
        commentaire (texte)
        publication (bool)
        valeurforcee (bool)
        dtmaj (datetime.datetime) = date de mise a jour
        valeurs (liste de Valeurseuil)

        La duree n'est pertinente que pour les seuils de type gradient.
        Le libelle et le mnemonique sont exclusifs.

    """

    def __init__(
        self, sitehydro=None, code=0, typeseuil=1, duree=0,
        nature=None, libelle=None, mnemo=None, gravite=None, commentaire=None,
        publication=False, valeurforcee=False,
        dtmaj=_datetime.datetime.utcnow(), valeurs=None, strict=True
    ):
        """Initialisation.

        Arguments:
            sitehydro (sitehydro.Sitehydro) = site hydro du seuil
            code (entier) = code seuil
            typeseuil (entier parmi NOMENCLATURE[528]) = type du seuil
            duree (numerique) = duree du seuil en minutes
            nature (entier parmi NOMENCLATURE[529]) = nature du seuil
            libelle (string[255]) = libelle du seuil
            mnemo (string[50]) = mnemonique
            gravite (0 < entier < 100)
            commentaire (texte)
            publication (bool, defaut False)
            valeurforcee (bool, defaut False)
            dtmaj (numpy.datetime64 string, datetime.datetime...) =
                date de mise a jour
            valeurs (liste de Valeurseuil)
            strict (bool, defaut True) = strict or fuzzy mode

        """
        # -- super --
        super(Seuilhydro, self).__init__(
            code=code, typeseuil=typeseuil, duree=duree,
            nature=nature, libelle=libelle, mnemo=mnemo, gravite=gravite,
            commentaire=commentaire, dtmaj=dtmaj, valeurs=valeurs,
            strict=strict
        )

        # -- simple properties --
        # FIXME - seuil.sitehydro should be  a full property
        self.sitehydro = sitehydro
        self.publication = bool(publication)
        self.valeurforcee = bool(valeurforcee)

    # -- other methods --
    # def __unicode__(self):
    #     """Return unicode representation."""
    #     return '''Seuil hydro {code} de type {typeseuil}'''.format(
    #         code=self.code,
    #         typeseuil=self.typeseuil
    #     )

    # def __str__(self):
    #     """Return string representation."""
    #     if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
    #         return self.__unicode__()
    #     else:  # Python 2
    #         return self.__unicode__().encode(_sys.stdout.encoding)


#-- class Valeurseuil ---------------------------------------------------------
class Valeurseuil (object):

    """Classe Valeurseuil.

    Proprietes:
        valeur (numerique) = valeur du seuil
        seuil (Seuilhydro ou Seuilmeteo)
        entite (Sitehydro, Stationhydro ou Grandeurmeteo)
        tolerance (numerique)
        dtactivation (datetime.datetime)
        dtdesactivation (datetime.datetime)

    """

    dtactivation = _composant.Datefromeverything(required=False)
    dtdesactivation = _composant.Datefromeverything(required=False)

    def __init__(
        self, valeur, seuil=None, entite=None,
        tolerance=None,
        dtactivation=None, dtdesactivation=None,
        strict=True
    ):
        """Initialisation.

        Arguments:
            valeur (numerique) = valeur du seuil
            seuil (Seuilhydro ou Seuilmeteo)
            entite (Sitehydro, stationhydro ou Grandeurmeteo)
            tolerance (numerique)
            dtactivation (numpy.datetime64 string, datetime.datetime...)
            dtdesactivation (numpy.datetime64 string, datetime.datetime...)
            strict (bool)

        La navigabilite des valeurs vers le seuil est assuree par le
        constructeur.

        """
        # -- simple properties --
        # TODO - all the Valeurseuil properties should be full properties
        self.valeur = float(valeur)
        # TODO - Valeurseuil.seuil is required unless strict is False
        self.seuil = seuil
        # TODO - Valeurseuil.entite is required unless strict is False
        self.entite = entite
        self.tolerance = float(tolerance) if tolerance else None
        self._strict = bool(strict)

        # -- descriptors --
        self.dtactivation = dtactivation
        self.dtdesactivation = dtdesactivation

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return '''{valeur} (tolerance {tolerance})'''.format(
            valeur=self.valeur,
            tolerance=self.tolerance or '<inconnue>'
        )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)

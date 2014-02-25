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
import numpy as _numpy

from .nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1c"""
__date__ = """2014-02-25"""

#HISTORY
#V0.1 - 2014-02-10
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - write Class Seuilmeteo
# TODO - in Class Seuilhydro: add ctrl 'duree is required only for grad type'
# TODO - in Class Seuilhydro: add ctrl 'libelle and mnemo are exclusive'
# TODO - in Class Valseuil: move all properties in full properties


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
            dtmaj (datetime.datetime) = date de mise a jour
            valeurs (liste de Valeurseuil)
            strict (bool, defaut True) = strict or fuzzy mode

        """
        # -- simple properties --
        self.libelle = unicode(libelle) if libelle else None
        self.mnemo = unicode(mnemo) if mnemo else None
        self.commentaire = unicode(commentaire) if commentaire else None
        self.valeurs = valeurs  # FIXME - should be a full property
        self._strict = bool(strict)

        # -- full properties --
        self._code = 0
        self.code = code
        self._typeseuil = 1
        self.typeseuil = typeseuil
        self._duree = 0
        self.duree = duree
        self._nature = self._gravite = self._dtmaj = None
        self.nature = nature
        self.gravite = gravite
        self.dtmaj = dtmaj

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

    # -- property typeseuil --
    @property
    def typeseuil(self):
        """Return typeseuil."""
        return self._typeseuil

    @typeseuil.setter
    def typeseuil(self, typeseuil):
        """Set typeseuil."""
        try:

            # None case
            if typeseuil is None:
                raise TypeError('typeseuil is required')

            # other cases
            typeseuil = int(typeseuil)
            if typeseuil not in _NOMENCLATURE[528]:
                raise ValueError('typeseuil incorrect')

            # all is well
            self._typeseuil = typeseuil

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

    # -- property nature --
    @property
    def nature(self):
        """Return nature."""
        return self._nature

    @nature.setter
    def nature(self, nature):
        """Set nature."""
        try:

            # all cases
            if nature is not None:
                nature = int(nature)
                if nature not in _NOMENCLATURE[529]:
                    raise ValueError('nature incorrect')

            # all is well
            self._nature = nature

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

    # -- property dtmaj --
    @property
    def dtmaj(self):
        """Return dtmaj."""
        if self._dtmaj is not None:
            return self._dtmaj.item()

    @dtmaj.setter
    def dtmaj(self, dtmaj):
        """Set dtmaj."""
        try:
            if dtmaj is not None:
                if not isinstance(dtmaj, _numpy.datetime64):
                    try:
                        dtmaj = _numpy.datetime64(dtmaj, 's')
                    except (ValueError, TypeError):
                        try:
                            dtmaj = _numpy.datetime64(dtmaj.isoformat(), 's')
                        except (ValueError, TypeError, AttributeError):
                            raise TypeError('dtmaj must be a date')
            self._dtmaj = dtmaj

        except:
            raise

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
            dtmaj (datetime.datetime) = date de mise a jour
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
        self.sitehydro = sitehydro  # FIXME - should be  a full property
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
            dtactivation (datetime.datetime)
            dtdesactivation (datetime.datetime)
            strict (bool)

        """
        # -- simple properties --
        # TODO - all these properties should be full properties
        self.valeur = float(valeur)
        self.seuil = seuil  # TODO - required unless strict is False
        self.entite = entite  # TODO - required unless strict is False
        self.tolerance = float(tolerance) if tolerance else None
        self._strict = bool(strict)

        # -- full properties --
        self._dtactivation = self._dtdesactivation = None
        self.dtactivation = dtactivation
        self.dtdesactivation = dtdesactivation

    # -- property dtactivation --
    @property
    def dtactivation(self):
        """Return dtactivation."""
        if self._dtactivation is not None:
            return self._dtactivation.item()

    @dtactivation.setter
    def dtactivation(self, dtactivation):
        """Set dtactivation."""
        try:
            if dtactivation is not None:
                if not isinstance(dtactivation, _numpy.datetime64):
                    try:
                        dtactivation = _numpy.datetime64(dtactivation, 's')
                    except (ValueError, TypeError):
                        try:
                            dtactivation = _numpy.datetime64(
                                dtactivation.isoformat(), 's'
                            )
                        except (ValueError, TypeError, AttributeError):
                            raise TypeError('dtactivation must be a date')
            self._dtactivation = dtactivation

        except:
            raise

    # -- property dtdesactivation --
    @property
    def dtdesactivation(self):
        """Return dtdesactivation."""
        if self._dtdesactivation is not None:
            return self._dtdesactivation.item()

    @dtdesactivation.setter
    def dtdesactivation(self, dtdesactivation):
        """Set dtdesactivation."""
        try:
            if dtdesactivation is not None:
                if not isinstance(dtdesactivation, _numpy.datetime64):
                    try:
                        dtdesactivation = _numpy.datetime64(
                            dtdesactivation, 's'
                        )
                    except (ValueError, TypeError):
                        try:
                            dtdesactivation = _numpy.datetime64(
                                dtdesactivation.isoformat(), 's'
                            )
                        except (ValueError, TypeError, AttributeError):
                            raise TypeError('dtdesactivation must be a date')
            self._dtdesactivation = dtdesactivation

        except:
            raise

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

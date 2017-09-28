# coding: utf-8
"""Module seuil.

Ce module contient les classes:
    # Seuilhydro
    # Valeurseuil

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from . import _composant


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2f"""
__date__ = """2014-12-17"""

# HISTORY
# V0.1 - 2014-02-10
#   first shot


# -- todos --------------------------------------------------------------------
# PROGRESS - Seuilhydro 100% - Valeurseuil 60% - Seuilmeteo 0%
# TODO - write Class Seuilmeteo
# TODO - in Class Seuilhydro: BDTR.Warning 'libelle and mnemo are exclusive' ?
# TODO - in Class Valseuil: move all properties in full properties
# TODO - write __unicode__ method for Seuilhydro


# -- class _Seuil -------------------------------------------------------------
class _Seuil(object):

    """Abstract base class for seuils.

    Properties:
        code (string) = code seuil
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
    typeseuil = _composant.Nomenclatureitem(nomenclature=528, required=False)
    nature = _composant.Nomenclatureitem(nomenclature=529, required=False)

    def __init__(
        self, code, typeseuil=None, duree=None,
        nature=None, libelle=None, mnemo=None, gravite=None, commentaire=None,
        dtmaj=None, valeurs=None, strict=True
    ):
        """Initialisation.

        Arguments:
            code (string) = code seuil
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
        self.libelle = str(libelle) if libelle else None
        self.mnemo = str(mnemo) if mnemo else None
        self.commentaire = str(commentaire) if commentaire else None
        self._strict = bool(strict)

        # -- descriptors --
        self.dtmaj = dtmaj
        self.typeseuil = typeseuil
        self.nature = nature

        # -- full properties --
        self._code = self._duree = self._gravite = self._valeurs = None
        self.code = code
        self.duree = duree
        self.gravite = gravite
        self.valeurs = valeurs

        # -- some checks
        self._check_typeseuil_and_duree()

    # -- property code --
    @property
    def code(self):
        """Return code."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code."""
        # None case
        if code is None:
            raise TypeError('code is required')

        # other cases
        self._code = str(code)

    # -- property duree --
    @property
    def duree(self):
        """Return duree."""
        return self._duree

    @duree.setter
    def duree(self, duree):
        """Set duree."""
        if duree is not None:
            try:
                duree = float(duree)
            except:
                raise TypeError('duree should be a number')
        self._duree = duree
        self._check_typeseuil_and_duree()

    # -- property gravite --
    @property
    def gravite(self):
        """Return gravite."""
        return self._gravite

    @gravite.setter
    def gravite(self, gravite):
        """Set gravite."""
        if gravite is not None:
            try:
                gravite = int(gravite)
            except:
                raise TypeError('gravite must be an int')
            if not (0 <= gravite <= 100):
                raise ValueError('gravite out of range')
        self._gravite = gravite

    @property
    def valeurs(self):
        """Return valeurs."""
        return self._valeurs

    @valeurs.setter
    def valeurs(self, valeurs):
        """Set valeurs."""
        # assert the navigability from valeur to seuil
        if self._strict and (valeurs is not None):
            try:
                for valeur in valeurs:
                    valeur.seuil = self

            except AttributeError:
                raise TypeError('valeurs should be an iterable of Valeurseuil')

        # all is well
        self._valeurs = valeurs

    # -- other methods --
    def _check_typeseuil_and_duree(self):
        """Assert some hydrologic rules."""
        if (self.typeseuil == 2) and (self.duree in (None, 0)):
                raise ValueError('gradient seuil must have a duree')
        if self.typeseuil == 1:  # absolute seuil
            if self.duree is None:
                self.duree = 0
            elif self.duree != 0:
                raise ValueError('absolute seuil duree must be 0')

    # -- special methods --
    def __unicode__(self):
        """Return unicode representation."""
        # init
        try:
            typeseuil = _NOMENCLATURE[528][self.typeseuil]
        except Exception:
            typeseuil = '<sans type>'
        try:
            if self.duree is None:
                raise TypeError
            duree = '%s mn' % self.duree
        except Exception:
            duree = '<sans duree>'
        try:
            nature = _NOMENCLATURE[529][self.nature]
        except Exception:
            nature = '<nature inconnue>'
        try:
            valeurs = '\n'.join(
                ['  %s' % str(v) for v in self.valeurs]
            )
        except Exception:
            valeurs = '%s<sans valeurs>' % (' ' * 4)

        # action !
        return '''Seuil {code} de type {typeseuil} ''' \
               '''et de duree {duree}\n''' \
               '''{nature}\n''' \
               '''Intitule: {intitule}\n''' \
               '''Gravite: {gravite}\n''' \
               '''Valeurs:\n{valeurs}\n'''.format(
                   code=self.code,
                   typeseuil=typeseuil,
                   duree=duree,
                   nature=nature,
                   intitule=self.libelle or self.mnemo or '<sans intitule>',
                   gravite=self.gravite or '<gravite inconnue>',
                   valeurs=valeurs
               )

    __str__ = _composant.__str__


# -- class Seuilhydro ---------------------------------------------------------
class Seuilhydro(_Seuil):

    """Classe Seuilhydro.

    Proprietes:
        code (string) = code seuil
        sitehydro (sitehydro.Sitehydro) = site hydro du seuil
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
        self, code, sitehydro=None, typeseuil=None, duree=None,
        nature=None, libelle=None, mnemo=None, gravite=None, commentaire=None,
        publication=None, valeurforcee=None, dtmaj=None, valeurs=None,
        strict=True
    ):
        """Initialisation.

        Arguments:
            code (string) = code seuil
            sitehydro (sitehydro.Sitehydro) = site hydro du seuil
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
        self.publication = bool(publication) if publication is not None \
            else None
        self.valeurforcee = bool(valeurforcee) if valeurforcee is not None \
            else None

    # -- special methods --
    __all__attrs__ = (
        'sitehydro', 'code', 'typeseuil', 'duree', 'nature', 'libelle',
        'mnemo', 'gravite', 'commentaire', 'publication', 'valeurforcee',
        'dtmaj', 'valeurs'
    )
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__


# -- class Valeurseuil --------------------------------------------------------
class Valeurseuil (object):

    """Classe Valeurseuil.

    Proprietes:
        valeur (numerique) = valeur du seuil
        seuil (Seuilhydro ou Seuilmeteo)
        entite (Sitehydro, Station ou Grandeurmeteo)
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
            entite (Sitehydro, Station ou Grandeurmeteo)
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

    # -- special methods --
    __all__attrs__ = (
        'valeur', 'seuil', 'entite', 'tolerance', 'dtactivation',
        'dtdesactivation'
    )
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        return '''{valeur} (tolerance {tolerance})'''.format(
            valeur=self.valeur,
            tolerance=self.tolerance or '<inconnue>'
        )

    __str__ = _composant.__str__

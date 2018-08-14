# coding: utf-8
"""Module composant_site.

Ce module contient les elements communs aux modules sitehydro et sitemeteo.

Il integre les classes:
    # Coord

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

from . import _composant
from .nomenclature import NOMENCLATURE as _NOMENCLATURE
# from . import sitemeteo as _sitemeteo


# -- strings ------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """1.0b"""
__date__ = """2014-07-18"""

# HISTORY
# V0.1 - 2014-07-16
#   split the composant file in 3 parts


# -- class Coord --------------------------------------------------------------
class Coord(object):

    """Classe Coord.

    Classe pour manipuler des coordonnees.

    Proprietes:
        x, y (float)
        proj (int parmi NOMENCLATURE[22]) = systeme de projection

    """

    proj = _composant.Nomenclatureitem(nomenclature=22)

    def __init__(self, x, y, proj=None, strict=True):
        """Initialisation.

        Arguments:
            x, y (float)
            proj (int parmi NOMENCLATURE[22]) = systeme de projection
            strict (bool, defaut True) = le mode permissif permet de rendre
                facultatif le parametre proj

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(self.__class__)['proj'].required = self._strict

        for crd in ('x', 'y'):
            try:
                self.__setattr__(crd, float(locals()[crd]))
            except Exception:
                raise TypeError('{} must be a number'.format(crd))

        # -- descriptors --
        self.proj = proj

    # -- other methods --
    __all__attrs__ = ('x', 'y', 'proj')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        # init
        try:
            proj = _NOMENCLATURE[22][self.proj]
        except Exception:
            proj = '<projection inconnue>'

        # action !
        return 'Coord (x={0}, y={1}) [proj {2}]'.format(
            self.x,
            self.y,
            proj
        )

    __str__ = _composant.__str__


# -- class Altitude -----------------------------------------------------------
class Altitude(object):

    """Classe Altitude.

    Classe pour manipuler des altitudes.

    Proprietes:
        altitude (float)
        sysalti (int parmi NOMENCLATURE[76]) = systeme altimétrique

    """

    sysalti = _composant.Nomenclatureitem(nomenclature=76)

    def __init__(self, altitude=None, sysalti=31, strict=True):
        """Initialisation.

        Arguments:
            altitude (float))
            sysalti (int parmi NOMENCLATURE[76]) = systeme altimétrique
            strict (bool, defaut True) = le mode permissif permet de rendre
                facultatif le parametre proj

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        vars(self.__class__)['sysalti'].required = self._strict

        # -- descriptors --
        self.sysalti = sysalti
        self._altitude = None
        self.altitude = altitude

    # -- property altitude --
    @property
    def altitude(self):
        """Return altitude."""
        return self._altitude

    @altitude.setter
    def altitude(self, altitude):
        """Set altitude."""
        # None case
        if altitude is None:
            if self._strict:
                raise ValueError('altitude must be defined')
            else:
                self._altitude = None
        else:
            self._altitude = float(altitude)

    # -- other methods --
    __all__attrs__ = ('altitude', 'sysalti')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        # init
        if self.sysalti in _NOMENCLATURE[76]:
            sysalti = _NOMENCLATURE[76][self.sysalti]
        else:
            sysalti = '<sysalti inconnu>'

        # action !
        return 'Altitude: {0} [sysalti: {1}]'.format(
            self.altitude,
            sysalti
        )

    __str__ = _composant.__str__


# -- class LoiStat -----------------------------------------------------------
class LoiStat(object):

    """Classe LoiStat.

    Classe pour manipuler des lois statistiques.

    Proprietes:
        contexte (int parmi NOMENCLATURE[521]) = Type de contexte
        loi (int parmi NOMENCLATURE[114]) = Loi pour le module

    """

    contexte = _composant.Nomenclatureitem(nomenclature=521)
    loi = _composant.Nomenclatureitem(nomenclature=114)

    def __init__(self, contexte=None, loi=0):
        """Initialisation.

        Arguments:
            contexte (int parmi NOMENCLATURE[521]) = Type de contexte
            loi (int parmi NOMENCLATURE[114]) = Loi pour le module

        """
        # -- descriptors --
        self.contexte = contexte
        self.loi = loi

    # -- other methods --
    __all__attrs__ = ('contexte', 'loi')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""

        return 'Type de contexte {0} [loi de {1}]'.format(
            _NOMENCLATURE[521][self.contexte],
            _NOMENCLATURE[114][self.loi]
        )

    __str__ = _composant.__str__


# -- class EntiteVigicrues ----------------------------------------------------
class EntiteVigiCrues(object):

    """Classe EntiteVigiCrues.

    Classe pour manipuler des entités de vigilance crues.

    Proprietes:
        code (str) = code de l'entité
        libelle (str ou None) = Libellé de l'entité
    """

    def __init__(self, code=None, libelle=None):
        """Initialisation.

        Arguments:
            code (str) = code de l'entité
            nom (str ou None) = Nom de l'entité

        """
        # -- descriptors --
        self.code = str(code)
        self.libelle = str(libelle) if libelle is not None else None

    # -- other methods --
    __all__attrs__ = ('code', 'libelle')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""

        return 'Entité {0} ({1}) de vigilance crues'.format(
            self.code,
            self.libelle if self.libelle is not None else '<Sans libellé>'
        )

    __str__ = _composant.__str__


# -- class Commune ----------------------------------------------------
class Commune(object):

    """Classe Commune.

    Classe pour manipuler des communes.

    Proprietes:
        code (str(5)) = code insee de la commune
        libelle (str ou None) = Nom de la commune
    """

    def __init__(self, code=None, libelle=None):
        """Initialisation.

        Arguments:
            code (str(5)) = code insee de la commune
            nom (str ou None) = Nom de la commune

        """
        # -- simple properties --
        self.libelle = str(libelle) if libelle is not None else None

        # -- descriptors --
        self._code = None
        self.code = code

    # -- property code --
    @property
    def code(self):
        """Return code."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code."""
        if _composant.is_code_insee(code, length=5, errors='strict'):
            self._code = (code)

    # -- other methods --
    __all__attrs__ = ('code', 'libelle')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""

        return 'Commune {0} ({1})'.format(
            self.code,
            self.libelle if self.libelle is not None else '<Sans libelle>'
        )

    __str__ = _composant.__str__

# -*- coding: utf-8 -*-
"""Module intervenant.

Ce module contient les classes:
    # Intervenant
    # Contact
    # Adresse -- not implemented --

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)


from .nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """version 0.1a"""
__date__ = """2013-08-20"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - use the BD Hydro intervenants list


# -- config -------------------------------------------------------------------


#-- Class Intervenant ---------------------------------------------------------
class Intervenant(object):
    """Classe Intervenant.

    Classe pour manipuler les intervenants Sandre.

    Proprietes:
        code (int) = code SIRET (14 chiffres) ou Sandre
        origine (string in (SIRET, SANDRE)) = origine du code
        nom (string) = nom de l'intervenant
        mnemo (string) = mnemonique
        contacts (une liste de Contact)

    """

    # TODO - Intervenant other properties

    # statut
    # auteur
    # activite
    # Adresse
    # commentaire
    # dtcreation
    # dtmaj

    def __init__(
        self, code=0, origine=None, nom=None, mnemo=None, contacts=None
    ):
        """Constructeur.

        Arguments:
            code (int, defaut 0) = code SIRET (14 chiffres) ou Sandre
            origine (string in ((S)I(RET), (S)A(NDRE))) = origine du code
            nom (string) = nom de l'intervenant
            mnemo (string) = mnemonique
            contacts (un Contact ou un iterable de Contact)

        """

        # -- simple properties --
        self.nom = self.mnemo = None
        if nom:
            self.nom = unicode(nom)
        if mnemo:
            self.mnemo = unicode(mnemo)

        # -- full properties --
        self._code = 0
        self._origine = None
        self._contacts = []
        if code is not None:
            self.code = code
        if origine is not None:
            self.origine = origine
        if contacts is not None:
            self.contacts = contacts

    # -- property code --
    @property
    def code(self):
        """Code intervenant."""
        return self._code

    @code.setter
    def code(self, code):
        try:
            code = int(code)
            if self._origine is None:
                if len(str(code)) == 14:
                    self._origine = 'SIRET'
                else:
                    self._origine = 'SANDRE'
            elif self._origine == 'SIRET':
                if len(str(code)) != 14:
                    raise ValueError('SIRET code must be 14 bytes long')
                # else:  # self.origine == 'SANDRE'
            self._code = code
        except:
            raise

    # -- property origine --
    @property
    def origine(self):
        """Origine du code intervenant."""
        return self._origine

    @origine.setter
    def origine(self, origine):
        if origine is None:
            self._origine = None
            return
        try:
            origine = unicode(origine.upper())
            # check origine
            if origine == 'I':
                origine = "SIRET"
            elif origine == 'A':
                origine = 'SANDRE'
            if origine not in ('SIRET', 'SANDRE'):
                raise ValueError('origine must be SIRET or SANDRE')
            # check with code
            if (self.code is not None)              \
                    and (len(str(self.code)) != 14) \
                    and (origine == 'SIRET'):
                raise ValueError('SIRET code must be 14 bytes long')
            self._origine = origine
        except:
            raise

    # -- property contacts --
    @property
    def contacts(self):
        """contacts."""
        return self._contacts

    @contacts.setter
    def contacts(self, contacts):
        self._contacts = []
        if contacts is None:
            return
        if isinstance(contacts, Contact):
            contacts = [contacts]
        for contact in contacts:
            # some checks
            if not isinstance(contact, Contact):
                raise TypeError(
                    'contacts must be a Contact or an iterable of Contact'
                )
            # add station
            self._contacts.append(contact)

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'Intervenant {0} {1}::{2} [{3} contact{4}]'.format(
            self.origine or '<sans origine>',
            self.code or '<sans code>',
            self.mnemo or '<sans mnemo>',
            len(self.contacts),
            '' if (len(self.contacts) < 2) else 's'
        ).encode('utf-8')


#-- class Contact --------------------------------------------------------------
class Contact(object):
    """Classe Contact.

    Classe pour manipuler des contacts.

    Proprietes:
        code (entier < 9999, defaut 0)
        nom (string)
        prenom (string)
        civilite (entier parmi NOMENCLATURE[538])
        intervenant (Intervenant)

    """

    # TODO - Contact other properties

    # profil
    # telephone
    # portable
    # fax
    # mel
    # pays
    # alias
    # dtactivation
    # dtdesactivation
    # dtmaj
    # profiladmin

    # Adresse

    def __init__(
        self, code=0, nom=None, prenom=None, civilite=None, intervenant=None
    ):
        """Constructeur.

        Arguments:
            code (entier < 9999, defaut 0)
            nom (string)
            prenom (string)
            civilite (entier parmi NOMENCLATURE[538])
            intervenant (Intervenant) = intervenant de rattachement

        """

        # -- simple properties --
        self.nom = self.prenom = None
        if nom:
            self.nom = unicode(nom)
        if prenom:
            self.prenom = unicode(prenom)

        # -- full properties --
        self.code = code
        self.civilite = civilite
        self.intervenant = intervenant

    # -- property code --
    @property
    def code(self):
        """Code du contact."""
        return self._code

    @code.setter
    def code(self, code):
        try:
            code = int(code)
            if not (0 <= code <= 9999):
                    raise ValueError('code must be in range 0-9999')
            self._code = code
        except:
            raise

    # -- property civilite --
    @property
    def civilite(self):
        """Civilite du contact."""
        return self._civilite

    @civilite.setter
    def civilite(self, civilite):
        if civilite is None:
            self._civilite = None
            return
        try:
            civilite = int(civilite)
            if civilite not in _NOMENCLATURE[538]:
                raise ValueError('civilite incorrect')
            self._civilite = civilite
        except:
            raise

    # -- property intervenant --
    @property
    def intervenant(self):
        """Intervenant de rattachement du contact."""
        return self._intervenant

    @intervenant.setter
    def intervenant(self, intervenant):
        if intervenant is None:
            self._intervenant = None
        else:
            if not isinstance(intervenant, Intervenant):
                raise TypeError('intervenant must be an Intervenant')
            self._intervenant = intervenant

    # -- other methods --
    def __str__(self):
        """String representation."""
        return 'Contact {0}::{1} {2} {3}'.format(
            self.code or '<sans code>',
            _NOMENCLATURE[538][self.civilite] if self.civilite
            else '<sans civilite>',
            self.nom or '<sans nom>',
            self.prenom or '<sans prenom>'
        ).encode('utf-8')


# -- Class Adresse ------------------------------------------------------------
class Adresse(object):
    """Classe Adresse."""

    def __init__(self):
        raise NotImplementedError

    # adresse1
    # adresse2
    # lieudit
    # bp
    # cp
    # localite
    # pays

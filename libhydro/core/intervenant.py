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

import sys as _sys

from .nomenclature import NOMENCLATURE as _NOMENCLATURE


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1e"""
__date__ = """2014-02-20"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - use the BD Hydro intervenants list


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

    # Intervenant other properties

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
        """Initialisation.

        Arguments:
            code (int, defaut 0) = code SIRET (14 chiffres) ou Sandre
            origine (string in ((S)I(RET), (S)A(NDRE)), defaut SIRET pour un
                code a 14 chiffres, sinon SANDRE) = origine du code
            nom (string) = nom de l'intervenant
            mnemo (string) = mnemonique
            contacts (un Contact ou un iterable de Contact)

        """

        # -- simple properties --
        self.nom = self.mnemo = None
        self.nom = unicode(nom) if (nom is not None) else None
        self.mnemo = unicode(mnemo) if (mnemo is not None) else None

        # -- full properties --
        self._code = 0
        self._origine = None  # don't move it !
        self.code = code
        if origine is not None:  # required
            self.origine = origine
        self._contacts = None
        self.contacts = contacts

    # -- property code --
    @property
    def code(self):
        """Return code intervenant."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code intervenant."""
        # None case
        if code is None:
            raise TypeError('code is required')

        # other cases
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

            # all is well
            self._code = code

        except:
            raise

    # -- property origine --
    @property
    def origine(self):
        """Return origine."""
        return self._origine

    @origine.setter
    def origine(self, origine):
        """Set origine."""
        # None case
        if origine is None:
            raise ValueError('origine must be SIRET or SANDRE')

        # other cases
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
            if (origine == 'SIRET')                \
                    and (self.code is not None)    \
                    and (len(str(self.code)) != 14):
                raise ValueError('SIRET code must be 14 bytes long')
            # all is well
            self._origine = origine

        except:
            raise

    # -- property contacts --
    @property
    def contacts(self):
        """Return contacts."""
        return self._contacts

    @contacts.setter
    def contacts(self, contacts):
        """Set contacts."""
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
            if (contact.intervenant is not None) \
                    and (contact.intervenant != self):
                raise ValueError(
                    'contact %s is already linked with intervenant %s' % (
                        contact.code if (contact.code is not None)
                        else '<sans code>',
                        contact.intervenant.code
                        if (contact.intervenant.code is not None)
                        else '<sans code>'
                    )
                )
            # add contact
            contact.intervenant = self
            self._contacts.append(contact)

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Intervenant {0} {1}::{2} [{3} contact{4}]'.format(
            self.origine or '<sans origine>',
            self.code or '<sans code>',
            self.mnemo or '<sans mnemo>',
            len(self.contacts),
            '' if (len(self.contacts) < 2) else 's'
        )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


#-- class Contact -------------------------------------------------------------
class Contact(object):

    """Classe Contact.

    Classe pour manipuler des contacts.

    Proprietes:
        code (entier < 9999)
        nom (string)
        prenom (string)
        civilite (entier parmi NOMENCLATURE[538])
        intervenant (Intervenant)

    """

    # Contact other properties

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
        self, code=None, nom=None, prenom=None, civilite=None, intervenant=None
    ):
        """Initialisation.

        Arguments:
            code (entier < 9999)
            nom (string)
            prenom (string)
            civilite (entier parmi NOMENCLATURE[538])
            intervenant (Intervenant) = intervenant de rattachement

        """

        # -- simple properties --
        self.nom = unicode(nom) if (nom is not None) else None
        self.prenom = unicode(prenom) if (prenom is not None) else None

        # -- full properties --
        self._code = self._civilite = self._intervenant = None
        self.code = code
        self.civilite = civilite
        self.intervenant = intervenant

    # -- property code --
    @property
    def code(self):
        """Return Code contact."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code contact."""
        try:

            # None case
            # if code is None:
            #     raise TypeError('code is required')

            # other cases
            if code is not None:
                code = int(code)
                if not (0 <= code <= 9999):
                    raise ValueError('code must be in range 0-9999')

            # all is well
            self._code = code

        except:
            raise

    # -- property civilite --
    @property
    def civilite(self):
        """Return civilite."""
        return self._civilite

    @civilite.setter
    def civilite(self, civilite):
        """Set civilite."""
        try:

            if civilite is not None:
                civilite = int(civilite)
                if civilite not in _NOMENCLATURE[538]:
                    raise ValueError('civilite incorrect')
            self._civilite = civilite

        except:
            raise

    # -- property intervenant --
    @property
    def intervenant(self):
        """Return intervenant de rattachement du contact."""
        return self._intervenant

    @intervenant.setter
    def intervenant(self, intervenant):
        """Set intervenant de rattachement du contact."""
        if intervenant is not None:
            if not isinstance(intervenant, Intervenant):
                raise TypeError('intervenant must be an Intervenant')
        self._intervenant = intervenant

    # -- other methods --
    def __unicode__(self):
        """Return unicode representation."""
        return 'Contact {0}::{1} {2} {3}'.format(
            self.code or '<sans code>',
            _NOMENCLATURE[538][self.civilite] if self.civilite
            else '<sans civilite>',
            self.nom or '<sans nom>',
            self.prenom or '<sans prenom>'
        )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


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

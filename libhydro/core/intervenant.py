# coding: utf-8
"""Module intervenant.

Ce module contient les classes:
    # Intervenant
    # Contact

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

from .nomenclature import NOMENCLATURE as _NOMENCLATURE
from . import _composant


# -- strings ------------------------------------------------------------------
__version__ = '0.3.2'
__date__ = '2017-05-04'

# HISTORY
# V0.3 - 2017-04-28
#   ajout de contact.profil et des proprietes derivees
#   le code d'un contact est obligatoire
#   fix Contact.code type
#   some refactoring
# V0.2 - 2014-03-02
#   use descriptors
# V0.1 - 2013-08-20
#   first shot


# -- todos --------------------------------------------------------------------
# PROGRESS - Intervenant 50% - Contact 30%
# TODO - use the BD Hydro intervenants list


# -- Class Intervenant --------------------------------------------------------
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

    def __init__(self, code=0, origine=None, nom=None, mnemo=None,
                 contacts=None):
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
        self.nom = str(nom) if (nom is not None) else None
        self.mnemo = str(mnemo) if (mnemo is not None) else None

        # -- full properties --
        self._code = 0
        self._origine = None  # don't move it !
        self.code = code
        if origine is not None:  # required
            self.origine = origine
        self._contacts = None
        self.contacts = contacts

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
            origine = str(origine.upper())
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
                    'contacts must be a Contact or an iterable of Contact')
            if (contact.intervenant is not None) \
                    and (contact.intervenant != self):
                raise ValueError(
                    'contact %s is already linked with intervenant %s' % (
                        contact.code if (contact.code is not None)
                        else '<sans code>',
                        contact.intervenant.code
                        if (contact.intervenant.code is not None)
                        else '<sans code>'))
            # add contact
            contact.intervenant = self
            self._contacts.append(contact)

    __all__attrs__ = ('code', 'origine', 'nom', 'mnemo', 'contacts')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__

    def __unicode__(self):
        """Return unicode representation."""
        # init nom
        if self.nom is not None:
            nom = self.nom
        elif self.mnemo is not None:
            nom = self.mnemo
        else:
            nom = '<sans nom>'
        # action !
        return 'Intervenant {0} {1}::{2} [{3} contact{4}]'.format(
            self.origine if self.origine is not None else '<sans origine>',
            self.code if self.code is not None else '<sans code>',
            nom,
            len(self.contacts),
            '' if (len(self.contacts) < 2) else 's')

    __str__ = _composant.__str__


# -- class Contact ------------------------------------------------------------
class Contact(object):

    """Classe Contact.

    Classe pour manipuler des contacts.

    Proprietes:
        code (string(5))
        nom (string)
        prenom (string)
        civilite (entier parmi NOMENCLATURE[538])
        intervenant (Intervenant)
        profil (0 < int < 7) = masque de bits sur 1 octet
            administrateur national / modelisateur / institutionnel
        profiladminnat (bool)
        profilmodel (bool)
        profilinst (bool)
        profilpublic (bool) = un contact a un profil public lorsque tous les
            elements du profil sont False (identique a profil = 0)

    Proprietes en lecture seule:
        profilasstr (string)

    """

    # Contact other properties

    # telephone
    # portable
    # fax
    # mel
    # pays
    # alias
    # dtactivation
    # dtdesactivation
    # dtmaj

    # Adresse

    civilite = _composant.Nomenclatureitem(nomenclature=538, required=False)

    def __init__(self, code=None, nom=None, prenom=None, civilite=None,
                 intervenant=None, profil=0):
        """Initialisation.

        Arguments:
            code (string(5))
            nom (string)
            prenom (string)
            civilite (entier parmi NOMENCLATURE[538])
            intervenant (Intervenant) = intervenant de rattachement
            profil (binary string ou entier, defaut 0)

        """

        # -- simple properties --
        self.nom = str(nom) if (nom is not None) else None
        self.prenom = str(prenom) if (prenom is not None) else None

        # -- descriptors --
        self.civilite = civilite

        # -- full properties --
        self._code = self._civilite = self._intervenant = None
        self._profil = 0
        self.code = code
        self.civilite = civilite
        self.intervenant = intervenant
        self.profil = profil

    @property
    def code(self):
        """Return Code contact."""
        return self._code

    @code.setter
    def code(self, code):
        """Set code contact."""
        try:

            # None case
            if code is None:
                raise TypeError('code is required')

            # other cases
            if code is not None:
                code = str(code).strip()
                if len(code) == 0:
                    raise ValueError('code is an empty string')
                if len(code) > 5:
                    raise ValueError('maximum code length is 5')

            # all is well
            self._code = code

        except:
            raise

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

    @property
    def profil(self):
        """Return profil."""
        return self._profil

    @profil.setter
    def profil(self, profil):
        """Set profil.

        Argument:
            profil (binary as string ou entier)

        """
        try:
            if isinstance(profil, str):
                profil = int(profil, 2)
            if not (0 <= profil <= 7):
                raise ValueError('invalid profil {}'.format(profil))
            self._profil = profil

        except:
            raise

    @property
    def profiladminnat(self):
        """Return profiladminnat."""
        # return bit 1: 4=int('100', 2)
        return self._profil & 4 != 0

    @profiladminnat.setter
    def profiladminnat(self, status):
        """Set profiladminnat."""
        try:
            if bool(status):
                # set bit 1 to True with 4=int('100', 2)
                self._profil |= 4
            else:
                # set bit 1 to False with 3=int('011', 2)
                self._profil &= 3
        except Exception:
            raise ValueError('status should be a boolean')

    @property
    def profilmodel(self):
        """Return profilmodel."""
        # return bit 2: 2=int('010', 2)
        return self._profil & 2 != 0

    @profilmodel.setter
    def profilmodel(self, status):
        """Set profilmodel."""
        try:
            if bool(status):
                # set bit 2 to True with 2=int('010', 2)
                self._profil |= 2
            else:
                # set bit 2 to False with 5=int('101', 2)
                self._profil &= 5
        except Exception:
            raise ValueError('status should be a boolean')

    @property
    def profilinst(self):
        """Return profilinst."""
        # return bit 3: 1=int('001', 2)
        return self._profil & 1 != 0

    @profilinst.setter
    def profilinst(self, status):
        """Set profilinst."""
        try:
            if bool(status):
                # set bit 3 to True with 1=int('001', 2)
                self._profil |= 1
            else:
                # set bit 3 to False with 6=int('110', 2)
                self._profil &= 6
        except Exception:
            raise ValueError('status should be a boolean')

    @property
    def profilpublic(self):
        """Return profilpublic."""
        return self._profil == 0

    @profilpublic.setter
    def profilpublic(self, status):
        """Set profilpublic."""
        try:
            # 7=bin('111', 2)
            self._profil = 0 if bool(status) else 7
        except Exception:
            raise ValueError('status should be a boolean')

    @property
    def profilasstr(self):
        """Return profil as a 3 chars string."""
        return '{:0=3b}'.format(self._profil)

    # -- special methods --
    __all__attrs__ = ('code', 'nom', 'prenom', 'civilite', 'intervenant',
                      'profil')
    __eq__ = _composant.__eq__
    __ne__ = _composant.__ne__
    __hash__ = _composant.__hash__

    def __unicode__(self):
        """Return unicode representation."""
        # init civilite
        try:
            civilite = _NOMENCLATURE[538][self.civilite]
        except Exception:
            civilite = '<sans civilite>'
        # init intervenant
        if (self.intervenant is None) or (self.intervenant.code is None):
            intervenant = '<sans intervenant>'
        else:
            intervenant = 'intervenant %s' % self.intervenant.code
        # action !
        return 'Contact {0}::{1} {2} {3} [{4}]'.format(
            self.code if self.code is not None else '<sans code>',
            civilite,
            self.nom if self.nom is not None else '<sans nom>',
            self.prenom if self.prenom is not None else '<sans prenom>',
            intervenant)

    __str__ = _composant.__str__


# -- Class Adresse ------------------------------------------------------------
# class Adresse(object):
#
#     """Classe Adresse."""
#
#     def __init__(self):
#         raise NotImplementedError
#
#     # adresse1
#     # adresse2
#     # lieudit
#     # bp
#     # cp
#     # localite
#     # pays

# -*- coding: utf-8 -*-
"""Module bdhydro.

Ce module expose les classes:
    # BdHydroWsClient, un client soap permettant de dialoguer avec les WS
          Bdhydro

Il contient une classe d'erreur specifique:
    # BdhydroError

"""
# TODO - # ChargeurCriteres, un file loader qui permet de lire depuis un
#          fichier la requete pour le WS 'rechercherStationHydro'
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys as _sys
import suds as _suds
from lxml import etree as _etree

from ..conv.xml import Message


#-- strings -------------------------------------------------------------------
__author__ = """Camilo.montes @ Synapse Informatique"""
__maintainer__ = """Philippe Gouin """ \
                 """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.2a"""
__date__ = """2014-04-22"""

#HISTORY
#V0.1 - 2013-10-31
#    first shot


#-- class BdhydroError ------------------------------------------------------
class BdhydroError(Exception):

    """Class BdhydroError."""

    def __init__(self, value):
            self.value = value

    def __unicode__(self):
        """Unicode representation."""
        return self.value

    def __str__(self):
        """String representation."""
        if _sys.version[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)


#-- class Error ---------------------------------------------------------------
class _Error(object):

    """A WS BDHYDRO error."""

    # Errors types:
    #     ErreurParametres, ErreurAuthentification, ErreurXSDSandre
    #     ErreurXSDSchapi, ErreurRole, ErreurBdtr

    def __init__(self, error, text):
        self.error = error
        self.text = text

    @staticmethod
    def fromelement(element):
        """Return an Error from an etree element."""
        if element is not None:
            return _Error(element.tag, element.text)


#-- class Report --------------------------------------------------------------
class _Report(object):

    """A WS BDHYDRO report."""

    def __init__(self, service, date, errors=None, infos=None, warnings=None):
        # TODO - docstring, properties ?
        self.service = service  # string
        self.date = date  # datetime
        self.errors = errors or []  # a list of strings
        self.infos = infos or []  # a list of strings
        self.warnings = warnings or []  # a list of strings

    # -- other methods --
    def __unicode__(self):
        """Unicode representation."""
        # add a spacer before each item
        # TODO - factorize
        errors = ('{}{}'.format(' ' * 4, error) for error in self.errors)
        infos = ('{}{}'.format(' ' * 4, info) for info in self.infos)
        warnings = (
            '{}{}'.format(' ' * 4, warning) for warning in self.warnings
        )

        # action
        return "Rapport du WS '{}' execute le {}\n" \
               'Errors\n:{}' \
               'Infos\n:{}' \
               'Warnings\n:{}'.format(
                   self.service or '<sans nom>',
                   self.date or '<sans date>',
                   '\n'.join(errors),
                   '\n'.join(infos),
                   '\n'.join(warnings)
               )

    def __str__(self):
        """String representation."""
        if _sys.version[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)

    @staticmethod
    def fromxml(xml):
        # TODO - docstring
        # init
        parser = _etree.XMLParser(
            remove_blank_text=True, remove_comments=True, ns_clean=True
        )
        tree = _etree.parse(xml, parser=parser)

        # parse
        if tree is not None:
            service = tree.find('NomService').text
            date = tree.find('DateTraitement').text
            errors = [
                _Error.fromelement(e) for e in tree.find('Erreurs')
            ]
            infos = [
                e.text for e in tree.findall('Informations/Information')
            ]
            warnings = [
                e.text for e in tree.findall('Avertissements/Avertissement')
            ]

            # return
            return _Report(
                service=service,
                date=date,
                errros=errors,
                infos=infos,
                warnings=warnings
            )


#-- class Answer --------------------------------------------------------------
class Answer(object):

    """A WS BDHYDRO answer."""

# STATUTS
# 0 Exécution correcte du service Web
# 1 Une erreur liée aux paramètres d’entrées est survenue
# 2 Une erreur liée à l’authentification est survenue
# 3 Une erreur liée à la validation XML par le XSD Sandre est survenue
# 4 Une erreur liée à la validation XML par le XSD SCHAPI est survenue
# 5 Une erreur liée aux contraintes de la base de données est survenue
# 6 Une erreur liée aux rôles de l’utilisateur est survenue
# 7 Une erreur liée à la recherche est survenue

    def __init__(self, status, report, xml):
        self.status = status
        self.report = report
        self.xml = xml

    @staticmethod
    def fromjson(json):
        # TODO
        pass


#-- BDHydroWsClient -----------------------------------------------------------
# # If you don't expect your WSDL to change often, you have two options that
# # can buy you a lot of speed:
# #     - downloading your WSDL to localhost
# #     - using caching
# # [ref: http://stackoverflow.com/questions/7739613/
# #       python-soap-client-use-suds-or-something-else
# # ]
#
#
#-- class Bdhydro -------------------------------------------------------------
# class Session(_suds.client.Client):
#     """Classe Session.
#
#     Sous classe de suds.Client pour ouvrir une session sur une BdHydro.
#
#     L'utilisation d'un wsdl local (fichier) ameliore les performances.
#
#     Les methodes sont un enrobage de celles contenues dans le wsdl.
#
#     """
#
#     # TODO - wsdl caching
#
#     def __init__(
#         self, user=None, password=None,
#         file=None,
#         host=None, wsdl=_os.path.join('wssoap', 'bdtr.wsdl'), proxy=None
#
#     ):
#         """Initialisation.
#
#         Si file n'est pas nul, les parametres host, wsdl et proxy sont ignores.
#
#         Arguments:
#             user, passwd (strings ou None pour une session anonyme)
#             file (string) = nom de fichier wsdl local
#             host, wsdl, proxy (strings)
#
#         """
#
#         # get the Client
#         super(Session, self).__init__(
#             'file:{}'.format(file) if (file is not None)
#             else 'http://{}/{}'.format(host, wsdl),
#             proxy=proxy
#         )
#
#         # open session
#         reply = self.service['AuthentificationPort'].authentifier(
#             user, password
#         )
#         self.idsession = reply['idsession']

class BdHydroWsClient(object):

    def __init__(self, url=None, user=None, pwd=None, useAuth=False):
        """Constructeur.

        Initialise un client SOAP en utilisant les parametres s'ils existent,
        a partir du fichier de configuration le cas echeant.

        Arguments:
            url  (string: url du webservice BDHydro)
            user (string: nom utilisateur si le ws requiere authentification)
            pwd  (string: mot de passe si le ws requiere authentification)
            useAuth (bool: True pour invoquer le service d'authentification
            des l'initialisation, False sinon)

        """

        if url is None:
            self.loadConfiguration(PATH_CONFIG)
        else:
            self.url = url
            self.user = user
            self.pwd = pwd
            self.useAuth = useAuth

        self._client = _suds.client.Client(self.url)

        if useAuth:
            try:
                if self.user is not None and self.pwd is not None:
                    self.authentifier(self.user, self.pwd, True)
            except AttributeError as ae:
                MigrationFatalError(u'WS002', None, ae)

        else:
            self._idSession = None

    def __handleWebServiceScenarioResult(self, wsResult, tmpFile):
        if wsResult['xmlprevcrues'] is not None:
            f = open(tmpFile, 'w')
            f.write(wsResult['xmlprevcrues'].encode('utf8'))
            f.close()
            message = Message.from_file(tmpFile)
            return message
        else:
            raise ValueError(
                'Impossible de traiter la reponse: balise xmlprevcrues absente'
            )

    def __handleWebServiceError(self, wsResult):
        if wsResult['rapport'] is not None:
            rapport = WSRapport.parseFromString(wsResult['rapport'])
            raise MigrationFatalError(u'WS003', rapport)
        else:
            msgErreur = u'La balise <{0}> est attendu mais non trouvée'
            raise MigrationFatalError(u'WS004', msgErreur.format('rapport'))

    # -- property client --
    @property
    def client(self):
        """Client Soap pour interroger le webservice BDHydro."""
        return self._client

    # -- property idSession --
    @property
    def idSession(self):
        """Sauvegarde l'id de session pour le reutiliser à la volée."""
        return self._idSession

    # -- other methods --
    def loadConfiguration(self, pathFichier):
        """ Charge la configuration du ws depuis un fichier, généralement
         appelé 'config.ini'.

            Arguments:
                pathFichier (chemin vers le fichier de configuration)
         """
        config = ConfigParser()
        config.read(pathFichier)
        try:
            self.url = config.get(u'WS_BDTR', u'WS_BDTR_URL')
            self.user = config.get(u'WS_BDTR', u'WS_BDTR_USER')
            self.pwd = config.get(u'WS_BDTR', u'WS_BDTR_PWD')
            self.useAuth = config.getboolean(u'WS_BDTR', u'WS_BDTR_AUTH')
        except (NoSectionError, MissingSectionHeaderError, NoOptionError) as e:
            messageErreur = u"le fichier {0} n'as pas le bon format";
            raise MigrationFatalError(u'CONF003',
                                      messageErreur.format(self.pathFichierConfig),
                                      e)
        except ParsingError as e:
            messageErreur = u"impossible de parser le fichier {0}";
            raise MigrationFatalError(u'CONF003',
                                      messageErreur.format(self.pathFichierConfig),
                                      e)
        except:
            raise MigrationFatalError(u'CONF003', None, e)

    # -- services exposés et utilisés --
    def authentifier(self, utilisateur, mdp, keepAuth):
        """Surcouche pour faciliter l'appel du webservice 'authentifier'"""

        try:
            self.client.set_options(port='AuthentificationPort')
            result = self.client.service.authentifier(utilisateur, mdp)
        except Exception as e:
            raise MigrationFatalError('WS004', 'authentifier', e)

        if result['statut'] == 0:
            if keepAuth:
                if result['idsession'] is not None:
                    self._idSession = result["idsession"]
                    log.info(u"Authentification au WebService reussie");
                    log.debug(u"Id de session: {0}".format(self._idSession))
                else:
                    raise AttributeError(u'Authentification demandee mais aucune session obtenue')
        else:
            self.__handleWebServiceError(result)

        return result

    def rechercherStationHydro(self, xmlrecherche):
        """Surcouche pour faciliter l'appel du webservice 'rechercherStationHydro'"""

        try:
            self.client.set_options(port=u'RecherchePublicationPort')
            if self.idSession is not None:
                result = self.client.service.rechercherStationHydro(idsession = self.idSession, xmlrecherche = xmlrecherche, typeretour = True)
            else:
                result = self.client.service.rechercherStationHydro(xmlrecherche = xmlrecherche, typeretour = True)
        except Exception as e:
            raise MigrationFatalError(u'WS004', u'rechercherStationHydro', e)

        message = None
        if result['statut'] == '0':
            message = self.__handleWebServiceScenarioResult(result, PATH_TMP_RECHERCHE)
            log.debug(u"L'appel au WebService 'rechercherStationHydro' s'est deroule correctement")
        else:
            self.__handleWebServiceError(result)

        return message

    def publierStationHydroListe(self, codesStations, dateMaj):
        """Surcouche pour faciliter l'appel du webservice 'publierStationHydroListe'"""

        try:
            self.client.set_options(port=u'SiteHydroPublicationPort')
            if self.idSession is not None:
                if dateMaj is not None:
                    result = self.client.service.publierStationHydroListe(idsession = self.idSession, listecdstationhydro = codesStations, dtmaj = dateMaj)
                else:
                    result = self.client.service.publierStationHydroListe(idsession = self.idSession, listecdstationhydro = codesStations)
            else:
                if dateMaj is not None:
                    result = self.client.service.publierStationHydroListe(listecdstationhydro = codesStations, dtmaj = dateMaj)
                else:
                    result = self.client.service.publierStationHydroListe(listecdstationhydro = codesStations)
        except Exception as e:
            raise MigrationFatalError(u'WS004', u'publierStationHydroListe', e)

        message = None
        if result['statut'] == '0':
            message = self.__handleWebServiceScenarioResult(result, PATH_TMP_STATIONS)
            log.debug(u"L'appel au WebService 'publierStationHydroListe' s'est deroule correctement")
        else:
            self.__handleWebServiceError(result)

        return message

    def publierSiteHydroListe(self, codesSitesHydro, dateMaj):
        """Surcouche pour faciliter l'appel du webservice 'publierSiteHydroListe'"""
        try:
            self.client.set_options(port='SiteHydroPublicationPort')
            if self.idSession is not None:
                if dateMaj is not None:
                    result = self.client.service.publierSiteHydroListe(idsession = self.idSession, listecdsitehydro = codesSitesHydro, dtmaj = dateMaj)
                else:
                    result = self.client.service.publierSiteHydroListe(idsession = self.idSession, listecdsitehydro = codesSitesHydro)
            else:
                if dateMaj is not None:
                    result = self.client.service.publierSiteHydroListe(listecdsitehydro = codesSitesHydro, dtmaj = dateMaj)
                else:
                    result = self.client.service.publierSiteHydroListe(listecdsitehydro = codesSitesHydro)
        except Exception as e:
            raise MigrationFatalError('WS004', 'publierSiteHydroListe', e)

        message = None
        if result['statut'] == '0':
            message = self.__handleWebServiceScenarioResult(result, PATH_TEMP_SITES)
            log.debug(u"L'appel au WebService 'publierSiteHydroListe' s'est deroule correctement")
        else:
            self.__handleWebServiceError(result)

        return message


#-- ChargeurCriteres --------------------------------------------------------
class ChargeurCriteres(object):

    def __init__(self, pathFichier):
        """ Constructeur

        Arguments:
            pathFicher (chemin vers le fichier de configuration)

        """
        self._pathFichier = pathFichier

    # -- property client --
    @property
    def pathFichier(self):
        """ Path vers le fichier de configuration """
        return self._pathFichier

    #-- autres methodes --
    def getCriteresSelectionStations(self):
        """ Lit le fichier de parametrage pour extraire le critere de selection
        des stations """

        #-- lit le fichier et retire les lignes vides, commentaires et namespaces
        parser = etree.XMLParser(remove_blank_text=True,
                                 remove_comments=True,
                                 ns_clean=True)

        #-- charge le fichier sous forme d'arbre xml
        tree = etree.parse(self.pathFichier, parser=parser)
        #-- recupere le premier noeud de l'arbre xml
        noeudRechercheHydro = tree.getroot()

        criteres = None
        #-- verifie que le noeud existe et qu'il correspond au noeud 'RechercheHydro'
        if noeudRechercheHydro is not None and noeudRechercheHydro.tag == 'RechercheHydro':
            #-- transforme le noeud 'RechercheHydro' sous forme de string utf-8
            criteres = etree.tostring(noeudRechercheHydro, encoding='utf8')
            log.debug(u"Les criteres de recherche des stations ont etes charges correctement");
            log.debug(u"    xml charge: {0}".format(criteres))
        else:
            #-- le format du fichier ne correspond pas à ce qui est attendu, on leve un exception
            raise ValueError(u"Le fichier {0} n'est pas valide: impossible de trouver la balise 'RechercheHydro'".format(self.pathFichier))

        return criteres

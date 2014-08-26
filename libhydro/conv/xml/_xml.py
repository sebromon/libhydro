# -*- coding: utf-8 -*-
"""Module xml.classes.

Ce module contient la classe:
    # Message

"""
#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import sys as _sys
import os as _os

from lxml import etree as _etree

from . import (_from_xml, _to_xml)
from libhydro.core import (
    _composant,
    intervenant as _intervenant,
    sitehydro as _sitehydro,
    sitemeteo as _sitemeteo,
    seuil as _seuil,
    modeleprevision as _modeleprevision,
    evenement as _evenement,
    obshydro as _obshydro,
    obsmeteo as _obsmeteo,
    simulation as _simulation
)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.5b"""
__date__ = """2014-08-26"""

#HISTORY
#V0.5 - 2014-08-22
#    add the intervenants
#V0.4 - 2014-07-18
#    add the modelesprevision element
#    add the sitesmeteo and seriesmeteo element
#    use a descriptor for Message components
#V0.1 - 2013-08-20
#    first shot


# -- class Message ------------------------------------------------------------
class Message(object):

    """ClasseMessage.

    Classe pour manipuler les messages Xml hydrometrie.

    Proprietes:
        scenario (xml.Scenario) = un objet Scenario obligatoire
        intervenants (liste d'intervenant.Intervenant)
        siteshydro (liste de sitehydro.Sitehydro)
        sitesmeteo (liste de sitemeteo.Sitemeteo)
        seuilshydro (liste de seuil.Seuilhydro)
        modelesprevision (liste de modeleprevision.Modeleprevision)
        evenements (liste de evenement.Evenement)
        serieshydro (liste de obshydro.Serie)
        seriesmeteo (liste de obsmeteo.Serie)
        simulations (liste de simulation.Simulation)

    """

        # 'courbestarage'
        # 'jaugeages'
        # 'courbescorrection'
        # 'obsselab'
        # 'gradshydro'
        # 'qualifsannee'
        # 'alarmes'

    intervenants = _composant.Rlistproperty(cls=_intervenant.Intervenant)
    siteshydro = _composant.Rlistproperty(cls=_sitehydro.Sitehydro)
    sitesmeteo = _composant.Rlistproperty(cls=_sitemeteo.Sitemeteo)
    seuilshydro = _composant.Rlistproperty(cls=_seuil.Seuilhydro)
    modelesprevision = _composant.Rlistproperty(
        cls=_modeleprevision.Modeleprevision
    )
    evenements = _composant.Rlistproperty(cls=_evenement.Evenement)
    serieshydro = _composant.Rlistproperty(cls=_obshydro.Serie)
    seriesmeteo = _composant.Rlistproperty(cls=_obsmeteo.Serie)
    simulations = _composant.Rlistproperty(cls=_simulation.Simulation)

    def __init__(
        self, scenario, intervenants=None, siteshydro=None, sitesmeteo=None,
        seuilshydro=None, modelesprevision=None, evenements=None,
        serieshydro=None, seriesmeteo=None, simulations=None,
        strict=True
    ):
        """Initialisation.

        Arguments:
            scenario (xml.Scenario) = un objet Scenario obligatoire
            intervenants (intervenant.Intervenant iterable ou None)
            siteshydro (sitehydro.Sitehydro iterable ou None)
            sitesmeteo (sitemeteo.Sitemeteo iterable ou None)
            seuilshydro (seuil.Seuilhydro iterable ou None)
            modelesprevision (modeleprevision.Modeleprevision iterable ou None)
            evenements (evenement.Evenement iterable ou None)
            serieshydro (obshydro.Serie iterable ou None)
            seriesmeteo (obsmeteo.Serie iterable ou None)
            simulations (simulation.Simulation iterable ou None)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite des elements

        """

        # -- simple properties --
        self._strict = bool(strict)

        # -- adjust the descriptor --
        for key in _to_xml.ORDERED_ACCEPTED_KEYS[1:]:
            vars(self.__class__)[key].strict = self._strict  # Rlist or []
            vars(self.__class__)[key].required = self._strict  # [] or None

        # -- descriptors --
        self.intervenants = intervenants or []
        self.siteshydro = siteshydro or []
        self.sitesmeteo = sitesmeteo or []
        self.seuilshydro = seuilshydro or []
        self.modelesprevision = modelesprevision or []
        self.evenements = evenements or []
        self.serieshydro = serieshydro or []
        self.seriesmeteo = seriesmeteo or []
        self.simulations = simulations or []

        # -- full properties --
        self._scenario = None
        self.scenario = scenario

    # -- property scenario --
    @property
    def scenario(self):
        """Return scenario."""
        return self._scenario

    @scenario.setter
    def scenario(self, scenario):
        """Set scenario."""
        try:

            # None case
            if scenario is None:
                raise TypeError('scenario is required')

            # other cases
            if (
                self._strict
                and not isinstance(scenario, _from_xml.Scenario)
            ):
                raise TypeError('scenario incorrect')

            # all is well
            self._scenario = scenario

        except:
            raise

    # -- static methods --
    @staticmethod
    def from_file(src, ordered=False):
        """Parse le fichier src et retourne un xml.Message.

        Supprime les eventuels namespaces.

        Arguments:
            src (nom de fichier, url, objet fichier...) = source de donnee. Les
                type de src acceptes sont ceux de lxml.etree.parse
            ordered (bool, defaut False) = si True essaie de conserver l'ordre
                de certains elements

        """
        # read the file
        parser = _etree.XMLParser(
            remove_blank_text=True, remove_comments=True, ns_clean=True
        )
        tree = _etree.parse(src, parser=parser)

        # remove all existing namespaces
        # standard nsmap should be: {
        #     None: 'http://xml.sandre.eaufrance.fr/scenario/hydrometrie/1.1',
        #    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        # }
        nsmap = tree.getroot().nsmap
        if nsmap != {}:
            for alias in nsmap:
                _remove_namespace(tree.getroot(), nsmap[alias])

        return Message(
            scenario=_from_xml._scenario_from_element(
                tree.find('Scenario')
            ),
            intervenants=_from_xml._intervenants_from_element(
                tree.find('RefHyd/Intervenants')
            ),
            siteshydro=_from_xml._siteshydro_from_element(
                tree.find('RefHyd/SitesHydro')
            ),
            sitesmeteo=_from_xml._sitesmeteo_from_element(
                tree.find('RefHyd/SitesMeteo')
            ),
            seuilshydro=_from_xml._seuilshydro_from_element(
                element=tree.find('RefHyd/SitesHydro'),
                ordered=ordered
            ),
            modelesprevision=_from_xml._modelesprevision_from_element(
                tree.find('RefHyd/ModelesPrevision')
            ),
            evenements=_from_xml._evenements_from_element(
                tree.find('Donnees/Evenements')
            ),
            serieshydro=_from_xml._serieshydro_from_element(
                tree.find('Donnees/Series')
            ),
            seriesmeteo=_from_xml._seriesmeteo_from_element(
                tree.find('Donnees/ObssMeteo')
            ),
            simulations=_from_xml._simulations_from_element(
                tree.find('Donnees/Simuls')
            )
        )

            # 'courbestarage'
            # 'jaugeages'
            # 'courbescorrection'
            # 'obsselab'
            # 'gradshydro'
            # 'qualifsannee'
            # 'alarmes'

    # -- other methods --
    def add(self, **kargs):
        """Ajoute des elements au Message.

        Les elements a ajouter doivent etre passes sous la forme:
            Message.add(cle=valeur, ...)

        avec les regles suivantes:
            CLE PARMI    /      VALEUR
            intervenants = iterable d'intervenant.Intervenant
            siteshydro   = iterable de sitehydro.Sitehydro
            sitesmeteo   = iterable de sitemeteo.Sitemeteo
            seuilshydro  = iterable de seuil.Seuilhydro
            modelesprevision = iterable de modeleprevision.Modeleprevision
            evenements   = iterable d'evenement.Evenement
            serieshydro  = iterable de obshydro.Serie
            seriesmeteo  = iterable de obsmeteo.Serie
            simulations  = iterable de simulation.Simulation

        """
        for key in kargs:

            if key not in _to_xml.ORDERED_ACCEPTED_KEYS:
                raise TypeError('key {} not accepted'.format(key))

            try:
                items = self.__getattribute__(key)
                items.extend(kargs[key])
                self.__setattr__(key, items)

            except Exception, e:
                raise ValueError('bad element, {}'.format(e))

    def write(
        self, file, encoding='utf-8', compression=0, force=False,
        bdhydro=False, ordered=False
    ):
        """Ecrit le Message dans le fichier dst.

        Cette methode est un wrapper autour de lxml.etree.ElementTree.write.
        Se referer a la documentation de lxml pour le detail des options.

        Arguments:
            file (str ou objet fichier)
            encoding (string)
            compression (int de 0 a 9) = niveau de compression gzip
            force (bool, defaut False) = ecrase un fichier deja existant
            bdhydro (bool, defaut False) = utilise le format bdhydro
            ordered (bool, defaut False) = si True essaie de conserver l'ordre
                de certains elements

        """
        # check file
        if (not force) and (_os.path.isfile(file)):
            raise IOError('file already exists')
        # procede !
        tree = _etree.ElementTree(
            _to_xml._to_xml(
                scenario=self.scenario,
                intervenants=self.intervenants,
                siteshydro=self.siteshydro,
                sitesmeteo=self.sitesmeteo,
                seuilshydro=self.seuilshydro,
                modelesprevision=self.modelesprevision,
                evenements=self.evenements,
                serieshydro=self.serieshydro,
                seriesmeteo=self.seriesmeteo,
                simulations=self.simulations,
                bdhydro=bdhydro,
                ordered=ordered,
                strict=self._strict
            )
        )
        tree.write(
            file=file,
            encoding=encoding,
            method='xml',
            pretty_print=False,
            xml_declaration=True,
            compression=compression
        )

    def show(self, bdhydro=False, ordered=False):
        """Return a pretty print XML.

       Arguments:
            bdhydro (bool, defaut False) = utilise le format bdhydro
            ordered (bool, defaut False) = si True essaie de conserver l'ordre
                de certains elements

        """
        return _etree.tostring(
            _to_xml._to_xml(
                scenario=self.scenario,
                intervenants=self.intervenants,
                siteshydro=self.siteshydro,
                sitesmeteo=self.sitesmeteo,
                seuilshydro=self.seuilshydro,
                modelesprevision=self.modelesprevision,
                evenements=self.evenements,
                serieshydro=self.serieshydro,
                seriesmeteo=self.seriesmeteo,
                simulations=self.simulations,
                strict=self._strict,
                bdhydro=bdhydro,
                ordered=ordered
            ),
            encoding=_sys.stdout.encoding,
            xml_declaration=1,
            pretty_print=1
        )

    def __unicode__(self):
        """Return unicode representation."""
        try:
            scenario = self.scenario.__unicode__()
        except AttributeError:
            scenario = 'Message <sans scenario>'
        return '{scenario}\n' \
               'Contenu:\n' \
               '{space}{intervenants} intervenants\n' \
               '{space}{siteshydro} siteshydro\n' \
               '{space}{sitesmeteo} sitesmeteo\n' \
               '{space}{seuilshydro} seuilshydro\n' \
               '{space}{modelesprevision} modelesprevision\n' \
               '{space}{evenements} evenements\n' \
               '{space}{serieshydro} serieshydro\n' \
               '{space}{seriesmeteo} seriesmeteo\n' \
               '{space}{simulations} simulations'.format(
                   space=' ' * 4,
                   scenario=scenario,
                   intervenants=0 if self.intervenants is None
                   else len(self.intervenants),
                   siteshydro=0 if self.siteshydro is None
                   else len(self.siteshydro),
                   sitesmeteo=0 if self.sitesmeteo is None
                   else len(self.sitesmeteo),
                   seuilshydro=0 if self.seuilshydro is None
                   else len(self.seuilshydro),
                   modelesprevision=0 if self.modelesprevision is None
                   else len(self.modelesprevision),
                   evenements=0 if self.evenements is None
                   else len(self.evenements),
                   serieshydro=0 if self.serieshydro is None
                   else len(self.serieshydro),
                   seriesmeteo=0 if self.seriesmeteo is None
                   else len(self.seriesmeteo),
                   simulations=0 if self.simulations is None
                   else len(self.simulations)
               )

    __str__ = _composant.__str__


# -- functions ----------------------------------------------------------------
def _remove_namespace(element, namespace):
    """Remove namespace in the passed etree.Element in place."""
    ns = '{%s}' % namespace
    nsl = len(ns)
    for e in element.getiterator():
        if e.tag.startswith(ns):
            e.tag = e.tag[nsl:]

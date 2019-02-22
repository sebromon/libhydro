# coding: utf-8
"""Module xml.classes.

Ce module contient la classe:
    # Message

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import sys as _sys
import os as _os

from lxml import etree as _etree

from . import (_from_xml, _to_xml, sandre_tags as _sandre_tags)
from libhydro.core import (
    _composant,
    intervenant as _intervenant,
    sitehydro as _sitehydro,
    sitemeteo as _sitemeteo,
    seuil as _seuil,
    modeleprevision as _modeleprevision,
    evenement as _evenement,
    courbetarage as _courbetarage,
    courbecorrection as _courbecorrection,
    obshydro as _obshydro,
    obsmeteo as _obsmeteo,
    simulation as _simulation,
    jaugeage as _jaugeage,
    obselaboreehydro as _obselaboreehydro,
    obselaboreemeteo as _obselaboreemeteo)


# -- strings ------------------------------------------------------------------
__version__ = '0.6.1'
__date__ = '2017-07-05'

# HISTORY
# V0.6.1 - SR - 2017-06-22
# Add jaugeages
# V0.6 - SR - 2017-06-22
# Ajout des courbes de correction et de targe au message
# V0.5 - 2014-08-22
#   expose pretty_print in show and write methods
#   add the intervenants
# V0.4 - 2014-07-18
#   add the modelesprevision element
#   add the sitesmeteo and seriesmeteo element
#   use a descriptor for Message components
# V0.1 - 2013-08-20
#   first shot


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
        seuilsmeteo (liste de seuil.Seuilmeteo)
        modelesprevision (liste de modeleprevision.Modeleprevision)
        evenements (liste de evenement.Evenement)
        courbestarage (liste de courbetarage.CourbeTarage)
        jaugeages (liste de jaugeage.Jaugeage)
        courbescorrection (liste de courbecorrection.CourbeCorrection)
        serieshydro (liste de obshydro.Serie)
        seriesmeteo (liste de obsmeteo.Serie)
        seriesobselab (liste de obselaboree.SerieObsElab)
        seriesobselabmeteo (liste de obselaboreemeteo.SerieObsElabMeteo)
        simulations (liste de simulation.Simulation)

    """

    # 'jaugeages'
    # 'obsselab'
    # 'gradshydro'
    # 'qualifsannee'
    # 'alarmes'

    intervenants = _composant.Rlistproperty(cls=_intervenant.Intervenant)
    siteshydro = _composant.Rlistproperty(cls=_sitehydro.Sitehydro)
    sitesmeteo = _composant.Rlistproperty(cls=_sitemeteo.Sitemeteo)
    seuilshydro = _composant.Rlistproperty(cls=_seuil.Seuilhydro)
    seuilsmeteo = _composant.Rlistproperty(cls=_seuil.Seuilmeteo)
    modelesprevision = _composant.Rlistproperty(
        cls=_modeleprevision.Modeleprevision)
    evenements = _composant.Rlistproperty(cls=_evenement.Evenement)
    courbestarage = _composant.Rlistproperty(cls=_courbetarage.CourbeTarage)
    jaugeages = _composant.Rlistproperty(cls=_jaugeage.Jaugeage)
    courbescorrection = _composant.Rlistproperty(cls=_courbecorrection.CourbeCorrection)
    serieshydro = _composant.Rlistproperty(cls=_obshydro.Serie)
    seriesmeteo = _composant.Rlistproperty(cls=_obsmeteo.Serie)
    seriesobselab = _composant.Rlistproperty(cls=_obselaboreehydro.SerieObsElab)
    seriesobselabmeteo = _composant.Rlistproperty(cls=_obselaboreemeteo.SerieObsElabMeteo)
    simulations = _composant.Rlistproperty(cls=_simulation.Simulation)

    def __init__(self, scenario, intervenants=None, siteshydro=None,
                 sitesmeteo=None, seuilshydro=None, seuilsmeteo=None,
                 modelesprevision=None, evenements=None, courbestarage=None,
                 jaugeages=None, courbescorrection=None, serieshydro=None,
                 seriesmeteo=None, seriesobselab=None, seriesobselabmeteo=None,
                 simulations=None, strict=True):
        """Initialisation.

        Arguments:
            scenario (xml.Scenario) = un objet Scenario obligatoire
            intervenants (intervenant.Intervenant iterable ou None)
            siteshydro (sitehydro.Sitehydro iterable ou None)
            sitesmeteo (sitemeteo.Sitemeteo iterable ou None)
            seuilshydro (seuil.Seuilhydro iterable ou None)
            seuilsmeteo (seuil.Seuilmeteo iterable ou None)
            modelesprevision (modeleprevision.Modeleprevision iterable ou None)
            evenements (evenement.Evenement iterable ou None)
            courbestarage (courbetarage.CourbeTarage iterable ou None)
            jaugeages (jaugeage.Jaugeage iterable ou None)
            courbescorrection (courbecorrection.CourbeCorrection ou None)
            serieshydro (obshydro.Serie iterable ou None)
            seriesmeteo (obsmeteo.Serie iterable ou None)
            seriesobselab (obselaboreehydro.SerieObsElab iterable ou None)
            seriesobselabmeteo (obselaboreemeteo.SerieObsElabMeteo iterable ou None)
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
        self.seuilsmeteo = seuilsmeteo or []
        self.modelesprevision = modelesprevision or []
        self.evenements = evenements or []
        self.courbestarage = courbestarage or []
        self.jaugeages = jaugeages or []
        self.courbescorrection = courbescorrection or []
        self.serieshydro = serieshydro or []
        self.seriesmeteo = seriesmeteo or []
        self.seriesobselab = seriesobselab or []
        self.seriesobselabmeteo = seriesobselabmeteo or []
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
            if self._strict and not isinstance(scenario, _from_xml.Scenario):
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
            remove_blank_text=True, remove_comments=True, ns_clean=True)
        tree = _etree.parse(src, parser=parser)
        return Message._from_element_tree(tree, ordered)

    @staticmethod
    def from_string(strxml, ordered=False):
        """Parse le xml fournis sous forme de string et retourne un xml.Message.

        Supprime les eventuels namespaces.

        Arguments:
            strxml (str(unicode) ou bytes) = source de donnee.
            ordered (bool, defaut False) = si True essaie de conserver l'ordre
                de certains elements

        """
        # etree.fromstring cannot parse unicode
        if isinstance(strxml, str):
            root = _etree.fromstring(strxml.encode('utf-8'))
        else:
            root = _etree.fromstring(strxml)

        tree = _etree.ElementTree(root)
        return Message._from_element_tree(tree, ordered)

    @staticmethod
    def _from_element_tree(tree, ordered=False):
        if tree is None:
            return None
        if not isinstance(tree, _etree._ElementTree):
            raise TypeError('tree is not an instance of ElementTree')

        # remove all existing namespaces
        # standard nsmap should be: {
        #     None: 'http://xml.sandre.eaufrance.fr/scenario/hydrometrie/1.1',
        #    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        # }
        nsmap = tree.getroot().nsmap
        if nsmap != {}:
            for alias in nsmap:
                _remove_namespace(tree.getroot(), nsmap[alias])

        scenario = _from_xml._scenario_from_element(tree.find('Scenario'))

        if scenario.version == '2':
            tags = _sandre_tags.SandreTagsV2
            seriesmeteo = _from_xml._seriesmeteo_from_element_v2(
                tree.find('Donnees/SeriesObsMeteo'))
            seriesobselab = _from_xml._seriesobselab_from_element_v2(
                tree.find('Donnees/' + tags.seriesobselabhydro))
            seriesobselabmeteo = _from_xml._seriesobselabmeteo_from_element_v2(
                tree.find('Donnees/SeriesObsElaborMeteo'))
            seuilshydro = _from_xml._seuilshydro_from_element_v2(
                element=tree.find('RefHyd/SeuilsHydro'),
                version=scenario.version, tags=tags)
            sitesmeteo = _from_xml._sitesmeteo_from_element_v2(
                tree.find('RefHyd/SitesMeteo'), version=scenario.version,
                tags=tags)
            seuilsmeteo = _from_xml._seuilsmeteo_from_element_v2(
                element=tree.find('RefHyd/SeuilsMeteo'), version=scenario.version,
                tags=tags)
        else:
            tags = _sandre_tags.SandreTagsV1
            seriesmeteo, seriesobselabmeteo = _from_xml._seriesmeteo_from_element(
                tree.find('Donnees/ObssMeteo'))
            seriesobselab = _from_xml._seriesobselab_from_element(
                tree.find('Donnees/' + tags.seriesobselabhydro))
            seuilshydro = _from_xml._seuilshydro_from_element(
                element=tree.find('RefHyd/SitesHydro'),
                version=scenario.version, tags=tags, ordered=ordered)
            sitesmeteo, seuilsmeteo = _from_xml._sitesmeteo_from_element(
                tree.find('RefHyd/SitesMeteo'), version=scenario.version,
                tags=tags)


        return Message(
            scenario=scenario,
            intervenants=_from_xml._intervenants_from_element(
                tree.find('RefHyd/Intervenants'), scenario.version, tags),
            siteshydro=_from_xml._siteshydro_from_element(
                tree.find('RefHyd/SitesHydro'), scenario.version, tags),
            sitesmeteo=sitesmeteo,
            seuilshydro=seuilshydro,
            seuilsmeteo=seuilsmeteo,
            modelesprevision=_from_xml._modelesprevision_from_element(
                tree.find('RefHyd/ModelesPrevision')),
            evenements=_from_xml._evenements_from_element(
                tree.find('Donnees/Evenements'), scenario.version, tags),
            courbestarage=_from_xml._courbestarage_from_element(
                tree.find('Donnees/CourbesTarage'),
                scenario.version, tags),
            jaugeages=_from_xml._jaugeages_from_element(
                tree.find('Donnees/Jaugeages'),
                scenario.version, tags),
            courbescorrection=_from_xml._courbescorrection_from_element(
                tree.find('Donnees/CourbesCorrH'),
                scenario.version, tags),
            serieshydro=_from_xml._serieshydro_from_element(
                tree.find('Donnees/' + tags.serieshydro),
                scenario.version, tags),
            seriesmeteo=seriesmeteo,
            seriesobselab=seriesobselab,
            seriesobselabmeteo=seriesobselabmeteo,
            simulations=_from_xml._simulations_from_element(
                tree.find('Donnees/Simuls')))

        # 'jaugeages'
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
            seuilsmeteo  = iterable de seuil.Seuilmeteo
            modelesprevision = iterable de modeleprevision.Modeleprevision
            evenements   = iterable d'evenement.Evenement
            courbestarage = iterable de courbetarage.CourbeTarage
            jaugeages = iterable de Jaugeage.Jaugeage
            courbescorrection = iterable de courbecorrection.CourbeCorrection
            serieshydro  = iterable de obshydro.Serie
            seriesmeteo  = iterable de obsmeteo.Serie
            seriesobselab = iterable de obselaboreehydro.SerieObsElab
            simulations  = iterable de simulation.Simulation

        """
        for key in kargs:

            if key not in _to_xml.ORDERED_ACCEPTED_KEYS:
                raise TypeError('key {} not accepted'.format(key))

            try:
                items = self.__getattribute__(key)
                items.extend(kargs[key])
                self.__setattr__(key, items)

            except Exception as e:
                raise ValueError('bad element, {}'.format(e))

    def _to_element(self, bdhydro=False, ordered=False, version=None):
        """Return etree.Element from Message"""
        return _to_xml._to_xml(
                scenario=self.scenario,
                intervenants=self.intervenants,
                siteshydro=self.siteshydro,
                sitesmeteo=self.sitesmeteo,
                seuilshydro=self.seuilshydro,
                seuilsmeteo=self.seuilsmeteo,
                modelesprevision=self.modelesprevision,
                evenements=self.evenements,
                courbestarage=self.courbestarage,
                jaugeages=self.jaugeages,
                courbescorrection=self.courbescorrection,
                serieshydro=self.serieshydro,
                seriesmeteo=self.seriesmeteo,
                seriesobselab=self.seriesobselab,
                simulations=self.simulations,
                bdhydro=bdhydro,
                ordered=ordered,
                strict=self._strict,
                version=version)

    def write(self, file, encoding='utf-8', compression=0, force=False,
              bdhydro=False, ordered=False, pretty_print=False, version=None):
        """Ecrit le Message dans le fichier <file>.

        Cette methode est un wrapper autour de lxml.etree.ElementTree.write.
        Se referer a la documentation de lxml pour le detail des options.

        Arguments:
            file (str ou objet fichier) = fichier de destination
            encoding (string, defaut utf-8) = encodage
            compression (int de 0 a 9, defaut 0) = niveau de compression gzip
            force (bool, defaut False) = ecrase un fichier deja existant
            bdhydro (bool, defaut False) = utilise le format bdhydro
            ordered (bool, defaut False) = si True essaie de conserver l'ordre
                de certains elements
            pretty_print (bool, defaut False) = option de debogage
            version (str or None) = version Sandre 1.1 ou 2
                récupération de la version du scenario si None

        """
        # check for an exisitng file
        if not force and isinstance(file, str) and \
                _os.path.isfile(file):
            raise IOError('file already exists')
        # procede !
        tree = _etree.ElementTree(
            self._to_element(bdhydro, ordered, version))
        tree.write(
            file=file, encoding=encoding, method='xml',
            pretty_print=pretty_print, xml_declaration=True,
            compression=compression)

    def show(self, bdhydro=False, ordered=False, pretty_print=False,
             version=None):
        """Return a pretty print XML.

       Arguments:
            bdhydro (bool, defaut False) = utilise le format bdhydro
            ordered (bool, defaut False) = si True essaie de conserver l'ordre
                de certains elements
            pretty_print (bool, defaut False) = option de debogage

        """
        return _etree.tostring(
            self._to_element(bdhydro, ordered, version),
            encoding=_sys.stdout.encoding,
            xml_declaration=True,
            pretty_print=pretty_print)

    def to_string(self, bdhydro=False, ordered=False, version=None):
        """Return an unicode xml"""
        # encoding=unicode doesn't support xml_declaration
        return _etree.tostring(
                       self._to_element(bdhydro, ordered, version),
                       encoding='UTF-8',
                       xml_declaration=True,
                       pretty_print=False).decode('utf-8')

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
               '{space}{seuilsmeteo} seuilsmeteo\n' \
               '{space}{modelesprevision} modelesprevision\n' \
               '{space}{evenements} evenements\n' \
               '{space}{courbestarage} courbestarage\n' \
               '{space}{jaugeages} jaugeages\n' \
               '{space}{courbescorrection} courbescorrection\n' \
               '{space}{serieshydro} serieshydro\n' \
               '{space}{seriesmeteo} seriesmeteo\n' \
               '{space}{seriesobselab} seriesobselab\n' \
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
                   seuilsmeteo=0 if self.seuilsmeteo is None
                   else len(self.seuilsmeteo),
                   modelesprevision=0 if self.modelesprevision is None
                   else len(self.modelesprevision),
                   evenements=0 if self.evenements is None
                   else len(self.evenements),
                   courbestarage=0 if self.courbestarage is None
                   else len(self.courbestarage),
                   jaugeages=0 if self.jaugeages is None
                   else len(self.jaugeages),
                   courbescorrection=0 if self.courbescorrection is None
                   else len(self.courbescorrection),
                   serieshydro=0 if self.serieshydro is None
                   else len(self.serieshydro),
                   seriesmeteo=0 if self.seriesmeteo is None
                   else len(self.seriesmeteo),
                   seriesobselab=0 if self.seriesobselab is None
                   else len(self.seriesobselab),
                   simulations=0 if self.simulations is None
                   else len(self.simulations))

    __str__ = _composant.__str__


# -- functions ----------------------------------------------------------------
def _remove_namespace(element, namespace):
    """Remove namespace in the passed etree.Element in place."""
    ns = '{%s}' % namespace
    nsl = len(ns)
    for e in element.getiterator():
        if e.tag.startswith(ns):
            e.tag = e.tag[nsl:]

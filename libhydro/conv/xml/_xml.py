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
    # intervenant as _intervenant,
    sitehydro as _sitehydro,
    sitemeteo as _sitemeteo,
    seuil as _seuil,
    # modeleprevision as _modeleprevison,
    evenement as _evenement,
    obshydro as _obshydro,
    obsmeteo as _obsmeteo,
    simulation as _simulation
)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.4a"""
__date__ = """2014-07-18"""

#HISTORY
#V0.4 - 2014-07-18
#    add sitemeteo and obsmeteo
#    use a descriptor for Message components
#V0.1 - 2013-08-20
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - factorize 7 Message properties in a descriptor (except scenario)


# -- class Message ------------------------------------------------------------
class Message(object):

    """ClasseMessage.

    Classe pour manipuler les messages Xml hydrometrie.

    Proprietes:
        scenario (xml.Scenario) = un objet Scenario obligatoire
        siteshydro (sitehydro.Sitehydro collection) = iterable ou None
        sitesmeteo (sitemeteo.Sitemeteo collection) = iterable ou None
        seuilshydro (seuil.Seuilhydro collection) = iterable ou None
        evenements (evenement.Evenement collection) = iterable ou None
        serieshydro (obshydro.Serie collection) = iterable ou None
        seriesmeteo (obsmeteo.Serie collection) = iterable ou None'
        simulations (simulation.Simulation collection) = iterable ou None

    """

        # 'intervenants': 'TODO',
        # 'modelesprevision': 'TODO'

        # 'courbestarage'
        # 'jaugeages'
        # 'courbescorrection'
        # 'obsselab'
        # 'gradshydro'
        # 'qualifsannee'
        # 'alarmes'

    siteshydro = ListMessage_iterable(cls=siteshydro)  # TODO descriptor
    sitesmeteo = sitesmeteo  # TODO
    seuilshydro = seuilshydro  # TODO
    evenements = evenements  # TODO
    serieshydro = serieshydro  # TODO
    seriesmeteo = seriesmeteo  # TODO
    simulations = simulations  # TODO

    def __init__(
        self, scenario, siteshydro=None, sitesmeteo=None, seuilshydro=None,
        evenements=None, serieshydro=None, seriesmeteo=None, simulations=None,
        ordered=False, strict=True
    ):
        """Initialisation.

        Arguments:
            scenario (xml.Scenario) = un objet Scenario obligatoire
            siteshydro (sitehydro.Sitehydro collection) = iterable ou None
            sitesmeteo (sitemeteo.Sitemeteo collection) = iterable ou None
            seuilshydro (seuil.Seuilhydro collection) = iterable ou None
            evenements (evenement.Evenement collection) = iterable ou None
            serieshydro (obshydro.Serie collection) = iterable ou None
            seriesmeteo (obsmeteo.Serie collection) = iterable ou None'
            simulations (simulation.Simulation collection) = iterable ou None
            ordered (bool, default False) = if True tries to keep things in
                order when serialising (slower)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite des elements

        """

        # -- simple properties --
        self._ordered = bool(ordered)
        self._strict = bool(strict)

        # -- descriptors --
        self.siteshydro = siteshydro
        self.sitesmeteo = sitesmeteo
        self.seuilshydro = seuilshydro
        self.evenements = evenements
        self.serieshydro = serieshydro
        self.seriesmeteo = seriesmeteo
        self.simulations = simulations

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

        Arguments:
            src (nom de fichier, url, objet fichier...) = source de donnee. Les
                type de src acceptes sont ceux de lxml.etree.parse
            ordered (bool, default False) = if True tries to keep things in
                order

        """
        # read the file
        parser = _etree.XMLParser(
            remove_blank_text=True, remove_comments=True, ns_clean=True
        )
        tree = _etree.parse(src, parser=parser)

        # deal with namespaces
        # TODO - we could certainly do better with namespaces
        if tree.getroot().nsmap != {}:
            raise ValueError("can't parse xml file with namespaces")

        return Message(
            scenario=_from_xml._scenario_from_element(
                tree.find('Scenario')
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

            # 'intervenants':
            # 'modelesprevision': 'TODOS',
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
            CLE PARMI   /      VALEUR
            siteshydro  = iterable de sitehydro.Sitehydro
            sitesmeteo  = iterable de sitemeteo.Sitemeteo
            seuilshydro = iterable de seuil.Seuilhydro
            evenements  = iterable d'evenement.Evenement
            serieshydro = iterable de obshydro.Serie
            seriesmeteo = iterable de obsmeteo.Serie
            simulations = iterable de simulation.Simulation

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

    def write(self, file, encoding='utf-8', compression=0, force=False):
        """Ecrit le Message dans le fichier dst.

        Cette methode est un wrapper autour de lxml.etree.ElementTree.write.
        Se referer a la documentation de lxml pour le detail des options.

        Arguments:
            dst (fichier)
            encoding (string)
            compression (int de 0 a 9) = niveau de compression gzip
            force (bool)

        """
        # check file
        if (not force) and (_os.path.isfile(file)):
            raise IOError('file already exists')
        # procede !
        tree = _etree.ElementTree(
            _to_xml._to_xml(
                scenario=self.scenario,
                siteshydro=self.siteshydro,
                sitesmeteo=self.sitesmeteo,
                seuilshydro=self.seuilshydro,
                evenements=self.evenements,
                serieshydro=self.serieshydro,
                seriesmeteo=self.seriesmeteo,
                simulations=self.simulations,
                ordered=self._ordered
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

    def show(self):
        """Return pretty print XML."""
        return _etree.tostring(
            _to_xml._to_xml(
                scenario=self.scenario,
                siteshydro=self.siteshydro,
                sitesmeteo=self.sitesmeteo,
                seuilshydro=self.seuilshydro,
                evenements=self.evenements,
                serieshydro=self.serieshydro,
                seriesmeteo=self.seriesmeteo,
                simulations=self.simulations
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
        return '{}\nContenu: {} siteshydro - {} seuilshydro - ' \
               '{} evenements - ' \
               '{} series - {} simulations'.format(
                   scenario,
                   len(self.siteshydro),
                   len(self.sitesmeteo),
                   len(self.seuilshydro),
                   len(self.evenements),
                   len(self.serieshydro),
                   len(self.seriesmeteo),
                   len(self.simulations)
               )

    __str__ = _composant.__str__


#-- class MessageNomenclatureitem ----------------------------------------------------
# TODO descriptor

descriptor model:

class Nomenclatureitem(object):

    """Class Nomenclatureitem.

    A descriptor to deal with 'in nomenclature.NOMENCLATURES' properties.

    Should raise only a ValueError when value is not allowed (even with
    the None case).

    Properties:
        nomenclature (int) = the nomenclature ref
        valuetype (type) = a function to cast values to the nomenclature's
            items type
        strict (bool, default True) = wether or not the instance value has
            to be in the nomenclature items
        required (bool, defaut True) = wether or not instance's value can
            be None
        default =  a defautl value returned if the instance's value is not
            in the dictionnary. Should be unused if the property has been
            initialized.
        data (weakref.WeakKeyDictionary)

    """

    def __init__(self, nomenclature, strict=True, required=True, default=None):
        """Initialization.

        Args:
            nomenclature (int) = the nomenclature ref
            strict (bool, default True) = wether or not the instance value has
                to be in the nomenclature items
            required (bool, defaut True) = wether or not instance's value can
                be None
            default =  a defautl value returned if the instance's value is not
                in the dictionnary. Should be unused if the property has been
                initialized.

        """
        self.nomenclature = int(nomenclature)
        if self.nomenclature not in _NOMENCLATURE:
            raise ValueError('unknown nomenclature')
        self.valuetype = type(_NOMENCLATURE[self.nomenclature].keys()[0])
        self.strict = bool(strict)
        self.required = bool(required)
        self.default = default
        self.data = _weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        """Return instance value."""
        return self.data.get(instance, default=self.default)

    def __set__(self, instance, value):
        """Set the 'in nomenclature' property."""
        # None case
        if (value is None):
            if self.required:
                raise ValueError('a value other than None is required')

        # other cases
        else:
            value = self.valuetype(value)
            if (
                (self.strict) and
                (value not in _NOMENCLATURE[self.nomenclature])
            ):
                raise ValueError(
                    'value should be in nomenclature %i' % self.nomenclature
                )

        # all is well
        self.data[instance] = value


property model:

    @property
    def siteshydro(self):
        """Return siteshydro."""
        return self._siteshydro

    @siteshydro.setter
    def siteshydro(self, siteshydro):
        """Set siteshydro."""
        try:

            # None case
            if (siteshydro is None):
                siteshydro = []

            # other cases
            if isinstance(siteshydro, _sitehydro.Sitehydro):
                siteshydro = [siteshydro]
            elif self._strict:
                for sitehydro in siteshydro:
                    if not isinstance(sitehydro, _sitehydro.Sitehydro):
                        raise TypeError(
                            'sitehydro {} incorrect'.format(sitehydro)
                        )

            # all is well
            self._siteshydro = siteshydro

        except:
            raise

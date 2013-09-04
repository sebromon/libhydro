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
    # intervenant as _intervenant,  # FIXME
    sitehydro as _sitehydro,
    obshydro as _obshydro,
    simulation as _simulation
)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1e"""
__date__ = """2013-09-04"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


# -- class Message ------------------------------------------------------------
class Message(object):
    """ClasseMessage.

    Classe pour manipuler les messages Xml hydrometrie.

    Proprietes:
        scenario (xml.Scenario) = un objet Scenario obligatoire
        sitesydro (sitehydro.Sitehydro collection) = iterable ou None
        series (obshydro.Serie collection) = iterable ou None
        simulations (simulation.Simulation collection) = iterable ou None

    """

        # 'intervenants':
        # 'sitesmeteo'
        # 'modelesprevision': 'TODOS',
        # 'evenements'
        # 'courbestarage'
        # 'jaugeages'
        # 'courbescorrection'
        # 'obssmeteo'
        # 'obsselab'
        # 'gradshydro'
        # 'qualifsannee'
        # 'alarmes'

    def __init__(
        self, scenario, siteshydro=None, series=None, simulations=None, strict=True
    ):
        """Initialisation.

        Arguments:
            scenario (xml.Scenario) = un objet Scenario obligatoire
            sitesydro (sitehydro.Sitehydro collection) = iterable ou None
            series (obshydro.Serie collection) = iterable ou None
            simulations (simulation.Simulation collection) = iterable ou None
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite des elements

        """

        # -- super --

        # -- simple properties --
        self._strict = strict

        # -- full properties --
        self.scenario = scenario
        self.siteshydro = siteshydro
        self.series = series
        self.simulations = simulations

    # -- property scenario --
    @property
    def scenario(self):
        """Scenario."""
        return self._scenario

    @scenario.setter
    def scenario(self, scenario):
        try:

            # None case
            if scenario is None:
                raise TypeError('scenario is required')

            # other cases
            if (self._strict) and (not isinstance(scenario, _from_xml.Scenario)):
                raise TypeError('scenario incorrect')

            # all is well
            self._scenario = scenario

        except:
            raise

    # -- property siteshydro --
    @property
    def siteshydro(self):
        """Siteshydro."""
        return self._siteshydro

    @siteshydro.setter
    def siteshydro(self, siteshydro):
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

    # -- property series --
    @property
    def series(self):
        """Series."""
        return self._series

    @series.setter
    def series(self, series):
        try:

            # None case
            if (series is None):
                series = []

            # other cases
            if isinstance(series, _obshydro.Serie):
                series = [series]
            elif self._strict:
                for serie in series:
                    if not isinstance(serie, _obshydro.Serie):
                        raise TypeError(
                            'serie {} incorrecte'.format(serie)
                        )

            # all is well
            self._series = series

        except:
            raise

    # -- property simulations --
    @property
    def simulations(self):
        """Simulations."""
        return self._simulations

    @simulations.setter
    def simulations(self, simulations):
        try:

            # None case
            if (simulations is None):
                simulations = []

            # other cases
            if isinstance(simulations, _simulation.Simulation):
                simulations = [simulations]
            elif self._strict:
                for simulation in simulations:
                    if not isinstance(simulation, _simulation.Simulation):
                        raise TypeError(
                            'simulation {} incorrecte'.format(simulation)
                        )

            # all is well
            self._simulations = simulations

        except:
            raise

    # -- class methods --
    @classmethod
    def from_file(cls, src):
        """Parse le fichier src et retourne un xml.Message.

        Arguments:
            src (nom de fichier, url, objet fichier...) = source de donnee. Les
                type de src acceptes sont ceux de lxml.etree.parse

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
            scenario=_from_xml._scenario_from_element(tree.find('Scenario')),
            siteshydro=_from_xml._siteshydro_from_element(tree.find('RefHyd/SitesHydro')),
            series=_from_xml._series_from_element(tree.find('Donnees/Series')),
            simulations=_from_xml._simulations_from_element(tree.find('Donnees/Simuls'))
        )

            # 'intervenants':
            # 'sitesmeteo'
            # 'modelesprevision': 'TODOS',
            # 'evenements'
            # 'courbestarage'
            # 'jaugeages'
            # 'courbescorrection'
            # 'obssmeteo'
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
            series      = iterable de obshydro.Serie
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

    def write(self, file, force=False, encoding='utf-8', compression=0):
        """Ecrit le Message dans le fichier dst.

        Cette methode est un wrapper autour de lxml.etree.ElementTree.write.
        Se referer a la documentation de lxml pour le detail des options.

        Arguments:
            dst (fichier)
            force (bool)
            encoding (string)
            compression (int de 0 a 9) = niveau de compression gzip

        """
        # check file
        if (not force) and (_os.path.isfile(file)):
            raise IOError('file already exists')
        # procede !
        tree = _etree.ElementTree(
            _to_xml._to_xml(
                scenario=self.scenario,
                siteshydro=self.siteshydro,
                series=self.series,
                simulations=self.simulations
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
        """Screen print XML."""
        return _etree.tostring(
            _to_xml._to_xml(
                scenario=self.scenario,
                siteshydro=self.siteshydro,
                series=self.series,
                simulations=self.simulations
            ),
            encoding=_sys.stdout.encoding,
            xml_declaration=1,
            pretty_print=1
        )

    def __unicode__(self):
        """Unicode representation."""
        try:
            scenario = self.scenario.__unicode__()
        except Exception:
            scenario = '<sans scenario>'
        return '{}\nContenu: {} siteshydro - {} series - {} simulations'.format(
            scenario,
            len(self.siteshydro),
            len(self.series),
            len(self.simulations)
        )

    def __str__(self):
        """String representation."""
        if _sys.version_info[0] >= 3:  # Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)

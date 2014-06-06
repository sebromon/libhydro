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
    seuil as _seuil,
    evenement as _evenement,
    obshydro as _obshydro,
    simulation as _simulation
)


#-- strings -------------------------------------------------------------------
__author__ = """Philippe Gouin """ \
             """<philippe.gouin@developpement-durable.gouv.fr>"""
__version__ = """0.1j"""
__date__ = """2014-03-23"""

#HISTORY
#V0.1 - 2013-08-20
#    first shot


#-- todos ---------------------------------------------------------------------
# TODO - factorize 5 Message properties in a descriptor (except scenario)
# TODO - implement intervenants and modelesprevision


# -- class Message ------------------------------------------------------------
class Message(object):

    """ClasseMessage.

    Classe pour manipuler les messages Xml hydrometrie.

    Proprietes:
        scenario (xml.Scenario) = un objet Scenario obligatoire
        siteshydro (sitehydro.Sitehydro collection) = iterable ou None
        seuilshydro (seuil.Seuilhydro collection) = iterable ou None
        evenements (evenement.Evenement collection) = iterable ou None
        series (obshydro.Serie collection) = iterable ou None
        simulations (simulation.Simulation collection) = iterable ou None

    """

        # 'intervenants': 'TODO',
        # 'modelesprevision': 'TODO'

        # 'sitesmeteo'
        # 'courbestarage'
        # 'jaugeages'
        # 'courbescorrection'
        # 'obssmeteo'
        # 'obsselab'
        # 'gradshydro'
        # 'qualifsannee'
        # 'alarmes'

    def __init__(
        self, scenario, siteshydro=None, seuilshydro=None, evenements=None,
        series=None, simulations=None, ordered=False, strict=True
    ):
        """Initialisation.

        Arguments:
            scenario (xml.Scenario) = un objet Scenario obligatoire
            siteshydro (sitehydro.Sitehydro collection) = iterable ou None
            seuilshydro (seuil.Seuilhydro collection) = iterable ou None
            evenements (evenement.Evenement collection) = iterable ou None
            series (obshydro.Serie collection) = iterable ou None
            simulations (simulation.Simulation collection) = iterable ou None
            ordered (bool, default False) = if True tries to keep things in
                order when serialising (slower)
            strict (bool, defaut True) = le mode permissif permet de lever les
                controles de validite des elements

        """

        # -- super --

        # -- simple properties --
        self._ordered = bool(ordered)
        self._strict = bool(strict)

        # -- full properties --
        self._scenario = self._siteshydro = self._seuilshydro = None
        self._evenements = self._series = self._simulations = None
        self.scenario = scenario
        self.siteshydro = siteshydro
        self.seuilshydro = seuilshydro
        self.evenements = evenements
        self.series = series
        self.simulations = simulations

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

    # -- property siteshydro --
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

    # -- property seuilshydro --
    @property
    def seuilshydro(self):
        """Return seuilshydro."""
        return self._seuilshydro

    @seuilshydro.setter
    def seuilshydro(self, seuilshydro):
        """Set seuilshydro."""
        try:

            # None case
            if (seuilshydro is None):
                seuilshydro = []

            # other cases
            if isinstance(seuilshydro, _seuil.Seuilhydro):
                seuilshydro = [seuilshydro]
            elif self._strict:
                for seuilhydro in seuilshydro:
                    if not isinstance(seuilhydro, _seuil.Seuilhydro):
                        raise TypeError(
                            'seuilhydro {} incorrect'.format(seuilhydro)
                        )

            # all is well
            self._seuilshydro = seuilshydro

        except:
            raise

    # -- property evenements --
    @property
    def evenements(self):
        """Return evenements."""
        return self._evenements

    @evenements.setter
    def evenements(self, evenements):
        """Set evenements."""
        # None case
        if (evenements is None):
            evenements = []

        # other cases
        if isinstance(evenements, _evenement.Evenement):
            evenements = [evenements]
        elif self._strict:
            for evenement in evenements:
                if not isinstance(evenement, _evenement.Evenement):
                    raise TypeError(
                        'evenement {} incorrect'.format(evenement)
                    )

        # all is well
        self._evenements = evenements

    # -- property series --
    @property
    def series(self):
        """Return series."""
        return self._series

    @series.setter
    def series(self, series):
        """Set series."""
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
        """Return simulations."""
        return self._simulations

    @simulations.setter
    def simulations(self, simulations):
        """Setsimulations."""
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
            seuilshydro=_from_xml._seuilshydro_from_element(
                element=tree.find('RefHyd/SitesHydro'),
                ordered=ordered
            ),
            evenements=_from_xml._evenements_from_element(
                tree.find('Donnees/Evenements')
            ),
            series=_from_xml._series_from_element(
                tree.find('Donnees/Series')
            ),
            simulations=_from_xml._simulations_from_element(
                tree.find('Donnees/Simuls')
            )
        )

            # 'intervenants':
            # 'sitesmeteo'
            # 'modelesprevision': 'TODOS',
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
            seuilshydro = iterable de seuil.Seuilhydro
            evenements  = iterable d'evenement.Evenement
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
                seuilshydro=self.seuilshydro,
                evenements=self.evenements,
                series=self.series,
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
                seuilshydro=self.seuilshydro,
                evenements=self.evenements,
                series=self.series,
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
                   len(self.seuilshydro),
                   len(self.evenements),
                   len(self.series),
                   len(self.simulations)
               )

    def __str__(self):
        """Return string representation."""
        if _sys.version_info[0] >= 3:  # pragma: no cover - Python 3
            return self.__unicode__()
        else:  # Python 2
            return self.__unicode__().encode(_sys.stdout.encoding)

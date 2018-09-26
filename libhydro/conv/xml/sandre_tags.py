# -*- coding: utf-8 -*-
"""
Module sandre_tags_v1

Ce module contient les balises sandre V1.1
"""

# imports recommandés
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)


class SandreTagsV1(object):
    """ Balises Sandre V1.1"""
    serieshydro = 'Series'
    seriehydro = 'Serie'
    grdseriehydro = 'GrdSerie'
    dtdebseriehydro = 'DtDebSerie'
    dtfinseriehydro = 'DtFinSerie'

    dtprodseriehydro = 'DtProdSerie'
    sysaltiseriehydro = 'SysAltiSerie'
    serieperimhydro = 'SeriePerim'

    # tags only Sandre V1.1
    statutseriehydro = 'StatutSerie'

    # séries obs élaborées hydro
    seriesobselabhydro = 'ObssElabHydro'
    serieobselabhydro = 'ObsElabHydro'

    # Courbes de tarage
    dtdebperiodeutilct = 'DtDebutPeriodeUtilisationCourbeTarage'
    histosactivationperiode = 'HistosActivPeriod'
    histoactivationperiode = 'HistoActivPeriod'
    dtactivationhistoperiode = 'DtActivHistoActivPeriod'
    dtdesactivationhistoperiode = 'DtDesactivHistoActivPeriod'

    # Courbes de correction
    dtdesactivationpointpivot = 'DtDesactivPointPivot'

    # Jaugeage
    vitessemaxsurface = 'VitesseMoySurfaceJaugeage'

    # Evenements
    publicationevenement = 'TypPublicationEvenement'

    # SiteHydro
    stsitehydro = 'StatutSiteHydro'
    comtlbsitehydro = 'ComtLbSiteHydro'
    dtmajsitehydro = 'DtMAJSiteHydro'

    # entites vigicrues / tronconvigilance
    entsvigicru = 'TronconsVigilanceSiteHydro'
    entvigicru = 'TronconVigilanceSiteHydro'
    cdentvigicru = 'CdTronconVigilance'
    nomentvigicru = 'NomCTronconVigilance'

    # Roles Site hydro
    rolscontactsitehydro = 'RolesContactSiteHydro'
    rolcontactsitehydro = 'RoleContactSiteHydro'  # à supprimer
    rolcontact = 'RoleContact'
    dtmajrolecontactsitehydro = 'DtMAJRoleContactSiteHydro'  # à supprimer
    dtmajrolecontact = 'DtMAJRoleContact'  # station or site

    # stations hydro
    complementlibellestationhydro = 'ComplementLibelleStationHydro'
    comprivestationhydro = 'DescriptifStationHydro'
    dtmajstationhydro = 'DtMAJStationHydro'
    rolscontactstationhydro = 'RolesContactStationHydro'
    rolcontactstationhydro = 'RoleContactStationHydro'


class SandreTagsV2(object):
    """Balises Sandre V2"""
    serieshydro = 'SeriesObsHydro'
    seriehydro = 'SerieObsHydro'
    grdseriehydro = 'GrdSerieObsHydro'
    dtdebseriehydro = 'DtDebSerieObsHydro'
    dtfinseriehydro = 'DtFinSerieObsHydro'
    dtprodseriehydro = 'DtProdSerieObsHydro'
    sysaltiseriehydro = 'SysAltiSerieObsHydro'
    serieperimhydro = 'SeriePerimSerieObsHydro'
    pdtseriehydro = 'PDTSerieObsHydro'

    # Onlys Sandre V2
    statutobshydro = 'StObsHydro'

    seriesobselabhydro = 'SeriesObsElaborHydro'
    serieobselabhydro = 'SerieObsElaborHydro'

    # Courbes de tarage
    dtdebperiodeutilct = 'DtDebPeriodeUtilisationCourbeTarage'
    histosactivationperiode = 'HistosActivationPeriode'
    histoactivationperiode = 'HistoActivationPeriode'
    dtactivationhistoperiode = 'DtActivationHistoActivationPeriode'
    dtdesactivationhistoperiode = 'DtDesactivationHistoActivationPeriode'

    # Courbes de correction
    dtdesactivationpointpivot = 'DtDesactivationPointPivot'

    # Jaugeage
    vitessemaxsurface = 'VitesseMaxSurfaceJaugeage'

    # Evenements
    publicationevenement = 'TypPubliEvenement'

    # SiteHydro
    stsitehydro = 'StSiteHydro'
    comtlbsitehydro = 'ComplementLbSiteHydro'
    dtmajsitehydro = 'DtMajSiteHydro'
    
    # entites vigicrues / tronconvigilance
    entsvigicru = 'EntsVigiCru'
    entvigicru = 'EntVigiCru'
    cdentvigicru = 'CdEntVigiCru'
    nomentvigicru = 'NomEntVigiCru'

    # Roles Site hydro
    rolscontactsitehydro = 'RolsContactSiteHydro'
    rolcontactsitehydro = 'RolContactSiteHydro' # à supprimer
    rolcontact = 'RolContact'
    dtmajrolecontactsitehydro = 'DtMajRoleContactSiteHydro'  # à supprimer
    dtmajrolecontact = 'DtMajRoleContact'  # station or site

    # stations hydro
    complementlibellestationhydro = 'ComplementLbStationHydro'
    comprivestationhydro = 'ComPrivStationHydro'
    dtmajstationhydro = 'DtMajStationHydro'
    rolscontactstationhydro = 'RolsContactStationHydro'
    rolcontactstationhydro = 'RolContactStationHydro'

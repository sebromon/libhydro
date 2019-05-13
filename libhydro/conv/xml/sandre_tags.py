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
    
    # Capteurs
    dtmajcapteur = 'DtMAJCapteur'
    pdtcapteur = 'PasDeTempsCapteur'

    # sites météo
    dtmajsitemeteo = 'DtMAJSiteMeteo'
    rolscontactsitemeteo = 'RolesContactSiteMeteo'
    rolcontactsitemeteo = 'RoleContactSiteMeteo'  # à supprimer
    dtmajrolecontactcitemeteo = 'DtMAJRoleContactSiteMeteo'

    # grandeur météo
    pdtgrdmeteo = 'PasDeTempsNominalGrdMeteo'

    # Seuils hydro
    seuilhydro = 'ValeursSeuilSiteHydro'
    cdseuilhydro = 'CdSeuilSiteHydro'
    typseuilhydro = 'TypSeuilSiteHydro'
    natureseuilhydro = 'NatureSeuilSiteHydro'
    dureeseuilhydro = 'DureeSeuilSiteHydro'
    lbusuelseuilhydro = 'LbUsuelSeuilSiteHydro'
    mnseuilhydro = 'MnemoSeuilSiteHydro'
    typpubliseuilhydro = 'DroitPublicationSeuilSiteHydro'
    indicegraviteseuilhydro = 'IndiceGraviteSeuilSiteHydro'
    valforceeseuilhydro = 'ValForceeSeuilSiteHydro'
    dtmajseuilhydro = 'DtMajSeuilSiteHydro'
    comseuilhydro = 'ComSeuilSiteHydro'
    valsseuilhydro = 'ValeursSeuilsStationHydro'
    valseuilhydro = 'ValeursSeuilStationHydro'

    # Seuils météo
    seuilmeteo = 'ValeurSeuilGrdMeteo'
    cdseuilmeteo = 'CdSeuilGrdMeteo'
    typseuilmeteo = 'TypSeuilGrdMeteo'
    natureseuilmeteo = 'NatureSeuilGrdMeteo'
    dureeseuilmeteo = 'DureeSeuilGrdMeteo'
    lbusuelseuilmeteo = 'LbUsuelSeuilGrdMeteo'
    mnseuilmeteo = 'MnSeuilGrdMeteo'
    indicegraviteseuilmeteo = 'IndGraviteSeuilGrdMeteo'
    dtmajseuilmeteo = 'DtMajSeuilGrdMeteo'
    comseuilmeteo = 'ComSeuilGrdMeteo'
    valvalseuilmeteo = 'ValSeuilGrdMeteo'
    tolerancevalseuilmeteo = 'ToleranceSeuilGrdMeteo'
    dtactivationvalseuilmeteo = 'DtActivationSeuilGrdMeteo'
    dtdesactivationvalseuilmeteo = 'DtDesactivationSeuilGrdMeteo'

    # Gradients hydro
    stgradhydro = 'StatutGradHydro'

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

    # Capteurs
    dtmajcapteur = 'DtMajCapteur'
    pdtcapteur = 'PDTCapteur'

    # sites météo
    dtmajsitemeteo = 'DtMajSiteMeteo'
    rolscontactsitemeteo = 'RolsContactSiteMeteo'
    rolcontactsitemeteo = 'RolContactSiteMeteo'
    dtmajrolecontactcitemeteo = 'DtMajRoleContactSiteMeteo'

    # grandeur météo
    pdtgrdmeteo = 'PDTGrdMeteo'

    # Seuils hydro
    seuilhydro = 'SeuilHydro'
    cdseuilhydro = 'CdSeuilHydro'
    typseuilhydro = 'TypSeuilHydro'
    natureseuilhydro = 'NatureSeuilHydro'
    dureeseuilhydro = 'DureeSeuilHydro'
    lbusuelseuilhydro = 'LbUsuelSeuilHydro'
    mnseuilhydro = 'MnSeuilHydro'
    typpubliseuilhydro = 'TypPubliSeuilHydro'
    indicegraviteseuilhydro = 'IndiceGraviteSeuilHydro'
    valforceeseuilhydro = 'ValForceeSeuilHydro'
    dtmajseuilhydro = 'DtMajSeuilHydro'
    comseuilhydro = 'ComSeuilHydro'
    valsseuilhydro = 'ValsSeuilHydro'
    valseuilhydro = 'ValSeuilHydro'

    # Seuils météo
    seuilmeteo = 'SeuilMeteo'
    cdseuilmeteo = 'CdSeuilMeteo'
    typseuilmeteo = 'TypSeuilMeteo'
    natureseuilmeteo = 'NatureSeuilMeteo'
    dureeseuilmeteo = 'DureeSeuilMeteo'
    lbusuelseuilmeteo = 'LbUsuelSeuilMeteo'
    mnseuilmeteo = 'MnSeuilMeteo'
    indicegraviteseuilmeteo = 'IndiceGraviteSeuilMeteo'
    dtmajseuilmeteo = 'DtMajSeuilMeteo'
    comseuilmeteo = 'ComSeuilMeteo'
    valvalseuilmeteo = 'ValValSeuilMeteo'
    tolerancevalseuilmeteo = 'ToleranceValSeuilMeteo'
    dtactivationvalseuilmeteo = 'DtActivationValSeuilMeteo'
    dtdesactivationvalseuilmeteo = 'DtDesactivationValSeuilMeteo'

    # Gradients hydro
    stgradhydro = 'StGradHydro'

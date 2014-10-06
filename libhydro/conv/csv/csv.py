

FIELDS = {
    sitehydro: {
        'CdSiteHydro': code,  # mandatory
        'LbSiteHydro': ''
        # <TypSiteHydro>
        # <CoordXSiteHydro>
        # <CoordYSiteHydro>
        # <ProjCoordSiteHydro>
        # <AltitudeSiteHydro>
        # <SysAltimetriqueSiteHydro>
        # <BassinVersantSiteHydro>
        # <FuseauHoraireSiteHydro>
        # <CdEuMasseDEau>
        # <cdZoneHydro>
        # <CdEntiteHydrographique>
        # <CdStationHydro>
        # <LbStationHydro>
        # <TypStationHydro>
        # <CoordXStationHydro>
        # <CoordYStationHydro>
        # <ProjCoordStationHydro>
        # <DtMiseServiceStationHydro>
        # <DtFermetureStationHydro>
        # <CdCommune>
    },
    sitemeteo: {},
    seriehydro: {},
    seriemeteo: {},

}


# for python 2.7+ / 3+:
#     inv_map = {v: k for k, v in map.items()}
#     in python2.7+, using map.iteritems() would be more efficient

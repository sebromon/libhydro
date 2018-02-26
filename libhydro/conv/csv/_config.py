# coding: utf-8
"""Module libhydro.conv.csv._config.

Configuration par defaut du codec CSV:
    # csv.Dialect('hydrometrie')
    # FLAG
    # SECOND_LINE
    # DECIMAL_POINT
    # MAPPER

Cette configuration est basee sur les regles des documents:
    # Presentation du format d'echange simplifie
    # Echange de donnees d'hydrometrie au format simplifie
disponibles sur le site du SANDRE <http://www.sandre.eaufrance.fr/>.

"""
# -- imports ------------------------------------------------------------------

import csv

# -----------------------------------------------------------------------------
#
# Configuration du Dialect CSV 'hydrometrie'
#
# -----------------------------------------------------------------------------
# Les valeurs du dialect 'hydrometrie' peuvent etre surchargees a la volee en
# passant 'cle=valeur' aux differents readers
#
# WARNING: le csv.register_dialect ne tolere pas les valeurs en unicode en
#          Python 2 :-(
#
# Python 3 supression bytes b
csv.register_dialect(
    'hydrometrie',
    **{
        #'delimiter': b';',
        'delimiter': ';',
        'doublequote': False,
        'escapechar': None,  # b'\\',
        #'lineterminator': b'\r\n',
        'lineterminator': '\r\n',
        'quoting': csv.QUOTE_NONE,
        # 'quotechar': '"',
        'skipinitialspace': True,
        'strict': False
    }
)

# -----------------------------------------------------------------------------
#
# FLAG de fin de ligne
#
# -----------------------------------------------------------------------------
# Par defaut chaque ligne doit se terminer par un flag
FLAG = {'header': '<FLG>', 'row': 'FLG'}
# Pour ne pas utiliser les flags, utiliser FLAG = None
# FLAG = None

# -----------------------------------------------------------------------------
#
# SECOND LINE
#
# -----------------------------------------------------------------------------
# Par defaut une seconde ligne d'en en-tete est utilisee
SECOND_LINE = True

# -----------------------------------------------------------------------------
#
# DECIMAL
#
# -----------------------------------------------------------------------------
# Separateur decimal. Utiliser None pour un separateur '.' (plus rapide).
DECIMAL_POINT = ','
# DECIMAL_POINT = None

# -----------------------------------------------------------------------------
#
# MAPPER
#
# -----------------------------------------------------------------------------
# Le mapper 'csv header' vers 'object attribute' pour chaque classe
MAPPER = {
    'libhydro.core.sitehydro.Sitehydro': {
        '<CdSiteHydro>': 'code',  # mandatory
        '<LbSiteHydro>': 'libelle',
        '<TypSiteHydro>': 'typesite',
        '<AltitudeSiteHydro>': None,  # NotImplemented yet
        '<SysAltimetriqueSiteHydro>': None,  # NotImplemented yet
        '<BassinVersantSiteHydro>': None,  # NotImplemented yet
        '<FuseauHoraireSiteHydro>': None,  # NotImplemented yet
        '<CdEuMasseDEau>': None,  # NotImplemented yet
        '<cdZoneHydro>': None,  # NotImplemented yet
        '<CdEntiteHydrographique>': None,  # NotImplemented yet
    },
    'libhydro.core.sitehydro.Sitehydro.coord': {
        '<CoordXSiteHydro>': 'x',
        '<CoordYSiteHydro>': 'y',
        '<ProjCoordSiteHydro>': 'proj'
    },
    'libhydro.core.sitehydro.Station': {
        '<CdStationHydro>': 'code',  # mandatory
        '<LbStationHydro>': 'libelle',
        '<TypStationHydro>': 'typestation',
        '<DtMiseServiceStationHydro>': None,  # NotImplemented yet
        '<DtFermetureStationHydro>': None,  # NotImplemented yetv
        '<CdCommune>': 'commune',
    },
    'libhydro.core.sitehydro.Station.coord': {
        '<CoordXStationHydro>': 'x',
        '<CoordYStationHydro>': 'y',
        '<ProjCoordStationHydro>': 'proj',
    },
    'libhydro.core.sitemeteo.Sitemeteo': {
        '<CdSiteMeteo>': 'code',  # mandatory
        '<LbSiteMeteo>': 'libelle',
        '<AltitudeSiteMeteo>': None,  # NotImplemented yetv
        '<SysAltimetriqueSiteMeteo>': None,  # NotImplemented yetv
        '<FuseauHoraireSiteMeteo>': None,  # NotImplemented yetv
        '<DtOuvertureSiteMeteo>': None,  # NotImplemented yetv
        '<DtFermSiteMeteo>': None,  # NotImplemented yetv
        '<CdSousSecteurHydro>': None,  # NotImplemented yetv
        '<CdCommune>': 'commune',
    },
    'libhydro.core.sitemeteo.Sitemeteo.coord': {
        '<CoordXSiteMeteo>': 'x',
        '<CoordYSiteMeteo>': 'y',
        '<ProjCoordSiteMeteo>': 'proj',
    },
    'libhydro.core.sitemeteo.Sitemeteo.grandeur': {
        '<CdGrdMeteo>': 'typemesure',  # mandatory
        '<DtMiseServiceGrdMeteo>': None,  # NotImplemented yet
        '<DtFermetureServiceGrdMeteo>': None,  # NotImplemented yet
    },
    'libhydro.core.obshydro.Serie': {
        '<GrdSerie>': 'grandeur'  # mandatory
    },
    'libhydro.core.obshydro.Serie.entite_sitehydro': {
        '<CdSiteHydro>': 'code',  # mandatory
    },
    'libhydro.core.obshydro.Serie.entite_station': {
        '<CdStationHydro>': 'code',
    },
    'libhydro.core.obshydro.Observation': {
        '<DtObsHydro>': 'dte',  # mandatory
        '<ResObsHydro>': 'res',  # mandatory
        '<MethObsHydro>': 'mth',
        '<StatutSerie>': 'statut'  # mandatory
    },
    'libhydro.core.obsmeteo.Serie': {
        '<DureeObsMeteo>': 'duree',
    },
    'libhydro.core.obsmeteo.Serie.grandeur.sitemeteo': {
        '<CdSiteMeteo>': 'code',  # mandatory
    },
    'libhydro.core.obsmeteo.Serie.grandeur': {
        '<CdGrdMeteo>': 'typemesure',  # mandatory
    },
    'libhydro.core.obsmeteo.Observation': {
        '<DtObsMeteo>': 'dte',  # mandatory
        '<ResObsMeteo>': 'res',  # mandatory
        '<MethObsMeteo>': 'mth',
        '<IndiceQualObsMeteo>': 'qua',
        '<StatutObsMeteo>': 'statut',
    }
}

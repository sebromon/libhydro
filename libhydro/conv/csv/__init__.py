# coding: utf-8
"""Package libhydro.conv.csv.

Ce package contient des fonctions pour faciliter la lecture et l'ecriture de
fichiers au format CSV.

Le format par defaut est celui decrit dans le document "Echange de donnees
d'hydrometrie au format simplifie" disponible sur le site du SANDRE
<http://www.sandre.eaufrance.fr/>, mais les fonctions sont configurables pour
lire ou ecrire toute forme de CSV avec en-tête.

L'encodage par defaut des fichiers est 'utf-8'. A defaut l'encodage doit etre
precise via le parametre 'encoding'.

Arguments avances des fonctions:
    # dialect = le format du CSV. Voir la documentation du module Python csv
    # mapping = relation entre les champs du CSV et les objets de la libhydro

Quelques exemples d'utilisation:

    siteshydro = libhydro.conv.csv.from_csv(
        # latin1 = iso-8859-1
        'siteshydro', 'fichier_csv', encoding='latin1'
    )

    siteshydro = libhydro.conv.csv.siteshydro_from_csv(
        'fichier_csv', delimiter=',', mapping={'sitehydro': {'CD': 'code'}}
    )

"""
__all__ = ['from_csv', 'siteshydro_from_csv', 'sitesmeteo_from_csv',
           'serieshydro_from_csv', 'seriesmeteo_from_csv']
# for the user, this package is like a module, sub-modules names are
# underscored to hide them
from ._from_csv import (
    from_csv, siteshydro_from_csv, sitesmeteo_from_csv,
    serieshydro_from_csv, seriesmeteo_from_csv
)
# from ._to_csv import ()

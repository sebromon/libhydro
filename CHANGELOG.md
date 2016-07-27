CHANGE LOG ([Réf 1][1])
===============================================================================

# [unreleased] - yyyy-mm-dd
## Changed
- La classe sitehydro.Stationhydro est renommée Station.
- Refonte ou ajout des méthodes spéciales __eq__ et __ne__ pour toutes les
  classes du package libhydro.core.  Peux entraîner un changement de
  comportement dans la comparaison de certains objets.  Des comparaisons
  avancées (paramétrables) sont disponibles en utilisant self.__eq__(other,
  *args, **kwds).

## Added
- Convertisseur CSV.

# [0.0 => 0.5] - 2013 & 2014
## Added
- Disponibilité du package libhydro.core, puis des codecs SHOM (lecture) et XML.

[1]: https://github.com/olivierlacan/keep-a-changelog "Keep a changelog"

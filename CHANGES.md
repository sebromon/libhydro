CHANGES
===============================================================================

Rubriques
-------------------------------------------------------------------------------

* [!!!] - Breaking change ou autre élément important
* [BUG] - Correctif
* [CFG] - Changement de configuration
* [DEP] - Changement de dépendance
* [IMP] - Amélioration
* [NEW] - Nouveauté
* [PER] - Performances

Liste des versions stables
-------------------------------------------------------------------------------

0.6 (2014/12)
-------------------------------------------------------------------------------
* [!!!] - La classe sitehydro.Stationhydro est renommée Station
* [!!!] - Refonte ou ajout des méthodes spéciales __eq__ et __ne__ pour toutes les classes du package libhydro.core.
Peux entraîner un changement de comportement dans la comparaison de certains objets.
Des comparaisons paramétrables sont disponibles en utilisant self.__eq__(other, ...).
* [NEW] - Convertisseur CSV


0.0 à 0.5 (2013 à 2014)
-------------------------------------------------------------------------------
[NEW] - Disponibilité du package libhydro.core, puis des codecs SHOM (lecture) et XML.

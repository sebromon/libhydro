Libhydro
===============================================================================

Présentation
-------------------------------------------------------------------------------
Libhydro contient un ensemble de modules Python permettant de manipuler
les objets modélisés dans les dictionnaires Hydrométrie publiés par le SANDRE:

  * [Référentiel hydrométrique](http://www.sandre.eaufrance.fr/Referentiel-hydrometrique,90)
  * [Processus d'accquisition des données hydrométriques](http://www.sandre.eaufrance.fr/Processus-d-acquisition-des,91)

La libraire contient aussi plusieurs convertisseurs pour différents formats
de données hydrométriques.

Se reporter à la documentation et au tutoriel pour l'utilisation des différents modules.

Installation
-------------------------------------------------------------------------------
Cette librairie fonctionne avec python 3 uniquement.

Récupérer l'archive et la décompresser puis faire "python setup.py install".

Sont nécessaires et installés automatiquement si besoin:

  * numpy 1.12
  * pandas 0.19.2
  * lxml.etree (>= 3.2.3) pour le convertisseur xml

Contact
-------------------------------------------------------------------------------
Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>

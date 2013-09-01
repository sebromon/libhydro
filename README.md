Libhydro
===============================================================================

[TOC]

Présentation
-------------------------------------------------------------------------------
Libhydro contient un ensemble de modules python permettant de manipuler
les objets modélisés dans les dictionnaires Hydrométrie publiés par le SANDRE:

  * [Référentiel hydrométrique](http://www.sandre.eaufrance.fr/Referentiel-hydrometrique,90)

  * [Processus d'accquisition des données hydrométriques](http://www.sandre.eaufrance.fr/Processus-d-acquisition-des,91)

La libraire contient aussi plusieurs convertisseurs pour différents formats
de données hydrométriques.

Un tutoriel et une documentation au format HTML sont disponibles dans le
répertoire doc du dépot.

Installation
-------------------------------------------------------------------------------
1. Installer les pré-requis
    * python 2.7
    * numpy 1.7.1
    * pandas 0.11.0
    * lxml 3.2.3 pour le convertisseur xml

2. Cloner ce dépot:
    hg clone http://arc.schapi:8001 (répertoire local)

3. Ajouter dans le PYTHONPATH le chemin vers le (répertoire local)

Contacts
-------------------------------------------------------------------------------
Philippe Gouin <philippe.gouin@developpement-durable.gouv.fr>

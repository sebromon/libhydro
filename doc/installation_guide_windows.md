INSTALLATION DE LIBHYDRO SOUS WINDOWS
===============================================================================

* Auteur: philippe.gouin@developpement-durable.gouv.fr
* Version: 0.2e
* Mise à jour: 2014-12-01

Installation packagée de Python (conseillé)
-------------------------------------------------------------------------------
### Télécharger et installer l'installeur miniconda ###
[Réf: http://conda.pydata.org/miniconda.html](http://conda.pydata.org/miniconda.html)

Conda est un gestionnaire de paquets compilés prenant en charge les dépendances.

Conda intègre la librairie 'virtualenv' permettant d'utiliser facilement
sur le même OS plusieurs distributions python isolées les unes des autres:

  * http://sametmax.com/les-environnement-virtuels-python-virtualenv-et-virtualenvwrapper/
  * http://conda.pydata.org/docs/commands/create.html,

### Déclarer le proxy du ministère ####
L'installateur conda doit pouvoir accéder à internet pour télécharger les
paquets à installer.

Si votre réseau local accède à internet via le proxy du MEDDE (à vérifier le
cas échéant avec votre administrateur réseau), les 2 variables à déclarer sont:

    http_proxy=http://(host:port)
    https_proxy=http://(host:port)

On peut le faire au choix:

  * dans les variables d'environnement (clic droit sur le poste de travail,
    propriétés, avancé, variables d'environnement, variables utilisateur)
  * dans un fichier .condarc ([Réf: http://conda.pydata.org/docs/config.html](http://conda.pydata.org/docs/config.htm))

### Installer les pré-requis à libhydro ###
Installer les pré-requis pour libhydro:

    conda install pandas lxml

Dépendances facultatives pour Pandas, permettant d'améliorer les performances
lors de l'utilisation de très grosses séries de données:

    * numexpr uses multiple cores as well as smart chunking and caching to achieve large speedups
    * bottleneck for accelerating certain types of nan evaluations

En profiter pour installer d'autres paquets utiles:

  * _ipython_, un "powerful interactive shell"
  * _spyder_, un éditeur "for the Python language with advanced editing, interactive testing, debugging and introspection features"

Si problème avec pip autour d'une erreur d'encodage ligne 249 du fichier
mimetypes.py, remplacer la ligne 250:

    except UnicodeEncodeError:

par:

    except (UnicodeEncodeError, UnicodeDecodeError):

Installation manuelle de Python (non conseillé)
-------------------------------------------------------------------------------
### Télécharger et installer Python ###
[Réf: https://www.python.org/downloads](https://www.python.org/downloads]())

Utiliser un 'Windows installer' en version 32 ou 64 bits en fonction de votre machine. Pour libhydro choisir la version la plus récente de Python 2.

### Régler les variables d'environnement ###
[Réf: http://docs.python.org/2/using/windows.html](http://docs.python.org/2/using/windows.html)

La variable 'path' permet au système de trouver le bon exécutable Python.
PYTHONPATH permet à Python de trouver ses librairies.
Les deux autres variables permettent à l'installateur PIP de télécharger des
paquets (l'utilisation des proxy du MEDDE pour accéder à internet est à valider
avec votre administrateur réseau).

Exemple:

    path=(chemin à personnaliser);C:\Program Files\Python27;C:\Program Files\Python27\scripts
    PYTHONPATH=(chemin à personnaliser)
    http_proxy=http://(host:port)
    https_proxy=http://(host:port)

### Installer les setup-tools et pip (optionnel) ###
[Réf: http://www.pip-installer.org/en/latest/installing.html](http://www.pip-installer.org/en/latest/installing.html)

PIP est un installeur (et désinstalleur) de paquets sources gérant les dépendances. Sous Windows il permet d'installer
facilement les librairies écrites en Python, mais pas celle qui nécessitent une
compilation et pour lesquelles l'utilisation de paquets déja compilés est préférable.

Dans tous les cas une installation manuelle des libraries via Pypi reste possible.

Récupérer le paquet 'ez_setup.py' et l'installer avec la commande:

    python ez_setup.py

Récupérer le paquet 'get-pip.py' et l'installer avec:

    python get-pip.py  # need the proxy !

Mettre à jour les setuptools:

    pip install --upgrade setuptools

### Installer les pré-requis à libhydro ###
Se reporter à la rubrique équivalent du paragraphe précédent.

Pour les dépendances suivantes qui nécessitent une compilation, il est préférable
d'utiliser des paquets déjà construits, disponibles sur Pypi ou
[ici](http://www.lfd.uci.edu/~gohlke/pythonlibs/):

  * numpy
  * python-dateutil
  * pandas
  * lxml

Installation de libhydro
-------------------------------------------------------------------------------
Télécharger et décompresser l'archive puis dans un terminal faire:

    python setup.py install

INSTALLATION DE LIBHYDRO SOUS WINDOWS
===============================================================================

* Auteur: philippe.gouin@developpement-durable.gouv.fr
* Version: 0.2f
* Mise à jour: 2015-01-22

Installation packagée de Python (CONSEILLE)
-------------------------------------------------------------------------------
### Télécharger et installer l'installeur miniconda ([Réf 1][1]) ###

Conda est un gestionnaire de paquets compilés prenant en charge les dépendances.

Conda intègre la librairie 'virtualenv' permettant d'utiliser facilement
sur le même OS plusieurs distributions python isolées les unes des autres
([Réf 2][2]) ([Réf 3][3]).

### Paramétrer le proxy ####
L'installateur conda doit pouvoir accéder à internet en http pour télécharger
les paquets à installer, ce qui peux nécessiter le paramétrage d'un proxy (à
vérifier le cas échéant avec votre administrateur réseau).

La méthode conseillée est l'utilisation d'un fichier .condarc ([Réf 4][4]).

Exemple:
```
#!bat
# Proxy settings: http://[username]:[password]@[server]:[port]
proxy_servers:
    http: http://user:pass@corp.com:8080
```

A défaut, le proxy internet peut être déclaré dans la console DOS avec la
commande set:
```
#!bat
set http_proxy=http://[username]:[password]@[server]:[port]
```

Il est déconseillé d'utiliser des variables d'environnement globales qui
peuvent impacter d'autres applications.

### Installer les pré-requis à libhydro ###
Installer les pré-requis pour libhydro:
```
#!bat
conda install pandas lxml
```

Dépendances facultatives pour Pandas, permettant d'améliorer les performances
lors de l'utilisation de très grosses séries de données:

  * numexpr uses multiple cores as well as smart chunking and caching to
    achieve large speedups
  * bottleneck for accelerating certain types of nan evaluations

En profiter pour installer d'autres paquets utiles:

  * _ipython-qtconsole_, un "powerful interactive shell"
  * _spyder_, un éditeur "for the Python language with advanced editing,
    interactive testing, debugging and introspection features"

Si problème avec pip autour d'une erreur d'encodage ligne 249 du fichier
mimetypes.py, remplacer ligne 250:
```
#!python
except UnicodeEncodeError:
```

par:
```
#!python
except (UnicodeEncodeError, UnicodeDecodeError):
```

Installation manuelle de Python (NON CONSEILLE)
-------------------------------------------------------------------------------
### Télécharger et installer Python ([Réf 5][5]) ###

Utiliser un 'Windows installer' en version 32 ou 64 bits en fonction de votre
machine. Pour libhydro choisir la version la plus récente de Python 2.

### Régler les variables d'environnement ([Réf 6][6]) ###

La variable 'path' permet au système de trouver le bon exécutable Python et
PYTHONPATH permet à Python de trouver ses librairies.
Les deux autres variables permettent à l'installateur PIP de télécharger des
paquets (l'utilisation d'un proxy pour accéder à internet est à valider
avec votre administrateur réseau).

Exemple:
```
#!bat
path=(chemin à personnaliser);C:\Program Files\Python27;C:\Program Files\Python27\scripts
PYTHONPATH=(chemin à personnaliser)
http_proxy=http://(host:port)
https_proxy=http://(host:port)
```

### Installer les setup-tools et pip (optionnel) ([Réf 7][7]) ###

PIP est un installeur (et désinstalleur) de paquets sources gérant les
dépendances. Sous Windows il permet d'installer facilement les librairies
écrites en Python, mais pas celle qui nécessitent une compilation et pour
lesquelles l'utilisation de paquets déja compilés est préférable.

Dans tous les cas une installation manuelle des libraries via Pypi reste
possible.

Récupérer le paquet 'ez_setup.py' et l'installer avec la commande:
```
#!bat
python ez_setup.py
```

Récupérer le paquet 'get-pip.py' et l'installer avec:
```
#!bat
python get-pip.py  # need the proxy !
```

Puis mettre à jour les setuptools:
```
#!bat
pip install --upgrade setuptools
```

### Installer les pré-requis à libhydro ###
Se reporter à la rubrique équivalent du guide d'installation Linux.

Pour les dépendances suivantes qui nécessitent une compilation, il est
préférable d'utiliser des paquets déjà construits, disponibles sur Pypi ou
[ici (Réf 8)][8]:

  * numpy
  * python-dateutil
  * pandas
  * lxml

Installation de libhydro
-------------------------------------------------------------------------------
Télécharger et décompresser l'archive puis dans un terminal faire:
```
#!bat
python setup.py install
```

[1]: http://conda.pydata.org/miniconda.html "Miniconda"
[2]: http://sametmax.com/les-environnement-virtuels-python-virtualenv-et-virtualenvwrapper/ "Virtualenv"
[3]: http://conda.pydata.org/docs/commands/create.html "Conda create"
[4]: http://conda.pydata.org/docs/config.html "Conda config"
[5]: https://www.python.org/downloads "Python downloads"
[6]: http://docs.python.org/2/using/windows.html "Python config windows"
[7]: http://www.pip-installer.org/en/latest/installing.html "Pip installer"
[8]: http://www.lfd.uci.edu/~gohlke/pythonlibs/ "Paquets python compilés pour Windows"

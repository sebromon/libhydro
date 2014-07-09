INSTALLATION DETAILLEE D'UN ENVIRONNEMENT PYTHON POUR LIBHYDRO
===============================================================================

* Auteur: philippe.gouin@developpement-durable.gouv.fr
* Version: 0.2b
* Mise à jour: 2014-07-08

Installation packagée sous Windows (conseillé)
-------------------------------------------------------------------------------
### Télécharger et installer l'installeur miniconda ###
Conda est un gestionnaire de paquets compilés prenant en charge les dépendances.

[Réf: http://conda.pydata.org/miniconda.html](http://conda.pydata.org/miniconda.html)

### Déclarer le proxy du ministère ####
L'installateur conda doit pouvoir accéder à internet pour télécharger les
paquets à installer.

Les 2 variables à déclarer sont:

    http_proxy=http://direct.proxy.i2:8080
    https_proxy=http://direct.proxy.i2:8080

On peut le faire au choix:

    * dans les variables d'environnement (clic droit sur le poste de travail,
      propriétés, avancé, variables d'environnement, variables utilisateur)
    * dans un fichier .condarc ([Réf: http://conda.pydata.org/docs/config.html)(http://conda.pydata.org/docs/config.htm))

### Installer les pré-requis à libhydro ###
Installer les pré-requis pour libhydro:

    conda install pandas lxml

En profiter pour installer d'autres paquets utiles:

   * _ipython_, un "powerful interactive shell"
   * _spider_, un editeur "for the Python language with advanced editing, interactive testing, debugging and introspection features"

Si problème avec pip autour d'une erreur d'encodage ligne 249 du fichier
mimetypes.py, remplacer la ligne 250:

    except UnicodeEncodeError:

par:

    except (UnicodeEncodeError, UnicodeDecodeError):

### Installer libhydro ###
Dans une console faire:

    python setup.py install

Installation manuelle sous Windows (non conseillé)
-------------------------------------------------------------------------------
### Installer Python ###
Utiliser python2.7.5.msi

### Régler les variables d'environnement ###
[Réf: http://docs.python.org/2/using/windows.html](http://docs.python.org/2/using/windows.html)

    path=... C:\Program Files\Python27;C:\Program Files\Python27\scripts
    PYTHONPATH=...
    http_proxy=http://direct.proxy.i2:8080
    https_proxy=http://direct.proxy.i2:8080

### Dépendances en C ou C++ ###
Pour les dépendances suivantes nécessitant une compilation, il est préférable
d'utiliser des paquets déjà construits, disponibles sur Pypi ou
[ici](http://www.lfd.uci.edu/~gohlke/pythonlibs/):

    * numpy
    * python-dateutil
    * pandas
    * lxml

### Installer les setup-tools et pip (optionnel) ###
[Réf: http://www.pip-installer.org/en/latest/installing.html](http://www.pip-installer.org/en/latest/installing.html)

Récupérer le paquet 'ez_setup.py'.
L'installer avec la commande: python ez_setup.py
Récupérer le paquet 'get-pip.py'.
L'installer avec: python get-pip.py (need the proxy !)
Mettre à jour les setuptools:  pip install --upgrade setuptools

### Installer libhydro ###
    python setup.py install

Installation sous Linux
-------------------------------------------------------------------------------
### Installer Python ###

#### Soit avec un gestionnaire de paquets ####

Installer python et pip (un installateur de librairies).

Si yum ou apt ne proposent pas la bonne version de Python, utiliser un dépot
ou un paquet tiers ou bien passer par une compilation.

Exemple:
    yum install python python-pip.noarch


#### Soit en le compilant (ci-dessous procédure pour CentOS 6.2) ####
[Réf: http://toomuchdata.com/2012/06/25/how-to-install-python-2-7-3-on-centos-6-2/](http://toomuchdata.com/2012/06/25/how-to-install-python-2-7-3-on-centos-6-2/)

La version python 2.4.3 de l'os, nécessaire pour pas mal de programmes, est
/usr/bin/python.

Installer les dépendances:

    yum groupinstall "Development tools"  # big but requested to enable all features in python
    yum install gcc zlib-devel bzip2-devel openssl-devel ncurses-devel readline-devel sqlite sqlite-devel
    yum install readline-devel.x86_64 readline-devel.i386
    yum install zlib-devel.x86_64 zlib-devel.i386
    yum install sqlite.x86_64 sqlite-devel.x86_64  # sqlite is requested by ipython
    yum install openssl-devel.i386 openssl-devel.x86_64  # optional

If failure when building sqlite3 (need a patch):

    wget -O patch_sqlite https://raw.github.com/gist/2727063/
    cat patch_sqlite | patch -p1

Compiler Python:

    wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2
    ./configure
    make
    # use 'make altinstall' if you care overwriting a previous python installation
    su -c 'make install' # installation dans /usr/local/bin/python

Installer pip: _TODO_

### Installer et configurer Virtualenv ###
[Réf: http://sametmax.com/les-environnement-virtuels-python-virtualenv-et-virtualenvwrapper/](http://sametmax.com/les-environnement-virtuels-python-virtualenv-et-virtualenvwrapper/)

Installer virtualenv avec pip:

    pip install virtualenv

Créer un environnement virtuel:

    mkvirtualenv --system-site-packages --prompt '[libhydro]' ~/.virtualenvs/libhydro

ou

    virtualenv --system-site-packages (dest_dir)

On peut:
    * utiliser les paquets de l'environnement de base avec --system-site-packages
(ces paquets sont surchargés par ceux du virtualenv)
    * forcer l'interpréteur à utiliser avec -p (python path)
    * spécifier un prompt spécifique avec --prompt=(prompt)

Pour utiliser l'environnement virtuel:
    * soit utiliser la commande 'source (virtualenv)/bin/activate' | 'deactivate' pour sortir (!! commande générale)
    * soit modifier le python PATH
    * utiliser virtualenvwrapper

### Installer les dépendances de libhydro dans l'environnement virtuel ###
Numpy:

Install Numpy first ! (c module, could be tricky).
Could need the python-devel package.

    (virtualenv)/bin/pip install numpy

Il inappropriate warnings from numpy.loadtxt():
   * edit
       (python)/lib/python2.7/site-packages/numpy-1.6.2-py2.7-linux-x86_64.egg/numpy/lib/npyio.py
     or
       /lib/python2.7/site-packages/numpy/lib/npyio.py
    * comment line 773 '''warnings.warn('loadtxt: Empty input file: "%s"' % fname)'''
    * comment line 1311 '''warnings.warn('genfromtxt: Empty input file: "%s"' % fname)'''

Pandas (do not forget the 's' !!):

    pip install pandas  # dependencies python-dateutil, pytz and six

Lxml:

    sudo yum install libxslt-devel.x86_64 libxml2-devel.x86_64
    pip install lxml  # 3.2.3

Suds (version suds-jurko):

   pip install suds-jurko

Check with pip freeze:

    pip freeze
        numpy==1.7.1
        pandas==0.11.0
        lxml==3.2.3
        python-dateutil==2.1
        pytz==2013b
        six==1.3.0

    pip install -r (pip_freeze_file)

### Installer libhydro ###
    python setup.py install

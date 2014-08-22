INSTALLATION DE LIBHYDRO SOUS LINUX
===============================================================================

* Auteur: philippe.gouin@developpement-durable.gouv.fr
* Version: 0.1a
* Mise à jour: 2014-08-22

Installation packagée de Python
-------------------------------------------------------------------------------

Installer python et pip, un installeur de librairies.

Si yum ou apt ne proposent pas la bonne version de Python, utiliser un dépot
ou un paquet tiers ou bien passer par une compilation.

Exemple:

    yum install python python-pip.noarch

Installation manuelle de Python (compilation)
-------------------------------------------------------------------------------
La procédure décrite ci-dessous est pour CentOS 6.2.
[Réf: http://toomuchdata.com/2012/06/25/how-to-install-python-2-7-3-on-centos-6-2/](http://toomuchdata.com/2012/06/25/how-to-install-python-2-7-3-on-centos-6-2/)

NB: la version python 2.4.3 de l'os, nécessaire pour pas mal de programmes, est
/usr/bin/python.

Installer les dépendances:

    yum groupinstall "Development tools"  # big but requested to enable all features in python
    yum install gcc zlib-devel bzip2-devel openssl-devel ncurses-devel readline-devel sqlite sqlite-devel
    yum install readline-devel.x86_64 readline-devel.i386
    yum install zlib-devel.x86_64 zlib-devel.i386
    yum install sqlite.x86_64 sqlite-devel.x86_64  # sqlite is requested by ipython
    yum install openssl-devel.i386 openssl-devel.x86_64  # optional

Compiler la version la plus récente de la série 2 de Python:

    wget http://www.python.org/ftp/python/2.x.y/Python-2.x.y.tar.bz2
    ./configure
    make
    # use 'make altinstall' if you care overwriting a previous python installation
    su -c 'make install' # default install dans /usr/local/bin/python

Si problème relatif à sqlite3, il faut patcher les sources:

    wget -O patch_sqlite https://raw.github.com/gist/2727063/
    cat patch_sqlite | patch -p1

Télécharger et installer pip et les setuptools:

  wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-x.y.tar.gz
  wget --no-check-certificate https://pypi.python.org/packages/source/p/pip/pip-x.y.z.tar.gz
  python setup.py install  # pour chacun des modules

Pip et les proxy
  Configurer les variables http_proxy, https_proxy et ftp_proxy pour permettre à pip de télécharger les paquets
  par tous les moyens possibles.

  A défaut on peux préciser le proxy directement dans la commande install:

    pip --proxy http://(proxy) install (paquet)

Installation et utilisation de virtualenv
-------------------------------------------------------------------------------
[Réf: http://sametmax.com/les-environnement-virtuels-python-virtualenv-et-virtualenvwrapper/](http://sametmax.com/les-environnement-virtuels-python-virtualenv-et-virtualenvwrapper/)

Installer virtualenv avec pip

    pip install virtualenv

Créer un environnement virtuel

    virtualenv --system-site-packages (dest_dir)

  On peut:

    * utiliser ou pas les paquets de l'environnement de base avec --system-site-packages / --no-site-packages
    (dans le premier cas les paquets sont surchargés par ceux du virtualenv)
    * forcer l'interpréteur à utiliser avec -p (python path)
    * spécifier un prompt spécifique avec --prompt=(prompt)

Utiliser l'environnement virtuel

  * avec la commande 'source (virtualenv)/bin/activate' | 'deactivate' pour sortir (!! commande générale)
  * en modifiant le python PATH
  * en utilisant virtualenvwrapper

Création d'un environnement virtuel avec le wrapper

    mkvirtualenv --system-site-packages --prompt '[libhydro]' ~/.virtualenvs/libhydro

Installer les dépendances de libhydro dans l'environnement virtuel
-------------------------------------------------------------------------------
### Numpy ####

Commande

    (virtualenv)/bin/pip install numpy

Difficultés éventuelles
  Install Numpy first ! (c module, could be tricky). Could need the python-devel package.

  If inappropriate warnings from numpy.loadtxt():

    * edit the npyio.py file
    (can be in (python)/lib/python2.7/site-packages/numpy-1.6.2-py2.7-linux-x86_64.egg/numpy/lib/
    or /lib/python2.7/site-packages/numpy/lib/)
    * comment the line 773 '''warnings.warn('loadtxt: Empty input file: "%s"' % fname)'''
    * comment the line 1311 '''warnings.warn('genfromtxt: Empty input file: "%s"' % fname)'''

#### Pandas (do not forget the 's' !!) ####

Commande

    pip install pandas

Les dépendances suivantes sont automatiquement installées
  python-dateutil, pytz et six

#### Lxml ####

Commande

    sudo yum install libxslt-devel.x86_64 libxml2-devel.x86_64
    pip install lxml  # 3.2.3

#### Suds (version suds-jurko) ####

    pip install suds-jurko

#### Check or install with pip freeze ###

    pip freeze
        numpy==1.7.1
        pandas==0.11.0
        lxml==3.2.3
        python-dateutil==2.1
        pytz==2013b
        six==1.3.0

    pip install -r (pip_freeze_file)


Installer libhydro
-------------------------------------------------------------------------------
Télécharger et décompresser l'archive puis dans un terminal faire:

    python setup.py install

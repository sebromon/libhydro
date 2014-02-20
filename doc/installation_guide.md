INSTALLATION DETAILLE D'UN ENVIRONNEMENT VIRTUEL PYTHON POUR LIBHYDRO
===============================================================================

Installation sous Windows
-------------------------------------------------------------------------------
### Installer Python ###
    utiliser python2.7.5.msi

### Régler les variables d'environnment ###
  [http://docs.python.org/2/using/windows.html]
    "path = ... C:\Program Files\Python27;C:\Program Files\Python27\scripts"
    "PYTHONPATH = ..."
    "proxy = http://direct.proxy.i2:8080"

### Pour ces dépendances en C/C++ utiliser les binaires de http://www.lfd.uci.edu/~gohlke/pythonlibs/ ###
    numpy
    python-dateutil
    pandas
    lxml

### Installer les setup-tools et pip (optionnel) ###
  [ref: http://www.pip-installer.org/en/latest/installing.html]
    get ez_setup.py
    python ez_setup.py
    get get-pip.py
    python get-pip.py (need the proxy !)
    pip install --upgrade setuptools

### Installer IPython (optionnel) ###
    pip install ipython

Installation sous Linux
-------------------------------------------------------------------------------
### Installer Python avec un gestionnaire de paquets ###
yum install python.
Si yum ne propose pas la bonne version, trouver un rpm ou se compiler sa propre version de python.

### Compiler Python sous Linux (CentOs 6.2) ###
Référence: [http://toomuchdata.com/2012/06/25/how-to-install-python-2-7-3-on-centos-6-2/]

La version python 2.4.3 de l'os, nécessaire pour pas mal de programmes, est:
    /usr/bin/python

Dependances:
    # yum groupinstall "Development tools" - big but needed to enable all features in python
    # yum install gcc zlib-devel bzip2-devel openssl-devel ncurses-devel readline-devel sqlite sqlite-devel

    Verifier que gcc est installe, sinon: yum install gcc
    Readline: yum install readline-devel.x86_64 readline-devel.i386
    Zlib: yum install zlib-devel.x86_64 zlib-devel.i386
    Sqlite (for iPython): yum install sqlite.x86_64 sqlite-devel.x86_64
    Ssl (if needed): yum install openssl-devel.i386 openssl-devel.x86_64

Failed to build sqlite3 (need a patch):
    wget -O patch_sqlite https://raw.github.com/gist/2727063/
    cat patch_sqlite | patch -p1

wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2
Python 2.7.3: "./configure", "make", "su -c 'make (alt)install'" -> /usr/local/bin/python
Make altinstall if you care overwriting a previous python installation

### Installer les setuptools ###
Installer de préférence pip qui remplace en mieux easy_install:
    yum install python-pip.noarch  # Pip installs packages

Installer et configurer Virtualenv (Linux)
-------------------------------------------------------------------------------
### Installer et configurer virtualenv ###
http://sametmax.com/les-environnement-virtuels-python-virtualenv-et-virtualenvwrapper/

pip install virtualenv

Creer un environnement virtuel:
    virtualenv --system-site-packages (dest_dir)
On peux utiliser les paquets de l'environnement de base avec --system-site-packages
(ces paquets sont surchargés par ceux du virtualenv)
On peux forcer l'interpréteur à utiliser avec -p (python path)
On peux spécifier un prompt spécifique avec --prompt=(prompt)

Pour utiliser l'environnement virtuel:
    # soit utiliser la commande 'source (virtualenv)/bin/activate' | 'deactivate' pour sortir (!! commande générale)
    # soit modifier le python PATH
    # utiliser virtualenvwrapper

Installer les dépendances dans l'environnement virtuel (Linux)
-------------------------------------------------------------------------------
Numpy
    install Numpy first ! (c module, could be tricky)
    could need: yum install python-devel
    (virtualenv)/bin/pip install numpy

    !!! Suppress numpy.loadtxt() inappropriate warnings: !!!
    * vi (python)/lib/python2.7/site-packages/numpy-1.6.2-py2.7-linux-x86_64.egg/numpy/lib/npyio.py
            OU    /lib/python2.7/site-packages/numpy/lib/npyio.py
    * comment line 773 '''warnings.warn('loadtxt: Empty input file: "%s"' % fname)'''
    * comment line 1311 '''warnings.warn('genfromtxt: Empty input file: "%s"' % fname)'''

Pandas (do not forget the 's' !!)
    pip install pandas
    (dependencies python-dateutil, pytz and six)

Lxml:
    sudo yum install libxslt-devel.x86_64 libxml2-devel.x86_64
    pip install lxml  # 3.2.3

Suds (version suds-jurko):
   pip install suds-jurko

Check with pip freeze:
    pip freeze:
        numpy==1.7.1
        pandas==0.11.0
        lxml==3.2.3
        python-dateutil==2.1
        pytz==2013b
        six==1.3.0

    pip install -r (pip_freeze_file)

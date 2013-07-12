===============================================================================
INSTALLATION D'UN ENVIRONNEMENT DE DEVELOPPEMENT EN PYTHON POUR LIBHYDRO
===============================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Python 2.7.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Installation sous Windows
-------------------------------------------------------------------------------
** TODO **

Installation sous Linux
-------------------------------------------------------------------------------
yum install python.
Si yum ne propose pas la bonne version, trouver un rpm ou se compiler sa propre version de python.

Compilation de Python sous Linux (CentOs 6.2)
-------------------------------------------------------------------------------
[ http://toomuchdata.com/2012/06/25/how-to-install-python-2-7-3-on-centos-6-2/ ]
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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
2.  Setuptools (pip) et virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Installer les setuptools sous Linux
-------------------------------------------------------------------------------
Installer de préférence pip qui remplace en mieux easy_install:
    yum install python-pip.noarch  # Pip installs packages

Installer et configurer virtualenv
-------------------------------------------------------------------------------
`<http://sametmax.com/les-environnement-virtuels-python-virtualenv-et-virtualenvwrapper/>`_

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

------------------------------------------------------------------------------
3. Installer les dépendances dans l'environnement virtuel
------------------------------------------------------------------------------

Numpy
    install Numpy first ! (c module, could be tricky)
    could need: yum install python-devel
    (virtualenv)/bin/pip install numpy

    --- ** bdimage doc ** ----------
    !!! Suppress numpy.loadtxt() inappropriate warnings: !!!
    * vi (python)/lib/python2.7/site-packages/numpy-1.6.2-py2.7-linux-x86_64.egg/numpy/lib/npyio.py
            OU    /lib/python2.7/site-packages/numpy/lib/npyio.py
    * comment line 773 '''warnings.warn('loadtxt: Empty input file: "%s"' % fname)'''
    * comment line 1311 '''warnings.warn('genfromtxt: Empty input file: "%s"' % fname)'''
    --- ** bdimage doc ** ----------

Pandas (do not forget the 's' !!)
    pip install pandas
    (dependencies python-dateutil, pytz and six)

** TODO ** ------------
    GENSHI 0.6 (templating engine)
    pip install genshi
** TODO ** ------------

Check with pip freeze:

    pip freeze:

        numpy==1.7.1
        pandas==0.11.0
        python-dateutil==2.1
        pytz==2013b
        six==1.3.0

    pip install -r (pip_freeze_file)

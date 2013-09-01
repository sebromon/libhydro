MERCURIAL INSTALLATION ET CONFIGURATION
===============================================================================

Références
-------------------------------------------------------------------------------
Le site de Mercurial <http://mercurial.selenic.com/>
A tutorial by Joel Spolsky <http://hginit.com/>

Installation de  Mercurial
-------------------------------------------------------------------------------
### Redhat linux ###
yum install mercurial

### Windows ###
** TODO **

Configuration locale
-------------------------------------------------------------------------------
Référence: [http://www.selenic.com/mercurial/hgrc.5.html](http://www.selenic.com/mercurial/hgrc.5.html])

### Linux ###
~/.hgrc pour un fichier de config générale

(repo)/.hg/hgrc pour un fichier de config spécifique au dépot (prioritaire)

### Windows ###
    %USERPROFILE%\mercurial.ini file

### Exemple de fichier hgrc ###

    [ui]
    username = Firstname Lastname <firstname.lastname@example.net>

** TODO ** installer un outil de merge

Cloner le dépôt de référence
-------------------------------------------------------------------------------
### Dépôt de test ###
    hg clone http://arc.schapi:8000/ (dest)

### Libhydro ###
    hg clone http://arc.schapi:8001/ (dest)

Organisation du dépot Libhydro
-------------------------------------------------------------------------------
### Tree ###
* bin - programmes
* conv (package) - convertisseurs de et vers differents formats
* core (package) - bibliotheque principale
* doc - documentation
* test - tests

### Branches ###
Default is the developpement branch
Stable is the releases branch
Référence: [http://stevelosh.com/blog/2010/05/mercurial-workflows-stable-default](http://stevelosh.com/blog/2010/05/mercurial-workflows-stable-defaul)

### Revisions ###
Référence: [http://semver.org/](http://semver.org/)

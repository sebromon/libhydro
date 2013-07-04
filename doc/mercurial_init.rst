~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 REF: http://mercurial.selenic.com/
TUTO: http://hginit.com/ - A tutorial by Joel Spolsky
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

===============================================================================
1./ Installation de  Mercurial
===============================================================================
# redhat linux: yum install mercurial
# windows

===============================================================================
2./ Configuration locale
===============================================================================
REF: http://www.selenic.com/mercurial/hgrc.5.html

# linux: ~/.hgrc
# windows: %USERPROFILE%\mercurial.ini

Basic content:
--------------
[ui]
username = Firstname Lastname <firstname.lastname@example.net>
verbose = True

===============================================================================
3./ Cloner le dépôt de référence
===============================================================================
Dépôt de test:
    hg clone http://arc.schapi:8000/ sandbox

Libhydro:
    hg clone http://arc.schapi:8001/ libhydro


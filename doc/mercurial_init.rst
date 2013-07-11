===============================================================================
MERCURIAL INIT
===============================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
0./ References
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Le site de Mercurial <http://mercurial.selenic.com/>`_.

`A tutorial by Joel Spolsky <http://hginit.com/>`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1./ Installation de  Mercurial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Redhat linux:

    yum install mercurial

Windows:

    ** TODO **

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
2./ Configuration locale
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. seealso: `<http://www.selenic.com/mercurial/hgrc.5.html>`_

Linux:

    ~/.hgrc pour un fichier de config générale
    (repo)/.hg/hgrc pour un fichier de config spécifique au dépot (prioritaire)

Windows:

    %USERPROFILE%\mercurial.ini file

Minimum content::
    [ui]
    username = Firstname Lastname <firstname.lastname@example.net>

** TODO ** installer un outil de merge

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
3./ Cloner le dépôt de référence
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dépôt de test:

    hg clone http://arc.schapi:8000/ (dest)

Libhydro:

    hg clone http://arc.schapi:8001/ (dest)


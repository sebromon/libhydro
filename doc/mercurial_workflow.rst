===============================================================================
MERCURIAL WORKFLOW
===============================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
0./ References
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 `Le site de Mercurial <http://mercurial.selenic.com/>`_.

`Reference cards and cheat sheets <http://mercurial.selenic.com/wiki/QuickReferenceCardsAndCheatSheets>`_.

`A tutorial by Joel Spolsky <http://hginit.com/>`_.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1./ Basic workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    (clone once)

        -->  --> <make changes>, commit (save changes)
        |    |_____
        |
        |    pull and merge (sync working directory <> local repository)
        |______

        push (local repo => main repo)


    Merge often! This makes merging easier for everyone and you find out
    about conflicts (which are often rooted in incompatible design decisions)
    earlier.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
2./ Basic commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

hg commit -m '(message)'
hg pull (project)         # pull changesets from project
hg merge                  # merge the new tip from project into our working directory
hg push (project)         # push changesets from project

hg parents
hg status
hg log

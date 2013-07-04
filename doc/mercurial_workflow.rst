~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 REF: http://mercurial.selenic.com/
      http://mercurial.selenic.com/wiki/QuickReferenceCardsAndCheatSheets - Reference cards and cheat sheets
TUTO: http://hginit.com/ - A tutorial by Joel Spolsky
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

===============================================================================
Basic workflow
===============================================================================
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

===============================================================================
Basic commands
===============================================================================
hg commit -m '(message)'
hg pull (project)   # pull changesets from project
hg merge            # merge the new tip from project into our working directory
hg push (project)   # push changesets from project

hg parents
hg status
hg log

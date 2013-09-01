MERCURIAL BASIC WORKFLOW
===============================================================================

References
-------------------------------------------------------------------------------

[Le site de Mercurial](http://mercurial.selenic.com/)

[Reference cards and cheat sheets](http://mercurial.selenic.com/wiki/QuickReferenceCardsAndCheatSheets)

[A tutorial by Joel Spolsky](http://hginit.com/)

Basic workflow
-------------------------------------------------------------------------------

    (clone once)

    -->  --> <make changes>, commit (save changes)
    |    |_____
    |
    |    pull and merge (sync working directory <> local repository)
    |______

    push (local repo => main repo)

* Merge often! * This makes merging easier for everyone and you find out
about conflicts (which are often rooted in incompatible design decisions)
earlier.

Basic commands
-------------------------------------------------------------------------------
    hg status
    hg log|glog
    hg parents
    hg commit -m '(message)'
    hg update

    hg incoming|pull (project)         # pull changesets from project
    hg merge                  # merge the new tip from project into our working directory
    hg outgoing|push (project)         # push changesets from project

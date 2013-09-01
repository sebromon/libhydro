INSTALLATION D'UN ENVIRONNEMENT DE DEVELOPPEMENT EN PYTHON POUR LIBHYDRO
===============================================================================

Ces outils sont à installer dans l'environnement virtuel.

Avec pip freeze
-------------------------------------------------------------------------------

pip install -r (pip_freeze_file)
ou
pip install < pip_freeze

Note: pip bundle could be an easy way

pip freeze:
    ** TODO **

Installation personnalisée
-------------------------------------------------------------------------------

### pip install ipython ###
???? ####pip install matplotlib pandas (scipy ympy nose)
pip install ipdb

### ipython qtconsole ###
    * difficile à installer uniquement dans l'environnement virtuel, le faire
      dans l'environnement de base avant et utiliser
      --system-site-packages à la création du virtualenv
    * installer PyQt4 et les autres dépendances

** TODO ** quality code tools

### Tests ###
nose et coverage

iPython, QtConsole and matplotlib
-------------------------------------------------------------------------------
Launch iPython QtConsole with dark colors and inbeded matplotlib graphs:
    ipython qtconsole --colors=linux --pylab=inline

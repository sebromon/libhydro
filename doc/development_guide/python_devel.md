INSTALLATION D'UN ENVIRONNEMENT DE DEVELOPPEMENT EN PYTHON POUR LIBHYDRO
===============================================================================

Ces outils sont à installer dans l'environnement virtuel.

IPython
-------------------------------------------------------------------------------
### ipython ###
pip install ipython, ipdb

### ipython qtconsole ###
* difficile à installer uniquement dans l'environnement virtuel, le faire
  dans l'environnement de base avant et utiliser
  --system-site-packages à la création du virtualenv
* installer PyQt4 et les autres dépendances

Launch iPython QtConsole with dark colors and inbeded matplotlib graphs:
    ipython qtconsole --colors=linux --pylab=inline

Outils de test
-------------------------------------------------------------------------------
pip install coverage, nose

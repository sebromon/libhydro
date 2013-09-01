INSTALLATION D'UN ENVIRONNEMENT DE DEVELOPPEMENT EN PYTHON POUR LIBHYDRO
===============================================================================

Ces outils sont à installer dans l'environnement virtuel.

Installer IPython et Qt Console (facultatif)
-------------------------------------------------------------------------------
### IPython ###
    pip install ipython, ipdb

### IPython Qt Console ###
* difficile à installer uniquement dans l'environnement virtuel, le faire
  dans l'environnement de base avant et utiliser
  --system-site-packages à la création du virtualenv
* installer PyQt4 et les autres dépendances

Launch iPython QtConsole with dark colors and inbeded matplotlib graphs:

    ipython qtconsole --colors=linux --pylab=inline

Installer les outils de test (facultatif)
-------------------------------------------------------------------------------
    pip install coverage, nose

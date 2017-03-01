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

Les test et PIP
-------------------------------------------------------------------------------
Les tests nécessitent que la libhydro soit accessible dans
l'environnement Python utilisé. Pour que la version de la libhydro en
cours de développement soit prise en compte, il convient de l'installer
avec le mode 'éditable' de PIP (option -e). Depuis le dossier principal
du dépôt ou figure le fichier setup.py, utiliser la commande:
```
#!sh
pip install -e .
```

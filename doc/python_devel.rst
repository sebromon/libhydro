===============================================================================
INSTALLATION D'UN ENVIRONNEMENT DE DEVELOPPEMENT EN PYTHON POUR LIBHYDRO
===============================================================================

Ces outils sont à installer dans l'environnement virtuel.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1./ Avec pip freeze
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pip install -r (pip_freeze_file)
ou
pip install < pip_freeze

.. note: pip bundle could be an easy way

pip freeze:
    ** TODO **

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
2./ Installation personnalisée
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pip install ipython
???? ####pip install matplotlib pandas (scipy ympy nose)
pip install ipdb

ipython qtconsole:
    difficile à installer uniquemetn dans l'environnement virtuel, le faire dans l'environnement de base avant et utiliser
        --system-site-packages à la création du virtualenv
    installer PyQt4 et les autres dépendances

** TODO ** quality code tools

Tests: nose et coverage

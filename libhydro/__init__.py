# coding: utf-8
"""Meta-package libhydro.

Le meta-package libhydro est constitue des packages:
    # core qui contient les classes permettant de manipuler les objets
        hydrometriques
    # conv qui propose des convertisseurs de et vers differents formats

"""
# bdhydro pour l'utilisation des services web d'Hydro3
__version__ = '0.6.0-alpha'
__all__ = ['core', 'conv']
# __all__ = ['core', 'conv', 'bdhydro']

# from .bdhydro import bdhydro

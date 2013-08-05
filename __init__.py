# -*- coding: utf-8 -*-
"""Package python libhydro.

Ce package expose les classes modelisees par le Sandre dans les dictionnaires:
    # Referentiel hydrometrique
    # Processus d'acquisition des donnees hydrometriques

Le sous package conv contient des convertisseurs de et vers differents formats.

"""
# These lines gives the user ability to ignore the core sub-package.
# One can use:
#     'from libhydro import (module)'
#         instead of 'from libhydro.core import (module)'
#     'from libhydro.module import (Class)'
#         instead of 'from libhydro.core.module import (Class)'
from libhydro.core import nomenclature
from libhydro.core import sitehydro
from libhydro.core import obshydro

# alarm
# courbecorrection
# courbetarage
# evenement
# gradienthydro
# intervenant
# jaugeage
# modeleprevision
# obselaboreehydro
# obsmeteo
# qualifannee
# scenario
# simulation
# sitemeteo

# -*- coding: utf-8 -*-
"""Module libhydro.conv.xml.

Le module xml contient des convertisseurs de et vers les fichiers au format
Xml Hydrometrie (version 1.1 exclusivement), disponibles au travers la classe
Message.

Il contient les classes:
    # Message
    # Scenario

Exemples d'utilisation:
    La fonction principale pour decoder des messages Xml est
    'xml.from_file(src)' qui permet d'instancier un objet Message contenant
    tous les objets decrits dans le fichier source.

    > m = xml.Message('fichier_xml_hydrometrie.xml')
    > print(m)
        Message du 2012-06-04 09:22:44
        Emis par le Contact 842:: Monsieur Jean Jean pour l'Intervenant
            SANDRE 845::SPC de la Colline [1 contact]
        Contenu: 5 siteshydro - 9 seuilshydro - 3 evenements
                 2 series - 5 simulations

    Pour serialiser (enregistrer dans un fichier) des donnees en Xml on
    utilise la methode 'write(file)' d'un Message.

"""
__all__ = ['Message', 'Scenario']
# for the user, this package is like a module, sub-modules names are
# underscored to hide them
from ._from_xml import Scenario
from ._xml import Message

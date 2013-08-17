# -*- coding: utf-8 -*-

#-- imports -------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals,
    absolute_import as _absolute_import,
    division as _division,
    print_function as _print_function
)

import datetime as _datetime
from lxml import etree as _etree

from . import mapping


class Scenario(object):

    def __init__(self):
        self.code = 'hydrometrie'
        self.version = 1.1
        self.nom = 'Echange de données hydrométriques'
        self.dtfichier = _datetime.datetime.utcnow()

    # <Emetteur><CdIntervenant schemeAgencyID="SANDRE">1537</CdIntervenant>
    #           <CdContact schemeAgencyID="SANDRE">1</CdContact>

        # destinataire = destinataire


def to_xml(scenario, *args):

        # import ipdb; ipdb.set_trace()

        tree = _etree.Element('hydrometrie')

        # add scenario
        s = _etree.SubElement(tree, 'Scenario')
        for (k, v) in mapping.scenario.iteritems():
            child = _etree.SubElement(s, v)
            child.text = unicode(getattr(scenario, k))

        # add args

        # return
        print(
            _etree.tostring(
                tree, encoding='utf-8', xml_declaration=1,  pretty_print=1
            )
        )
        return tree

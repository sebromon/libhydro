# -*- coding: utf-8 -*-
"""Test program for rolecontact.

To run all tests just type:
    python -m unittest test_core_rolecontact

To run only a class test:
    python -m unittest test_core_rolecontact.TestClass

To run only a specific test:
    python -m unittest test_core_rolecontact.TestClass.test_method

"""

# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import unittest
import datetime as _datetime
from libhydro.core.rolecontact import RoleContact
from libhydro.core import intervenant as _intervenant


class TestRoleContact(unittest.TestCase):
    """Role class tests."""

    def test_base_01(self):
        """Simple Role"""
        contact = _intervenant.Contact(code='1234')
        role = 'ADM'
        rol = RoleContact(contact=contact, role=role)
        self.assertEqual((rol.contact, rol.role, rol.dtdeb, rol.dtfin,
                          rol.dtmaj),
                         (contact, role, None, None, None))

    def test_base_02(self):
        """Full role"""
        contact = _intervenant.Contact(code='4321')
        role = 'EXP'
        dtdeb = _datetime.datetime(2010, 4, 1, 10, 30, 40)
        dtfin = _datetime.datetime(2034, 10, 12, 17, 25, 51)
        dtmaj = _datetime.datetime(2018, 8, 14, 11, 15, 23)
        rol = RoleContact(contact=contact, role=role, dtdeb=dtdeb, dtfin=dtfin,
                          dtmaj=dtmaj)
        self.assertEqual((rol.contact, rol.role, rol.dtdeb, rol.dtfin,
                          rol.dtmaj),
                         (contact, role, dtdeb, dtfin, dtmaj))

    def test_str_01(self):
        """Test representation simple role"""
        code = '1234'
        contact = _intervenant.Contact(code=code)
        role = 'ADM'
        rol = RoleContact(contact=contact, role=role)
        rol_str = rol.__unicode__()
        self.assertTrue(rol_str.find(code) != -1)
        self.assertTrue(rol_str.find(role) != -1)

    def test_str_02(self):
        """Test representation full role"""
        code = '1234'
        contact = _intervenant.Contact(code=code)
        role = 'PRV'
        dtdeb = _datetime.datetime(2010, 4, 1, 10, 30, 40)
        dtfin = _datetime.datetime(2034, 10, 12, 17, 25, 51)
        dtmaj = _datetime.datetime(2018, 8, 14, 11, 15, 23)
        rol = RoleContact(contact=contact, role=role, dtdeb=dtdeb, dtfin=dtfin,
                          dtmaj=dtmaj)
        rol_str = rol.__unicode__()
        self.assertTrue(rol_str.find(code) != -1)
        self.assertTrue(rol_str.find(role) != -1)
        self.assertTrue(rol_str.find(dtdeb.strftime('%Y-%m-%d %H:%M:%S')))
        self.assertTrue(rol_str.find(dtfin.strftime('%Y-%m-%d %H:%M:%S')))

    def test_error_contact(self):
        """Test error contact"""
        contact = _intervenant.Contact(code='4321')
        role = 'EXP'
        RoleContact(contact=contact, role=role)
        for contact in [None, '4321', 'toto']:
            with self.assertRaises(TypeError):
                RoleContact(contact=contact, role=role)

    def test_error_role(self):
        """Test error role"""
        contact = _intervenant.Contact(code='4321')
        role = 'PRV'
        RoleContact(contact=contact, role=role)
        for role in [None, 0, 'toto']:
            with self.assertRaises(Exception):
                RoleContact(contact=contact, role=role)

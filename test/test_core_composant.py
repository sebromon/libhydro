# coding: utf-8
"""Test program for composant.

To run all tests just type:
    python -m unittest test_core_composant

To run only a class test:
    python -m unittest test_core_composant.TestClass

To run only a specific test:
    python -m unittest test_core_composant.TestClass.test_method

"""
# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import sys
import unittest
# python3
import io

from libhydro.core import _composant as composant
import datetime
import numpy


# -- strings ------------------------------------------------------------------
__version__ = '0.5.3'
__date__ = '2014-12-18'

# HISTORY
# V0.5 - 2014-12-18
#   add the __eq__ and __ne__ tests
# V0.4 - 2014-07-20
#   add the error_handler, Rlist and Rlistpropery tests
# V0.3 - 2014-07-16
#   remove the composant_site part
# V0.2 - 2014-03-01
#   add the descriptor tests
# V0.1 - 2013-11-07
#   first shot


# -- class TestErrorHandler ---------------------------------------------------
class TestErrorHandler(unittest.TestCase):

    """Error handler class tests."""

    def test_ignore(self):
        """Ignore error test."""
        error_handler = composant.ERROR_HANDLERS['ignore']
        self.assertIsNone(error_handler())
        self.assertIsNone(
            error_handler(msg='a message', error=TypeError))
        self.assertIsNone(error_handler('egfsksdùkf'))

    def test_warn(self):
        """Warn error test."""
        # we need stderr to be a string
        f = io.StringIO()
        sys.stderr = f
        error_handler = composant.ERROR_HANDLERS['warn']
        error_handler('message')
        f.seek(0)
        message = f.readlines()[0]
        self.assertTrue(message.rfind('wwwww') == -1)
        self.assertTrue(message.rfind('message') > -1)
        self.assertTrue(message.rfind('UserWarning') > -1)

    def test_strict(self):
        """Strict error test."""
        error_handler = composant.ERROR_HANDLERS['strict']
        with self.assertRaises(TypeError):
            error_handler(msg='a message', error=TypeError)
        with self.assertRaises(ValueError):
            error_handler(msg='a message', error=ValueError)


# -- class TestRlist ----------------------------------------------------------
class TestRlist(unittest.TestCase):

    """Rlist class tests."""

    def test_01(self):
        """Rlist base test."""
        intl = composant.Rlist(int, [1, 2, 3])
        intl.append(4)
        intl.insert(0, 0)
        self.assertEqual(intl.cls, int)
        self.assertEqual(len(intl), 5)

    def test_02(self):
        """Rlist other test."""
        strl = composant.Rlist(str, ['0', '1', '2', '3'])
        strl.extend(['444'])
        strl[0:2] = ['000', '111']
        self.assertEqual(strl.cls, str)
        self.assertEqual(len(strl), 5)

    def test_checkiterable(self):
        """Test checkiterable."""
        strl = composant.Rlist(str, [str('aa'), str('bb')])
        self.assertTrue(strl.checkiterable([str('c'), str('d')]))
        # Replace this test 
        #self.assertFalse(strl.checkiterable(['c', 'd'], errors='ignore'))
        self.assertFalse(strl.checkiterable(['c', 8], errors='ignore'))

    def test_error_01(self):
        """Error handler test."""
        strl = composant.Rlist(str, [str('aa'), str('bb')])
        with self.assertRaises(ValueError):
            strl.checkiterable([], errors='gloups!')


# -- class TestRlistproperty --------------------------------------------------
class TestRlistproperty(unittest.TestCase):

    """Rlistproperty class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # define a class with int datas
        class List_of_int_required(object):
            data = composant.Rlistproperty(int, required=True)

            def __init__(self, data=None):
                self.data = data

        self.LOIR = List_of_int_required

        # define a class with int datas
        class List_of_int_not_required(object):
            data = composant.Rlistproperty(int, required=False)

            def __init__(self, data=None):
                self.data = data

        self.LOINR = List_of_int_not_required

    def test_list_of_int_required(self):
        """List_of_int_required test."""
        l = self.LOIR([1, 2, 3])
        self.assertEqual(len(l.data), 3)
        with self.assertRaises(ValueError):
            self.LOIR(None)

    def test_list_of_int_not_required(self):
        """List_of_int_not_required test."""
        l = self.LOINR(None)
        l = self.LOINR([1, 2, 3])
        self.assertEqual(len(l.data), 3)


# -- class TestDatefromeverything ---------------------------------------------
class TestDatefromeverything(unittest.TestCase):

    """Datefromeverything class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # define a class with value required
        class VR(object):
            dt = composant.Datefromeverything(required=True)

            def __init__(self, dt=None):
                self.dt = dt

        self.VR = VR

        # define a class with value not required
        class VNR(object):
            dt = composant.Datefromeverything(required=False)

            def __init__(self, dt=None):
                self.dt = dt

        self.VNR = VNR

    def test_value_required_init(self):
        """Test the setters and getters when value is required."""
        # init
        dt = datetime.datetime(2008, 10, 10, 9, 33)
        vrs = []
        # build various objects
        vrs.append(self.VR(
            numpy.datetime64('2008-10-10T09:33')))
        vrs.append(self.VR('2008-10-10T09:33'))
        vrs.append(self.VR(dt))
        vrs.append(self.VR([2008, 10, 10, 9, 33]))
        vrs.append(self.VR(
            {'year': 2008, 'month': 10, 'day': 10, 'hour': 9, 'minute': 33}))
        for vr in vrs:
            self.assertEqual(vr.dt, dt)

    def test_value_required_error(self):
        """The value required error."""
        with self.assertRaises(TypeError):
            self.VR(None)
        with self.assertRaises(ValueError):
            self.VR('2014-13-08')
        with self.assertRaises(ValueError):
            self.VR(2014)
        with self.assertRaises(ValueError):
            self.VR([2014])

    def test_value_not_required_init(self):
        """Test the setters and getters when value is not required."""
        # init
        dt = datetime.datetime(2010, 1, 5)
        vnrs = []
        # build various objects
#         vnrs.append(self.VNR(
#             numpy.datetime64('2010-01-05T02:00+02:00')))
#         vnrs.append(self.VNR('2010-01-05T02:00+02:00'))
        vnrs.append(self.VNR(dt))
        vnrs.append(self.VNR([2010, 1, 5, 0, 0]))
        vnrs.append(self.VNR([2010, 1, 5]))
        vnrs.append(self.VNR(
            {'year': 2010, 'month': 1, 'day': 5, 'minute': 0}))
        vnrs.append(self.VNR(
            {'year': 2010, 'month': 1, 'day': 5}))
        for vnr in vnrs:
            self.assertEqual(vnr.dt, dt)

    def test_value_not_required_error(self):
        vnr = self.VNR()
        self.assertEqual(vnr.dt, None)
        vnr.dt = None


# -- class TestNomenclatureitem -----------------------------------------------
class TestNomenclatureitem(unittest.TestCase):

    """Nomenclatureitem class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        # define a default class
        class NI_strict_required(object):
            ni = composant.Nomenclatureitem(nomenclature=509)

            def __init__(self, ni):
                self.ni = ni

        self.NI_strict_required = NI_strict_required

        # define a class with strict=False
        class NI_required(object):
            ni = composant.Nomenclatureitem(nomenclature=509, strict=False)

            def __init__(self, ni='default value not in nomenclature'):
                self.ni = ni

        self.NI_required = NI_required

        # define a class with required=False
        class NI_strict(object):
            ni = composant.Nomenclatureitem(nomenclature=509, required=False)

            def __init__(self, ni='H'):
                self.ni = ni

        self.NI_strict = NI_strict

    def test_NI_strict_required(self):
        """NI_strict_required test.

        Test the setters and getters when a value is required and has to
        match the nomenclature.

        """
        ni = self.NI_strict_required('H')
        self.assertEqual(ni.ni, 'H')
        ni = self.NI_strict_required('Q')
        self.assertEqual(ni.ni, 'Q')
        ni.ni = 'H'
        self.assertEqual(ni.ni, 'H')

    def test_NI_strict_required_error(self):
        """NI_strict_required error."""
        with self.assertRaises(ValueError):
            self.NI_strict_required(None)
        with self.assertRaises(ValueError):
            self.NI_strict_required('Z')
        ni = self.NI_strict_required('H')
        with self.assertRaises(ValueError):
            ni.__setattr__(*('ni', 'Z'))
        with self.assertRaises(ValueError):
            ni.__setattr__(*('ni', None))

    def test_NI_required(self):
        """NI_required test.

        Test the setters and getters when a value is required.

        """
        ni = self.NI_required('H')
        self.assertEqual(ni.ni, 'H')
        ni = self.NI_required('Q')
        self.assertEqual(ni.ni, 'Q')
        ni = self.NI_required('Z')
        self.assertEqual(ni.ni, 'Z')
        ni = self.NI_required(3)
        self.assertEqual(ni.ni, '3')
        ni = self.NI_required()
        self.assertEqual(ni.ni, 'default value not in nomenclature')
        ni.ni = 5
        self.assertEqual(ni.ni, '5')

    def test_NI_required_error(self):
        """NI_required error."""
        with self.assertRaises(ValueError):
            self.NI_required(None)
        ni = self.NI_required('H')
        with self.assertRaises(ValueError):
            ni.__setattr__(*('ni', None))

    def test_NI_strict(self):
        """NI_strict test.

        Test the setters and getters whith a strict property.

        """
        ni = self.NI_strict('H')
        self.assertEqual(ni.ni, 'H')
        ni = self.NI_strict('Q')
        self.assertEqual(ni.ni, 'Q')
        ni = self.NI_strict(None)
        self.assertEqual(ni.ni, None)
        # default value
        ni = self.NI_strict()
        self.assertEqual(ni.ni, 'H')
        ni.ni = None
        self.assertEqual(ni.ni, None)
        ni.ni = 'Q'
        self.assertEqual(ni.ni, 'Q')

    def test_NI_strict_error(self):
        """NI_strict error."""
        with self.assertRaises(ValueError):
            self.NI_strict(3)
        with self.assertRaises(ValueError):
            self.NI_strict('Z')
        ni = self.NI_strict('H')
        with self.assertRaises(ValueError):
            ni.__setattr__(*('ni', '333'))

    def test_error_01(self):
        """Nomenclature error."""
        with self.assertRaises(ValueError):
            composant.Nomenclatureitem(**{'nomenclature': 0})


# -- class TestPasDeTemps -----------------------------------------------
class TestPasDeTemps(unittest.TestCase):

    """PasDeTemps class tests."""

    def test_base_01(self):
        """ Test pas de temps in minutes."""
        duree = 4
        pas = composant.PasDeTemps(duree=duree)
        self.assertEqual(pas.duree, datetime.timedelta(minutes=duree))
        self.assertEqual(pas.unite, composant.PasDeTemps.MINUTES)
        self.assertEqual(pas.to_int(), duree)
        unite = composant.PasDeTemps.MINUTES
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.duree, datetime.timedelta(minutes=duree))
        self.assertEqual(pas.unite, unite)
        self.assertEqual(pas.to_int(), duree)

    def test_base_02(self):
        """ Test pas de temps in hours."""
        duree = 8
        unite = composant.PasDeTemps.HEURES
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.duree, datetime.timedelta(hours=duree))
        self.assertEqual(pas.unite, unite)
        self.assertEqual(pas.to_int(), duree)

    def test_base_03(self):
        """ Test pas de temps in days."""
        duree = 3
        unite = composant.PasDeTemps.JOURS
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.duree, datetime.timedelta(days=duree))
        self.assertEqual(pas.unite, unite)
        self.assertEqual(pas.to_int(), duree)

    def test_base_04(self):
        """ test pas de temps in seconds."""
        duree = 48
        unite = composant.PasDeTemps.SECONDES
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.duree, datetime.timedelta(seconds=duree))
        self.assertEqual(pas.unite, unite)
        self.assertEqual(pas.to_int(), duree)

    def test_base_05(self):
        """ test duree timedelta"""
        duree = datetime.timedelta(minutes=5)
        unite = composant.PasDeTemps.MINUTES
        pdt = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pdt.duree, duree)

    def test_to_int_01(self):
        """test method to_int with duree int"""
        duree = 3
        unite = composant.PasDeTemps.JOURS
        pdt = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pdt.to_int(), 3)

    def test_to_int_02(self):
        """test method to_int with duree timedelta """
        duree = datetime.timedelta(days=1)
        unite = composant.PasDeTemps.MINUTES
        pdt = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pdt.to_int(), 1440)

    def test_error_unite(self):
        """Error unite"""
        duree = 15
        unite = composant.PasDeTemps.MINUTES
        composant.PasDeTemps(duree=duree, unite=unite)

        unite = 'toto'
        with self.assertRaises(ValueError):
            composant.PasDeTemps(duree=duree, unite=unite)

    def test_error_duree(self):
        """Error duree"""
        duree = 15
        unite = composant.PasDeTemps.MINUTES
        composant.PasDeTemps(duree=duree, unite=unite)

        duree = -1
        with self.assertRaises(ValueError):
            composant.PasDeTemps(duree=duree, unite=unite)

        duree = 'toto'
        with self.assertRaises(Exception):
            composant.PasDeTemps(duree=duree, unite=unite)

        duree = None
        with self.assertRaises(Exception):
            composant.PasDeTemps(duree=duree, unite=unite)

    def test_str_01(self):
        """str pas de temps in minutes"""
        duree = 8
        unite = composant.PasDeTemps.MINUTES
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.__unicode__(), '8 m')

    def test_str_02(self):
        """str pas de temps in hours"""
        duree = 5
        unite = composant.PasDeTemps.HEURES
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.__unicode__(), '5 h')

    def test_str_03(self):
        """str pas de temps in days"""
        duree = 10
        unite = composant.PasDeTemps.JOURS
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.__unicode__(), '10 j')
        self.assertEqual(pas.__str__(), '10 j')

    def test_str_04(self):
        """str pas de temps in days"""
        duree = datetime.timedelta(days=10)
        unite = composant.PasDeTemps.MINUTES
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.__unicode__(), '14400 m')
        self.assertEqual(pas.__str__(), '14400 m')

    def test_str_05(self):
        """str pas de temps in days"""
        duree = datetime.timedelta(minutes=10, seconds=8)
        unite = composant.PasDeTemps.MINUTES
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.__unicode__(), '10 m')
        self.assertEqual(pas.__str__(), '10 m')

    def test_str_06(self):
        """str pas de temps in seconds"""
        duree = datetime.timedelta(minutes=10, seconds=17)
        unite = composant.PasDeTemps.SECONDES
        pas = composant.PasDeTemps(duree=duree, unite=unite)
        self.assertEqual(pas.__unicode__(), '617 s')
        self.assertEqual(pas.__str__(), '617 s')


# -- class TestIsCodeHydro ----------------------------------------------------
class TestIsCodeHydro(unittest.TestCase):

    """Function is_code_hydro class tests."""

    def test_bool_true(self):
        """True test."""
        self.assertTrue(composant.is_code_hydro('A3330510', errors='ignore'))
        self.assertTrue(composant.is_code_hydro('A3330510', errors='strict'))
        self.assertTrue(
            composant.is_code_hydro('A333051002', 10, errors='ignore'))
        # code hydro can begin with a digit
        self.assertTrue(
            composant.is_code_hydro('1333051002', 10, errors='ignore'))
        self.assertTrue(
            composant.is_code_hydro('A333051002', 10, errors='strict'))
        self.assertTrue(
            composant.is_code_hydro('A33305100101', 12, errors='ignore'))
        self.assertTrue(
            composant.is_code_hydro('A33305100101', 12, errors='strict'))
        # a bastard code Hydro2 !
        self.assertTrue(composant.is_code_hydro('A842020C', errors='strict'))
        self.assertTrue(composant.is_code_hydro('A842020C', errors='ignore'))

    def test_bool_false(self):
        """False test."""
        # TypeError
        self.assertFalse(composant.is_code_hydro(33, errors='ignore'))
        # too short
        self.assertFalse(composant.is_code_hydro('A330010', errors='ignore'))
        # too long
        self.assertFalse(
            composant.is_code_hydro('A2233305100101', 12, errors='ignore'))
        # wrong chars
        self.assertFalse(
            composant.is_code_hydro('a330051002', 10, errors='ignore'))
        self.assertFalse(
            composant.is_code_hydro('A330C5100201', 12, errors='ignore'))
        self.assertFalse(
            composant.is_code_hydro('A33051CC', errors='ignore'))

    def test_errors_01(self):
        """Error code test."""
        # TypeError
        with self.assertRaises(TypeError):
            composant.is_code_hydro(**{'code': 33, 'errors': 'strict'})
        # too short
        with self.assertRaises(ValueError):
            composant.is_code_hydro(**{'code': 'A330010', 'errors': 'strict'})
        # too long
        with self.assertRaises(ValueError):
            composant.is_code_hydro(
                **{'code': 'A2233305100101', 'length': 12, 'errors': 'strict'})
        # wrong first char
        with self.assertRaises(ValueError):
            composant.is_code_hydro(**{'code': 'z3001000', 'errors': 'strict'})
        # wrong last char
        with self.assertRaises(ValueError):
            composant.is_code_hydro(**{'code': 'A333101a', 'errors': 'strict'})
        # wrong chars
        with self.assertRaises(ValueError):
            composant.is_code_hydro(**{'code': 'A33001CC', 'errors': 'strict'})

    def test_errors_02(self):
        """Error handler test."""
        with self.assertRaises(ValueError):
            composant.is_code_hydro('wrong code', errors='houps!')


# -- class TestIsCodeInsee ----------------------------------------------------
class TestIsCodeInsee(unittest.TestCase):

    """Function is_code_insee class tests."""

    def test_bool_true(self):
        """True test."""
        # commune code
        self.assertTrue(composant.is_code_insee('32150', errors='ignore'))
        self.assertTrue(composant.is_code_insee(32150, errors='ignore'))
        self.assertTrue(composant.is_code_insee('02531', errors='strict'))
        self.assertTrue(composant.is_code_insee('2A531', errors='ignore'))
        self.assertTrue(composant.is_code_insee('2A531', errors='strict'))
        self.assertTrue(
            composant.is_code_insee('2B531', length=5, errors='ignore'))
        self.assertTrue(
            composant.is_code_insee('2B531', length=5, errors='strict'))
        # meteo code
        self.assertTrue(
            composant.is_code_insee('032150010', length=9, errors='ignore'))
        self.assertTrue(
            composant.is_code_insee(211503310, length=9, errors='ignore'))
        self.assertTrue(
            composant.is_code_insee('025312113', length=9, errors='strict'))
        self.assertTrue(
            composant.is_code_insee('02A531979', length=9, errors='ignore'))
        self.assertTrue(
            composant.is_code_insee('02B531001', length=9, errors='strict'))

    def test_bool_false(self):
        """False test."""
        # TypeError
        self.assertFalse(composant.is_code_insee([], errors='ignore'))
        # too short
        self.assertFalse(composant.is_code_insee('3310', errors='ignore'))
        self.assertFalse(
            composant.is_code_insee('3310', length=5, errors='ignore'))
        self.assertFalse(
            composant.is_code_insee('03311001', length=9, errors='ignore'))
        # too long
        self.assertFalse(composant.is_code_insee('333051', errors='ignore'))
        self.assertFalse(
            composant.is_code_insee('333051', length=5, errors='ignore'))
        self.assertFalse(
            composant.is_code_insee('0333333333', length=9, errors='ignore'))
        # wrong chars
        self.assertFalse(composant.is_code_insee('3A250', errors='ignore'))
        self.assertFalse(composant.is_code_insee('2C201', errors='ignore'))
        self.assertFalse(
            composant.is_code_insee('02C201001', length=9, errors='ignore'))

    def test_errors_01(self):
        """Error code test."""
        # TypeError (ValueError because code is cast in unicode)
        with self.assertRaises(ValueError):
            composant.is_code_insee(**{'code': [], 'errors': 'strict'})
        # too short
        with self.assertRaises(ValueError):
            composant.is_code_insee(**{'code': '3310', 'errors': 'strict'})
        # too long
        with self.assertRaises(ValueError):
            composant.is_code_insee(**{'code': '233305', 'errors': 'strict'})
        # wrong chars
        with self.assertRaises(ValueError):
            composant.is_code_insee(**{'code': '2D100', 'errors': 'strict'})
        with self.assertRaises(ValueError):
            composant.is_code_insee(**{'code': '2A10W', 'errors': 'strict'})
        # wrong length
        with self.assertRaises(ValueError):
            composant.is_code_insee(
                **{'code': '233305', 'length': -1, 'errors': 'strict'})

    def test_errors_02(self):
        """Error handler test."""
        with self.assertRaises(ValueError):
            composant.is_code_insee('wrong code', errors='houps!')


# -- class TestEqAndNe --------------------------------------------------------
class TestEqAndNe(unittest.TestCase):

    """Special functions __eq__ and __ne__ class tests."""

    def setUp(self):
        """Hook method for setting up the test fixture before exercising it."""
        class Mock(object):

            """A mock class."""

            # we use a list here to have a stronger test but a tuple is
            # better :)
            __all__attrs__ = ['a', 'b', 'c']

            def __init__(self, a, b, c):
                self.a = a
                self.b = b
                self.c = c

            __eq__ = composant.__eq__
            __ne__ = composant.__ne__
        self.Mock = Mock

    def test_base(self):
        """Base test."""
        # with __all__attrs__
        mock = self.Mock(1, 2, 3)
        other = self.Mock(1, 2, 3)
        self.assertEqual(mock, other)
        other = self.Mock(1, 2, 4)
        self.assertNotEqual(mock, other)
        # without __all__attrs__
        del self.Mock.__all__attrs__
        mock = self.Mock(1, 2, 3)
        other = self.Mock(1, 2, 3)
        self.assertEqual(mock, other)
        other = self.Mock(1, 2, 4)
        self.assertNotEqual(mock, other)

    def test_attrs(self):
        """Attrs test."""
        mock = self.Mock(1, 2, 3)
        other = self.Mock(1, 4, 3)
        self.assertTrue(mock.__eq__(other, attrs=['a']))
        self.assertTrue(mock.__eq__(other, attrs=['a', 'c']))
        self.assertTrue(mock.__ne__(other, attrs=['b']))

    def test_ignore(self):
        """Ignore test."""
        mock = self.Mock(1, 2, 3)
        other = self.Mock(1, 4, 5)
        self.assertNotEqual(mock, other)
        self.assertTrue(mock.__eq__(other, ignore=['b', 'c']))
        self.assertTrue(mock.__eq__(other, attrs=['a']))
        self.assertNotEqual(mock, other)
        self.assertEqual(self.Mock.__all__attrs__, ['a', 'b', 'c'])

    def test_lazzy(self):
        """Lazzy test."""
        mock = self.Mock(1, None, 3)
        other = self.Mock(1, 2, None)
        self.assertNotEqual(mock, other)
        self.assertTrue(mock.__eq__(other, lazzy=True))
        self.assertTrue(mock.__eq__(other, attrs=['a']))
        self.assertTrue(mock.__eq__(other, attrs=['c', 'b'], lazzy=True))

    def test_errors(self):
        """Error test."""
        mock = self.Mock(1, 2, 3)
        other = self.Mock(1, 2, 3)
        with self.assertRaises(AttributeError):
            mock.__eq__(other, attrs=['z'])
        with self.assertRaises(AttributeError):
            mock.__eq__(other, ignore=['w'])

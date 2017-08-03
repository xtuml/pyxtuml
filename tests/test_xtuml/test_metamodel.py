# encoding: utf-8
# Copyright (C) 2017 John Törnblom
#
# This file is part of pyxtuml.
#
# pyxtuml is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# pyxtuml is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with pyxtuml. If not, see <http://www.gnu.org/licenses/>.

import unittest

import xtuml
from bridgepoint import ooaofooa
from xtuml import where_eq as where


class TestModel(unittest.TestCase):
    '''
    Test suite for the class xtuml.MetaModel
    '''
    
    @classmethod
    def setUpClass(cls):
        cls.loader = ooaofooa.Loader()
 
    def setUp(self):
        self.metamodel = self.loader.build_metamodel()

    def tearDown(self):
        del self.metamodel

    def test_select_any(self):
        m = self.metamodel
        self.assertNotEqual(m.select_any('S_DT'), None)

    def test_select_one(self):
        m = self.metamodel
        self.assertNotEqual(m.select_one('S_DT'), None)
        
    def test_select_many(self):
        m = self.metamodel
        q = m.select_many('S_DT')
        self.assertIsInstance(q, xtuml.QuerySet)
        self.assertTrue(len(q) > 0)
        
        q = m.select_many('S_EDT')
        self.assertIsInstance(q, xtuml.QuerySet)
        self.assertTrue(len(q) == 0)

    def test_navigate_many_where(self):
        m = self.metamodel
        s_cdt = m.select_many('S_CDT')
        c_dt = xtuml.navigate_many(s_cdt).S_DT[17](where(Name='integer'))
        self.assertEqual(1, len(c_dt))
        
    def test_select_any_where(self):
        m = self.metamodel
        inst = m.select_any('S_DT', where(Name='void'))
        self.assertEqual(inst.Name, 'void')
        
    def test_empty(self):
        m = self.metamodel
        self.assertTrue(len(m.select_many('S_DT', lambda inst: False)) == 0)
        self.assertFalse(len(m.select_many('S_DT')) == 0)
       
    def test_cardinality(self):
        m = self.metamodel
        
        q = m.select_many('S_DT', lambda inst: False)
        self.assertEqual(0, len(q))
        
        q = m.select_many('S_DT')
        self.assertTrue(len(q) > 0)
        
        x = 0
        for _ in q:
            x += 1
            
        self.assertEqual(x, len(q))
        
    def test_is_set(self):
        m = self.metamodel

        q = m.select_many('S_DT', lambda inst: False)
        self.assertIsInstance(q, xtuml.QuerySet)
        
        q = m.select_many('S_DT')
        self.assertIsInstance(q, xtuml.QuerySet)
                
    def test_is_instance(self):
        m = self.metamodel
        
        q = m.select_any('S_DT')
        self.assertIsInstance(q, xtuml.Class)

    def test_query_order(self):
        m = self.metamodel
        q = m.select_many('S_DT')
        
        length = len(q)
        for index, inst in enumerate(q):
            self.assertEqual(index == 0, inst == q.first)
            self.assertEqual(index != 0, inst != q.first)
            self.assertEqual(index == length - 1, inst == q.last)
            self.assertEqual(index != length - 1, inst != q.last)

    def test_case_sensitivity(self):
        self.metamodel.define_class('Aa', [('Id', 'unique_id')])

        self.metamodel.new('AA')

        self.assertTrue(self.metamodel.select_any('aA'))
        self.assertTrue(self.metamodel.select_any('AA'))
        self.assertTrue(self.metamodel.select_any('Aa'))
        self.assertTrue(self.metamodel.select_any('aa'))

        self.metamodel.new('Aa')
        self.metamodel.new('aA')
        self.metamodel.new('aa')
        
        self.assertEqual(len(self.metamodel.select_many('aA')), 4)
        self.assertEqual(len(self.metamodel.select_many('AA')), 4)
        self.assertEqual(len(self.metamodel.select_many('Aa')), 4)
        self.assertEqual(len(self.metamodel.select_many('aa')), 4)
        
        metaclass = self.metamodel.find_metaclass('aa')
        metaclass.append_attribute('Next_Id', 'unique_id')
        
        ass = self.metamodel.define_association(rel_id='R1', 
                                                source_kind='AA', 
                                                source_keys=['ID'], 
                                                source_many=False, 
                                                source_conditional=False,
                                                source_phrase='prev',
                                                target_kind='aa',
                                                target_keys=['next_id'],
                                                target_many=False,
                                                target_conditional=False,
                                                target_phrase='next')
        next_id = None
        for inst in self.metamodel.select_many('aa'):
            inst.next_ID = next_id
            next_id = inst.Id
        
        ass.batch_relate()
        ass.formalize()
            
        self.assertTrue(xtuml.navigate_one(inst).aa[1, 'next'].AA[1, 'next']())
        
    def test_unknown_type(self):
        self.metamodel.define_class('A', [('Id', '<invalid type>')])
        self.assertRaises(xtuml.MetaException, self.metamodel.new, 'A')
        
    def test_undefined_class(self):
        self.assertRaises(xtuml.UnknownClassException, self.metamodel.new, 
                          'MY_UNDEFINED_CLASS')

    def test_redefined_class(self):
        self.metamodel.define_class('MY_CLASS', [])
        self.assertRaises(xtuml.MetaModelException, self.metamodel.define_class, 
                          'MY_CLASS', [])

    def test_select_any_undefined(self):
        self.assertRaises(xtuml.UnknownClassException, self.metamodel.select_any,
                          'MY_CLASS')

    def test_select_many_undefined(self):
        self.assertRaises(xtuml.UnknownClassException, self.metamodel.select_many,
                          'MY_CLASS')
        
    def test_delete(self):
        inst = self.metamodel.select_any('S_DT', where(Name='void'))
        self.assertTrue(xtuml.navigate_one(inst).PE_PE[8001]())
        
        xtuml.delete(inst)
        self.assertFalse(xtuml.navigate_one(inst).PE_PE[8001]())
        
        inst = self.metamodel.select_any('S_DT', where(Name='void'))
        self.assertFalse(inst)
    
    def test_delete_twise(self):
        inst = self.metamodel.select_any('S_DT', where(Name='void'))
        xtuml.delete(inst)
        self.assertRaises(xtuml.DeleteException, xtuml.delete, inst)

    def test_clone(self):
        s_ee = self.metamodel.new('S_EE', Name='Test', Descrip='test', Key_Lett='TEST')
        pe_pe = self.metamodel.new('PE_PE')
        self.assertTrue(xtuml.relate(s_ee, pe_pe, 8001))
        
        m = ooaofooa.empty_model()
        self.assertNotEqual(pe_pe, m.clone(pe_pe))
        self.assertNotEqual(s_ee, m.clone(s_ee))
        
        s_ee_clone = m.select_any('S_EE', where(Name='Test'))
        self.assertNotEqual(s_ee, s_ee_clone)
        self.assertEqual(s_ee_clone.EE_ID, s_ee.EE_ID)
        self.assertEqual(s_ee_clone.Name, s_ee.Name)
        self.assertEqual(s_ee_clone.Descrip, s_ee.Descrip)
        self.assertEqual(s_ee_clone.Key_Lett, s_ee.Key_Lett)
        
        pe_pe_clone = xtuml.navigate_one(s_ee_clone).PE_PE[8001]()
        self.assertTrue(pe_pe_clone)
        self.assertNotEqual(pe_pe, pe_pe_clone)
        self.assertEqual(pe_pe_clone.Element_ID, pe_pe.Element_ID)
        self.assertEqual(pe_pe_clone.Visibility, pe_pe.Visibility)
        self.assertEqual(pe_pe_clone.Package_ID, pe_pe.Package_ID)
        self.assertEqual(pe_pe_clone.Component_ID, pe_pe.Component_ID)
        self.assertEqual(pe_pe_clone.type, pe_pe.type)
    
    def test_delete_unknown_instance(self):
        self.assertRaises(xtuml.DeleteException, xtuml.delete, self)


class TestDefineAssociations(unittest.TestCase):
    '''
    Test suite for the tests the class xtuml.MetaModel ability to define associations.
    '''
 
    def setUp(self):
        self.metamodel = xtuml.MetaModel()

    def tearDown(self):
        del self.metamodel

    def test_reflexive(self):
        self.metamodel.define_class('A', [('Id', 'unique_id'),
                                          ('Next_Id', 'unique_id'),
                                          ('Name', 'string')])
        
        ass = self.metamodel.define_association(rel_id='R1', 
                                                source_kind='A', 
                                                source_keys=['Id'], 
                                                source_many=False, 
                                                source_conditional=False,
                                                source_phrase='prev',
                                                target_kind='A',
                                                target_keys=['Next_Id'],
                                                target_many=False,
                                                target_conditional=False,
                                                target_phrase='next')
        ass.formalize()
        
        first = self.metamodel.new('A', Name="First")
        second = self.metamodel.new('A', Name="Second")

        self.assertTrue(xtuml.relate(first, second, 1, 'prev'))

        inst = xtuml.navigate_one(first).A[1, 'prev']()
        self.assertEqual(inst.Name, second.Name)

        inst = xtuml.navigate_one(first).A[1, 'next']()
        self.assertIsNone(inst)
        
        inst = xtuml.navigate_one(second).A[1, 'next']()
        self.assertEqual(inst.Name, first.Name)
        
        inst = xtuml.navigate_one(second).A[1, 'prev']()
        self.assertIsNone(inst)

    def test_one_to_many(self):
        self.metamodel.define_class('A', [('Id', 'unique_id')])
        self.metamodel.define_class('B', [('Id', 'unique_id'), ('A_Id', 'unique_id')])
        
        ass = self.metamodel.define_association(rel_id=1, 
                                                source_kind='A', 
                                                source_keys=['Id'], 
                                                source_many=False, 
                                                source_conditional=False,
                                                source_phrase='',
                                                target_kind='B',
                                                target_keys=['A_Id'],
                                                target_many=True,
                                                target_conditional=False,
                                                target_phrase='')
        ass.formalize()
        a = self.metamodel.new('A')
        b = self.metamodel.new('B')
        self.assertTrue(xtuml.relate(a, b, 1))
        
        self.assertEqual(a, xtuml.navigate_one(b).A[1]())


class TestClass(unittest.TestCase):
    '''
    Test suite for the class xtuml.Class
    '''
    My_Class = xtuml.MetaClass('My_Class')

    def test_plus_operator(self):
        inst1 = self.My_Class()
        inst2 = self.My_Class()

        q = inst1 + inst2
        self.assertEqual(2, len(q))
        self.assertIn(inst1, q)
        self.assertIn(inst2, q)
        
    def test_minus_operator(self):
        inst1 = self.My_Class()
        inst2 = self.My_Class()

        q = inst1 - inst2
        self.assertEqual(1, len(q))
        self.assertIn(inst1, q)
        self.assertNotIn(inst2, q)
        
    def test_non_persisting_attribute(self):
        inst = self.My_Class()
        
        setattr(inst, 'test1', 1)
        self.assertEqual(getattr(inst, 'test1'), 1)
        self.assertEqual(inst.test1, 1)
        
        inst.__dict__['test2'] = 2
        self.assertEqual(getattr(inst, 'test2'), 2)
        self.assertEqual(inst.test2, 2)

        inst.test3 = 3
        self.assertEqual(getattr(inst, 'test3'), 3)
        self.assertEqual(inst.test3, 3)
        
    def test_gettattr_with_undefined_attribute(self):
        inst = self.My_Class()
        self.assertRaises(AttributeError, getattr, inst, 'test')
        
    def test_undefined_attribute_access(self):
        inst = self.My_Class()
        try:
            _ = inst.test
            self.fail('AttributeError expected')
        except AttributeError:
            pass


class TestMetaClass(unittest.TestCase):
    '''
    Test suite for xtuml.MetaClass
    '''
    
    def setUp(self):
        self.metaclass = xtuml.MetaClass('Test')
        
    def test_default_value(self):
        self.assertEqual(self.metaclass.default_value('integer'), 0)
        self.assertEqual(self.metaclass.default_value('Integer'), 0)
        self.assertEqual(self.metaclass.default_value('real'), 0.0)
        self.assertEqual(self.metaclass.default_value('STRING'), '')
        self.assertEqual(self.metaclass.default_value('unique_id'), None)
        self.assertEqual(self.metaclass.default_value('boolean'), False)
    
    def test_modifying_attributes(self):
        self.metaclass.append_attribute('number', 'integer')
        self.metaclass.append_attribute('name', 'string')
        self.metaclass.insert_attribute(1, 'email', 'string')
    
        inst1 = self.metaclass(number=2, name='test', email='test@test.com')
        self.assertEqual(inst1.number, 2)
        self.assertEqual(inst1.name, 'test')
        self.assertEqual(inst1.email, 'test@test.com')
    
        for expected_name, name in zip(['number', 'email', 'name'], 
                                       self.metaclass.attribute_names):
            self.assertEqual(expected_name, name)
    
        self.metaclass.delete_attribute('name')
        self.assertNotIn('name', self.metaclass.attribute_names)
        
        self.assertEqual(inst1.number, 2)
        self.assertEqual(inst1.name, 'test')
        
        
class TestQuerySet(unittest.TestCase):
    '''
    Test suite for the class xtuml.QuerySet
    '''
    def test_first(self):
        q = xtuml.QuerySet([1, 2, 3])
        self.assertEqual(q.first, 1)
        
        q = xtuml.QuerySet()
        self.assertIsNone(q.first)
        
    def test_last(self):
        q = xtuml.QuerySet([1, 2, 3])
        self.assertEqual(q.last, 3)
        
        q = xtuml.QuerySet()
        self.assertIsNone(q.last)
        
    def test_one_item(self):
        q = xtuml.QuerySet([2])
        self.assertEqual(q.first, 2)
        self.assertEqual(q.last, 2)
        
        
if __name__ == "__main__":
    unittest.main()


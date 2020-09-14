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

from xtuml import relate
from xtuml import navigate_one as one


class TestAssocClass(unittest.TestCase):
    '''
    CREATE TABLE Assoc (
        one_side_ID UNIQUE_ID,
        other_side_ID UNIQUE_ID
    );

    CREATE TABLE Class (
        ID UNIQUE_ID
    );

    CREATE ROP REF_ID R1
        FROM MC Assoc (one_side_ID) PHRASE 'one'
        TO 1 Class (ID) PHRASE 'other';

    CREATE ROP REF_ID R1
        FROM MC Assoc (other_side_ID) PHRASE 'other'
        TO 1 Class (ID) PHRASE 'one';
    '''

    def setUp(self):
        l = xtuml.ModelLoader()
        l.input(self.__class__.__doc__)
        self.m = l.build_metamodel()
        
    def tearDown(self):
        del self.m

    def test_serialize(self):
        s1 = xtuml.serialize(self.m)
        l = xtuml.ModelLoader()
        l.input(s1)
        s2 = xtuml.serialize(l.build_metamodel())
        self.assertEqual(s1, s2)
        
    def test_relate_assoc_to_class_across_one(self):
        cls = self.m.new('Class')
        assoc = self.m.new('Assoc')

        self.assertTrue(relate(assoc, cls, 1, 'one'))
        self.assertEqual(assoc.one_side_ID, cls.ID)

    def test_relate_assoc_to_class_across_other(self):
        cls = self.m.new('Class')
        assoc = self.m.new('Assoc')

        self.assertTrue(relate(assoc, cls, 1, 'other'))
        self.assertEqual(assoc.other_side_ID, cls.ID)
    
    def test_relate_class_to_assoc_across_one(self):
        cls = self.m.new('Class')
        assoc = self.m.new('Assoc')

        self.assertTrue(relate(cls, assoc, 1, 'one'))
        self.assertEqual(assoc.other_side_ID, cls.ID)

    def test_relate_class_to_assoc_across_other(self):
        cls = self.m.new('Class')
        assoc = self.m.new('Assoc')

        self.assertTrue(relate(cls, assoc, 1, 'other'))
        self.assertEqual(assoc.one_side_ID, cls.ID)

    def test_navigate_assoc_to_class_across_one(self):
        cls = self.m.new('Class')
        assoc = self.m.new('Assoc', other_side_ID=cls.ID)
        self.assertTrue(one(assoc).Class[1, 'one']())

    def test_navigate_assoc_to_class_across_other(self):
        cls = self.m.new('Class')
        assoc = self.m.new('Assoc', one_side_ID=cls.ID)
        self.assertTrue(one(assoc).Class[1, 'other']())

    def test_navigate_class_to_assoc_across_one(self):
        cls = self.m.new('Class')
        assoc = self.m.new('Assoc', one_side_ID=cls.ID)
        self.assertTrue(one(cls).Assoc[1, 'one']())
    
    def test_navigate_class_to_assoc_across_other(self):
        cls = self.m.new('Class')
        assoc = self.m.new('Assoc', other_side_ID=cls.ID)
        self.assertTrue(one(cls).Assoc[1, 'other']())

    def test_relate_two_classes_to_assoc(self):
        cls1 = self.m.new('Class')
        cls2 = self.m.new('Class')
        assoc = self.m.new('Assoc')

        self.assertTrue(relate(cls1, assoc, 1, 'one'))
        self.assertTrue(relate(cls2, assoc, 1, 'other'))

    def test_relate_assoc_to_two_classes(self):
        cls1 = self.m.new('Class')
        cls2 = self.m.new('Class')
        assoc = self.m.new('Assoc')

        self.assertTrue(relate(assoc, cls1, 1, 'one'))
        self.assertTrue(relate(assoc, cls2, 1, 'other'))
        
        self.assertTrue(one(cls1).Class[1, 'other']())
        self.assertFalse(one(cls2).Class[1, 'other']())
        
        self.assertFalse(one(cls1).Class[1, 'one']())
        self.assertTrue(one(cls2).Class[1, 'one']())

    def test_relate_assoc_to_two_classes_incorrectly(self):
        cls1 = self.m.new('Class')
        cls2 = self.m.new('Class')
        assoc = self.m.new('Assoc')

        self.assertTrue(relate(assoc, cls1, 1, 'one'))
        self.assertRaises(xtuml.RelateException, relate,
                          assoc, cls2, 1, 'one')


class TestReflexiveClass(unittest.TestCase):
    '''
    CREATE TABLE Reflexive (
        ID UNIQUE_ID,
        Ref_ID UNIQUE_ID
    );

    CREATE ROP REF_ID R1
        FROM 1C Reflexive (Ref_ID) PHRASE 'one'
        TO 1C Reflexive (ID) PHRASE 'other';
    '''

    def setUp(self):
        l = xtuml.ModelLoader()
        l.input(self.__class__.__doc__)
        self.m = l.build_metamodel()
        
    def tearDown(self):
        del self.m

    def test_serialize(self):
        s1 = xtuml.serialize(self.m)
        l = xtuml.ModelLoader()
        l.input(s1)
        s2 = xtuml.serialize(l.build_metamodel())
        self.assertTrue(s1 == s2)

    def test_relate_across_one(self):
        cls1 = self.m.new('Reflexive')
        cls2 = self.m.new('Reflexive')

        self.assertTrue(relate(cls1, cls2, 1, 'one'))
        self.assertEqual(cls1.Ref_ID, cls2.ID)

    def test_relate_across_other(self):
        cls1 = self.m.new('Reflexive')
        cls2 = self.m.new('Reflexive')

        self.assertTrue(relate(cls1, cls2, 1, 'other'))
        self.assertEqual(cls2.Ref_ID, cls1.ID)

    def test_navgate_across_one(self):
        cls1 = self.m.new('Reflexive')
        cls2 = self.m.new('Reflexive', Ref_ID=cls1.ID)

        self.assertEqual(one(cls1).Reflexive[1, 'one'](), cls2)
        self.assertFalse(one(cls2).Reflexive[1, 'one']())

    def test_navgate_across_other(self):
        cls1 = self.m.new('Reflexive')
        cls2 = self.m.new('Reflexive', Ref_ID=cls1.ID)

        self.assertEqual(one(cls2).Reflexive[1, 'other'](), cls1)
        self.assertFalse(one(cls1).Reflexive[1, 'other']())

        
if __name__ == "__main__":
    unittest.main()



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
import os
import tempfile
import atexit

import xtuml
    

class TestPersist(unittest.TestCase):
    '''
    Test suite for the module xtuml.persist
    '''

    def test_serialize(self):
        schema = '''
            CREATE TABLE X (BOOLEAN BOOLEAN,
                            INTEGER INTEGER,
                            REAL REAL,
                            STRING STRING,
                            UNIQUE_ID UNIQUE_ID);
        '''
        
        loader = xtuml.ModelLoader()
        loader.input(schema)
        
        m = loader.build_metamodel()
        m.new('X', BOOLEAN=True,
                   INTEGER=1,
                   REAL=-5.5,
                   UNIQUE_ID=1)
        
        s = xtuml.serialize_instances(m)
        
        loader = xtuml.ModelLoader()
        loader.input(schema)
        loader.input(s)
        
        m = loader.build_metamodel()
        x = m.select_any('X')
        self.assertEqual(x.BOOLEAN, True)
        self.assertEqual(x.INTEGER, 1)
        self.assertEqual(x.REAL, -5.5)
        self.assertEqual(x.UNIQUE_ID, 1)
        
        self.assertIsInstance(x.BOOLEAN, bool)
        self.assertIsInstance(x.INTEGER, int)
        self.assertIsInstance(x.REAL, float)
        
        # don't check type of unique_ids. they may differ.
        # python2 uses long, while python3 uses int.
        # besides, only equals comparisons operator (==) shall be used on these types.
        # self.assertIsInstance(x.UNIQUE_ID, int)
        
    def test_serialize_default_values(self):
        schema = '''
            CREATE TABLE X (BOOLEAN BOOLEAN,
                            INTEGER INTEGER,
                            REAL REAL,
                            STRING STRING,
                            UNIQUE_ID UNIQUE_ID);
        '''
        
        loader = xtuml.ModelLoader()
        loader.input(schema)

        id_generator = xtuml.IntegerGenerator()
        m = loader.build_metamodel(id_generator)
        m.new('X')
        
        s = xtuml.serialize_instances(m)
  
        loader = xtuml.ModelLoader()
        loader.input(schema)
        loader.input(s)

        id_generator = xtuml.IntegerGenerator()
        m = loader.build_metamodel(id_generator)
        x = m.select_any('X')
        self.assertEqual(x.BOOLEAN, False)
        self.assertEqual(x.INTEGER, 0)
        self.assertEqual(x.REAL, 0.0)
        self.assertEqual(x.UNIQUE_ID, 1)


    def test_persist_default_values(self):
        schema = '''
            CREATE TABLE X (BOOLEAN BOOLEAN,
                            INTEGER INTEGER,
                            REAL REAL,
                            STRING STRING,
                            UNIQUE_ID UNIQUE_ID);
        '''
        
        loader = xtuml.ModelLoader()
        loader.input(schema)
        
        id_generator = xtuml.IntegerGenerator()
        m = loader.build_metamodel(id_generator)
        m.new('X')
        
        s = xtuml.serialize_instances(m)
        
        (_, filename) = tempfile.mkstemp()
        try:
            xtuml.persist_instances(m, filename)
            with open(filename) as f:
                self.assertEqual(s, f.read())
        finally:
            atexit.register(os.remove, filename)
        
        loader = xtuml.ModelLoader()
        loader.input(schema)
        loader.input(s)

        id_generator = xtuml.IntegerGenerator()
        m = loader.build_metamodel(id_generator)
        x = m.select_any('X')
        self.assertEqual(x.BOOLEAN, False)
        self.assertEqual(x.INTEGER, 0)
        self.assertEqual(x.REAL, 0.0)
        self.assertEqual(x.UNIQUE_ID, 1)

    def test_persist_schema(self):
        schema = '''
            CREATE TABLE X (BOOLEAN BOOLEAN,
                            INTEGER INTEGER,
                            REAL REAL,
                            STRING STRING,
                            UNIQUE_ID UNIQUE_ID,
                            Next UNIQUE_ID);
                            
        CREATE ROP REF_ID R1 FROM 1C X ( UNIQUE_ID ) PHRASE 'precedes'
                             TO   1C X ( Next ) PHRASE 'succeeds';
        '''
        loader = xtuml.ModelLoader()
        loader.input(schema)
        m = loader.build_metamodel()
        s = xtuml.serialize_schema(m)
    
        (_, filename) = tempfile.mkstemp()
        try:
            xtuml.persist_schema(m, filename)
            with open(filename) as f:
                self.assertEqual(s, f.read())
        finally:
            atexit.register(os.remove, filename)

    def test_persist_database(self):
        schema = '''
            CREATE TABLE X (BOOLEAN BOOLEAN,
                            INTEGER INTEGER,
                            REAL REAL,
                            STRING STRING,
                            UNIQUE_ID UNIQUE_ID,
                            Next UNIQUE_ID);
                            
        CREATE ROP REF_ID R1 FROM 1C X ( Next ) PHRASE 'precedes'
                             TO   1C X ( UNIQUE_ID ) PHRASE 'succeeds';
        '''
        loader = xtuml.ModelLoader()
        loader.input(schema)
        m = loader.build_metamodel()
        m.new('X', Boolean=True, Integer=4, String='str', Uniquie_Id=5)
        
        s = xtuml.serialize(m)
    
        (_, filename) = tempfile.mkstemp()
        try:
            xtuml.persist_database(m, filename)
            with open(filename) as f:
                self.assertEqual(s, f.read())
        finally:
            atexit.register(os.remove, filename)

    def test_serialize_schema(self):
        schema = '''
            CREATE TABLE X (BOOLEAN BOOLEAN,
                            INTEGER INTEGER,
                            REAL REAL,
                            STRING STRING,
                            UNIQUE_ID UNIQUE_ID,
                            Next UNIQUE_ID);
                            
        CREATE ROP REF_ID R1 FROM 1C X ( Next ) PHRASE 'precedes'
                             TO   1C X ( UNIQUE_ID ) PHRASE 'succeeds';
        '''
        loader = xtuml.ModelLoader()
        loader.input(schema)
        m = loader.build_metamodel()
        x1 = m.new('X', Boolean=True, Integer=4, String='str')
        x2 = m.new('X', Boolean=True, Integer=4, String='str')
        xtuml.relate(x1, x2, 1, 'precedes')
        
        s = xtuml.serialize_schema(m)
        loader = xtuml.ModelLoader()
        loader.input(s)
        m = loader.build_metamodel()

        self.assertFalse(m.select_any('X'))

        x1 = m.new('X', Boolean=True, Integer=4, String='str')
        x2 = m.new('X', Boolean=True, Integer=4, String='str')
        xtuml.relate(x1, x2, 1, 'succeeds')

        self.assertTrue(xtuml.navigate_one(x1).X[1, 'succeeds']())

    def test_serialize_unique_identifiers(self):
        schema = '''
        CREATE TABLE X (s1 STRING, s2 STRING);
        CREATE UNIQUE INDEX I1 ON X (s1, s2);
        '''
        
        loader = xtuml.ModelLoader()
        loader.input(schema)
        m = loader.build_metamodel()
        
        s = xtuml.serialize_schema(m)
        s += xtuml.serialize_unique_identifiers(m)
        
        loader = xtuml.ModelLoader()
        loader.input(s)
        m = loader.build_metamodel()

        x1 = m.new('X', s1='s1', s2='s2')
        x2 = m.new('X', s1='s1', s2='s2')

        self.assertFalse(m.is_consistent())
        x2.s2 = 'S2'
        self.assertTrue(m.is_consistent())
        
    def test_serialize_none_values(self):
        schema = '''
            CREATE TABLE X (BOOLEAN BOOLEAN,
                            INTEGER INTEGER,
                            REAL REAL,
                            STRING STRING,
                            UNIQUE_ID UNIQUE_ID);
        '''
        loader = xtuml.ModelLoader()
        loader.input(schema)

        id_generator = xtuml.IntegerGenerator()
        m = loader.build_metamodel(id_generator)
        x = m.new('X')
        x.boolean = None
        x.Integer = None
        x.ReaL = None
        x.UNIQUE_ID = None
        s = xtuml.serialize_instances(m)

        loader = xtuml.ModelLoader()
        loader.input(schema)
        loader.input(s)

        id_generator = xtuml.IntegerGenerator()
        m = loader.build_metamodel(id_generator)
        x = m.select_any('X')
        self.assertEqual(x.BOOLEAN, False)
        self.assertEqual(x.INTEGER, 0)
        self.assertEqual(x.REAL, 0.0)
        self.assertEqual(x.UNIQUE_ID, 0)

    def test_serialize_attribute_named_self(self):
        schema = '''
            CREATE TABLE X (self UNIQUE_ID);
        '''
        
        loader = xtuml.ModelLoader()
        loader.input(schema)
        
        m = loader.build_metamodel()
        m.new('X', 1)
        
        s = xtuml.serialize_instances(m)
        
        loader = xtuml.ModelLoader()
        loader.input(schema)
        loader.input(s)
        
        m = loader.build_metamodel()
        x = m.select_any('X')
        self.assertEqual(x.self, 1)

    def test_serialize_undefined_table(self):
        schema = '''
        CREATE TABLE X (
          _0 UNIQUE_ID,
          _1 STRING,
          _2 STRING,
          _3 INTEGER,
          _4 INTEGER,
          _5 BOOLEAN,
          _6 BOOLEAN,
          _7 INTEGER,
          _8 REAL,
          _9 REAL
        );
        '''
        
        instances = '''
            INSERT INTO X VALUES (
              "00000000-0000-0000-0000-000000000000",
              'TE''ST',
              'test',
              1,
              0,
              false,
              true,
              -5,
              1.543,
              -0.543
            );
        '''
        loader = xtuml.ModelLoader()
        loader.input(instances)
        m = loader.build_metamodel()
        
        s1 = xtuml.serialize_database(m)
        
        loader = xtuml.ModelLoader()
        loader.input(schema)
        loader.input(instances)
        m = loader.build_metamodel()

        s2 = xtuml.serialize_database(m)
        
        self.assertEqual(s1, s2)

    def test_implicit_serialize(self):
        schema = '''
            CREATE TABLE X (BOOLEAN BOOLEAN,
                            INTEGER INTEGER,
                            REAL REAL,
                            STRING STRING,
                            UNIQUE_ID UNIQUE_ID,
                            Next UNIQUE_ID);
                            
        CREATE ROP REF_ID R1 FROM 1C X ( Next ) PHRASE 'precedes'
                             TO   1C X ( UNIQUE_ID ) PHRASE 'succeeds';
        '''
        loader = xtuml.ModelLoader()
        loader.input(schema)
        m = loader.build_metamodel()
        
        X = m.find_class('X')
        s1 = xtuml.serialize(X)
        s2 = xtuml.serialize_class(X)
        self.assertTrue(s1)
        self.assertEqual(s1, s2)
        
        R1 = m.associations[0]
        s1 = xtuml.serialize(R1)
        s2 = xtuml.serialize_association(R1)
        self.assertTrue(s1)
        self.assertEqual(s1, s2)

        x = m.new('X', Boolean=True, Integer=4, String='str')
        
        s1 = xtuml.serialize(x)
        s2 = xtuml.serialize_instance(x)
        self.assertTrue(s1)
        self.assertEqual(s1, s2)
        
        s1 = xtuml.serialize(m)
        s2 = xtuml.serialize_database(m)
        self.assertTrue(s1)
        self.assertEqual(s1, s2)
        
        
def compare_metamodel_classes(m1, m2):
    '''
    Helper function for detecting differences in class definitions 
    in two metamodels.
    '''
    if len(m1.metaclasses.keys()) != len(m2.metaclasses.keys()):
        return False
    
    for kind in m1.metaclasses.keys():
        metaclass1 = m1.metaclasses[kind]
        metaclass2 = m2.metaclasses[kind]
        
        if metaclass1.kind != metaclass2.kind:
            return False
        
        if metaclass1.attributes != metaclass2.attributes:
            return False

        if metaclass1.identifying_attributes != metaclass2.identifying_attributes:
            return False

        if metaclass1.referential_attributes != metaclass2.referential_attributes:
            return False

        if metaclass1.indices != metaclass2.indices:
            return False
        
    return True


def schema_compare(fn):
    '''
    Decorator for testing schema serialization capabilities 
    from stimuli defined as doc-strings on unit tests.
    '''
    def compare_wrapper(self, *args, **kwargs):
        loader = xtuml.ModelLoader()
        loader.input(fn.__doc__)
        m1 = loader.build_metamodel()
        
        s = xtuml.serialize_schema(m1)

        loader = xtuml.ModelLoader()
        loader.input(s)
        m2 = loader.build_metamodel()
        
        self.assertTrue(compare_metamodel_classes(m1, m2))
        fn(self)
    
    return compare_wrapper


class TestSchema(unittest.TestCase):
    '''
    Test suite for schema serialization capabilities in 
    the module xtuml.persist
    '''
    
    @schema_compare
    def test_class_with_data_type_names(self):
        '''
            CREATE TABLE X (BOOLEAN BOOLEAN,
                            INTEGER INTEGER,
                            REAL REAL,
                            STRING STRING,
                            UNIQUE_ID UNIQUE_ID);
        '''
        
    @schema_compare
    def test_rop_named_as_cardinality(self):
        '''
        CREATE TABLE M  (Id INTEGER, MC_Id INTEGER);
        CREATE TABLE MC (Id INTEGER);
        
        CREATE ROP REF_ID R1 FROM M M ( MC_Id )
                             TO   1 MC ( Id );
        '''

    @schema_compare
    def test_rop_without_identifiers(self):
        '''
        CREATE TABLE X ();
        CREATE TABLE Y ();
        
        CREATE ROP REF_ID R1 FROM MC X ()
                             TO   MC Y ();
        '''

if __name__ == "__main__":
    unittest.main()


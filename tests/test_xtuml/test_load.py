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

import xtuml


def load_docstring(fn):
    '''
    Decorator for loading a meta model from a test case doc string
    '''
    def load_wrapper(self, *args, **kwargs):
        try:
            loader = xtuml.ModelLoader()
            loader.input(fn.__doc__)
            res = loader.build_metamodel()
        except Exception as ex:
            res = ex
            
        fn(self, res)
            
    return load_wrapper


class TestLoader(unittest.TestCase):
    '''
    Test suite for loading serialized models
    '''

    def test_filename_input(self):
        resources = os.path.dirname(__file__) + os.sep + '..' + os.sep + 'resources'
        schema = resources + os.sep + 'ooaofooa_schema.sql'
        globs = resources + os.sep + 'Globals.xtuml'

        metamodel = xtuml.load_metamodel([globs, schema])
        self.assertTrue(metamodel.select_any('S_DT', xtuml.where_eq(Name='integer')) is not None)
        
    @load_docstring
    def test_table_named_create(self, m):
        '''
        CREATE TABLE CREATE (Id UNIQUE_ID);
        INSERT INTO CREATE VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('CREATE') is not None)
        
    @load_docstring
    def test_table_named_table(self, m):
        '''
        CREATE TABLE TABLE (Id UNIQUE_ID);
        INSERT INTO TABLE VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('TABLE') is not None)
        
    @load_docstring
    def test_table_named_insert(self, m):
        '''
        CREATE TABLE INSERT (Id UNIQUE_ID);
        INSERT INTO INSERT VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('INSERT') is not None)
        
    @load_docstring
    def test_table_named_into(self, m):
        '''
        CREATE TABLE INTO (Id UNIQUE_ID);
        INSERT INTO INTO VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('INTO') is not None)
        
    @load_docstring
    def test_table_named_values(self, m):
        '''
        CREATE TABLE VALUES (Id UNIQUE_ID);
        INSERT INTO VALUES VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('VALUES') is not None)
        
    @load_docstring
    def test_table_named_rop(self, m):
        '''
        CREATE TABLE ROP (Id UNIQUE_ID);
        INSERT INTO ROP VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('ROP') is not None)
        
    @load_docstring
    def test_table_named_ref_id(self, m):
        '''
        CREATE TABLE REF_ID (Id UNIQUE_ID);
        INSERT INTO REF_ID VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('REF_ID') is not None)
        
    @load_docstring
    def test_table_named_from(self, m):
        '''
        CREATE TABLE FROM (Id UNIQUE_ID);
        INSERT INTO FROM VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('FROM') is not None)
        
    @load_docstring
    def test_table_named_to(self, m):
        '''
        CREATE TABLE TO (Id UNIQUE_ID);
        INSERT INTO TO VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('TO') is not None)
        
    @load_docstring
    def test_table_named_phrase(self, m):
        '''
        CREATE TABLE PHRASE (Id UNIQUE_ID);
        INSERT INTO PHRASE VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('PHRASE') is not None)
        
    @load_docstring
    def test_table_named_true(self, m):
        '''
        CREATE TABLE TRUE (Id UNIQUE_ID);
        INSERT INTO TRUE VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('TRUE') is not None)
        
    @load_docstring
    def test_table_named_false(self, m):
        '''
        CREATE TABLE FALSE (Id UNIQUE_ID);
        INSERT INTO FALSE VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        self.assertTrue(m.select_any('FALSE') is not None)
        
    @load_docstring
    def test_empty_attribute_sequence(self, m):
        '''
        CREATE TABLE X ();
        INSERT INTO X VALUES ();
        '''
        self.assertTrue(m.select_any('X') is not None)

    @load_docstring
    def test_insert_string(self, m):
        '''
        CREATE TABLE X (Id STRING);
        INSERT INTO X VALUES ('TEST');
        '''
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, 'TEST')
        
    @load_docstring
    def test_insert_escaped_string(self, m):
        '''
        CREATE TABLE X (Id STRING);
        INSERT INTO X VALUES ('TE''ST');
        '''
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, "TE'ST")

    @load_docstring
    def test_insert_escaped_single_quot(self, m):
        """
        CREATE TABLE X (Id STRING);
        INSERT INTO X VALUES ('''');
        """
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, "'")
        
    @load_docstring
    def test_insert_escaped_string_beginning(self, m):
        """
        CREATE TABLE X (Id STRING);
        INSERT INTO X VALUES ('''TEST');
        """
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, "'TEST")

    @load_docstring
    def test_insert_escaped_string_end(self, m):
        """
        CREATE TABLE X (Id STRING);
        INSERT INTO X VALUES ('TEST''');
        """
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, "TEST'")
        
    @load_docstring
    def test_insert_null_uuid(self, m):
        '''
        CREATE TABLE X (Id UNIQUE_ID);
        INSERT INTO X VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(0, val.Id)

    @load_docstring
    def test_insert_zero_uuid(self, m):
        '''
        CREATE TABLE X (Id UNIQUE_ID);
        INSERT INTO X VALUES (0);
        '''
        val = m.select_any('X')
        self.assertEqual(0, val.Id)

    @load_docstring
    def test_insert_integer_as_uuid(self, m):
        '''
        CREATE TABLE X (Id INTEGER);
        INSERT INTO X VALUES ("00000000-0000-0000-0000-000000000000");
        '''
        val = m.select_any('X')
        self.assertEqual(0, val.Id)

    @load_docstring
    def test_insert_positive_real(self, m):
        '''
        CREATE TABLE X (Id REAL);
        INSERT INTO X VALUES (1.1);
        '''
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, 1.1)
        
    @load_docstring
    def test_insert_negative_real(self, m):
        '''
        CREATE TABLE X (Id REAL);
        INSERT INTO X VALUES (-5.2);
        '''
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, -5.2)

    @load_docstring
    def test_insert_positive_integer(self, m):
        '''
        CREATE TABLE X (Id INTEGER);
        INSERT INTO X VALUES (5);
        '''
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, 5)

    @load_docstring
    def test_insert_negative_integer(self, m):
        '''
        CREATE TABLE X (Id INTEGER);
        INSERT INTO X VALUES (-1000);
        '''
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, -1000) 

    @load_docstring
    def test_insert_true(self, m):
        '''
        CREATE TABLE X (Id BOOLEAN);
        INSERT INTO X VALUES (true);
        '''
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, True)
        
    @load_docstring
    def test_insert_false(self, m):
        '''
        CREATE TABLE X (Id BOOLEAN);
        INSERT INTO X VALUES (false);
        '''
        val = m.select_any('X')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, False)
        
    @load_docstring
    def test_rop_named_as_cardinality(self, m):
        '''
        CREATE TABLE M  (Id INTEGER, MC_Id INTEGER);
        CREATE TABLE MC (Id INTEGER);
        
        CREATE ROP REF_ID R1 FROM M M ( MC_Id )
                             TO   1 MC ( Id );
                             
        INSERT INTO MC VALUES (2);
        INSERT INTO M  VALUES (1, 2);
        '''
        val = m.select_any('M')
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, 1) 
        
        val = xtuml.navigate_one(val).MC[1]()
        self.assertTrue(val is not None)
        self.assertEqual(val.Id, 2) 

    @load_docstring
    def test_rop_without_identifier_sequence(self, m):
        '''
        CREATE TABLE X  ();
        CREATE TABLE Y ();
        
        CREATE ROP REF_ID R1 FROM MC X ()
                             TO   MC Y ();
                             
        INSERT INTO X VALUES ();
        INSERT INTO Y VALUES ();
        '''
        x = m.select_any('X')
        self.assertTrue(x is not None)

        y = xtuml.navigate_one(x).Y[1]()
        self.assertTrue(y is not None)

    @load_docstring
    def test_empty_input(self, m):
        ''''''
        pass
    
    @load_docstring
    def test_empty_input_with_comment(self, m):
        '''-- Some comment'''
        pass
        
    @load_docstring
    def test_illegal_character(self, m):
        '''
        CREATE TABLE & (Id INTEGER);
        '''
        self.assertIsInstance(m, xtuml.ParsingException)
        
    @load_docstring
    def test_missing_semicolon(self, m):
        '''
        CREATE TABLE X (Id INTEGER)
        '''
        self.assertIsInstance(m, xtuml.ParsingException)
        
    @load_docstring
    def test_invalid_token_sequence(self, m):
        '''
        TABLE CREATE X (Id INTEGER);
        '''
        self.assertIsInstance(m, xtuml.ParsingException)
        
    @load_docstring
    def test_invalid_first_cardinality_number(self, m):
        '''
        CREATE ROP REF_ID R1 FROM 2 X ( Id )
                             TO   1 Y ( Id );
        '''
        self.assertIsInstance(m, xtuml.ParsingException)
        
    @load_docstring
    def test_invalid_second_cardinality_number(self, m):
        '''
        CREATE ROP REF_ID R1 FROM 1 X ( Id )
                             TO   2 Y ( Id );
        '''
        self.assertIsInstance(m, xtuml.ParsingException)
        
    @load_docstring
    def test_invalid_first_cardinality_letter(self, m):
        '''
        CREATE ROP REF_ID R1 FROM 1 X ( Id )
                             TO   X Y ( Id );
        '''
        self.assertIsInstance(m, xtuml.ParsingException)
        
    @load_docstring
    def test_invalid_second_cardinality_letter(self, m):
        '''
        CREATE ROP REF_ID R1 FROM Y X ( Id )
                             TO   1 Y ( Id );
        '''
        self.assertIsInstance(m, xtuml.ParsingException)
        
    @load_docstring
    def test_invalid_boolean_literal(self, m):
        '''
        CREATE TABLE X (B BOOLEAN);
        INSERT INTO X VALUES ('test');
        '''
        self.assertIsInstance(m, xtuml.ParsingException)

    @load_docstring
    def test_invalid_type(self, m):
        '''
        CREATE TABLE X (VAR SOME_TYPE);
        INSERT INTO X VALUES ('test');
        '''
        self.assertIsInstance(m, xtuml.MetaException)

    @load_docstring
    def test_insert_with_undefined_table_and_argument(self, m):
        '''
        INSERT INTO X VALUES ('test');
        '''
        self.assertTrue(m.select_any('X'))
        
    @load_docstring
    def test_insert_with_undefined_table(self, m):
        '''
        INSERT INTO X VALUES ();
        '''
        self.assertTrue(m.select_any('X'))
    
    @load_docstring
    def test_insert_with_undefined_argument(self, m):
        '''
        CREATE TABLE X (VAR STRING);
        INSERT INTO X VALUES ('test', 1);
        '''
        self.assertTrue(m.select_any('X'))
        
    @load_docstring
    def test_insert_with_missing_argument(self, m):
        '''
        CREATE TABLE X (VAR STRING);
        INSERT INTO X VALUES ();
        '''
        self.assertTrue(m.select_any('X'))

    @load_docstring
    def test_insert_named_values(self, m):
        '''
        CREATE TABLE X (VAR1 STRING, VAR2 BOOLEAN, VAR3 INTEGER);
        INSERT INTO X (VAR2, VAR3, VAR1) VALUES (TRUE, 5, 'test');
        '''
        x = m.select_any('X')
        self.assertTrue(x)
        self.assertEqual(x.VAR1, 'test')
        self.assertEqual(x.VAR2, True)
        self.assertEqual(x.VAR3, 5)

    @load_docstring
    def test_insert_incomplete_named_values(self, m):
        '''
        CREATE TABLE X (VAR1 STRING, VAR2 BOOLEAN, VAR3 INTEGER);
        INSERT INTO X (VAR2, VAR1) VALUES (TRUE, 'test');
        '''
        x = m.select_any('X')
        self.assertTrue(x)
        self.assertEqual(x.VAR1, 'test')
        self.assertEqual(x.VAR2, True)
        self.assertTrue(x.VAR3 is None)

    @load_docstring
    def test_insert_value_named_self(self, m):
        '''
        CREATE TABLE X (self STRING);
        INSERT INTO X (self) VALUES ('test');
        '''
        x = m.select_any('X')
        self.assertTrue(x)
        self.assertEqual(x.self, 'test')

    @load_docstring
    def test_insert_unknown_named_values(self, m):
        '''
        INSERT INTO X (VAR2, VAR1) VALUES (TRUE, 'test');
        '''
        x = m.select_any('X')
        self.assertTrue(x)
        self.assertEqual(x.VAR1, 'test')
        self.assertEqual(x.VAR2, True)


if __name__ == "__main__":
    unittest.main()


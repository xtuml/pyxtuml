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

'''
Loading support for xtUML models (based on sql).
'''

import uuid
import logging
import os
import re

from ply import lex
from ply import yacc

import xtuml


logger = logging.getLogger(__name__)


def guess_type_name(value):
    '''
    Guess the type name of a serialized value.
    '''
    value = str(value)
    
    if value.upper() in ['TRUE', 'FALSE']:
        return 'BOOLEAN'
    
    elif re.match(r'(-)?(\d+)(\.\d+)', value):
        return 'REAL'
    
    elif re.match(r'(-)?(\d+)', value):
        return 'INTEGER'
    
    elif re.match(r'\'((\'\')|[^\'])*\'', value):
        return 'STRING'
    
    elif re.match(r'\"([^\\\n]|(\\.))*?\"', value):
        return 'UNIQUE_ID'


def deserialize_value(ty, value):
    '''
    Deserialize a value of some type
    '''
    uty = ty.upper()
    
    if uty == 'BOOLEAN':
        if value.isdigit():
            return bool(int(value))
        elif value.upper() == 'FALSE':
            return False
        elif value.upper() == 'TRUE':
            return True
        else:
            raise ParsingException("Unable to convert '%s' to a boolean" % value)
    
    elif uty == 'INTEGER': 
        return int(value)
    
    elif uty == 'REAL': 
        return float(value)
    
    elif uty == 'STRING': 
        return value.replace("''", "'")[1:-1]
    
    elif uty == 'UNIQUE_ID': 
        if '"' in value:
            return uuid.UUID(value[1:-1]).int
        else:
            return int(value)
    
    else:
        raise ParsingException("Unknown type named '%s'" % ty)


class ParsingException(Exception):
    '''
    An exception that may be thrown while loading (and parsing) a metamodel.
    '''
    pass


class CreateInstanceStmt(object):
    
    def __init__(self, kind, values, names):
        self.kind = kind
        self.values = values
        self.names = names


class CreateClassStmt(object):
    
    def __init__(self, kind, attributes):
        self.kind = kind
        self.attributes = attributes
        

class CreateAssociationStmt(object):
    def __init__(self, rel_id, source_kind, source_cardinality, source_keys, 
                 source_phrase, target_kind, target_cardinality, target_keys,
                target_phrase):
        self.rel_id = rel_id
        self.source_kind = source_kind
        self.target_kind = target_kind
        self.source_keys = source_keys
        self.target_keys = target_keys
        self.source_cardinality = source_cardinality
        self.target_cardinality = target_cardinality
        self.source_phrase = source_phrase
        self.target_phrase = target_phrase
        
 
class CreateUniqueStmt(object):
    
    def __init__(self, kind, name, attributes):
        self.kind = kind
        self.name = name
        self.attributes = attributes


class ModelLoader(object):
    '''
    Class for loading metamodels previously persisted to disk.
    
    Data may be provided in any order, e.g. instances followed by associations, 
    followed by class definitions. One single loader may be used to build
    several *xtuml.MetaModel* objects, and additional data may be provided at
    any time.
    
    **Note:** Additional data will not affect previosly built metamodels.
    
    Usage example:
    
    >>> l = xtuml.ModelLoader()
    >>> l.filename_input('data.sql')
    >>> l.filename_input('schema.sql')
    >>> m1 = l.build_metamodel()
    >>> l.filename_input('additional_data.sql')
    >>> m2 = l.build_metamodel()
    '''
    reserved = (
        'CREATE',
        'FALSE',
        'FROM',
        'INDEX',
        'INSERT',
        'INTO',
        'ON',
        'PHRASE',
        'REF_ID',
        'ROP',
        'TABLE',
        'TO',
        'TRUE',
        'UNIQUE',
        'VALUES'
    )

    tokens = reserved + (
        'CARDINALITY',
        'COMMA',
        'FRACTION',
        'GUID',
        'ID',
        'LPAREN',
        'MINUS',
        'NUMBER',
        'RPAREN',
        'RELID',
        'SEMICOLON',
        'STRING'
    )

    # A string containing ignored characters (spaces and tabs).
    t_ignore = ' \t\r\x0c'

    parser = None
    lexer = None
    statements = None
    
    def __init__(self):
        self.statements = list()
        self.parser = yacc.yacc(debuglog=logger,
                                errorlog=logger,
                                optimize=1,
                                module=self,
                                outputdir=os.path.dirname(__file__),
                                tabmodule='xtuml.__xtuml_parsetab')

    def build_parser(self):
        '''
        This method is deprecated.
        '''
        pass
    
    def input(self, data, name='<string>'):
        '''
        Parse *data* directly from a string. The *name* is used when reporting
        positional information if the parser encounter syntax errors.
        '''
        lexer = lex.lex(debuglog=logger,
                        errorlog=logger,
                        optimize=1,
                        module=self,
                        outputdir=os.path.dirname(__file__),
                        lextab="xtuml.__xtuml_lextab")
        lexer.filename = name
        logger.debug('parsing %s' % name)
        s = self.parser.parse(lexer=lexer, input=data)
        self.statements.extend(s)

    def filename_input(self, filename):
        '''
        Open and read from a *filename* on disk, and parse its content.
        '''
        with open(filename, 'r') as f:
            return self.file_input(f)
    
    def file_input(self, file_object):
        '''
        Read and parse data from a *file object*, i.e. the type of object 
        returned by the builtin python function *open()*.
        '''
        return self.input(file_object.read(), name=file_object.name)

    def populate_classes(self, metamodel):
        '''
        Populate a *metamodel* with classes previously encountered from input.
        '''
        for stmt in self.statements:
            if isinstance(stmt, CreateClassStmt):
                metamodel.define_class(stmt.kind, stmt.attributes)

    def populate_associations(self, metamodel):
        '''
        Populate a *metamodel* with associations previously encountered from
        input.
        '''
        for stmt in self.statements:
            if isinstance(stmt, CreateAssociationStmt):
                metamodel.define_association(stmt.rel_id, 
                                             stmt.source_kind, 
                                             stmt.source_keys,
                                             'M' in stmt.source_cardinality,
                                             'C' in stmt.source_cardinality,
                                             stmt.source_phrase,
                                             stmt.target_kind, 
                                             stmt.target_keys,
                                             'M' in stmt.target_cardinality,
                                             'C' in stmt.target_cardinality,
                                             stmt.target_phrase)

    def populate_unique_identifiers(self, metamodel):
        '''
        Populate a *metamodel* with class unique identifiers previously
        encountered from input.
        '''
        for stmt in self.statements:
            if isinstance(stmt, CreateUniqueStmt):
                metamodel.define_unique_identifier(stmt.kind, stmt.name, 
                                                   *stmt.attributes)

    @staticmethod
    def _populate_matching_class(metamodel, kind, names, values):
        '''
        Populate a *metamodel* with a class that matches the given *insert
        statement*.
        '''
        attributes = list()
        for name, value in zip(names, values):
            ty = guess_type_name(value)
            attr = (name, ty)
            attributes.append(attr)
                
        return metamodel.define_class(kind, attributes)
    
    @staticmethod
    def _populate_instance_with_positional_arguments(metamodel, stmt):
        '''
        Populate a *metamodel* with an instance previously encountered from 
        input that was defined using positional arguments.
        '''
        if stmt.kind.upper() not in metamodel.metaclasses:
            names = ['_%s' % idx for idx in range(len(stmt.values))]
            ModelLoader._populate_matching_class(metamodel, stmt.kind, 
                                                 names, stmt.values)
            
        metaclass = metamodel.find_metaclass(stmt.kind)
        args = list()
            
        if len(metaclass.attributes) != len(stmt.values):
            logger.warn('schema mismatch while loading an instance of %s',
                        stmt.kind)
                
        for attr, value in zip(metaclass.attributes, stmt.values):
            _, ty = attr
            value = deserialize_value(ty, value) 
            args.append(value)
            
        metamodel.new(stmt.kind, *args)
    
    @staticmethod
    def _populate_instance_with_named_arguments(metamodel, stmt):
        '''
        Populate a *metamodel* with an instance previously encountered from 
        input that was defined using named arguments.
        '''
        if stmt.kind.upper() not in metamodel.metaclasses:
            ModelLoader._populate_matching_class(metamodel, stmt.kind, 
                                                 stmt.names, stmt.values)
            
        metaclass = metamodel.find_metaclass(stmt.kind)
            
        schema_unames = [name.upper() for name in metaclass.attribute_names]
        inst_unames = [name.upper() for name in stmt.names]
        
        if set(inst_unames) - set(schema_unames):
            logger.warn('schema mismatch while loading an instance of %s',
                        stmt.kind)
            
        args = list()
        for name, ty in metaclass.attributes:
            uname = name.upper()
            if uname in inst_unames:
                idx = inst_unames.index(uname)
                value = deserialize_value(ty, stmt.values[idx])
            else:
                value = None
                
            args.append(value)
                
        metamodel.new(stmt.kind, *args)

    def populate_instances(self, metamodel):
        '''
        Populate a *metamodel* with instances previously encountered from
        input.
        '''
        for stmt in self.statements:
            if not isinstance(stmt, CreateInstanceStmt):
                continue
            
            if stmt.names:
                self._populate_instance_with_named_arguments(metamodel, stmt)
            else:
                self._populate_instance_with_positional_arguments(metamodel,
                                                                  stmt)
                
    def populate(self, metamodel):
        '''
        Populate a *metamodel* with entities previously encountered from input.
        '''
        self.populate_classes(metamodel)
        self.populate_associations(metamodel)
        self.populate_unique_identifiers(metamodel)
        self.populate_instances(metamodel)
        
    def build_metamodel(self, id_generator=None):
        '''
        Build and return a *xtuml.MetaModel* containing previously loaded input.
        '''
        m = xtuml.MetaModel(id_generator)
        
        self.populate(m)
        
        return m

    def t_comment(self, t):
        r'\-\-([^\n]*\n?)'
        t.lexer.lineno += (t.value.count("\n"))
        t.endlexpos = t.lexpos + len(t.value)

    def t_COMMA(self, t):
        r','
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_FRACTION(self, t):
        r'(\d+)(\.\d+)'
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_RELID(self, t):
        r'R[0-9]+'
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_CARDINALITY(self, t):
        r'(1C)'
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_ID(self, t):
        r'[A-Za-z_][\w_]*'
        vup = t.value.upper()
        if vup in self.reserved:
            t.type = vup
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_LPAREN(self, t):
        r'\('
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_MINUS(self, t):
        r'-'
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_NUMBER(self, t):
        r'[0-9]+'
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_RPAREN(self, t):
        r'\)'
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_SEMICOLON(self, t):
        r';'
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_STRING(self, t):
        r'\'((\'\')|[^\'])*\''
        t.lexer.lineno += (t.value.count("\n"))
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_GUID(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        t.endlexpos = t.lexpos + len(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.endlexpos = t.lexpos + len(t.value)

    def t_error(self, t):
        raise ParsingException("illegal character '%s' at %s:%d" % (t.value[0],
                               t.lexer.filename, t.lineno))

    def p_empty_translation_unit(self, p):
        '''translation_unit :'''
        p[0] = list()
        
    def p_translation_unit(self, p):
        '''translation_unit : statement_sequence'''
        p[0] = p[1]

    def p_statement_sequence(self, p):
        '''statement_sequence : statement_sequence statement'''
        p[0] = p[1]
        p[0].append(p[2])

    def p_statement_sequence_endpoint(self, p):
        '''statement_sequence : statement'''
        p[0] = [p[1]]
        
    def p_statement(self, p):
        '''
        statement : create_table_statement SEMICOLON
                  | insert_into_statement SEMICOLON
                  | create_rop_statement SEMICOLON
                  | create_index_statement SEMICOLON
        '''
        p[0] = p[1]

    def p_create_table_statement(self, p):
        '''create_table_statement : CREATE TABLE identifier LPAREN attribute_sequence RPAREN'''
        p[0] = CreateClassStmt(p[3], p[5])

    def p_empty_attribute_sequence(self, p):
        '''attribute_sequence : '''
        p[0] = []
        
    def p_attribute_sequence_endpoint(self, p):
        '''attribute_sequence : attribute'''
        p[0] = [p[1]]

    def p_attribute_sequence(self, p):
        '''attribute_sequence : attribute_sequence COMMA attribute'''
        p[0] = p[1]
        p[0].append(p[3])

    def p_attribute(self, p):
        '''attribute : identifier identifier'''
        p[0] = (p[1], p[2])

    def p_ordered_insert_into_statement(self, p):
        '''
        insert_into_statement : INSERT INTO identifier VALUES LPAREN value_sequence RPAREN
        '''
        p[0] = CreateInstanceStmt(p[3], p[6], None)

    def p_named_insert_into_statement(self, p):
        '''
        insert_into_statement : INSERT INTO identifier LPAREN identifier_sequence RPAREN VALUES LPAREN value_sequence RPAREN
        '''
        p[0] = CreateInstanceStmt(p[3], p[9], p[5])
    
    def p_empty_value_sequence(self, p):
        '''value_sequence : '''
        p[0] = []

    def p_value_sequence(self, p):
        '''value_sequence : value_sequence COMMA value'''
        p[0] = p[1]
        p[0].append(p[3])
        
    def p_value_sequence_endpoint(self, p):
        '''value_sequence : value'''
        p[0] = [p[1]]
        
    def p_value(self, p):
        '''
        value : FRACTION
              | NUMBER
              | STRING
              | GUID
              | TRUE
              | FALSE
        '''
        p[0] = p[1]

    def p_negative_value(self, p):
        '''
        value : MINUS FRACTION
              | MINUS NUMBER
        '''
        p[0] = p[1] + p[2]
        
    def p_create_rop_statement(self, p):
        '''create_rop_statement : CREATE ROP REF_ID RELID FROM association_end TO association_end'''
        args = [p[4]]
        args.extend(p[6])
        args.extend(p[8])
        p[0] = CreateAssociationStmt(*args)

    def p_association_end(self, p):
        '''association_end : cardinality identifier LPAREN identifier_sequence RPAREN'''
        p[0] = (p[2], p[1], p[4], '')

    def p_phrased_association_end(self, p):
        '''association_end : cardinality identifier LPAREN identifier_sequence RPAREN PHRASE STRING'''
        p[0] = (p[2], p[1], p[4], p[7][1:-1])

    def p_cardinality_1(self, p):
        '''cardinality : NUMBER'''
        if p[1] != '1':
            raise ParsingException("illegal cardinality (%s) at %s:%d" % (p[1],
                                   p.lexer.filename, p.lineno(1)))
        p[0] = p[1]

    def p_cardinality_many(self, p):
        '''cardinality : ID'''
        if p[1] not in ['M', 'MC']:
            raise ParsingException("illegal cardinality (%s) at %s:%d" % (p[1],
                                   p.lexer.filename, p.lineno(1)))
        p[0] = p[1]

    def p_cardinality_01(self, p):
        '''cardinality : CARDINALITY'''
        p[0] = p[1]

    def p_empty_identifier_sequence(self, p):
        '''identifier_sequence : '''
        p[0] = []
        
    def p_identifier_sequence(self, p):
        '''identifier_sequence : identifier_sequence COMMA identifier'''
        p[0] = p[1]
        p[0].append(p[3])

    def p_identifier_sequence_endpoint(self, p):
        '''identifier_sequence : identifier'''
        p[0] = [p[1]]

    def p_identifier(self, p):
        '''
        identifier : ID
                   | CREATE
                   | INSERT
                   | INTO
                   | VALUES
                   | TABLE
                   | ROP
                   | REF_ID
                   | FROM
                   | TO
                   | PHRASE
                   | UNIQUE
                   | INDEX
                   | ON
                   | TRUE
                   | FALSE
        '''
        p[0] = p[1]
        
    def p_create_index_statement(self, p):
        '''
        create_index_statement : CREATE UNIQUE INDEX identifier ON identifier LPAREN identifier_sequence RPAREN
        '''
        p[0] = CreateUniqueStmt(p[6], p[4], p[8])

    def p_error(self, p):
        if p:
            raise ParsingException("illegal token %s (%s) at %s:%d" % (p.type, 
                                   p.value, p.lexer.filename, p.lineno))
        else:
            raise ParsingException("unknown error")


def load_metamodel(resource):
    '''
    Load and return a metamodel from a *resource*. The *resource* may be either
    a filename, or a list of filenames.
    
    Usage example:
    
    >>> metamodel = xtuml.load_metamodel(['schema.sql', 'data.sql'])
    '''
    if isinstance(resource, str):
        resource = [resource]
        
    loader = ModelLoader()
    for filename in resource:
        loader.filename_input(filename)
    
    return loader.build_metamodel()


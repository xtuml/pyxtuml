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
Parser for the Object Action Language (OAL). 
Heavily inspired by: 
   - https://github.com/xtuml/mc/blob/master/mcmc/arlan/arlan.l
   - https://github.com/xtuml/mc/blob/master/mcmc/arlan/arlan.y
   - https://github.com/xtuml/bridgepoint/blob/master/src/org.xtuml.bp.als.oal/bnf/oal.bnf
'''

import os
import logging

from ply import lex
from ply import yacc
from functools import wraps


logger = logging.getLogger(__name__)


class Position(object):
    start_line = -1
    start_column = -1
    end_line = -1
    end_column = -1
    
    def __init__(self, start_line=0, start_column=0, end_line=0, end_column=0):
        self.start_line = start_line
        self.start_column = start_column
        self.end_line = end_line
        self.end_column = end_column
        
    def __str__(self):
        return '%s:%s - %s:%s' % (self.start_line, self.start_column,
                                  self.end_line, self.end_column)
    
    
class Node(object):
    position = None
    character_stream = None
    
    @property
    def children(self):
        return tuple()
    
    def __str__(self):
        return '[%s]:%s' % (self.position, self.__class__.__name__)
    
    
class BodyNode(Node):
    block = None
    
    def __init__(self, block):
        self.block = block
        
    @property
    def children(self):
        return (self.block,)
    
    
class BlockNode(Node):
    statement_list = None
    
    def __init__(self, statement_list):
        self.statement_list = statement_list
        
    @property
    def children(self):
        return (self.statement_list,)


class StatementListNode(Node):
    children = None
    
    def __init__(self):
        self.children = list()
            
    
class BreakNode(Node):
    pass


class ContinueNode(Node):
    pass


class ControlNode(Node):
    pass


class ReturnNode(Node):
    expression = None
    
    def __init__(self, expression):
        self.expression = expression
        
    @property
    def children(self):
        return (self.expression,)


class AssignmentNode(Node):
    variable_access = None
    expression = None
    
    def __init__(self, variable_access, expression):
        self.variable_access = variable_access
        self.expression = expression
        
    @property
    def children(self):
        return (self.variable_access, self.expression)
    
    
class InvocationStatementNode(Node):
    invocation = None
    
    def __init__(self, invocation):
        self.invocation = invocation

    @property
    def children(self):
        return (self.invocation,)
    

class MessageStatementNode(Node):
    invocation = None
    
    def __init__(self, invocation):
        self.invocation = invocation

    @property
    def children(self):
        return (self.invocation,)


class GenerateClassEventNode(Node):
    event_specification = None
    key_letter = None
    
    def __init__(self, event_specification, key_letter):
        self.event_specification = event_specification
        self.key_letter = key_letter
        
    @property
    def children(self):
        return (self.event_specification,)


class GenerateCreatorEventNode(Node):
    event_specification = None
    key_letter = None
    
    def __init__(self, event_specification, key_letter):
        self.event_specification = event_specification
        self.key_letter = key_letter
        
    @property
    def children(self):
        return (self.event_specification,)


class GenerateInstanceEventNode(Node):
    event_specification = None
    variable_name = None
    
    def __init__(self, event_specification, variable_name):
        self.event_specification = event_specification
        self.variable_name = variable_name
        
    @property
    def children(self):
        return (self.event_specification,)


class CreateClassEventNode(Node):
    variable_name = None
    event_specification = None
    key_letter = None
    
    def __init__(self, variable_name, event_specification, key_letter):
        self.variable_name = variable_name
        self.event_specification = event_specification
        self.key_letter = key_letter
        
    @property
    def children(self):
        return (self.event_specification,)


class CreateCreatorEventNode(Node):
    variable_name = None
    event_specification = None
    key_letter = None
    
    def __init__(self, variable_name, event_specification, key_letter):
        self.variable_name = variable_name
        self.event_specification = event_specification
        self.key_letter = key_letter
        
    @property
    def children(self):
        return (self.event_specification,)


class CreateInstanceEventNode(Node):
    variable_name = None
    event_specification = None
    to_variable_name = None
    
    def __init__(self, variable_name, event_specification, to_variable_name):
        self.variable_name = variable_name
        self.event_specification = event_specification
        self.to_variable_name = to_variable_name
        
    @property
    def children(self):
        return (self.event_specification,)


class GeneratePreexistingNode(Node):
    variable_access = None
    
    def __init__(self, variable_access):
        self.variable_access = variable_access
        
    @property
    def children(self):
        return (self.variable_access,)
    
    
    
class CreateObjectNode(Node):
    variable_name = None
    key_letter = None
    
    def __init__(self, variable_name, key_letter):
        self.variable_name = variable_name
        self.key_letter = key_letter


class CreateObjectNoVariableNode(Node):
    key_letter = None
    
    def __init__(self, key_letter):
        self.key_letter = key_letter
        

class DeleteNode(Node):
    variable_name = None
    
    def __init__(self, variable_name):
        self.variable_name = variable_name

    @property
    def children(self):
        return (self.variable_name,)


class CreateEventNode(Node):
    variable_name = None
    event_spec = None
    
    def __init__(self, variable_name, event_spec):
        self.variable_name = variable_name
        self.event_spec = event_spec
        
    @property
    def children(self):
        return (self.event_spec,)


class EventSpecNode(Node):
    identifier = None
    meaning = None
    event_data = None
    
    def __init__(self, identifier, meaning, event_data):
        self.identifier = identifier
        self.meaning = meaning
        self.event_data = event_data
    
    @property
    def children(self):
        return (self.event_data,)


class EventDataListNode(Node):
    children = None
    
    def __init__(self):
        self.children = list()
    

class EventDataItemNode(Node):
    name = None
    expression = None
    
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        
    @property
    def children(self):
        return (self.expression,)


class ForEachNode(Node):
    instance_variable_name = None
    set_variable_name = None
    block = None
    
    def __init__(self, instance_variable_name, set_variable_name, block):
        self.instance_variable_name = instance_variable_name
        self.set_variable_name = set_variable_name
        self.block = block
        
    @property
    def children(self):
        return (self.block,)
    
    
class WhileNode(Node):
    expression = None
    block = None
    
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block
        
    @property
    def children(self):
        return (self.expression, self.block)


class IfNode(Node):
    expression = None
    block = None
    else_clause = None
    elif_list = None
    
    def __init__(self, expression, block, elif_list, else_clause):
        self.expression = expression
        self.block = block
        self.elif_list = elif_list
        self.else_clause = else_clause
        
    @property
    def children(self):
        return (self.expression, self.block, self.elif_list, self.else_clause)
    
    
class ElIfListNode(Node):
    children = None
    
    def __init__(self):
        self.children = list()
        
        
class ElIfNode(Node):
    expression = None
    block = None
    
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block

    @property
    def children(self):
        return (self.expression, self.block)
    
    
class ElseNode(Node):
    block = None
    
    def __init__(self, block):
        self.block = block
        
    @property
    def children(self):
        return (self.block,)


class RelateNode(Node):
    from_variable_name = None
    to_variable_name = None
    rel_id = None
    phrase = None
    
    def __init__(self, from_variable_name, to_variable_name, rel_id, phrase):
        self.from_variable_name = from_variable_name
        self.to_variable_name = to_variable_name
        self.rel_id = rel_id
        self.phrase = phrase
    

class RelateUsingNode(Node):
    from_variable_name = None
    to_variable_name = None
    using_variable_name = None
    rel_id = None
    phrase = None
    
    def __init__(self, from_variable_name, to_variable_name, rel_id, phrase, using_variable_name):
        self.from_variable_name = from_variable_name
        self.to_variable_name = to_variable_name
        self.using_variable_name = using_variable_name
        self.rel_id = rel_id
        self.phrase = phrase


class UnrelateNode(Node):
    from_variable_name = None
    to_variable_name = None
    rel_id = None
    phrase = None
    
    def __init__(self, from_variable_name, to_variable_name, rel_id, phrase):
        self.from_variable_name = from_variable_name
        self.to_variable_name = to_variable_name
        self.rel_id = rel_id
        self.phrase = phrase


class UnrelateUsingNode(Node):
    from_variable_name = None
    to_variable_name = None
    using_variable_name = None
    rel_id = None
    phrase = None
    
    def __init__(self, from_variable_name, to_variable_name, rel_id, phrase, using_variable_name):
        self.from_variable_name = from_variable_name
        self.to_variable_name = to_variable_name
        self.using_variable_name = using_variable_name
        self.rel_id = rel_id
        self.phrase = phrase
    

class SelectRelatedNode(Node):
    cardinality = None
    variable_name = None
    handle = None
    navigation_chain = None

    
    def __init__(self, cardinality, variable_name, handle, navigation_chain):
        self.cardinality = cardinality
        self.variable_name = variable_name
        self.handle = handle
        self.navigation_chain = navigation_chain
    
    @property
    def many(self):
        return self.cardinality.lower() == 'many'
    
    @property
    def children(self):
        return (self.handle, self.navigation_chain)


class SelectRelatedWhereNode(Node):
    cardinality = None
    variable_name = None
    handle = None
    navigation_chain = None
    where_clause = None
    
    def __init__(self, cardinality, variable_name, handle, navigation_chain, where_clause):
        self.cardinality = cardinality
        self.variable_name = variable_name
        self.handle = handle
        self.navigation_chain = navigation_chain
        self.where_clause = where_clause
    
    @property
    def many(self):
        return self.cardinality.lower() == 'many'
    
    @property
    def children(self):
        return (self.handle, self.navigation_chain, self.where_clause)


class NavigationListNode(Node):
    children = None
    
    def __init__(self):
        self.children = list()
        

class NavigationStepNode(Node):
    key_letter = None
    rel_id = None
    phrase = None
    
    def __init__(self, key_letter, rel_id, phrase):
        self.key_letter = key_letter
        self.rel_id = rel_id
        self.phrase = phrase
    

class SelectFromNode(Node):
    cardinality = None
    variable_name = None
    key_letter = None
    
    def __init__(self, cardinality, variable_name, key_letter):
        self.cardinality = cardinality
        self.variable_name = variable_name
        self.key_letter = key_letter
    
    @property
    def many(self):
        return self.cardinality.lower() == 'many'
    
    
class SelectFromWhereNode(Node):
    cardinality = None
    variable_name = None
    key_letter = None
    where_clause = None
    
    def __init__(self, cardinality, variable_name, key_letter, where_clause):
        self.cardinality = cardinality
        self.variable_name = variable_name
        self.key_letter = key_letter
        self.where_clause = where_clause
        
    @property
    def many(self):
        return self.cardinality.lower() == 'many'
    
    @property
    def children(self):
        return (self.where_clause,)


class InstanceInvocationNode(Node):
    handle = None
    action_name = None
    parameter_list = None
    
    def __init__(self, handle, action_name, parameter_list):
        self.handle = handle
        self.action_name = action_name
        self.parameter_list = parameter_list
        
    @property
    def children(self):
        return (self.handle, self.parameter_list)
    

class FunctionInvocationNode(Node):
    action_name = None
    parameter_list = None
    
    def __init__(self, action_name, parameter_list):
        self.action_name = action_name
        self.parameter_list = parameter_list
        
    @property
    def children(self):
        return (self.parameter_list,)
    
    
class ImplicitInvocationNode(Node):
    namespace = None
    action_name = None
    parameter_list = None
    
    def __init__(self, namespace, action_name, parameter_list):
        self.namespace = namespace
        self.action_name = action_name
        self.parameter_list = parameter_list

    @property
    def children(self):
        return (self.parameter_list,)


class ClassInvocationNode(ImplicitInvocationNode):
    
    @property
    def key_letter(self):
        return self.namespace
    
    
class BridgeInvocationNode(ImplicitInvocationNode):
    
    @property
    def key_letter(self):
        return self.namespace
    
    
class PortInvocationNode(ImplicitInvocationNode):
    
    @property
    def port_name(self):
        return self.namespace


class GeneratePortEventNode(Node):
    port_name = None
    action_name = None
    parameter_list = None
    expression = None
    
    def __init__(self, port_name, action_name, parameter_list, expression):
        self.port_name = port_name
        self.action_name = action_name
        self.parameter_list = parameter_list
        self.expression = expression
        
    @property
    def children(self):
        return (self.parameter_list, self.expression)


class ParameterListNode(Node):
    children = None
    
    def __init__(self):
        self.children = list()
           

class ParameterNode(Node):
    name = None
    expression = None
    
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        
    @property
    def children(self):
        return (self.expression,)


class UnaryOperationNode(Node):
    operator = None
    operand = None
    
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
        
    @property
    def children(self):
        return (self.operand,)


class BinaryOperationNode(Node):
    left = None
    operator = None
    right = None
    
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        
    @property
    def children(self):
        return (self.left, self.right)


class SelfAccessNode(Node):
    pass


class SelectedAccessNode(Node):
    pass


class VariableAccessNode(Node):
    variable_name = None
    
    def __init__(self, variable_name):
        self.variable_name = variable_name


class ParamAccessNode(Node):
    variable_name = None
    
    def __init__(self, variable_name):
        self.variable_name = variable_name
    

class FieldAccessNode(Node):
    handle = None
    name = None
    
    def __init__(self, handle, name):
        self.handle = handle
        self.name = name

    @property
    def children(self):
        return (self.handle,)


class IndexAccessNode(Node):
    handle = None
    expression = None
    
    def __init__(self, handle, expression):
        self.handle = handle
        self.expression = expression

    @property
    def children(self):
        return (self.handle, self.expression)
    

class IntegerNode(Node):
    value = None
    
    def __init__(self, value):
        self.value = value


class RealNode(Node):
    value = None
    
    def __init__(self, value):
        self.value = value


class StringNode(Node):
    value = None
    
    def __init__(self, value):
        self.value = value


class BooleanNode(Node):
    value = None
    
    def __init__(self, value):
        self.value = value


class EnumNode(Node):
    namespace = None
    name = None
    
    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name


def find_column(lexdata, lexpos):
    '''
    Find the column index
    '''
    return lexpos - lexdata.rfind('\n', 0, lexpos)


def set_positional_info(node, p):
    '''
    set positional information on a node
    '''
    node.position = Position()
    node.position.start_stream = p.lexpos(1)
    node.position.start_line = p.lineno(1)
    node.position.start_column = find_column(p.lexer.lexdata,
                                             node.position.start_stream)
    
    _, node.position.end_stream = p.lexspan(len(p) - 1)
    _, node.position.end_line = p.linespan(len(p) - 1)
    node.position.end_column = find_column(p.lexer.lexdata,
                                             node.position.end_stream) - 1
    
    node.character_stream = p.lexer.lexdata[node.position.start_stream:
                                            node.position.end_stream]
    
def track_production(f):
    '''
    decorator for adding positional information to returning nodes
    '''
    @wraps(f)
    def wrapper(self, p):
        r = f(self, p)
        node = p[0]
        if isinstance(node, Node) and len(p) > 1:
            set_positional_info(node, p)
        return r
    
    return wrapper


class ParseException(Exception):
    pass


class OALParser(object):
    keywords = ('ASSIGN',
                'ASSIGNER',
                'BREAK',
                'BRIDGE',
                'SEND',
                'CONTROL',
                'STOP',
                'CONTINUE',
                'CREATE',
                'EVENT',
                'INSTANCE',
                'OF',
                'OBJECT',
                'DELETE',
                'FOR',
                'EACH',
                'IN',
                'GENERATE',
                'IF',
                'ELIF',
                'ELSE',
                'RELATE',
                'TO',
                'ACROSS',
                'USING',
                'RETURN',
                'SELECT',
                'ONE',
                'ANY',
                'MANY',
                'TRANSFORM',
                'UNRELATE',
                'FROM',
                'WHILE',
                'CLASS',
                'CREATOR',
                'RELATED',
                'BY',
                'INSTANCES',
                'WHERE',
                'CARDINALITY',
                'EMPTY',
                'FALSE',
                'NOT',
                'NOT_EMPTY',
                'TRUE',
                'AND',
                'OR',
                'PARAM',
                'RCVD_EVT',
                'SELF',
                'SELECTED'
    )
    
    tokens = keywords + (
                         'SEMICOLON',
                         'EQUAL',
                         'DOT',
                         'DOUBLECOLON',
                         'LPAREN',
                         'RPAREN',
                         'TIMES',
                         'COLON',
                         'COMMA',
                         'ARROW',
                         'LSQBR',
                         'RSQBR',
                         'ID',
                         'NAMESPACE',
                         'END_FOR',
                         'END_IF',
                         'END_WHILE',
                         'TICKED_PHRASE',
                         'QMARK',
                         'FRACTION',
                         'NUMBER',
                         'STRING',
                         'DOUBLEEQUAL',
                         'NOTEQUAL',
                         'LESSTHAN',
                         'LE',
                         'GT',
                         'GE',
                         'PLUS',
                         'MINUS',
                         'DIV',
                         'MOD',
                         'COMMENT',
                         'SL_STRING'
        )
    
    
    t_ignore = ' \t\r'
    
    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('nonassoc', 'LESSTHAN', 'LE', 'DOUBLEEQUAL', 'GT', 'GE', 'NOTEQUAL'),
        ('left', 'PLUS', "MINUS"),
        ('left', "TIMES", "DIV"),
        ('left', 'MOD'),
        ('right', 'UNARY'),
    )
    
    def __init__(self):
        self.parser = yacc.yacc(debuglog=logger,
                                errorlog=logger,
                                optimize=1,
                                module=self,
                                outputdir=os.path.dirname(__file__),
                                tabmodule='bridgepoint.__oal_parsetab')

    def text_input(self, text):
        lexer = lex.lex(debuglog=logger,
                        errorlog=logger,
                        optimize=1,
                        module=self,
                        outputdir=os.path.dirname(__file__),
                        lextab="bridgepoint.__oal_lextab")

        return self.parser.parse(lexer=lexer,
                                 input=text,
                                 tracking=1)

    def t_COMMENT(self, t):
        r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
        t.lexer.lineno += t.value.count('\n')
        t.endlexpos = t.lexpos + len(t.value)
    
    def t_SL_STRING(self, t):
        r'\/\/.*\n'
        t.lexer.lineno += t.value.count('\n')
        t.endlexpos = t.lexpos + len(t.value)
    
    def t_TICKED_PHRASE(self, t):
        r"\'[^\']*\'"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_STRING(self, t):
        r'"[^"\n]*"'
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_END_FOR(self, t):
        r"(?i)end[\s]+for"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_END_IF(self, t):
        r"(?i)end[\s]+if"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_END_WHILE(self, t):
        r"(?i)end[\s]+while"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_NAMESPACE(self, t):
        r"([0-9a-zA-Z_])+(?=::)"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_ID(self, t):
        r"[a-zA-Z_][0-9a-zA-Z_]*|[a-zA-Z][0-9a-zA-Z_]*[0-9a-zA-Z_]+"
        t.endlexpos = t.lexpos + len(t.value)
        
        value = t.value.upper()
        if value in self.keywords:
            t.type = value
            
        return t
        
    def t_FRACTION(self, t):
        r"(((\d*\.\d+)|(\d+\.)([eE][-+]?\d+)?)|(\d+([eE][-+]?\d+)))[FfLl]?"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_NUMBER(self, t):
        r"\d+"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_DOUBLECOLON(self, t):
        r"::"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_DOUBLEEQUAL(self, t):
        r"\=\="
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_NOTEQUAL(self, t):
        r"!\="
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_ARROW(self, t):
        r"\-\>"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_LE(self, t):
        r"\<\="
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_GE(self, t):
        r"\>\="
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_SEMICOLON(self, t):
        r";"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_EQUAL(self, t):
        r"\="
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_DOT(self, t):
        r"\."
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_LPAREN(self, t):
        r"\("
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_RPAREN(self, t):
        r"\)"
        t.endlexpos = t.lexpos + len(t.value)
        return t
        
    def t_TIMES(self, t):
        r"\*"
        t.endlexpos = t.lexpos + len(t.value)
        return t
        
    def t_COLON(self, t):
        r":"
        t.endlexpos = t.lexpos + len(t.value)
        return t
        
    def t_COMMA(self, t):
        r","
        t.endlexpos = t.lexpos + len(t.value)
        return t
        
    def t_LSQBR(self, t):
        r"\["
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_RSQBR(self, t):
        r"\]"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_QMARK(self, t):
        r"\?"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_LESSTHAN(self, t):
        r"\<"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_GT(self, t):
        r"\>"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_PLUS(self, t):
        r"\+"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_MINUS(self, t):
        r"\-"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_DIV(self, t):
        r"/"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_MOD(self, t):
        r"%"
        t.endlexpos = t.lexpos + len(t.value)
        return t
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.endlexpos = t.lexpos + len(t.value)
        
    def t_error(self, t):
        logger.error("%d,%d:illegal character '%s'in INITIAL" % (t.lineno, t.lexpos, t.value[0]))
        t.lexer.skip(1)
    
    @track_production
    def p_action(self, p):
        '''action : action_body'''
        p[0] = p[1]
         
    @track_production
    def p_action_body(self, p):
        '''action_body : block'''
        p[0] = BodyNode(block=p[1])
    
    @track_production
    def p_block(self, p):
        '''block : statement_list'''
        p[0] = BlockNode(statement_list=p[1])
    
    @track_production
    def p_empty_block(self, p):
        '''block : '''
        p[0] = BlockNode(statement_list=StatementListNode())
        
    @track_production       
    def p_statement_list_1(self, p):
        '''statement_list : statement SEMICOLON statement_list'''
        p[0] = p[3]
        if p[1] is not None:
            p[0].children.insert(0, p[1])
    
    @track_production
    def p_statement_list_2(self, p):
        '''statement_list : statement SEMICOLON'''
        p[0] = StatementListNode()
        if p[1] is not None:
            p[0].children.insert(0, p[1])
    
    @track_production
    def p_empty_statement(self, p):
        '''statement : '''
        pass
    
    @track_production
    def p_break_statement(self, p):
        '''statement : BREAK'''
        p[0] = BreakNode()
    
    @track_production
    def p_continue_statement(self, p):
        '''statement : CONTINUE'''
        p[0] = ContinueNode()
    
    @track_production
    def p_control_statement(self, p):
        '''statement : CONTROL STOP'''
        p[0] = ControlNode()
        
    @track_production
    def p_return_statement_1(self, p):
        '''statement : RETURN expression'''
        p[0] = ReturnNode(expression=p[2])
    
    @track_production
    def p_return_statement_2(self, p):
        '''statement : RETURN'''
        p[0] = ReturnNode(expression=None)

    @track_production
    def p_explicit_assignment_statement(self, p):
        '''statement : ASSIGN variable_access EQUAL expression'''
        p[0] = AssignmentNode(variable_access=p[2],
                              expression=p[4])
    
    @track_production
    def p_implicit_assignment_statement(self, p):
        '''statement : variable_access EQUAL expression'''
        p[0] = AssignmentNode(variable_access=p[1],
                              expression=p[3])
    
    @track_production
    def p_function_invocation_statement(self, p):
        '''statement : invocation'''
        p[0] = InvocationStatementNode(p[1])
    
    @track_production
    def p_bridge_assignment_statement(self, p):
        '''statement : BRIDGE variable_access EQUAL implicit_invocation'''
        p[4].__class__ = BridgeInvocationNode
        p[0] = AssignmentNode(variable_access=p[2],
                              expression=p[4])
        
    @track_production
    def p_bridge_invocation_statement(self, p):
        '''statement : BRIDGE implicit_invocation'''
        p[2].__class__ = BridgeInvocationNode
        p[0] = InvocationStatementNode(p[2])
        
    @track_production
    def p_instance_invocation_statement(self, p):
        '''statement : TRANSFORM instance_invocation'''
        p[0] = InvocationStatementNode(p[2])
    
    @track_production
    def p_instance_invocation_assignment_statement(self, p):
        '''statement : TRANSFORM variable_access EQUAL instance_invocation'''
        p[0] = AssignmentNode(variable_access=p[2],
                              expression=p[4])
        
    @track_production
    def p_class_invocation_statement(self, p):
        '''statement : TRANSFORM implicit_invocation'''
        p[2].__class__ = ClassInvocationNode
        p[0] = InvocationStatementNode(p[2])
        
    @track_production
    def p_class_invocation_assignment_statement(self, p):
        '''statement : TRANSFORM variable_access EQUAL implicit_invocation'''
        p[4].__class__ = ClassInvocationNode
        p[0] = AssignmentNode(variable_access=p[2],
                              expression=p[4])
    
    @track_production
    def p_port_invocation_statement(self, p):
        '''statement : SEND implicit_invocation'''
        p[2].__class__ = PortInvocationNode
        p[0] = InvocationStatementNode(p[2])
        
    @track_production
    def p_port_invocation_assignment_statement(self, p):
        '''statement : SEND variable_access EQUAL implicit_invocation'''
        p[4].__class__ = PortInvocationNode
        p[0] = AssignmentNode(variable_access=p[2],
                              expression=p[4])
    
    @track_production
    def p_port_event_generation(self, p):
        '''statement : SEND namespace DOUBLECOLON identifier LPAREN parameter_list RPAREN TO expression'''
        p[0] = GeneratePortEventNode(port_name=p[2],
                                     action_name=p[4],
                                     parameter_list=p[6],
                                     expression=p[9])
        
    @track_production
    def p_generate_class_event_statement(self, p):
        '''statement : GENERATE event_specification TO identifier CLASS'''
        p[0] = GenerateClassEventNode(event_specification=p[2],
                                      key_letter=p[4])
    
    @track_production
    def p_generate_assigner_event_statement(self, p):
        '''statement : GENERATE event_specification TO identifier ASSIGNER'''
        p[0] = GenerateClassEventNode(event_specification=p[2],
                                      key_letter=p[4])
        
    @track_production
    def p_generate_creator_event_statement(self, p):
        '''statement : GENERATE event_specification TO identifier CREATOR'''
        p[0] = GenerateCreatorEventNode(event_specification=p[2],
                                        key_letter=p[4])
    
    @track_production
    def p_generate_instance_event_statement_1(self, p):
        '''statement : GENERATE event_specification TO identifier'''
        p[0] = GenerateInstanceEventNode(event_specification=p[2],
                                         variable_name=p[4])
        
    @track_production
    def p_create_class_event_statement(self, p):
        '''statement : CREATE EVENT INSTANCE variable_name OF event_specification TO identifier CLASS'''
        p[0] = CreateClassEventNode(variable_name=p[4],
                                    event_specification=p[6],
                                    key_letter=p[8])
        
    @track_production
    def p_create_assigner_event_statement(self, p):
        '''statement : CREATE EVENT INSTANCE variable_name OF event_specification TO identifier ASSIGNER'''
        p[0] = CreateClassEventNode(variable_name=p[4],
                                    event_specification=p[6],
                                    key_letter=p[8])
        
    @track_production
    def p_create_creator_event_statement(self, p):
        '''statement : CREATE EVENT INSTANCE variable_name OF event_specification TO identifier CREATOR'''
        p[0] = CreateCreatorEventNode(variable_name=p[4],
                                      event_specification=p[6],
                                      key_letter=p[8])
    
    @track_production
    def p_create_instance_event_statement_1(self, p):
        '''statement : CREATE EVENT INSTANCE variable_name OF event_specification TO variable_name'''
        p[0] = CreateInstanceEventNode(variable_name=p[4],
                                       event_specification=p[6],
                                       to_variable_name=p[8])
    
    @track_production
    def p_create_instance_event_statement_2(self, p):
        '''statement : CREATE EVENT INSTANCE variable_name OF event_specification TO SELF'''
        p[0] = CreateInstanceEventNode(variable_name=p[4],
                                       event_specification=p[6],
                                       to_variable_name=p[8])
        
    @track_production
    def p_generate_preexisting_event_statement(self, p):
        '''statement : GENERATE variable_access'''
        p[0] = GeneratePreexistingNode(variable_access=p[2])
    
    @track_production
    def p_event_specification(self, p):
        '''event_specification : identifier event_meaning event_data'''
        p[0] = EventSpecNode(identifier=p[1],
                             meaning=p[2],
                             event_data=p[3])
    
    @track_production
    def p_ploymorphic_event_spec(self, p):
        '''event_specification : identifier TIMES event_meaning event_data'''
        p[0] = EventSpecNode(identifier=p[1],
                             meaning=p[3],
                             event_data=p[4])
    
    
    def p_phrase_1(self, p):
        '''phrase : TICKED_PHRASE'''
        p[0] = p[1]
        
    def p_phrase_2(self, p):
        '''phrase : identifier'''
        p[0] = "'%s'" % p[1]
        
    @track_production
    def p_event_meaning(self, p):
        '''event_meaning : COLON phrase'''
        p[0] = p[2]
            
    @track_production
    def p_event_meaning_4(self, p):
        '''event_meaning : '''
        p[0] = None
    
    @track_production
    def p_event_data_1(self, p):
        '''event_data : LPAREN event_parameter_list RPAREN'''
        p[0] = p[2]
    
    @track_production
    def p_event_data_2(self, p):
        '''event_data : '''
        p[0] = EventDataListNode()

    @track_production
    def p_event_parameter_list_1(self, p):
        '''event_parameter_list : event_parameter'''
        p[0] = EventDataListNode()
        p[0].children.append(p[1])
    
    @track_production
    def p_event_parameter_list_2(self, p):
        '''event_parameter_list : event_parameter COMMA event_parameter_list'''
        p[0] = p[3]
        p[0].children.insert(0, p[1])
    
    @track_production
    def p_event_parameter_list_3(self, p):
        '''event_parameter_list : '''
        p[0] = EventDataListNode()
    
    @track_production
    def p_event_parameter(self, p):
        '''event_parameter : identifier COLON expression'''
        p[0] = EventDataItemNode(name=p[1],
                                 expression=p[3])

    @track_production
    def p_create_object_statement(self, p):
        '''statement : CREATE OBJECT INSTANCE variable_name OF identifier'''
        p[0] = CreateObjectNode(variable_name=p[4],
                                key_letter=p[6])
    
    @track_production
    def p_create_object_no_variable_statement(self, p):
        '''statement : CREATE OBJECT INSTANCE OF identifier'''
        p[0] = CreateObjectNoVariableNode(key_letter=p[5])
        
    @track_production
    def p_delete_statement(self, p):
        '''statement : DELETE OBJECT INSTANCE instance_name'''
        p[0] = DeleteNode(variable_name=p[4])
    
    @track_production
    def p_for_statement(self, p):
        '''statement : FOR EACH variable_name IN variable_name block END_FOR'''
        p[0] = ForEachNode(instance_variable_name=p[3],
                           set_variable_name=p[5],
                           block=p[6])
    
    @track_production
    def p_while_statement(self, p):
        '''statement : WHILE expression block END_WHILE'''
        p[0] = WhileNode(expression=p[2],
                         block=p[3])
    
    @track_production
    def p_if_statement(self, p):
        '''statement : IF expression block elif_list else_clause END_IF'''
        p[0] = IfNode(expression=p[2],
                      block=p[3],
                      elif_list=p[4],
                      else_clause=p[5])
    
    @track_production       
    def p_elif_list_1(self, p):
        '''elif_list : '''
        p[0] = ElIfListNode()
            
    @track_production       
    def p_elif_list_2(self, p):
        '''elif_list : ELIF elif_clause elif_list'''
        p[0] = p[3]
        p[0].children.insert(0, p[2])
        
    @track_production
    def p_elif_clause(self, p):
        '''elif_clause : expression block'''
        p[0] = ElIfNode(expression=p[1],
                        block=p[2])

    @track_production
    def p_else_clause_1(self, p):
        '''else_clause : ELSE block'''
        p[0] = ElseNode(p[2])
    
    @track_production
    def p_else_clause_2(self, p):
        '''else_clause : '''
        p[0] = None
    
    def p_rel_id(self, p):
        '''rel_id : limited_identifier'''
        p[0] = p[1]
        
    @track_production
    def p_relate_statement_1(self, p):
        '''statement : RELATE instance_name TO instance_name ACROSS rel_id'''
        p[0] = RelateNode(from_variable_name=p[2],
                          to_variable_name=p[4],
                          rel_id=p[6],
                          phrase=None)
    
    @track_production
    def p_relate_statement_2(self, p):
        '''statement : RELATE instance_name TO instance_name ACROSS rel_id DOT phrase'''
        p[0] = RelateNode(from_variable_name=p[2],
                          to_variable_name=p[4],
                          rel_id=p[6],
                          phrase=p[8])
    
    @track_production
    def p_relate_using_statement_1(self, p):
        '''statement : RELATE instance_name TO instance_name ACROSS rel_id USING instance_name'''
        p[0] = RelateUsingNode(from_variable_name=p[2],
                               to_variable_name=p[4],
                               rel_id=p[6],
                               phrase=None,
                               using_variable_name=p[8])
    
    @track_production
    def p_relate_using_statement_2(self, p):
        '''statement : RELATE instance_name TO instance_name ACROSS rel_id DOT phrase USING instance_name'''
        p[0] = RelateUsingNode(from_variable_name=p[2],
                               to_variable_name=p[4],
                               rel_id=p[6],
                               phrase=p[8],
                               using_variable_name=p[10])
    
    @track_production
    def p_unrelate_statement_1(self, p):
        '''statement : UNRELATE instance_name FROM instance_name ACROSS rel_id'''
        p[0] = UnrelateNode(from_variable_name=p[2],
                            to_variable_name=p[4],
                            rel_id=p[6],
                            phrase=None)
    
    @track_production
    def p_unrelate_statement_2(self, p):
        '''statement : UNRELATE instance_name FROM instance_name ACROSS rel_id DOT phrase'''
        p[0] = UnrelateNode(from_variable_name=p[2],
                            to_variable_name=p[4],
                            rel_id=p[6],
                            phrase=p[8])
    
    @track_production
    def p_unrelate_statement_using_1(self, p):
        '''statement : UNRELATE instance_name FROM instance_name ACROSS rel_id USING instance_name'''
        p[0] = UnrelateUsingNode(from_variable_name=p[2],
                                 to_variable_name=p[4],
                                 rel_id=p[6],
                                 phrase=None,
                                 using_variable_name=p[8])
    
    @track_production
    def p_unrelate_statement_using_2(self, p):
        '''statement : UNRELATE instance_name FROM instance_name ACROSS rel_id DOT phrase USING instance_name'''
        p[0] = UnrelateUsingNode(from_variable_name=p[2],
                                 to_variable_name=p[4],
                                 rel_id=p[6],
                                 phrase=p[8],
                                 using_variable_name=p[10])
    
    @track_production
    def p_select_from_statement_1(self, p):
        '''
        statement : SELECT ANY variable_name FROM INSTANCES OF identifier
                  | SELECT MANY variable_name FROM INSTANCES OF identifier
        '''
        p[0] = SelectFromNode(cardinality=p[2],
                              variable_name=p[3],
                              key_letter=p[7])
                              
    @track_production
    def p_select_from_statement_2(self, p):
        '''
        statement : SELECT ANY variable_name FROM identifier
                  | SELECT MANY variable_name FROM identifier
        '''
        p[0] = SelectFromNode(cardinality=p[2],
                              variable_name=p[3],
                              key_letter=p[5])
    
    @track_production
    def p_select_from_where_statement_1(self, p):
        '''
        statement : SELECT ANY variable_name FROM INSTANCES OF identifier WHERE expression
                  | SELECT MANY variable_name FROM INSTANCES OF identifier WHERE expression
        '''
        p[0] = SelectFromWhereNode(cardinality=p[2],
                                   variable_name=p[3],
                                   key_letter=p[7],
                                   where_clause=p[9])
    
    @track_production
    def p_select_from_where_statement_2(self, p):
        '''
        statement : SELECT ANY variable_name FROM identifier WHERE expression
                  | SELECT MANY variable_name FROM identifier WHERE expression
        '''
        p[0] = SelectFromWhereNode(cardinality=p[2],
                                   variable_name=p[3],
                                   key_letter=p[5],
                                   where_clause=p[7])
                                   
    def p_navigation_hook(self, p):
        '''
        navigation_hook : variable_access
                        | self_access
        '''
        p[0] = p[1]
        
    @track_production
    def p_select_related_statement(self, p):
        '''
        statement : SELECT ONE  variable_name RELATED BY navigation_hook navigation_chain
                  | SELECT ANY  variable_name RELATED BY navigation_hook navigation_chain
                  | SELECT MANY variable_name RELATED BY navigation_hook navigation_chain
        '''
        p[0] = SelectRelatedNode(cardinality=p[2],
                                 variable_name=p[3],
                                 handle=p[6],
                                 navigation_chain=p[7])
    
    @track_production
    def p_select_related_where_statement(self, p):
        '''
        statement : SELECT ONE  variable_name RELATED BY navigation_hook navigation_chain WHERE expression
                  | SELECT ANY  variable_name RELATED BY navigation_hook navigation_chain WHERE expression
                  | SELECT MANY variable_name RELATED BY navigation_hook navigation_chain WHERE expression
        '''
        p[0] = SelectRelatedWhereNode(cardinality=p[2],
                                      variable_name=p[3],
                                      handle=p[6],
                                      navigation_chain=p[7],
                                      where_clause=p[9])
        
    @track_production
    def p_navigation_chain_1(self, p):
        '''navigation_chain : navigation_step'''
        p[0] = NavigationListNode()
        p[0].children.append(p[1])
    
    @track_production
    def p_navigation_chain_2(self, p):
        '''navigation_chain : navigation_step navigation_chain'''
        p[0] = p[2]
        p[0].children.insert(0, p[1])
    
    @track_production
    def p_navigation_step_1(self, p):
        '''navigation_step : ARROW identifier LSQBR identifier RSQBR'''
        p[0] = NavigationStepNode(key_letter=p[2],
                                  rel_id=p[4],
                                  phrase=None)

    @track_production
    def p_navigation_step_2(self, p):
        '''navigation_step : ARROW identifier LSQBR identifier DOT phrase RSQBR'''
        p[0] = NavigationStepNode(key_letter=p[2],
                                  rel_id=p[4],
                                  phrase=p[6])

    @track_production
    def p_invocation(self, p):
        '''
        invocation : implicit_invocation
                   | function_invocation
                   | instance_invocation
        '''
        p[0] = p[1]
        
    @track_production
    def p_implicit_invocation(self, p):
        '''implicit_invocation : namespace DOUBLECOLON identifier LPAREN parameter_list RPAREN'''
        p[0] = ImplicitInvocationNode(namespace=p[1],
                                      action_name=p[3],
                                      parameter_list=p[5])
    
    @track_production
    def p_function_invocation(self, p):
        '''function_invocation : DOUBLECOLON identifier LPAREN parameter_list RPAREN'''
        p[0] = FunctionInvocationNode(action_name=p[2],
                                      parameter_list=p[4])
    
    @track_production
    def p_operation_invocation_1(self, p):
        '''instance_invocation : structure DOT identifier LPAREN parameter_list RPAREN'''
        p[0] = InstanceInvocationNode(handle=p[1],
                                      action_name=p[3],
                                      parameter_list=p[5])

    @track_production
    def p_parameter_list_1(self, p):
        '''parameter_list : parameter'''
        p[0] = ParameterListNode()
        p[0].children.append(p[1])
    
    @track_production
    def p_parameter_list_2(self, p):
        '''parameter_list : parameter COMMA parameter_list'''
        p[0] = p[3]
        p[0].children.insert(0, p[1])
    
    @track_production
    def p_parameter_list_3(self, p):
        '''parameter_list : '''
        p[0] = ParameterListNode()
    
    @track_production
    def p_parameter(self, p):
        '''parameter : identifier COLON expression'''
        p[0] = ParameterNode(name=p[1],
                             expression=p[3])
        
    @track_production
    def p_expression_1(self, p):
        '''expression : constant'''
        p[0] = p[1]
    
    @track_production
    def p_expression_2(self, p):
        '''expression : variable_access'''
        p[0] = p[1]

    @track_production
    def p_expression_4(self, p):
        '''expression : self_access'''
        p[0] = p[1]
        
    @track_production
    def p_expression_5(self, p):
        '''expression : selected_access'''
        p[0] = p[1]
        
    @track_production
    def p_grouped_expression(self, p):
        '''expression : LPAREN expression RPAREN'''
        p[0] = p[2]   

    @track_production
    def p_invocation_expression(self, p):
        '''expression : invocation'''
        p[0] = p[1]

    @track_production
    def p_unary_expression(self, p):
        '''expression : unary_operator expression %prec UNARY'''
        p[0] = UnaryOperationNode(operator=p[1],
                                  operand=p[2])
    
    @track_production
    def p_arithmetic_expression(self, p):
        '''
        expression : expression PLUS  expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIV   expression
                   | expression MOD   expression
        '''
        p[0] = BinaryOperationNode(left=p[1],
                                   operator=p[2],
                                   right=p[3])
    
    @track_production
    def p_boolean_expression(self, p):
        '''
        expression : expression LE          expression
                   | expression LESSTHAN    expression
                   | expression DOUBLEEQUAL expression
                   | expression NOTEQUAL    expression
                   | expression GE          expression
                   | expression GT          expression
                   | expression AND         expression
                   | expression OR          expression
        '''
        p[0] = BinaryOperationNode(left=p[1],
                                   operator=p[2],
                                   right=p[3])
    
    @track_production
    def p_limited_identifier(self, p):
        '''
        limited_identifier : ID
                           | kw_as_identifier_1
        '''
        p[0] = p[1]
        
    @track_production
    def p_namespace(self, p):
        '''
        namespace : NAMESPACE
        '''
        p[0] = p[1]
    
    @track_production
    def p_kw_as_identifier_1(self, p):
        '''kw_as_identifier_1 : ACROSS
                              | ANY
                              | ASSIGN
                              | ASSIGNER
                              | BREAK
                              | BY
                              | CLASS
                              | CONTINUE
                              | CONTROL
                              | CREATE
                              | CREATOR
                              | DELETE
                              | EACH
                              | EVENT
                              | FOR
                              | FROM
                              | GENERATE
                              | IN
                              | INSTANCES
                              | INSTANCE
                              | MANY
                              | OBJECT
                              | ONE
                              | RELATED
                              | RELATE
                              | SELECT
                              | STOP
                              | TO
                              | WHERE
                              | UNRELATE
                              | USING
        '''
        p[0] = p[1]
        #FIXME: the oal parser currently does not allow variables named 'of'
    
    @track_production
    def p_kw_as_identifier_2(self, p):
        '''
        kw_as_identifier_2 : BRIDGE
                           | CARDINALITY
                           | EMPTY
                           | FALSE
                           | NOT
                           | NOT_EMPTY
                           | SEND
                           | TRANSFORM
                           | TRUE
                           | OF
        '''
        p[0] = p[1]
        
    @track_production
    def p_kw_as_identifier_3(self, p):
        '''
        kw_as_identifier_3 : PARAM
                           | RCVD_EVT
                           | SELECTED
                           | SELF
        '''
        p[0] = p[1]
        
    @track_production
    def p_kw_as_identifier_4(self, p):
        '''
        kw_as_identifier_4 : AND
                           | ELIF
                           | ELSE
                           | IF
                           | OR
                           | RETURN
                           | WHILE
        '''
        p[0] = p[1]
                
    @track_production
    def p_variable_name(self, p):
        '''variable_name : limited_identifier'''
        p[0] = p[1]

    @track_production
    def p_instance_name(self, p):
        '''instance_name : variable_name
                         | SELF
        '''
        p[0] = p[1]
        
    @track_production
    def p_identifier(self, p):
        '''
        identifier : limited_identifier
              | kw_as_identifier_2
              | kw_as_identifier_3
              | kw_as_identifier_4
        '''
        p[0] = p[1]
        
    @track_production
    def p_structure_1(self, p):
        '''structure : variable_name'''
        p[0] = VariableAccessNode(variable_name=p[1])
        
    @track_production
    def p_structure_2(self, p):
        '''structure : SELF'''
        p[0] = SelfAccessNode()
        
    @track_production
    def p_structure_3(self, p):
        '''structure : SELECTED'''
        p[0] = SelectedAccessNode()
        
    @track_production
    def p_field_access(self, p):
        '''
        field_access : structure    DOT identifier
                     | index_access DOT identifier
                     | field_access DOT identifier
                     | param_access DOT identifier
        '''
        p[0] = FieldAccessNode(handle=p[1], name=p[3])

    @track_production
    def p_array(self, p):
        '''array : variable_name'''
        p[0] = VariableAccessNode(variable_name=p[1])
        
    @track_production
    def p_index_access(self, p):
        '''index_access : array        LSQBR expression RSQBR
                        | index_access LSQBR expression RSQBR
                        | field_access LSQBR expression RSQBR
                        | param_access LSQBR expression RSQBR
        '''
        p[0] = IndexAccessNode(handle=p[1], expression=p[3])
        
    @track_production
    def p_param(self, p):
        '''
        param : PARAM
              | RCVD_EVT
        '''
        p[0] = p[1]
        
    @track_production
    def p_param_access_1(self, p):
        '''param_access : param DOT variable_name'''
        p[0] = ParamAccessNode(variable_name=p[3])

    @track_production
    def p_self_access_1(self, p):
        '''self_access : SELF'''
        p[0] = SelfAccessNode()
        
    @track_production
    def p_selected_access_1(self, p):
        '''selected_access : SELECTED'''
        p[0] = SelectedAccessNode()
    
    @track_production
    def p_variable_access_1(self, p):
        '''variable_access : variable_name'''
        p[0] = VariableAccessNode(variable_name=p[1])
        
    @track_production
    def p_variable_access_2(self, p):
        '''variable_access : field_access'''
        p[0] = p[1]
        
    @track_production
    def p_variable_access_3(self, p):
        '''variable_access : index_access'''
        p[0] = p[1]
        
    @track_production
    def p_variable_access_4(self, p):
        '''variable_access : param_access'''
        p[0] = p[1]
        
    @track_production
    def p_constant_fraction(self, p):
        '''constant : FRACTION'''
        p[0] = RealNode(value=p[1])

    @track_production
    def p_constant_number(self, p):
        '''constant : NUMBER'''
        p[0] = IntegerNode(value=p[1])
    
    @track_production
    def p_constant_string(self, p):
        '''constant : STRING'''
        p[0] = StringNode(value=p[1])
    
    @track_production
    def p_constant_boolean(self, p):
        '''
        constant : TRUE
                 | FALSE
        '''
        p[0] = BooleanNode(value=p[1])
    
    @track_production
    def p_constant_enum(self, p):
        '''constant : namespace DOUBLECOLON identifier'''
        p[0] = EnumNode(namespace=p[1],
                        name=p[3])

    @track_production
    def p_unary_operator(self, p):
        '''
        unary_operator : NOT
                       | EMPTY
                       | NOT_EMPTY
                       | CARDINALITY
                       | PLUS
                       | MINUS
        '''
        p[0] = p[1]
    
    def p_error(self, p):
        if p:
            raise ParseException("invalid token '%s' at %s:%s" % (p.type,
                                                                  p.lineno,
                                                                  find_column(p.lexer.lexdata, p.lexpos)))
        else:
            raise ParseException("unknown parsing error")


def parse(action_code):
    '''
    Parse and construct an abstract syntax tree for text expressed in the
    Object Action Language (OAL).
    '''
    parser = OALParser()
    return parser.text_input(action_code + '\n')


if __name__ == '__main__':
    import sys
    import xtuml.tools
    logging.basicConfig(level=logging.WARN)
    
    print ('Enter the character stream below. Press Ctrl-D to begin parsing.')
    print ('')
    s = sys.stdin.read()
    
    print ('--------- Token Stream ----------')
    parser = OALParser()
    lexer = lex.lex(module=parser)
    lexer.input(s)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    print ('--------- Syntax Tree ----------')
    root = parse(s)
    w = xtuml.tools.Walker()
    w.visitors.append(xtuml.tools.NodePrintVisitor())
    w.accept(root)


    
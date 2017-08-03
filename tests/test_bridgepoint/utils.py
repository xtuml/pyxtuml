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
from bridgepoint import oal
from bridgepoint import sourcegen
from bridgepoint import prebuild
from bridgepoint import ooaofooa


class CompareAST(unittest.TestCase):
    '''
    Walk the syntax tree and compare each node.
    '''
    def compare(self, x, y):
        name = 'compare_' + x.__class__.__name__ + '_with_' + y.__class__.__name__
        fn = getattr(self, name, None)
        if fn: return fn(x, y)
        
        name = 'compare_' + y.__class__.__name__ + '_with_' + x.__class__.__name__
        fn = getattr(self, name, None)
        if fn: return fn(y, x)
        
        if x.__class__.__name__ == y.__class__.__name__:
            name = 'compare_' + x.__class__.__name__
            fn = getattr(self, name, None)
            if fn: return fn(x, y)

        return self.default_compare(x, y)
        
    def default_compare(self, x, y):
        self.assertEqual(x, y)
        
    def compare_BodyNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
        
    def compare_BlockNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
        
    def compare_StatementListNode(self, x, y):
        self.assertEqual(len(x.children), len(y.children))
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
        
    def compare_CreateObjectNode(self, x, y):
        self.assertEqual(x.variable_name, y.variable_name)
        self.assertEqual(x.key_letter, y.key_letter)
        
    def compare_CreateObjectNoVariableNode(self, x, y):
        self.assertEqual(x.key_letter, y.key_letter)
        
    def compare_GenerateClassEventNode(self, x, y):
        self.assertEqual(x.key_letter, y.key_letter)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)

    def compare_GenerateCreatorEventNode(self, x, y):
        self.assertEqual(x.key_letter, y.key_letter)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_GenerateInstanceEventNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_CreateInstanceEventNode(self, x, y):
        self.assertEqual(x.variable_name, y.variable_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
          
    def compare_CreateCreatorEventNode(self, x, y):
        self.assertEqual(x.variable_name, y.variable_name)
        self.assertEqual(x.key_letter, y.key_letter)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_CreateClassEventNode(self, x, y):
        self.assertEqual(x.variable_name, y.variable_name)
        self.assertEqual(x.key_letter, y.key_letter)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_GeneratePreexistingNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
              
    def compare_EventSpecNode(self, x, y):
        self.assertEqual(x.identifier, y.identifier)
        if None not in [x.meaning, y.meaning]:
            self.assertEqual(x.meaning, y.meaning)
            
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_EventDataListNode(self, x, y):
        self.assertEqual(len(x.children), len(y.children))
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_EventDataItemNode(self, x, y):
        self.assertEqual(x.name, y.name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_ParameterListNode(self, x, y):
        self.assertEqual(len(x.children), len(y.children))
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_ParameterNode(self, x, y):
        self.assertEqual(x.name, y.name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_NavigationListNode(self, x, y):
        self.assertEqual(len(x.children), len(y.children))
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_NavigationStepNode(self, x, y):
        self.assertEqual(x.key_letter, y.key_letter)
        self.assertEqual(x.rel_id.lower(), y.rel_id.lower())
        if None not in [x.phrase, y.phrase]:
            self.assertEqual(x.phrase, y.phrase)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_SelectRelatedNode(self, x, y):
        self.assertEqual(x.cardinality, y.cardinality)
        self.assertEqual(x.variable_name, y.variable_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_SelectRelatedWhereNode(self, x, y):
        self.assertEqual(x.cardinality, y.cardinality)
        self.assertEqual(x.variable_name, y.variable_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_SelectFromNode(self, x, y):
        self.assertEqual(x.cardinality, y.cardinality)
        self.assertEqual(x.variable_name, y.variable_name)
        self.assertEqual(x.key_letter, y.key_letter)
            
    def compare_SelectFromWhereNode(self, x, y):
        self.assertEqual(x.cardinality, y.cardinality)
        self.assertEqual(x.variable_name, y.variable_name)
        self.assertEqual(x.key_letter, y.key_letter)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_IfNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
        
    def compare_UnaryOperationNode(self, x, y):
        self.assertEqual(x.operator.lower(), y.operator.lower())
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
                   
    def compare_IndexAccessNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)

    def compare_VariableAccessNode(self, x, y):
        self.assertEqual(x.variable_name, y.variable_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_FieldAccessNode(self, x, y):
        self.assertEqual(x.name, y.name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
        
    def compare_SelfAccessNode(self, x, y):
        pass
            
    def compare_SelectedAccessNode(self, x, y):
        pass
    
    def compare_ParamAccessNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
    
    def compare_CreateEventNode(self, x, y):
        self.assertEqual(x.variable_name, y.variable_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_AssignmentNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
        
    def compare_ImplicitInvocationNode_with_BridgeInvocationNode(self, x, y):
        self.assertEqual(x.namespace, y.key_letter)
        self.assertEqual(x.action_name, y.action_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_InvocationStatementNode_with_MessageStatementNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_ImplicitInvocationNode(self, x, y):
        self.assertEqual(x.namespace, y.namespace)
        self.assertEqual(x.action_name, y.action_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_BridgeInvocationNode(self, x, y):
        self.assertEqual(x.key_letter, y.key_letter)
        self.assertEqual(x.action_name, y.action_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_OperationInvocationNode(self, x, y):
        self.assertEqual(x.action_name, y.action_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_FunctionInvocationNode(self, x, y):
        self.assertEqual(x.action_name, y.action_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_BooleanNode(self, x, y):
        self.assertEqual(x.value.lower(), y.value.lower())

    def compare_IntegerNode(self, x, y):
        self.assertEqual(x.value, y.value)

    def compare_RealNode(self, x, y):
        self.assertEqual(x.value, y.value)

    def compare_StringNode(self, x, y):
        self.assertEqual(x.value, y.value)

    def compare_EnumNode(self, x, y):
        self.assertEqual(x.namespace, y.namespace)
        self.assertEqual(x.name, y.name)
            
    def compare_ElIfListNode(self, x, y):
        self.assertEqual(len(x.children), len(y.children))
        for x, y in zip(x.children, y.children):
            self.compare(x, y)

    def compare_InvocationStatementNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_BinaryOperationNode(self, x, y):
        self.assertEqual(x.operator.lower(), y.operator.lower())
        for x, y in zip(x.children, y.children):
            self.compare(x, y)

    def compare_ElIfNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)

    def compare_RelateNode(self, x, y):
        self.assertEqual(x.from_variable_name, y.from_variable_name)
        self.assertEqual(x.to_variable_name, y.to_variable_name)
        self.assertEqual(x.rel_id.lower(), y.rel_id.lower())
        if None not in [x.phrase, y.phrase]:
            self.assertEqual(x.phrase, y.phrase)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)

    def compare_RelateUsingNode(self, x, y):
        self.assertEqual(x.from_variable_name, y.from_variable_name)
        self.assertEqual(x.to_variable_name, y.to_variable_name)
        self.assertEqual(x.using_variable_name, y.using_variable_name)
        self.assertEqual(x.rel_id.lower(), y.rel_id.lower())
        if None not in [x.phrase, y.phrase]:
            self.assertEqual(x.phrase, y.phrase)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_UnrelateNode(self, x, y):
        self.assertEqual(x.from_variable_name, y.from_variable_name)
        self.assertEqual(x.to_variable_name, y.to_variable_name)
        self.assertEqual(x.rel_id.lower(), y.rel_id.lower())
        if None not in [x.phrase, y.phrase]:
            self.assertEqual(x.phrase, y.phrase)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_UnrelateUsingNode(self, x, y):
        self.assertEqual(x.from_variable_name, y.from_variable_name)
        self.assertEqual(x.to_variable_name, y.to_variable_name)
        self.assertEqual(x.using_variable_name, y.using_variable_name)
        self.assertEqual(x.rel_id.lower(), y.rel_id.lower())
        if None not in [x.phrase, y.phrase]:
            self.assertEqual(x.phrase, y.phrase)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_ElseNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_DeleteNode(self, x, y):
        self.assertEqual(x.variable_name, y.variable_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_ControlNode(self, x, y):
        pass
            
    def compare_BreakNode(self, x, y):
        pass
    
    def compare_ContinueNode(self, x, y):
        pass
    
    def compare_ClassEventRecieverNode(self, x, y):
        self.assertEqual(x.key_letter, y.key_letter)
    
    def compare_CreatorEventRecieverNode(self, x, y):
        self.assertEqual(x.key_letter, y.key_letter)
    
    def compare_InstanceEventRecieverNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
    
    def compare_ForEachNode(self, x, y):
        self.assertEqual(x.instance_variable_name, y.instance_variable_name)
        self.assertEqual(x.set_variable_name, y.set_variable_name)
        for x, y in zip(x.children, y.children):
            self.compare(x, y)

    def compare_WhileNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)
            
    def compare_ReturnNode(self, x, y):
        for x, y in zip(x.children, y.children):
            self.compare(x, y)



class PrebuildFunctionTestCase(CompareAST):
    
    @classmethod
    def setUpClass(cls):
        cls.loader = ooaofooa.Loader()
        
    def setUp(self):
        self.metamodel = self.loader.build_metamodel()
        pe_pe = self.metamodel.new('PE_PE')
        s_sync = self.metamodel.new('S_SYNC')
        xtuml.relate(s_sync, pe_pe, 8001)
        
        s_dt = self.metamodel.select_any('S_DT', lambda sel: sel.Name == 'void')
        xtuml.relate(s_dt, s_sync, 25)
        
    def tearDown(self):
        del self.metamodel
        
    def prebuild_text(self, s):
        s_sync = self.metamodel.select_any('S_SYNC')
        s_sync.Action_Semantics_internal = s
        s_sync.Suc_Pars = 1
        
        prebuild.prebuild_model(self.metamodel)
        self.assertTrue(self.metamodel.is_consistent())
        
        generated_code = sourcegen.gen_text_action(s_sync)
        
        handwritten_ast = oal.parse(s)
        generated_ast = oal.parse(generated_code)

        self.compare(handwritten_ast, generated_ast)


def prebuild_docstring(f):
    
    def wrapper(self):
        self.prebuild_text(f.__doc__)
        f(self)
        
    return wrapper

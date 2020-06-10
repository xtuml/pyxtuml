#!/usr/bin/env python
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

import sys
import logging
import optparse
import functools

import xtuml

from bridgepoint import oal
from xtuml import where_eq as where

from functools import partial


logger = logging.getLogger(__name__)


class SymtabException(Exception):
    pass


class Block(dict):
    pass


class Scope(list):
    
    def __init__(self):
        self.append(Block())

    @property
    def symbols(self):
        return_symbols = dict()
        for d in self:
            return_symbols.update(d)
            
        return return_symbols.items()
    

class SymbolTable(object):
    domain = None
    
    def __init__(self, domain):
        self.domain = domain
        self._scopes = list()
        
    @property
    def scope_head(self):
        if not len(self._scopes): 
            raise SymtabException('Out of scope')
        
        return self._scopes[-1]
    
    def enter_scope(self):
        scope = Scope()
        self._scopes.append(scope)

    def leave_scope(self):
        if not len(self._scopes): 
            raise SymtabException('Out of scope')
        
        d = dict()
        for block in self._scopes.pop():
            d.update(block)
        return d
    
    def enter_block(self):        
        block = Block()
        self.scope_head.append(block)
    
    def leave_block(self):
        if not len(self.scope_head): 
            raise SymtabException('Out of block')
        
        block = self.scope_head.pop()
        del block
        
    def install_symbol(self, name, handle):
        for block in self.scope_head:
            if name in block:
                block[name] = handle
                return

        block = self.scope_head[-1]
        block[name] = handle

    def find_symbol(self, name, default=None):
        for block in self.scope_head:
            if name in block:
                return block[name]
        
        if default is not None:
            self.install_symbol(name, default)
            return default
        
        return self.domain.find_symbol(name)


class ReturnException(Exception):
    pass


class BreakException(Exception):
    pass


class ContinueException(Exception):
    pass


class StopException(Exception):
    pass


class NodePrintVisitor(xtuml.NodePrintVisitor):
    
    def default_render(self, node):
        if not node.position:
            return type(node).__name__
        
        return '%s (%d:%d)' % (type(node).__name__,
                               node.position.start_line,
                               node.position.start_column)


class ActionWalker(xtuml.Walker):
    domain = None
    return_value = None
    
    def __init__(self, domain):
        self.domain = domain
        self.symtab = SymbolTable(domain)
        xtuml.Walker.__init__(self)
    
    def accept(self, node, **kwargs):
        try:
            return xtuml.Walker.accept(self, node, **kwargs)
        except xtuml.MetaException as e:
            logger.error('%s:%d:%s' % (node.position.label,
                                       node.position.start_line,
                                       e))
            
    def default_accept(self, node, **kwargs):
        logger.error("%s:%d:%s '%s'" % (node.position.label,
                                        node.position.start_line,
                                       'unsupported statement',
                                        node.character_stream.splitlines()[0]))
            
    def accept_BodyNode(self, node):
        self.symtab.enter_scope()
        
        try:
            self.accept(node.block)
        except ReturnException:
            pass
        except StopException:
            pass
    
        self.symtab.leave_scope()
        
    def accept_BlockNode(self, node):
        self.symtab.enter_block()
        self.accept(node.statement_list)
        self.symtab.leave_block()
        
    def accept_StatementListNode(self, node):
        for child in node.children:
            self.accept(child)
        
    def accept_ReturnNode(self, node):
        value = self.accept(node.expression)
        self.return_value = value.fget()
        raise ReturnException()

    def accept_BreakNode(self, node):
        raise BreakException()
    
    def accept_ContinueNode(self, node):
        raise ContinueException()
    
    def accept_ControlNode(self, node):
        raise StopException()
    
    def accept_CreateObjectNode(self, node):
        inst = self.domain.new(node.key_letter)
        self.symtab.install_symbol(node.variable_name, inst)
        
    def accept_CreateObjectNoVariableNode(self, node):
        self.domain.new(node.key_letter)
    
    def accept_DeleteNode(self, node):
        inst = self.symtab.find_symbol(node.variable_name)
        xtuml.delete(inst)
    
    def accept_RelateNode(self, node):
        inst1 = self.symtab.find_symbol(node.from_variable_name)
        inst2 = self.symtab.find_symbol(node.to_variable_name)
        
        xtuml.relate(inst1, inst2, node.rel_id, node.phrase.replace("'", ''))
    
    def accept_RelateUsingNode(self, node):
        from_inst = self.symtab.find_symbol(node.from_variable_name)
        to_inst = self.symtab.find_symbol(node.to_variable_name)
        using_inst = self.symtab.find_symbol(node.using_variable_name)
        
        xtuml.relate(from_inst, using_inst, node.rel_id, node.phrase.replace("'", ''))
        xtuml.relate(using_inst, to_inst, node.rel_id, node.phrase.replace("'", ''))
        
    def accept_UnrelateNode(self, node):
        inst1 = self.symtab.find_symbol(node.from_variable_name)
        inst2 = self.symtab.find_symbol(node.to_variable_name)
        
        xtuml.unrelate(inst1, inst2, node.rel_id, node.phrase.replace("'", ''))
        
    def accept_UnrelateUsingNode(self, node):
        from_inst = self.symtab.find_symbol(node.from_variable_name)
        to_inst = self.symtab.find_symbol(node.to_variable_name)
        using_inst = self.symtab.find_symbol(node.using_variable_name)
        
        xtuml.unrelate(from_inst, using_inst, node.rel_id, node.phrase.replace("'", ''))
        xtuml.unrelate(using_inst, to_inst, node.rel_id, node.phrase.replace("'", ''))
        
    def accept_SelectFromNode(self, node):
        if node.cardinality == 'many':
            handle = self.domain.select_many(node.key_letter)
        else:
            handle = self.domain.select_any(node.key_letter)
        
        self.symtab.install_symbol(node.variable_name, handle)

    def accept_SelectedAccessNode(self, node):
        selected = self.symtab.find_symbol('selected')
        return property(lambda: selected)
    
    def accept_SelectFromWhereNode(self, node):
        def where(selected):
            self.symtab.enter_block()
            self.symtab.install_symbol('selected', selected)
            value = self.accept(node.where_clause)
            self.symtab.leave_block()
            return value.fget()
        
        if node.cardinality == 'many':
            handle = self.domain.select_many(node.key_letter, where)
        else:
            handle = self.domain.select_any(node.key_letter, where)
        
        self.symtab.install_symbol(node.variable_name, handle)
            
    def accept_SelectRelatedNode(self, node):
        handle = self.accept(node.handle).fget()
        if node.cardinality == 'many':
            chain = xtuml.navigate_many(handle)
        else:
            chain = xtuml.navigate_one(handle)
            
        for step in self.accept(node.navigation_chain):
            chain = step(chain)
        
        self.symtab.install_symbol(node.variable_name, chain())
    
    def accept_SelectRelatedWhereNode(self, node):
        def where(selected):
            self.symtab.enter_block()
            self.symtab.install_symbol('selected', selected)
            value = self.accept(node.where_clause)
            self.symtab.leave_block()
            return value.fget()
        
        handle = self.accept(node.handle).fget()
        if node.cardinality == 'many':
            chain = xtuml.navigate_many(handle)
        else:
            chain = xtuml.navigate_one(handle)
            
        for step in self.accept(node.navigation_chain):
            chain = step(chain)
        
        self.symtab.install_symbol(node.variable_name, chain(where))
        
    def accept_NavigationListNode(self, node):
        for child in node.children:
            yield self.accept(child)
            
    def accept_NavigationStepNode(self, node):
        return lambda chain: chain.nav(node.key_letter, node.rel_id, 
                                       node.phrase.replace("'", ''))

    def accept_ForEachNode(self, node):
        set_handle = self.symtab.find_symbol(node.set_variable_name)
        for handle in set_handle:
            self.symtab.install_symbol(node.instance_variable_name, handle)
            try:
                self.accept(node.block)
            except ContinueException:
                continue
            except BreakException:
                break
    
    def accept_IfNode(self, node):
        if self.accept(node.expression).fget():
            self.accept(node.block)
            
        elif not self.accept(node.elif_list):
            self.accept(node.else_clause)
    
    def accept_ElIfListNode(self, node):
        for child in node.children:
            if self.accept(child):
                return True
    
    def accept_ElIfNode(self, node):
        if self.accept(node.expression).fget():
            self.accept(node.block)
            return True
    
    def accept_ElseNode(self, node):
        self.accept(node.block)
    
    def accept_WhileNode(self, node):
        while self.accept(node.expression).fget():
            try:
                self.accept(node.block)
            except ContinueException:
                continue
            except BreakException:
                break
    
    def accept_AssignmentNode(self, node):
        value = self.accept(node.expression).fget()
        variable = self.accept(node.variable_access)
        variable.fset(value)
        
    def accept_FieldAccessNode(self, node):
        handle = self.accept(node.handle).fget()
        return property(fget=lambda: getattr(handle, node.name),
                        fset=lambda value: setattr(handle, node.name, value))
    
    def accept_IndexAccessNode(self, node, default=None):
        index = self.accept(node.expression).fget()
        handle = self.accept(node.handle, default=[default] * (index + 1)).fget()
        fget = lambda: handle[index]
        fset = lambda value: handle.__setitem__(index, value)
        return property(fget, fset)

    def accept_VariableAccessNode(self, node, default=None):
        fget = partial(self.symtab.find_symbol, node.variable_name, default=default)
        fset = partial(self.symtab.install_symbol, node.variable_name)
        return property(fget, fset)
    
    def accept_BinaryOperationNode(self, node):
        ops = {
            '+':   lambda lhs, rhs: (lhs + rhs),
            '-':   lambda lhs, rhs: (lhs - rhs),
            '*':   lambda lhs, rhs: (lhs * rhs),
            '/':   lambda lhs, rhs: (lhs / rhs),
            '%':   lambda lhs, rhs: (lhs % rhs),
            '<':   lambda lhs, rhs: (lhs < rhs),
            '<=':  lambda lhs, rhs: (lhs <= rhs),
            '>':   lambda lhs, rhs: (lhs > rhs),
            '>=':  lambda lhs, rhs: (lhs >= rhs),
            '!=':  lambda lhs, rhs: (lhs != rhs),
            '==':  lambda lhs, rhs: (lhs == rhs),
            'or':  lambda lhs, rhs: (lhs or  rhs),
            'and': lambda lhs, rhs: (lhs and rhs),
        }
        operator = node.operator.lower()
        
        left_value = self.accept(node.left).fget()
        right_value = self.accept(node.right).fget()
        value = ops[operator](left_value, right_value)
        
        return property(lambda: value)    
    
    def accept_UnaryOperationNode(self, node):
        ops = {
            '-':           lambda value: -value,
            '+':           lambda value: +value,
            'not':         lambda value: not value,
            'cardinality': lambda value: xtuml.cardinality(value),
            'empty':       lambda value: not value,
            'not_empty':   lambda value: not not value,
        }
        
        value = self.accept(node.operand).fget()
        operator = node.operator.lower()
        value = ops[operator](value)
        
        return property(lambda: value) 
    
    def accept_BooleanNode(self, node):
        value = node.value.upper() == 'TRUE'
        return property(lambda: value)
    
    def accept_IntegerNode(self, node):
        value = int(node.value)
        return property(lambda: value)
    
    def accept_RealNode(self, node):
        value = float(node.value)
        return property(lambda: value)
    
    def accept_StringNode(self, node):
        value = node.value[1:-1]
        return property(lambda: value)
    
    def accept_EnumOrNamedConstantNode(self, node):
        item = self.symtab.find_symbol(node.namespace)
        value = getattr(item, node.name)
        return property(lambda: value)
        
    def accept_InvocationStatementNode(self, node):
        return self.accept(node.invocation)
    
    def accept_ImplicitInvocationNode(self, node):
        kwargs = self.accept(node.parameter_list)
        item = self.symtab.find_symbol(node.namespace)
        fn = getattr(item, node.action_name)
        value = fn(**kwargs)
        return property(lambda: value)
            
    def accept_InstanceInvocationNode(self, node):
        inst = self.accept(node.handle).fget()
        op = getattr(inst.__class__, node.action_name)
        kwargs = self.accept(node.parameter_list)
        value = op(inst, **kwargs)
        return property(lambda: value)
    
    def accept_ClassInvocationNode(self, node):
        cls = self.symtab.find_symbol(node.key_letter)
        op = getattr(cls, node.action_name)
        kwargs = self.accept(node.parameter_list)
        value = op(**kwargs)
        return property(lambda: value)
    
    def accept_BridgeInvocationNode(self, node):
        kwargs = self.accept(node.parameter_list)
        ee = self.symtab.find_symbol(node.namespace)
        fn = getattr(ee, node.action_name)
        value = fn(**kwargs)
        return property(lambda: value)
        
    def accept_FunctionInvocationNode(self, node):
        kwargs = self.accept(node.parameter_list)
        fn = self.symtab.find_symbol(node.action_name)
        value = fn(**kwargs)
        return property(lambda: value)

    def accept_ParameterListNode(self, node):
        kwargs = dict()
        for child in node.children:
            value = self.accept(child.expression).fget()
            kwargs[child.name] = value
            
        return kwargs
    

class OperationWalker(ActionWalker):
    instance = None
    return_value = None
    
    def __init__(self, domain, kwargs, instance):
        self.kwargs = kwargs
        self.instance = instance
        ActionWalker.__init__(self, domain)

    def accept_ParamAccessNode(self, node):
        value = self.kwargs[node.variable_name]
        return property(lambda: value)
    
    def accept_SelfAccessNode(self, node):
        return property(lambda: self.instance)
    
    
def run_operation(metaclass, label, action, kwargs, inst):
    w = OperationWalker(metaclass.metamodel, kwargs, inst)
    #w.visitors.append(NodePrintVisitor())
    root = oal.parse(action, label)
    w.accept(root)
    return w.return_value


class DerivedAttributeWalker(ActionWalker):
    attribute_name = None
    instance = None
    return_value = None
        
    def __init__(self, domain, attribute_name, instance):
        self.attribute_name = attribute_name
        self.instance = instance
        ActionWalker.__init__(self, domain)

    def accept_SelfAccessNode(self, node):
        return property(lambda: self.instance)
    
    def accept_FieldAccessNode(self, node):
        inst = self.accept(node.handle).fget()
        if node.name == self.attribute_name and inst == self.instance:
            return property(fget=functools.partial(getattr, self, 'return_value'),
                            fset=functools.partial(setattr, self, 'return_value'))

        else:
            return property(fget=functools.partial(getattr, inst, node.name),
                            fset=functools.partial(setattr, inst, node.name))


def run_derived_attribute(metaclass, label, action, attribute_name, inst):
    w = DerivedAttributeWalker(metaclass.metamodel, attribute_name, inst)
    #w.visitors.append(NodePrintVisitor())
    root = oal.parse(action, label)
    w.accept(root)
    return w.return_value


class FunctionWalker(ActionWalker):
    return_value = None
    
    def __init__(self, domain, kwargs):
        self.kwargs = kwargs
        ActionWalker.__init__(self, domain)

    def accept_ParamAccessNode(self, node):
        value = self.kwargs[node.variable_name]
        return property(lambda: value)


def run_function(domain, label, action, kwargs):
    w = FunctionWalker(domain, kwargs)
    #w.visitors.append(NodePrintVisitor())
    root = oal.parse(action, label)
    w.accept(root)
    return w.return_value


def main():
    '''
    Parse command line options and launch the interpreter
    '''
    parser = optparse.OptionParser(usage="%prog [options] <model_path> [another_model_path..]",
                                   version=xtuml.version.complete_string,
                                   formatter=optparse.TitledHelpFormatter())

    parser.add_option("-v", "--verbosity", dest='verbosity', action="count",
                      default=1, help="increase debug logging level")
    
    parser.add_option("-f", "--function", dest='function', action="store",
                      help="invoke function named NAME", metavar='NAME')
    
    parser.add_option("-c", "--component", dest='component', action="store",
                      help="look for the function in a component named NAME",
                      metavar='NAME', default=None)
    
    (opts, args) = parser.parse_args()
    if len(args) == 0 or not opts.function:
        parser.print_help()
        sys.exit(1)
        
    levels = {
              0: logging.ERROR,
              1: logging.WARNING,
              2: logging.INFO,
              3: logging.DEBUG,
    }
    logging.basicConfig(level=levels.get(opts.verbosity, logging.DEBUG))
    
    from bridgepoint import ooaofooa
    mm = ooaofooa.load_metamodel(args)
    c_c = mm.select_any('C_C', where(Name=opts.component))
    domain = ooaofooa.mk_component(mm, c_c, derived_attributes=False)
    
    func = domain.find_symbol(opts.function)
    return func()


if __name__ == '__main__':
    rc = main()
    sys.exit(rc)


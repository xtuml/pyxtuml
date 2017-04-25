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
'''
Transform OAL actions from its textual form into instances in a the ooaofooa
metamodel.
'''

import logging
import optparse
import sys
import xtuml
import xtuml.tools

from xtuml import navigate_one as one
from xtuml import navigate_subtype as subtype
from xtuml import where_eq as where
from xtuml import unrelate

from bridgepoint import ooaofooa
from bridgepoint import oal


logger = logging.getLogger('bridgepoint.prebuild')


def relate(*args, **kwargs):
    assert xtuml.relate(*args, **kwargs)


def get_defining_component(pe_pe):
    '''
    get the C_C in which pe_pe is defined
    '''
    if pe_pe is None:
        return None
    
    if pe_pe.__class__.__name__ != 'PE_PE':
        pe_pe = xtuml.navigate_one(pe_pe).PE_PE[8001]()
    
    
    ep_pkg = xtuml.navigate_one(pe_pe).EP_PKG[8000]()
    if ep_pkg:
        return get_defining_component(ep_pkg)
    
    return xtuml.navigate_one(pe_pe).C_C[8003]()
    

class Scope(object):

    def __init__(self, handle=None):
        self.handle = handle
        self.symbols = dict()


class SymbolTable(object):
    
    def __init__(self):
        self.stack = list()
    
    def enter_scope(self, handle=None):
        s = Scope(handle)
        self.stack.append(s)
        
        return handle
        
    def leave_scope(self):
        s = self.stack.pop()
        return s.handle
    
    @property    
    def scope(self):
        return self.stack[-1].handle
       
    def find_symbol(self, name=None, kind=None):
        '''
        Find a symbol in the symbol table by name, kind, or both.
        '''
        for s in reversed(self.stack):
                        
            for symbol_name, handle in s.symbols.items():
                symbol_kind = handle.__class__.__name__
                
                if name == symbol_name and kind == symbol_kind:
                    return handle
                
                elif name is None and kind == handle.__class__.__name__:
                    return handle
                
                elif name == symbol_name and kind is None:
                    return handle
            
            if name is None and kind == s.handle.__class__.__name__:
                return s.handle
            
    def install_symbol(self, name, handle):
        self.stack[-1].symbols[name] = handle
        

class ConstantEvalutation(xtuml.tools.Walker):
    '''
    Simple walker for evaluating constant expressions expressed on ooaofooa.
    '''
    
    def accept_V_VAL(self, inst):
        return self.accept(subtype(inst, 801))
    
    def accept_V_LIN(self, inst):
        return int(inst.Value)
    
    def accept_V_BIN(self, inst):
        ops = {
            '+':   lambda lhs, rhs: (lhs + rhs),
            '-':   lambda lhs, rhs: (lhs - rhs),
            '*':   lambda lhs, rhs: (lhs * rhs),
            '/':   lambda lhs, rhs: (lhs / rhs)
        }

        lhs = self.accept(one(inst).V_VAL[802]())
        rhs = self.accept(one(inst).V_VAL[803]())
            
        return ops[inst.Operator](lhs, rhs)
    
    def accept_V_UNY(self, inst):
        ops = {
            '+':   lambda val: val,
            '-':   lambda val:-val,
        }

        value = self.accept(one(inst).V_VAL[804]())
            
        return ops[inst.Operator](value)
    
    def default_accept(self, node):
        logger.error('Unable to evaluate constant expression (%s)',
                     node.__class__.__name__)
        return 0


def eval_constant_expression(v_val):
    '''
    Evaluate a constant expression, e.g. for constant folding or for 
    calculating array sizes at compile-time.
    '''
    w = ConstantEvalutation()
    return w.accept(v_val)


class ActionPrebuilder(xtuml.tools.Walker):
    # TODO: Consider adding TerminalNode to better keep track of all posinfo
    m = None
    c_c = None
    symtab = None
    
    def __init__(self, metamodel, c_c=None):
        self.m = metamodel
        self.c_c = c_c
        self.symtab = SymbolTable()
        self.is_lvalue = False
        self.pe_pe_cache = xtuml.QuerySet()
        
        scope_filt = lambda sel: (ooaofooa.is_contained_in(sel, self.c_c) or
                                 ooaofooa.is_global(sel)) 
        
        self.pe_pe_cache |= self.m.select_many('PE_PE', scope_filt)
        
        xtuml.tools.Walker.__init__(self)        

    def any(self, key_letter, where_clause=None):
        return self.m.select_any(key_letter, where_clause)
    
    def one(self, key_letter, where_clause=None):
        return self.m.select_one(key_letter, where_clause)
    
    def many(self, key_letter, where_clause=None):
        return self.m.select_many(key_letter, where_clause)
            
    def new(self, *args, **kwargs):
        return self.m.new(*args, **kwargs)
    
    def o_obj(self, key_letter):            
        return one(self.pe_pe_cache).O_OBJ[8001](where(Key_Lett=key_letter))
    
    def s_sync(self, action_name):
        return one(self.pe_pe_cache).S_SYNC[8001](where(Name=action_name))
    
    def s_ee(self, key_letter):
        return one(self.pe_pe_cache).S_EE[8001](where(Key_Lett=key_letter))
    
    def r_rel(self, rel_id):
        where_clause = lambda sel: 'r%d' % sel.Numb == rel_id.lower()
        return self.any('R_REL', where_clause)
    
    def cnst_syc(self, name):
        where_clause = lambda sel:(ooaofooa.is_contained_in(sel, self.c_c) or
                                            ooaofooa.is_global(sel))
        
        cnst_csp = self.many('CNST_CSP', where_clause)
        return one(cnst_csp).CNST_SYC[1504](where(Name=name))

    
    def v_val(self, node, **kwargs):
        act_blk = self.symtab.find_symbol(kind='ACT_BLK')
        v_val = self.new('V_VAL',
                         LineNumber=node.position.start_line,
                         StartPosition=node.position.start_column,
                         EndPosition=node.position.end_column,
                         **kwargs)
        
        relate(v_val, act_blk, 826)
        
        return v_val
    
    def v_var(self, node, **kwargs):
        act_blk = self.symtab.find_symbol(kind='ACT_BLK')
        v_var = self.new('V_VAR', **kwargs)
        v_loc = self.new('V_LOC',
                         LineNumber=node.position.start_line,
                         StartPosition=node.position.start_column,
                         EndPosition=node.position.end_column)
        
        relate(v_var, act_blk, 823)
        relate(v_var, v_loc, 835)
        
        return v_var
    
    def v_int(self, node, name, o_obj):
        s_dt = self.s_dt('inst_ref<Object>')
        v_var = self.v_var(node, Name=name)
        v_int = self.new('V_INT')  # TODO: V_INT.IsImplicitInFor
        
        relate(v_var, s_dt, 848)
        relate(v_var, v_int, 814)
        relate(o_obj, v_int, 818)
        
        # TODO: install symbol in v_var instead
        self.symtab.install_symbol(v_var.Name, v_var)
        
        return v_int
        
    def v_ins(self, node, name, o_obj):
        s_dt = self.s_dt('inst_ref_set<Object>')
        v_var = self.v_var(node, Name=name)
        v_ins = self.new('V_INS')
        
        relate(v_var, s_dt, 848)
        relate(v_var, v_ins, 814)
        relate(o_obj, v_ins, 819)
        
        # TODO: install symbol in v_var instead
        self.symtab.install_symbol(v_var.Name, v_var)
        
        return v_ins
    
    def v_trn(self, node, name):
        v_var = self.v_var(node, Name=name)
        v_trn = self.new('V_TRN')
        
        relate(v_var, v_trn, 814)
        # NOTE: V_TRN data type is related when assigned a value
        
        # TODO: install symbol in v_var instead
        self.symtab.install_symbol(v_var.Name, v_var)
        
        return v_trn
    
    def v_isr(self, node, name):
        s_dt = self.s_dt('inst_ref_set<Object>')
        v_var = self.find_symbol(node, name)
        v_val = self.v_val(node)
        v_isr = self.new('V_ISR')
        
        relate(v_isr, v_val, 801)
        relate(v_isr, v_var, 809)
        relate(v_val, s_dt, 820)
        
        return v_isr
    
    def v_irf(self, node, name):
        s_dt = self.s_dt('inst_ref<Object>')
        v_var = self.find_symbol(node, name)
        v_val = self.v_val(node)
        v_irf = self.new('V_IRF')
        
        relate(v_irf, v_val, 801)
        relate(v_irf, v_var, 808)
        relate(v_val, s_dt, 820)
        
        return v_irf

    def v_avl(self, node, o_attr, root_v_val):
        s_dt = one(o_attr).S_DT[114]()
            
        v_val = self.v_val(node)
        v_avl = self.new('V_AVL')
            
        relate(v_val, s_dt, 820)
        relate(v_avl, v_val, 801)
        relate(v_avl, root_v_val, 807)
        relate(v_avl, o_attr, 806)
        
        return v_avl
    
    def v_mvl(self, node, s_mbr, root_v_val):
        v_val = self.v_val(node)
        s_dt = one(s_mbr).S_DT[45]()
        
        v_mvl = self.new('V_MVL')
        
        relate(v_val, s_dt, 820)
        relate(v_mvl, v_val, 801)
        relate(v_mvl, root_v_val, 837)
        relate(v_mvl, s_mbr, 836)
        
        return v_mvl
    
    def e_gsme(self, node, sm_evt):
        act_smt = self.act_smt(node)
        
        e_ess = self.new('E_ESS')
        e_ges = self.new('E_GES')
        e_gsme = self.new('E_GSME')

        relate(act_smt, e_ess, 603)
        relate(e_ess, e_ges, 701)
        relate(e_ges, e_gsme, 703)
        relate(e_gsme, sm_evt, 707)

        for v_par in self.accept(node.event_specification.event_data):
            relate(v_par, e_ess, 700)
            
        return e_gsme
    
    def e_csme(self, node, sm_evt, v_var, implicit):
        act_smt = self.act_smt(node)
        
        e_ess = self.new('E_ESS')
        e_ces = self.new('E_CES', is_implicit=implicit)
        e_csme = self.new('E_CSME')
        
        relate(act_smt, e_ess, 603)
        relate(e_ess, e_ces, 701)
        relate(e_ces, e_csme, 702)
        relate(e_ces, v_var, 710)
        relate(e_csme, sm_evt, 706)

        for v_par in self.accept(node.event_specification.event_data):
            relate(v_par, e_ess, 700)
            
        return e_csme
    
    def act_smt(self, node):
        act_blk = self.symtab.find_symbol(kind='ACT_BLK')
        act_smt = self.new('ACT_SMT')
        
        act_smt.LineNumber = node.position.start_line
        act_smt.StartPosition = node.position.start_column
        act_smt.EndPosition = node.position.end_column
        act_smt.Label = node.character_stream
        
        relate(act_blk, act_smt, 602)
        
        return act_smt
    
    def act_sel(self, node):
        act_smt = self.act_smt(node)
        act_lnk = act_lnk_start = act_lnk_end = self.accept(node.navigation_chain)
        
        while act_lnk:
            act_lnk_end = act_lnk
            act_lnk = one(act_lnk).ACT_LNK[604, 'succeeds']()
            
        v_val = self.accept(node.handle)
        
        # resulting variable
        v_var = self.find_symbol(node, node.variable_name)
        implicit = v_var is None
        if implicit:
            o_obj = one(act_lnk_end).O_OBJ[678]()
            if node.many:
                v_ins = self.v_ins(node, node.variable_name, o_obj)
                v_var = one(v_ins).V_VAR[814]()
            else:
                v_int = self.v_int(node, node.variable_name, o_obj)
                v_var = one(v_int).V_VAR[814]()
        
        act_sel = self.new('ACT_SEL',
                           is_implicit=implicit,
                           cardinality=node.cardinality)
        
        relate(act_sel, act_smt, 603)
        relate(act_sel, act_lnk_start, 637)
        relate(act_sel, v_val, 613)
        relate(act_sel, v_var, 638)
        
        return act_sel
    
    def s_dt(self, name):
        return self.any('S_DT', where(Name=name))
    
    def find_symbol(self, node, name):
        # TODO: introduce a new keyword SENDER, and SenderAccessNode?
        v_var = self.symtab.find_symbol(name)
        if not v_var and name.lower() == 'sender':
            v_trn = self.v_trn(node, 'sender')
            v_var = one(v_trn).V_VAR[814]()
            s_dt = self.s_dt('component_ref')
            relate(v_var, s_dt, 848)
            
        return v_var
            
    def default_accept(self, node, **kwargs):
        sys.stderr.write(node.__class__.__name__ + '\n')
            
    def accept_BodyNode(self, node):
        act_blk = self.new('ACT_BLK')
        relate(act_blk, self.act_act, 666)
        relate(act_blk, self.act_act, 601)
        
        self.symtab.enter_scope(act_blk)
        self.accept(node.block.statement_list)
        self.symtab.leave_scope()
        
        return self.act_act
    
    def accept_BlockNode(self, node):
        act_blk = self.new('ACT_BLK')
        
        relate(act_blk, self.act_act, 601)
        
        self.symtab.enter_scope(act_blk)
        self.accept(node.statement_list)
        self.symtab.leave_scope()
        
        return act_blk
        
    def accept_StatementListNode(self, node):
        prev = None
        for child in node.children:
            act_smt = self.accept(child)
            xtuml.relate(prev, act_smt, 661, 'succeeds')
            prev = act_smt
        
    def accept_ReturnNode(self, node):
        act_smt = self.act_smt(node)
        act_ret = self.new('ACT_RET')
        v_val = self.accept(node.expression)
        
        relate(act_ret, act_smt, 603)
        xtuml.relate(act_ret, v_val, 668)
        
        return act_smt

    def accept_BreakNode(self, node):
        act_smt = self.act_smt(node)
        act_brk = self.new('ACT_BRK')
        
        relate(act_brk, act_smt, 603)
        
        return act_smt
    
    def accept_ContinueNode(self, node):
        act_smt = self.act_smt(node)
        act_con = self.new('ACT_CON')
        
        relate(act_con, act_smt, 603)
        
        return act_smt
    
    def accept_ControlNode(self, node):
        act_smt = self.act_smt(node)
        act_ctl = self.new('ACT_CTL')
        
        relate(act_ctl, act_smt, 603)
        
        return act_smt
    
    def accept_CreateObjectNode(self, node):
        act_smt = self.act_smt(node)
        o_obj = self.o_obj(node.key_letter)
        v_var = self.find_symbol(node, node.variable_name)
        
        implicit = v_var is None
        if implicit:
            v_int = self.v_int(node, node.variable_name, o_obj)
            v_var = one(v_int).V_VAR[814]()
        
        act_cr = self.new('ACT_CR', is_implicit=implicit)
        
        relate(act_cr, act_smt, 603)
        relate(act_cr, v_var, 633)
        relate(act_cr, o_obj, 671)
        
        return act_smt
    
    def accept_CreateObjectNoVariableNode(self, node):
        act_smt = self.act_smt(node)
        o_obj = self.o_obj(node.key_letter)

        act_cnv = self.new('ACT_CNV')
        
        relate(act_cnv, act_smt, 603)
        relate(act_cnv, o_obj, 672)
        
        return act_smt
    
    def accept_DeleteNode(self, node):
        act_smt = self.act_smt(node)
        v_var = self.find_symbol(node, node.variable_name)
        
        act_del = self.new('ACT_DEL')
        
        relate(act_del, act_smt, 603)
        relate(act_del, v_var, 634)
        
        return act_smt
    
    def accept_RelateNode(self, node):
        act_smt = self.act_smt(node)
        v_var_from = self.find_symbol(node, node.from_variable_name)
        v_var_to = self.find_symbol(node, node.to_variable_name)
        r_rel = self.r_rel(node.rel_id)

        act_rel = self.new('ACT_REL', relationship_phrase=node.phrase)
        
        relate(act_rel, act_smt, 603)
        relate(act_rel, v_var_from, 615)
        relate(act_rel, v_var_to, 616)
        relate(act_rel, r_rel, 653)
        
        return act_smt
    
    def accept_RelateUsingNode(self, node):
        act_smt = self.act_smt(node)
        v_var_from = self.find_symbol(node, node.from_variable_name)
        v_var_to = self.find_symbol(node, node.to_variable_name)
        v_var_using = self.find_symbol(node, node.using_variable_name)
        r_rel = self.r_rel(node.rel_id)

        act_ru = self.new('ACT_RU', relationship_phrase=node.phrase)
        
        relate(act_ru, act_smt, 603)
        relate(act_ru, v_var_from, 617)
        relate(act_ru, v_var_to, 618)
        relate(act_ru, v_var_using, 619)
        relate(act_ru, r_rel, 654)
        
        return act_smt
    
    def accept_UnrelateNode(self, node):
        act_smt = self.act_smt(node)
        v_var_from = self.find_symbol(node, node.from_variable_name)
        v_var_to = self.find_symbol(node, node.to_variable_name)
        r_rel = self.r_rel(node.rel_id)
        
        act_unr = self.new('ACT_UNR', relationship_phrase=node.phrase)
        
        relate(act_unr, act_smt, 603)
        relate(act_unr, v_var_from, 620)
        relate(act_unr, v_var_to, 621)
        relate(act_unr, r_rel, 655)
        
        return act_smt
    
    def accept_UnrelateUsingNode(self, node):
        act_smt = self.act_smt(node)
        v_var_from = self.find_symbol(node, node.from_variable_name)
        v_var_to = self.find_symbol(node, node.to_variable_name)
        v_var_using = self.find_symbol(node, node.using_variable_name)
        r_rel = self.r_rel(node.rel_id)
        
        act_uru = self.new('ACT_URU', relationship_phrase=node.phrase)
        
        relate(act_uru, act_smt, 603)
        relate(act_uru, v_var_from, 622)
        relate(act_uru, v_var_to, 623)
        relate(act_uru, v_var_using, 624)
        relate(act_uru, r_rel, 656)
        
        return act_smt
    
    def accept_SelectFromNode(self, node):
        act_smt = self.act_smt(node)
        v_var = self.find_symbol(node, node.variable_name)
        o_obj = self.o_obj(node.key_letter)

        implicit = v_var is None
        if implicit:
            if node.many:
                v_ins = self.v_ins(node, node.variable_name, o_obj)
                v_var = one(v_ins).V_VAR[814]()
            else:
                v_int = self.v_int(node, node.variable_name, o_obj)
                v_var = one(v_int).V_VAR[814]()
            
        act_fio = self.new('ACT_FIO',
                           is_implicit=implicit,
                           cardinality=node.cardinality)
        
        relate(act_fio, act_smt, 603)
        relate(act_fio, v_var, 639)
        relate(act_fio, o_obj, 677)
        
        return act_smt
    
    def accept_SelectFromWhereNode(self, node):
        act_smt = self.act_smt(node)
        v_var = self.find_symbol(node, node.variable_name)
        o_obj = self.o_obj(node.key_letter)
        
        self.symtab.enter_scope(o_obj)
        v_val = self.accept(node.where_clause)
        self.symtab.leave_scope()
        
        implicit = v_var is None
        if implicit:
            if node.many:
                v_ins = self.v_ins(node, node.variable_name, o_obj)
                v_var = one(v_ins).V_VAR[814]()
            else:
                v_int = self.v_int(node, node.variable_name, o_obj)
                v_var = one(v_int).V_VAR[814]()
            
        act_fiw = self.new('ACT_FIW',
                           is_implicit=implicit,
                           cardinality=node.cardinality)
        
        relate(act_fiw, act_smt, 603)
        relate(act_fiw, v_var, 665)
        relate(act_fiw, o_obj, 676)
        relate(act_fiw, v_val, 610)
        
        return act_smt
    
    def accept_SelectRelatedNode(self, node):
        act_sel = self.act_sel(node)
        act_sr = self.new('ACT_SR')
        
        relate(act_sr, act_sel, 664)
        
        return one(act_sel).ACT_SMT[603]()
    
    def accept_SelectRelatedWhereNode(self, node):
        act_sel = self.act_sel(node)
        o_obj = (one(act_sel).V_VAR[638].V_INT[814].O_OBJ[818]() or
                 one(act_sel).V_VAR[638].V_INS[814].O_OBJ[819]())
        act_srw = self.new('ACT_SRW')

        self.symtab.enter_scope(o_obj)
        v_val = self.accept(node.where_clause)    
        self.symtab.leave_scope()
        
        relate(act_srw, act_sel, 664)
        relate(act_srw, v_val, 611)
        
        return one(act_sel).ACT_SMT[603]()
    
    def accept_NavigationListNode(self, node):
        prev = None
        for child in reversed(node.children):
            act_lnk = self.accept(child)
            xtuml.relate(prev, act_lnk, 604, 'succeeds')
            prev = act_lnk
        
        return prev
    
    def accept_NavigationStepNode(self, node):
        r_rel = self.r_rel(node.rel_id)
        o_obj = self.o_obj(node.key_letter)
        
        # TODO: set the Multiplicity correctly
        act_lnk = self.new('ACT_LNK', Mult=2, Rel_Phrase=node.phrase)
        
        relate(act_lnk, r_rel, 681)
        relate(act_lnk, o_obj, 678)
        
        return act_lnk

    def accept_ForEachNode(self, node):
        act_smt = self.act_smt(node)
        v_var = self.find_symbol(node, node.instance_variable_name)
        v_var_set = self.find_symbol(node, node.set_variable_name)
        o_obj = one(v_var_set).V_INS[814].O_OBJ[819]()

        # NOTE: the loop variable is intentionally declared outside the loop scope
        implicit = v_var is None
        if implicit:
            v_int = self.v_int(node, node.instance_variable_name, o_obj)
            v_var = one(v_int).V_VAR[814]()
            
        act_blk = self.accept(node.block)
        act_for = self.new('ACT_FOR', is_implicit=implicit)
        
        relate(act_for, act_smt, 603)
        relate(act_for, act_blk, 605)
        relate(act_for, v_var, 614)
        relate(act_for, v_var_set, 652)
        relate(act_for, o_obj, 670)
        
        return act_smt
    
    def accept_IfNode(self, node):
        act_smt = self.act_smt(node)
        v_val = self.accept(node.expression)
        act_blk = self.accept(node.block)
        
        act_if = self.new('ACT_IF')
        
        relate(act_if, act_smt, 603)
        relate(act_if, act_blk, 607)
        relate(act_if, v_val, 625)
        
        self.accept(node.elif_list, act_if=act_if)
        self.accept(node.else_clause, act_if=act_if)

        return act_smt
    
    def accept_ElIfListNode(self, node, act_if=None):
        for child in node.children:
            self.accept(child, act_if=act_if)
    
    def accept_ElIfNode(self, node, act_if):
        act_smt = self.act_smt(node)
        v_val = self.accept(node.expression)
        act_blk = self.accept(node.block)
        
        act_el = self.new('ACT_EL')
        
        relate(act_el, act_smt, 603)
        relate(act_el, act_blk, 658)
        relate(act_el, v_val, 659)
        relate(act_el, act_if, 682)
        
        return act_smt
    
    def accept_ElseNode(self, node, act_if):
        act_smt = self.act_smt(node)
        act_blk = self.accept(node.block)
        
        act_e = self.new('ACT_E')
        
        relate(act_e, act_smt, 603)
        relate(act_e, act_blk, 606)
        relate(act_e, act_if, 683)
        
        return act_smt
    
    def accept_WhileNode(self, node):
        act_smt = self.act_smt(node)
        v_val = self.accept(node.expression)
        act_blk = self.accept(node.block)
        
        act_whl = self.new('ACT_WHL')
        
        relate(act_whl, act_smt, 603)
        relate(act_whl, act_blk, 608)
        relate(act_whl, v_val, 626)
        
        return act_smt
    
    def accept_AssignmentNode(self, node):
        act_smt = self.act_smt(node)
        v_val_r = self.accept(node.expression)
        self.is_lvalue = True
        v_val_l = self.accept(node.variable_access)
        v_val_l.isLValue = True
        self.is_lvalue = False
        
        # Set the type of implicitly defined variables
        v_tvl = one(v_val_l).V_TVL[801]()
        v_aer = one(v_val_l).V_AER[801]()
        v_var = one(v_tvl).V_VAR[805]()
        s_dt = one(v_val_r).S_DT[820]()

        v_aer_list = list()
        while v_aer:
            v_aer_list.append(v_aer)
            v_val = one(v_aer).V_VAL[838]()
            v_tvl = one(v_val).V_TVL[801]()
            v_var = one(v_tvl).V_VAR[805]()
            v_aer = one(v_val).V_AER[801]()
            if not one(v_val).S_DT[820]():
                relate(v_val, s_dt, 820)

        if v_var and not v_var.Declared:
            v_var.Declared = True
            s_dt = one(v_val_r).S_DT[820]()
            relate(v_var, s_dt, 848)
            relate(v_val_l, s_dt, 820)
            
            for idx, v_aer in enumerate(reversed(v_aer_list)):
                v_val_index = one(v_aer).V_VAL[839]()
                element_count = eval_constant_expression(v_val_index) + 1
                s_dim = self.new('S_DIM', elementCount=element_count, dimensionCount=idx)
                relate(v_var, s_dim, 849)
                
            v_trn = one(v_var).V_TRN[814]()
            v_irf = one(v_val_r).V_IRF[801]()
            v_isr = one(v_val_r).V_ISR[801]()
            s_irdt = one(s_dt).S_IRDT[17]()
            
            # migrate Transient Variable (V_TRN) to Instance Handle (V_INT)
            def migrate_instance(o_obj):
                v_int = self.new('V_INT')
                relate(o_obj, v_int, 818)
                
                unrelate(v_var, v_trn, 814)
                relate(v_var, v_int, 814)
                xtuml.delete(v_trn)
                
                v_irf = self.m.new('V_IRF')
                
                unrelate(v_val_l, v_tvl, 801)
                relate(v_val_l, v_irf, 801)
                
                unrelate(v_var, v_tvl, 805)
                relate(v_var, v_irf, 808)
                xtuml.delete(v_tvl)
            
            # migrate Transient Variable (V_TRN) to Instance Set (V_INS)
            def migrate_instance_set(o_obj):
                v_ins = self.new('V_INS')
                relate(o_obj, v_ins, 819)
                
                unrelate(v_var, v_trn, 814)
                relate(v_var, v_ins, 814)
                xtuml.delete(v_trn)
                
                v_isr = self.m.new('V_ISR')
                
                unrelate(v_val_l, v_tvl, 801)
                relate(v_val_l, v_isr, 801)
                
                unrelate(v_var, v_tvl, 805)
                relate(v_var, v_isr, 809)
                
                xtuml.delete(v_tvl)
            
            if v_trn and s_irdt:
                o_obj = one(s_irdt).O_OBJ[123]()
                if s_irdt.isSet:
                    migrate_instance_set(o_obj)
                else:
                    migrate_instance(o_obj)
                
            elif v_trn and v_irf:
                o_obj = one(v_irf).V_VAR[808].V_INT[814].O_OBJ[818]()
                migrate_instance(o_obj)
            
            elif v_trn and v_isr:
                o_obj = one(v_isr).V_VAR[809].V_INS[814].O_OBJ[819]()
                migrate_instance_set(o_obj)
            
        act_ai = self.new('ACT_AI')

        relate(act_ai, act_smt, 603)
        relate(act_ai, v_val_r, 609)
        relate(act_ai, v_val_l, 689)
        
        return act_smt
        
    def accept_FieldAccessNode(self, node):
        root_v_val = self.accept(node.handle)
        inst = subtype(root_v_val, 801)
        kind = inst.__class__.__name__

        s_dt = one(root_v_val).S_DT[820]()
        while one(s_dt).S_UDT[17]():
            s_dt = one(s_dt).S_UDT[17].S_DT[18]()
        
        if one(s_dt).S_IRDT[17]():
            o_obj = one(s_dt).S_IRDT[17].O_OBJ[123]()
            o_attr = one(o_obj).O_ATTR[102](where(Name=node.name))
            v_avl = self.v_avl(node, o_attr, root_v_val)
            return one(v_avl).V_VAL[801]()

        elif kind == 'V_SLR':
            o_obj = self.symtab.find_symbol(kind='O_OBJ')
            o_attr = one(o_obj).O_ATTR[102](where(Name=node.name))
            v_avl = self.v_avl(node, o_attr, root_v_val)
            return one(v_avl).V_VAL[801]()
            
        elif kind == 'V_IRF':
            o_obj = one(inst).V_VAR[808].V_INT[814].O_OBJ[818]()
            o_attr = one(o_obj).O_ATTR[102](where(Name=node.name))
            v_avl = self.v_avl(node, o_attr, root_v_val)
            return one(v_avl).V_VAL[801]()
            
        else:
            s_mbr = one(s_dt).S_SDT[17].S_MBR[44](where(Name=node.name))
            if s_mbr:
                v_mvl = self.v_mvl(node, s_mbr, root_v_val)
                return one(v_mvl).V_VAL[801]()
        
        # Assume its an array.length access
        if node.name == 'length':
            v_val = self.v_val(node)
            s_dt = self.s_dt('integer')
            v_alv = self.new('V_ALV')
                
            relate(v_val, s_dt, 820)
            relate(v_val, v_alv, 801)
            relate(v_alv, root_v_val, 840)
                
            return v_val
    
    def accept_IndexAccessNode(self, node):
        v_val_root = self.accept(node.handle)
        v_val_index = self.accept(node.expression)
        s_dt = one(v_val_root).S_DT[820]()
        v_val = self.v_val(node)
        v_aer = self.new('V_AER')
        
        if s_dt:
            relate(v_val, s_dt, 820)
            
        relate(v_aer, v_val, 801)
        relate(v_aer, v_val_root, 838)
        relate(v_aer, v_val_index, 839)
        
        return v_val
    
    def accept_SelectedAccessNode(self, node):
        s_dt = self.s_dt('inst_ref<Object>')
        v_val = self.v_val(node)
        v_slr = self.new('V_SLR')
        
        relate(v_val, s_dt, 820)
        relate(v_val, v_slr, 801)
        
        return v_val
    
    def accept_SelfAccessNode(self, node):
        v_var = self.find_symbol(node, 'self')
        s_dt = one(v_var).S_DT[848]()
        v_val = self.v_val(node)
        
        v_irf = self.new('V_IRF')

        relate(v_val, s_dt, 820)
        relate(v_val, v_irf, 801)
        relate(v_var, v_irf, 808)
        
        return v_val

    def accept_VariableAccessNode(self, node):
        v_var = self.find_symbol(node, name=node.variable_name)
        if not v_var:
            cnst_syc = self.cnst_syc(node.variable_name)
            if cnst_syc:
                v_val = self.v_val(node)
                s_dt = one(cnst_syc).S_DT[1500]()
                v_scv = self.new('V_SCV')
                relate(v_val, v_scv, 801)
                relate(v_val, s_dt, 820)
                relate(v_scv, cnst_syc, 850)
            elif self.is_lvalue:
                v_trn = self.v_trn(node, node.variable_name)
                v_var = one(v_trn).V_VAR[814]()
                v_val = self.v_val(node, isImplicit=True)
                v_tvl = self.new('V_TVL')
            
                relate(v_tvl, v_val, 801)
                relate(v_tvl, v_var, 805)
            else:
                raise Exception("Unknown transient '%s'" % node.variable_name)
            
        elif one(v_var).V_INT[814]():
            v_irf = self.v_irf(node, node.variable_name)
            v_val = one(v_irf).V_VAL[801]()
            
        elif one(v_var).V_INS[814]():
            v_isr = self.v_isr(node, node.variable_name)
            v_val = one(v_isr).V_VAL[801]()
            
        elif one(v_var).V_TRN[814]():
            s_dt = one(v_var).S_DT[848]()
            v_val = self.v_val(node)
            v_tvl = self.new('V_TVL')
            
            relate(v_tvl, v_val, 801)
            relate(v_val, s_dt, 820)
            relate(v_tvl, v_var, 805)
        
        return v_val
    
    def accept_BinaryOperationNode(self, node):
        # TODO: coersion and/or casting of binops??
        # Perhaps that is up the the model compiler???
        v_val_l = self.accept(node.left)
        v_val_r = self.accept(node.right)

        if node.operator.lower() in ['<', '<=', '==', '!=', '>=', '>',
                                     'and', 'or']:
            s_dt = self.s_dt('boolean')
        else:
            s_dt = one(v_val_l).S_DT[820]()
        
        v_val = self.v_val(node)
        v_bin = self.new('V_BIN', Operator=node.operator.lower())
        
        relate(v_val, s_dt, 820)
        relate(v_bin, v_val, 801)
        relate(v_bin, v_val_l, 802)
        relate(v_bin, v_val_r, 803)
        
        return v_val
    
    def accept_UnaryOperationNode(self, node):
        v_val_op = self.accept(node.operand)
        operator = node.operator.lower()
        
        if operator in ['not', 'empty', 'not_empty']:
            s_dt = self.s_dt('boolean')
            
        elif operator == 'cardinality':
            s_dt = self.s_dt('integer')
            
        else:
            s_dt = one(v_val_op).S_DT[820]()
        
        v_val = self.v_val(node)
        v_uny = self.new('V_UNY', Operator=node.operator.lower())
        
        relate(v_val, s_dt, 820)
        relate(v_uny, v_val, 801)
        relate(v_uny, v_val_op, 804)
        
        return v_val
    
    def accept_BooleanNode(self, node):
        s_dt = self.s_dt('boolean')
        v_val = self.v_val(node)
        v_lbo = self.new('V_LBO', Value=str(node.value).upper())
        
        relate(v_val, s_dt, 820)
        relate(v_lbo, v_val, 801)
        
        return v_val
    
    def accept_IntegerNode(self, node):
        s_dt = self.s_dt('integer')
        v_val = self.v_val(node)
        v_lin = self.new('V_LIN', Value=node.value)
        
        relate(v_val, s_dt, 820)
        relate(v_lin, v_val, 801)
        
        return v_val
    
    def accept_RealNode(self, node):
        s_dt = self.s_dt('real')
        v_val = self.v_val(node,)
        v_lrl = self.new('V_LRL', Value=node.value)
        
        relate(v_val, s_dt, 820)
        relate(v_lrl, v_val, 801)
        
        return v_val
    
    def accept_StringNode(self, node):
        s_dt = self.s_dt('string')
        v_val = self.v_val(node)
        v_lst = self.new('V_LST', Value=node.value[1:-1])
        
        relate(v_val, s_dt, 820)
        relate(v_lst, v_val, 801)
        
        return v_val
    
    def accept_EnumNode(self, node):
        s_dt = self.s_dt(node.namespace)
        while one(s_dt).S_UDT[17]():
            s_dt = one(s_dt).S_UDT[17].S_DT[18]()
            
        s_enum = one(s_dt).S_EDT[17].S_ENUM[27](where(name=node.name))
        v_val = self.v_val(node)
        v_len = self.new('V_LEN')
        
        relate(v_val, s_dt, 820)
        relate(v_len, v_val, 801)
        relate(v_len, s_enum, 824)
        
        return v_val
    
    def accept_GenerateClassEventNode(self, node):
        act_smt = self.act_smt(node)
        
        evt_filter = lambda sel: (sel.Drv_Lbl == node.event_specification.identifier or
                                  sel.Drv_Lbl == node.event_specification.identifier + '*')
                                  
        o_obj = self.o_obj(node.key_letter)
        sm_evt = one(o_obj).SM_ASM[519].SM_SM[517].SM_EVT[502](evt_filter)
        
        e_ess = self.new('E_ESS')
        e_ges = self.new('E_GES')
        e_gsme = self.new('E_GSME')
        e_gar = self.new('E_GAR')

        relate(act_smt, e_ess, 603)
        relate(e_ess, e_ges, 701)
        relate(e_ges, e_gsme, 703)
        relate(e_gsme, e_gar, 705)
        relate(e_gsme, sm_evt, 707)   
        
        for v_par in self.accept(node.event_specification.event_data):
            relate(v_par, e_ess, 700)
            
        return act_smt
    
    def accept_GenerateCreatorEventNode(self, node):
        o_obj = self.o_obj(node.key_letter)
        evt_filter = lambda sel: (sel.Drv_Lbl == node.event_specification.identifier or
                                  sel.Drv_Lbl == node.event_specification.identifier + '*')
        sm_evt = one(o_obj).SM_ISM[518].SM_SM[517].SM_EVT[502](evt_filter)
        
        e_gsme = self.e_gsme(node, sm_evt)
        e_gec = self.new('E_GEC')

        relate(e_gsme, e_gec, 705)
            
        return one(e_gsme).E_GES[703].E_ESS[701].ACT_SMT[603]()
    
    def accept_GenerateInstanceEventNode(self, node):
        v_var = self.find_symbol(node, name=node.variable_name)
        o_obj = one(v_var).V_INT[814].O_OBJ[818]()
        evt_filter = lambda sel: (sel.Drv_Lbl == node.event_specification.identifier or
                                  sel.Drv_Lbl == node.event_specification.identifier + '*')
        
        sm_evt = one(o_obj).SM_ISM[518].SM_SM[517].SM_EVT[502](evt_filter)
        e_gsme = self.e_gsme(node, sm_evt)
        e_gen = self.new('E_GEN')

        relate(e_gsme, e_gen, 705)
        relate(e_gen, v_var, 712)
        
        return one(e_gsme).E_GES[703].E_ESS[701].ACT_SMT[603]()

    def accept_CreateInstanceEventNode(self, node):
        v_var = self.find_symbol(node, node.variable_name)
        implicit = v_var is None
        if implicit:
            s_dt = self.s_dt('inst<Event>')
            v_trn = self.v_trn(node, node.variable_name)
            v_var = one(v_trn).V_VAR[814]()
            relate(v_var, s_dt, 848)
        
        v_var_to = self.find_symbol(node, name=node.to_variable_name)            
        o_obj = one(v_var_to).V_INT[814].O_OBJ[818]()
        evt_filter = lambda sel: (sel.Drv_Lbl == node.event_specification.identifier or
                                  sel.Drv_Lbl == node.event_specification.identifier + '*')
        sm_evt = one(o_obj).SM_ISM[518].SM_SM[517].SM_EVT[502](evt_filter)

        e_csme = self.e_csme(node, sm_evt, v_var, implicit)
        e_eci = self.new('E_CEI')
        
        relate(e_csme, e_eci, 704)
        relate(e_eci, v_var_to, 711)
        
        return one(e_csme).E_CES[702].E_ESS[701].ACT_SMT[603]()
    
    def accept_CreateCreatorEventNode(self, node):
        v_var = self.find_symbol(node, node.variable_name)
        implicit = v_var is None
        if implicit:
            s_dt = self.s_dt('inst<Event>')
            v_trn = self.v_trn(node, node.variable_name)
            v_var = one(v_trn).V_VAR[814]()
            relate(v_var, s_dt, 848)
        
        o_obj = self.o_obj(node.key_letter)
        evt_filter = lambda sel: (sel.Drv_Lbl == node.event_specification.identifier or
                                  sel.Drv_Lbl == node.event_specification.identifier + '*')
        sm_evt = one(o_obj).SM_ISM[518].SM_SM[517].SM_EVT[502](evt_filter)
        
        e_csme = self.e_csme(node, sm_evt, v_var, implicit)
        e_cec = self.new('E_CEC')

        relate(e_csme, e_cec, 704)
            
        return one(e_csme).E_CES[702].E_ESS[701].ACT_SMT[603]()
    
    def accept_CreateClassEventNode(self, node):
        v_var = self.find_symbol(node, node.variable_name)
        implicit = v_var is None
        if implicit:
            s_dt = self.s_dt('inst<Event>')
            v_trn = self.v_trn(node, node.variable_name)
            v_var = one(v_trn).V_VAR[814]()
            relate(v_var, s_dt, 848)
            
        o_obj = self.o_obj(node.key_letter)
        evt_filter = lambda sel: (sel.Drv_Lbl == node.event_specification.identifier or
                                  sel.Drv_Lbl == node.event_specification.identifier + '*')
        sm_evt = one(o_obj).SM_ASM[519].SM_SM[517].SM_EVT[502](evt_filter)
        
        e_csme = self.e_csme(node, sm_evt, v_var, implicit)
        e_cea = self.new('E_CEA')

        relate(e_csme, e_cea, 704)
            
        return one(e_csme).E_CES[702].E_ESS[701].ACT_SMT[603]()

    def accept_EventDataListNode(self, node):
        prev = None
        for child in node.children:
            v_par = self.accept(child)
            xtuml.relate(prev, v_par, 816, 'succeeds')
            prev = v_par
            yield v_par
            
    def accept_EventDataItemNode(self, node):
        v_val = self.accept(node.expression)
        v_par = self.new('V_PAR', Name=node.name)
        
        relate(v_val, v_par, 800)
        
        return v_par

    def accept_GeneratePreexistingNode(self, node):
        act_smt = self.act_smt(node)
        v_val = self.accept(node.variable_access)
        
        e_gpr = self.new('E_GPR')
        
        relate(e_gpr, act_smt, 603)
        relate(e_gpr, v_val, 714)
        
        return act_smt
    
    def accept_InvocationStatementNode(self, node):
        act_smt = self.act_smt(node)
        
        self.accept(node.invocation, act_smt=act_smt)

        return act_smt
    
    def accept_ImplicitInvocationNode(self, node, act_smt=None):
        if self.s_ee(node.namespace):
            return self.accept_BridgeInvocationNode(node, act_smt=act_smt)
        
        elif self.o_obj(node.namespace):
            return self.accept_ClassInvocationNode(node, act_smt=act_smt)

        else:
            return self.accept_PortInvocationNode(node, act_smt=act_smt)
            
    def accept_InstanceInvocationNode(self, node, act_smt=None):
        inst_v_val = self.accept(node.handle)
        v_var = one(inst_v_val).V_IRF[801].V_VAR[808]()
        o_obj = one(v_var).V_INT[814].O_OBJ[818]()
        o_tfr = one(o_obj).O_TFR[115](where(Name=node.action_name))
        s_dt = one(o_tfr).S_DT[116]()
        v_val = self.v_val(node)
        v_trv = self.new('V_TRV', ParmListOK=True)
        
        relate(v_val, s_dt, 820)
        relate(v_trv, v_val, 801)
        relate(v_trv, o_tfr, 829)
        relate(v_trv, v_var, 830)
        
        if act_smt:
            act_tfm = self.new('ACT_TFM')
            relate(act_tfm, act_smt, 603)
            relate(act_tfm, o_tfr, 673)
            relate(act_tfm, v_var, 667)
        
        self.accept(node.parameter_list, act_smt=act_smt, v_val=v_val)
        
        return v_val
    
    def accept_ClassInvocationNode(self, node, act_smt=None):
        o_obj = self.o_obj(node.namespace)
        o_tfr = one(o_obj).O_TFR[115](where(Name=node.action_name))
        s_dt = one(o_tfr).S_DT[116]()
        v_val = self.v_val(node)
        v_trv = self.new('V_TRV', ParmListOK=True)
        
        relate(v_val, s_dt, 820)
        relate(v_trv, v_val, 801)
        relate(v_trv, o_tfr, 829)
        
        if act_smt:
            act_tfm = self.new('ACT_TFM')
            relate(act_tfm, act_smt, 603)
            relate(act_tfm, o_tfr, 673)
        
        self.accept(node.parameter_list, act_smt=act_smt, v_val=v_val)
           
        return v_val
    
    def accept_BridgeInvocationNode(self, node, act_smt=None):
        s_ee = self.s_ee(node.namespace)
        s_brg = one(s_ee).S_BRG[19](where(Name=node.action_name))
        s_dt = one(s_brg).S_DT[20]()
        v_val = self.v_val(node)
        v_brv = self.new('V_BRV', ParmListOK=True)
        
        relate(v_val, s_dt, 820)
        relate(v_val, v_brv, 801)
        relate(v_brv, s_brg, 828)
        
        if act_smt:
            act_brg = self.new('ACT_BRG')
            relate(act_brg, act_smt, 603)
            relate(act_brg, s_brg, 674)
            
        self.accept(node.parameter_list, act_smt=act_smt, v_val=v_val)
        
        return v_val
    
    def accept_FunctionInvocationNode(self, node, act_smt=None):
        s_sync = self.s_sync(node.action_name)
        s_dt = one(s_sync).S_DT[25]()
        v_val = self.v_val(node)
        v_fnv = self.new('V_FNV', ParmListOK=True)
        
        relate(v_val, s_dt, 820)
        relate(v_fnv, v_val, 801)
        relate(v_fnv, s_sync, 827)
        
        if act_smt:
            act_fnc = self.new('ACT_FNC')
            relate(act_fnc, act_smt, 603)
            relate(act_fnc, s_sync, 675)

        self.accept(node.parameter_list, act_smt=act_smt, v_val=v_val)
        
        return v_val
    
    def accept_PortInvocationNode(self, node, act_smt=None):
        port_filt = lambda sel: (sel.Name == node.namespace or 
                                 one(sel).C_IR[4016].C_I[4012](where(Name=node.namespace)))
        c_po = one(self.c_c).C_PO[4010](port_filt)        
        c_ir = one(c_po).C_IR[4016]()
        c_ep = one(c_ir).C_I[4012].C_EP[4003](where(Name=node.action_name))            
        spr_ro = one(c_ep).SPR_REP[4500].SPR_RO[4502]()
        spr_rs = one(c_ep).SPR_REP[4500].SPR_RS[4502]()
        spr_po = one(c_ep).SPR_PEP[4501].SPR_PO[4503]()
        spr_ps = one(c_ep).SPR_PEP[4501].SPR_PS[4503]()
        
        if act_smt:
            if spr_ro:
                self.new('ACT_IOP',
                         Statement_ID=act_smt.Statement_ID,
                         RequiredOp_Id=spr_ro.Id)
    
            if spr_po:
                self.new('ACT_IOP',
                         Statement_ID=act_smt.Statement_ID,
                         ProvidedOp_Id=spr_po.Id)
    
            if spr_rs:
                self.new('ACT_SGN',
                         Statement_ID=act_smt.Statement_ID,
                         RequiredSig_Id=spr_rs.Id)
            
            if spr_ps:
                self.new('ACT_IOP',
                         Statement_ID=act_smt.Statement_ID,
                         ProvidedSig_Id=spr_ps.Id)
        
        spr_rep = one(spr_ro).SPR_REP[4502]()
        spr_pep = one(spr_po).SPR_PEP[4503]()
        c_io = one(c_ep).C_IO[4004]()
        v_val = None
        
        if spr_rep:
            v_val = self.v_val(node, DT_ID=c_io.DT_ID)
            self.new('V_MSV',
                     Value_ID=v_val.Value_ID,
                     REP_Id=spr_rep.Id,
                     ParmListOK=True)
            
        if spr_pep:
            v_val = self.v_val(node, DT_ID=c_io.DT_ID)
            self.new('V_MSV',
                     Value_ID=v_val.Value_ID,
                     PEP_Id=spr_pep.Id,
                     ParmListOK=True)
            
        self.accept(node.parameter_list, act_smt=act_smt, v_val=v_val)
        
        return v_val

    def accept_ParameterListNode(self, node, act_smt, v_val):
        next_value_id = None
        for child in reversed(node.children):
            v_par = self.accept(child)
            v_par.Next_Value_ID = next_value_id
            
            if act_smt:
                v_par.Statement_ID = act_smt.Statement_ID
            
            if v_val:
                v_par.Invocation_Value_ID = v_val.Value_ID
                
            next_value_id = v_par.Value_ID
    
    def accept_ParameterNode(self, node):
        v_val = self.accept(node.expression)
        return self.new('V_PAR',
                        Value_ID=v_val.Value_ID,
                        Invocation_Value_ID=v_val.Value_ID,
                        Name=node.name)
        
    def accept_GeneratePortEventNode(self, node):
        port_filt = lambda sel: (sel.Name == node.port_name or 
                                 one(sel).C_IR[4016].C_I[4012](where(Name=node.port_name)))
        c_po = one(self.c_c).C_PO[4010](port_filt)

        c_ir = one(c_po).C_IR[4016]()
        c_ep = one(c_ir).C_I[4012].C_EP[4003](where(Name=node.action_name))            
        spr_rs = one(c_ep).SPR_REP[4500].SPR_RS[4502]()
        spr_ps = one(c_ep).SPR_PEP[4501].SPR_PS[4503]()
        

        act_smt = self.act_smt(node)
        v_val = self.accept(node.expression)
        act_sgn = self.new('ACT_SGN')
    
        relate(act_sgn, act_smt, 603)
        relate(act_sgn, v_val, 630)
        xtuml.relate(act_sgn, spr_rs, 660)
        xtuml.relate(act_sgn, spr_ps, 663)
        
        return act_smt
    
class BridgePrebuilder(ActionPrebuilder):
    def __init__(self, metamodel, s_brg):
        self._s_brg = s_brg
        s_ee = one(s_brg).S_EE[19]()
        c_c = get_defining_component(s_ee)
        ActionPrebuilder.__init__(self, metamodel, c_c)      

    @property
    def label(self):
        s_ee = one(self._s_brg).S_EE[19]()
        return '%s::%s' % (s_ee.Name, self._s_brg.Name)
    
    def accept_BodyNode(self, node):
        act_brb = self.new('ACT_BRB')
        relate(act_brb, self._s_brg, 697)
        
        self.act_act = self.new('ACT_ACT', Type='bridge')
        relate(act_brb, self.act_act, 698)
        
        return ActionPrebuilder.accept_BodyNode(self, node)

    def accept_ParamAccessNode(self, node):
        s_bparm = one(self._s_brg).S_BPARM[21](where(Name=node.variable_name))
        s_dt = one(s_bparm).S_DT[22]()
        v_val = self.v_val(node)
        v_pvl = self.new('V_PVL')
        
        relate(v_val, s_dt, 820)
        relate(v_pvl, s_bparm, 831)
        relate(v_pvl, v_val, 801)
        
        return v_val


class FunctionPrebuilder(ActionPrebuilder):
    def __init__(self, metamodel, s_sync):
        self._s_sync = s_sync
        c_c = get_defining_component(s_sync)
        ActionPrebuilder.__init__(self, metamodel, c_c)      
    
    @property
    def label(self):
        return self._s_sync.Name
    
    def accept_BodyNode(self, node):
        act_fnb = self.new('ACT_FNB')
        relate(act_fnb, self._s_sync, 695)
        
        self.act_act = self.new('ACT_ACT',
                                Type='function',
                                Label=self.label)
        
        relate(act_fnb, self.act_act, 698)
        
        return ActionPrebuilder.accept_BodyNode(self, node)

    def accept_ParamAccessNode(self, node):
        s_sparm = one(self._s_sync).S_SPARM[24](where(Name=node.variable_name))
        s_dt = one(s_sparm).S_DT[26]()
        v_val = self.v_val(node)
        v_pvl = self.new('V_PVL')
        
        relate(v_val, s_dt, 820)
        relate(v_pvl, s_sparm, 832)
        relate(v_pvl, v_val, 801)
        
        return v_val


class OperationPrebuilder(ActionPrebuilder):
    
    def __init__(self, metamodel, o_tfr):
        self._o_tfr = o_tfr
        self._o_obj = one(o_tfr).O_OBJ[115]()
        c_c = get_defining_component(self._o_obj)
        ActionPrebuilder.__init__(self, metamodel, c_c)      

    def find_symbol(self, node, name):
        v_var = ActionPrebuilder.find_symbol(self, node, name)
        if not v_var and name.lower() == 'self':
            v_int = self.v_int(node, 'self', self._o_obj)
            v_var = one(v_int).V_VAR[814]()
        
        return v_var
    
    @property
    def label(self):
        return '%s::%s' % (self._o_obj.Name, self._o_tfr.Name)
    
    def accept_BodyNode(self, node):
        act_opb = self.new('ACT_OPB')
        relate(act_opb, self._o_tfr, 696)
        
        self.act_act = self.new('ACT_ACT',
                                Type='operation',
                                Label=self.label)
        
        relate(act_opb, self.act_act, 698)
        
        return ActionPrebuilder.accept_BodyNode(self, node)

    def accept_ParamAccessNode(self, node):
        o_tparm = one(self._o_tfr).O_TPARM[117](where(Name=node.variable_name))
        s_dt = one(o_tparm).S_DT[118]()
        v_val = self.v_val(node)
        v_pvl = self.new('V_PVL')
        
        relate(s_dt, v_val, 820)
        relate(v_pvl, o_tparm, 833)
        relate(v_pvl, v_val, 801)
        
        return v_val


class TransitionPrebuilder(ActionPrebuilder):
    
    def __init__(self, metamodel, sm_act):
        self._sm_act = sm_act
        self._o_obj = (one(sm_act).SM_SM[515].SM_ISM[517].O_OBJ[518]() or
                       one(sm_act).SM_SM[515].SM_ASM[517].O_OBJ[519]())
        c_c = get_defining_component(self._o_obj)
        ActionPrebuilder.__init__(self, metamodel, c_c)

    def find_symbol(self, node, name):
        v_var = ActionPrebuilder.find_symbol(self, node, name)
        if not v_var and name.lower() == 'self':
            v_int = self.v_int(node, 'self', self._o_obj)
            v_var = one(v_int).V_VAR[814]()
        
        return v_var
    
    @property
    def label(self):
        return ''
        
    def accept_BodyNode(self, node):
        act_sab = self.new('ACT_SAB')
        relate(act_sab, self._sm_act, 691)
        
        self.act_act = self.new('ACT_ACT')
        
        relate(act_sab, self.act_act, 698)
        
        return ActionPrebuilder.accept_BodyNode(self, node)

    def accept_ParamAccessNode(self, node):
        filt = where(Name=node.variable_name)
        sm_txn = (one(self._sm_act).SM_AH[514].SM_MOAH[513].SM_STATE[511].SM_TXN[506]() or
                  one(self._sm_act).SM_AH[514].SM_TAH[513].SM_TXN[530]())
        sm_evt = (one(sm_txn).SM_NSTXN[507].SM_SEME[504].SM_SEVT[503].SM_EVT[525]() or
                  one(sm_txn).SM_CRTXN[507].SM_LEVT[509].SM_SEVT[526].SM_EVT[525]())
        sm_evt = one(sm_evt).SM_SEVT[525].SM_NLEVT[526].SM_PEVT[527].SM_EVT[525]() or sm_evt
        sm_evt_di = one(sm_evt).SM_EVTDI[532](filt)
        
        spr_pep = one(sm_evt).SM_SEVT[525].SM_SGEVT[526].SPR_PS[528].SPR_PEP[4503]()
        spr_rep = one(sm_evt).SM_SEVT[525].SM_SGEVT[526].SPR_RS[529].SPR_REP[4502]()

        c_pp = (one(spr_pep).C_EP[4501].C_PP[4006](filt) or
                one(spr_rep).C_EP[4500].C_PP[4006](filt))
    
        s_dt = one(sm_evt_di).S_DT[524]() or one(c_pp).S_DT[4007]()
        
        v_val = self.v_val(node)
        v_edv = self.new('V_EDV')
        v_epr = self.new('V_EPR')

        relate(v_val, v_edv, 801)
        relate(v_val, s_dt, 820)
        relate(v_epr, v_edv, 834)
        xtuml.relate(v_epr, sm_evt_di, 846)
        xtuml.relate(v_epr, c_pp, 847)
        
        return v_val

    
class DerivedAttributePrebuilder(ActionPrebuilder):
    
    def __init__(self, metamodel, o_dbattr):
        self._o_dbattr = o_dbattr
        self._o_obj = one(o_dbattr).O_BATTR[107].O_ATTR[106].O_OBJ[102]()
        c_c = get_defining_component(self._o_obj)
        ActionPrebuilder.__init__(self, metamodel, c_c)      

    def find_symbol(self, node, name):
        v_var = ActionPrebuilder.find_symbol(self, node, name)
        if not v_var and name.lower() == 'self':
            v_int = self.v_int(node, 'self', self._o_obj)
            v_var = one(v_int).V_VAR[814]()
        
        return v_var
    
    @property
    def label(self):
        o_attr = one(self._o_dbattr).O_BATTR[107].O_ATTR[106]()
        return '%s::%s' % (self._o_obj.Name, o_attr.Name)
    
    def accept_BodyNode(self, node):
        act_dab = self.new('ACT_DAB')
        relate(act_dab, self._o_dbattr, 693)
        
        self.act_act = self.new('ACT_ACT',
                                Type='derived attribute',
                                Label=self.label)
        
        relate(act_dab, self.act_act, 698)
        
        return ActionPrebuilder.accept_BodyNode(self, node)
    
    
class RequiredOperationPrebuilder(ActionPrebuilder):
    
    def __init__(self, metamodel, spr_ro):
        self._spr_ro = spr_ro
        c_c = one(spr_ro).SPR_REP[4502].C_R[4500].C_IR[4009].C_PO[4016].C_C[4010]()
        ActionPrebuilder.__init__(self, metamodel, c_c)      

    @property
    def label(self):
        # interface = one(self._spr_ro).SPR_REP[4502].C_R[4500].C_IR[4009].C_I[4012]()
        # port = one(self._spr_ro).SPR_REP[4502].C_R[4500].C_IR[4009].C_PO[4016]()
        # return '%s::%s::%s' % (port.Name, interface.Name, self._spr_ro.Name)
        return ''
    
    def accept_BodyNode(self, node):
        act_rob = self.new('ACT_ROB')
        relate(act_rob, self._spr_ro, 685)
        
        self.act_act = self.new('ACT_ACT', Type='interface operation', Label=self.label)
        relate(act_rob, self.act_act, 698)
        
        return ActionPrebuilder.accept_BodyNode(self, node)
    
    def accept_ParamAccessNode(self, node):
        c_pp = one(self._spr_ro).SPR_REP[4502].C_EP[4500].C_PP[4006](where(Name=node.variable_name))
        s_dt = one(c_pp).S_DT[4007]()
        v_val = self.v_val(node)
        v_pvl = self.new('V_PVL')
        
        relate(v_val, s_dt, 820)
        relate(v_pvl, c_pp, 843)
        relate(v_pvl, v_val, 801)
        
        return v_val


class RequiredSignalPrebuilder(ActionPrebuilder):
    
    def __init__(self, metamodel, spr_rs):
        self._spr_rs = spr_rs
        c_c = one(spr_rs).SPR_REP[4502].C_R[4500].C_IR[4009].C_PO[4016].C_C[4010]()
        ActionPrebuilder.__init__(self, metamodel, c_c)  

    @property
    def label(self):
        return ''
    
    def accept_BodyNode(self, node):
        act_rsb = self.new('ACT_RSB')
        relate(act_rsb, self._spr_rs, 684)
        
        self.act_act = self.new('ACT_ACT', Type='interface signal')
        relate(act_rsb, self.act_act, 698)
        
        return ActionPrebuilder.accept_BodyNode(self, node)
    
    def accept_ParamAccessNode(self, node):
        c_pp = one(self._spr_rs).SPR_REP[4502].C_EP[4500].C_PP[4006](where(Name=node.variable_name))
        s_dt = one(c_pp).S_DT[4007]()
        v_val = self.v_val(node)
        v_pvl = self.new('V_PVL')
        
        relate(v_val, s_dt, 820)
        relate(v_pvl, c_pp, 843)
        relate(v_pvl, v_val, 801)
        
        return v_val


class ProvidedOperationPrebuilder(ActionPrebuilder):

    def __init__(self, metamodel, spr_po):
        self._spr_po = spr_po
        c_c = one(spr_po).SPR_PEP[4503].C_P[4501].C_IR[4009].C_PO[4016].C_C[4010]()
        ActionPrebuilder.__init__(self, metamodel, c_c)  
        
    @property
    def label(self):
        # interface = one(self._spr_po).SPR_PEP[4503].C_P[4501].C_IR[4009].C_I[4012]()
        # port = one(self._spr_po).SPR_PEP[4503].C_P[4501].C_IR[4009].C_PO[4016]()
        # return '%s::%s::%s' % (port.Name, interface.Name, self._spr_po.Name)
        return ''
    
    def accept_BodyNode(self, node):
        act_pob = self.new('ACT_POB')
        relate(act_pob, self._spr_po, 687)
        
        self.act_act = self.new('ACT_ACT', Type='interface operation', Label=self.label)
        relate(act_pob, self.act_act, 698)
        
        return ActionPrebuilder.accept_BodyNode(self, node)

    def accept_ParamAccessNode(self, node):
        c_pp = one(self._spr_po).SPR_PEP[4503].C_EP[4501].C_PP[4006](where(Name=node.variable_name))
        s_dt = one(c_pp).S_DT[4007]()
        v_val = self.v_val(node)
        v_pvl = self.new('V_PVL')
        
        relate(v_val, s_dt, 820)
        relate(v_pvl, c_pp, 843)
        relate(v_pvl, v_val, 801)
        
        return v_val


class ProvidedSignalPrebuilder(ActionPrebuilder):

    def __init__(self, metamodel, spr_ps):
        self._spr_ps = spr_ps
        c_c = one(spr_ps).SPR_PEP[4503].C_P[4501].C_IR[4009].C_PO[4016].C_C[4010]()
        ActionPrebuilder.__init__(self, metamodel, c_c)  

    @property
    def label(self):
        return ''
    
    def accept_BodyNode(self, node):
        act_psb = self.new('ACT_PSB')
        relate(act_psb, self._spr_ps, 686)
        
        self.act_act = self.new('ACT_ACT', Type='interface signal')
        relate(act_psb, self.act_act, 698)
        
        return ActionPrebuilder.accept_BodyNode(self, node)

    def accept_ParamAccessNode(self, node):
        c_pp = one(self._spr_ps).SPR_PEP[4503].C_EP[4501].C_PP[4006](where(Name=node.variable_name))
        s_dt = one(c_pp).S_DT[4007]()
        v_val = self.v_val(node)
        v_pvl = self.new('V_PVL')
        
        relate(v_val, s_dt, 820)
        relate(v_pvl, c_pp, 843)
        relate(v_pvl, v_val, 801)
        
        return v_val


def prebuild_action(instance):
    '''
    Transform textual OAL actions of an *instance* to instances in the ooaofooa
    subsystems Value and Body. The provided *instance* must be an instance of 
    one of the following classes:
    
    - S_SYNC
    - S_BRG
    - O_TFR
    - O_DBATTR
    - SM_ACT
    - SPR_RO
    - SPR_RS
    - SPR_PO
    - SPR_PS
    '''
    walker_map = {
        'S_SYNC': FunctionPrebuilder,
        'S_BRG': BridgePrebuilder,
        'O_TFR': OperationPrebuilder,
        'O_DBATTR': DerivedAttributePrebuilder,
        'SM_ACT': TransitionPrebuilder,
        'SPR_RO': RequiredOperationPrebuilder,
        'SPR_RS': RequiredSignalPrebuilder,
        'SPR_PO': ProvidedOperationPrebuilder,
        'SPR_PS': ProvidedSignalPrebuilder
    }
    metaclass = instance.__metaclass__
    walker = walker_map[metaclass.kind](metaclass.metamodel, instance)
    logger.info('processing action %s' % walker.label)
    # walker.visitors.append(xtuml.tools.NodePrintVisitor())
    root = oal.parse(instance.Action_Semantics_internal)
    return walker.accept(root)
    
                
def prebuild_model(metamodel):
    '''
    Transform textual OAL actions in a ooaofooa *metamodel* to instances in the
    subsystems Value and Body. Instances of the following classes are supported:
    
    - S_SYNC
    - S_BRG
    - O_TFR
    - O_DBATTR
    - SM_ACT
    - SPR_RO
    - SPR_RS
    - SPR_PO
    - SPR_PS
    '''
    for kind in ['S_SYNC','S_BRG','O_TFR', 'O_DBATTR', 'SM_ACT', 'SPR_RO',
                 'SPR_RS', 'SPR_PO', 'SPR_PS']:
        for inst in metamodel.select_many(kind):
            if inst.Suc_Pars:
                prebuild_action(inst)


def main():
    '''
    Parse command line options and launch the prebuilder.
    '''
    parser = optparse.OptionParser(usage="%prog [options] <model_path> [another_model_path..]",
                                   version=xtuml.version.complete_string,
                                   formatter=optparse.TitledHelpFormatter())

    parser.add_option("-v", "--verbosity", dest='verbosity',
                                           action="count",
                                           help="increase debug logging level",
                                           default=1)
    
    parser.add_option("-o", "--output", dest="output", metavar="PATH",
                                        help="set output to PATH",
                                        action="store",
                                        default=None)
    
    (opts, args) = parser.parse_args()
    if len(args) == 0 or opts.output is None:
        parser.print_help()
        sys.exit(1)
        
    levels = {
              0: logging.ERROR,
              1: logging.WARNING,
              2: logging.INFO,
              3: logging.DEBUG,
    }
    logging.basicConfig(level=levels.get(opts.verbosity, logging.DEBUG))
    
    m = ooaofooa.load_metamodel(args)
    prebuild_model(m)
    
    xtuml.persist_instances(m, opts.output)


if __name__ == '__main__':
    main()
    

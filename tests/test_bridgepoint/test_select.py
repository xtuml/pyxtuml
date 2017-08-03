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

from tests.test_bridgepoint.utils import PrebuildFunctionTestCase
from tests.test_bridgepoint.utils import prebuild_docstring

from xtuml import navigate_one as one
from xtuml import relate


class TestSelect(PrebuildFunctionTestCase):

    def setUp(self):
        PrebuildFunctionTestCase.setUp(self)
        pe_pe = self.metamodel.new('PE_PE')
        a = self.metamodel.new('O_OBJ', Key_Lett='A')
        relate(pe_pe, a, 8001)
        
        pe_pe = self.metamodel.new('PE_PE')
        b = self.metamodel.new('O_OBJ', Key_Lett='B')
        relate(pe_pe, b, 8001)
        
        pe_pe = self.metamodel.new('PE_PE')
        c = self.metamodel.new('O_OBJ', Key_Lett='C')
        relate(pe_pe, c, 8001)
        
        r1 = self.metamodel.new('R_REL', Numb=1)
        r2 = self.metamodel.new('R_REL', Numb=2)
        r3 = self.metamodel.new('R_REL', Numb=3)
        
        relate(self.metamodel.new('PE_PE'), r1, 8001)
        relate(self.metamodel.new('PE_PE'), r2, 8001)
        relate(self.metamodel.new('PE_PE'), r3, 8001)
    
        r_oir = self.metamodel.new('R_OIR')
        relate(r_oir, r1, 201)
        relate(r_oir, a, 201)
        
        r_oir = self.metamodel.new('R_OIR')
        relate(r_oir, r1, 201)
        relate(r_oir, c, 201)
                
        r_oir = self.metamodel.new('R_OIR')
        relate(r_oir, r2, 201)
        relate(r_oir, a, 201)
        
        r_oir = self.metamodel.new('R_OIR')
        relate(r_oir, r2, 201)
        relate(r_oir, b, 201)
        
        r_oir = self.metamodel.new('R_OIR')
        relate(r_oir, r3, 201)
        relate(r_oir, a, 201)
        
        r_oir = self.metamodel.new('R_OIR')
        relate(r_oir, r3, 201)
        relate(r_oir, b, 201)
        
        r_oir = self.metamodel.new('R_OIR')
        relate(r_oir, r3, 201)
        relate(r_oir, c, 201)
        
    @prebuild_docstring
    def test_select_from_instances(self):
        '''
        select any a from instances of A;
        '''
        act_fio = self.metamodel.select_one('ACT_FIO')
        self.assertTrue(act_fio.is_implicit)
        self.assertEqual(act_fio.cardinality, 'any')
        
        act_smt = one(act_fio).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_fio).V_VAR[639]()
        self.assertEqual(v_var.Name, 'a')
        
        o_obj = one(act_fio).O_OBJ[677]()
        self.assertEqual(o_obj.Key_Lett, 'A')

    @prebuild_docstring
    def test_select_from_instances_where(self):
        '''
        select any a from instances of A where (false);
        '''
        act_fiw = self.metamodel.select_one('ACT_FIW')
        self.assertTrue(act_fiw.is_implicit)
        self.assertEqual(act_fiw.cardinality, 'any')
        
        act_smt = one(act_fiw).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_fiw).V_VAR[665]()
        self.assertEqual(v_var.Name, 'a')
        
        o_obj = one(act_fiw).O_OBJ[676]()
        self.assertEqual(o_obj.Key_Lett, 'A')
        
        v_val = one(act_fiw).V_VAL[610]()
        self.assertIsNotNone(v_val)

    @prebuild_docstring
    def test_select_related_by(self):
        '''
        select any a from instances of A;
        select one b related by a->A[R1]->B[R2];
        '''
        act_sr = self.metamodel.select_one('ACT_SR')
        self.assertIsNotNone(act_sr)
        
        act_sr = one(act_sr).ACT_SEL[664]()
        self.assertTrue(act_sr.is_implicit)
        self.assertEqual(act_sr.cardinality, 'one')
        
        act_smt = one(act_sr).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_sr).V_VAR[638]()
        self.assertEqual(v_var.Name, 'b')
        
        v_val = one(act_sr).V_VAL[613]()
        self.assertIsNotNone(v_val)
        self.assertFalse(v_val.isLValue)
        self.assertFalse(v_val.isImplicit)
        
        act_lnk = one(act_sr).ACT_LNK[637]()
        self.assertIsNotNone(act_lnk)
        self.assertFalse(act_lnk.Rel_Phrase)
        
        o_obj = one(act_lnk).O_OBJ[678]()
        self.assertEqual(o_obj.Key_Lett, 'A')
        
        r_rel = one(act_lnk).R_REL[681]()
        self.assertEqual(r_rel.Numb, 1)
        
        act_lnk = one(act_lnk).ACT_LNK[604, 'precedes']()
        self.assertIsNotNone(act_lnk)
        self.assertFalse(act_lnk.Rel_Phrase)
        
        o_obj = one(act_lnk).O_OBJ[678]()
        self.assertEqual(o_obj.Key_Lett, 'B')
        
        r_rel = one(act_lnk).R_REL[681]()
        self.assertEqual(r_rel.Numb, 2)
        
        # TODO: Multiplicity
        
    @prebuild_docstring
    def test_select_related_by_where(self):
        '''
        select any a from instances of A;
        select one b related by a->A[R1.'test']->B[R2] where (false);
        '''
        act_srw = self.metamodel.select_one('ACT_SRW')
        self.assertIsNotNone(act_srw)
        
        v_val = one(act_srw).V_VAL[611]()
        self.assertIsNotNone(v_val)
        self.assertFalse(v_val.isLValue)
        self.assertFalse(v_val.isImplicit)
        
        act_sr = one(act_srw).ACT_SEL[664]()
        self.assertTrue(act_sr.is_implicit)
        self.assertEqual(act_sr.cardinality, 'one')
        
        act_smt = one(act_sr).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_sr).V_VAR[638]()
        self.assertEqual(v_var.Name, 'b')
        
        v_val = one(act_sr).V_VAL[613]()
        self.assertIsNotNone(v_val)
        self.assertFalse(v_val.isLValue)
        self.assertFalse(v_val.isImplicit)
        
        act_lnk = one(act_sr).ACT_LNK[637]()
        self.assertIsNotNone(act_lnk)
        self.assertEqual(act_lnk.Rel_Phrase, "'test'")
        
        o_obj = one(act_lnk).O_OBJ[678]()
        self.assertEqual(o_obj.Key_Lett, 'A')
        
        r_rel = one(act_lnk).R_REL[681]()
        self.assertEqual(r_rel.Numb, 1)
        
        act_lnk = one(act_lnk).ACT_LNK[604, 'precedes']()
        self.assertIsNotNone(act_lnk)
        self.assertFalse(act_lnk.Rel_Phrase)
        
        o_obj = one(act_lnk).O_OBJ[678]()
        self.assertEqual(o_obj.Key_Lett, 'B')
        
        r_rel = one(act_lnk).R_REL[681]()
        self.assertEqual(r_rel.Numb, 2)
        
        # TODO: Multiplicity


if __name__ == "__main__":
    import logging
    import unittest
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    

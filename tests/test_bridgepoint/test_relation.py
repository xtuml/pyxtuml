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


class TestRelation(PrebuildFunctionTestCase):

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
    def test_relate(self):
        '''
        create object instance a of A;
        create object instance b of B;
        relate a to b across R2;
        '''
        act_rel = self.metamodel.select_one('ACT_REL')
        self.assertFalse(act_rel.relationship_phrase)
        
        act_smt = one(act_rel).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_rel).V_VAR[615]()
        self.assertEqual(v_var.Name, 'a')
        
        v_var = one(act_rel).V_VAR[616]()
        self.assertEqual(v_var.Name, 'b')

        r_rel = one(act_rel).R_REL[653]()
        self.assertEqual(r_rel.Numb, 2)

    @prebuild_docstring
    def test_relate_with_phrase(self):
        '''
        create object instance a of A;
        create object instance b of B;
        relate a to b across R2.'some phrase';
        '''
        act_rel = self.metamodel.select_one('ACT_REL')
        self.assertEqual(act_rel.relationship_phrase, "'some phrase'")
        
        act_smt = one(act_rel).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_rel).V_VAR[615]()
        self.assertEqual(v_var.Name, 'a')
        
        v_var = one(act_rel).V_VAR[616]()
        self.assertEqual(v_var.Name, 'b')

        r_rel = one(act_rel).R_REL[653]()
        self.assertEqual(r_rel.Numb, 2)
        
    @prebuild_docstring
    def test_relate_using(self):
        '''
        create object instance a of A;
        create object instance b of B;
        create object instance c of C;
        relate a to b across R2 using c;
        '''
        act_rel = self.metamodel.select_one('ACT_RU')
        self.assertFalse(act_rel.relationship_phrase)
        
        act_smt = one(act_rel).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_rel).V_VAR[617]()
        self.assertEqual(v_var.Name, 'a')
        
        v_var = one(act_rel).V_VAR[618]()
        self.assertEqual(v_var.Name, 'b')

        v_var = one(act_rel).V_VAR[619]()
        self.assertEqual(v_var.Name, 'c')

        r_rel = one(act_rel).R_REL[654]()
        self.assertEqual(r_rel.Numb, 2)

    @prebuild_docstring
    def test_relate_using_with_phrase(self):
        '''
        create object instance a of A;
        create object instance b of B;
        create object instance c of C;
        relate a to b across R2.'some phrase' using c;
        '''
        act_rel = self.metamodel.select_one('ACT_RU')
        self.assertEqual(act_rel.relationship_phrase, "'some phrase'")
        
        act_smt = one(act_rel).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_rel).V_VAR[617]()
        self.assertEqual(v_var.Name, 'a')
        
        v_var = one(act_rel).V_VAR[618]()
        self.assertEqual(v_var.Name, 'b')

        v_var = one(act_rel).V_VAR[619]()
        self.assertEqual(v_var.Name, 'c')

        r_rel = one(act_rel).R_REL[654]()
        self.assertEqual(r_rel.Numb, 2)
        
    @prebuild_docstring
    def test_unrelate(self):
        '''
        create object instance a of A;
        create object instance b of B;
        relate a to b across R2;
        unrelate a from b across R2;
        '''
        act_unr = self.metamodel.select_one('ACT_UNR')
        self.assertFalse(act_unr.relationship_phrase)
        
        act_smt = one(act_unr).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_unr).V_VAR[620]()
        self.assertEqual(v_var.Name, 'a')
        
        v_var = one(act_unr).V_VAR[621]()
        self.assertEqual(v_var.Name, 'b')

        r_rel = one(act_unr).R_REL[655]()
        self.assertEqual(r_rel.Numb, 2)

    @prebuild_docstring
    def test_unrelate_with_phrase(self):
        '''
        create object instance a of A;
        create object instance b of B;
        relate a to b across R2.'some phrase';
        unrelate b from a across R2.'some invalid phrase';
        '''
        act_unr = self.metamodel.select_one('ACT_UNR')
        self.assertEqual(act_unr.relationship_phrase, "'some invalid phrase'")
        
        act_smt = one(act_unr).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_unr).V_VAR[620]()
        self.assertEqual(v_var.Name, 'b')
        
        v_var = one(act_unr).V_VAR[621]()
        self.assertEqual(v_var.Name, 'a')

        r_rel = one(act_unr).R_REL[655]()
        self.assertEqual(r_rel.Numb, 2)
        
    @prebuild_docstring
    def test_unrelate_using(self):
        '''
        create object instance a of A;
        create object instance b of B;
        create object instance c of C;
        relate a to b across R2 using c;
        unrelate a from b across R2 using c;
        '''
        act_unr = self.metamodel.select_one('ACT_URU')
        self.assertFalse(act_unr.relationship_phrase)
        
        act_smt = one(act_unr).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_unr).V_VAR[622]()
        self.assertEqual(v_var.Name, 'a')
        
        v_var = one(act_unr).V_VAR[623]()
        self.assertEqual(v_var.Name, 'b')

        v_var = one(act_unr).V_VAR[624]()
        self.assertEqual(v_var.Name, 'c')
        
        r_rel = one(act_unr).R_REL[656]()
        self.assertEqual(r_rel.Numb, 2)

    @prebuild_docstring
    def test_unrelate_using_with_phrase(self):
        '''
        create object instance a of A;
        create object instance b of B;
        create object instance c of C;
        relate a to b across R2.'some phrase' using c;
        unrelate b from a across R2.'some invalid phrase' using c;
        '''
        act_unr = self.metamodel.select_one('ACT_URU')
        self.assertEqual(act_unr.relationship_phrase, "'some invalid phrase'")
        
        act_smt = one(act_unr).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_var = one(act_unr).V_VAR[622]()
        self.assertEqual(v_var.Name, 'b')
        
        v_var = one(act_unr).V_VAR[623]()
        self.assertEqual(v_var.Name, 'a')

        v_var = one(act_unr).V_VAR[624]()
        self.assertEqual(v_var.Name, 'c')
        
        r_rel = one(act_unr).R_REL[656]()
        self.assertEqual(r_rel.Numb, 2)


if __name__ == "__main__":
    import logging
    import unittest
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    

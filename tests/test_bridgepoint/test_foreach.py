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


class TestForEach(PrebuildFunctionTestCase):
    
    def setUp(self):
        PrebuildFunctionTestCase.setUp(self)
        pe_pe = self.metamodel.new('PE_PE')
        o_obj = self.metamodel.new('O_OBJ', Key_Lett='A')
        relate(pe_pe, o_obj, 8001)
        
    @prebuild_docstring
    def test_for_each(self):
        '''
        create object instance of A;
        create object instance of A;       
        select many a_set from instances of A;
        for each a in a_set
        end for;
        '''
        act_for = self.metamodel.select_one('ACT_FOR')
        self.assertTrue(act_for.is_implicit)
        
        act_smt = one(act_for).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        act_blk = one(act_for).ACT_BLK[605]()
        self.assertIsNotNone(act_blk)
        
        v_var = one(act_for).V_VAR[614]()
        self.assertEqual(v_var.Name, 'a')
        
        v_var = one(act_for).V_VAR[652]()
        self.assertEqual(v_var.Name, 'a_set')

        o_obj = one(act_for).O_OBJ[670]()
        self.assertEqual(o_obj.Key_Lett, 'A')
        
    @prebuild_docstring
    def test_for_each_loop(self):
        '''
        create object instance of A;
        create object instance of A;       
        select many a_set from instances of A;
        for each a in a_set loop
        end for;
        '''
        act_for = self.metamodel.select_one('ACT_FOR')
        self.assertTrue(act_for.is_implicit)
        
        act_smt = one(act_for).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        act_blk = one(act_for).ACT_BLK[605]()
        self.assertIsNotNone(act_blk)
        
        v_var = one(act_for).V_VAR[614]()
        self.assertEqual(v_var.Name, 'a')
        
        v_var = one(act_for).V_VAR[652]()
        self.assertEqual(v_var.Name, 'a_set')

        o_obj = one(act_for).O_OBJ[670]()
        self.assertEqual(o_obj.Key_Lett, 'A')

    @prebuild_docstring
    def test_mixed_casing_in_end_for(self):
        '''
        create object instance of A;
        create object instance of A;       
        select many a_set from instances of A;
        for each a in a_set
        eNd FoR;
        '''
        act_for = self.metamodel.select_one('ACT_FOR')
        self.assertTrue(act_for.is_implicit)
        
        act_smt = one(act_for).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        act_blk = one(act_for).ACT_BLK[605]()
        self.assertIsNotNone(act_blk)
        
        v_var = one(act_for).V_VAR[614]()
        self.assertEqual(v_var.Name, 'a')
        
        v_var = one(act_for).V_VAR[652]()
        self.assertEqual(v_var.Name, 'a_set')

        o_obj = one(act_for).O_OBJ[670]()
        self.assertEqual(o_obj.Key_Lett, 'A')
        
if __name__ == "__main__":
    import logging
    import unittest
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()


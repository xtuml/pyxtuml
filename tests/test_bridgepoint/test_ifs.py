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
from xtuml import navigate_many as many


class TestIfStatements(PrebuildFunctionTestCase):

    @prebuild_docstring
    def test_single_if_true(self):
        '''
        if ( 0 == 0 ) then
            return 1;
        end if;
        return 0;
        '''
        act_if = self.metamodel.select_one('ACT_IF')
        self.assertIsNotNone(act_if)
        
        act_smt = one(act_if).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_if).V_VAL[625]()
        self.assertIsNotNone(v_val)
        
        act_blk = one(act_if).ACT_BLK[607]()
        self.assertIsNotNone(act_blk)
        
        act_el = many(act_if).ACT_EL[682]()
        self.assertEqual(len(act_el), 0)
        
        act_e = one(act_if).ACT_E[683]()
        self.assertIsNone(act_e)

    @prebuild_docstring
    def test_mixed_casing_in_end_if(self):
        '''
        if ( 0 == 0 ) then
            return 1;
        eNd If;
        return 0;
        '''
        act_if = self.metamodel.select_one('ACT_IF')
        self.assertIsNotNone(act_if)
        
        act_smt = one(act_if).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_if).V_VAL[625]()
        self.assertIsNotNone(v_val)
        
        act_blk = one(act_if).ACT_BLK[607]()
        self.assertIsNotNone(act_blk)
        
        act_el = many(act_if).ACT_EL[682]()
        self.assertEqual(len(act_el), 0)
        
        act_e = one(act_if).ACT_E[683]()
        self.assertIsNone(act_e)

    @prebuild_docstring
    def test_elif(self):
        '''
        assign x = 0;
        if (1 == 0) then
            assign x = 1;
        elif (1 == 1) then
            assign x = 2;
        end if;
        return x;
        '''
        act_if = self.metamodel.select_one('ACT_IF')
        self.assertIsNotNone(act_if)
        
        act_smt = one(act_if).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_if).V_VAL[625]()
        self.assertIsNotNone(v_val)
        
        act_blk = one(act_if).ACT_BLK[607]()
        self.assertIsNotNone(act_blk)
        
        act_el = many(act_if).ACT_EL[682]()
        self.assertEqual(len(act_el), 1)
        
        act_el = one(act_if).ACT_EL[682]()
        act_smt = one(act_el).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)

        v_val = one(act_el).V_VAL[659]()
        self.assertIsNotNone(v_val)
        
        act_blk = one(act_el).ACT_BLK[658]()
        self.assertIsNotNone(act_blk)
        
        act_e = one(act_if).ACT_E[683]()
        self.assertIsNone(act_e)

    @prebuild_docstring
    def test_elif_no_then(self):
        '''
        assign x = 0;
        if (1 == 0)
            assign x = 1;
        elif (1 == 1)
            assign x = 2;
        end if;
        return x;
        '''
        act_if = self.metamodel.select_one('ACT_IF')
        self.assertIsNotNone(act_if)
        
        act_smt = one(act_if).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_if).V_VAL[625]()
        self.assertIsNotNone(v_val)
        
        act_blk = one(act_if).ACT_BLK[607]()
        self.assertIsNotNone(act_blk)
        
        act_el = many(act_if).ACT_EL[682]()
        self.assertEqual(len(act_el), 1)
        
        act_el = one(act_if).ACT_EL[682]()
        act_smt = one(act_el).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)

        v_val = one(act_el).V_VAL[659]()
        self.assertIsNotNone(v_val)
        
        act_blk = one(act_el).ACT_BLK[658]()
        self.assertIsNotNone(act_blk)
        
        act_e = one(act_if).ACT_E[683]()
        self.assertIsNone(act_e)
        
    @prebuild_docstring
    def test_elif_else(self):
        '''
        assign x = 0;
        if (1 == 0) then
            assign x = 1;
        elif (1 == 1) then
            assign x = 2;
        else
            assign x = 3;
        end if;
        return x;
        '''
        act_if = self.metamodel.select_one('ACT_IF')
        self.assertIsNotNone(act_if)
        
        act_smt = one(act_if).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_if).V_VAL[625]()
        self.assertIsNotNone(v_val)
        
        act_blk = one(act_if).ACT_BLK[607]()
        self.assertIsNotNone(act_blk)
        
        act_el = many(act_if).ACT_EL[682]()
        self.assertEqual(len(act_el), 1)
        
        act_el = one(act_if).ACT_EL[682]()
        act_smt = one(act_el).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)

        v_val = one(act_el).V_VAL[659]()
        self.assertIsNotNone(v_val)
        
        act_blk = one(act_el).ACT_BLK[658]()
        self.assertIsNotNone(act_blk)
        
        act_e = one(act_if).ACT_E[683]()
        act_blk = one(act_e).ACT_BLK[606]()
        self.assertIsNotNone(act_blk)
        
        
if __name__ == "__main__":
    import logging
    import unittest
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

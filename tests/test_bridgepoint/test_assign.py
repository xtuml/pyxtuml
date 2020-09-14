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


class TestAssign(PrebuildFunctionTestCase):

    @prebuild_docstring
    def test_positive_integer(self):
        '''assign x = 1;'''
        act_ai = self.metamodel.select_one('ACT_AI')
        self.assertIsNotNone(act_ai)
        
        act_smt = one(act_ai).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        self.assertEqual(act_smt.Label, 'assign x = 1')
        v_val = one(act_ai).V_VAL[609]()
        self.assertFalse(v_val.isLValue)
        self.assertFalse(v_val.isImplicit)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 12)
        self.assertEqual(v_val.EndPosition, 12)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_val = one(act_ai).V_VAL[689]()
        self.assertTrue(v_val.isLValue)
        self.assertTrue(v_val.isImplicit)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 8)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_tvl = one(v_val).V_TVL[801]()
        self.assertIsNotNone(v_tvl)
        
        v_var = one(v_tvl).V_VAR[805]()
        self.assertEqual(v_var.Name, 'x')
        self.assertTrue(v_var.Declared)
        
        s_dt = one(v_var).S_DT[848]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_trn = one(v_var).V_TRN[814]()
        self.assertIsNotNone(v_trn)
                
    @prebuild_docstring
    def test_positive_real(self):
        '''assign x = 1.1;'''
        act_ai = self.metamodel.select_one('ACT_AI')
        self.assertIsNotNone(act_ai)
        
        act_smt = one(act_ai).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ai).V_VAL[609]()
        self.assertFalse(v_val.isLValue)
        self.assertFalse(v_val.isImplicit)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 12)
        self.assertEqual(v_val.EndPosition, 14)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'real')
        
        v_val = one(act_ai).V_VAL[689]()
        self.assertTrue(v_val.isLValue)
        self.assertTrue(v_val.isImplicit)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 8)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'real')
        
        v_tvl = one(v_val).V_TVL[801]()
        self.assertIsNotNone(v_tvl)
        
        v_var = one(v_tvl).V_VAR[805]()
        self.assertEqual(v_var.Name, 'x')
        self.assertTrue(v_var.Declared)
        
        s_dt = one(v_var).S_DT[848]()
        self.assertEqual(s_dt.Name, 'real')
        
        v_trn = one(v_var).V_TRN[814]()
        self.assertIsNotNone(v_trn)
        
    @prebuild_docstring
    def test_string(self):
        '''assign x = "Hello";'''
        act_ai = self.metamodel.select_one('ACT_AI')
        self.assertIsNotNone(act_ai)
        
        act_smt = one(act_ai).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ai).V_VAL[609]()
        self.assertFalse(v_val.isLValue)
        self.assertFalse(v_val.isImplicit)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 12)
        self.assertEqual(v_val.EndPosition, 18)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'string')
        
        v_val = one(act_ai).V_VAL[689]()
        self.assertTrue(v_val.isLValue)
        self.assertTrue(v_val.isImplicit)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 8)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'string')
        
        v_tvl = one(v_val).V_TVL[801]()
        self.assertIsNotNone(v_tvl)
        
        v_var = one(v_tvl).V_VAR[805]()
        self.assertEqual(v_var.Name, 'x')
        self.assertTrue(v_var.Declared)
        
        s_dt = one(v_var).S_DT[848]()
        self.assertEqual(s_dt.Name, 'string')
        
        v_trn = one(v_var).V_TRN[814]()
        self.assertIsNotNone(v_trn)


if __name__ == "__main__":
    import logging
    import unittest
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    

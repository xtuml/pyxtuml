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
from bridgepoint import prebuild


class TestConstLiterals(PrebuildFunctionTestCase):

    @prebuild_docstring
    def test_positive_integer(self):
        '''return 1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 8)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_lin = one(v_val).V_LIN[801]()
        self.assertEqual(v_lin.Value, '1')

    @prebuild_docstring
    def test_negative_integer(self):
        '''return -1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 9)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_uny = one(v_val).V_UNY[801]()
        self.assertEqual(v_uny.Operator, '-')

        v_val = one(v_uny).V_VAL[804]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 9)
        self.assertEqual(v_val.EndPosition, 9)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'integer')
        
        v_lin = one(v_val).V_LIN[801]()
        self.assertEqual(v_lin.Value, '1')
        
    @prebuild_docstring
    def test_positive_real(self):
        '''return 1.1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 10)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'real')
        
        v_lrl = one(v_val).V_LRL[801]()
        self.assertEqual(v_lrl.Value, '1.1')
        
    @prebuild_docstring
    def test_negative_real(self):
        '''return -1.1;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 11)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'real')
        
        v_uny = one(v_val).V_UNY[801]()
        self.assertEqual(v_uny.Operator, '-')

        v_val = one(v_uny).V_VAL[804]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 9)
        self.assertEqual(v_val.EndPosition, 11)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'real')
        
        v_lrl = one(v_val).V_LRL[801]()
        self.assertEqual(v_lrl.Value, '1.1')
        
    @prebuild_docstring
    def test_string(self):
        '''return "Hello";'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 14)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'string')
        
        v_lst = one(v_val).V_LST[801]()
        self.assertEqual(v_lst.Value, 'Hello')
        
    @prebuild_docstring
    def test_empty_string(self):
        '''return "";'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 9)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'string')
        
        v_lst = one(v_val).V_LST[801]()
        self.assertEqual(v_lst.Value, '')
        
    @prebuild_docstring
    def test_true(self):
        '''return True;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 11)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'boolean')
        
        v_lbo = one(v_val).V_LBO[801]()
        self.assertEqual(v_lbo.Value, 'TRUE')
        
    @prebuild_docstring
    def test_false_1(self):
        '''return False;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 12)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'boolean')
        
        v_lbo = one(v_val).V_LBO[801]()
        self.assertEqual(v_lbo.Value, 'FALSE')
        
    @prebuild_docstring
    def test_false_2(self):
        '''return FaLsE;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 12)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'boolean')
        
        v_lbo = one(v_val).V_LBO[801]()
        self.assertEqual(v_lbo.Value, 'FALSE')
        
    @prebuild_docstring
    def test_enum(self):
        '''return DayOfWeek::Monday;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 24)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'DayOfWeek')
        
        s_enum = one(v_val).V_LEN[801].S_ENUM[824]()
        self.assertEqual(s_enum.Name, 'Monday')

    @prebuild_docstring
    def test_named_string(self):
        '''return CNST::STR;'''
        act_ret = self.metamodel.select_one('ACT_RET')
        self.assertIsNotNone(act_ret)
        
        act_smt = one(act_ret).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)
        
        v_val = one(act_ret).V_VAL[668]()
        self.assertEqual(v_val.isLValue, False)
        self.assertEqual(v_val.isImplicit, False)
        self.assertEqual(v_val.LineNumber, 1)
        self.assertEqual(v_val.StartPosition, 8)
        self.assertEqual(v_val.EndPosition, 16)
        
        s_dt = one(v_val).S_DT[820]()
        self.assertEqual(s_dt.Name, 'string')
        
        cnst_syc = one(v_val).V_SCV[801].CNST_SYC[850]()
        self.assertEqual(cnst_syc.Name, 'STR')

    def test_unknown_named_const(self):
        s_sync = self.metamodel.select_any('S_SYNC')
        s_sync.Action_Semantics_internal = 'return CNST::MISS_SPELLED;'
        s_sync.Suc_Pars = 1

        self.assertRaises(Exception,
                          prebuild.prebuild_model,
                          self.metamodel)

        
if __name__ == "__main__":
    import logging
    import unittest
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    

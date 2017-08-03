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


class TestCreate(PrebuildFunctionTestCase):

    def setUp(self):
        PrebuildFunctionTestCase.setUp(self)
        pe_pe = self.metamodel.new('PE_PE')
        o_obj = self.metamodel.new('O_OBJ', Key_Lett='A')
        relate(pe_pe, o_obj, 8001)
    
    @prebuild_docstring
    def test_create_object(self):
        '''
        create object instance inst of A;
        '''
        act_cr = self.metamodel.select_one('ACT_CR')
        self.assertTrue(act_cr.is_implicit)
        
        act_smt = one(act_cr).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)

        v_var = one(act_cr).V_VAR[633]()
        self.assertEqual(v_var.Name, 'inst')
        
        s_dt = one(v_var).S_DT[848]()
        self.assertEqual(s_dt.Name, 'inst_ref<Object>')
        
        self.assertTrue(one(v_var).V_INT[814]())
        
        o_obj = one(act_cr).O_OBJ[671]()
        self.assertEqual(o_obj.Key_Lett, 'A')
        
    @prebuild_docstring
    def test_create_object_no_variable(self):
        '''
        create object instance of A;
        '''
        act_cnv = self.metamodel.select_one('ACT_CNV')

        act_smt = one(act_cnv).ACT_SMT[603]()
        self.assertIsNotNone(act_smt)

        o_obj = one(act_cnv).O_OBJ[672]()
        self.assertEqual(o_obj.Key_Lett, 'A')
        
        
if __name__ == "__main__":
    import logging
    import unittest
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    

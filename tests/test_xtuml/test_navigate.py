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
import bridgepoint


class TestNavigation(unittest.TestCase):
    '''
    Test suite for xtuml navigate operations
    '''
    def setUp(self):
        self.m = bridgepoint.load_metamodel()

    def tearDown(self):
        del self.m

    def test_navigate_one(self):
        s_dt = self.m.select_any('S_DT',  xtuml.where_eq(Name='void'))
        pe_pe = xtuml.navigate_one(s_dt).PE_PE[8001](lambda inst: True)
        self.assertEqual(s_dt.DT_ID, pe_pe.Element_ID)
        
    def test_navigate_many(self):
        s_dt = self.m.select_many('S_DT')
        pe_pe = xtuml.navigate_many(s_dt).PE_PE[8001](lambda inst: True)
        self.assertEqual(len(s_dt), len(pe_pe))
   
    def test_navigate_suptype(self):
        s_dt = self.m.select_any('S_DT', xtuml.where_eq(Name='void'))
        s_cdt = xtuml.navigate_subtype(s_dt, 17)
        self.assertTrue(s_cdt)
        self.assertIsInstance(s_cdt, self.m.find_class('S_CDT'))

    def test_navigate_assoc(self):
        s_sys = self.m.new('S_SYS')
        g_eis = self.m.new('G_EIS')
        s_dt = self.m.select_any('S_DT', xtuml.where_eq(Name='void'))
        pe_pe = xtuml.navigate_one(s_dt).PE_PE[8001]()
        
        self.assertTrue(xtuml.relate(g_eis, s_sys, 9100))
        self.assertTrue(xtuml.relate(g_eis, pe_pe, 9100))
        
        self.assertTrue(xtuml.navigate_one(s_sys).G_EIS[9100].PE_PE[9100]())
        self.assertTrue(xtuml.navigate_one(pe_pe).G_EIS[9100].S_SYS[9100]())
        
        inst = xtuml.navigate_one(pe_pe).S_SYS[9100]()
        self.assertEqual(inst, s_sys)
        
    def test_navigate_none(self):
        self.assertIsNone(xtuml.navigate_one(None)())
        self.assertIsNone(xtuml.navigate_subtype(None, 0))
        self.assertEqual(len(xtuml.navigate_many(None)()), 0)

    def test_navigate_invalid_handle(self):
        self.assertRaises(xtuml.MetaException, xtuml.navigate_one, 50)

        
if __name__ == "__main__":
    unittest.main()


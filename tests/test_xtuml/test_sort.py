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

class TestSortReflexive(unittest.TestCase):
    '''
    Test suite for xtuml relate/unrelate operations
    '''
    def setUp(self):
        self.m = bridgepoint.load_metamodel()

    def tearDown(self):
        del self.m

    def test_sort(self):
        act_blk = self.m.new('ACT_BLK')
        
        prev = None
        for idx in range(10):
            inst = self.m.new('ACT_SMT', LineNumber=idx)
            self.assertTrue(xtuml.relate(inst, act_blk, 602))
            xtuml.relate(prev, inst, 661, 'precedes')
            prev = inst
            
        inst_set = xtuml.navigate_many(act_blk).ACT_SMT[602]()
        inst_set = xtuml.sort_reflexive(inst_set, 661, 'succeeds')
        self.assertEqual(len(inst_set), 10)
        for idx, inst in enumerate(inst_set):
            self.assertEqual(inst.LineNumber, idx)
        
        inst_set = xtuml.navigate_many(act_blk).ACT_SMT[602]()
        inst_set = xtuml.sort_reflexive(inst_set, 661, 'precedes')
        self.assertEqual(len(inst_set), 10)
        for idx, inst in enumerate(inst_set):
            self.assertEqual(inst.LineNumber, 9 - idx)

    def test_invalid_arguments(self):
        self.assertRaises(xtuml.MetaException, xtuml.sort_reflexive, [], 1, '')
    
    def test_empty_set(self):
        inst_set = self.m.select_many('S_BPARM')
        inst_set = xtuml.sort_reflexive(inst_set, 55, 'precedes')
        self.assertFalse(inst_set)
        
    def test_unknown_phrase(self):
        for _ in range(5):
            self.m.new('S_BPARM')
            
        inst_set = self.m.select_many('S_BPARM')
        self.assertRaises(xtuml.UnknownLinkException, 
                          xtuml.sort_reflexive,
                          inst_set, 55, '<invalid phrase>')

    def test_recursion(self):
        p1 = self.m.new('S_BPARM', Name='p1')
        p2 = self.m.new('S_BPARM', Name='p2')
        p3 = self.m.new('S_BPARM', Name='p3')
        p4 = self.m.new('S_BPARM', Name='p4')
        
        self.assertTrue(xtuml.relate(p1, p2, 55, 'precedes'))
        self.assertTrue(xtuml.relate(p2, p3, 55, 'precedes'))
        self.assertTrue(xtuml.relate(p3, p4, 55, 'precedes'))
        self.assertTrue(xtuml.relate(p4, p1, 55, 'precedes'))
        
        inst_set = self.m.select_many('S_BPARM')
        inst_set = xtuml.sort_reflexive(inst_set, 55, 'succeeds')

        self.assertEqual(len(inst_set), 4)
        for inst1, inst2 in zip(inst_set, [p1, p2, p3, p4]):
            self.assertEqual(inst1, inst2)

    def test_unknown_link(self):
        p1 = self.m.new('S_BPARM', Name='p1')
        p2 = self.m.new('S_BPARM', Name='p2')
        
        self.assertTrue(xtuml.relate(p1, p2, 55, 'precedes'))
        
        inst_set = self.m.select_many('S_BPARM')
        self.assertRaises(xtuml.UnknownLinkException,
                          xtuml.sort_reflexive, inst_set, 5, 'precedes')
    
if __name__ == "__main__":
    unittest.main()


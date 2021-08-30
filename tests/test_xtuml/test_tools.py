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

import sys
import unittest
import pytest

import xtuml.tools


class Node(object):
    '''
    Test Node used for testing xtuml.tools.NodePrintVisitor
    '''
    def __init__(self):
        self.children = list()
        

class TestNodePrinter(unittest.TestCase):
    '''
    Test the walker and visitor in xtuml.tools
    '''
    def test_node(self):
        w = xtuml.tools.Walker()
        w.visitors.append(xtuml.tools.NodePrintVisitor())
        
        root = Node()
        root.children.append(Node())
        root.children.append(Node())
        
        w.accept(root)
        
        try:
            s = sys.stdout.getvalue()
        except AttributeError:
            s, _ = self.capfd.readouterr()

        expected  = 'Node\n'
        expected += '  Node\n'
        expected += '  Node\n'
        
        self.assertEqual(s, expected)
        
    def test_generic_class(self):
        w = xtuml.tools.Walker()
        w.visitors.append(xtuml.tools.NodePrintVisitor())
        
        w.accept(self)
        
        try:
            s = sys.stdout.getvalue()
        except AttributeError:
            s, _ = self.capfd.readouterr()
        
        self.assertEqual(s, 'TestNodePrinter\n')

    def test_none(self):
        w = xtuml.tools.Walker()
        w.visitors.append(xtuml.tools.NodePrintVisitor())
        
        w.accept(None)
        
        try:
            s = sys.stdout.getvalue()
        except AttributeError:
            s, _ = self.capfd.readouterr()
        
        self.assertEqual(s, '')

    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.capfd = capfd


class TestIdGenerator(unittest.TestCase):
    '''
    Test suite for the IdGenerator classes
    '''

    def test_next_pattern(self):
        i = xtuml.IntegerGenerator()
        self.assertEqual(i.peek(), 1)
        self.assertEqual(i.next(), 1)
        self.assertEqual(i.next(), 2)
        self.assertEqual(i.peek(), 3)
        self.assertEqual(i.peek(), 3)

    def test_generator_pattern(self):
        i = xtuml.IntegerGenerator()
        count = 1
        for v in i:
            self.assertEqual(v, count)
            count += 1
            if count == 10:
                break


class TestOrderedSet(unittest.TestCase):
    '''
    Test suite for the class xtuml.OrderedSet
    '''
    
    def test_equal_operator(self):
        s1 = xtuml.OrderedSet()
        s2 = xtuml.OrderedSet()
        
        self.assertEqual(s1, s2)
        
        s1 = xtuml.OrderedSet([1])
        s2 = xtuml.OrderedSet([1])
        
        self.assertEqual(s1, s2)
        
        s1 = xtuml.OrderedSet([1, 2, 3])
        s2 = xtuml.OrderedSet([1, 2, 3])
        
        self.assertEqual(s1, s2)
        self.assertEqual(s1, [1, 2, 3])
        
    def test_not_equal_operator(self):
        s1 = xtuml.OrderedSet()
        s2 = xtuml.OrderedSet([1])
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s2, s1)
        
        s1 = xtuml.OrderedSet([1, 2, 3])
        s2 = xtuml.OrderedSet([1, 3])
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s2, s1)
        
        s1 = xtuml.OrderedSet([1, 2, 3])
        s2 = xtuml.OrderedSet([1, 3, 2])
        self.assertNotEqual(s1, s2)
        
    def test_pop_empty(self):
        q = xtuml.OrderedSet()
        self.assertRaises(KeyError, q.pop)

    def test_pop_last(self):
        s1 = xtuml.OrderedSet([1, 2])
        s2 = xtuml.OrderedSet([1])
        self.assertNotEqual(s1, s2)

        s1.pop()
        self.assertEqual(s1, s2)
        
    def test_pop_first(self):
        s1 = xtuml.OrderedSet([2, 1])
        s2 = xtuml.OrderedSet([1])
        self.assertNotEqual(s1, s2)

        s1.pop(last=False)
        self.assertEqual(s1, s2)


if __name__ == "__main__":
    unittest.main()


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
import bridgepoint.gen_xsd_schema
import xtuml
import tempfile
import os

import xml.etree.ElementTree as ET


simple_model = (os.path.dirname(__file__) + os.path.sep + os.path.pardir +
                os.path.sep + 'resources' + os.path.sep + 'Simple_Model.xtuml')


class TestSchemaGen(unittest.TestCase):
    
    def test_build_component(self):
        l = bridgepoint.ModelLoader()
        l.filename_input(simple_model)
        m = l.build_component()
        
        cls = m.new('Class')
        self.assertTrue(cls.Id)
        
        supertype = m.new('Supertype')
        subtype = m.new('Subtype')
        self.assertTrue(xtuml.relate(supertype, subtype, 2))
        self.assertTrue(xtuml.relate(supertype, cls, 3))
        self.assertTrue(supertype.Id)
        self.assertTrue(subtype.Id)
        
        reflexive_class1 = m.new('Reflexive_Class')
        reflexive_class2 = m.new('Reflexive_Class')
        self.assertTrue(xtuml.relate(reflexive_class1, cls, 4))
        self.assertTrue(xtuml.relate(reflexive_class2, cls, 4))
        
        assoc_class = m.new('Assoc_Class')
        self.assertTrue(xtuml.relate(reflexive_class1, assoc_class, 1, 'one'))
        self.assertTrue(xtuml.relate(reflexive_class2, assoc_class, 1, 'other'))

    def test_gen_xsd(self):
        outfile = tempfile.mktemp()
        args = ['-c', 'Comp', '-o', outfile, simple_model]
        bridgepoint.gen_xsd_schema.main(args)
        
        ns = 'http://www.w3.org/2001/XMLSchema'
        tree = ET.parse(outfile)
        
        self.assertTrue(tree.findall(".//{%s}simpleType[@name='boolean']" % ns))
        self.assertTrue(tree.findall(".//{%s}simpleType[@name='integer']" % ns))
        self.assertTrue(tree.findall(".//{%s}simpleType[@name='real']" % ns))
        self.assertTrue(tree.findall(".//{%s}simpleType[@name='string']" % ns))
        self.assertTrue(tree.findall(".//{%s}simpleType[@name='unique_id']" % ns))
        self.assertTrue(tree.findall(".//{%s}simpleType[@name='My_Enum']" % ns))
        self.assertTrue(tree.findall(".//{%s}enumeration[@value='E1']" % ns))
        self.assertTrue(tree.findall(".//{%s}simpleType[@name='My_Integer']" % ns))
        self.assertTrue(tree.findall(".//{%s}element[@name='Comp']" % ns))
        self.assertTrue(tree.findall(".//{%s}attribute[@name='One_Id']" % ns))

        
if __name__ == "__main__":
    unittest.main()
    

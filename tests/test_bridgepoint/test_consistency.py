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

import os
import unittest

import bridgepoint.consistency_check


class TestConcistencyCLI(unittest.TestCase):
    '''
    Test suite for the bridgepoint.consistency_check 
    command line interface.
    '''
    def main(self, *args):
        try:
            return bridgepoint.consistency_check.main(list(args))
        except SystemExit as e:
            return e.code
    
    def test_no_args(self):
        rc = self.main()
        self.assertEqual(1, rc)
        
    def test_auto_include_globals(self):
        path = (os.path.dirname(__file__) + os.sep + os.pardir + os.sep + 
                'resources' + os.sep + 'Globals.xtuml')
                
        rc = self.main(path)
        self.assertEqual(0, rc)
        
        rc = self.main(path, '-g')
        self.assertNotEqual(0, rc)
        
    def test_limit_searchspace(self):
        path = (os.path.dirname(__file__) + os.sep + os.pardir + os.sep + 
                'resources' + os.sep + 'Globals.xtuml')

        rc = self.main(path, '-g')
        self.assertNotEqual(0, rc)
        
        rc = self.main(path, '-g', '-k', 'O_OBJ', '-r', '0')
        self.assertEqual(0, rc)
        

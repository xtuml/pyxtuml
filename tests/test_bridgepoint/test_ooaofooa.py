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
import atexit
import os
import shutil
import unittest
import xtuml
from bridgepoint import ooaofooa


class TestOoaOfOoa(unittest.TestCase):

    def test_remove_globals(self):
        m = ooaofooa.empty_model(load_globals=False)
        s = xtuml.serialize_instances(m)
        self.assertFalse(s)
        
        m = ooaofooa.empty_model(load_globals=True)
        s = xtuml.serialize_instances(m)
        self.assertTrue(s)
        
        ooaofooa.delete_globals(m)
        s = xtuml.serialize_instances(m)
        self.assertFalse(s)
        
    def test_folder_input(self):
        dirname = os.path.dirname(__file__) + os.sep + '..' + os.sep + 'resources'
        metamodel = ooaofooa.load_metamodel(dirname, load_globals=False)
        self.assertTrue(metamodel.select_any('S_DT', xtuml.where_eq(Name='integer')) is not None)

    def test_zipfile_input(self):
        dirname = os.path.dirname(__file__) + os.sep + '..' + os.sep + 'resources'
        zipfile = shutil.make_archive(dirname, 'zip', dirname)
        atexit.register(os.remove, zipfile)

        metamodel = ooaofooa.load_metamodel(zipfile, load_globals=False)
        self.assertTrue(metamodel.select_any('S_DT', xtuml.where_eq(Name='integer')) is not None)
        
        
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    

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
        
    
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    

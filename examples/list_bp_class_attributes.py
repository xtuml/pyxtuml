#!/usr/bin/env python
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

from xtuml import navigate_one as one
from xtuml import navigate_many as many
from bridgepoint import ooaofooa


if len(sys.argv) < 2:
    print('')
    print('  usage: %s <path to bridgepoint model folder>' % sys.argv[0])
    print('')
    sys.exit(1)

    
m = ooaofooa.load_metamodel(sys.argv[1])


by_name = lambda inst: inst.Name
for o_obj in sorted(m.select_many('O_OBJ'), key=by_name):
    print(o_obj.Name)

    for o_attr in sorted(many(o_obj).O_ATTR[102](), key=by_name):
        s_dt = one(o_attr).S_DT[114]()
        print('   %s : %s' % (o_attr.Name, s_dt.Name))


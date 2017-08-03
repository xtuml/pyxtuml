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
from bridgepoint import ooaofooa


if len(sys.argv) < 2:
    print('')
    print('  usage: %s <path to bridgepoint model folder>' % sys.argv[0])
    print('')
    sys.exit(1)

    
m = ooaofooa.load_metamodel(sys.argv[1])


get_name = lambda inst: one(inst).S_DT[17]().Name
for s_edt in sorted(m.select_many('S_EDT'), key=get_name):
    print(get_name(s_edt))

    is_first = lambda inst: not one(inst).S_ENUM[56, 'succeeds']()
    s_enum = one(s_edt).S_ENUM[27](is_first)
    while s_enum:
        print('    %s' % s_enum.Name)
        s_enum = one(s_enum).S_ENUM[56, 'precedes']()


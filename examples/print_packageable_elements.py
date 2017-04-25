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
import xtuml

from xtuml import navigate_many as many
from xtuml import navigate_subtype as subtype

from bridgepoint import ooaofooa


class MyWalker(xtuml.Walker):
    '''
    Walk the ooaofooa packageable element tree-like structure
    '''
    
    def accept_S_SYS(self, inst):
        '''
        A System Model contains top-level packages
        '''
        for child in many(inst).EP_PKG[1401]():
            self.accept(child)
    
    def accept_PE_PE(self, inst):
        '''
        Packeable Element is the supertype of something packageable
        '''
        self.accept(subtype(inst, 8001))

    def accept_C_C(self, inst):
        '''
        A Component contains packageable elements
        '''
        for child in many(inst).PE_PE[8003]():
            self.accept(child)
            
    def accept_EP_PKG(self, inst):
        '''
        A Package contains packageable elements
        '''
        for child in many(inst).PE_PE[8000]():
            self.accept(child)


class MyPrinter(xtuml.NodePrintVisitor):

    def render_PE_PE(self, inst):
        '''suppress instances of PE_PE'''
        pass
    
    def render_O_IOBJ(self, inst):
        '''suppress imported classes'''
        pass
    
    def render_R_REL(self, inst):
        return 'R%d (Association)' % inst.Numb
    
    def default_render(self, inst):
        if hasattr(inst, 'Name'):
            return '%s (%s)' % (inst.Name, type(inst).__name__)
        else:
            return type(inst).__name__

    
if len(sys.argv) < 2:
    print('')
    print('  usage: %s <path to bridgepoint model folder>' % sys.argv[0])
    print('')
    sys.exit(1)



m = ooaofooa.load_metamodel(sys.argv[1:])

w = MyWalker()
w.visitors.append(MyPrinter())

for s_sys in m.select_many('S_SYS'):
    w.accept(s_sys)


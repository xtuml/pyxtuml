# encoding: utf-8
# Copyright (C) 2020 John Törnblom
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

import importlib.abc
import importlib.machinery

import types
import sys
import os.path

from bridgepoint import ooaofooa


def _get_version(filename):
    with open(filename, 'r') as f:
        line = f.readline()
        _, value = line.split("persistence-version: ", 1)
        return  value.strip()


def _check_magic(filename):
    if not os.path.exists(filename):
        return False
    
    with open(filename, 'r') as f:
        line = f.readline()
        return 'content: SystemModel' in line


class ModelLoader(importlib.abc.Loader):
    models_path = None
    
    def __init__(self, models_path):
        self.models_path = models_path
        
    def create_module(self, spec):
        module = types.ModuleType(spec.name)
        bp_model = ooaofooa.load_metamodel(self.models_path)
        
        for c_c in bp_model.select_many('C_C'):
            comp = ooaofooa.mk_component(bp_model, c_c)
            setattr(module, c_c.name, comp)

        return module
    
    def exec_module(self, module):
        pass


class ModelFinder(importlib.abc.MetaPathFinder):
    
    def find_spec(self, fullname, path, target=None):
        if not fullname:
            return

        names = fullname.split('.')
        project_name = names[-1]
        
        for f in sys.path:
            models_path =  os.path.join(os.path.realpath(f), 'models')
            project_path = os.path.join(models_path, project_name)
            source = os.path.join(project_path, project_name + '.xtuml')
            if _check_magic(source):
                loader = ModelLoader(models_path)
                return importlib.machinery.ModuleSpec(fullname, loader, is_package=True)


def install():
    if ModelFinder not in sys.meta_path:
        sys.meta_path.append(ModelFinder())



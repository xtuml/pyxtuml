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


class ModelImporter(object):
    
    def __init__(self, path):
        self.path = path
        
    @classmethod
    def find_module(cls, fullname, paths=None):
        if paths is None:
            paths = sys.path
                        
        names = fullname.split('.')
        model_name = names[-1]
        
        for f in paths:
            path = os.path.join(os.path.realpath(f), 'models')
            path = os.path.join(path, model_name)
            source = os.path.join(path, model_name + '.xtuml')
            if _check_magic(source):
                return cls(path)
    
    def get_code(self, module):
        pass

    def get_data(self, module):
        pass

    def get_filename(self, name):
        pass

    def get_source(self, name):
        pass

    def is_package(self, *args, **kwargs):
        return False

    def load_module(self, fullname):
        l = ooaofooa.Loader()
        l.filename_input(self.path)
        return l


def install():
    if ModelImporter not in sys.meta_path:
        sys.meta_path.append(ModelImporter)


def remove():
    sys.meta_path.remove(ModelImporter)


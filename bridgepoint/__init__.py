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

from .prebuild import prebuild_action
from .prebuild import prebuild_model

from .sourcegen import gen_text_action

from .ooaofooa import ModelLoader
from .ooaofooa import load_metamodel
from .ooaofooa import load_component

# loading ooaofooa models with import sytnax is only
# supported when running python 3.
if sys.version_info >= (3, 0):
    from bridgepoint import imp
    imp.install()

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
import logging

from setuptools import setup

logging.basicConfig(level=logging.DEBUG)

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst')) as f:
    long_description = f.read()

setup(name='pyxtuml',
      version='3.0.0', # ensure that this is the same as in xtuml.version
      description='Library for parsing, manipulating, and generating BridgePoint xtUML models',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author=u'John Törnblom',
      author_email='john.tornblom@gmail.com',
      url='https://github.com/xtuml/pyxtuml',
      license='LGPLv3+',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Code Generators',
          'Topic :: Software Development :: Compilers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Programming Language :: Python :: 3 :: Only'],
      keywords='xtuml bridgepoint',
      packages=['xtuml', 'bridgepoint'],
      requires=['ply'],
      install_requires=['ply'],
      setup_requires=['ply'])

# assure PLY parstab and lextab get generated for OAL and SQL parsers
import xtuml
ml = xtuml.ModelLoader()
ml.input('')
m = ml.build_metamodel()
import bridgepoint.oal
bridgepoint.oal.parse('')

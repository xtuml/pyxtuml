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
import unittest
import sys

try:
    from setuptools import setup
    from setuptools import Command
    from setuptools.command.build_py import build_py
except ImportError:
    from distutils.core import setup
    from distutils.core  import Command
    from distutils.command.build_py import build_py


logging.basicConfig(level=logging.DEBUG)


class BuildCommand(build_py):
    
    def run(self):
        import xtuml
        from bridgepoint import oal

        l = xtuml.ModelLoader()
        l.input('', name='<empty string>')
        l.build_metamodel()
        oal.parse('')
        build_py.run(self)


class TestCommand(Command):
    description = "Execute unit tests"
    user_options = [('name=', None, 'Limit testing to a single test case or test method')]

    def initialize_options(self):
        self.name = None
    
    def finalize_options(self):
        if self.name and not self.name.startswith('tests.'):
            self.name = 'tests.' + self.name

    def run(self):
        if self.name:
            suite = unittest.TestLoader().loadTestsFromName(self.name)
        else:
            suite = unittest.TestLoader().discover('tests')
        
        runner = unittest.TextTestRunner(verbosity=2, buffer=True)
        exit_code = not runner.run(suite).wasSuccessful()
        sys.exit(exit_code)


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst')) as f:
    long_description = f.read()

setup(name='pyxtuml',
      version='2.3.1', # ensure that this is the same as in xtuml.version
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
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'],
      keywords='xtuml bridgepoint',
      packages=['xtuml', 'bridgepoint'],
      requires=['ply'],
      install_requires=['ply'],
      setup_requires=['ply'],
      cmdclass={'build_py': BuildCommand,
                'test': TestCommand}
      )


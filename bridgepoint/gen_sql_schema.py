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
'''
Generate an sql schema file for an xtUML model. 
The arguments are either xtuml files, or folders containing *.xtuml files.
Note that some type of attributes are not supported, e.g. instance handles or
timers.
'''

import sys
import optparse
import logging

import xtuml

from . import ooaofooa


logger = logging.getLogger('gen_sql_schema')


def main():
    '''
    Parse argv for options and arguments, and start schema generation.
    '''
    parser = optparse.OptionParser(usage="%prog [options] <model_path> [another_model_path...]",
                                   version=xtuml.version.complete_string,
                                   formatter=optparse.TitledHelpFormatter())
                                   
    parser.set_description(__doc__.strip())
    
    parser.add_option("-c", "--component", dest="component", metavar="NAME",
                      help="export sql schema for the component named NAME",
                      action="store", default=None)
    
    parser.add_option("-d", "--derived-attributes", dest="derived",
                      help="include derived attributes in the schema",
                      action="store_true", default=False)
    
    parser.add_option("-o", "--output", dest='output', metavar="PATH",
                      help="save sql schema to PATH (required)",
                      action="store", default=None)
    
    parser.add_option("-v", "--verbosity", dest='verbosity', action="count", 
                      help="increase debug logging level", default=2)

    
    (opts, args) = parser.parse_args()
    if len(args) == 0 or opts.output is None:
        parser.print_help()
        sys.exit(1)

    levels = {
              0: logging.ERROR,
              1: logging.WARNING,
              2: logging.INFO,
              3: logging.DEBUG,
    }
    logging.basicConfig(level=levels.get(opts.verbosity, logging.DEBUG))

    loader = ooaofooa.Loader()
    for filename in args:
        loader.filename_input(filename)

    c = loader.build_component(opts.component, opts.derived)
    xtuml.persist_database(c, opts.output)

    
if __name__ == '__main__':
    main()


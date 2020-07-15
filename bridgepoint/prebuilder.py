#!/usr/bin/env python
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
'''
Command line interface for module bridgepoint.prebuild.
'''

import logging
import optparse
import sys

import xtuml
import bridgepoint

from bridgepoint import ooaofooa


def main():
    '''
    Parse command line options and launch the prebuilder.
    '''
    parser = optparse.OptionParser(usage="%prog [options] <model_path> [another_model_path..]",
                                   version=xtuml.version.complete_string,
                                   formatter=optparse.TitledHelpFormatter())

    parser.add_option("-v", "--verbosity", dest='verbosity',
                                           action="count",
                                           help="increase debug logging level",
                                           default=1)
    
    parser.add_option("-o", "--output", dest="output", metavar="PATH",
                                        help="set output to PATH",
                                        action="store",
                                        default=None)
    
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
    
    m = ooaofooa.load_metamodel(args)
    bridgepoint.prebuild_model(m)
    
    xtuml.persist_instances(m, opts.output)


if __name__ == '__main__':
    main()
    

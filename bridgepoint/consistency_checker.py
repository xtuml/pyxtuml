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
Check a bridgepoint model for association constraint violations in its 
metamodel (ooaofooa).
'''

import logging
import optparse
import sys
import xtuml
from bridgepoint import ooaofooa


logger = logging.getLogger('consistency_check')


def main(args):
    parser = optparse.OptionParser(usage="%prog [options] <model_path> [another_model_path...]",
                                   version=xtuml.version.complete_string,
                                   formatter=optparse.TitledHelpFormatter())
    
    parser.set_description(__doc__.strip())
    
    parser.add_option("-r", "-R", dest="rel_ids", type='int', metavar="<number>",
                      help="limit consistency check to one or more associations",
                      action="append", default=[])

    parser.add_option("-k", dest="kinds", type='string', metavar="<key letter>",
                      help="limit check for uniqueness constraint violations to one or more classes",
                      action="append", default=[])
    
    parser.add_option("-g", "--globals", dest="globals",
                      help="add builtin global data types automatically, e.g. boolean, integer and real",
                      action="store_true", default=False)
                      
    parser.add_option("-v", "--verbosity", dest='verbosity', action="count",
                      help="increase debug logging level", default=1)
    
    (opts, args) = parser.parse_args(args)
    if len(args) == 0:
        parser.print_help()
        sys.exit(1)
        
    levels = {
              0: logging.ERROR,
              1: logging.WARNING,
              2: logging.INFO,
              3: logging.DEBUG,
    }
    logging.basicConfig(level=levels.get(opts.verbosity, logging.DEBUG))
    
    loader = ooaofooa.Loader(load_globals=opts.globals)
    for filename in args:
        loader.filename_input(filename)

    m = loader.build_metamodel()
    
    error = 0
    for rel_id in opts.rel_ids:
        error += xtuml.check_association_integrity(m, rel_id)
    
    if not opts.rel_ids:
        error += xtuml.check_association_integrity(m)

    for kind in opts.kinds:
        error += xtuml.check_uniqueness_constraint(m, kind)
    
    if not opts.kinds:
        error += xtuml.check_uniqueness_constraint(m)
    
    return error
    

if __name__ == '__main__':
    num_errors = main(sys.argv[1:])
    sys.exit(num_errors > 0)

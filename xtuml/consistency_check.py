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
Check an xtuml model for association constraint violations in its metamodel.
'''

import logging
import optparse
import sys
import xtuml


logger = logging.getLogger('consistency_check')


def pretty_to_link(inst, link):
    '''
    Create a human-readable representation of a link on the 'TO'-side
    '''
    values = ''
    prefix = ''
    metaclass = inst.__metaclass__

    for name, ty in metaclass.attributes:
        if name in link.key_map:
            value = getattr(inst, name)
            value = xtuml.serialize_value(value, ty)
            name = link.key_map[name]
            values += '%s%s=%s' % (prefix, name, value)
            prefix = ', '
                
    return '%s(%s)' % (link.kind, values)
        

def pretty_from_link(inst, link):
    '''
    Create a human-readable representation of a link on the 'FROM'-side
    '''
    values = ''
    prefix = ''
    metaclass = inst.__metaclass__
    
    for name, ty in metaclass.attributes:
        if name in link.key_map:
            value = getattr(inst, name)
            value = xtuml.serialize_value(value, ty)
            values += '%s%s=%s' % (prefix, name, value)
            prefix = ', '
                
    return '%s(%s)' % (metaclass.kind, values)


def pretty_unique_identifier(inst, identifier):
    '''
    Create a human-readable representation a unique identifier.
    '''
    values = ''
    prefix = ''
    metaclass = inst.__metaclass__
    
    for name, ty in metaclass.attributes:
        if name in metaclass.identifying_attributes:
            value = getattr(inst, name)
            value = xtuml.serialize_value(value, ty)
            values += '%s%s=%s' % (prefix, name, value)
            prefix = ', '
                    
    return '%s(%s)' % (identifier, values)


def check_uniqueness_constraint(m, kind=None):
    '''
    Check the model for uniqueness constraint violations.
    '''
    if kind is None:
        metaclasses = m.metaclasses.values()
    else:
        metaclasses = [m.find_metaclass(kind)]
    
    res = 0
    for metaclass in metaclasses:
        for inst in metaclass.select_many():
            
            for name, ty in metaclass.attributes:
                if name not in metaclass.identifying_attributes:
                    continue
                
                value = getattr(inst, name)
                isnull = value is None
                isnull |= (ty == 'UNIQUE_ID' and not value)
                if isnull:
                    res += 1 
                    logger.warning('%s.%s is part of an identifier and is null' 
                                   % (metaclass.kind, name))
            
            
            for identifier in metaclass.indices:
                kwargs = dict()
                for name in metaclass.indices[identifier]:
                    kwargs[name] = getattr(inst, name)
                
                where_clause = xtuml.where_eq(**kwargs)
                s = metaclass.select_many(where_clause)
                if len(s) > 1:
                    res += 1
                    id_string = pretty_unique_identifier(inst, identifier)
                    logger.warning('uniqueness constraint violation in %s, %s' 
                                   % (metaclass.kind, id_string))

    return res


def check_link_integrity(m, link):
    '''
    Check the model for integrity violations on an association in a particular direction.
    '''
    res = 0
    for inst in link.from_metaclass.select_many():
        q_set = list(link.navigate(inst))

        if(len(q_set) < 1 and not link.conditional) or (
          (len(q_set) > 1 and not link.many)):
            res += 1
            logger.warning('integrity violation in '
                           '%s --(%s)--> %s' % (pretty_from_link(inst, link),
                                                link.rel_id,
                                                pretty_to_link(inst, link)))
    
    return res


def check_subtype_integrity(m, super_kind, rel_id):
    '''
    Check the model for integrity violations across a subtype association.
    '''
    if isinstance(rel_id, int):
        rel_id = 'R%d' % rel_id

    res = 0
    for inst in m.select_many(super_kind):
        if not xtuml.navigate_subtype(inst, rel_id):
            res += 1
            logger.warning('integrity violation across '
                           '%s[%s]' % (super_kind, rel_id))
        
    return res


def check_association_integrity(m, rel_id=None):
    '''
    Check the model for integrity violations on association(s).
    '''
    if isinstance(rel_id, int):
        rel_id = 'R%d' % rel_id
            
    res = 0
    for ass in m.associations:
        if rel_id in [ass.rel_id, None]:
            res += check_link_integrity(m, ass.link)
            res += check_link_integrity(m, ass.reversed_link)

    return res


def main(args):
    parser = optparse.OptionParser(usage="%prog [options] <sql_file> [another_sql_file...].",
                                   version=xtuml.version.complete_string,
                                   formatter=optparse.TitledHelpFormatter())
    
    parser.set_description(__doc__.strip())
    
    parser.add_option("-r", "-R", dest="rel_ids", type='int', metavar="<number>",
                      help="limit consistency check to one or more associations",
                      action="append", default=[])

    parser.add_option("-k", dest="kinds", type='string', metavar="<key letter>",
                      help="limit check for uniqueness constraint violations to one or more classes",
                      action="append", default=[])
    
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
    
    loader = xtuml.ModelLoader()
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


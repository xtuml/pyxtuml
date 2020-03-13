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
Generate the pyxtuml bridgepoint schema module from a bridgepoint metamodel.
'''

import optparse
import string
import sys
import logging
import re
import xtuml

from xtuml import navigate_many as many
from xtuml import navigate_one as one
from xtuml import navigate_subtype as subtype
from xtuml import relate
from xtuml import unrelate
from xtuml import where_eq as where

from bridgepoint import ooaofooa


tmpl = string.Template("""
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
This file was generated by bridgepoint.gen_pyxtuml_schema.
'''

__version__ = '${version}'


classes = '''
${classes}
'''

associations = '''
${associations}
'''

indices = '''
${indices}
'''

globals = '''
${globals}
'''
""")


logger = logging.getLogger('schema_gen')


def parse_keyword(expr, keyword):
    regexp = re.compile(keyword + ":([^\n]*)")
    result = regexp.search(expr)
        
    if result:
        return result.groups()[0].strip().lower()
    else:
        return ''

    
def description_filter(inst):
    description = inst.Descrip.lower()
    keymap = dict(persistent='false',
                  translate_for_external_use='false')
                  
    for key, value in keymap.items():
        if parse_keyword(description, key) == value:
            return True
    

def mk_ooaofooa_component(filename):
    loader = ooaofooa.Loader()
    loader.filename_input(filename)
    
    m = loader.build_metamodel()

    for r_rel in m.select_many('R_REL', description_filter):
        logger.info('Filtering R%d' % r_rel.Numb)
        xtuml.delete(r_rel)

    for o_obj in m.select_many('O_OBJ', description_filter):
        logger.info('Filtering %s' % o_obj.Key_Lett)
        for r_rel in many(o_obj).R_OIR[201].R_REL[201]():
            logger.info('Filtering R%d' % r_rel.Numb)
            for r_oir in many(r_rel).R_OIR[201]():
                xtuml.unrelate(r_rel, r_oir, 201)
                
            xtuml.delete(r_rel)
            
        xtuml.delete(o_obj)

    for o_attr in m.select_many('O_ATTR', where(Name='SMspd_ID')):
        if not one(o_attr).O_RATTR[106]():
            continue
            
        for o_oida in many(o_attr).O_OIDA[105]():
            for o_rtida in many(o_oida).O_RTIDA[110]():
                xtuml.delete(o_rtida)
            xtuml.delete(o_oida)

        for o_ref in many(o_attr).O_RATTR[106].O_REF[108]():
            xtuml.delete(o_ref)
            
    c = ooaofooa.mk_component(m, None, derived_attributes=True)
    metaclass = c.find_metaclass('ACT_ACT')
    metaclass.insert_attribute(index=5, name='return_value', type_name='INTEGER')

    for o_obj in m.select_many('O_OBJ'):
        for o_attr in many(o_obj).O_ATTR[102](description_filter):
            logger.info('Filtering %s.%s' % (o_obj.Key_Lett, o_attr.Name))
            metaclass = c.find_metaclass(o_obj.Key_Lett)
            metaclass.delete_attribute(o_attr.Name)
            
    return c


def main():
    '''
    Parse argv for options and arguments, and start schema generation.
    '''
    parser = optparse.OptionParser(usage="%prog [options] <metamodel_path>",
                                   version=xtuml.version.complete_string,
                                   formatter=optparse.TitledHelpFormatter())
                                   
    parser.set_description(__doc__.strip())
    
    parser.add_option("-o", "--output", dest='output', metavar="PATH",
                      help="save sql schema to PATH (required)",
                      action="store", default=None)

    parser.add_option("-V", "--version-info", dest='vinfo', action="store", 
                      help="Version info for the schema", default='')
    
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

    ooaofooa_path = args[0] + '/src/org.xtuml.bp.core/models/org.xtuml.bp.core/ooaofooa'
    globals_path = args[0] + '/src/org.xtuml.bp.pkg/globals/Globals.xtuml'

    with open(globals_path, 'r') as f:
        globals_instances = f.read()
        
    m = mk_ooaofooa_component(ooaofooa_path)
    
    s = tmpl.substitute(version=opts.vinfo,
                        classes=xtuml.serialize_classes(m).strip(),
                        associations=xtuml.serialize_associations(m).strip(),
                        indices=xtuml.serialize_unique_identifiers(m).strip(),
                        globals=globals_instances.strip())

    with open(opts.output, 'w') as f:
        f.write(s.strip())
        f.write('\n')
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
    
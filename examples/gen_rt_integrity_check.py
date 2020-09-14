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
Generate OAL actions that checks for model integrity violations at runtime.

The following checks are performed: cardinality constraints on associations,
sub types are associated with a super type, and that uniqueness constiants are 
not violated.
'''

import logging
import optparse
import sys
import xtuml

from bridgepoint import ooaofooa
from string import Template

from xtuml import where_eq as where
from xtuml import navigate_many as many
from xtuml import navigate_one as one
from xtuml import navigate_subtype as subtype
from xtuml import relate


logger = logging.getLogger('gen_rt_integrity_check')


constraint_tmpl = Template('''
select many Instances_Of_${Kind} from instances of ${Kind};
for each ${Kind}_Instance in Instances_Of_${Kind}
    select many ${Kind}_Instance_Duplicates from instances of ${Kind} where (${Where_Clause});
    if (cardinality ${Kind}_Instance_Duplicates) != 1
        LOG::LogInfo(message: "Uniqueness violation in ${Kind} I${Numb}");
    end if;
end for;
''')
    
subtype_tmpl = Template('''
select many Instances_Of_${From} from instances of ${From};
for each ${From}_Instance in Instances_Of_${From}
    select ${Cardinality} ${Cardinality}_${To}_Instance related by ${From}_Instance->${To}[R${Numb}];
    if empty ${Cardinality}_${To}_Instance
        LOG::LogInfo(message: "Integrity violation in ${From}->${To}[R${Numb}]");
        return False;
    end if;
end for;
''')


atleast_one_tmpl = Template('''
select many Instances_Of_${From} from instances of ${From};
for each ${From}_Instance in Instances_Of_${From}
    select ${Cardinality} ${Cardinality}_${To}_Instance related by ${From}_Instance->${To}[R${Numb}.'${Phrase}'];
    if empty ${Cardinality}_${To}_Instance
        LOG::LogInfo(message: "Integrity violation in ${From}->${To}[R${Numb}.'${Phrase}']");
        return False;
    end if;
end for;
''')


supertype_loop_tmpl = Template('''
select many Instances_Of_${From} from instances of ${From};
for each ${From}_Instance in Instances_Of_${From}
    $Loop_Body
    LOG::LogInfo(message: "Integrity violation in R${Numb}");
    return False;
end for;
''')


supertype_body_tmpl = Template('''
    select one one_${To}_Instance related by ${From}_Instance->${To}[R${Numb}];
    if not_empty one_${To}_Instance
        continue;
    end if;
''')


def mk_simple_association_check(m, r_simp):
    text = ''
    
    r_rel = one(r_simp).R_REL[206]()
    
    r_part = one(r_simp).R_PART[207]()
    r_rto = one(r_part).R_RTO[204]()
    target_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
    
    r_form = one(r_simp).R_FORM[208]()
    if r_form:
        r_rgo = one(r_form).R_RGO[205]()
        source_o_obj = one(r_rgo).R_OIR[203].O_OBJ[201]()
    else:  # the association is not formalized
        r_form = one(r_simp).R_PART[207](lambda sel: sel != r_part)
        r_rto = one(r_form).R_RTO[204]()
        source_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
    
    if not r_part.Cond:
        if r_part.Mult:
            cardinality = 'many'
        else:
            cardinality = 'one'
            
        text += atleast_one_tmpl.substitute(From=source_o_obj.Key_Lett,
                                            To=target_o_obj.Key_Lett,
                                            Numb=r_rel.Numb,
                                            Cardinality=cardinality,
                                            Phrase=r_part.Txt_Phrs)
    if not r_form.Cond:
        if r_form.Mult:
            cardinality = 'many'
        else:
            cardinality = 'one'
            
        text += atleast_one_tmpl.substitute(From=target_o_obj.Key_Lett,
                                            To=source_o_obj.Key_Lett,
                                            Numb=r_rel.Numb,
                                            Cardinality=cardinality,
                                            Phrase=r_form.Txt_Phrs)
    return text


def mk_linked_association_check(m, r_assoc):
    r_rel = one(r_assoc).R_REL[206]()
    r_rgo = one(r_assoc).R_ASSR[211].R_RGO[205]()
    source_o_obj = one(r_rgo).R_OIR[203].O_OBJ[201]()
    
    def check_link(side):
        r_rto = one(side).R_RTO[204]()
        target_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
        
        if side.Mult:
            cardinality = 'many'
        else:
            cardinality = 'one'
                
        text = atleast_one_tmpl.substitute(From=target_o_obj.Key_Lett,
                                           To=source_o_obj.Key_Lett,
                                           Numb=r_rel.Numb,
                                           Cardinality=cardinality,
                                           Phrase=side.Txt_Phrs)
        if not side.Cond:
            if side.Mult:
                cardinality = 'one'
            else:
                cardinality = 'one'
                
            text += atleast_one_tmpl.substitute(From=source_o_obj.Key_Lett,
                                                To=target_o_obj.Key_Lett,
                                                Numb=r_rel.Numb,
                                                Cardinality=cardinality,
                                                Phrase=side.Txt_Phrs)
        return text
    
    r_aone = one(r_assoc).R_AONE[209]()
    r_aoth = one(r_assoc).R_AOTH[210]()
    
    return check_link(r_aone) + check_link(r_aoth)

    
def mk_subsuper_association_check(m, r_subsup):
    r_rel = one(r_subsup).R_REL[206]()
    r_rto = one(r_subsup).R_SUPER[212].R_RTO[204]()
    target_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
    
    text = ''
    loop_body = ''
    for r_sub in many(r_subsup).R_SUB[213]():
        r_rgo = one(r_sub).R_RGO[205]()
        source_o_obj = one(r_rgo).R_OIR[203].O_OBJ[201]()
        
        text += subtype_tmpl.substitute(From=source_o_obj.Key_Lett,
                                        To=target_o_obj.Key_Lett,
                                        Numb=r_rel.Numb,
                                        Cardinality='one')

        loop_body += supertype_body_tmpl.substitute(From=target_o_obj.Key_Lett,
                                                    To=source_o_obj.Key_Lett,
                                                    Numb=r_rel.Numb)
    
    text += supertype_loop_tmpl.substitute(From=target_o_obj.Key_Lett,
                                           Numb=r_rel.Numb,
                                           Loop_Body=loop_body)

    return text


def mk_derived_association_check(m, r_comp):
    return ''


def mk_unique_constraint_check(m, o_id):
    o_obj = one(o_id).O_OBJ[104]()
    where_clause = prefix = ''
    for o_oida in many(o_id).O_OIDA[105]():
        clause = '(%s.%s == %s_Instance.%s)' % ('selected',
                                                o_oida.localAttributeName,
                                                o_obj.Key_Lett,
                                                o_oida.localAttributeName)
        where_clause += (prefix + clause)
        prefix = ' and '
    
    if not where_clause:
        return ''
    
    return constraint_tmpl.substitute(Kind=o_obj.Key_Lett,
                                      Where_Clause=where_clause,
                                      Numb=o_id.Oid_ID + 1)


def generate_actions(m, c_c, s_sync):
    text = ''
    
    handler = {
        'R_SIMP': mk_simple_association_check,
        'R_ASSOC': mk_linked_association_check,
        'R_SUBSUP': mk_subsuper_association_check,
        'R_COMP': mk_derived_association_check,
    }

    filt = lambda sel: ooaofooa.is_contained_in(sel, c_c)
    for r_rel in m.select_many('R_REL', filt):
        inst = subtype(r_rel, 206)
        fn = handler.get(inst.__class__.__name__)
        text += fn(m, inst)

    o_objs = m.select_many('O_OBJ', filt)
    for o_id in many(o_objs).O_ID[104]():
        text += mk_unique_constraint_check(m, o_id)
    
    text += 'return True;'
    s_sync.Action_Semantics_internal = text
    s_sync.Suc_Pars = 1


def main():
    '''
    Parse argv for options and arguments, and start schema generation.
    '''
    parser = optparse.OptionParser(usage="%prog [options] <model_path> [another_model_path...]",
                                   formatter=optparse.TitledHelpFormatter())
                                   
    parser.set_description(__doc__.strip())
    
    parser.add_option("-f", "--function", dest="function", metavar="NAME",
                      help="append integrity checking actions to functions named NAME (required)",
                      action="store", default=None)
    
    parser.add_option("-o", "--output", dest='output', metavar="PATH",
                      help="save sql model instances to PATH (required)",
                      action="store", default=None)
    
    parser.add_option("-v", "--verbosity", dest='verbosity', action="count",
                      help="increase debug logging level", default=2)

    
    (opts, args) = parser.parse_args()
    if len(args) == 0 or None in [opts.output, opts.function]:
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
    for c_c in m.select_many('C_C'):

        filt = lambda sel: ooaofooa.is_contained_in(sel, c_c) and sel.Name == opts.function
        s_sync = m.select_any('S_SYNC', filt)
        if not s_sync:
            s_sync = m.new('S_SYNC', Name=opts.function)
            pe_pe = m.new('PE_PE')
            s_dt = m.select_any('S_DT', where(Name='boolean'))
            
            relate(pe_pe, s_sync, 8001)
            relate(s_dt, s_sync, 25)

        generate_actions(m, c_c, s_sync)
    
    xtuml.persist_instances(m, opts.output)

    
if __name__ == '__main__':
    main()
    

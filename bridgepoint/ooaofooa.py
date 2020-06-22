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

import collections
import functools
import os
import logging
import zipfile
import keyword
import xtuml
import io

from xtuml import navigate_one as one
from xtuml import navigate_many as many
from xtuml import navigate_subtype as subtype
from xtuml import where_eq as where

from bridgepoint import interpret
from bridgepoint import external_entities as builtin_ee
from bridgepoint import schema


logger = logging.getLogger(__name__)


class OoaOfOoaException(Exception):
    pass


class Domain(xtuml.MetaModel):
    symbols = None
    
    def __init__(self, id_generator=None):
        self.symbols = dict()
        xtuml.MetaModel.__init__(self, id_generator)
        
    def add_symbol(self, name, handle):
        self.symbols[name] = handle
        
    def find_symbol(self, name):
        if name in self.symbols:
            return self.symbols[name]
        
        try:
            return self.find_class(name)
        except:
            raise OoaOfOoaException('Unknown symbol %s' % name)


def is_contained_in(pe_pe, root):
    '''
    Determine if a PE_PE is contained within a EP_PKG, EP_PKGREF, or a C_C.
    '''
    if not pe_pe:
        return False
    
    if type(pe_pe).__name__ != 'PE_PE':
        pe_pe = one(pe_pe).PE_PE[8001]()
    
    ep_pkg = one(pe_pe).EP_PKG[8000]()
    c_c = one(pe_pe).C_C[8003]()
    
    if root in [ep_pkg, c_c]:
        return True
    
    elif is_contained_in(ep_pkg, root):
        return True
    
    elif is_contained_in(c_c, root):
        return True

    for ep_pkg in many(ep_pkg).EP_PKG[1402, 'is referenced by']():
        if is_contained_in(ep_pkg, root):
            return True

    return False
    

def is_global(pe_pe):
    '''
    Check if a PE_PE is globally defined, i.e. not inside a C_C
    '''
    if type(pe_pe).__name__ != 'PE_PE':
        pe_pe = one(pe_pe).PE_PE[8001]()
    
    if one(pe_pe).C_C[8003]():
        return False
    
    pe_pe = one(pe_pe).EP_PKG[8000].PE_PE[8001]()
    if not pe_pe:
        return True
    
    return is_global(pe_pe)


def get_defining_component(pe_pe):
    '''
    Get the BridgePoint component (C_C) that defines the packeable element
    *pe_pe*.
    '''
    if pe_pe is None:
        return None
    
    if type(pe_pe).__name__ != 'PE_PE':
        pe_pe = one(pe_pe).PE_PE[8001]()
    
    ep_pkg = one(pe_pe).EP_PKG[8000]()
    if ep_pkg:
        return get_defining_component(ep_pkg)
    
    return one(pe_pe).C_C[8003]()


def get_attribute_type(o_attr):
    '''
    Get the base data type (S_DT) associated with a BridgePoint attribute.
    '''
    ref_o_attr = one(o_attr).O_RATTR[106].O_BATTR[113].O_ATTR[106]()
    if ref_o_attr:
        return get_attribute_type(ref_o_attr)
    else:
        return one(o_attr).S_DT[114]()
 

def _get_data_type_name(s_dt):
    '''
    Convert a BridgePoint data type to a pyxtuml meta model type.
    '''
    s_cdt = one(s_dt).S_CDT[17]()
    if s_cdt and s_cdt.Core_Typ in range(1, 6):
        return s_dt.Name.upper()
    
    if one(s_dt).S_EDT[17]():
        return 'INTEGER'
    
    s_dt = one(s_dt).S_UDT[17].S_DT[18]()
    if s_dt:
        return _get_data_type_name(s_dt)
    

def _get_related_attributes(r_rgo, r_rto):
    '''
    The two lists of attributes which relates two classes in an association.
    '''
    l1 = list()
    l2 = list()
    
    ref_filter = lambda ref: ref.OIR_ID == r_rgo.OIR_ID
    for o_ref in many(r_rto).O_RTIDA[110].O_REF[111](ref_filter):
        o_attr = one(o_ref).O_RATTR[108].O_ATTR[106]()
        l1.append(o_attr.Name)
        
        o_attr = one(o_ref).O_RTIDA[111].O_OIDA[110].O_ATTR[105]()
        l2.append(o_attr.Name)
        
    return l1, l2


def mk_enum(s_edt):
    '''
    Create a named tuple from a BridgePoint enumeration.
    '''
    s_dt = one(s_edt).S_DT[17]()
    enums = list()
    kwlist =['False', 'None', 'True'] + keyword.kwlist
    for enum in many(s_edt).S_ENUM[27]():
        if enum.Name in kwlist:
            enums.append(enum.Name + '_')
        else:
            enums.append(enum.Name)
            
    Enum = collections.namedtuple(s_dt.Name, enums)
    return Enum(*range(len(enums)))


def mk_bridge(metamodel, s_brg):
    '''
    Create a python function from a BridgePoint bridge.
    '''
    action = s_brg.Action_Semantics_internal
    label = s_brg.Name
    return lambda **kwargs: interpret.run_function(metamodel, label, 
                                                   action, kwargs)


def mk_external_entity(metamodel, s_ee):
    '''
    Create a python object from a BridgePoint external entity with bridges
    realized as python member functions.
    '''
    bridges = many(s_ee).S_BRG[19]()
    names = [brg.Name for brg in bridges]
    EE = collections.namedtuple(s_ee.Key_Lett, names)

    funcs = list()
    for s_brg in many(s_ee).S_BRG[19]():
        fn = mk_bridge(metamodel, s_brg)
        funcs.append(fn)

    return EE(*funcs)


def mk_function(metamodel, s_sync):
    '''
    Create a python function from a BridgePoint function.
    '''
    action = s_sync.Action_Semantics_internal
    label = s_sync.Name
    return lambda **kwargs: interpret.run_function(metamodel, label, 
                                                   action, kwargs)
    
    
def mk_constant(cnst_syc):
    '''
    Create a python value from a BridgePoint constant.
    '''
    s_dt = one(cnst_syc).S_DT[1500]()
    cnst_lsc = one(cnst_syc).CNST_LFSC[1502].CNST_LSC[1503]()
    
    if s_dt.Name == 'boolean':
        return cnst_lsc.Value.lower() == 'true'
    
    if s_dt.Name == 'integer':
        return int(cnst_lsc.Value)
    
    if s_dt.Name == 'real':
        return float(cnst_lsc.Value)
    
    if s_dt.Name == 'string':
        return str(cnst_lsc.Value)


def mk_operation(metaclass, o_tfr):
    '''
    Create a python function that interprets that action of a BridgePoint class
    operation.
    '''
    o_obj = one(o_tfr).O_OBJ[115]()
    action = o_tfr.Action_Semantics_internal
    label = '%s::%s' % (o_obj.Name, o_tfr.Name)
    run = interpret.run_operation
    
    if o_tfr.Instance_Based:
        return lambda self, **kwargs: run(metaclass, label, action, kwargs, self)
    else:
        fn = lambda cls, **kwargs: run(metaclass, label, action, kwargs, None)
        return classmethod(fn)


def mk_derived_attribute(metaclass, o_dbattr):
    '''
    Create a python property that interprets that action of a BridgePoint derived
    attribute.
    '''
    o_attr = one(o_dbattr).O_BATTR[107].O_ATTR[106]()
    o_obj = one(o_attr).O_OBJ[102]()
    action = o_dbattr.Action_Semantics_internal
    label = '%s::%s' % (o_obj.Name, o_attr.Name)
    fget = functools.partial(interpret.run_derived_attribute, metaclass, 
                             label, action, o_attr.Name)
    return property(fget)


def mk_class(m, o_obj, derived_attributes=False):
    '''
    Create a pyxtuml class from a BridgePoint class.
    '''
    first_filter = lambda selected: not one(selected).O_ATTR[103, 'succeeds']()
    o_attr = one(o_obj).O_ATTR[102](first_filter)
    attributes = list()
        
    while o_attr:
        s_dt = get_attribute_type(o_attr)
        ty = _get_data_type_name(s_dt)
        if not derived_attributes and one(o_attr).O_BATTR[106].O_DBATTR[107]():
            pass
#            logger.warning('Omitting derived attribute %s.%s ' %
#                           (o_obj.Key_Lett, o_attr.Name))
        elif not ty:
            logger.warning('Omitting unsupported attribute %s.%s ' %
                           (o_obj.Key_Lett, o_attr.Name))
        else:
            attributes.append((o_attr.Name, ty))
        
        o_attr = one(o_attr).O_ATTR[103, 'precedes']()
            
    metaclass = m.define_class(o_obj.Key_Lett, list(attributes), o_obj.Descrip)

    for o_id in many(o_obj).O_ID[104]():
        o_oida = many(o_id).O_OIDA[105]()
        o_attrs = many(o_oida).O_ATTR[105]()
        if not derived_attributes and one(o_attrs).O_BATTR[106].O_DBATTR[107]():
            logger.warning('Omitting unique identifier %s.I%d' %
                           (o_obj.Key_Lett, o_id.Oid_ID + 1))
            continue
        
        names = [o_attr.Name for o_attr in o_attrs]
        m.define_unique_identifier(o_obj.Key_Lett, o_id.Oid_ID + 1, *names)
    
    for o_tfr in many(o_obj).O_TFR[115]():
        fn = mk_operation(metaclass, o_tfr)
        setattr(metaclass.clazz, o_tfr.Name, fn)
        
    for o_dbattr in many(o_obj).O_ATTR[102].O_BATTR[106].O_DBATTR[107]():
        o_attr = one(o_dbattr).O_BATTR[107].O_ATTR[106]()
        fn = mk_derived_attribute(metaclass, o_dbattr)
        setattr(metaclass.clazz, o_attr.Name, fn)
            
    return metaclass


def mk_simple_association(m, r_simp):
    '''
    Create a pyxtuml association from a simple association in BridgePoint.
    '''
    r_rel = one(r_simp).R_REL[206]()

    r_form = one(r_simp).R_FORM[208]()
    r_part = one(r_simp).R_PART[207]()
    
    r_rgo = one(r_form).R_RGO[205]()
    r_rto = one(r_part).R_RTO[204]()
    
    if not r_form:
        logger.info('unformalized association R%s' % (r_rel.Numb))
        r_form = one(r_simp).R_PART[207](lambda sel: sel != r_part)
        r_rgo = one(r_form).R_RTO[204]()
        
    source_o_obj = one(r_rgo).R_OIR[203].O_OBJ[201]()
    target_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
    source_ids, target_ids = _get_related_attributes(r_rgo, r_rto)

    if source_o_obj.Obj_ID != target_o_obj.Obj_ID:
        source_phrase = target_phrase = ''
    else:
        source_phrase = r_part.Txt_Phrs
        target_phrase = r_form.Txt_Phrs
            
    m.define_association(rel_id=r_rel.Numb, 
                         source_kind=source_o_obj.Key_Lett,
                         target_kind=target_o_obj.Key_Lett,
                         source_keys=source_ids,
                         target_keys=target_ids,
                         source_conditional=r_form.Cond,
                         target_conditional=r_part.Cond,
                         source_phrase=source_phrase,
                         target_phrase=target_phrase,
                         source_many=r_form.Mult,
                         target_many=r_part.Mult)


def mk_linked_association(m, r_assoc):
    '''
    Create pyxtuml associations from a linked association in BridgePoint.
    '''
    r_rel = one(r_assoc).R_REL[206]()
    r_rgo = one(r_assoc).R_ASSR[211].R_RGO[205]()
    source_o_obj = one(r_rgo).R_OIR[203].O_OBJ[201]()
    
    def _mk_assoc(side1, side2):
        r_rto = one(side1).R_RTO[204]()

        target_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
        source_ids, target_ids = _get_related_attributes(r_rgo, r_rto)
        if side1.Obj_ID != side2.Obj_ID:
            source_phrase = target_phrase = ''
        else:
            source_phrase = side1.Txt_Phrs
            target_phrase = side2.Txt_Phrs
            
        m.define_association(rel_id=r_rel.Numb, 
                             source_kind=source_o_obj.Key_Lett,
                             target_kind=target_o_obj.Key_Lett,
                             source_keys=source_ids,
                             target_keys=target_ids,
                             source_conditional=side2.Cond,
                             target_conditional=False,
                             source_phrase=source_phrase,
                             target_phrase=target_phrase,
                             source_many=side2.Mult,
                             target_many=False)
        
    r_aone = one(r_assoc).R_AONE[209]()
    r_aoth = one(r_assoc).R_AOTH[210]()
    
    _mk_assoc(r_aone, r_aoth)
    _mk_assoc(r_aoth, r_aone)
  
    
def mk_subsuper_association(m, r_subsup):
    '''
    Create pyxtuml associations from a sub/super association in BridgePoint.
    '''
    r_rel = one(r_subsup).R_REL[206]()
    r_rto = one(r_subsup).R_SUPER[212].R_RTO[204]()
    target_o_obj = one(r_rto).R_OIR[203].O_OBJ[201]()
    
    for r_sub in many(r_subsup).R_SUB[213]():
        r_rgo = one(r_sub).R_RGO[205]()

        source_o_obj = one(r_rgo).R_OIR[203].O_OBJ[201]()
        source_ids, target_ids = _get_related_attributes(r_rgo, r_rto)
        m.define_association(rel_id=r_rel.Numb, 
                             source_kind=source_o_obj.Key_Lett,
                             target_kind=target_o_obj.Key_Lett,
                             source_keys=source_ids,
                             target_keys=target_ids,
                             source_conditional=True,
                             target_conditional=False,
                             source_phrase='',
                             target_phrase='',
                             source_many=False,
                             target_many=False)
                           

def mk_derived_association(m, r_comp):
    '''
    Create a pyxtuml association from a derived association in BridgePoint.
    '''
    pass


def mk_association(m, r_rel):
    '''
    Create a pyxtuml association from a R_REL in ooaofooa.
    '''
    handler = {
        'R_SIMP': mk_simple_association,
        'R_ASSOC': mk_linked_association,
        'R_SUBSUP': mk_subsuper_association,
        'R_COMP': mk_derived_association,
    }
    inst = subtype(r_rel, 206)
    fn = handler.get(type(inst).__name__)
    return fn(m, inst)


def mk_component(bp_model, c_c=None, derived_attributes=False):
    '''
    Create a pyxtuml meta model from a BridgePoint model. 
    Optionally, restrict to classes and associations contained in the
    component c_c.
    '''
    target = Domain()

    c_c_filt = lambda sel: c_c is None or is_contained_in(sel, c_c)
    
    for o_obj in bp_model.select_many('O_OBJ', c_c_filt):
        mk_class(target, o_obj, derived_attributes)
        
    for r_rel in bp_model.select_many('R_REL', c_c_filt):
        mk_association(target, r_rel)
        
    for s_sync in bp_model.select_many('S_SYNC', c_c_filt):
        fn = mk_function(target, s_sync)
        target.add_symbol(s_sync.Name, fn)
    
    for s_dt in bp_model.select_many('S_DT', c_c_filt):
        s_edt = one(s_dt).S_EDT[17]()
        if s_edt:
            enum = mk_enum(s_edt)
            target.add_symbol(s_dt.Name, enum)
        
    for cnst_csp in bp_model.select_many('CNST_CSP', c_c_filt):
        for cnst_syc in many(cnst_csp).CNST_SYC[1504]():
            value = mk_constant(cnst_syc)
            target.add_symbol(cnst_syc.Name, value)
        
    for ass in target.associations:
        ass.formalize()
    
    for s_ee in bp_model.select_many('S_EE', c_c_filt):
        if s_ee.Key_Lett in ['LOG', 'ARCH', 'TIM', 'NVS', 'PERSIST']:
            target.add_symbol(s_ee.Key_Lett, getattr(builtin_ee, s_ee.Key_Lett))
                              
        else:
            ee = mk_external_entity(target, s_ee)
            target.add_symbol(s_ee.Key_Lett, ee)
    
    return target


class ModelLoader(xtuml.ModelLoader):
    '''
    A *xtuml.MetaModel* loader with ooaofooa schema and globals pre-defined.
    '''
    
    def __init__(self, load_globals=True):
        xtuml.ModelLoader.__init__(self)
        self.input(schema.classes, 'ooaofooa classes (v%s)' % schema.__version__)
        self.input(schema.associations, 'ooaofooa associations (v%s)' % schema.__version__)
        self.input(schema.indices, 'ooaofooa indices (v%s)' % schema.__version__)
        if load_globals:
            self.input(schema.globals, 'predefined ooaofooa globals (v%s)' % schema.__version__)
        
    def filename_input(self, path_or_filename):
        '''
        Open and read input from a *path or filename*, and parse its content.
        
        If the filename is a directory, files that ends with .xtuml located
        somewhere in the directory or sub directories will be loaded as well.

        If the filename is a zip archive, files that ends with .xtuml located
        somewhere in the archive will be loaded as well.
        '''
        if os.path.isdir(path_or_filename):
            for path, _, files in os.walk(path_or_filename):
                for name in files:
                    if name.endswith('.xtuml'):
                        xtuml.ModelLoader.filename_input(self, os.path.join(path, name))
        elif zipfile.is_zipfile(path_or_filename):
            with zipfile.ZipFile(path_or_filename) as zipinput:
                for zipinfo in zipinput.filelist:
                    if zipinfo.filename.endswith('.xtuml'):
                        with zipinput.open(zipinfo) as f:
                            xtuml.ModelLoader.file_input(self, io.TextIOWrapper(f, encoding='UTF-8'))
        else:
            xtuml.ModelLoader.filename_input(self, path_or_filename)

    def build_component(self, name=None, derived_attributes=False):
        '''
        Instantiate and build a component from ooaofooa named *name* as a
        pyxtuml model. Classes, associations, attributes and unique identifers,
        i.e. O_OBJ, R_REL, O_ATTR in ooaofooa, are defined in the resulting
        pyxtuml model.
        
        Optionally, control whether *derived attributes* shall be mapped into
        the resulting pyxtuml model as attributes or not.
        
        Futhermore, if no *name* is provided, the entire content of the ooaofooa
        model is instantiated into the pyxtuml model.
        '''
        mm = self.build_metamodel()
        c_c = mm.select_any('C_C', where(Name=name))
        if c_c:
            return mk_component(mm, c_c, derived_attributes)
        elif name:
            raise OoaOfOoaException('Unable to find the component %s' % name)
        else:
            return mk_component(mm, c_c, derived_attributes)
    

def _mk_loader(resource, load_globals):
    resource = resource or list()
        
    if isinstance(resource, str):
        resource = [resource]
        
    loader = Loader(load_globals)
    for filename in resource:
        loader.filename_input(filename)
    
    return loader


def load_metamodel(resource=None, load_globals=True):
    '''
    Load and return a metamodel expressed in ooaofooa from a *resource*.
    The resource may be either a filename, a path, or a list of filenames
    and/or paths.
    '''
    loader = _mk_loader(resource, load_globals)
    return loader.build_metamodel()


def load_component(resource, name=None, load_globals=True):
    '''
    Load and return a model from a *resource*. The resource may be either a
    filename, a path, or a list of filenames and/or paths.
    '''
    loader = _mk_loader(resource, load_globals)
    return loader.build_component()


def delete_globals(m, disconnect=False):
    '''
    Remove global instances, e.g. the core data type integer.
    '''
    filt = lambda sel: (247728914420827907967735776184937480192 <= 
                        sel.DT_ID <= 
                        247728914420827907967735776184937480208)

    for s_dt in m.select_many('S_DT', filt):
        xtuml.delete(one(s_dt).PE_PE[8001](), disconnect)
        xtuml.delete(subtype(s_dt, 17), disconnect)
        xtuml.delete(s_dt, disconnect)


# Backwards compatibility with older versions of pyxtuml
Loader = ModelLoader
empty_model = load_metamodel


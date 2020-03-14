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
Serialize xtuml models and its schema to an sql-based file format and persist
to disk.
'''

import uuid
import logging

import xtuml


logger = logging.getLogger(__name__)


def serialize_value(value, ty):
    '''
    Serialize a value from an xtuml metamodel instance.
    '''
    ty = ty.upper()
    
    null_value = {
        'BOOLEAN'   : False,
        'INTEGER'   : 0,
        'REAL'      : 0.0,
        'STRING'    : '',
        'UNIQUE_ID' : 0
    }
    
    transfer_fn = {
        'BOOLEAN'     : lambda v: '%d' % int(v),
        'INTEGER'     : lambda v: '%d' % v,
        'REAL'        : lambda v: '%f' % v,
        'STRING'      : lambda v: "'%s'" % v.replace("'", "''"),
        'UNIQUE_ID'   : lambda v: '"%s"' % uuid.UUID(int=v)
    }

    if value is None:
        value = null_value[ty]
    
    return transfer_fn[ty](value)
    
    
def serialize_instance(instance):
    '''
    Serialize an *instance* from a metamodel.
    '''
    attr_count = 0
    metaclass = xtuml.get_metaclass(instance)
    s = 'INSERT INTO %s VALUES (' % metaclass.kind
    for name, ty in metaclass.attributes:
        value = getattr(instance, name)
            
        s += '\n    '
        s += serialize_value(value, ty)

        attr_count += 1
        if attr_count < len(metaclass.attributes):
            s += ', -- %s : %s' % (name, ty)
        else:
            s += ' -- %s : %s' % (name, ty)

    s += '\n);\n'

    return s


def serialize_instances(metamodel):
    '''
    Serialize all instances in a *metamodel*.
    '''
    s = ''
    for inst in metamodel.instances:
        s += serialize_instance(inst)
    
    return s


def serialize_association(ass):
    '''
    Serialize an xtuml metamodel association.
    '''
    s1 = '%s %s (%s)' % (ass.source_link.cardinality,
                         ass.source_link.to_metaclass.kind,
                         ', '.join(ass.source_keys))

    if ass.target_link.phrase:
        s1 += " PHRASE '%s'" % ass.target_link.phrase

    s2 = '%s %s (%s)' % (ass.target_link.cardinality,
                         ass.target_link.to_metaclass.kind,
                         ', '.join(ass.target_keys))
    
    if ass.source_link.phrase:
        s2 += " PHRASE '%s'" % ass.source_link.phrase

    return 'CREATE ROP REF_ID %s FROM %s TO %s;\n' % (ass.rel_id,
                                                      s1,
                                                      s2)


def serialize_class(Cls):
    '''
    Serialize an xtUML metamodel class.
    '''
    metaclass = xtuml.get_metaclass(Cls)
    attributes = ['%s %s' % (name, ty.upper())
                  for name, ty in metaclass.attributes]
    
    s = 'CREATE TABLE %s (\n    ' % metaclass.kind
    s += ',\n    '.join(attributes)
    s += '\n);\n'

    return s

def serialize_unique_identifiers(metamodel):
    s = ''
    for kind in sorted(metamodel.metaclasses.keys()):
        metaclass = metamodel.metaclasses[kind]
        for index_name, attribute_names in metaclass.indices.items():
            attribute_names = ', '.join(attribute_names)
            s += 'CREATE UNIQUE INDEX %s ON %s (%s);\n' % (index_name,
                                                          metaclass.kind,
                                                          attribute_names)
    return s


def serialize_classes(metamodel):
    '''
    Serialize all class definitions in a *metamodel*.
    '''
    return ''.join([serialize_class(metamodel.metaclasses[kind].clazz)
                    for kind in sorted(metamodel.metaclasses.keys())])


def serialize_associations(metamodel):
    '''
    Serialize all association definitions in a *metamodel*.
    '''
    orderby = lambda x: (x.rel_id, x.target_link.from_metaclass.kind)
    return ''.join([serialize_association(ass)
                    for ass in sorted(metamodel.associations, key=orderby)])


def serialize_schema(metamodel):
    '''
    Serialize all class and association definitions in a *metamodel*.
    '''
    return serialize_classes(metamodel) + serialize_associations(metamodel)


def serialize_database(metamodel):
    '''
    Serialize all instances, class definitions, association definitions, and
    unique identifiers  in a *metamodel*.
    '''
    schema = serialize_schema(metamodel)
    instances = serialize_instances(metamodel)
    identifiers = serialize_unique_identifiers(metamodel)
    
    return ''.join([schema, instances, identifiers])


def serialize(resource):
    '''
    Serialize some xtuml *resource*, e.g. an instance or a complete metamodel.
    '''
    if isinstance(resource, xtuml.MetaModel):
        return serialize_database(resource)

    elif isinstance(resource, type) and issubclass(resource, xtuml.Class):
        return serialize_class(resource)
    
    elif isinstance(resource, xtuml.Association):
        return serialize_association(resource)

    elif isinstance(resource, xtuml.Class):
        return serialize_instance(resource)


def persist_instances(metamodel, path, mode='w'):
    '''
    Persist all instances in a *metamodel* by serializing them and saving to a 
    *path* on disk.
    '''
    with open(path, mode) as f:
        for inst in metamodel.instances:
            s = serialize_instance(inst)
            f.write(s)


def persist_schema(metamodel, path, mode='w'):
    '''
    Persist all class and association definitions in a *metamodel* by 
    serializing them and saving to a *path* on disk.
    '''
    with open(path, mode) as f:
        for kind in sorted(metamodel.metaclasses.keys()):
            s = serialize_class(metamodel.metaclasses[kind].clazz)
            f.write(s)
            
        for ass in sorted(metamodel.associations, key=lambda x: x.rel_id):
            s = serialize_association(ass)
            f.write(s)


def persist_unique_identifiers(metamodel, path, mode='w'):
    '''
    Persist all unique identifiers in a *metamodel* by serializing them and
    saving to a *path* on disk.
    '''
    with open(path, mode) as f:
        for metaclass in metamodel.metaclasses.values():
            for index_name, attribute_names in metaclass.indices.items():
                attribute_names = ', '.join(attribute_names)
                s = 'CREATE UNIQUE INDEX %s ON %s (%s);\n' % (index_name,
                                                              metaclass.kind,
                                                              attribute_names)
                f.write(s)


def persist_database(metamodel, path, mode='w'):
    '''
    Persist all instances, class definitions and association definitions in a
    *metamodel* by serializing them and saving to a *path* on disk.
    '''
    with open(path, mode) as f:
        for kind in sorted(metamodel.metaclasses.keys()):
            metaclass = metamodel.metaclasses[kind]
            s = serialize_class(metaclass.clazz)
            f.write(s)
            
            for index_name, attribute_names in metaclass.indices.items():
                attribute_names = ', '.join(attribute_names)
                s = 'CREATE UNIQUE INDEX %s ON %s (%s);\n' % (index_name,
                                                              metaclass.kind,
                                                              attribute_names)
                f.write(s)
                
        for ass in sorted(metamodel.associations, key=lambda x: x.rel_id):
            s = serialize_association(ass)
            f.write(s)

        for inst in metamodel.instances:
            s = serialize_instance(inst)
            f.write(s)


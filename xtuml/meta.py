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
Perform various xtUML meta operations, e.g. create new metamodels and
metaclasses, relate instances and perform navigations and queries.
'''

import logging
import collections

import xtuml

from functools import partial

try:
    from future_builtins import filter, zip
except ImportError:
    pass


logger = logging.getLogger(__name__)



class MetaException(Exception):
    '''
    Base class for all exceptions thrown by the xtuml.meta module.
    '''


class DeleteException(MetaException):
    '''
    An exception that may be thrown during delete operations.
    '''


class RelateException(MetaException):
    '''
    An exception that may be thrown during relate operations.
    '''


class UnrelateException(MetaException):
    '''
    An exception that may be thrown during unrelate operations.
    '''


class UnknownLinkException(MetaException):
    '''
    An exception that may be thrown when a link is not found.
    '''
    def __init__(self, from_kind, to_kind, rel_id, phrase):
        if phrase:
            msg = "%s->%s[%s, %s]" % (from_kind, to_kind, repr(rel_id), repr(phrase))
        else:
            msg = "%s->%s[%s]" % (from_kind, to_kind, repr(rel_id))

        MetaException.__init__(self, msg)


class MetaModelException(MetaException):
    '''
    Base class for exceptions thrown by the MetaModel class.
    '''


class UnknownClassException(MetaModelException):
    '''
    An exception that may be thrown when a metaclass is not found.
    '''


def _is_null(instance, name):
    '''
    Determine if an attribute of an *instance* with a specific *name* 
    is null.
    '''
    value = getattr(instance, name)
    if value:
        return False
    
    elif value is None:
        return True

    name = name.upper()
    for attr_name, attr_ty in instance.__metaclass__.attributes:
        if attr_name.upper() != name:
            continue

        attr_ty = attr_ty.upper()
        if attr_ty == 'UNIQUE_ID':
            # UUID(int=0) is reserved for null
            return value == 0

        elif attr_ty == 'STRING':
            # empty string is reserved for null
            return len(value) == 0

        else:
            #null-values for integer, boolean and real are not supported
            return False


class Association(object):
    '''
    An association connects two metaclasses to each other via two directed
    links.
    '''
    rel_id = None
    link = None
    reversed_link = None
    
    def __init__(self, rel_id, link, reversed_link):
        self.rel_id = rel_id
        self.link = link
        self.reversed_link = reversed_link
        
    @property
    def is_reflexive(self):
        return self.link.kind == self.reversed_link.kind


class Link(object):
    '''
    A link connects one metaclass to another in a single direction. 
    
    *rel_id* is used to specify the association between the to metaclasses,
    and a *key map* is used to define the mapping from a primary key in the 
    *from_metaclass* to a foreign key in the *to_metaclass*. The *phrase* is
    used to specify the direction when the association is reflexive.
    
    In addition, links also specify cardinality constraints via the *many*
    and *conditional* attributes.
    '''
    from_metaclass = None
    rel_id = None
    to_metaclass = None
    phrase = None
    key_map = None
    conditional = None
    many = None
    
    def __init__(self, from_metaclass, rel_id, to_metaclass, key_map, phrase='',
                 conditional=False, many=False):
        if isinstance(rel_id, int):
            rel_id = 'R%d' % rel_id
        
        self.from_metaclass = from_metaclass
        self.rel_id = rel_id
        self.to_metaclass = to_metaclass
        self.key_map = key_map
        self.phrase = phrase
        self.conditional = conditional
        self.many = many

    @property
    def cardinality(self):
        '''
        Obtain the cardinality string.
        
        Example: '1C' for a conditional link with a single instance [0..1]
                 'MC' for a link with any number of instances [0..*]
                 'M'  for a more than one instance [1..*]
                 'M'  for a link with exactly one instance [1]
        '''
        if self.many:
            s = 'M'
        else:
            s = '1'
            
        if self.conditional:
            s += 'C'
            
        return s
    
    @property
    def kind(self):
        '''
        Obtain the resulting kind when the link is navigated.
        '''
        return self.to_metaclass.kind
    
    def navigate(self, instance):
        '''
        Navigate accross a link starting from an *instance*.
        '''
        kwargs = dict()
        for key, mapped_key in self.key_map.items():
            kwargs[mapped_key] = getattr(instance, key)

        return self.to_metaclass.query(kwargs)
    
    def __repr__(self):
        if self.phrase:
            return "%s->%s[%s, %s]" % (self.from_metaclass.kind, self.kind, 
                                       repr(self.rel_id), repr(self.phrase))
        else:
            return "%s->%s[%s]" % (self.from_metaclass.kind, self.kind, 
                                   repr(self.rel_id))


class ReversedLink(Link):
    '''
    A reversed (directed) link is identical to a regular link, but with the
    *key_map* being inverted upon initialisation.
    '''
    def __init__(self, from_metaclass, rel_id, to_metaclass, key_map, phrase='',
                 conditional=False, many=False):
        Link.__init__(self, from_metaclass, rel_id, to_metaclass,
                      dict(zip(key_map.values(), key_map.keys())),
                      phrase, conditional, many)


class Query(object):
    '''
    A *Query* retrive instances from a metaclass by matching instance
    attributes against a dictonary of values provided upon initialisation.
    '''
    storage = None
    result = None
    evaluation = None
    
    def __init__(self, storage, kwargs):
        self.result = collections.deque()
        self.items = collections.deque(kwargs.items())
        self.storage = storage
        self.evaluation = self.evaluate()
        
    def evaluate(self):
        '''
        Evaluate the query by iterating all instances in the metaclass.
        
        **Note**: if the instance population is modified during evaluation,
        an exception is thrown.
        '''
        for inst in iter(self.storage):
            for name, value in iter(self.items):
                if getattr(inst, name) != value or _is_null(inst, name):
                    break
            else:
                self.result.append(inst)
                yield inst
    
        self.evaluation = None
    
    def execute(self):
        '''
        Execute the query. 
        
        **Note**: Each instance is evaluated for inclusion only once, even
        if the query is executed multiple times. To re-evaluate the query,
        create a new one.
        '''
        for inst in self.result:
            yield inst
            
        while self.evaluation:
            yield next(self.evaluation)
        
        
class QuerySet(xtuml.OrderedSet):
    '''
    An ordered set which holds instances that match queries.
    '''
    @property
    def first(self):
        '''
        Obtain the first element in the set.
        '''
        if len(self):
            return next(iter(self))
    
    @property
    def last(self):
        '''
        Obtain the last element in the set.
        '''
        if len(self):
            return next(reversed(self))


class Class(object):
    '''
    A class that all instances created by a metaclass inherits from. 
    
    **Note**: Accesses to attributes, e.g. getattr/setattr, on these objects
    are case insensitive.
    '''
    def __add__(self, other):
        assert isinstance(other, Class)
        return QuerySet([self, other])

    def __sub__(self, other):
        assert isinstance(other, Class)
        if self == other: return QuerySet()
        else: return QuerySet([self])

    def __getattr__(self, name):
        uname = name.upper()
        for attr, _ in self.__metaclass__.attributes:
            if attr.upper() == uname:
                return self.__dict__[attr]

        return object.__getattribute__(self, name)
    
    def __setattr__(self, name, value):
        uname = name.upper()
        for attr, _ in self.__metaclass__.attributes:
            if attr.upper() == uname:
                self.__dict__[attr] = value
                self.__metaclass__.cache.clear()
                return

        self.__dict__[name] = value
        
    def __str__(self):
        return str(self.__dict__)


# Backwards compatabillity with older versions of pyxtuml
BaseObject = Class


class MetaClass(object):
    '''
    A metaclass contain metadata for instances, e.g. what attributes are 
    available, what thier types are, and so on.
    
    In addition, each metaclass also handle allocations of instances.
    '''
    metamodel = None
    kind = None
    attributes = None
    referential_attributes = None
    identifying_attributes = None
    links = None
    indices = None
    clazz = None
    storage = None
    cache = None
    
    def __init__(self, kind, metamodel=None):
        self.metamodel = metamodel
        self.kind = kind
        self.attributes = list()
        self.referential_attributes = set()
        self.identifying_attributes = set()
        self.indices = dict()
        self.links = dict()
        self.storage = list()
        self.cache = dict()
        self.clazz = type(kind, (Class,), dict(__metaclass__=self))
        
    def __call__(self, *args, **kwargs):
        '''
        Create and return a new instance using the metaclass constructor.
        '''
        return self.new(*args, **kwargs)
        
    @property
    def attribute_names(self):
        '''
        Obtain an ordered list of all attribute names.
        '''
        return [name for name, _ in self.attributes]

    def attribute_type(self, attribute_name):
        '''
        Obtain the type of an attribute.
        '''
        attribute_name = attribute_name.upper()
        for name, ty in self.attributes:
            if name.upper() == attribute_name:
                return ty
    
    def add_link(self, metaclass, rel_id, key_map, phrase, conditional,
                 many, reverse=False):
        '''
        Add a new link from *self* to *metaclass*. Keys in the link are added
        to the set of identifying or referential attributes depending on the
        direction, i.e. if the link is reversed or not.
        '''
        if isinstance(rel_id, int):
            rel_id = 'R%d' % rel_id
        
        if reverse:
            link = ReversedLink(self, rel_id, metaclass, key_map, phrase, conditional, many)
            self.identifying_attributes |= set(link.key_map.keys())
        else:
            link = Link(self, rel_id, metaclass, key_map, phrase, conditional, many)
            self.referential_attributes |= set(link.key_map.keys())
            
        key = (metaclass.kind.upper(), rel_id, phrase)
        self.links[key] = link

        return link
        
    def find_link(self, kind, rel_id, phrase):
        '''
        Find a link with a given *rel_id* and *phrase* that yeld instances of
        some *kind*.
        '''
        if isinstance(rel_id, int):
            rel_id = 'R%d' % rel_id
            
        key = (kind.upper(), rel_id, phrase)
        return self.links.get(key, None)
        
    def append_attribute(self, name, type_name):
        '''
        Append an attribute with a given *name* and *type name* at the end of
        the list of attributes.
        '''
        attr = (name, type_name)
        self.attributes.append(attr)
        
    def insert_attribute(self, index, name, type_name):
        '''
        Insert an attribute with a given *name* and *type name* at some *index*
        in the list of attributes.
        '''
        attr = (name, type_name)
        self.attributes.insert(index, attr)
        
    def delete_attribute(self, name):
        '''
        Delete an attribute with a given *name* from the list of attributes.
        '''
        for idx, attr in enumerate(self.attributes):
            attr_name, _ = attr
            if attr_name == name:
                del self.attributes[idx]
                return
        
    def default_value(self, type_name):
        '''
        Obtain the default value for some *type name*.
        '''
        uname = type_name.upper()
        if   uname == 'BOOLEAN':
            return False
            
        elif uname == 'INTEGER':
            return 0
            
        elif uname == 'REAL':
            return 0.0
            
        elif uname == 'STRING':
            return ''
            
        elif uname == 'UNIQUE_ID':
            if self.metamodel:
                return next(self.metamodel.id_generator)
            else:
                return None
        else:
            raise MetaException("Unknown type named '%s'" % type_name)
        
    def new(self, *args, **kwargs):
        '''
        Create and return a new instance.
        '''
        self.cache.clear()
        inst = self.clazz()
        
        # set all attributes with an initial default value
        for name, ty in self.attributes:
            if name in self.referential_attributes:
                value = None
            else:
                value = self.default_value(ty)
            setattr(inst, name, value)
            
        # set all positional arguments
        for attr, value in zip(self.attributes, args):
            name, ty = attr
            setattr(inst, name, value)
            
        # set all named arguments
        for name, value in kwargs.items():
            setattr(inst, name, value)
            
        self.storage.append(inst)
        
        return inst

    def clone(self, instance):
        '''
        Create a shallow clone of an *instance*.
        
        **Note:** the clone and the original instance **does not** have to be
        part of the same metaclass. 
        '''
        clone = self.new()
        for name, _ in instance.__metaclass__.attributes:
            value = getattr(instance, name)
            setattr(clone, name, value)
            
        return clone
    
    def delete(self, instance):
        '''
        Delete an *instance* from the instance pool. If the *instance* is not
        part of the metaclass, a *MetaException* is thrown.
        '''
        if instance in self.storage:
            self.storage.remove(instance)
            self.cache.clear()
        else:
            raise DeleteException("Instance not found in the instance pool")

    def select_one(self, where_clause=None):
        '''
        Select a single instance from the instance pool. Optionally, a
        conditional *where-clause* in the form of a function may be provided.
        '''
        if isinstance(where_clause, dict):
            s = self.query(where_clause)
        else:
            s = iter(filter(where_clause, self.storage))
            
        return next(s, None)

    def select_many(self, where_clause=None):
        '''
        Select several instances from the instance pool. Optionally,
        a conditional *where-clause* in the form of a function may be provided.
        '''
        if isinstance(where_clause, dict):
            s = self.query(where_clause)
        else:
            s = filter(where_clause, self.storage)
        
        return QuerySet(s)

    def navigate(self, inst, kind, rel_id, phrase=''):
        '''
        Navigate across a link with some *rel_id* and *phrase* that yields
        instances of some *kind*.
        '''
        key = (kind.upper(), rel_id, phrase)
        if key in self.links:
            link = self.links[key]
            return link.navigate(inst)
        else:
            raise UnknownLinkException(self.kind, kind, rel_id, phrase)
            
    def query(self, dictonary_of_values):
        '''
        Query the instance pool for instances with attributes that match a given
        *dictonary of values*.
        '''
        index = frozenset(list(dictonary_of_values.items()))
        if index not in self.cache:
            self.cache[index] = Query(self.storage, dictonary_of_values)
            
        return self.cache[index].execute()

        
class NavChain(object):
    '''
    A navigation chain initializes a navigation from one or more instances.
    Navigation may be syntactically cascaded in several ways:
    
       res = NavChain(inst).nav('X', 'R100', 'phrase').nav('Y', 101)

    or using an OAL/RSL inspired syntax:
    
       res = NavChain(inst).X[100, 'phrase'].Y[101](lamda x: <filter expression>)
    '''
    
    def __init__(self, handle):
        if handle is None:
            handle = []
            
        elif isinstance(handle, Class):
            handle = [handle]
        
        elif not isinstance(handle, collections.Iterable):
            raise MetaException("Unable to navigate across '%s'" % type(handle))
        
        self.handle = handle
        self._kind = None
        
    def nav(self, kind, relid, phrase=''):
        self.handle = NavChain._nav(self.handle, kind, relid, phrase)
        return self
    
    @staticmethod
    def _nav(handle, kind, rel_id, phrase):
        if isinstance(rel_id, int):
            rel_id = 'R%d' % rel_id
    
        for inst in iter(handle):
            for result in inst.__metaclass__.navigate(inst, kind, rel_id, phrase):
                yield result
            
    def __getattr__(self, kind):
        '''
        The navigation chain specified a *kind*, e.g.
        >>> chain.X
        '''
        self._kind = kind
        return self
    
    def __getitem__(self, args):
        '''
        The navigation chain specified a link, e.g. the rel_id and phrase, e.g.
        >>> chain[100, 'phrase']
        '''
        if not isinstance(args, tuple):
            args = (args, '')
        
        relid, phrase = args
        
        return self.nav(self._kind, relid, phrase)

    def __call__(self, where_clause=None):
        '''
        The navigation chain is invoked. Optionally, a conditional
        *where-clause* in the form of a function may be provided, e.g
        
        >>> chain(lambda selected: selected.Name == 'test')
        '''
        handle = self.handle or list()
        return QuerySet(filter(where_clause, handle))
    
    
class NavOneChain(NavChain):
    '''
    A navigation chain that yeilds an instance, or None.
    '''
    def __call__(self, where_clause=None):
        handle = self.handle or iter([])
        if not where_clause:
            return next(handle, None)
        
        for inst in handle:
            if where_clause(inst):
                return inst


def navigate_one(instance):
    '''
    Initialize a navigation from one *instance* to another across a one-to-one
    association.
    
    The resulting query will return an instance or None.
    
    Usage example:
    
    >>> from xtuml import navigate_one as one
    >>> m = xtuml.load_metamodel('db.sql')
    >>> inst = m.select_any('My_Modeled_Class')
    >>> other_inst = one(inst).Some_Other_Class[4]()
    
    The syntax is somewhat similar to the action language used in BridgePoint.
    The same semantics would be expressed in BridgePoint as::
    
        select any inst from instances of My_Modeled_Class;
        select one other_inst related by inst->Some_Other_Class[R4];
    
    **Note:** If the navigated association is reflexive, a phrase must be 
    provided, e.g.
    
    >>> other_inst = one(inst).Some_Other_Class[4, 'some phrase']()
    '''
    return navigate_any(instance)


def navigate_any(instance_or_set):
    '''
    Initialize a navigation from an instance, or a set of instances, to 
    associated instances across a one-to-many or many-to-many association.

    The resulting query will return an instance or None.
    '''
    return NavOneChain(instance_or_set)


def navigate_many(instance_or_set):
    '''
    Initialize a navigation from an instance, or a set of instances, to 
    associated instances across a one-to-many or many-to-many association.
    
    The resulting query will return a set of instances.
    '''
    return NavChain(instance_or_set)


def navigate_subtype(supertype, rel_id):
    '''
    Perform a navigation from *supertype* to its subtype across *rel_id*. The
    navigated association must be modeled as a subtype-supertype association.
    
    The return value will an instance or None.
    '''
    if not supertype:
        return
    
    if isinstance(rel_id, int):
        rel_id = 'R%d' % rel_id

    for kind, rel_id_candidate, _ in supertype.__metaclass__.links:
        if rel_id != rel_id_candidate:
            continue
        
        subtype = navigate_one(supertype).nav(kind, rel_id)()
        if subtype:
            return subtype


class WhereEqual(dict):
    '''
    Helper class to create a dictonary of values for queries using
    python keyword arguments to *where_eq()*
    '''
    def __call__(self, selected):
        for name in self:
            if getattr(selected, name) != self.get(name):
                return False
            
        return True


def where_eq(**kwargs):
    '''
    Return a where-clause that filters out instances based on named 
    keywords.
    
    Usage example:
    
    >>> from xtuml import where_eq as where
    >>> m = xtuml.load_metamodel('db.sql')
    >>> inst = m.select_any('My_Modeled_Class', where(My_Number=5))
    '''
    return WhereEqual(kwargs)


def sort_reflexive(set_of_instances, rel_id, phrase):
    '''
    Sort a *set of instances* in the order they appear across a conditional and
    reflexive association. The first instance in the resulting ordered set is
    **not** associated to an instance across the given *phrase*.
    '''
    if not isinstance(set_of_instances, QuerySet):
        raise MetaException('The collection to sort must be a QuerySet')
    
    if not set_of_instances.first:
        return QuerySet()
    
    if isinstance(rel_id, int):
        rel_id = 'R%d' % rel_id
    
    # Figure out the phrase in the other direction
    metaclass = set_of_instances.first.__metaclass__
    for link in metaclass.links.values():
        if link.to_metaclass != metaclass:
            continue
        
        if link.rel_id != rel_id:
            continue

        if link.phrase == phrase:
            continue

        other_phrase = link.phrase
        break
    else:
        raise UnknownLinkException(metaclass.kind, metaclass.kind, rel_id, phrase)
    
    first_filt = lambda sel: not navigate_one(sel).nav(metaclass.kind, rel_id, phrase)()
    first_instances = list(filter(first_filt, set_of_instances))
    if not first_instances:
        #the instance sequence is recursive, start anywhere
        first_instances = [set_of_instances.first]
    
    def sequence_generator():
        for first in first_instances:
            inst = first
            while inst:
                yield inst
                inst = navigate_one(inst).nav(metaclass.kind, rel_id, other_phrase)()
                if inst is first:
                    break
                
    return QuerySet(sequence_generator())

    
def _find_link(inst1, inst2, rel_id, phrase):
    '''
    Find links that correspond to the given arguments.
    '''
    metaclass1 = inst1.__metaclass__
    metaclass2 = inst2.__metaclass__

    if isinstance(rel_id, int):
        rel_id = 'R%d' % rel_id
        
    for ass in metaclass1.metamodel.associations:
        if ass.rel_id != rel_id:
            continue

        if (ass.link.from_metaclass == metaclass1 and
            ass.link.to_metaclass == metaclass2 and
            ass.reversed_link.phrase == phrase):
            return inst1, inst2, ass.link

        if (ass.reversed_link.from_metaclass == metaclass1 and
            ass.reversed_link.to_metaclass == metaclass2 and
            ass.link.phrase == phrase):
            return inst2, inst1, ass.link

    raise UnknownLinkException(metaclass1.kind, metaclass2.kind, rel_id, phrase)
                                          

def _deferred_link_operation(inst, link, op):
    '''
    Generate a list of deferred operations that needs to be invoked after an
    update is made to identifying attributes on the association *link*.
    '''
    l = list()
    
    metaclass = inst.__metaclass__
    keys = set(link.key_map.keys())
    for link in metaclass.links.values():
        if not isinstance(link, ReversedLink):
            continue
        
        derived_keys = set(link.key_map.values())
        if not (keys & derived_keys):
            continue
        
        nav = navigate_many(inst).nav(link.to_metaclass.kind, link.rel_id, link.phrase)
        for from_inst in nav():
            fn = partial(op, from_inst, inst, link.rel_id, link.phrase)
            l.append(fn)

    return l


def relate(from_instance, to_instance, rel_id, phrase=''):
    '''
    Relate *from_instance* to *to_instance* across *rel_id*. For reflexive
    association, a *phrase* indicating the direction must also be provided.
    
    The two instances are related to each other by copying the identifying 
    attributes from the instance on the TO side of a association to the instance
    n the FROM side. Updated values which affect existing associations are 
    propagated. A set of all affected instances will be returned.
    '''
    affected_instances = set()
    if None in [from_instance, to_instance]:
        return affected_instances
        
    from_instance, to_instance, link = _find_link(from_instance, to_instance,
                                                  rel_id, phrase)
                                                      
    post_process = _deferred_link_operation(from_instance, link, relate)
    for from_name, to_name in link.key_map.items():
        if _is_null(to_instance, to_name):
            raise RelateException('undefined referential attribute %s' % to_name)
        
        from_value = getattr(from_instance, from_name)
        to_value = getattr(to_instance, to_name)

        if from_value == to_value:
            continue

        if not _is_null(from_instance, from_name):
            raise RelateException('instance is already related'
                                  ' (%s.%s=%s)' % (from_instance.__metaclass__.kind,
                                                   from_name, from_value))
        
        affected_instances.add(from_instance)
        setattr(from_instance, from_name, to_value)

    if affected_instances:
        for deferred_relate in post_process:
            affected_instances |= deferred_relate()

    return affected_instances


def unrelate(from_instance, to_instance, rel_id, phrase=''):
    '''
    Unrelate *from_instance* from *to_instance* across *rel_id*. For reflexive
    associations, a *phrase* indicating the direction must also be provided.
    
    The two instances are unrelated from each other by reseting the identifying
    attributes on the FROM side of the association. Updated values which affect
    existing associations are propagated. A set of all affected instances will
    be returned.
    '''
    affected_instances = set()
    if None in [from_instance, to_instance]:
        return affected_instances
    
    from_instance, to_instance, link = _find_link(from_instance, to_instance,
                                                  rel_id, phrase)
    post_process = _deferred_link_operation(from_instance, link, unrelate)

    for from_name in link.key_map:
        if _is_null(from_instance, from_name):
            raise UnrelateException('instances are not related')

        if not from_name in from_instance.__metaclass__.identifying_attributes:
            affected_instances.add(from_instance)
            setattr(from_instance, from_name, None)

    if affected_instances:
        for deferred_unrelate in post_process:
            affected_instances |= deferred_unrelate()
        
    return affected_instances


def delete(instance):
    '''
    Delete an *instance* from its metaclass instance pool.
    '''
    if not isinstance(instance, Class):
        raise DeleteException("the provided argument is not an xtuml instance")
            
    return instance.__metaclass__.delete(instance)


class MetaModel(object):
    '''
    A metamodel contains metaclasses with associations between them.
    
    **Note:** All identifiers, e.g. attributes, association ids, key letters 
    (the kind or name of a class), are case **insensitive**.
    '''
    metaclasses = None
    associations = None
    id_generator = None
    
    def __init__(self, id_generator=None):
        '''
        Create a new, empty metamodel. Optionally, specify an id generator
        used to obtain unique identifiers.
        '''
        if id_generator is None:
            id_generator = xtuml.UUIDGenerator()
        
        self.metaclasses = dict()
        self.associations = list()
        self.id_generator = id_generator
    
    @property
    def instances(self):
        '''
        Obtain a sequence of all instances in the metamodel.
        '''
        for metaclass in self.metaclasses.values():
            for inst in metaclass.storage:
                yield inst
    
    def define_class(self, kind, attributes, doc=''):
        '''
        Define a new class in the metamodel, and return its metaclass.
        '''
        ukind = kind.upper()
        if ukind in self.metaclasses:
            raise MetaModelException('A class with the name %s is already defined' % kind)

        metaclass = MetaClass(kind, self)
        for name, ty in attributes:
            metaclass.append_attribute(name, ty)
            
        self.metaclasses[ukind] = metaclass
        
        return metaclass

    def find_class(self, kind):
        '''
        Find a class of some *kind* in the metamodel.
        '''
        return self.find_metaclass(kind).clazz

    def find_metaclass(self, kind):
        '''
        Find a metaclass of some *kind* in the metamodel.
        '''
        ukind = kind.upper()
        if ukind in self.metaclasses:
            return self.metaclasses[ukind]
        else:
            raise UnknownClassException(kind)

    def new(self, kind, *args, **kwargs):
        '''
        Create and return a new instance in the metamodel of some *kind*.
        
        Optionally, initial attribute values may be assigned to the new instance
        by passing them as positional or keyword arguments. Positional arguments
        are assigned in the order in which they appear in the metaclass.
        '''
        metaclass = self.find_metaclass(kind)
        return metaclass.new(*args, **kwargs)
        
    def clone(self, instance):
        '''
        Create a shallow clone of an *instance*.
        
        **Note:** the clone and the original instance **does not** have to be
        part of the same metaclass. 
        '''
        metaclass = self.find_metaclass(instance.__metaclass__.kind)
        return metaclass.clone(instance)
            
    def define_association(self, rel_id, source_kind, source_keys, source_many,
                           source_conditional, source_phrase, target_kind, 
                           target_keys, target_many, target_conditional, 
                           target_phrase):
        '''
        Define and return an association from one kind of class (the source 
        kind) to some other kind of class (the target kind).
        '''
        if isinstance(rel_id, int):
            rel_id = 'R%d' % rel_id
            
        source_metaclass = self.find_metaclass(source_kind)
        target_metaclass = self.find_metaclass(target_kind)
        key_map = dict(zip(source_keys, target_keys))
        
        link1 = source_metaclass.add_link(target_metaclass, rel_id, key_map,
                                          many=target_many, phrase=target_phrase,
                                          conditional=target_conditional)
        
        link2 = target_metaclass.add_link(source_metaclass, rel_id, key_map,
                                          many=source_many, phrase=source_phrase,
                                          conditional=source_conditional, reverse=True)
        
        ass = Association(rel_id, link1, link2)
        self.associations.append(ass)

        return ass
        
    def define_unique_identifier(self, kind, name, *named_attributes):
        '''
        Define a unique identifier for some *kind* of class based on its
        *named attributes*.
        '''
        if not named_attributes:
            return
        
        if isinstance(name, int):
            name = 'I%d' % name
        
        metaclass = self.find_metaclass(kind)
        metaclass.indices[name] = tuple(named_attributes)

    def select_many(self, kind, where_clause=None):
        '''
        Query the metamodel for a set of instances of some *kind*. Optionally,
        a conditional *where-clause* in the form of a function may be provided.
        
        Usage example:
        
        >>> m = xtuml.load_metamodel('db.sql')
        >>> inst_set = m.select_many('My_Class', lambda sel: sel.number > 5)
        '''
        metaclass = self.find_metaclass(kind)
        return metaclass.select_many(where_clause)
    
    def select_one(self, kind, where_clause=None):
        '''
        Query the metamodel for a single instance of some *kind*. Optionally, a
        conditional *where-clause* in the form of a function may be provided.
        
        Usage example:
        
        >>> m = xtuml.load_metamodel('db.sql')
        >>> inst = m.select_one('My_Class', lambda sel: sel.name == 'Test')
        '''
        metaclass = self.find_metaclass(kind)
        return metaclass.select_one(where_clause)
    
    # Backwards compatabillity with older versions of pyxtuml
    select_any = select_one

    def is_consistent(self):
        '''
        Check the metamodel for integrity violations.
        '''
        if xtuml.check_association_integrity(self):
            return False
        
        return xtuml.check_uniqueness_constraint(self) == 0


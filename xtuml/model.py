# encoding: utf-8
# Copyright (C) 2015 John Törnblom

from itertools import chain
from functools import partial

import logging
import uuid
import collections

try:
    from future_builtins import filter, zip
except ImportError:
    pass

import xtuml


logger = logging.getLogger(__name__)


class ModelException(Exception):
    pass


def navigation(handle, kind, relid, phrase):
    kind = kind.upper()
    if isinstance(relid, int):
        relid = 'R%d' % relid

    for start_inst in iter(handle):
        query = start_inst.__q__[kind][relid][phrase]
        for inst in query(start_inst):
            yield inst


class NavChain(object):
    '''
    A navigation chain initializes a query from one or more instances.
    Queries may be syntactically cascaded in several ways:
    
       res = NavChain(inst).nav('X', 'R100', 'phrase').nav('Y', 101)

    or using an OAL/RSL inspired syntax:
    
       res = NavChain(inst).X[100, 'phrase'].Y[101](lamda x: <filter expression>)
    '''
    
    def __init__(self, handle):
        if handle is None:
            handle = []
            
        elif isinstance(handle, BaseObject):
            handle = [handle]
        
        elif not isinstance(handle, collections.Iterable):
            raise ModelException("Unable to navigate across '%s'" % type(handle))
        
        self.handle = handle
        self._kind = None
        
    def nav(self, kind, relid, phrase=''):
        self.handle = navigation(self.handle, kind, relid, phrase)
        return self
    
    def __getattr__(self, name):
        self._kind = name
        return self
    
    def __getitem__(self, args):
        if not isinstance(args, tuple):
            args = (args, '')
        
        relid, phrase = args
        
        return self.nav(self._kind, relid, phrase)


class NavOneChain(NavChain):
    
    def __call__(self, where_clause=None):
        handle = self.handle or list()
        if not where_clause:
            where_clause = lambda sel: True
        
        for inst in handle:
            if where_clause(inst):
                return inst


class NavManyChain(NavChain):
    
    def __call__(self, where_clause=None):
        handle = self.handle or list()
        return QuerySet(filter(where_clause, handle))


class Association(object):
    '''
    An association connects two classes to each other via two association links.
    '''
    
    def __init__(self, relid, source, target):
        if isinstance(relid, int):
            relid = 'R%d' % relid
        self.id = relid
        self.source = source
        self.target = target    

    @property
    def is_reflexive(self):
        return self.source.kind.upper() == self.target.kind.upper()

    
class AssociationLink(object):
    '''
    An association link represent an end point in an association.
    '''
    
    def __init__(self, kind, cardinality, ids, phrase=''):
        self.cardinality = cardinality
        self.kind = kind
        self.phrase = phrase
        self.ids = ids

    @property
    def is_many(self):
        return self.cardinality.upper() in ['M', 'MC']

    @property
    def is_conditional(self):
        return 'C' in self.cardinality.upper()


class SingleAssociationLink(AssociationLink):
    '''
    An association link that identifies an end point with cardinality 0..1 or 1.
    '''
    
    def __init__(self, kind, conditional=False, ids=[], phrase=''):
        if conditional: cardinality = '1C'
        else:           cardinality = '1'
        AssociationLink.__init__(self, kind, cardinality, ids, phrase)


class ManyAssociationLink(AssociationLink):
    '''
    An association link that identifies an end point with cardinality * or 1..*.
    '''
    
    def __init__(self, kind, conditional=False, ids=[], phrase=''):
        if conditional: cardinality = 'MC'
        else:           cardinality = 'M'
        AssociationLink.__init__(self, kind, cardinality, ids, phrase)
        

class OrderedSet(collections.MutableSet):
    '''
    Set that remembers original insertion order.
    '''
    # Originally posted on http://code.activestate.com/recipes/576694
    # by Raymond Hettinger.
    
    def __init__(self, iterable=None):
        self.end = end = [] 
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:        
            key, prev, next_ = self.map.pop(key)
            prev[2] = next_
            next_[1] = prev

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        
        if last:
            key = self.end[1][0]
        else:
            key = self.end[2][0]
            
        self.discard(key)
        return key
    
    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if not isinstance(other, OrderedSet):
            return self == OrderedSet(iter(other))
        
        if not len(self) == len(other):
            return False
        
        return list(self) == list(other)


class QuerySet(OrderedSet):
    '''
    An ordered set which holds instances that match queries from a metamodel.
    '''
    
    @property
    def first(self):
        if len(self):
            return next(iter(self))
    
    @property
    def last(self):
        if len(self):
            return next(reversed(self))


class Query(object):
    result = None
    generator = None
    
    def __init__(self, table, kwargs):
        self.result = collections.deque()
        self.items = collections.deque(kwargs.items())
        self.table = table
        self.generator = self.mk_generator()
        
    def mk_generator(self):
        for inst in iter(self.table):
            for name, value in iter(self.items):
                if getattr(inst, name) != value or _is_null(inst, name):
                    break
            else:
                self.result.append(inst)
                yield inst
    
        self.generator = None
    
    def execute(self):
        for inst in self.result:
            yield inst
            
        while self.generator:
            yield next(self.generator)
        
        
class BaseObject(object):
    '''
    A common base object for all instances created in a metamodel. Accesses 
    to attributes, e.g. getattr/setattr, on these objects are case insensitive.
    '''
    __r__ = None  # store relations
    __q__ = None  # store predefined queries
    __m__ = None  # store a handle to the metamodel which created the instance
    __c__ = dict()  # store a cached results from queries
    __a__ = list()  # store a list of attributes (name, type)
    __i__ = set() # set of identifying attributes
    __d__ = set() # set of derived attributes
    __u__ = dict() # store unique identifiers
    
    def __init__(self):
        self.__c__.clear()
        
    def __add__(self, other):
        assert isinstance(other, BaseObject)
        return QuerySet([self, other])

    def __sub__(self, other):
        assert isinstance(other, BaseObject)
        if self == other: return QuerySet()
        else: return QuerySet([self])

    def __getattr__(self, name):
        uname = name.upper()
        for attr, _ in self.__a__:
            if attr.upper() == uname:
                return self.__dict__[attr]

        return object.__getattribute__(self, name)
    
    def __setattr__(self, name, value):
        uname = name.upper()
        for attr, _ in self.__a__:
            if attr.upper() == uname:
                self.__dict__[attr] = value
                self.__c__.clear()
                return

        self.__dict__[name] = value
        
    def __str__(self):
        return str(self.__dict__)
    
    
class IdGenerator(object):
    '''
    Base class for generating unique identifiers in a metamodel.
    '''
    
    readfunc = None

    def __init__(self):
        '''
        Initialize an id generator with a start value.
        '''
        self._current = self.readfunc()
    
    def peek(self):
        '''
        Peek at the current value without progressing to the next one.
        '''
        return self._current
    
    def next(self):
        '''
        Progress to the next identifier, and return the current one.
        '''
        val = self._current
        self._current = self.readfunc()
        return val
    
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()


class UUIDGenerator(IdGenerator):
    '''
    A uuid-based id generator for metamodels. 128-bit unique identifiers
    are generated randomly when requested by a metamodel. 
    
    **Note:** This is the default id generator.
    '''
    def readfunc(self):
        return uuid.uuid4().int


class IntegerGenerator(IdGenerator):
    '''
    An integer-based id generator for metamodels. integers are generated
    sequentially, starting from the number one. 
    
    Generally, the uuid-based id generator shall be used. In some cases such as 
    testing however, having deterministic unique ids in a metamodel may be 
    benifitial.
    
    Usage example:
    
    >>> l = xtuml.ModelLoader()
    >>> l.filename_input("schema.sql")
    >>> l.filename_input("data.sql")
    >>> m = l.build_metamodel(xtuml.IntegerGenerator())
    '''
    
    _current = 0
    def readfunc(self):
        return self._current + 1


def _is_null(inst, name):
    value = getattr(inst, name)
    if value:
        return False
    
    elif value is None:
        return True

    name = name.upper()
    for attr_name, attr_ty in inst.__a__:
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

        
class MetaModel(object):
    '''
    A metamodel contains class definitions with associations between them,
    and instances of different kinds of classes.
    
    **Note:** All identifiers, e.g. attributes, association ids, key letters 
    (the kind or name of a class), are case **insensitive**.
    '''
    
    classes = None
    instances = None
    associations = None
    id_generator = None
    
    def __init__(self, id_generator=None):
        '''
        Create a new, empty metamodel. 
        Optionally, specify an id generator used to obtain unique identifiers.
        '''
        if id_generator is None:
            id_generator = UUIDGenerator()
            
        self.classes = dict()
        self.instances = dict()
        self.associations = list()
        self.id_generator = id_generator
        
    def define_class(self, kind, attributes, doc=''):
        '''
        Define and return a new class in the metamodel.
        '''
        ukind = kind.upper()
        if ukind in self.classes.keys() or ukind in self.instances.keys():
            raise ModelException('A class with the name %s is already defined' % kind)
    
        Cls = type(kind, (BaseObject,), dict(__r__=dict(), __q__=dict(),
                                             __c__=dict(), __m__=self,
                                             __i__=set(), __d__=set(),
                                             __u__=dict(), __doc__=doc,
                                             __a__=attributes))
        self.classes[ukind] = Cls
        self.instances[ukind] = list()
        
        return Cls

    def new(self, kind, *args, **kwargs):
        '''
        Create and return a new instance in the metamodel of some *kind*.
        
        Optionally, initial attribute values may be assigned to the new instance
        by passing them as positional or keyword arguments. Positional arguments
        are assigned in the order in which they appear in the metamodel schema.
        '''
        ukind = kind.upper()
        if ukind not in self.classes:
            raise ModelException("Unknown class %s" % kind)
            
        Cls = self.classes[ukind]
        inst = Cls()
        
        # set all attributes with an initial default value
        for name, ty in inst.__a__:
            if name in inst.__d__:
                value = None
            else:
                value = self._default_value(ty)
            setattr(inst, name, value)
            
        # set all positional arguments
        for attr, value in zip(inst.__a__, args):
            name, ty = attr
            setattr(inst, name, value)
            
        # set all named arguments
        for name, value in kwargs.items():
            setattr(inst, name, value)
            
        self.instances[ukind].append(inst)
        
        return inst
    
    def clone(self, instance):
        '''
        Create a shallow clone of an *instance*.
        
        **Note:** the clone and the original instance **does not** have to be
        part of the same metamodel. 
        '''
        clone = self.new(instance.__class__.__name__)
        for name, _ in instance.__a__:
            value = getattr(instance, name)
            setattr(clone, name, value)
            
        return clone
        
    def define_relation(self, rel_id, source, target):
        '''
        This method is deprecated. Use *define_association* instead.
        '''
        return self.define_association(rel_id, source, target)
    
    def define_association(self, rel_id, source, target):
        '''
        Define and return an association between *source* to *target* named 
        *rel_id*.
        '''
        ass = Association(rel_id, source, target)
        self.associations.append(ass)
        
        source_kind = source.kind.upper()
        target_kind = target.kind.upper()
        
        Source = self.classes[source_kind]
        Target = self.classes[target_kind]

        Source.__d__ |= set(ass.source.ids)
        Target.__i__ |= set(ass.target.ids)
        
        if ass.id not in Source.__r__:
            Source.__r__[ass.id] = set()
            
        if ass.id not in Target.__r__:
            Target.__r__[ass.id] = set()
            
        Source.__r__[ass.id].add(ass)
        Target.__r__[ass.id].add(ass)
        
        if target_kind not in Source.__q__:
            Source.__q__[target_kind] = dict()
            
        if source_kind not in Target.__q__:
            Target.__q__[source_kind] = dict()
        
        if ass.id not in Source.__q__[target_kind]:
            Source.__q__[target_kind][ass.id] = dict()
            
        if ass.id not in Target.__q__[source_kind]:
            Target.__q__[source_kind][ass.id] = dict()
        
        Source.__q__[target_kind][ass.id][target.phrase] = self._formalized_query(source, target)
        Target.__q__[source_kind][ass.id][source.phrase] = self._formalized_query(target, source)
    
        return ass
        
    def define_unique_identifier(self, kind, name, *named_attributes):
        '''
        Define a unique identifier for some *kind* of class based on its *named attributes*
        '''
        if not named_attributes:
            return
        
        kind = kind.upper()
        if isinstance(name, int):
            name = 'I%d' % name
        
        Cls = self.classes[kind]
        Cls.__u__[name] = set(named_attributes)

    def select_many(self, kind, where_clause=None):
        '''
        Query the metamodel for a set of instances of some *kind*. Optionally,
        a conditional *where-clause* in the form of a function may be provided.
        
        Usage example:
        
        >>> m = xtuml.load_metamodel('db.sql')
        >>> inst_set = m.select_many('My_Class', lambda sel: sel.number > 5)
        '''
        ukind = kind.upper()
        if ukind not in self.instances:
            raise ModelException("Unknown class %s" % kind)

        return QuerySet(filter(where_clause, self.instances[ukind]))
    
    def select_any(self, kind, where_clause=None):
        '''
        This method is deprecated. Use *select_any* instead.
        '''
        return self.select_one(kind, where_clause)
    
    def select_one(self, kind, where_clause=None):
        '''
        Query the model for a single instance of some *kind*. Optionally, a
        conditional *where-clause* in the form of a function may be provided.
        
        Usage example:
        
        >>> m = xtuml.load_metamodel('db.sql')
        >>> inst = m.select_one('My_Class', lambda sel: sel.name == 'Test')
        '''
        ukind = kind.upper()
        if ukind not in self.instances:
            raise ModelException("Unknown class %s" % kind)

        s = filter(where_clause, self.instances[ukind])
        return next(s, None)
        
    def is_consistent(self):
        '''
        Check the model for integrity violations.
        '''
        if not xtuml.check_association_integrity(self):
            return False
        
        return xtuml.check_uniqueness_constraint(self)
    
    def _default_value(self, ty_name):
        '''
        Obtain the default value for a named metamodel type.
        '''
        uname = ty_name.upper()
        if   uname == 'BOOLEAN': return False
        elif uname == 'INTEGER': return 0
        elif uname == 'REAL': return 0.0
        elif uname == 'STRING': return ''
        elif uname == 'UNIQUE_ID': return next(self.id_generator)
        else: raise ModelException("Unknown type named '%s'" % ty_name)
        
    def _select_endpoint(self, inst, source, target, kwargs):
        target_kind = target.kind.upper()
        if not target_kind in self.instances:
            return frozenset()
        
        keys = chain(target.ids, kwargs.keys())
        values = chain([getattr(inst, name) for name in source.ids],
                       kwargs.values())
        kwargs = dict(zip(keys, values))

        cache_key = frozenset(list(kwargs.items()))
        cache = self.classes[target_kind].__c__
        if cache_key not in cache:
            cache[cache_key] = Query(self.instances[target_kind], kwargs)
            
        return cache[cache_key].execute()

    def _formalized_query(self, source, target):
        return lambda inst, **kwargs: self._select_endpoint(inst, source,
                                                            target, kwargs)
    

def _find_association_links(inst1, inst2, rel_id, phrase):
    '''
    Find association links which correspond to the given arguments.
    '''
    if isinstance(rel_id, int):
        rel_id = 'R%d' % rel_id
    
    kind1 = inst1.__class__.__name__.upper()
    kind2 = inst2.__class__.__name__.upper()
    
    if (rel_id not in inst1.__r__ or
        rel_id not in inst2.__r__):
        raise ModelException('Unknown association %s---(%s)---%s' % (kind1,
                                                                     rel_id,
                                                                     kind2))
    for ass in chain(inst1.__r__[rel_id], inst2.__r__[rel_id]):
        source_kind = ass.source.kind.upper()
        target_kind = ass.target.kind.upper()
        
        if  (kind1 == source_kind and 
             kind2 == target_kind and 
             ass.source.phrase == phrase):
            return inst1, inst2, ass
        
        elif (kind1 == target_kind and 
              kind2 == source_kind and 
              ass.target.phrase == phrase):
            return inst2, inst1, ass

    raise ModelException("Unknown association %s---(%s.'%s')---%s" % (inst1.__class__.__name__,
                                                                      rel_id,
                                                                      phrase,
                                                                      inst2.__class__.__name__))


def _deferred_association_operation(inst, end, op):
    '''
    Generate list of deferred operations which needs to be invoked after an 
    update to identifying attributes on the association end point is made.
    '''
    kind = inst.__class__.__name__.upper()
    l = list()
    for ass in chain(*inst.__r__.values()):
        if kind != ass.target.kind.upper():
            continue
        if not set(end.ids) & inst.__d__ - inst.__i__ & set(ass.target.ids):
            # TODO: what about attributes which are both identifying, and referential?
            continue

        nav = navigate_many(inst).nav(ass.source.kind, ass.id, ass.source.phrase)
        for from_inst in nav():
            fn = partial(op, from_inst, inst, ass.id, ass.target.phrase)
            l.append(fn)

    return l


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
    return NavManyChain(instance_or_set)


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

    for kind, query in supertype.__q__.items():
        if rel_id not in query:
            continue
        
        subtype = navigate_one(supertype).nav(kind, rel_id)()
        if subtype:
            return subtype


def sort_reflexive(set_of_instances, rel_id, phrase):
    '''
    Sort a *set of instances* in the order they appear across a conditional and
    reflexive association. The first instance in the resulting ordered set is
    **not** associated to an instance across the given *phrase*.
    '''
    if (not isinstance(set_of_instances, QuerySet) or 
        not set_of_instances.first):
        return QuerySet()
    
    if isinstance(rel_id, int):
        rel_id = 'R%d' % rel_id
        
    kind = type(set_of_instances.first).__name__.upper()
    ass = next(iter(set_of_instances.first.__r__[rel_id]))
    if ass.source.phrase == phrase:
        other_phrase = ass.target.phrase
    else:
        other_phrase = ass.source.phrase
        
    first_filt = lambda sel: not navigate_one(sel).nav(kind, rel_id, phrase)()
    set_of_instances.first.__r__[rel_id]
    def sequence_generator():
        count = 0
        for inst in filter(first_filt, set_of_instances):
            while inst:
                count += 1
                yield inst
                inst = navigate_one(inst).nav(kind, rel_id, other_phrase)()
                
                if count > len(set_of_instances):
                    raise ModelException('Detected recursion in '
                                         'reflexive navigation')
                
    return QuerySet(sequence_generator())

    
def relate(from_instance, to_instance, rel_id, phrase=''):
    '''
    Relate *from_instance* to *to_instance* across *rel_id*. For refelxive
    association, a *phrase* indicating the direction must also be provided.
    
    The two instances are related to each other by copying the identifying 
    attributes from the instance on the TO side of a association to the instance
    n the FROM side. Updated values which affect existing associations are 
    propagated.
    '''
    if None in [from_instance, to_instance]:
        return False
    
    from_instance, to_instance, ass = _find_association_links(from_instance,
                                                              to_instance,
                                                              rel_id,
                                                              phrase)
                                                      
    post_process = _deferred_association_operation(from_instance, ass.source,
                                                   relate)

    updated = False
    for from_name, to_name in zip(ass.source.ids, ass.target.ids):
        if _is_null(to_instance, to_name):
            raise ModelException('undefined referential attribute %s' % to_name)
        
        from_value = getattr(from_instance, from_name)
        to_value = getattr(to_instance, to_name)

        if from_value == to_value:
            continue

        if not _is_null(from_instance, from_name):
            raise ModelException('instance is already related')
        
        updated = True
        setattr(from_instance, from_name, to_value)

    if updated:
        for deferred_relate in post_process:
            deferred_relate()

    return updated


def unrelate(from_instance, to_instance, rel_id, phrase=''):
    '''
    Unrelate *from_instance* from *to_instance* across *rel_id*. For refelxive
    association, a *phrase* indicating the direction must also be provided.
    
    The two instances are unrelated from each other by reseting the identifying
    attributes on the FROM side of the association. Updated values which affect
    existing associations are propagated.
    '''
    if None in [from_instance, to_instance]:
        return False
    
    from_instance, to_instance, ass = _find_association_links(from_instance,
                                                              to_instance,
                                                              rel_id,
                                                              phrase)
                                                              
    post_process = _deferred_association_operation(from_instance, ass.source,
                                                   unrelate)

    updated = False
    from_names = set(ass.source.ids) & from_instance.__d__ - from_instance.__i__
    for from_name in from_names:
        if _is_null(from_instance, from_name):
            raise ModelException('instances not related')
        
        updated = True
        setattr(from_instance, from_name, None)

    if updated:
        for deferred_unrelate in post_process:
            deferred_unrelate()
        
    return updated


def delete(instance):
    '''
    Delete an *instance* from its metamodel.
    '''
    if not isinstance(instance, BaseObject):
        raise ModelException("not an xtuml instance")
            
    kind = instance.__class__.__name__.upper()
    if kind not in instance.__m__.classes:
        raise ModelException("Unknown class %s" % instance.__class__.__name__)
        
    if instance in instance.__m__.instances[kind]:
        instance.__m__.instances[kind].remove(instance)
        instance.__class__.__c__.clear()
    else:
        raise ModelException("Instance not found in its model")


def where_eq(**kwargs):
    '''
    Return a where-clause function which filters out instances based on named 
    keywords.
    
    Usage example:
    
    >>> from xtuml import where_eq as where
    >>> m = xtuml.load_metamodel('db.sql')
    >>> inst = m.select_any('My_Modeled_Class', where(My_Number=5))
    '''
    items = list(kwargs.items())
    def query_filter(selected):
        for name, value in items:
            if getattr(selected, name) != value:
                return False
            
        return True

    return query_filter


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
import uuid


class IdGenerator(object):
    '''
    Base class for generating unique identifiers.
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
    A uuid-based id generator. 128-bit unique numbers are generated
    randomly each time a new id is requested.
    '''
    def readfunc(self):
        return uuid.uuid4().int


class IntegerGenerator(IdGenerator):
    '''
    An integer-based id generator. Integers are generated sequentially,
    starting from the number one. 
    
    Generally, the uuid-based id generator shall be used. In some cases such as
    testing however, having deterministic unique ids may be benifitial.
    
    Usage example:
    
    >>> l = xtuml.ModelLoader()
    >>> l.filename_input("schema.sql")
    >>> l.filename_input("data.sql")
    >>> m = l.build_metamodel(xtuml.IntegerGenerator())
    '''
    
    _current = 0
    def readfunc(self):
        return self._current + 1


class Visitor(object):
    '''
    A visitor may be used to visit tree nodes walked by a walker.
    '''
    
    def enter(self, node):
        '''
        Tries to invoke a method matching the pattern *enter_<type name>*, where
        <type name> is the name of the type of the *node*.
        '''
        name = 'enter_' + node.__class__.__name__
        fn = getattr(self, name, self.default_enter)
        fn(node)

    def leave(self, node):
        '''
        Tries to invoke a method matching the pattern *leave_<type name>*, where
        <type name> is the name of the type of the *node*.
        '''
        name = 'leave_' + node.__class__.__name__
        fn = getattr(self, name, self.default_leave)
        fn(node)

    def default_enter(self, node):
        '''
        The default behaviour when entering a *node* if no other action is
        defined by a subclass is to do nothing.
        '''
        pass

    def default_leave(self, node):
        '''
        The default behaviour when leaving a *node* if no other action is
        defined by a subclass is to do nothing.
        '''
        pass
    
    
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


class Walker(object):
    '''
    A walker may be used to walk a tree.
    '''
    def __init__(self):
        #: A list of *visitors* to notify when visiting nodes.
        self.visitors = list()
        
    def accept(self, node, **kwargs):
        '''
        Invoke the visitors before and after decending down the tree. 
        The walker will also try to invoke a method matching the pattern 
        *accept_<type name>*, where <type name> is the name of the accepted
        *node*.
        '''
        if node is None:
            return
        
        for v in self.visitors:
            v.enter(node)
        
        name = 'accept_' + node.__class__.__name__
        fn = getattr(self, name, self.default_accept)
        r = fn(node, **kwargs)
        
        for v in self.visitors:
            v.leave(node)
        
        return r
    
    def default_accept(self, node, **kwargs):
        '''
        The default accept behaviour is to decend into the iterable member
        *node.children* (if available).
        '''
        if not hasattr(node, 'children'):
            return
        
        for child in node.children:
            self.accept(child, **kwargs)


class NodePrintVisitor(Visitor):
    '''
    A visitor that prints a tree-like structure to stdout.
    '''
    
    def __init__(self):
        self._lvl = 0
        self._suppressed = list()
        
    def default_enter(self, node):
        text = self.render(node)
        if text is None:
            self._suppressed.append(node)
        else:
            print('%s%s' % ("  " * self._lvl, text))
            self._lvl += 1

    def default_leave(self, node):
        if self._suppressed and self._suppressed[-1] == node:
            self._suppressed.pop()
        else:
            self._lvl -= 1
    
    def render(self, node):
        '''
        Try to invoke a method matching the pattern *render_<type name>*, where
        <type name> is the name of the rendering *node*.
        '''
        name = 'render_' + type(node).__name__
        fn = getattr(self, name, self.default_render)
        return fn(node)
        
    def default_render(self, node):
        '''
        The default behaviour when rendering a *node* if no other rendering
        method is defined by a subclass is to render the class name.
        '''
        return type(node).__name__


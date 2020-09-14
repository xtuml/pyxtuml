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
pyxtuml is a python library for parsing, manipulating, and generating
BridgePoint xtUML models.
'''
from . import version

from .tools import IdGenerator
from .tools import UUIDGenerator
from .tools import IntegerGenerator
from .tools import OrderedSet

from .tools import Walker
from .tools import Visitor
from .tools import NodePrintVisitor

from .load import load_metamodel
from .load import ParsingException
from .load import ModelLoader

from .persist import persist_database
from .persist import persist_instances
from .persist import persist_schema
from .persist import persist_unique_identifiers

from .persist import serialize_database
from .persist import serialize_schema
from .persist import serialize_class
from .persist import serialize_classes
from .persist import serialize_association
from .persist import serialize_associations
from .persist import serialize_unique_identifiers
from .persist import serialize_instances
from .persist import serialize_instance
from .persist import serialize_value
from .persist import serialize

from .meta import Association
from .meta import Link

from .meta import QuerySet
from .meta import Class
from .meta import BaseObject
from .meta import MetaClass
from .meta import MetaModel

from .meta import MetaException
from .meta import DeleteException
from .meta import RelateException
from .meta import UnrelateException
from .meta import MetaModelException
from .meta import UnknownLinkException
from .meta import UnknownClassException

from .meta import navigate_any
from .meta import navigate_one
from .meta import navigate_many
from .meta import navigate_subtype
from .meta import relate
from .meta import unrelate
from .meta import delete
from .meta import cardinality
from .meta import where_eq
from .meta import sort_reflexive
from .meta import get_metaclass
from .meta import get_metamodel
from .meta import order_by
from .meta import reverse_order_by

from .consistency_check import check_association_integrity
from .consistency_check import check_uniqueness_constraint
from .consistency_check import check_subtype_integrity


#
# Suppress false import warning when invoking python3 -m xtuml.consistency_check.
# For details, see http://bugs.python.org/issue27487
#
import warnings
import sys

if not sys.warnoptions: # Overridable with -W flag
    warnings.filterwarnings('ignore', category=RuntimeWarning, module='runpy')


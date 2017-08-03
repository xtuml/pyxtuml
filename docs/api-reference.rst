API Reference
=============
xtuml
-----
The following section lists functions, classes and exceptions from the xtuml 
module. The operations are independent of the underlying metamodel definition, 
i.e. the sql schema.

Loading Metamodels
^^^^^^^^^^^^^^^^^^
.. autofunction:: xtuml.load_metamodel

.. autoclass:: xtuml.ModelLoader
   :members: build_metamodel, file_input, filename_input, input, populate

Metamodel Operations
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: xtuml.MetaModel
   :members: clone, new, find_class, find_metaclass, select_one, select_many

.. autofunction:: xtuml.navigate_one
.. autofunction:: xtuml.navigate_any
.. autofunction:: xtuml.navigate_many
.. autofunction:: xtuml.navigate_subtype
.. autofunction:: xtuml.relate
.. autofunction:: xtuml.unrelate
.. autofunction:: xtuml.delete
.. autofunction:: xtuml.cardinality
.. autofunction:: xtuml.where_eq
.. autofunction:: xtuml.sort_reflexive
.. autofunction:: xtuml.get_metamodel
.. autofunction:: xtuml.get_metaclass

.. autoclass:: xtuml.MetaClass
   :members: clone, new, select_one, select_many, query, navigate, delete,
	     attribute_names, append_attribute, insert_attribute, delete_attribute,
	     referential_attributes, identifying_attributes, attribute_type

.. autofunction:: xtuml.check_association_integrity
.. autofunction:: xtuml.check_uniqueness_constraint

Persistance
^^^^^^^^^^^
.. autofunction:: xtuml.persist_database
.. autofunction:: xtuml.persist_instances
.. autofunction:: xtuml.persist_schema

.. autofunction:: xtuml.serialize
.. autofunction:: xtuml.serialize_database
.. autofunction:: xtuml.serialize_schema
.. autofunction:: xtuml.serialize_instances
.. autofunction:: xtuml.serialize_instance

Tools
^^^^^
.. autoclass:: xtuml.UUIDGenerator

.. autoclass:: xtuml.IntegerGenerator

.. autoclass:: xtuml.Walker
   :members: accept, default_accept

   .. autoinstanceattribute:: xtuml.Walker.visitors
      
.. autoclass:: xtuml.Visitor
   :members: enter, leave, default_enter, default_leave
   
.. autoclass:: xtuml.NodePrintVisitor
   :members: render, default_render

Exceptions
^^^^^^^^^^
.. autoexception:: xtuml.ParsingException
.. autoexception:: xtuml.MetaException
.. autoexception:: xtuml.DeleteException
.. autoexception:: xtuml.RelateException
.. autoexception:: xtuml.UnrelateException
.. autoexception:: xtuml.MetaModelException
.. autoexception:: xtuml.UnknownLinkException
.. autoexception:: xtuml.UnknownClassException


bridgepoint
-----------
The following section lists functions and classes from the bridgepoint module. 
All operations require input expressed in the BridgePoint metamodel (ooaofooa).

Loading Models
^^^^^^^^^^^^^^
.. autofunction:: bridgepoint.load_metamodel

.. autoclass:: bridgepoint.ModelLoader
   :members: filename_input, build_component

Model Transformation
^^^^^^^^^^^^^^^^^^^^
.. autofunction:: bridgepoint.gen_text_action
.. autofunction:: bridgepoint.prebuild_action
.. autofunction:: bridgepoint.prebuild_model



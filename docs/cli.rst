Command Line Tools
==================

pyxtuml contain a few useful command line tools which are described below.

Consistency Check
-----------------
A model may be checked for association constraint violations. By default, all 
associations present in a model are checked. Optionally, the check may be
limited to one or more associations by appending the -r argument for each 
association to check.

::

   $ python -m xtuml.consistency_check [options] <sql_file> [another_sql_file...]

**Note:** both the model and its schema needs to be provided by the user.

**Available options**

===============  ===================================================
Option           Description
===============  ===================================================
--version        show program's version number and exit
--help, -h       show this help message and exit
-r NUMBER        limit consistency check to one or more associations
-k KEY_LETTER    limit check for uniqueness constraint violations to
                 one or more classes
--verbosity, -v  increase debug logging level
===============  ===================================================

BridgePoint metamodel
~~~~~~~~~~~~~~~~~~~~~
There is also a tool available that checks for constraint violations in ooaofooa,
the metamodel used by the BridgePoint editor. It can be used to detect various
fatal issues in a BridgePoint model, e.g. parameters that lacks a type.

::

   $ python -m bridgepoint.consistency_check [options] <model_path> [another_model_path...]


**Available options**

===============  ===================================================
Option           Description
===============  ===================================================
--version        show program's version number and exit
--help, -h       show this help message and exit
-r NUMBER        limit consistency check to one or more associations
-k KEY_LETTER    limit check for uniqueness constraint violations to
                 one or more classes
--globals, -g    add builtin global data types automatically, e.g.
                 boolean, integer and real
--verbosity, -v  increase debug logging level
===============  ===================================================

Model Execution
---------------
pyxtuml is able to execute BridgePoint functions, derived attributes and class 
operations (both class-based and instance-based). There is also support for the
built-in external entities ARCH and LOG. Asynchronous execution is currently 
not supported, i.e. events, signals and state machines.

::

   $ python -m bridgepoint.interpret [options] <model_path> [another_model_path...]


**Available options**

=========================  =========================================================
Option                     Description
=========================  =========================================================
--version                  show program's version number and exit
--help, -h                 show this help message and exit
--function=NAME, -f NAME   invoke a function named NAME
--component=NAME, -c NAME  look for the function to invoke in a component named NAME
--verbosity, -v            increase debug logging level
=========================  =========================================================

SQL Schema Generator
--------------------
To create an sql schema from a BridgePoint model, the following command may be used:

::

   $ python -m bridgepoint.gen_sql_schema [options] <model_path> [another_model_path...]

**Available options**

=========================  ==============================================
Option                     Description
=========================  ==============================================
--version                  show program's version number and exit
--help, -h                 show this help message and exit
--component=NAME, -c NAME  export sql schema for the component named NAME
--derived-attributes, -d   include derived attributes in the schema
--output=PATH, -o PATH     save sql schema to PATH (required)
--verbosity, -v            increase debug logging level
=========================  ==============================================

XSD Schema Generator
--------------------
To create an XSD schema for XML files, the following command may be used:

::

   $ python -m bridgepoint.gen_xsd_schema [options] <model_path> [another_model_path...]

**Available options**

=========================  ==============================================
Option                     Description
=========================  ==============================================
--version                  show program's version number and exit
--help, -h                 show this help message and exit
--component=NAME, -c NAME  export xsd schema for the component named NAME
--output=PATH, -o PATH     save xsd schema to PATH (required)
--verbosity, -v            increase debug logging level
=========================  ==============================================

Note that the XSD schema is compatible with Microsoft Excel. Consequently, Excel 
may be used to define instances in a model that can be easily exported to XML
files.

OAL Prebuilder
--------------
Generally, all model compilers takes as input an sql where all OAL actions
has been translated from its textual representation into instances in the 
ooaofooa meta model. This translation is usually conducted by the Eclipse-
based prebuilder included with the BridgePoint IDE. pyxtuml contains an 
independent prebuilder, implemented in python (and thus may be somewhat 
slower). The pyxtuml prebuilder may be invoked using the folling command:

::

   $ python -m bridgepoint.prebuild [options] <model_path> [another_model_path..]

**Available options**


======================  ======================================
Option                  Description
======================  ======================================
--version               show program's version number and exit
--help, -h              show this help message and exit
--verbosity, -v         increase debug logging level
--output=PATH, -o PATH  set output to PATH
======================  ======================================

Getting Started
===============

Dependencies
------------
In addition to python itself, pyxtuml also depend on the python library 
`ply <http://www.dabeaz.com/ply>`__. For people running Ubuntu, everything is
available via apt-get:

::

   $ sudo apt-get install python2.7 python-ply

pyxtuml also works with python3 and `pypy <http://pypy.org>`__.

Installation
------------
pyxtuml is published on `pypi <https://pypi.python.org>`__, and thus may be 
installed using pip:

::

    $ python -m pip install pyxtuml

You could also fetch the source code from github and install it manually:

::

    $ git clone https://github.com/xtuml/pyxtuml.git
    $ cd pyxtuml
    $ python setup.py install
   
Optionally, you can also execute a test suite:

::

    $ python setup.py test

Usage example
-------------

The `examples
folder <https://github.com/xtuml/pyxtuml/tree/master/examples>`__
contains a few scripts which demonstrate how pyxtuml may be used.

The following command will create an empty metamodel and populate it
with some sample data:

::

    $ python examples/create_external_entity.py > test.sql

Copy the SQL statements saved in test.sql to your clipboard, and paste
them into the BridgePoint editor with a project selected in the project
explorer.

If you are on a more recent GNU/Linux system, you can also pipe the
output directly to your clipboard without bouncing via disk:

::

    $ python examples/create_external_entity.py | xclip -selection clipboard


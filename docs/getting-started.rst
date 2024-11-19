Getting Started
===============

Dependencies
------------
pyxtuml requires ``python3`` and ``pip``. Follow instructions for your specific
system to install and configure. pyxtuml does not support ``python2``

`pyenv <https://github.com/pyenv/pyenv>`__ is a useful tool for managing
multiple versions of python on a single system.

pyxtuml also works with `pypy <http://pypy.org>`__.

In order to run the unit tests, ``pytest`` is required:

::

    $ python -m pip install pytest

Installation
------------
pyxtuml is published on `PyPI <https://pypi.python.org>`__, and thus may be 
installed using pip:

::

    $ python -m pip install pyxtuml

If you would like to use the most recent changes that might not have made it
into a release yet, you can bypass PyPI and install from github directly:

::

    $ python -m pip install git+https://github.com/xtuml/pyxtuml.git
   
You could also fetch the source code from github and manually,
which also allows you to run test cases:

::

    $ git clone https://github.com/xtuml/pyxtuml.git
    $ cd pyxtuml
    $ python -m pytest
    $ python -m pip install .

Add ``--editable`` to the last command for local changes to the repository to
take immediate effect.

Character encoding
------------------

pyxtuml requires all inputs to be UTF-8 encoded.

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


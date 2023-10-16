UNICEF Power Query
==================


Installation
------------

.. code-block:: bash

    pip install unicef-power-query


Setup
-----

Add ``power_query`` to ``INSTALLED_APPS`` in settings

.. code-block:: bash

    INSTALLED_APPS = [
        'power_query',
    ]


Usage
-----

TODO

Contributing
------------

Coding Standards
~~~~~~~~~~~~~~~~

See `PEP 8 Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_ for complete details on the coding standards.

To run checks on the code to ensure code is in compliance


Testing
~~~~~~~

Testing is important and tests are located in `tests/` directory and can be run with;

.. code-block:: bash

    $ pytest tests

Coverage report is viewable in `build/coverage` directory, and can be generated with;



Links
~~~~~

+--------------------+----------------+--------------+--------------------+
| Stable             | |master-build| | |master-cov| |                    |
+--------------------+----------------+--------------+--------------------+
| Development        | |dev-build|    | |dev-cov|    |                    |
+--------------------+----------------+--------------+--------------------+
| Source Code        |https://github.com/unicef/unicef-power-query           |
+--------------------+----------------+-----------------------------------+
| Issue tracker      |https://github.com/unicef/unicef-power-query/issues    |
+--------------------+----------------+-----------------------------------+


.. |master-build| image:: https://secure.travis-ci.org/unicef/unicef-power-query.svg?branch=master
                    :target: http://travis-ci.org/unicef/unicef-power-query/

.. |master-cov| image:: https://codecov.io/gh/unicef/unicef-power-query/branch/master/graph/badge.svg
                    :target: https://codecov.io/gh/unicef/unicef-power-query

.. |dev-build| image:: https://secure.travis-ci.org/unicef/unicef-power-query.svg?branch=develop
                  :target: http://travis-ci.org/unicef/unicef-power-query/

.. |dev-cov| image:: https://codecov.io/gh/unicef/unicef-power-query/branch/develop/graph/badge.svg
                    :target: https://codecov.io/gh/unicef/unicef-power-query

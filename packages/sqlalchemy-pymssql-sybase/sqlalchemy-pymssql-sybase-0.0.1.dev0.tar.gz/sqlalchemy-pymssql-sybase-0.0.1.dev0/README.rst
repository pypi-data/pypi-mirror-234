sqlalchemy-pymssql-sybase
=========================

.. image:: https://img.shields.io/pypi/dm/sqlalchemy-pymssql-sybase.svg
        :target: https://pypi.org/project/sqlalchemy-pymssql-sybase/

SAP ASE (Sybase) dialect for SQLAlchemy using PyMsSql.

The latest version of this dialect requires SQLAlchemy 2.0 or later and pymssql 2.2.8 or later

Overview
--------

This is a very  thin wrap around the SQLAlchemy's mssql+pymysql dialect
repurposed for connecting to sybase databases.

Database Version Support
------------------------

This dialect is tested against SAP ASE version 16.
Current support is very tiny

Installing
----------

SQLAlchemy and pymssql are specified as requirements so ``pip`` will install
them if they are not already in place. To install, just::

    pip install sqlalchemy-pymssql-sybase

Getting Started
---------------

To register the dialect, import the sqlalchemy_pymssql_sybase module somewhere in your app.
Then use sqlalchemy as usual::

    import sqlalchemy_pymssql_sybase
    from sqlalchemy import create_engine
    engine = create_engine("sybase+pymssql://user:password@host/database")


The SQLAlchemy Project
======================

sqlalchemy-pymssql-sybase is affiliated with the `SQLAlchemy Project <https://www.sqlalchemy.org>`_ and
adheres to the same standards and conventions as the core project.

Development / Bug reporting / Pull requests
-------------------------------------------

Please refer to the
`SQLAlchemy Community Guide <https://www.sqlalchemy.org/develop.html>`_ for
guidelines on coding and participating in this project.

Code of Conduct
_______________

Above all, SQLAlchemy places great emphasis on polite, thoughtful, and
constructive communication between users and developers.
Please see the current Code of Conduct at
`Code of Conduct <https://www.sqlalchemy.org/codeofconduct.html>`_.

License
=======

sqlalchemy-pymssql-sybase is distributed under the `MIT license
<https://opensource.org/licenses/MIT>`_.

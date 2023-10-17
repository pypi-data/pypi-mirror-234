# sybase/__init__.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from sqlalchemy.dialects import registry as _registry
from sqlalchemy.dialects.mssql import (
    CHAR, VARCHAR, VARBINARY, NCHAR, NVARCHAR, TEXT,
    TIME, DATE, DATETIME, FLOAT,
    NUMERIC, BIGINT, INTEGER, SMALLINT, TINYINT,
    BINARY, IMAGE, BIT, MONEY, SMALLMONEY
)
from . import pymssql  # noqa

__version__ = "0.0.1.dev0"

# default dialect
dialect = pymssql.dialect

_registry.register(
    "sybase.pymssql", "sqlalchemy_pymssql_sybase.pymssql", "SybaseDialect_pymssql"
)

__all__ = (
    "CHAR", "VARCHAR", "VARBINARY", "NCHAR", "NVARCHAR", "TEXT",
    "TIME", "DATE", "DATETIME", "FLOAT",
    "NUMERIC", "BIGINT", "INTEGER", "SMALLINT", "TINYINT",
    "BINARY", "IMAGE", "BIT", "MONEY", "SMALLMONEY",
    "dialect",
)

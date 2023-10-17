# sybase/pymssql.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""
.. dialect:: sybase+pymssql
    :name: pymssql
    :dbapi: pymssql
    :connectstring: sybase+pymssql://<username>:<password>@<dsnname>[/<database>]
    :url: http://pypi.python.org/pypi/pymssql/

"""  # noqa

import re
from sqlalchemy.dialects.mssql.pymssql import MSDialect_pymssql


class SybaseDialect_pymssql(MSDialect_pymssql):
    name = "sybase"

    def _get_default_schema_name(self, connection):
        return self.schema_name

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user")
        opts["conn_properties"] = ""
        opts.update(url.query)
        port = opts.pop("port", None)
        if port and "host" in opts:
            opts["host"] = "%s:%s" % (opts["host"], port)
        return ([], opts)

    def _get_server_version_info(self, connection):
        vers = connection.exec_driver_sql("select @@version").scalar()
        m = re.match(r"Adaptive Server Enterprise/(\d+)\.(\d+)", vers)
        if m:
            return tuple(int(x) for x in m.group(1, 2)) + (0, 0)
        else:
            return None

    def _setup_version_attributes(self):
        self.supports_multivalues_insert = False
        self.deprecate_large_types = False
        self._supports_offset_fetch = False
        self.supports_statement_cache = False

        if (
            self.server_version_info is not None
            and self.server_version_info < (15,)
        ):
            self.max_identifier_length = 30
        else:
            self.max_identifier_length = 255


dialect = SybaseDialect_pymssql

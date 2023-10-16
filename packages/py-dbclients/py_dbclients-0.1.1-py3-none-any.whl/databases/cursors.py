from collections import namedtuple

try:
    from pymysql.cursors import Cursor as PYMYSQL_CURSOR
    _has_pymysql = True
except ImportError:
    _has_pymysql = False

try:
    from aiomysql.cursors import Cursor as AIOMYSQL_CURSOR
    _has_aiomysql = True
except ImportError:
    _has_aiomysql = False
#--------------------------------------------------------------------------->

def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

if _has_aiomysql:
    class _AIOMYSQLNamedTupleMixin:
        # You can override this to use OrderedDict or other dict-like types.
        dict_type = namedtuple

        async def _do_get_result(self):
            await super()._do_get_result()
            fields = []
            if self._description:
                for f in self._result.fields:
                    name = f.name
                    if name in fields:
                        name = f.table_name + '.' + name
                    fields.append(name)
                self._fields = fields
                self.namedtuple = namedtuple("row", self._fields)

            if fields and self._rows:
                self._rows = [self._conv_row(r) for r in self._rows]

        def _conv_row(self, row):
            if row is None:
                return None
            row = super()._conv_row(row)
            return self.namedtuple(*row)


    class AIOMYSQL_NAMEDTUPLE_CURSOR(_AIOMYSQLNamedTupleMixin, AIOMYSQL_CURSOR):
        """A cursor which returns results as a namedtuple"""

if _has_pymysql:
    class _PYMYSQLNamedTupleMixin:
        # You can override this to use OrderedDict or other dict-like types.
        dict_type = dict

        def _do_get_result(self):
            super()._do_get_result()
            fields = []
            if self.description:
                for f in self._result.fields:
                    name = f.name
                    if name in fields:
                        name = f.table_name + "." + name
                    fields.append(name)
                self._fields = fields
                self.namedtuple = namedtuple("row", self._fields)

            if fields and self._rows:
                self._rows = [self._conv_row(r) for r in self._rows]

        def _conv_row(self, row):
            if row is None:
                return None
            row = super()._conv_row(row)
            return self.namedtuple(*row)

    class PYMYSQL_NAMEDTUPLE_CURSOR(_PYMYSQLNamedTupleMixin, PYMYSQL_CURSOR):
        """A cursor which returns results as a namedtuple"""
import time
from datetime import datetime

try:
    import aiomysql
    from aiomysql.cursors import Cursor, DictCursor
    from .cursors import AIOMYSQL_NAMEDTUPLE_CURSOR as NamedTupleCursor
    _has_aiomysql = True
except ImportError:
    _has_aiomysql = False

if _has_aiomysql:
    def execute_prior(func):
        async def wrapper(self, stmt, dt=(), *, cursor=None, database=None):
            conn, _cursor = await self.get_conn(cursor=cursor, database=database)
            try:
                results = await func(self, conn, _cursor, stmt, dt, cursor=cursor, database=database)
                
            except (aiomysql.OperationalError, aiomysql.InterfaceError):
                self = await self.__class__.new(**self.init_params)
                return wrapper(self, stmt, dt=dt, cursor=cursor, database=database)
            await self._post_query(conn, _cursor)

            return results
        return wrapper

    class BaseAIOMySQL:
        _CURSORS = {
            "default": Cursor,
            "dict": DictCursor,
            "namedtuple": NamedTupleCursor
        }
        def __init__(self, *, host="localhost", port=3306, user, password="", database, autocommit=False, cursor="default", pool=False, **kwargs):
            self.connection_params = dict(
                host=host,
                port=int(port),
                user=user,
                password=password,
                db=database,
                autocommit=autocommit
            )
            self.init_params = dict(
                **{key if key != "db" else "database": value for key, value in self.connection_params.items()},
                **kwargs,
                cursor=cursor,
                pool=pool   
            )
            self.__dict__.update(self.connection_params)

            self.conn = None
            self.use_pool = pool
            self._current_cursor = self._default_cursor = cursor
            self._current_database = self._default_database = database

        @property
        def default_database(self):
            return self._default_database

        @property
        def default_cursor(self):
            return self._default_cursor
        
        @classmethod
        @property
        def current_timestamp(self):
            return int(time.time())

        @classmethod
        @property
        def now(self):
            return datetime.now()
        
        @classmethod
        async def new(cls, *args, **kwargs):
            self = cls(*args, **kwargs)

            if self.use_pool:
                await self.create_pool()
            else:
                await self.connect()
            return self

        async def __aenter__(self):
            if self.use_pool:
                await self.create_pool()
            else:
                await self.connect()
            return self
        
        async def __aexit__(self, *args):
            if any(arg is not None for arg in args):
                print(*args)
            await self.close()

        async def close(self):
            if self.use_pool:
                self.conn.close()
                await self.conn.wait_closed()
            else:
                self.conn.close()

        async def connect(self):
            self.conn = await aiomysql.connect(**self.connection_params)

        async def create_pool(self):
            self.conn = await aiomysql.create_pool(**self.connection_params)

        async def get_conn(self, database=None, cursor=None):
            conn = await self.conn.acquire() if self.use_pool else self.conn
            if database is not None:
                conn = await self._switch_database(database, conn)

            _cursor = await conn.cursor()
            if cursor is not None:
                _cursor = await self._switch_cursor(_cursor, conn)
                    
            return (conn, _cursor)

        async def _switch_database(self, database, conn):
            await conn.select_db(db=database)
            self._current_database = database
            return conn

        async def _switch_cursor(self, cursor, conn):
            cursor = await conn.cursor(
                self._CURSORS[cursor]
            )
            return cursor
        
        async def _pre_query(self, conn, cursor=None, database=None):
            if database is not None:
                conn = await self._switch_database(database, conn)
            if cursor is not None:
                cursor = await self._switch_cursor(cursor, conn)
            return (conn, cursor)
        
        async def _post_query(self, conn, _cursor):
            await conn.commit()
            if self.use_pool:
                self.conn.release(conn)
                await _cursor.close()
            else:
                if self._current_database != self.default_database:
                    await self._switch_database(self.default_database, self.conn)

        @execute_prior
        async def execute(self, conn, _cursor, stmt, dt=(), *, cursor=None, database=None):
            return await _cursor.execute(stmt, dt)

        @execute_prior
        async def executemany(self, conn, _cursor, stmt, dt, *, cursor=None, database=None):
            return await _cursor.executemany(stmt, dt)

        @execute_prior
        async def query(self, conn, _cursor, stmt, dt=(), *, cursor=None, database=None):
            await _cursor.execute(stmt)
            return await _cursor.fetchall()
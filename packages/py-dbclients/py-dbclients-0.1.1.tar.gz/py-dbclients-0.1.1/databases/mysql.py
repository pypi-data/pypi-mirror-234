
import threading
import time
from datetime import datetime

try:
    import pymysql
    from pymysql.cursors import Cursor, DictCursor
    from .cursors import PYMYSQL_NAMEDTUPLE_CURSOR as NamedTupleCursor
    _has_pymysql = True
except ImportError:
    _has_pymysql = False

if _has_pymysql:
    class KeepaliveThread(threading.Thread):
        def __init__(self, target, args=(), **kwargs):
            super().__init__()
            self.target = target
            self.args = args
            self.kwargs = kwargs
            self._stop_event = threading.Event()
        
        def run(self):
            while not self._stop_event.is_set():
                self.target(*self.args, **self.kwargs)

        def stop(self):
            self._stop_event.set()


    def keepalive(db, **kwargs):
        try:
            db.conn.ping(reconnect=True)
            db.__CONNECTED__ = True
            time.sleep(5)
        except Exception as e:
            db.__CONNECTED__ = False
            while not db:
                try:
                    db.conn.ping(reconnect=True)
                    db.__CONNECTED__ = True
                except Exception as e:
                    time.sleep(1)


    def execute_prior(func):
        def wrapper(self, stmt, dt=(), *, cursor=None, database=None):
            previous_database = self.default_database
            try:
                self._pre_query(cursor=cursor, database=database)
                results = func(self, stmt, dt, cursor, database)
                
            except (pymysql.OperationalError, pymysql.InterfaceError):
                try:
                    self.conn.ping(reconnect=True)
                except:
                    time.sleep(1)
                return wrapper(self, stmt, dt=dt, cursor=cursor, database=database)
            self._post_query()
            self.conn.commit()
            return results
        return wrapper



    class BaseMySQL:
        _CURSORS = {
            "default": Cursor,
            "dict": DictCursor,
            "namedtuple": NamedTupleCursor
        }
        def __init__(self, *, user, database, host="localhost", port=3306, password="", cursor="default", keepalive=False, **kwargs):
            self.keepalive = False
            self.connection_params = dict(
                host=host,
                port=int(port),
                user=user,
                password=password,
                database=database
            )
            self.__dict__.update(self.connection_params)

            self.conn = None
            self._current_cursor = self._default_cursor = cursor
            self._current_database = self._default_database = database
            self.connect()
            if keepalive:
                self.keepalive = True
                self.start_ping_thread()

        def __repr__(self):
            return f"<MySQL host={self.host} port={self.port} user={self.user} database={self.database}>"
        

        def __enter__(self):
            return self
        
        def __exit__(self, *args):
            if any(arg is not None for arg in args):
                print(*args)
            self.close()
        
        def __bool__(self):
            return self.__CONNECTED__

        @property
        def default_database(self):
            return self._default_database
        
        @property
        def default_cursor(self):
            return self._default_cursor
        
        @property
        def current_cursor(self):
            if isinstance(self.cursor, pymysql.cursors.Cursor):
                return pymysql.cursors.Cursor
            elif isinstance(self.cursor, pymysql.cursors.DictCursor):
                return pymysql.cursors.DictCursor
            elif isinstance(self.cursor, NamedTupleCursor):
                return NamedTupleCursor
            else:
                return None
            
        @classmethod
        @property
        def current_timestamp(cls):
            return int(time.time())

        @classmethod
        @property
        def now(cls):
            return datetime.now()


        def reconnect(self):
            self = self.__class__(**self.connection_params)

        def connect(self):
            self.conn = pymysql.connect(
                host=self.host,
                port = self.port,
                user=self.user, 
                password=self.password, 
                database=self.database
            )

            self.cursor = self.conn.cursor(
                self._CURSORS[self._default_cursor]
            )
            self.__CONNECTED__ = True


        def start_ping_thread(self):
            self.thread = KeepaliveThread(target=keepalive, args=(self,), name="mysql-keepalive")
            self.thread.daemon = True
            self.thread.start()


        def stop_ping_thread(self):
            self.thread.stop()


        def close(self):
            self.conn.commit()
            self.conn.close()
            if self.keepalive:
                self.stop_ping_thread()
            self.__CONNECTED__ = False


        def _switch_cursor(self, cursor):
            if not isinstance(
                self.current_cursor,
                (cursor := self._CURSORS[cursor])
            ):
                self.cursor = self.conn.cursor(cursor)
                self._current_cursor = cursor
        

        def _switch_database(self, database):
            self.conn.select_db(database)
            self._current_database = database
        

        def _pre_query(self, *, cursor=None, database=None):
            if cursor is not None:
                self._switch_cursor(cursor)
            if database is not None:
                self._switch_database(database)


        def _post_query(self):
            if self._current_database != self.default_database:
                self._switch_database(database=self.default_database)
            if self._current_cursor != self.default_cursor:
                self._switch_cursor(cursor=self.default_cursor)
        

        @execute_prior    
        def query(self, stmt, dt=(), cursor=None, database=None):
            self.cursor.execute(stmt, dt)
            return self.cursor.fetchall()

        @execute_prior
        def execute(self, stmt, dt=(), cursor=None, database=None):
            return self.cursor.execute(stmt, dt)
        
        @execute_prior
        def executemany(self, stmt, dt, cursor=None, database=None):
            return self.cursor.executemany(stmt, dt)
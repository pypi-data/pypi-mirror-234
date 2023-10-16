import sqlite3
from time import time
from datetime import datetime
from .cursors import dict_factory, namedtuple_factory

def execute_prior(func):
    def wrapper(self, stmt, *, dt=(), cursor=None):
        self._pre_query(cursor=cursor or self._default_cursor)
        results = func(self, stmt, dt, cursor)
        self._post_query()        
        self.__CONNECTED__ = True
        self.conn.commit()
        return results
    return wrapper


class BaseSQLite:
    _CURSORS = {
        "default": None,
        "dict": dict_factory,
        "namedtuple": namedtuple_factory,
    }

    def __init__(self, path, cursor="default"):
        self.path = path
        self.__CONNECTED__ = False
        self.connect(path)

        self._current_cursor = self._default_cursor = cursor.lower()


    def __bool__(self):
        return self.__CONNECTED__
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if any(arg is not None for arg in args):
            print(args)
        self.close()

    @property
    def is_connected(self):
        return self.__CONNECTED__
    
    @classmethod
    @property
    def current_timestamp(cls):
        return int(time())
    
    @classmethod
    @property
    def now(cls):
        return datetime.now()
    

    def connect(self, path):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        self.__CONNECTED__ = True
    
    def close(self):
        self.conn.commit()
        self.conn.close()
        self.__CONNECTED__ = False

    def _pre_query(self, cursor, **kwargs):
        if self._current_cursor != cursor:
            self._current_cursor = cursor
            self.conn.row_factory = self._CURSORS[cursor]
            self.cursor = self.conn.cursor()
    
    def _post_query(self):
        if self._current_cursor != self._default_cursor:
            self._current_cursor = "default"
            self.conn.row_factory = self._CURSORS["default"]
            self.cursor = self.conn.cursor()

    def execute(self, stmt, dt=()):
        results = self.cursor.execute(stmt, dt)
        return results
    
    def executemany(self, stmt, dt):
        results = self.cursor.executemany(stmt, dt)
        return results
    
    @execute_prior
    def query(self, stmt, dt=(), cursor="default"):
        self.cursor.execute(stmt, dt)
        results = self.cursor.fetchall()
        return results
from __future__ import annotations
from abc import ABC, abstractmethod

from dataclasses import dataclass
from threading import local

from typing import Dict, Any, Optional, Type, List, Tuple, TypeVar
from types import TracebackType
from pathlib import Path

import atexit
import os
import sys
import tempfile

import numpy as np
import pandas as pd
import pyarrow as pa

from .settings import DatabaseSettings
import shapelets_native as sn

this = sys.modules[__name__]
this.settings = None
this.db = None
this.connections = dict()
this.transactions = dict()
this.tls = local()


@dataclass
class NativeDBSettings:
    schema: str
    options: List[Tuple[str, Any]]
    path: Optional[str] = None

    @staticmethod
    def from_settings(settings: DatabaseSettings) -> NativeDBSettings:

        path = None  # In-Memory by default
        if settings.path is not None:
            p = Path(os.path.expandvars(os.path.expanduser(settings.path)))
            p.parent.mkdir(exist_ok=True)
            path = str(p.resolve())

        opt = []

        if settings.temp_directory is not None:
            p = Path(os.path.expandvars(os.path.expanduser(settings.temp_directory)))
            p.mkdir(exist_ok=True)
            opt.append(('temp_directory', str(p.resolve())))
        else:
            tmp_dir = tempfile.TemporaryDirectory(suffix="tmp_db", prefix="sh")
            settings.temp_directory = str(tmp_dir.name)
            atexit.register(lambda: tmp_dir.cleanup())
            opt.append(('temp_directory', str(tmp_dir.name)))

        if settings.collation is not None:
            opt.append(('default_collation', str(settings.collation)))

        if settings.memory_limit is not None:
            opt.append(('max_memory', settings.memory_limit.human_readable()))

        if settings.threads is not None:
            opt.append(('threads', str(settings.threads)))

        if settings.order is not None:
            opt.append(('default_order', str(settings.order)))

        if settings.null_order is not None:
            opt.append(('default_null_order', f'NULLS_{settings.null_order}'))

        if settings.object_cache is not None:
            opt.append(('enable_object_cache', str(settings.object_cache)))

        return NativeDBSettings(settings.db_schema, opt, path)


class Connection:

    __slots__ = ('__conn', '__result')

    """
    A database connection.
    
    Connections are thread dependent and they should not be shared 
    among threads.
    """

    def __init__(self, connection: sn.Connection) -> None:
        self.__conn = connection
        self.__result = None

    def begin(self):
        self.__conn.begin()

    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()

    def execute(self, sql: str, params: Optional[object] = None):
        if params is None:
            self.__result = self.__conn.execute(sql, None, False)
        else:
            self.__result = self.__conn.execute(sql, params, False)

    def execute_many(self, sql: str, params: Optional[list] = None):
        if params is None:
            self.__result = self.__conn.execute(sql, None, True)
        else:
            self.__result = self.__conn.execute(sql, params, True)

    def fetch_one(self) -> Optional[Tuple[Any, ...]]:
        if self.__result is None:
            return None

        return self.__result.fetch_one()

    def fetch_all(self) -> List[Tuple[Any, ...]]:
        if self.__result is None:
            return []

        return self.__result.fetch_all()

    def fetch_many(self, count: int) -> List[Tuple[Any, ...]]:
        if self.__result is None:
            return []

        return self.__result.fetch_many(count)

    def to_numpy(self) -> Dict[str, np.array]:
        if self.__result is None:
            return {}
        return self.__result.to_numpy()

    def to_pandas(self) -> Optional[pd.DataFrame]:
        if self.__result is None:
            return None
        return self.__result.to_pandas()

    def to_arrow_table(self, batchRows: int = 1000000) -> pa.lib.Table:
        if self.__result is None:
            return None
        return self.__result.to_arrow_table(batchRows)

    def to_arrow_record_batch_reader(self, batchRows: int = 1000000) -> pa.lib.RecordBatchReader:
        if self.__result is None:
            return None

        return self.__result.to_arrow_record_batch_reader(batchRows)

    def close(self) -> None:
        self.__result = None
        self.__conn = None


class ScopedConnection(ABC):
    """
    A wrapper around connections to ensure properly and orderly 
    management of resources.

    On entering a instance of this wrapper, a connection 
    will be provided, whose life time will be associated with the 
    current thread.  
    """

    @abstractmethod
    def __enter__(self) -> Connection:
        pass

    @abstractmethod
    def __exit__(self,
                 type: Optional[Type[BaseException]],
                 value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Optional[bool]:
        pass


class ConnectionWrapper(ScopedConnection):
    """
    Manages database connections 
    """

    __slots__ = ('__refCount', '__dbConnection')

    def __init__(self) -> None:
        self.__refCount = 0
        self.__dbConnection = None

    def get_connection(self) -> Connection:
        self.__refCount += 1
        if self.__refCount == 1:
            self.__dbConnection = this.db.connect()

        connObj = Connection(self.__dbConnection)

        if self.__refCount == 1:
            connObj.execute(f"CREATE SCHEMA IF NOT EXISTS {this.settings.schema};")
            connObj.execute(f"SET SCHEMA = '{this.settings.schema}';")

        return connObj

    def release_connection(self) -> None:
        self.__refCount -= 1
        if self.__refCount == 0:
            self.__dbConnection.close()
            self.__dbConnection = None
            this.tls.connection = None

    def __enter__(self) -> Connection:
        return self.get_connection()

    def __exit__(self, type: Optional[Type[BaseException]], value: Optional[BaseException], traceback: Optional[TracebackType]) -> Optional[bool]:
        self.release_connection()
        return None


class TransactionWrapper(ScopedConnection):
    """
    Manages transactions
    """
    __slots__ = ('__conWrapper', '__connection', '__transCount')

    def __init__(self, conWrapper: ConnectionWrapper) -> None:
        self.__conWrapper = conWrapper
        self.__connection = None
        self.__transCount = 0

    def __enter__(self) -> Connection:
        self.__transCount += 1
        if self.__transCount == 1:
            self.__connection = self.__conWrapper.get_connection()
            self.__connection.begin()
        return self.__connection

    def __exit__(self,
                 type: Optional[Type[BaseException]],
                 value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Optional[bool]:

        self.__transCount -= 1
        if (self.__transCount == 0):
            if value is not None:
                self.__connection.rollback()
            else:
                self.__connection.commit()
            self.__connection = None
            self.__conWrapper.release_connection()
            this.tls.transactions = None

        return None


def initialize_db(settings: DatabaseSettings = DatabaseSettings()):
    """
    Initializes a database
    """
    this.settings = NativeDBSettings.from_settings(settings)
    this.db = sn.Database(this.settings.path, False, this.settings.options)


def connect() -> ScopedConnection:
    """
    Returns a contextual wrapper around a connection, which is associated 
    to the current thread.

    If the same thread calls multiple times this function, the life time 
    of the underlying connection will be governed by the duration of the 
    first call.

    """
    if this.settings is None or this.db is None:
        raise RuntimeError("Initialize database first by calling `initialize_db`")

    current = getattr(this.tls, 'connection', None)
    if current is None:
        this.tls.connection = ConnectionWrapper()
    return this.tls.connection


def transaction() -> ScopedConnection:
    """
    Returns a contextual wrapper over a connection within a transaction, following 
    the same semantics as the connection objects returned by `connect`.

    Since it is not possible to have inner transactions, if the same thread calls 
    multiple times this method, the transaction will be fully committed when the 
    first transaction goes out of scope.

    Transactions will be committed unless an exception is raised within scoped
    block.
    """
    if this.settings is None:
        raise RuntimeError("Initialize database first by calling `initialize_db`")

    # check if tls is initialized for this thread
    current = getattr(this.tls, 'transaction', None)
    if current is None:
        # set it
        this.tls.transaction = TransactionWrapper(connect())
    # return the current instance
    return this.tls.transaction

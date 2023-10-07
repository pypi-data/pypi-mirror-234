from __future__ import annotations
from dataclasses import dataclass
import functools
from typing import Callable, Dict, Union

import shapelets_native as sn

import uuid 
import datetime 
import decimal 

from .core import Database, Optional, make_query, construct_sql_from_query, construct_query_from_lambda_args, add_column_to_sql, rewrite_query
from . import prototypes

_IntegerTypeCodes = set([
    'TINYINT', 'SMALLINT', 'INTEGER', 'BIGINT', 'HUGEINT', 
    'UTINYINT', 'USMALLINT', 'UINTEGER', 'UBIGINT'
])

_StringTypeCodes = set(['VARCHAR', 'TEXT'])

_FloatTypeCodes = set(['REAL', 'FLOAT', 'DOUBLE'])

def _colDescriptor(colType):
    if colType in _FloatTypeCodes:
        return float
    elif colType in _IntegerTypeCodes:
        return int 
    elif colType in _StringTypeCodes:
        return str 
    elif colType == 'UUID':
        return uuid.UUID
    elif 'TIMESTAMP' in colType:
        return datetime.datetime
    elif colType == 'TIME':
        return datetime.time
    elif colType == 'INTERVAL':
        return datetime.timedelta
    elif 'DECIMAL' in colType:
        return decimal.Decimal
    elif colType == 'DATE':
        return datetime.date
    elif colType == 'BLOB':
        return bytes
    elif colType == 'BOOLEAN':
        return bool
    elif colType == 'MAP(FLOAT, UBIGINT)':
        return float
    raise ValueError(f"Unknown data type {colType}")


@dataclass
class RelationDescriptor:
    alias: str 
    columns: Dict[str, str]

def _map_relation(db: Database,  relation: Union[sn.Relation, RelationDescriptor]) -> type:
    if isinstance(relation, sn.Relation):
        descriptor = RelationDescriptor(relation.alias, relation.dtypes)
    elif isinstance(relation, RelationDescriptor):
        descriptor = relation 
    else:
        raise ValueError("Expected a native relation or a descriptor")
    
    metadata = { '_table_': descriptor.alias }
    for cname, value in descriptor.columns.items():
        metadata[cname] = Optional(_colDescriptor(value[1]))

    tblObj = type(descriptor.alias, (db.Entity,), metadata)
    db.generate_mapping()   
    return tblObj 


def relation_to_python() -> Callable[[sn.Relation], type]:
    db = Database()
    db.bind(provider='native')
    return functools.partial(_map_relation, db)

__all__ = [
    'RelationDescriptor', 'relation_mapper', 'make_query', 
    'construct_sql_from_query', 'prototypes', 'construct_query_from_lambda_args', 'add_column_to_sql','rewrite_query'
]

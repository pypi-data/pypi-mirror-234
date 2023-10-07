from __future__ import annotations
from abc import abstractmethod
import re

from typing import Dict, Optional, Union, List, Tuple, Any
from typing_extensions import Literal


from pydantic import BaseModel 

class ColumnMeta(BaseModel):
    dtype_code: str 
    sql_type: Optional[str] = None 
    
RelationKind = Literal['csv', 'parquet', 'in_memory', 'table', 'transient']    
    
class RelationSource(BaseModel):
    kind: RelationKind     
    parameters: Optional[Any] = None 
    
    
class RelationMeta(BaseModel):
    alias: str 
    columns: Dict[str, ColumnMeta]
    source: RelationSource
    
class IDataService:
    
    @abstractmethod
    def release(self, relation_alias: str) -> None:
        pass 
    
    @abstractmethod
    def distinct(self, relation_alias: str) -> RelationMeta:
        pass 

    @abstractmethod
    def limit(self, relation_alias: str, n: int, offset: Optional[int] = None) -> RelationMeta:
        pass 
    
    @abstractmethod
    def order(self, relation_alias: str, cols: Union[str, List[str]], order: Optional[Union[bool, List[bool]]] = None) -> RelationMeta:
        pass 
    
    @abstractmethod
    def cross_product(self, first_rel: str, second_rel: str) -> RelationMeta:
        pass 

    @abstractmethod
    def intersect(self, first_rel: str, second_rel: str) -> RelationMeta:
        pass 
    
    @abstractmethod
    def minus(self, first_rel: str, second_rel: str) -> RelationMeta:
        pass 
    
    @abstractmethod
    def union(self, first_rel: str, second_rel: str) -> RelationMeta:
        pass 
    
    @abstractmethod
    def count(self, relation_alias: str) -> int:
        pass  
    
    @abstractmethod
    def columns(self, relation_alias: str) -> Dict[str, ColumnMeta]:
        pass 
    
    @abstractmethod
    def drop_columns_by_position(self, relation_alias: str, positions: List[int]) -> RelationRef:
        pass 
    
    @abstractmethod
    def drop_columns_by_name(self, relation_alias: str, names: List[str]) -> RelationRef:
        pass 
    
    @abstractmethod
    def drop_columns_by_regex(self, relation_alias: str, pattern: str, full_match: bool, flags: int) -> RelationRef:
        pass 
    
    @abstractmethod
    def select_columns_by_position(self, relation_alias: str, positions: List[int]) -> RelationRef:
        pass 
    
    @abstractmethod
    def select_columns_by_name(self, relation_alias: str, names: List[str]) -> RelationRef:
        pass 
    
    @abstractmethod
    def select_columns_by_regex(self, relation_alias: str, pattern: str, full_match: bool, flags: int) -> RelationRef:
        pass     
    
    @abstractmethod
    def rename_columns(self, relation_alias: str, cols: Union[Tuple[Union[str,int], str], List[Tuple[Union[str, int], str]]]) -> RelationRef:
        pass

    @abstractmethod
    def sql_transform(self, relation_alias: str, query_relation_alias: str, query: str) -> RelationRef:
        pass
    
    @abstractmethod
    def map(self, sql: str) -> RelationMeta:
        pass 
    
    @abstractmethod
    def materialize(self, relation_alias: str, namespace: str, name: str, override: bool = True, map_columns: Optional[Dict[str, str]] = None) -> RelationMeta:
        pass 

    @abstractmethod
    def open(self, namespace: str, name: str) -> RelationMeta:
        pass 

    @abstractmethod
    def drop(self, namespace: str, name: str) -> bool:
        pass 

    @abstractmethod
    def materialized(self, namespace: str) -> List[str]:
        pass 
    
    @abstractmethod
    def namespaces(self) -> List[str]:
        pass

    @abstractmethod
    def drop_namespace(self, namespace: str) -> None:
        pass    
    

class RelationRef:
    __slots__ = ('__server', '__alias', '__columns')
    
    def __init__(self, server: IDataService, meta: RelationMeta):
        self.__server = server 
        self.__alias = meta.alias
        self.__columns = meta.columns
        
    def __del__(self):
        if self.__alias is not None:
            self.__server.release(self.__alias)
            
        self.__alias = None 
        self.__server = None 
        self.__columns = None 

    @property
    def alias(self) -> str: 
        return self.__alias 

    @property
    def columns(self) -> Dict[str, ColumnMeta]:
        return self.__columns
    
    def __len__(self) -> int:
        return self.__server.count(self.__alias)    

    def distinct(self) -> RelationRef:
        new_rel = self.__server.distinct(self.__alias)        
        return RelationRef(self.__server, new_rel)
    
    def limit(self, n: int, offset: Optional[int] = None) -> RelationRef:
        new_rel = self.__server.limit(self.__alias, n, offset)
        return RelationRef(self.__server, new_rel)
    
    def order(self, cols: Union[str, List[str]], order: Optional[Union[bool, List[bool]]] = None) -> RelationRef:
        new_rel = self.__server.order(self.__alias, cols, order)
        return RelationRef(self.__server, new_rel)
    
    def cross_product(self, other: RelationRef) -> RelationRef:
        new_rel = self.__server.cross_product(self.__alias, other.__alias)
        return RelationRef(self.__server, new_rel)
    
    def intersect(self, other: RelationRef) -> RelationRef:
        new_rel = self.__server.intersect(self.__alias, other.__alias)
        return RelationRef(self.__server, new_rel)

    def minus(self, other: RelationRef) -> RelationRef:
        new_rel = self.__server.minus(self.__alias, other.__alias)
        return RelationRef(self.__server, new_rel)
                
    def union(self, other: RelationRef) -> RelationRef:
        new_rel = self.__server.union(self.__alias, other.__alias)
        return RelationRef(self.__server, new_rel)
    
    def materialize(self, namespace: str, name: str, *, override: bool = True, map_columns: Optional[Dict[str, str]] = None) -> RelationRef:
        new_rel = self.__server.materialize(self.__alias, namespace, name, override, map_columns)
        return RelationRef(self.__server, new_rel)

    def rename_columns(self, cols: Union[Tuple[Union[str,int], str], List[Tuple[Union[str, int], str]]]) -> RelationRef:
        new_rel = self.__server.rename_columns(self.__alias, cols)
        return RelationRef(self.__server, new_rel)

    def drop_columns(self, *, 
                     position: Optional[Union[int, List[int]]] = None, 
                     names: Optional[Union[str, List[str]]] = None, 
                     pattern: Optional[str] = None,
                     full_match: bool = True,
                     flags: int = 0) -> RelationRef:
        if position is not None and isinstance(position, (int, list)):
            lst = [position] if isinstance(position, int) else [int(x) for x in position]
            new_rel = self.__server.drop_columns_by_position(self.__alias, lst) 
        if names is not None and isinstance(names, (str, list)):
            lst = [names] if isinstance(names, str) else [str(x) for x in names]
            new_rel = self.__server.drop_columns_by_name(self.__alias, lst) 
        elif pattern is not None and isinstance(pattern, str):
            new_rel = self.__server.drop_columns_by_regex(self.__alias, pattern, full_match, flags)
        else:
            raise ValueError("One of position, names or matching arguments should be specified")
        
        return RelationRef(self.__server, new_rel)
        
    def select_columns(self, *, 
                       position: Optional[Union[int, List[int]]] = None, 
                       names: Optional[Union[str, List[str]]] = None,
                       pattern: Optional[str] = None,
                       full_match: bool = True, 
                       flags: int = 0) -> RelationRef:
        
        if position is not None and isinstance(position, (int, list)):
            lst = [position] if isinstance(position, int) else [x if isinstance(x, int) else int(x) for x in position]
            new_rel = self.__server.select_columns_by_position(self.__alias, lst) 
        if names is not None and isinstance(names, (str, list)):
            lst = [names] if isinstance(names, str) else [x if isinstance(x, str) else str(x) for x in names]
            new_rel = self.__server.select_columns_by_name(self.__alias, lst) 
        elif pattern is not None and isinstance(pattern, str):
            new_rel = self.__server.select_columns_by_regex(self.__alias, pattern, full_match, flags)
        else:
            raise ValueError("One of position, names or matching arguments should be specified")
        
        return RelationRef(self.__server, new_rel)  
    
    def sql_transform(self, query_rel_alias: str, query: str) -> RelationRef:
        new_rel = self.__server.sql_transform(self.__alias, query_rel_alias, query)
        return RelationRef(self.__server, new_rel)
    
import shapelets_native as sn

class RelationNotFound(Exception):
    def __init__(self, rel_name: str) -> None:
        self.rel_name = rel_name
        super().__init__()
        
        
def _unique_name_generator(prefix: str = "Rel_", suffix: str = ""):
    """
    An endless generator for names.
    """
    num = 0
    while True:
        yield f"{prefix}{num}{suffix}"
        num += 1


_unique_name = _unique_name_generator()
        
        
class PersistentRelation(BaseModel):
    namespace: str 
    name: str
    kind: str 
    parameters: Any 
    description: Optional[str] = None 

class IRelationsStore:
    
    @abstractmethod
    def drop_namespace(self, namespace: str) -> None:
        pass 
    
    @abstractmethod
    def relations_in_namespace(self, namespace: str) -> List[PersistentRelation]:
        pass 
    
    @abstractmethod
    def load(self, namespace: str, name: str) -> Optional[PersistentRelation]:
        pass 

    @abstractmethod
    def drop_relation(self, namespace: str, name: str) -> None:
        pass 
    
    @abstractmethod
    def store(self, namespace: str, name: str, kind: str, parameters: Any, description: Optional[str] = None)  -> None:
        pass 
            
        

class DataService(IDataService):
    
    __slots__ = ('__relations', '__store')
    
    def __init__(self, relationsStore: IRelationsStore) -> None:
        self.__relations: Dict[str, sn.Relation] = dict()
        self.__store = relationsStore
        super().__init__()   
         
    def __columns_meta(self, native: sn.Relation) -> Dict[str, ColumnMeta]:
        
        pass 
    
    def __build_meta(self, native: sn.Relation) -> RelationMeta:
        # don't forget to add it to __relations dic
        # call __columns_meta    
        pass
    
    def __find_by_alias(self, relation_alias: str) -> sn.Relation:
        if relation_alias not in self.__relations:
            raise RelationNotFound(relation_alias)
        return self.__relations[relation_alias]
         
    def release(self, relation_alias: str) -> None:
        if relation_alias in self.__relations:
            del self.__relations[relation_alias]
    
    def distinct(self, relation_alias: str) -> RelationMeta:
        rel = self.__find_by_alias(relation_alias)
        return self.__build_meta(rel.distinct())

    def limit(self, relation_alias: str, n: int, offset: Optional[int] = None) -> RelationMeta:
        rel = self.__find_by_alias(relation_alias)
        return self.__build_meta(rel.limit(n, offset))
    
    def order(self, relation_alias: str, cols: Union[str, List[str]], order_by: Optional[Union[bool, List[bool]]] = None) -> RelationMeta:
        rel = self.__find_by_alias(relation_alias)
        
        if isinstance(cols, str):
            checkedOrder = True
            if order_by is not None:
                if not isinstance(order_by, bool):
                    raise ValueError("Order should be None or boolean.")
                checkedOrder = order_by
                return self.__build_meta(rel.order([cols, order_by]))
        elif isinstance(cols, list):
            checkedOrder = []
            if order_by is None:
                checkedOrder = [True] * len(cols)
            elif isinstance(order_by, list):
                if len(order_by) != len(cols):
                    raise ValueError("Length of order should be the same as the length of cols")
                checkedOrder = order_by
            else:
                raise ValueError("Order should be None or a boolean list")

            pairs = list(zip(cols, checkedOrder))
            return self.__build_meta(rel.order(pairs))
        else:
            raise ValueError("cols parameter should be a string or a list of strings.")        
    
    def cross_product(self, first_rel: str, second_rel: str) -> RelationMeta:
        first = self.__find_by_alias(first_rel)
        second = self.__find_by_alias(second_rel)
        return self.__build_meta(first.cross_product(second))

    def intersect(self, first_rel: str, second_rel: str) -> RelationMeta:
        first = self.__find_by_alias(first_rel)
        second = self.__find_by_alias(second_rel)
        return self.__build_meta(first.intersect(second))
    
    def minus(self, first_rel: str, second_rel: str) -> RelationMeta:
        first = self.__find_by_alias(first_rel)
        second = self.__find_by_alias(second_rel)
        return self.__build_meta(first.minus(second))
    
    def union(self, first_rel: str, second_rel: str) -> RelationMeta:
        first = self.__find_by_alias(first_rel)
        second = self.__find_by_alias(second_rel)
        return self.__build_meta(first.union(second))

    def count(self, relation_alias: str) -> int:
        rel = self.__find_by_alias(relation_alias)
        c = rel.count()
        return 0 if c is None else int(c[0])
    
    def columns(self, relation_alias: str) -> Dict[str, ColumnMeta]:
        rel = self.__find_by_alias(relation_alias)
        return self.__columns_meta(rel)
    
    def drop_columns_by_position(self, relation_alias: str, positions: List[int]) -> RelationRef:
        rel = self.__find_by_alias(relation_alias)
        col_count = len(rel.columns)
        checked = sorted(filter(lambda x: x>=0 and x<col_count, positions), reverse=True)
        if len(checked) == 0:
            raise ValueError(f"List {positions} was empty or yield no valid indices")
        
        keep_cols = rel.columns.copy()
        for p in checked:
            del keep_cols[p]
        
        return self.__build_meta(rel.keep_columns(keep_cols)) # <-- TODO
    
    def drop_columns_by_name(self, relation_alias: str, names: List[str]) -> RelationRef:
        rel = self.__find_by_alias(relation_alias)
        keep_cols = rel.columns.copy()
        for n in names:
            try:
                keep_cols.remove(n)
            except:
                pass # ignore if not found, just move along
        
        return self.__build_meta(rel.keep_columns(keep_cols)) # <-- TODO 
    
    def drop_columns_by_regex(self, relation_alias: str, pattern: str, full_match: bool = True, flags: int = 0) -> RelationRef:
        rel = self.__find_by_alias(relation_alias)
        expr = re.compile(pattern, flags)
        fn = expr.fullmatch if full_match else expr.match
        keep_cols = list(filter(lambda x: fn(x) is None, rel.columns))
        return self.__build_meta(rel.select(keep_cols)) 
    
    def select_columns_by_position(self, relation_alias: str, positions: List[int]) -> RelationRef:
        rel = self.__find_by_alias(relation_alias)
        col_count = len(rel.columns)
        checked = list(filter(lambda x: x>=0 and x<col_count, positions))
        if len(checked) == 0:
            raise ValueError(f"List {positions} was empty or yield no valid indices")
        
        all_cols = rel.columns
        keep_cols = []
        for p in checked:
            keep_cols.append(all_cols[p])
        
        return self.__build_meta(rel.keep_columns(keep_cols)) # <-- TODO        
    
    def select_columns_by_name(self, relation_alias: str, names: List[str]) -> RelationRef:
        rel = self.__find_by_alias(relation_alias)
        all_cols = set(rel.columns)
        checked = [n for n in names if n in all_cols]
        return self.__build_meta(rel.keep_columns(checked)) # <-- TODO 
    
    def select_columns_by_regex(self, relation_alias: str, pattern: str, full_match: bool, flags: int) -> RelationRef:
        rel = self.__find_by_alias(relation_alias)
        expr = re.compile(pattern, flags)
        fn = expr.fullmatch if full_match else expr.match
        keep_cols = list(filter(lambda x: fn(x) is not None, rel.columns))
        return self.__build_meta(rel.keep_columns(keep_cols))  # <-- TODO 
    
    def rename_columns(self, relation_alias: str, cols: Union[Tuple[Union[str,int], str], List[Tuple[Union[str, int], str]]]) -> RelationRef:
        rel = self.__find_by_alias(relation_alias)
        if not isinstance(cols, (tuple, list)):
            raise ValueError("Argument cols should be a tuple or a list of tuples")
        
        existing_cols = rel.columns
        
        col_lst = [cols] if isinstance(cols, tuple) else cols
        renames = dict()
        for entry in col_lst:
            if not isinstance(entry, tuple):
                raise ValueError(f"Expected a tuple, but got a {type(entry)} [{entry}] instead")
            if len(entry) != 2:
                raise ValueError(f"Expected a tuple with two arguments, but received {entry} instead")
            
            pos_or_name = entry[0]
            new_name = entry[1]
            if not isinstance(pos_or_name, (int, str)):
                raise ValueError(f"First argument in tuple {entry} should be an int or a string")
            if not isinstance(new_name, str):
                raise ValueError(f"Second argument in tuple {entry} should be a string")
            if isinstance(pos_or_name, int):
                if pos_or_name <0 or pos_or_name >= len(existing_cols):
                    raise IndexError(f"Invalid position in tuple {entry}")
                renames[existing_cols[pos_or_name]] = new_name
            else:
                if pos_or_name not in existing_cols:
                    raise ValueError(f"Unknown column in tuple {entry}")
                renames[pos_or_name] = new_name                
        
        aliases = []
        for c in existing_cols:
            if c in renames:
                aliases.append(renames[c])
            else:
                aliases.append(c)
                
        return self.__build_meta(rel.rename_columns(existing_cols, aliases))  
    
    def sql_transform(self, relation_alias: str, query_relation_alias: str, query: str) -> RelationRef:
        rel = self.__find_by_alias(relation_alias)
        new_rel = rel.sql_transform(query_relation_alias, query)
        return self.__build_meta(new_rel)
    
    def map(self, sql: str) -> RelationMeta:
        pass 
    
    def materialize(self, 
                    relation_alias: str, 
                    namespace: str, 
                    name: str, 
                    override: bool = True, 
                    map_columns: Optional[Dict[str, str]] = None) -> RelationMeta:
        pass 

    def open(self, namespace: str, name: str) -> RelationMeta:
        pass 

    def drop(self, namespace: str, name: str) -> bool:
        pass 

    def materialized(self, namespace: str) -> List[str]:
        pass 
    
    def namespaces(self) -> List[str]:
        pass
    
    def drop_namespace(self, namespace: str) -> None:
        pass
    
    


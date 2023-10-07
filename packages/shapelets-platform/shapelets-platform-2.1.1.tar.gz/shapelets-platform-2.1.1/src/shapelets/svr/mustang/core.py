from __future__ import print_function, division
# import astpretty
import inspect
import string
import sys
import types
import datetime
import itertools
import ast

from operator import attrgetter
from decimal import Decimal
from random import random

from .sqltranslation import EntityMeta, Entity, Attribute, SQLTranslator
from .sqlbuilding import SQLBuilder, Value
from .decompiling import captureObjectsInFrame, decompile
from .asttranslation import create_extractors, extract_vars_translation

from .exceptions import throw
from .serialization import pickle_ast, unpickle_ast

__all__ = ['Database', 'Optional']


class Database(object):

    def __deepcopy__(self, memo):
        return self  # Database cannot be cloned by deepcopy()

    def __init__(self, *args, **kwargs):
        self.id = 1
        self.entities = {}

        self.Entity = type.__new__(EntityMeta, 'Entity', (Entity,), {})
        self.Entity._database_ = self

        self.provider = self.provider_name = None
        if args or kwargs:
            self._bind(*args, **kwargs)

    def bind(self, *args, **kwargs):
        self._bind(*args, **kwargs)

    def _bind(self, *args, **kwargs):
        provider = 'native'
        self.provider_name = provider
        provider_cls = NativeProvider

        args = []
        kwargs = {}
        self.provider = provider_cls(self, *args, **kwargs)

    def generate_mapping(self):
        entities = list(sorted(self.entities.values(), key=attrgetter('_id_')))

        for entity in entities:
            for attr in entity._new_attrs_:
                attr.columns = [attr.name]
                attr.column = attr.name


def string2ast(s):

    module_node = ast.parse('(%s)' % s)
    if not isinstance(module_node, ast.Module):
        throw(TypeError)
    assert len(module_node.body) == 1
    expr = module_node.body[0]
    assert isinstance(expr, ast.Expr)
    result = expr.value
    return result

def get_alias_in_query(col:str) -> str:
    return col.partition("AS")[-1]

def rewrite_col(id: int, col: str, duplicated: set) -> str:
        
        composed_char = {  '(': '_COMP_', 
                           ')': '_COMP_',
                           '-': '_COMP_',
                           ',': '_COMP_',
                           '*': '_COMP_',
                           '/': '_COMP_',
                           '+': '_COMP_',
                           '-': '_COMP_',
                           '%': '_COMP_' }
        
        new_col = col.translate(str.maketrans(composed_char))

        if 'AS' in new_col:
            new_col = get_alias_in_query(new_col)       
            item = col if new_col==col else new_col
        else:
            if new_col==col:            
                if '.' in col:
                    item = col.split('.')[1]
                    item = item.replace('"','')
                    if item in duplicated:
                        item = col.split('.')[1].replace('"','') + '_' + col.split('.')[0].replace('"','')
                else:
                    item = col
            else:
                new_col = 'column_' + str(id)        
                item = col if new_col==col else new_col

        return item
    
def rewrite_query(sql):
    # This function is due to be removed because we are going to replace this to do it directly in the C engine
    
    select_2 = sql.partition("SELECT DISTINCT ")[2]
    if select_2=='':
        select_2 = sql.partition("SELECT ")[2]
        
    from_str = "\nFROM"
    return_char = from_str in select_2
    cols = select_2.partition(from_str)[0].split(",")
    if return_char is False:
        from_str = " FROM"
        cols = select_2.partition(from_str)[0].split(",")
        if cols==['*']:
            return sql
    
    names = []
    duplicated = set()
    for id, col in enumerate(cols):
        name = rewrite_col(id, col, set())
        if name in names:
            duplicated.add(name)
        names.append(name)
    
    sql_new = "SELECT "
    for id, col in enumerate(cols):
        # if "column" in names[id]:
        #     sql_new = sql_new + col + " AS \"" + rewrite_col(id, col, duplicated) + "\","
        # else:
        sql_new = sql_new + col + ","
    
    sql_new = sql_new[:-1] + select_2.partition(from_str)[1] + select_2.partition(from_str)[2]
        
    return sql_new

def construct_sql_from_query(query, limit=None, offset=None, range=None, aggr_func_name=None, aggr_func_distinct=None, sep=None, alias=True):
    '''
    This method converts a Query object into an SQL query. First of all it translates an AST tree to a pre-SQL format.
    After that, it composes the final SQL query
    '''
    translator = query._translator

    database = query._database
    sql_ast = translator.construct_sql_ast(
        limit, offset, query._distinct, aggr_func_name, aggr_func_distinct, sep)

    sql = database.provider.ast2sql(sql_ast)

    if (query.flr_join is not None):
        if query.flr_join == 'left':
            join_mode = ' LEFT JOIN '
        elif query.flr_join == 'right':
            join_mode = ' RIGHT JOIN '
        elif query.flr_join == 'full':
            join_mode = ' FULL JOIN '
        else:
            join_mode = ' LEFT JOIN '
            
        rest_str0 = sql.partition("FROM ")[0]
        rest_str1 = sql.partition("FROM ")[1]
        rest_str2 = sql.partition("FROM ")[2]
        rest_str = rest_str2.partition(", ")[0]
        rest_str3 = rest_str2.partition(", ")[2]
        rest_str3 = join_mode + rest_str3
        sql = rest_str0 + rest_str1 + rest_str + rest_str3
        sql = sql.replace("WHERE", "ON")

    sql = rewrite_query(sql) if alias else sql
    return sql


def add_column_to_sql(colname: string, sql: string):
    '''
    This method adds a new column (colname) to an SQL Query (sql)
    '''
    
    rest_str = sql.partition("SELECT ")[2]
    result = sql.find('WHERE')
    
    if (result!=-1):
        sql = "SELECT " + rest_str.partition("WHERE ")[2] + " AS " + colname + "," + rest_str.partition("WHERE ")[0]
    else:
        select_str = rest_str.partition("\nFROM ")[0]
        result = select_str.find('DISTINCT')
        if (result!=-1):
            from_str = rest_str.partition("\nFROM ")[2]
            select_str = select_str.partition("DISTINCT ")[2]
            sql = select_str + " AS " + colname + "\nFROM " + from_str
        else:
            from_str = rest_str.partition("\nFROM ")[2]
            sql = select_str + " AS " + colname + "\nFROM " + from_str
        
    return sql


def make_query(args, frame_depth, left_join=False):

    objInFrame = captureObjectsInFrame(args[0], frame_depth=frame_depth + 1 if frame_depth is not None else None)

    gen = args[0]

    if isinstance(gen, types.GeneratorType):
        astTree = decompile(gen)
        code_key = id(gen.gi_frame.f_code)
    elif isinstance(gen, str):
        astTree = string2ast(gen)
        if not isinstance(astTree.tree, ast.GeneratorExp):
            throw(TypeError, 'Source code should represent generator. Got: %s' % gen)
        code_key = gen
    else:
        assert False

    return Query(code_key, astTree.tree, objInFrame.globals, objInFrame.locals, astTree.cells, left_join)


def get_lambda_args(func):

    if type(func) is types.FunctionType:
        if hasattr(inspect, 'signature'):
            names, argsname, kwname, defaults = [], None, None, []
            for p in inspect.signature(func).parameters.values():
                if p.default is not p.empty:
                    defaults.append(p.default)

                if p.kind == p.POSITIONAL_OR_KEYWORD:
                    names.append(p.name)
                elif p.kind == p.VAR_POSITIONAL:
                    argsname = p.name
                elif p.kind == p.VAR_KEYWORD:
                    kwname = p.name
                elif p.kind == p.POSITIONAL_ONLY:
                    throw(TypeError, 'Positional-only arguments like %s are not supported' % p.name)
                elif p.kind == p.KEYWORD_ONLY:
                    throw(TypeError, 'Keyword-only arguments like %s are not supported' % p.name)
                else:
                    assert False
        else:
            names, argsname, kwname, defaults = inspect.getargspec(func)
    elif isinstance(func, ast.Lambda):
        argsname = func.args.vararg
        kwname = func.args.kwarg
        defaults = func.args.defaults + func.args.kw_defaults
        names = [arg.arg for arg in func.args.args]
    else:
        assert False  # pragma: no cover
    if argsname:
        throw(TypeError, '*%s is not supported' % argsname)
    if kwname:
        throw(TypeError, '**%s is not supported' % kwname)
    if defaults:
        throw(TypeError, 'Defaults are not supported')

    return names


def _query_from_args(entity, func, frame_depth):
    objInFrame = captureObjectsInFrame(func, frame_depth=frame_depth + 2 if frame_depth is not None else None)
    if type(func) is types.FunctionType:
        names = get_lambda_args(func)
        code_key = id(func.__code__)
        astTree = decompile(func)
    elif isinstance(func, str):
        code_key = func
        lambda_ast = string2ast(func)
        if not isinstance(lambda_ast, ast.Lambda):
            throw(TypeError, 'Lambda function is expected. Got: %s' % func)
        names = get_lambda_args(lambda_ast)
    else:
        assert False  # pragma: no cover

    if len(names) != 1:
        throw(TypeError,
              'Lambda query requires exactly one parameter name, like %s.select(lambda %s: ...). '
              'Got: %d parameters' % (entity.__name__, entity.__name__[0].lower(), len(names)))
    name = names[0]

    for_expr = ast.comprehension(
        target=ast.Name(name, ast.Store()), iter=ast.Name('.0', ast.Load()), ifs=[astTree.tree])
    inner_expr = ast.GeneratorExp(elt=ast.Name(name, ast.Load()), generators=[for_expr])

    objInFrame.locals = objInFrame.locals.copy() if objInFrame.locals is not None else {}
    objInFrame.locals['.0'] = entity

    return Query(code_key, inner_expr, objInFrame.globals, objInFrame.locals, astTree.cells)


def construct_query_from_lambda_args(entity, func, frame_depth):
    '''
    This method create a Query object from args (including lambda function, func).
    After that, it constructs an SQL query
    '''
    query = _query_from_args(entity, func, frame_depth=1)
    sql = construct_sql_from_query(query)

    return sql


class NativeValue(Value):
    __slots__ = []

    def __str__(self):
        value = self.value
        if isinstance(value, bool):
            return value and 'true' or 'false'
        return Value.__str__(self)


class NativeSQLBuilder(SQLBuilder):
    dialect = 'PostgreSQL'
    value_class = NativeValue

    def TO_INT(builder, expr):
        return '(', builder(expr), ')'

    def TO_STR(builder, expr):
        return '(', builder(expr), ')'

    def TO_REAL(builder, expr):
        return '(', builder(expr), ')'

    def DATE(builder, expr):
        return '(', builder(expr), ')'


class NativeProvider():
    dialect = 'native'

    sqlbuilder_cls = NativeSQLBuilder
    translator_cls = SQLTranslator

    paramstyle = 'qmark'
    quote_char = '"'
    max_name_len = 128
    dialect = None

    def __init__(self, *args, **kwargs):
        kwargs["fileName"] = kwargs.get("fileName", ":memory:")
        kwargs["config"] = kwargs.get("config", {})
        kwargs["readOnly"] = kwargs.get("readOnly", False)
        self.in_memory = kwargs["fileName"] == ":memory:"

    def quote_name(self, name):
        quote_char = '"'
        if isinstance(name, str):
            name = name.replace(quote_char, quote_char + quote_char)
            return quote_char + name + quote_char
        return '.'.join(self.quote_name(item) for item in name)

    def ast2sql(self, ast):
        builder = self.sqlbuilder_cls(self, ast)
        return builder.sql


class Query(object):
    def __init__(self, code_key, tree, globals, locals, cells=None, left_join=False):

        assert isinstance(tree, ast.GeneratorExp)

        # astpretty.pprint(tree, indent=' ', show_offsets=False)
 
        tree, extractors, flr_join = create_extractors(tree, globals, locals, special_functions, const_functions)
        vars, vartypes = extract_vars_translation(code_key, 0, extractors, globals, locals, cells)

        node = tree.generators[0].iter
        varkey = 0, node.src, code_key
        origin = vars[varkey]

        database = origin._database_

        self._filter_num = 0
        self.flr_join = flr_join
        self._code_key = code_key
        self._database = database

        # initialize translator
        pickled_tree = pickle_ast(tree)
        tree_copy = unpickle_ast(pickled_tree)  # tree = deepcopy(tree)

        translator_cls = database.provider.translator_cls  # ty_check_required

        try:
            translator = translator_cls(tree_copy, None, code_key, 0, vartypes.copy(), left_join=left_join, locals=locals, globals=globals)
        except TypeError as e:
            translator = e.translator

        translator.pickled_tree = pickled_tree

        self._translator = translator
        self._next_kwarg_id = 0
        self._distinct = None


special_functions = {itertools.count, random, getattr}
const_functions = {Decimal, datetime.datetime, datetime.date, datetime.time, datetime.timedelta}


class Optional(Attribute):
    pass

import ast
import types
import sys
import re
import itertools

from datetime import date, time, datetime
from copy import deepcopy
from functools import update_wrapper
from collections import defaultdict
from operator import attrgetter
from threading import local as localbase

from .asttranslation import ASTTranslator, ast2src, get_child_nodes
from .ormtypes import numeric_types, SetType, FuncType, normalize, normalize_type, coerce_types
from .python_versions import PY310
from .exceptions import ERDiagramError, throw, reraise
from .identifier import is_ident

from . import prototypes
from .prototypes import *

_operator_mapping = {
    '==': ast.Eq,
    '!=': ast.NotEq,
    '<': ast.Lt,
    '<=': ast.LtE,
    '>': ast.Gt,
    '>=': ast.GtE,
    'is': ast.Is,
    'is not': ast.IsNot,
    'in': ast.In,
    'not in': ast.NotIn
}

entity_id_counter = itertools.count(1)
attr_id_counter = itertools.count(1)


class UsingAnotherTranslator():
    def __init__(self, translator):
        Exception.__init__(self, 'This exception should be catched internally by PonyORM')
        self.translator = translator

def generic():
    pass


def distinct():
    pass


NoneType = type(None)


def check_comparable(left_monad, right_monad, op='=='):
    t1, t2 = left_monad.type, right_monad.type
    if t1 == 'METHOD':
        raise_forgot_parentheses(left_monad)
    if t2 == 'METHOD':
        raise_forgot_parentheses(right_monad)


def sqland(items):
    if not items:
        return []
    if len(items) == 1:
        return items[0]
    result = ['AND']
    for item in items:
        if item[0] == 'AND':
            result.extend(item[1:])
        else:
            result.append(item)
    return result


def sqlor(items):
    if not items:
        return []
    if len(items) == 1:
        return items[0]
    result = ['OR']
    for item in items:
        if item[0] == 'OR':
            result.extend(item[1:])
        else:
            result.append(item)
    return result


def join_tables(alias1, alias2, columns1, columns2):
    assert len(columns1) == len(columns2)
    return sqland([['EQ', ['COLUMN', alias1, c1], ['COLUMN', alias2, c2]] for c1, c2 in zip(columns1, columns2)])


class Local(localbase):
    def __init__(local):
        local.translators = []

    @property
    def translator(self):
        return local.translators[-1]


translator_counter = itertools.count(1)

local = Local()

# function to return key for any value


def get_function_dictionary_key(val):
    for key, value in prototypes.function_dictionary.items():
        if val == value:
            return key

    return "key doesn't exist"


class SQLTranslator(ASTTranslator):
    dialect = None
    row_value_syntax = True

    rowid_support = False

    def default_post(translator, node):
        throw(NotImplementedError)  # pragma: no cover

    def dispatch(translator, node, **kwargs):
        if hasattr(node, 'monad'):
            return  # monad already assigned somehow
        if not getattr(node, 'external', False) or getattr(node, 'constant', False):
            return ASTTranslator.dispatch(translator, node)  # default route

        try:
            func = kwargs['custom_func']
            if (func is None):
                func = ast2src(node)
        except:
            func = ast2src(node)

        translator.call(translator.__class__.dispatch_external, node, custom_func=func)

    def dispatch_external(translator, node, **kwargs):
        varkey = translator.filter_num, node.src, translator.code_key

        try:
            f = kwargs['custom_func']
            custom = get_function_dictionary_key(f)
        except:
            custom = None

        if (custom is not None):
            varkey = translator.filter_num, custom, translator.code_key
            for v in translator.root_translator.vartypes:
                if v[1].find(custom)!=-1:
                    varkey = translator.filter_num, v[1], translator.code_key
                    break           

        # CHANGE KEY TO ADD FN.
        for v in translator.root_translator.vartypes:
            if v[1].find(node.src)!=-1:
                varkey = translator.filter_num, v[1], translator.code_key
                break
           
        t = translator.root_translator.vartypes[varkey]

        tt = type(t)

        if t is NoneType:
            monad = ConstMonad.new(None)
        elif tt is FuncType:
            func = t.func

            func = make_aggrfunction(generic)
            monad = FuncGenericMonad(func)
        else:
            value = None
            try:
                expr = node.id
                value = translator.locals[expr]
            except:
                value = translator.globals[expr]
            finally:
                monad = ConstMonad.new(value)   

        node.monad = monad
        monad.node = node
        monad.aggregated = monad.nogroup = False

    def call(translator, method, node, **kwargs):

        try:
            if (ast2src(node) == 'generic'):
                func = kwargs['custom_func']
                monad = method(translator, node, custom_func=func)
            else:
                monad = method(translator, node)

        except Exception:
            exc_class, exc, tb = sys.exc_info()
            try:
                if not exc.args:
                    exc.args = (ast2src(node),)
                else:
                    msg = exc.args[0]
                    if isinstance(msg, str) and '{EXPR}' in msg:
                        msg = msg.replace('{EXPR}', ast2src(node))
                        exc.args = (msg,) + exc.args[1:]
                reraise(exc_class, exc, tb)
            finally:
                del exc, tb
        else:
            if monad is None:
                return
            node.monad = monad
            monad.node = node
            if not hasattr(monad, 'aggregated'):
                if isinstance(monad, QuerySetMonad):
                    monad.aggregated = False
                else:
                    for child in get_child_nodes(node):
                        m = getattr(child, 'monad', None)
                        if m and getattr(m, 'aggregated', False):
                            monad.aggregated = True
                            break
                    else:
                        monad.aggregated = False
            if not hasattr(monad, 'nogroup'):
                for child in get_child_nodes(node):
                    m = getattr(child, 'monad', None)
                    if m and getattr(m, 'nogroup', False):
                        monad.nogroup = True
                        break
                else:
                    monad.nogroup = False
            if monad.aggregated:
                try:
                    if checkAggregatedFunctionProtoype(monad.node.func.id):
                        translator.aggregated = True        
                except:
                    pass
                
            return monad

    def __repr__(translator):
        return '%s<%d>' % (translator.__class__.__name__, translator.id)

    def deepcopy(self):
        result = deepcopy(self)
        result.id = next(translator_counter)
        result.copied_from = self
        return result

    def __init__(translator, tree, parent_translator, code_key=None, filter_num=None, vartypes=None, left_join=False, optimize=None, locals=locals, globals=globals):
        ASTTranslator.__init__(translator, tree)
        translator.id = next(translator_counter)
        local.translators.append(translator)
        try:
            translator.init(tree, parent_translator, code_key, filter_num, vartypes, left_join, optimize, locals, globals)
        finally:
            assert local.translators
            local.translators.pop()

    def init(translator, tree, parent_translator, code_key=None, filter_num=None, vartypes=None, left_join=False, optimize=None, locals=None, globals=None):

        translator.parent = parent_translator
        translator.locals = locals
        translator.globals = globals

        if parent_translator is None:

            translator.root_translator = translator
            translator.database = None
            translator.sqlquery = SqlQuery(translator, left_join=left_join)
            assert code_key is not None and filter_num is not None
            translator.code_key = code_key
            translator.filter_num = filter_num
        else:

            translator.root_translator = parent_translator.root_translator
            translator.database = parent_translator.database
            translator.sqlquery = SqlQuery(translator, parent_translator.sqlquery, left_join=left_join)
            assert code_key is None and filter_num is None
            translator.code_key = parent_translator.code_key
            translator.filter_num = parent_translator.filter_num

        translator.vartypes = vartypes
        translator.namespace_stack = [{}] if not parent_translator else [parent_translator.namespace.copy()]

        translator.left_join = left_join
        translator.optimize = optimize
        translator.distinct = False
        translator.conditions = translator.sqlquery.conditions

        translator.order = []
        translator.limit = translator.offset = None

        translator.aggregated = False if not optimize else True

        for i, generator in enumerate(tree.generators):
            target = generator.target

            if isinstance(target, ast.Tuple):
                ass_names = tuple(target.elts)
            elif isinstance(target, ast.Name):
                ass_names = (target,)

            names = tuple(ass_name.id for ass_name in ass_names)
            name = names[0] if len(names) == 1 else None

            database = entity = None

            node = generator.iter
            monad = getattr(node, 'monad', None)

            if monad:  # Lambda was encountered inside generator
                entity = monad.type.item_type
                translator.namespace[name] = ObjectIterMonad(tableref, entity)
            elif node.external:

                varkey = translator.filter_num, node.src, translator.code_key
                
                iterable = translator.root_translator.vartypes[varkey]
                if isinstance(iterable, SetType):
                    entity = iterable.item_type
                    if i > 0:
                        translator.distinct = True
                    tableref = TableRef(translator.sqlquery, name, entity)
                    translator.sqlquery.tablerefs[name] = tableref
                    tableref.make_join()
                    translator.namespace[name] = node.monad = ObjectIterMonad(tableref, entity)

            else:

                translator.dispatch(node)
                monad = node.monad

                attr_names = []
                while monad.parent is not None:
                    attr_names.append(monad.attr.name)
                    monad = monad.parent
                attr_names.reverse()

                name_path = monad.tableref.alias  # or name_path, it is the same

                parent_tableref = monad.tableref
                parent_entity = parent_tableref.entity

                last_index = len(attr_names) - 1

                for j, attrname in enumerate(attr_names):
                    attr = parent_entity._adict_.get(attrname)
                    entity = attr.py_type

                    if j == last_index:
                        name_path = name
                    else:
                        name_path += '-' + attr.name
                    tableref = translator.sqlquery.add_tableref(name_path, parent_tableref, attr)
                    tableref.make_join(pk_only=True)
                    if j == last_index:
                        translator.namespace[name] = ObjectIterMonad(tableref, tableref.entity)

                    parent_tableref = tableref
                    parent_entity = entity

            if database is None:
                assert entity is not None
                database = entity._database_

            if translator.database is None:
                translator.database = database

            for if_ in generator.ifs:
                translator.dispatch(if_)
                if if_.monad.type is not bool:
                    if (monad is not None):
                        if_.monad = if_.monad.nonzero()
                cond_monads = if_.monad.operands if isinstance(if_.monad, AndMonad) else [if_.monad]
                for m in cond_monads:
                    if not getattr(m, 'aggregated', False):
                        translator.conditions.extend(m.getsql())

        translator.dispatch(tree.elt)

        monad = tree.elt.monad

        translator.expr_monads = monad.items if isinstance(monad, ListMonad) else [monad]
        translator.groupby_monads = None
        expr_type = monad.type
        if isinstance(expr_type, SetType):
            expr_type = expr_type.item_type
        if isinstance(expr_type, EntityMeta):
            entity = expr_type
            translator.expr_type = entity

            if isinstance(monad, ObjectMixin):
                tableref = monad.tableref

            if translator.aggregated:
                translator.groupby_monads = [monad]
            else:
                translator.distinct |= monad.requires_distinct()
            translator.tableref = tableref
            pk_only = parent_translator is not None or translator.aggregated
            alias, pk_columns = tableref.make_join(pk_only=pk_only)
            translator.alias = alias
            translator.expr_columns = [['COLUMN', alias, column] for column in pk_columns]
            translator.row_layout = None
            translator.col_names = [attr.name for attr in entity._attrs_]
        else:
            translator.alias = None
            expr_monads = translator.expr_monads
            if len(expr_monads) > 1:
                translator.expr_type = tuple(m.type for m in expr_monads)  # ?????
                expr_columns = []
                for m in expr_monads:
                    sql_col = m.getsql()
                    if sql_col:
                        expr_columns.extend(sql_col)
                    else:
                        type = m.type
                        if isinstance(type, EntityMeta):
                            entity = type
                            if isinstance(m, ObjectMixin):
                                tableref = m.tableref

                            if translator.aggregated:
                                translator.groupby_monads = [m]
                            else:
                                translator.distinct |= m.requires_distinct()

                            pk_only = parent_translator is not None or translator.aggregated
                            alias, pk_columns = tableref.make_join(pk_only=pk_only)
                            translator.alias = alias
                            
                            if pk_columns:
                                expr_columns.extend([['COLUMN', alias, column] for column in pk_columns])
                            else:
                                pk_columns = [attr.name for attr in entity._attrs_]
                                expr_columns.extend([['COLUMN', alias, column] for column in pk_columns])
                                
                        
                translator.expr_columns = expr_columns
            else:
                translator.expr_type = monad.type
                translator.expr_columns = monad.getsql()
            if translator.aggregated:
                translator.groupby_monads = [m for m in expr_monads if not m.aggregated and not m.nogroup]
            else:
                expr_set = set()
                for m in expr_monads:
                    if isinstance(m, ObjectIterMonad):
                        expr_set.add(m.tableref.name_path)
                    elif isinstance(m, AttrMonad) and isinstance(m.parent, ObjectIterMonad):
                        expr_set.add((m.parent.tableref.name_path, m.attr))
                for tr in translator.sqlquery.tablerefs.values():
                    if tr.entity is None:
                        continue

                    if tr.name_path in expr_set:
                        continue
                    if any((tr.name_path, attr) not in expr_set for attr in ()):
                        translator.distinct = True
                        break
            row_layout = []
            offset = 0

            for m in expr_monads:
                expr_type = m.type
                if isinstance(expr_type, SetType):
                    expr_type = expr_type.item_type
                if isinstance(expr_type, EntityMeta):
                    next_offset = offset
                    row_layout.append(ast2src(m.node))
                    offset = next_offset
                else:
                    row_layout.append(ast2src(m.node))
                    offset += 1
            translator.row_layout = row_layout

            translator.col_names = [src for src in translator.row_layout]
        if translator.aggregated:
            translator.distinct = False

    @property
    def namespace(translator):
        return translator.namespace_stack[-1]

    def construct_subquery_ast(translator, limit=None, offset=None, aliases=None, star=None,
                               distinct=None, is_not_null_checks=False):
        subquery_ast = translator.construct_sql_ast(
            limit, offset, distinct, is_not_null_checks=is_not_null_checks)
        assert len(subquery_ast) >= 3 and subquery_ast[0] == 'SELECT'

        select_ast = subquery_ast[1][:]

        from_ast = subquery_ast[2][:]
        assert from_ast[0] in ('FROM', 'LEFT_JOIN')

        if len(subquery_ast) == 3:
            where_ast = ['WHERE']
            other_ast = []
        elif subquery_ast[3][0] != 'WHERE':
            where_ast = ['WHERE']
            other_ast = subquery_ast[3:]
        else:
            where_ast = subquery_ast[3][:]
            other_ast = subquery_ast[4:]

        if len(from_ast[1]) == 4:
            outer_conditions = from_ast[1][-1]
            from_ast[1] = from_ast[1][:-1]
            if outer_conditions[0] == 'AND':
                where_ast[1:1] = outer_conditions[1:]
            else:
                where_ast.insert(1, outer_conditions)

        return ['SELECT', select_ast, from_ast, where_ast] + other_ast

    def construct_sql_ast(translator, limit=None, offset=None, distinct=None,
                          aggr_func_name=None, aggr_func_distinct=None, sep=None,
                          is_not_null_checks=False):

        if distinct is None:
            if not translator.order:
                distinct = translator.distinct

        def ast_transformer(ast): return ast
        sql_ast = ['SELECT']

        select_ast = ['DISTINCT' if distinct else 'ALL'] + translator.expr_columns
        if aggr_func_name:
            expr_type = translator.expr_type

            generic_funcion = aggr_func_name.startswith('GENERIC_')
            if (generic_funcion):
                x = aggr_func_name.split("_")
                aggr_func_name = x[0]

            assert len(translator.expr_columns) == 1
            aggr_ast = None
            if translator.groupby_monads or (
                    aggr_func_name == 'COUNT' and distinct and
                    isinstance(translator.expr_type, EntityMeta) and
                    len(translator.expr_columns) > 1):
                outer_alias = 't'
                if aggr_func_name == 'COUNT' and not aggr_func_distinct:
                    outer_aggr_ast = ['COUNT', None]
                else:
                    assert len(translator.expr_columns) == 1
                    expr_ast = translator.expr_columns[0]
                    if expr_ast[0] == 'COLUMN':
                        outer_alias, column_name = expr_ast[1:]
                        outer_aggr_ast = [aggr_func_name, aggr_func_distinct, ['COLUMN', outer_alias, column_name]]

                    else:
                        select_ast = ['DISTINCT' if distinct else 'ALL'] + [['AS', expr_ast, 'expr']]
                        outer_aggr_ast = [aggr_func_name, aggr_func_distinct, ['COLUMN', 't', 'expr']]

                def ast_transformer(ast):
                    return ['SELECT', ['AGGREGATES', outer_aggr_ast],
                            ['FROM', [outer_alias, 'SELECT', ast[1:]]]]
            else:
                if aggr_func_name == 'COUNT':
                    if isinstance(expr_type, (tuple, EntityMeta)) and not distinct and not aggr_func_distinct:
                        aggr_ast = ['COUNT', aggr_func_distinct]
                    else:
                        aggr_ast = ['COUNT', True if aggr_func_distinct is None else aggr_func_distinct,
                                    translator.expr_columns[0]]
                else:
                    aggr_ast = [aggr_func_name, aggr_func_distinct, translator.expr_columns[0]]

            if aggr_ast:
                select_ast = ['AGGREGATES', aggr_ast]
        elif isinstance(translator.expr_type, EntityMeta) and not translator.parent \
                and not translator.aggregated and not translator.optimize:
            select_ast = translator.expr_type._construct_select_clause_(
                translator.alias, distinct, translator.tableref.used_attrs)
        sql_ast.append(select_ast)
        sql_ast.append(translator.sqlquery.from_ast)

        conditions = translator.conditions[:]

        if conditions:
            sql_ast.append(['WHERE'] + conditions)

        if translator.groupby_monads:
            group_by = ['GROUP_BY']
            
            for m in translator.groupby_monads:
                only_agg = False
                if isinstance(m.node,ast.Call):
                    if (m.node.func.id in prototypes.aggregatedFunctionList):
                        only_agg = True
                    else:
                        sql = m.getsql()
                        list_agg = flatList(sql)
                        only_agg = any(list_agg)
                    
                if (not only_agg):
                    group_by.extend(m.getsql())
            
            if (group_by==['GROUP_BY']):
                group_by = None
            else:    
                sql_ast.append(group_by)
        else:
            group_by = None

        if translator.order and not aggr_func_name:
            sql_ast.append(['ORDER_BY'] + translator.order)

        sql_ast = ast_transformer(sql_ast)
        return sql_ast

    def preGeneratorExp(translator, node):
        translator_cls = translator.__class__
        try:
            subtranslator = translator_cls(node, translator)
        except UsingAnotherTranslator(translator):
            assert False
        return QuerySetMonad(subtranslator)

    def postExpr(translator, node):
        return node.value.monad

    def preCompare(translator, node):
        monads = []
        ops = zip(node.ops, node.comparators)
        left = node.left
        translator.dispatch(left)
        # op: '<' | '>' | '=' | '>=' | '<=' | '<>' | '!=' | '=='
        #         | 'in' | 'not in' | 'is' | 'is not'
        for op_node, right in ops:
            for op, cls in _operator_mapping.items():
                if isinstance(op_node, cls):
                    break
            else:
                assert False, str(op_node)
            translator.dispatch(right)
            if op.endswith('in'):
                monad = right.monad.contains(left.monad, op == 'not in')
            else:
                monad = left.monad.cmp(op, right.monad)
            if not hasattr(monad, 'aggregated'):
                monad.aggregated = getattr(left.monad, 'aggregated', False) or getattr(right.monad, 'aggregated', False)
            if not hasattr(monad, 'nogroup'):
                monad.nogroup = getattr(left.monad, 'nogroup', False) or getattr(right.monad, 'nogroup', False)
            if monad.aggregated and monad.nogroup:
                throw(NotImplementedError,
                      'Too complex aggregation, expressions cannot be combined: {EXPR}')
            monads.append(monad)
            left = right
        if len(monads) == 1:
            return monads[0]
        return AndMonad(monads)

    def postConstant(translator, node):
        value = node.value
        if type(value) is frozenset:
            value = tuple(sorted(value))
        return ConstMonad.new(value)

    def postNameConstant(translator, node):  # Python <= 3.7
        return ConstMonad.new(node.value)

    def postNum(translator, node):  # Python <= 3.7
        return ConstMonad.new(node.n)

    def postStr(translator, node):  # Python <= 3.7
        return ConstMonad.new(node.s)

    def postBytes(translator, node):  # Python <= 3.7
        return ConstMonad.new(node.s)

    def postList(translator, node):
        return ListMonad([item.monad for item in node.elts])

    def postTuple(translator, node):
        return ListMonad([item.monad for item in node.elts])

    def postName(translator, node):
        monad = translator.resolve_name(node.id)
        assert monad is not None
        return monad

    def resolve_name(translator, name):
        monad = translator.namespace[name]
        return monad

    def postAdd(translator, node):
        return node.left.monad + node.right.monad

    def postSub(translator, node):
        return node.left.monad - node.right.monad

    def postMult(translator, node):
        return node.left.monad * node.right.monad

    def postMatMult(translator, node):
        throw(NotImplementedError)

    def postDiv(translator, node):
        return node.left.monad / node.right.monad

    def postFloorDiv(translator, node):
        return node.left.monad // node.right.monad

    def postMod(translator, node):
        return node.left.monad % node.right.monad

    def postLShift(translator, node):
        throw(NotImplementedError)

    def postRShift(translator, node):
        throw(NotImplementedError)

    def postPow(translator, node):
        return node.left.monad ** node.right.monad

    def postUSub(translator, node):
        return -node.operand.monad

    def postAttribute(translator, node):
        return node.value.monad.getattr(node.attr)

    def postAnd(translator, node):
        return AndMonad([expr.monad for expr in node.values])

    def postOr(translator, node):
        return OrMonad([expr.monad for expr in node.values])

    def postBitOr(translator, node):
        return node.left.monad | node.right.monad

    def postBitAnd(translator, node):
        return node.left.monad & node.right.monad

    def postBitXor(translator, node):
        return node.left.monad ^ node.right.monad

    def postNot(translator, node):
        return node.operand.monad.negate()

    def preCall(translator, node, **kwargs):

        func_node = node.func
        if isinstance(func_node, ast.Call):
            if isinstance(func_node.func, ast.Name) and func_node.func.id == 'getattr':
                return

        if len(node.args) > 1:
            return
        if not node.args:
            return
        arg = node.args[0]
        if isinstance(arg, ast.GeneratorExp):
            id = func_node.id
            if (id in prototypes.allowedFunctionList):
                dbname = prototypes.function_dictionary[id]
                func = dbname

                func_node.id = 'generic'
                func_node.src = 'generic'
            else:
                func = None

            translator.dispatch(func_node, custom_func=func)
            func_monad = func_node.monad
            id = func_node.id
            translator.dispatch(arg)
            query_set_monad = arg.monad
            if (id == 'generic'):
                return func_monad(query_set_monad, custom_func=func)
            else:
                return func_monad(query_set_monad)

        if not isinstance(arg, ast.Lambda):
            return
        lambda_expr = arg
        translator.dispatch(func_node)
        method_monad = func_node.monad

        entity_monad = method_monad.parent

        entity = entity_monad.type.item_type
        method_name = method_monad.attrname

        iter_name = lambda_expr.args.args[0].arg
        cond_expr = lambda_expr.body
        name_ast = ast.Name(entity.__name__, ast.Load())
        name_ast.monad = entity_monad
        for_expr = ast.comprehension(ast.Name(iter_name, ast.Store()), name_ast, [cond_expr], False)
        inner_expr = ast.GeneratorExp(ast.Name(iter_name, ast.Load()), [for_expr])
        translator_cls = translator.__class__
        try:
            subtranslator = translator_cls(inner_expr, translator)
        except UsingAnotherTranslator(translator):
            assert False
        monad = QuerySetMonad(subtranslator)
        if method_name == 'exists':
            monad = monad.nonzero()
        return monad

    def postCall(translator, node):
        args = []
        kwargs = {}
        for arg in node.args:
            args.append(arg.monad)
        for kw in node.keywords:
            kwargs[kw.arg] = kw.value.monad
        func_monad = node.func.monad

        return func_monad(*args, **kwargs)

    def postIndex(translator, node):
        return node.value.monad

    def postFormattedValue(translator, node):
        return node.value.monad


def coerce_monads(m1, m2, for_comparison=False):
    result_type = coerce_types(m1.type, m2.type)
    if result_type in numeric_types and bool in (m1.type, m2.type) and (
            result_type is not bool or not for_comparison):
        translator = m1.translator
        if translator.dialect == 'PostgreSQL':
            if result_type is bool:
                result_type = int
            if m1.type is bool:
                new_m1 = NumericExprMonad(int, ['TO_INT', m1.getsql()[0]], nullable=m1.nullable)
                new_m1.aggregated = m1.aggregated
                m1 = new_m1
            if m2.type is bool:
                new_m2 = NumericExprMonad(int, ['TO_INT', m2.getsql()[0]], nullable=m2.nullable)
                new_m2.aggregated = m2.aggregated
                m2 = new_m2
    return result_type, m1, m2


max_alias_length = 30


class SqlQuery(object):
    def __init__(sqlquery, translator, parent_sqlquery=None, left_join=False):
        sqlquery.translator = translator
        sqlquery.parent_sqlquery = parent_sqlquery
        sqlquery.left_join = left_join
        sqlquery.from_ast = ['LEFT_JOIN' if left_join else 'FROM']
        sqlquery.conditions = []
        sqlquery.outer_conditions = []
        sqlquery.tablerefs = {}
        if parent_sqlquery is None:
            sqlquery.alias_counters = {}
        else:
            sqlquery.alias_counters = parent_sqlquery.alias_counters.copy()

    def make_alias(sqlquery, name):
        name = name[:max_alias_length - 3].lower()
        i = sqlquery.alias_counters.setdefault(name, 0) + 1
        alias = name if i == 1 and name != 't' else '%s-%d' % (name, i)
        sqlquery.alias_counters[name] = i
        return alias


class TableRef(object):
    def __init__(tableref, sqlquery, name, entity):
        tableref.sqlquery = sqlquery
        tableref.alias = sqlquery.make_alias(name)
        tableref.name_path = tableref.alias
        tableref.entity = entity
        tableref.joined = False
        tableref.used_attrs = set()

    def make_join(tableref, pk_only=False):
        entity = tableref.entity
        if not tableref.joined:
            sqlquery = tableref.sqlquery
            sqlquery.from_ast.append([tableref.alias, 'TABLE', entity._table_])

            tableref.joined = True
        return tableref.alias, []


class JoinedTableRef(object):
    def __init__(tableref, sqlquery, name_path, parent_tableref, attr):
        tableref.sqlquery = sqlquery
        tableref.name_path = name_path
        tableref.var_name = name_path if is_ident(name_path) else None
        tableref.alias = None
        tableref.optimized = None
        tableref.parent_tableref = parent_tableref
        tableref.attr = attr
        tableref.entity = attr.py_type
        assert isinstance(tableref.entity, EntityMeta)
        tableref.joined = False
        tableref.used_attrs = set()

    def make_join(tableref, pk_only=False):
        entity = tableref.entity
        if tableref.joined:
            if pk_only or not tableref.optimized:
                return tableref.alias, tableref.pk_columns
        sqlquery = tableref.sqlquery
        attr = tableref.attr

        parent_alias, left_pk_columns = tableref.parent_tableref.make_join(False)

        pk_columns = []

        if not attr.columns:
            # one-to-one relationship with foreign key column on the right side
            reverse = attr.reverse
            assert reverse.columns and not reverse.is_collection
            rentity = reverse.entity
            pk_columns = []

            alias = sqlquery.make_alias(tableref.var_name or rentity.__name__)
            join_cond = join_tables(parent_alias, alias, left_pk_columns, reverse.columns)
        else:
            # one-to-one or many-to-one relationship with foreign key column on the left side
            left_columns = attr.columns

            alias = sqlquery.make_alias(tableref.var_name or entity.__name__)
            join_cond = join_tables(parent_alias, alias, left_columns, pk_columns)

        translator = tableref.sqlquery.translator.root_translator
        if translator.optimize == False:
            pass
        else:
            sqlquery.join_table(parent_alias, alias, entity._table_, join_cond)
        tableref.alias = alias
        tableref.pk_columns = pk_columns
        tableref.optimized = False
        tableref.joined = True
        return tableref.alias, pk_columns


def wrap_monad_method(cls_name, func):
    overrider_name = '%s_%s' % (cls_name, func.__name__)

    def wrapper(monad, *args, **kwargs):

        method = getattr(monad.translator, overrider_name, func)

        if (overrider_name == 'QuerySetMonad_aggregate'):
            func_name = args[0]
            generic_funcion = func_name.startswith('GENERIC_')
            if (generic_funcion):
                x = func_name.split("_")
                func_name = x[1]

            return method(monad, *args, custom_func=func_name)

        if (overrider_name == 'FuncGenericMonad_call'):
            try:
                f = kwargs['custom_func']
                try:
                    custom = prototypes.function_dictionary[f]
                except:
                    custom = f
            except:
                f = monad.node.id
                try:
                    custom = prototypes.function_dictionary[f]
                except:
                    custom = f

            return method(monad, *args, custom_func=custom)

        return method(monad, *args, **kwargs)
    return update_wrapper(wrapper, func)


class MonadMeta(type):
    def __new__(meta, cls_name, bases, cls_dict):
        for name, func in cls_dict.items():
            if not isinstance(func, types.FunctionType):
                continue
            if name in ('__new__', '__init__'):
                continue
            cls_dict[name] = wrap_monad_method(cls_name, func)
        return super(MonadMeta, meta).__new__(meta, cls_name, bases, cls_dict)


class MonadMixin(object, metaclass=MonadMeta):
    pass


class Monad(object, metaclass=MonadMeta):

    def __init__(monad, type, nullable=True):
        monad.node = None
        monad.translator = local.translator
        monad.type = type
        monad.nullable = nullable
        # monad.mixin_init()

    def mixin_init(monad):
        pass

    def to_single_cell_value(monad):
        return monad

    def cmp(monad, op, monad2):
        return CmpMonad(op, monad, monad2)

    def contains(monad, item, not_in=False):
        throw(TypeError)

    def negate(monad):
        return NotMonad(monad)

    def getattr(monad, attrname):
        property_method = getattr(monad, 'attr_' + attrname)
        return property_method()

    def len(monad): throw(TypeError)

    def count(monad, distinct=None):
        distinct = distinct_from_monad(distinct, default=True)
        translator = monad.translator
        if monad.aggregated:
            throw(NotImplementedError, 'Aggregated functions cannot be nested. Got: {EXPR}')
        expr = monad.getsql()

        if monad.type is bool:
            expr = ['CASE', None, [[expr[0], ['VALUE', 1]]], ['VALUE', None]]
            distinct = None
        elif len(expr) == 1:
            expr = expr[0]
        elif translator.dialect == 'PostgreSQL':
            row = ['ROW'] + expr
            expr = ['CASE', None, [[['IS_NULL', row], ['VALUE', None]]], row]
        # elif translator.dialect == 'PostgreSQL':  # another way
        #     alias, pk_columns = monad.tableref.make_join(pk_only=False)
        #     expr = [ 'COLUMN', alias, 'ctid' ]
        elif translator.dialect in ('SQLite', 'Oracle'):
            alias, pk_columns = monad.tableref.make_join(pk_only=False)
            expr = ['COLUMN', alias, 'ROWID']
        # elif translator.row_value_syntax == True:  # doesn't work in MySQL
        #     expr = ['ROW'] + expr
        else:
            throw(NotImplementedError,
                  '%s database provider does not support entities '
                  'with composite primary keys inside aggregate functions. Got: {EXPR}'
                  % translator.dialect)
        result = ExprMonad.new(int, ['COUNT', distinct, expr], nullable=False)

        result.aggregated = True
        return result

    def aggregate(monad, *args):
        
        args_original = args
        
        func_name = args[0]
        args = args[1]
        
        if len(args)>=1:
            p1 = args[0]
            
            if isinstance(p1, NumericConstMonad):
                p1 = p1.value
            
            
        if len(args)>=2:
            p2 = args[1]
            
            if isinstance(p2, NumericConstMonad):
                p2 = p2.value
          
        if len(args)>=3:
            p3 = args[2]
            
            if isinstance(p3, NumericConstMonad):
                p3 = p3.value

        translator = monad.translator
        expr_type = monad.type

        alt_func = None

        generic_funcion = func_name.startswith('GENERIC_')
        if (generic_funcion):
            x = func_name.split("_")
            func_name = x[0]
            alt_func = x[1]

        if func_name in ('SUM', 'GENERIC'):
            if expr_type not in numeric_types:
                if expr_type is str:
                    monad = monad.to_str()
                elif expr_type is datetime:
                    monad = monad.to_datetime()
        else:
            assert False  # pragma: no cover
        expr = monad.getsql()
        if len(expr) == 1:
            expr = expr[0]
        elif translator.row_value_syntax:
            expr = ['ROW'] + expr
        else:
            throw(NotImplementedError,
                  '%s database provider does not support entities '
                  'with composite primary keys inside aggregate functions. Got: {EXPR} '
                  '(you can suggest us how to write SQL for this query)'
                  % translator.dialect)

        if func_name == 'GENERIC':
            if (expr_type is str or expr_type is datetime):
                result_type = str
            else:
                result_type = float
        else:
            result_type = expr_type
        if p1 is None:
            p1 = getattr(monad, 'forced_distinct', False) and func_name in ('SUM', 'GENERIC')

        if (alt_func is not None):
            func_name = func_name + '_' + alt_func

        if (len(args)==1):
            aggr_ast = [func_name, convertExpr(p1)]
        elif (len(args)==2):
            aggr_ast = [func_name, convertExpr(p1), convertExpr(p2)]
        elif (len(args)==3):
            aggr_ast = [func_name, convertExpr(p1), convertExpr(p2), convertExpr(p3)]
        else:
            aggr_ast = []
            aggr_ast.append(func_name)
            d = distinct.node.monad.getsql()
            aggr_ast.append(d)
            aggr_ast.append(expr)

        result = ExprMonad.new(result_type, aggr_ast, nullable=True)
        if (alt_func is not None):
            if (alt_func in prototypes.aggregatedFunctionList or alt_func == 'SUM'):
                result.aggregated = True
            else:
                result.aggregated = False
        elif (func_name in ('SUM', 'MIN', 'MAX')):
            result.aggregated = True

        return result

    def __call__(monad, *args, **kwargs): throw(TypeError)
    def __getitem__(monad, key): throw(TypeError)
    def __add__(monad, monad2): throw(TypeError)
    def __sub__(monad, monad2): throw(TypeError)
    def __mul__(monad, monad2): throw(TypeError)
    def __truediv__(monad, monad2): throw(TypeError)
    def __floordiv__(monad, monad2): throw(TypeError)
    def __pow__(monad, monad2): throw(TypeError)
    def __neg__(monad): throw(TypeError)
    def __or__(monad, monad2): throw(TypeError)
    def __and__(monad, monad2): throw(TypeError)
    def __xor__(monad, monad2): throw(TypeError)
    def abs(monad): throw(TypeError)
    def cast_from_json(monad, type): assert False, monad

    def to_int(monad):
        return NumericExprMonad(int, ['TO_INT', monad.getsql()[0]], nullable=monad.nullable)

    def to_str(monad):
        return StringExprMonad(str, ['TO_STR', monad.getsql()[0]], nullable=monad.nullable)

    def to_datetime(monad):
        return StringExprMonad(str, ['DATE', monad.getsql()[0]], nullable=monad.nullable)

    def to_real(monad):
        return NumericExprMonad(float, ['TO_REAL', monad.getsql()[0]], nullable=monad.nullable)


def convertExpr(expression):

    if (isinstance(expression,int) or isinstance(expression,float) or isinstance(expression,str)):
        expr = expression
    else:
        expr = expression.getsql()
        if len(expr) == 1:
            expr = expr[0]
    
    return expr

def flatList(myList):
    new_lst = []
    for item in myList:
        if isinstance(item, list):
            new_lst.extend(flatList(item))
        else:
            f = isAggregated(item) if isinstance(item, str) else False
            new_lst.append(f)
            # print(item)
            # print(isAggregated(item))
    
    return new_lst

def isAggregated(item):
    if item.startswith('GENERIC_'):
        x = item.split("_")
        res = True if x[1] in prototypes.aggregatedFunctionList else False
        return res
    else:
        return False
        
def distinct_from_monad(distinct, default=None):
    if distinct is None:
        return default

    if isinstance(distinct, NumericConstMonad):
        return distinct.value
    
    return default


typeerror_re_1 = re.compile(r'\(\) takes (no|(?:exactly|at (?:least|most)))(?: (\d+))? arguments \((\d+) given\)')
typeerror_re_2 = re.compile(r'\(\) takes from (\d+) to (\d+) positional arguments but (\d+) were given')


def reraise_improved_typeerror(exc, func_name, orig_func_name):
    if not exc.args:
        throw(exc)
    msg = exc.args[0]
    if PY310:
        dot_index = msg.find('.') + 1
        msg = msg[dot_index:]
    if not msg.startswith(func_name):
        throw(exc)
    msg = msg[len(func_name):]

    match = typeerror_re_1.match(msg)
    if match:
        what, takes, given = match.groups()
        takes, given = int(takes), int(given)
        if takes:
            what = '%s %d' % (what, takes - 1)
        plural = 's' if takes > 2 else ''
        new_msg = '%s() takes %s argument%s (%d given)' % (orig_func_name, what, plural, given - 1)
        exc.args = (new_msg,)
        throw(exc)

    match = typeerror_re_2.match(msg)
    if match:
        start, end, given = match.groups()
        start, end, given = int(start) - 1, int(end) - 1, int(given) - 1
        if not start:
            plural = 's' if end > 1 else ''
            new_msg = '%s() takes at most %d argument%s (%d given)' % (orig_func_name, end, plural, given)
        else:
            new_msg = '%s() takes from %d to %d arguments (%d given)' % (orig_func_name, start, end, given)
        exc.args = (new_msg,)
        throw(exc)

    exc.args = (orig_func_name + msg,)
    throw(exc)


def raise_forgot_parentheses(monad):
    assert monad.type == 'METHOD'
    throw(TypeError, 'You seems to forgot parentheses after %s' % ast2src(monad.node))


class ListMonad(Monad):
    def __init__(monad, items):
        Monad.__init__(monad, tuple(item.type for item in items))
        monad.items = items

    def getsql(monad, sqlquery=None):
        return [['ROW'] + [item.getsql()[0] for item in monad.items]]


def make_numeric_binop(op, sqlop):
    def numeric_binop(monad, monad2):
        if monad2.type == 'METHOD':
            raise_forgot_parentheses(monad2)
        result_type, monad, monad2 = coerce_monads(monad, monad2)

        left_sql = monad.getsql()[0]
        right_sql = monad2.getsql()[0]
        return NumericExprMonad(result_type, [sqlop, left_sql, right_sql])
    numeric_binop.__name__ = sqlop
    return numeric_binop


class NumericMixin(MonadMixin):
    __add__ = make_numeric_binop('+', 'ADD')
    __sub__ = make_numeric_binop('-', 'SUB')
    __mul__ = make_numeric_binop('*', 'MUL')
    __truediv__ = make_numeric_binop('/', 'DIV')
    __floordiv__ = make_numeric_binop('//', 'FLOORDIV')
    __mod__ = make_numeric_binop('%', 'MOD')
    __and__ = make_numeric_binop('&', 'BITAND')
    __or__ = make_numeric_binop('|', 'BITOR')
    __xor__ = make_numeric_binop('^', 'BITXOR')


sql_negation = {'IN': 'NOT_IN', 'EXISTS': 'NOT_EXISTS',
                'LIKE': 'NOT_LIKE', 'BETWEEN': 'NOT_BETWEEN', 'IS_NULL': 'IS_NOT_NULL'}
sql_negation.update((value, key) for key, value in list(sql_negation.items()))


class BoolMonad(Monad):
    def __init__(monad, nullable=True):
        Monad.__init__(monad, bool, nullable=nullable)

    def nonzero(monad):
        return monad


class BoolExprMonad(BoolMonad):
    def __init__(monad, sql, nullable=True):
        BoolMonad.__init__(monad, nullable=nullable)
        monad.sql = sql

    def getsql(monad, sqlquery=None):
        return [monad.sql]

    def negate(monad):
        sql = monad.sql
        sqlop = sql[0]
        negated_op = sql_negation.get(sqlop)
        if negated_op is not None:
            negated_sql = [negated_op] + sql[1:]
        elif negated_op == 'NOT':
            assert len(sql) == 2
            negated_sql = sql[1]
        else:
            return NotMonad(monad)
        return BoolExprMonad(negated_sql, nullable=monad.nullable)


def numeric_attr_factory(name):
    def attr_func(monad):
        sql = [name, monad.getsql()[0]]
        return NumericExprMonad(int, sql, nullable=monad.nullable)
    attr_func.__name__ = name.lower()
    return attr_func


def make_datetime_binop(op, sqlop):
    def datetime_binop(monad, monad2):

        expr_monad_cls = DateExprMonad if monad.type is date else DatetimeExprMonad
        return expr_monad_cls(monad.type, [sqlop, monad.getsql()[0], monad2.getsql()[0]],
                              nullable=monad.nullable or monad2.nullable)
    datetime_binop.__name__ = sqlop
    return datetime_binop


class ExprMonad(Monad):
    @staticmethod
    def new(t, sql, nullable=True):
        if t in numeric_types:
            cls = NumericExprMonad
        elif t is str:
            cls = StringExprMonad
        elif t is date:
            cls = DateExprMonad
        elif t is time:
            cls = TimeExprMonad
        elif t is datetime.datetime:
            cls = DatetimeExprMonad
        elif isinstance(t, EntityMeta):
            cls = ObjectExprMonad
        else:
            throw(NotImplementedError, t)  # pragma: no cover
        return cls(t, sql, nullable=nullable)

    def __new__(cls, *args, **kwargs):
        if cls is ExprMonad:
            assert False, 'Abstract class'  # pragma: no cover
        return Monad.__new__(cls)

    def __init__(monad, type, sql, nullable=True):
        Monad.__init__(monad, type, nullable=nullable)
        monad.sql = sql

    def getsql(monad, sqlquery=None):
        return [monad.sql]


def make_string_binop(op, sqlop):
    def string_binop(monad, monad2):
        left_sql = monad.getsql()
        right_sql = monad2.getsql()
        assert len(left_sql) == len(right_sql) == 1
        return StringExprMonad(monad.type, [sqlop, left_sql[0], right_sql[0]],
                               nullable=monad.nullable or monad2.nullable)
    string_binop.__name__ = sqlop
    return string_binop


def make_string_func(sqlop):
    def func(monad):
        sql = monad.getsql()
        assert len(sql) == 1
        return StringExprMonad(monad.type, [sqlop, sql[0]], nullable=monad.nullable)
    func.__name__ = sqlop
    return func


class ObjectMixin(MonadMixin):

    def getattr(monad, attrname):

        entity = monad.type
        attr = entity._adict_.get(attrname)

        if hasattr(monad, 'tableref'):
            monad.tableref.used_attrs.add(attr)
        
        if (attr is None):
            raise ValueError(
                f"Attribute {monad.node.src}.{attrname} not found"
            )
        
        return AttrMonad.new(monad, attr)    

    def requires_distinct(monad, joined=False):
        return monad.parent.requires_distinct(joined)  # parent ???


class ObjectIterMonad(ObjectMixin, Monad):
    def __init__(monad, tableref, entity):
        Monad.__init__(monad, entity)
        monad.tableref = tableref

    def getsql(monad, sqlquery=None):
        entity = monad.type
        alias, pk_columns = monad.tableref.make_join(pk_only=True)
        return [['COLUMN', alias, column] for column in pk_columns]

    def requires_distinct(monad, joined=False):
        return monad.tableref.name_path != monad.translator.tree.generators[-1].target.id


class AttrMonad(Monad):
    @staticmethod
    def new(parent, attr, *args, **kwargs):
        t = normalize_type(attr.py_type)
        if t in numeric_types:
            cls = NumericAttrMonad
        elif t is str:
            cls = StringAttrMonad
        elif t is date:
            cls = DateAttrMonad
        elif t is datetime:
            cls = DatetimeAttrMonad
        else:
            throw(NotImplementedError, t)  # pragma: no cover
        return cls(parent, attr, *args, **kwargs)

    def __new__(cls, *args):
        if cls is AttrMonad:
            assert False, 'Abstract class'  # pragma: no cover
        return Monad.__new__(cls)

    def __init__(monad, parent, attr):
        assert monad.__class__ is not AttrMonad
        attr_type = normalize_type(attr.py_type)
        Monad.__init__(monad, attr_type)
        monad.parent = parent
        monad.attr = attr
        monad.nullable = attr.nullable

    def getsql(monad, sqlquery=None):
        parent = monad.parent
        attr = monad.attr

        alias, parent_columns = parent.tableref.make_join(False)
        columns = attr.columns

        return [['COLUMN', alias, column] for column in columns]


class StringAttrMonad(AttrMonad):
    pass


class NumericAttrMonad(NumericMixin, AttrMonad):
    pass


class DateAttrMonad(AttrMonad):
    pass


class DatetimeAttrMonad(AttrMonad):
    pass


class ExprMonad(Monad):
    @staticmethod
    def new(t, sql, nullable=True):
        if t in numeric_types:
            cls = NumericExprMonad
        elif t is str:
            cls = StringExprMonad
        elif t is date:
            cls = DateExprMonad
        elif t is time:
            cls = TimeExprMonad
        elif t is datetime:
            cls = DatetimeExprMonad
        elif isinstance(t, EntityMeta):
            cls = ObjectExprMonad
        else:
            throw(NotImplementedError, t)  # pragma: no cover
        return cls(t, sql, nullable=nullable)

    def __new__(cls, *args, **kwargs):
        if cls is ExprMonad:
            assert False, 'Abstract class'  # pragma: no cover
        return Monad.__new__(cls)

    def __init__(monad, type, sql, nullable=True):
        Monad.__init__(monad, type, nullable=nullable)
        monad.sql = sql

    def getsql(monad, sqlquery=None):
        return [monad.sql]


class ObjectExprMonad(ObjectMixin, ExprMonad):
    def getsql(monad, sqlquery=None):
        return monad.sql


class StringExprMonad(ExprMonad):
    pass


class NumericExprMonad(NumericMixin, ExprMonad):
    pass


class DateExprMonad(ExprMonad):
    pass


class TimeExprMonad(ExprMonad):
    pass


class DatetimeExprMonad(ExprMonad):
    pass


class ConstMonad(Monad):
    @staticmethod
    def new(value):
        value_type, value = normalize(value)
        if isinstance(value_type, tuple):
            return ListMonad([ConstMonad.new(item) for item in value])
        elif value_type in numeric_types:
            cls = NumericConstMonad
        elif value_type is str:
            cls = StringConstMonad
        elif value_type is date:
            cls = DateConstMonad
        elif value_type is time:
            cls = TimeConstMonad
        elif value_type is datetime:
            cls = DatetimeConstMonad
        else:
            throw(NotImplementedError, value_type)  # pragma: no cover
        result = cls(value)
        result.aggregated = False
        return result

    def __new__(cls, *args):
        if cls is ConstMonad:
            assert False, 'Abstract class'  # pragma: no cover
        return Monad.__new__(cls)

    def __init__(monad, value):
        value_type, value = normalize(value)
        Monad.__init__(monad, value_type, nullable=value_type is NoneType)
        monad.value = value

    def getsql(monad, sqlquery=None):
        return [['VALUE', monad.value]]


class StringConstMonad(ConstMonad):
    def len(monad):
        return ConstMonad.new(len(monad.value))


class BufferConstMonad(ConstMonad):
    pass


class NumericConstMonad(NumericMixin, ConstMonad):
    pass


class DateConstMonad(ConstMonad):
    pass


class TimeConstMonad(ConstMonad):
    pass


class DatetimeConstMonad(ConstMonad):
    pass


class BoolMonad(Monad):
    def __init__(monad, nullable=True):
        Monad.__init__(monad, bool, nullable=nullable)

    def nonzero(monad):
        return monad


cmp_ops = {'>=': 'GE', '>': 'GT', '<=': 'LE', '<': 'LT'}
cmp_negate = {'<': '>=', '<=': '>', '==': '!=', 'is': 'is not'}
cmp_negate.update((b, a) for a, b in list(cmp_negate.items()))


class CmpMonad(BoolMonad):
    EQ = 'EQ'
    NE = 'NE'

    def __init__(monad, op, left, right):
        if op == '<>':
            op = '!='
        if left.type is NoneType:
            left, right = right, left
        if right.type is NoneType:
            if op == '==':
                op = 'is'
            elif op == '!=':
                op = 'is not'
        elif op == 'is':
            op = '=='
        elif op == 'is not':
            op = '!='
        check_comparable(left, right, op)
        result_type, left, right = coerce_monads(left, right, for_comparison=True)
        BoolMonad.__init__(monad, nullable=left.nullable or right.nullable)
        monad.op = op
        monad.aggregated = getattr(left, 'aggregated', False) or getattr(right, 'aggregated', False)

        monad.left = left
        monad.right = right

    def negate(monad):
        return CmpMonad(cmp_negate[monad.op], monad.left, monad.right)

    def getsql(monad, sqlquery=None):
        op = monad.op
        if monad.left.type is NoneType and monad.right.type is NoneType:  # in hybrid methods
            return [['EQ' if op == 'is' else 'NE', ['VALUE', 1], ['VALUE', 1]]]
        left_sql = monad.left.getsql()
        if op == 'is':
            return [sqland([['IS_NULL', item] for item in left_sql])]
        if op == 'is not':
            return [sqland([['IS_NOT_NULL', item] for item in left_sql])]
        right_sql = monad.right.getsql()
        if len(left_sql) == 1 and left_sql[0][0] == 'ROW':
            left_sql = left_sql[0][1:]
        if len(right_sql) == 1 and right_sql[0][0] == 'ROW':
            right_sql = right_sql[0][1:]
        assert len(left_sql) == len(right_sql)
        size = len(left_sql)
        if op in ('<', '<=', '>', '>='):
            if size == 1:
                return [[cmp_ops[op], left_sql[0], right_sql[0]]]
            if monad.translator.row_value_syntax:
                return [[cmp_ops[op], ['ROW'] + left_sql, ['ROW'] + right_sql]]
            clauses = []
            for i in range(size):
                clause = [[monad.EQ, left_sql[j], right_sql[j]] for j in range(i)]
                clause.append([cmp_ops[op], left_sql[i], right_sql[i]])
                clauses.append(sqland(clause))
            return [sqlor(clauses)]
        if op == '==':
            return [sqland([[monad.EQ, a, b] for a, b in zip(left_sql, right_sql)])]
        if op == '!=':
            return [sqlor([[monad.NE, a, b] for a, b in zip(left_sql, right_sql)])]
        assert False, op  # pragma: no cover


class LogicalBinOpMonad(BoolMonad):
    def __init__(monad, operands):
        assert len(operands) >= 2
        items = []
        for operand in operands:
            if operand.type is not bool:
                items.append(operand.nonzero())
            elif isinstance(operand, LogicalBinOpMonad) and monad.binop == operand.binop:
                items.extend(operand.operands)
            else:
                items.append(operand)
        nullable = any(item.nullable for item in items)
        BoolMonad.__init__(monad, nullable=nullable)
        monad.operands = items

    def getsql(monad, sqlquery=None):
        result = [monad.binop]
        for operand in monad.operands:
            operand_sql = operand.getsql()
            assert len(operand_sql) == 1
            result.extend(operand_sql)
        return [result]


class AndMonad(LogicalBinOpMonad):
    binop = 'AND'


class OrMonad(LogicalBinOpMonad):
    binop = 'OR'


class NotMonad(BoolMonad):
    def __init__(monad, operand):
        if operand.type is not bool:
            operand = operand.nonzero()
        BoolMonad.__init__(monad, nullable=operand.nullable)
        monad.operand = operand

    def negate(monad):
        return monad.operand

    def getsql(monad, sqlquery=None):
        return [['NOT', monad.operand.getsql()[0]]]


class FuncMonadMeta(MonadMeta):
    def __new__(meta, cls_name, bases, cls_dict):
        monad_cls = super(FuncMonadMeta, meta).__new__(meta, cls_name, bases, cls_dict)
        return monad_cls


class FuncMonad(Monad, metaclass=FuncMonadMeta):
    def __call__(monad, *args, **kwargs):
        try:
            return monad.call(*args, **kwargs)
        except TypeError as exc:
            reraise_improved_typeerror(exc, 'call', monad.type.__name__)


def count(*args, **kwargs):
    if kwargs:
        return itertools.count(*args, **kwargs)
    if len(args) != 1:
        return itertools.count(*args)
    arg = args[0]
    if hasattr(arg, 'count'):
        return arg.count()
    try:
        it = iter(arg)
    except TypeError:
        return itertools.count(arg)
    return len(set(it))


class FuncCountMonad(FuncMonad):
    func = itertools.count, count

    def call(monad, x=None, distinct=None):
        if isinstance(x, StringConstMonad) and x.value == '*':
            x = None
            
        if x is not None:
            return x.count(distinct)
        
        result = ExprMonad.new(int, ['COUNT', None], nullable=False)
        result.aggregated = True
        return result


class FuncGenericMonad(FuncMonad):
    func = generic

    def call(self, *args, **kwargs):
        if (len(args)>0):
            x = args[0]
        else:
            reraise_improved_typeerror(x, 'call', "FuncGenericMonad wrong args")

        custom_func = kwargs['custom_func']
        generic_function = 'GENERIC_' + custom_func

        return x.aggregate(generic_function, args)

class SetMixin(MonadMixin):
    forced_distinct = False

    def call_distinct(monad):
        new_monad = object.__new__(monad.__class__)
        new_monad.__dict__.update(monad.__dict__)
        new_monad.forced_distinct = True
        return new_monad


class QuerySetMonad(SetMixin, Monad):
    nogroup = True

    def __init__(monad, subtranslator):
        item_type = subtranslator.expr_type
        monad_type = SetType(item_type)
        Monad.__init__(monad, monad_type)
        monad.subtranslator = subtranslator
        monad.item_type = item_type
        monad.limit = monad.offset = None

    def to_single_cell_value(monad):
        return ExprMonad.new(monad.item_type, monad.getsql()[0])

    def requires_distinct(monad, joined=False):
        assert False

    def aggregate(monad, func_name, distinct=None, sep=None, **kwargs):

        func_gen_name = func_name

        generic_funcion = func_name.startswith('GENERIC_')
        if (generic_funcion):
            x = func_name.split("_")
            func_gen_name = x[0]

        distinct = distinct_from_monad(
            distinct, default=monad.forced_distinct and func_gen_name in ('GENERIC'))
        sub = monad.subtranslator
        if sub.aggregated:
            throw(TypeError, 'Too complex aggregation in {EXPR}')
        subquery_ast = sub.construct_subquery_ast(distinct=False)
        from_ast, where_ast = subquery_ast[2:4]
        expr_type = sub.expr_type

        assert len(sub.expr_columns) == 1
        aggr_ast = [func_name, distinct, sub.expr_columns[0]]

        select_ast = ['AGGREGATES', aggr_ast]
        sql_ast = ['SELECT', select_ast, from_ast, where_ast]

        if func_gen_name == 'GENERIC':
            result_type = float

        else:
            result_type = expr_type
        return ExprMonad.new(result_type, sql_ast, func_gen_name != 'SUM')

    def getsql(monad):
        return [monad.subtranslator.construct_subquery_ast(monad.limit, monad.offset)]


def make_aggrfunction(std_func):
    def aggrfunc(*args, **kwargs):
        if not args:
            return std_func(**kwargs)
        arg = args[0]
        if type(arg) is types.GeneratorType:
            try:
                iterator = arg.gi_frame.f_locals['.0']
            except:
                return std_func(*args, **kwargs)

        return std_func(*args, **kwargs)
    aggrfunc.__name__ = std_func.__name__
    return aggrfunc


class EntityMeta(type):
    def __new__(meta, name, bases, cls_dict):
        if 'Entity' in globals():
            if '__slots__' in cls_dict:
                throw(TypeError, 'Entity classes cannot contain __slots__ variable')
            cls_dict['__slots__'] = ()
        return super(EntityMeta, meta).__new__(meta, name, bases, cls_dict)

    def __init__(entity, name, bases, cls_dict):
        super(EntityMeta, entity).__init__(name, bases, cls_dict)
        entity._database_ = None
        if name == 'Entity':
            return

        if not entity.__name__[:1].isupper():
            throw(ERDiagramError, 'Entity class name should start with a capital letter. Got: %s' % entity.__name__)

        for base_class in bases:
            if isinstance(base_class, EntityMeta):
                database = base_class._database_

        entity._database_ = database

        entity._id_ = next(entity_id_counter)

        entity._root_ = entity

        new_attrs = []
        for name, attr in list(entity.__dict__.items()):

            if not isinstance(attr, Attribute):
                continue

            attr._init_(entity, name)
            new_attrs.append(attr)

        new_attrs.sort(key=attrgetter('id'))

        entity._new_attrs_ = new_attrs
        entity._attrs_ = new_attrs
        entity._adict_ = {attr.name: attr for attr in entity._attrs_}

        try:
            table_name = entity.__dict__['_table_']
        except KeyError:
            entity._table_ = None
        else:
            if not isinstance(table_name, str):
                entity._table_ = table_name = tuple(table_name)

        database.entities[entity.__name__] = entity
        setattr(database, entity.__name__, entity)

        iter_name = (
            ''.join(letter for letter in entity.__name__ if letter.isupper()).lower() or
            entity.__name__
        )
        comprehension = ast.comprehension(
            target=ast.Name(iter_name, ast.Store()),
            iter=ast.Name('.0', ast.Load()),
            ifs=[]
        )
        entity._default_genexpr_ = ast.GeneratorExp(ast.Name(iter_name, ast.Load()), [comprehension])

        entity._access_rules_ = defaultdict(set)

    def __iter__(entity):
        return EntityIter(entity)

    def _construct_select_clause_(entity, alias=None, distinct=False, query_attrs=(), all_attributes=False):

        select_list = ['DISTINCT'] if distinct else ['ALL']
        root = entity._root_

        for attr in itertools.chain(root._attrs_, []):
            if not all_attributes and not issubclass(attr.entity, entity) \
                    and not issubclass(entity, attr.entity):
                continue

            if not attr.columns:
                continue

            for column in attr.columns:
                select_list.append(['COLUMN', alias, column])
        return select_list


class Entity(object, metaclass=EntityMeta):
    __slots__ = '_status_', '_pkval_', '_newid_', '_dbvals_', '_vals_', '_rbits_', '_wbits_', '__weakref__'


class EntityIter(object):
    def __init__(self, entity):
        self.entity = entity

    def next(self):
        throw(TypeError, 'Use select(...) function or %s.select(...) method for iteration'
                         % self.entity.__name__)
    __next__ = next


class Attribute(object):
    __slots__ = 'nullable', 'id', 'py_type', 'entity', 'name'

    def __init__(attr, py_type, *args, **kwargs):
        attr.nullable = False
        attr.id = next(attr_id_counter)
        attr.py_type = py_type
        attr.entity = attr.name = None

    def _init_(attr, entity, name):
        attr.entity = entity
        attr.name = name

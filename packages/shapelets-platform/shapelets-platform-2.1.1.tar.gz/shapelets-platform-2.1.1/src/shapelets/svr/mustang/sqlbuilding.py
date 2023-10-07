from decimal import Decimal
from datetime import date, datetime, timedelta
from binascii import hexlify

from .conversions import datetime2timestamp, timedelta2str
from .exceptions import AstError, throw


class Value(object):
    __slots__ = 'paramstyle', 'value'

    def __init__(self, paramstyle, value):
        self.paramstyle = paramstyle
        self.value = value

    def __str__(self):
        value = self.value
        if value is None:
            return 'null'
        if isinstance(value, bool):
            return value and '1' or '0'
        if isinstance(value, str):
            return self.quote_str(value)
        if isinstance(value, datetime):
            return 'TIMESTAMP ' + self.quote_str(datetime2timestamp(value))
        if isinstance(value, date):
            return 'DATE ' + self.quote_str(str(value))
        if isinstance(value, timedelta):
            return "INTERVAL '%s' HOUR TO SECOND" % timedelta2str(value)
        if isinstance(value, (int, float, Decimal)):
            return str(value)
        if isinstance(value, bytes):
            return "X'%s'" % hexlify(value).decode('ascii')
        assert False, repr(value)  # pragma: no cover

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.value)

    def quote_str(self, s):
        if self.paramstyle in ('format', 'pyformat'):
            s = s.replace('%', '%%')
        return "'%s'" % s.replace("'", "''")


def flat(tree):
    stack = [tree]
    result = []
    stack_pop = stack.pop
    stack_extend = stack.extend
    result_append = result.append
    while stack:
        x = stack_pop()
        if isinstance(x, str):
            result_append(x)
        else:
            try:
                stack_extend(x)
            except TypeError:
                result_append(x)
    return result[::-1]


def flat_conditions(conditions):
    result = []
    for condition in conditions:
        if condition[0] == 'AND':
            result.extend(flat_conditions(condition[1:]))
        else:
            result.append(condition)
    return result


def join(delimiter, items):
    items = iter(items)
    try:
        result = [next(items)]
    except StopIteration:
        return []
    for item in items:
        result.append(delimiter)
        result.append(item)
    return result


def move_conditions_from_inner_join_to_where(sections):
    new_sections = list(sections)
    for i, section in enumerate(sections):
        if section[0] == 'FROM':
            new_from_list = ['FROM'] + [list(item) for item in section[1:]]
            new_sections[i] = new_from_list
            if len(sections) > i + 1 and sections[i + 1][0] == 'WHERE':
                new_where_list = list(sections[i + 1])
                new_sections[i + 1] = new_where_list
            else:
                new_where_list = ['WHERE']
                new_sections.insert(i + 1, new_where_list)
            break
    else:
        return sections
    for join in new_from_list[2:]:
        if join[1] in ('TABLE', 'SELECT') and len(join) == 4:
            new_where_list.append(join.pop())
    return new_sections


def make_binary_op(symbol, default_parentheses=False):
    def binary_op(builder, expr1, expr2, parentheses=None):
        if parentheses is None:
            parentheses = default_parentheses
        if parentheses:
            return '(', builder(expr1), symbol, builder(expr2), ')'
        return builder(expr1), symbol, builder(expr2)
    return binary_op


def indentable(method):
    def new_method(builder, *args, **kwargs):
        result = method(builder, *args, **kwargs)
        if builder.indent <= 1:
            return result
        return builder.indent_spaces * (builder.indent - 1), result
    new_method.__name__ = method.__name__
    return new_method


class SQLBuilder(object):
    dialect = None
    value_class = Value
    indent_spaces = " " * 4
    least_func_name = 'least'
    greatest_func_name = 'greatest'

    def __init__(builder, provider, ast):
        builder.provider = provider
        builder.quote_name = provider.quote_name
        builder.paramstyle = provider.paramstyle
        builder.ast = ast
        builder.indent = 0
        builder.inner_join_syntax = False
        builder.suppress_aliases = False
        builder.result = flat(builder(ast))

        builder.sql = u''.join(map(str, builder.result)).rstrip('\n')

    def __call__(builder, ast):
        if isinstance(ast, str):
            throw(AstError, 'An SQL AST list was expected. Got string: %r' % ast)
        try:
            symbol = ast[0]
        except:
            symbol = ast

        if not isinstance(symbol, str):
            throw(AstError, 'Invalid node name in AST: %r' % ast)

        if (symbol in ['SUM', 'MIN', 'MAX']):
            symbol = 'GENERIC_' + symbol

        method = getattr(builder, symbol, None)
        generic_funcion = symbol.startswith('GENERIC_')

        try:
            if (generic_funcion):
                x = symbol.split("_")
                new_symbol = x[0]
                method = getattr(builder, new_symbol, None)
                func = x[1]

                return method(*ast[1:], custom_func=func)
            else:
                return method(*ast[1:])

        except TypeError:
            raise

    def DEFAULT(builder):
        return 'DEFAULT'

    def _subquery(builder, *sections):
        builder.indent += 1
        if not builder.inner_join_syntax:
            sections = move_conditions_from_inner_join_to_where(sections)
        result = [builder(s) for s in sections]
        builder.indent -= 1
        return result

    def SELECT(builder, *sections):
        prev_suppress_aliases = builder.suppress_aliases
        builder.suppress_aliases = False
        try:
            result = builder._subquery(*sections)
            if builder.indent:
                indent = builder.indent_spaces * builder.indent
                return '(\n', result, indent + ')'
            return result
        finally:
            builder.suppress_aliases = prev_suppress_aliases

    @indentable
    def ALL(builder, *expr_list):
        exprs = [builder(e) for e in expr_list]
        return 'SELECT ', join(', ', exprs), '\n'

    @indentable
    def DISTINCT(builder, *expr_list):
        exprs = [builder(e) for e in expr_list]
        return 'SELECT DISTINCT ', join(', ', exprs), '\n'

    @indentable
    def AGGREGATES(builder, *expr_list, **kwargs):
        exprs = [builder(e) for e in expr_list]
        return 'SELECT ', join(', ', exprs), '\n'

    def sql_join(builder, join_type, sources):
        indent = builder.indent_spaces * (builder.indent - 1)
        indent2 = indent + builder.indent_spaces
        result = [indent, 'FROM ']
        for i, source in enumerate(sources):
            if len(source) == 3:
                alias, kind, x = source
                join_cond = None
            elif len(source) == 4:
                alias, kind, x, join_cond = source
            else:
                throw(AstError, 'Invalid source in FROM section: %r' % source)
            if i > 0:
                if join_cond is None:
                    result.append(', ')
                else:
                    result += ['\n', indent, '  %s JOIN ' % join_type]
            if builder.suppress_aliases:
                alias = None
            elif alias is not None:
                alias = builder.quote_name(alias)
            if kind == 'TABLE':
                if isinstance(x, str):
                    result.append(builder.quote_name(x))
                else:
                    result.append(builder.compound_name(x))
                if alias is not None:
                    result += ' ', alias  # Oracle does not support 'AS' here
            elif kind == 'SELECT':
                if alias is None:
                    throw(AstError, 'Subquery in FROM section must have an alias')
                result += builder.SELECT(*x), ' ', alias  # Oracle does not support 'AS' here
            else:
                throw(AstError, 'Invalid source kind in FROM section: %r' % kind)
            if join_cond is not None:
                result += ['\n', indent2, 'ON ', builder(join_cond)]
        result.append('\n')
        return result

    def FROM(builder, *sources):
        return builder.sql_join('INNER', sources)

    def INNER_JOIN(builder, *sources):
        builder.inner_join_syntax = True
        return builder.sql_join('INNER', sources)

    @indentable
    def LEFT_JOIN(builder, *sources):
        return builder.sql_join('LEFT', sources)

    def WHERE(builder, *conditions):
        if not conditions:
            return ''
        conditions = flat_conditions(conditions)
        indent = builder.indent_spaces * (builder.indent - 1)
        result = [indent, 'WHERE ']
        extend = result.extend
        extend((builder(conditions[0]), '\n'))
        for condition in conditions[1:]:
            extend((indent, '  AND ', builder(condition), '\n'))
        return result

    @indentable
    def GROUP_BY(builder, *expr_list):
        exprs = [builder(e) for e in expr_list]
        return 'GROUP BY ', join(', ', exprs), '\n'

    def COLUMN(builder, table_alias, col_name):
        if builder.suppress_aliases or not table_alias:
            return ['%s' % builder.quote_name(col_name)]
        return ['%s.%s' % (builder.quote_name(table_alias), builder.quote_name(col_name))]

    def ROW(builder, *items):
        return '(', join(', ', map(builder, items)), ')'

    def VALUE(builder, value):
        return builder.value_class(builder.paramstyle, value)

    EQ = make_binary_op(' = ')
    NE = make_binary_op(' <> ')
    LT = make_binary_op(' < ')
    LE = make_binary_op(' <= ')
    GT = make_binary_op(' > ')
    GE = make_binary_op(' >= ')
    ADD = make_binary_op(' + ', True)
    SUB = make_binary_op(' - ', True)
    MUL = make_binary_op(' * ', True)
    DIV = make_binary_op(' / ', True)
    FLOORDIV = make_binary_op(' / ', True)

    def GENERIC(builder, *args, **kwargs):

        custom = kwargs['custom_func']
        
        result = None
        
        if len(args)==1:
            expr = args[0]
            result = custom + '(', builder(expr), ')'
            res = convert_date(custom,builder,expr)
            if (res is not None):
                result = res
        
        if len(args)>1:
            result = custom + '('
            last = len(args)
            idx = 0
            for arg in args:
                str_expr = get_str_expression(builder, custom, arg)
                idx += 1
                if (str_expr is not None):
                    if (idx==last):
                        result = result, str_expr
                    else:
                        result = result, str_expr, ','
                
            result = result, ')'
   
        return result

def get_str_expression(builder, custom, expr):
    
    if type(expr) == int or type(expr) == float:
        str_expr = list(str(expr))
    elif type(expr) == bool:
        return None
    else:
        str_expr = builder(expr)

    res = convert_date(custom,builder,expr)
    if (res is not None):
        str_expr = res
        
    return str_expr
    
def convert_date(custom,builder,expr):
    
    res = None
    
    if (custom == 'getDate'):
        res = 'CAST(', builder(expr), ' AS DATE)'
    elif (custom == 'getTime'):
        res = 'CAST(', builder(expr), ' AS TIME)'
    elif (custom == 'day'):
        res = 'extract (day from ', builder(expr), ')'
    elif (custom == 'month'):
        res = 'extract (month from ', builder(expr), ')'
    elif (custom == 'year'):
        res = 'extract (year from ', builder(expr), ')'
    elif (custom == 'hour'):
        res = 'extract (hour from ', builder(expr), ')'
    elif (custom == 'minute'):
        res = 'extract (minute from ', builder(expr), ')'
    elif (custom == 'second'):
        res = 'extract (second from ', builder(expr), ')'

    return res
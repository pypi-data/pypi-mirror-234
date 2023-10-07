from __future__ import annotations

from typing import Any, Dict, Optional, Set, Union

import ast
import sys
import types
import inspect

from collections import defaultdict
from dataclasses import dataclass, field, replace

from opcode import (opname as opNames, HAVE_ARGUMENT, EXTENDED_ARG, cmp_op, hasconst as hasConst,
                    hasname as hasName, hasjrel as hasJRel, haslocal as hasLocal, hascompare as hasCompare,
                    hasfree as hasFree, hasjabs as hasJAbs)

from .python_versions import PY36, PYPY, PY37, PY38, PY39, PY310
from .exceptions import DecompileError, InvalidQuery


@dataclass
class ObjectsInFrame:
    locals: Dict[str, Any]
    globals: Dict[str, Any]


def captureObjectsInFrame(codeObj: Union[str, types.GeneratorType, types.FunctionType],
                          givenGlobals: Optional[Dict[str, Any]] = None,
                          givenLocals: Optional[Dict[str, Any]] = None,
                          frame_depth: Optional[int] = None) -> ObjectsInFrame:
    r"""
    Captures defined variables either at local or global level 

    """

    globals = {} if givenGlobals is None else givenGlobals.copy()
    locals = {} if givenLocals is None else givenLocals.copy()

    if givenLocals is not None:
        if type(codeObj) is types.GeneratorType:
            locals.update(codeObj.gi_frame.f_locals)
            if givenGlobals is None:
                globals = codeObj.gi_frame.f_globals
    else:

        if frame_depth is not None:
            frame = sys._getframe(frame_depth + 1)
            locals.update(frame.f_locals)
            globals = frame.f_globals

        if type(codeObj) is types.GeneratorType:
            # just change the reference
            globals = codeObj.gi_frame.f_globals
            # but always update (last) locals from codeObj
            locals.update(codeObj.gi_frame.f_locals)

    return ObjectsInFrame(locals, globals)



@dataclass(frozen=True)
class ASTTree:
    tree: ast.AST
    externalNames: Set[str] = field(default_factory=lambda: set())
    cells: Optional[Dict[str, types._Cell]] = None



def string2ast(s: str) -> ASTTree:

    module_node = ast.parse('(%s)' % s)
    assert isinstance(module_node, ast.Module)
    assert len(module_node.body) == 1
    expr = module_node.body[0]
    assert isinstance(expr, ast.Expr)

    result = ASTTree(expr.value)

    return result



def decompile(x: Union[types.CodeType, types.GeneratorType, types.FunctionType]) -> ASTTree:
    cells = {}
    t = type(x)

    if t is types.CodeType:
        codeObject = x

    elif t is types.GeneratorType:
        codeObject = x.gi_frame.f_code

    elif t is types.FunctionType:
        codeObject = x.__code__
        if x.__closure__:
            cells = dict(zip(codeObject.co_freevars, x.__closure__))
    else:
        raise TypeError()

    decompiler = Decompiler()
    result = decompiler.run(codeObject)

    return replace(result, cells=cells)


def _simplify(clause):
    if isinstance(clause, ast.BoolOp) and isinstance(clause.op, ast.And):
        if len(clause.values) == 1:
            result = clause.values[0]
        else:
            return clause
    elif isinstance(clause, ast.BoolOp) and isinstance(clause.op, ast.Or):
        if len(clause.values) == 1:
            result = ast.UnaryOp(op=ast.Not(), operand=clause.values[0])
        else:
            return clause
    else:
        return clause

    if getattr(result, 'endpos', 0) < clause.endpos:
        result.endpos = clause.endpos

    return result


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


def _clean_assign(node):
    if isinstance(node, ast.Assign):
        return node.targets
    return node


def _is_const(value):
    if isinstance(value, ast.Constant):
        return True
    if PY38:
        return False
    if isinstance(value, (ast.Num, ast.Str, ast.Bytes)):
        return True
    if isinstance(value, ast.Tuple):
        return all(_is_const(elt) for elt in value.elts)
    return False


def _make_const(value):
    if _is_const(value):
        return value
    if PY39:
        return ast.Constant(value)
    elif PY38:
        return ast.Constant(value, None)
    elif isinstance(value, (int, float)):
        return ast.Num(value)
    elif isinstance(value, str):
        return ast.Str(value)
    elif isinstance(value, bytes):
        return ast.Bytes(value)
    elif isinstance(value, tuple):
        return ast.Tuple([_make_const(elt) for elt in value], ast.Load())
    elif value in (True, False, None):
        return ast.NameConstant(value)
    elif isinstance(value, types.CodeType):
        return ast.Constant(value)
    elif value is Ellipsis:
        return ast.Constant(value)
    assert False, value


def _unwrap_str(key):
    if PY38:
        assert isinstance(key, str)
        return key
    assert isinstance(key, ast.Str)
    return key.s



class Decompiler:

    def __init__(self):
        self._stack = []
        self._jump_map = defaultdict(list)
        self._targets = {}
        self._names = set()
        self._assNames = set()
        self._conditions_end = 0
        self._instructions = []
        self._instructions_map = {}
        self._or_jumps = set()
        self._abs_jump_to_top = -1
        self._for_iter_pos = -1

    def run(self, code: types.CodeType, start: int = 0, end: Optional[int] = None) -> ASTTree:
        self._code = code
        self._start = start
        self._pos = start
        self._end = end if end is not None else len(code.co_code)

        self._get_instructions()
        self._analyze_jumps()
        self._decompile()

        ast = self._stack.pop()
        externalNames = self._names - self._assNames

        if self._stack:
            raise DecompileError('Compiled code should represent a single expression')

        return ASTTree(ast, externalNames)

    def _get_instructions(self):
        """
        This is the first pass through the python instruction.

        It collects the offsets, the instruction code and the arguments 
        for later processing.
        """
        beforeYield = True
        code = self._code
        co_code = code.co_code
        free = code.co_cellvars + code.co_freevars
        self._abs_jump_to_top = self._for_iter_pos = -1

        while self._pos < self._end:
            i = self._pos
            op = code.co_code[i]
            opName = opNames[op].replace('+', '_')
            if PY36:
                extended_arg = 0
                opArg = code.co_code[i + 1]
                while op == EXTENDED_ARG:
                    extended_arg = (extended_arg | opArg) << 8
                    i += 2
                    op = code.co_code[i]
                    opArg = code.co_code[i + 1]
                opArg = None if op < HAVE_ARGUMENT else opArg | extended_arg
                i += 2
            else:
                i += 1
                if op >= HAVE_ARGUMENT:
                    opArg = co_code[i] + co_code[i + 1] * 256
                    i += 2
                    if op == EXTENDED_ARG:
                        op = code.co_code[i]
                        i += 1
                        opArg = co_code[i] + co_code[i + 1] * 256 + opArg * 65536
                        i += 2
            if op >= HAVE_ARGUMENT:
                if op in hasConst:
                    arg = [code.co_consts[opArg]]
                elif op in hasName:
                    arg = [code.co_names[opArg]]
                elif op in hasJRel:
                    arg = [i + opArg * (2 if PY310 else 1)]
                elif op in hasLocal:
                    arg = [code.co_varnames[opArg]]
                elif op in hasCompare:
                    arg = [cmp_op[opArg]]
                elif op in hasFree:
                    arg = [free[opArg]]
                elif op in hasJAbs:
                    arg = [opArg * (2 if PY310 else 1)]
                else:
                    arg = [opArg]
            else:
                arg = []
            if opName == 'FOR_ITER':
                self._for_iter_pos = self._pos
            if opName == 'JUMP_ABSOLUTE' and arg[0] == self._for_iter_pos:
                self._abs_jump_to_top = self._pos

            if beforeYield:
                if 'JUMP' in opName:
                    endPos = arg[0]
                    if endPos < self._pos:
                        self._conditions_end = i
                    self._jump_map[endPos].append(self._pos)
                self._instructions_map[self._pos] = len(self._instructions)
                self._instructions.append((self._pos, i, opName, arg))
            if opName == 'YIELD_VALUE':
                beforeYield = False
            self._pos = i

    def _analyze_jumps(self):
        if PYPY:
            targets = self._jump_map.pop(self._abs_jump_to_top, [])
            self._jump_map[self._for_iter_pos] = targets
            for i, (x, y, opName, arg) in enumerate(self._instructions):
                if 'JUMP' in opName:
                    target = arg[0]
                    if target == self._abs_jump_to_top:
                        self._instructions[i] = (x, y, opName, [self._for_iter_pos])
                        self._conditions_end = y

        i = self._instructions_map[self._conditions_end]
        while i > 0:
            pos, next_pos, opName, arg = self._instructions[i]
            if pos in self._jump_map:
                for jump_start_pos in self._jump_map[pos]:
                    if jump_start_pos > pos:
                        continue
                    for or_jump_start_pos in self._or_jumps:
                        if pos > or_jump_start_pos > jump_start_pos:
                            break  # And jump
                    else:
                        self._or_jumps.add(jump_start_pos)
            i -= 1

    def _decompile(self):
        for pos, next_pos, opName, arg in self._instructions:
            if pos in self._targets:
                self._process_target(pos)
            method = getattr(self, opName, None)

            if method is None:
                raise DecompileError('Unsupported operation: %s' % opName)

            self._pos = pos
            self.next_pos = next_pos
            # do the call to the handler
            x = method(*arg)
            if x is not None:
                self._stack.append(x)

    def _pop_items(self, size):
        if not size:
            return []
        result = self._stack[-size:]
        self._stack[-size:] = []
        return result

    def _store(self, node):
        stack = self._stack
        if not stack:
            stack.append(node)
            return
        top = stack[-1]
        if isinstance(top, ast.Assign):
            target = top.targets
            if isinstance(target, (ast.Tuple, ast.List)) and len(target.elts) < top.count:
                target.elts.append(_clean_assign(node))
                if len(target.elts) == top.count:
                    self._store(stack.pop())
            else:
                stack.append(node)
        elif isinstance(top, ast.comprehension):
            assert top.target is None
            if isinstance(node, ast.Assign):
                node = node.targets
            top.target = node
        else:
            stack.append(node)

    def _call_function(self, args, keywords=None):
        tos = self._stack.pop()
        if isinstance(tos, ast.GeneratorExp):
            assert len(args) == 1 and not keywords
            genExpr = tos
            qual = genExpr.generators[0]
            assert isinstance(qual.iter, ast.Name)
            assert qual.iter.id == '.0'
            qual.iter = args[0]
            return genExpr
        return ast.Call(tos, args, keywords)

    def BINARY_POWER(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.Pow(), right=op2)

    def BINARY_MULTIPLY(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.Mult(), right=op2)

    def BINARY_DIVIDE(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.Div(), right=op2)

    def BINARY_FLOOR_DIVIDE(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.FloorDiv(), right=op2)

    def BINARY_ADD(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.Add(), right=op2)

    def BINARY_SUBTRACT(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.Sub(), right=op2)

    def BINARY_LSHIFT(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.LShift(), right=op2)

    def BINARY_RSHIFT(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.RShift(), right=op2)

    def BINARY_AND(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.BitAnd(), right=op2)

    def BINARY_XOR(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.BitXor(), right=op2)

    def BINARY_OR(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.BitOr(), right=op2)

    def BINARY_TRUE_DIVIDE(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.Div(), right=op2)

    def BINARY_MODULO(self):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        return ast.BinOp(left=op1, op=ast.Mod(), right=op2)

    def BINARY_SUBSCR(self):
        node2 = self._stack.pop()
        node1 = self._stack.pop()
        if isinstance(node2, ast.Slice):  # and len(node2.nodes) == 2:
            if isinstance(node2.lower, ast.Constant) and node2.lower.value is None:
                node2.lower = None
            if isinstance(node2.upper, ast.Constant) and node2.upper.value is None:
                node2.upper = None
        elif not PY38:
            if isinstance(node2, ast.Tuple) and any(isinstance(item, ast.Slice) for item in node2.elts):
                node2 = ast.ExtSlice(node2.elts)
            else:
                node2 = ast.Index(node2)
        return ast.Subscript(value=node1, slice=node2, ctx=ast.Load())

    def BUILD_CONST_KEY_MAP(self, length):
        keys = self._stack.pop()
        if PY38:
            assert isinstance(keys, ast.Constant), keys
            keys = [_make_const(key) for key in keys.value]
        else:
            assert isinstance(keys, ast.Tuple) and _is_const(keys), keys
            keys = [_make_const(key) for key in keys.elts]

        values = self._pop_items(length)
        return ast.Dict(keys=keys, values=values)

    def BUILD_LIST(self, size):
        return ast.List(self._pop_items(size), ast.Load())

    def BUILD_MAP(self, length):
        if sys.version_info < (3, 5):
            return ast.Dict(())
        data = self._pop_items(2 * length)  # [key1, value1, key2, value2, ...]
        keys, values = [], []
        for i in range(0, len(data), 2):
            keys.append(data[i])
            values.append(data[i + 1])
        return ast.Dict(keys=keys, values=values)

    def BUILD_SET(self, size):
        return ast.Set(self._pop_items(size))

    def BUILD_SLICE(self, size):
        items = self._pop_items(size)
        if not PY38:
            items = [None if isinstance(item, ast.NameConstant) and item.value is None else item for item in items]
        items += [None] * (3 - len(items))
        return ast.Slice(*items, ctx=ast.Load())

    def BUILD_TUPLE(self, size):
        return ast.Tuple(self._pop_items(size), ast.Load())

    def BUILD_STRING(self, count):
        items = list(reversed([self._stack.pop() for _ in range(count)]))
        for i, item in enumerate(items):
            if isinstance(item, ast.Constant):
                if not isinstance(item.value, str):
                    raise NotImplementedError(item)
            elif not isinstance(item, ast.FormattedValue):
                items[i] = ast.FormattedValue(item, -1)
        return ast.JoinedStr(items)

    def CALL_FUNCTION(self, argc, star=None, star2=None):
        pop = self._stack.pop
        kwArg, posArg = divmod(argc, 256)
        keywords = []
        for i in range(kwArg):
            arg = pop()
            key = pop().value
            keywords.append(ast.keyword(_unwrap_str(key), arg))
        keywords.reverse()
        args = []
        for i in range(posArg):
            args.append(pop())
        args.reverse()
        if star:
            args.append(ast.Starred(value=star))
        if star2:
            keywords.append(ast.keyword(value=star2))
        return self._call_function(args, keywords)

    def CALL_FUNCTION_VAR(self, argc):
        return self.CALL_FUNCTION(argc, self._stack.pop())

    def CALL_FUNCTION_KW(self, argc):
        if sys.version_info < (3, 6):
            return self.CALL_FUNCTION(argc, star2=self._stack.pop())

        keys = self._stack.pop()
        assert _is_const(keys), keys
        if PY38:
            assert isinstance(keys, ast.Constant)
            keys = keys.value
        else:
            assert isinstance(keys, ast.Tuple)
            keys = keys.elts
        values = self._pop_items(argc)
        assert len(keys) <= len(values)
        args = values[:-len(keys)]
        keywords = [ast.keyword(_unwrap_str(k), v) for k, v in zip(keys, values[-len(keys):])]
        return self._call_function(args, keywords)

    def CALL_FUNCTION_VAR_KW(self, argc):
        star2 = self._stack.pop()
        star = self._stack.pop()
        return self.CALL_FUNCTION(argc, star, star2)

    def CALL_FUNCTION_EX(self, argc):
        star2 = None
        if argc:
            if argc != 1:
                raise DecompileError()
            star2 = self._stack.pop()
        star = self._stack.pop()
        args = [ast.Starred(value=star)] if star else None
        keywords = [ast.keyword(value=star2)] if star2 else None
        return self._call_function(args, keywords)

    def CALL_METHOD(self, argc):
        pop = self._stack.pop
        args = []
        keywords = []
        if argc >= 256:
            kwarg_c = argc // 256
            argc = argc % 256
            for i in range(kwarg_c):
                v = pop()
                k = pop()
                assert isinstance(k, ast.Constant)
                k = k.value  # ast.Name(k.value)
                keywords.append(ast.keyword(k, v))
        for i in range(argc):
            args.append(pop())
        args.reverse()
        method = pop()
        
        if (isinstance(method,ast.Attribute)):
            name = method.attr
            method = method.value
            method.id = name
            
        return ast.Call(method, args, keywords)

    def COMPARE_OP(self, op):
        op2 = self._stack.pop()
        op1 = self._stack.pop()
        op = _operator_mapping[op]()
        return ast.Compare(op1, [op], [op2])

    def CONTAINS_OP(self, invert):
        return self.COMPARE_OP('not in' if invert else 'in')

    def DUP_TOP(decompiler):
        return decompiler._stack[-1]

    def FOR_ITER(self, endpos):
        target = None
        iter = self._stack.pop()
        ifs = []
        return ast.comprehension(target, iter, ifs, 0)

    def FORMAT_VALUE(self, flags):
        conversion = -1
        format_spec = None
        if flags in (0, 1, 2, 3):
            value = self._stack.pop()
            if flags == 0:
                conversion = -1
            elif flags == 1:
                conversion = ord('s')  # str conversion
            elif flags == 2:
                conversion = ord('r')  # repr conversion
            elif flags == 3:
                conversion = ord('a')  # ascii conversion
        elif flags == 4:
            format_spec = self._stack.pop()
            value = self._stack.pop()
        return ast.FormattedValue(value=value, conversion=conversion, format_spec=format_spec)

    def GEN_START(self, kind):
        assert kind == 0  # only support sync

    def GET_ITER(self):
        pass

    def JUMP_IF_FALSE(self, endpos):
        return self._conditional_jump(endpos, False)

    def JUMP_IF_FALSE_OR_POP(self, endpos):
        return self._conditional_jump(endpos, False)

    def JUMP_IF_NOT_EXC_MATCH(self, endpos):
        raise NotImplementedError()

    def JUMP_IF_TRUE(self, endpos):
        return self._conditional_jump(endpos, True)

    def JUMP_IF_TRUE_OR_POP(self, endpos):
        return self._conditional_jump(endpos, True)

    def _conditional_jump(self, endpos, if_true):
        if PY37 or PYPY:
            return self._conditional_jump_new(endpos, if_true)
        return self._conditional_jump_old(endpos, if_true)

    def _conditional_jump_old(self, endpos, if_true):
        i = self.next_pos
        if i in self._targets:
            self._process_target(i)
        expr = self._stack.pop()
        clausetype = ast.Or if if_true else ast.And
        clause = ast.BoolOp(op=clausetype(), values=[expr])
        clause.endpos = endpos
        self._targets.setdefault(endpos, clause)
        return clause

    def _conditional_jump_new(self, endpos, if_true):
        expr = self._stack.pop()
        if self._pos >= self._conditions_end:
            clausetype = ast.Or if if_true else ast.And
        elif self._pos in self._or_jumps:
            clausetype = ast.Or
            if not if_true:
                expr = ast.UnaryOp(op=ast.Not(), operand=expr)
        else:
            clausetype = ast.And
            if if_true:
                expr = ast.UnaryOp(op=ast.Not(), operand=expr)
        self._stack.append(expr)

        if self.next_pos in self._targets:
            self._process_target(self.next_pos)

        expr = self._stack.pop()
        clause = ast.BoolOp(op=clausetype(), values=[expr])
        clause.endpos = endpos
        self._targets.setdefault(endpos, clause)
        return clause

    def _process_target(self, pos, partial=False):
        if pos is None:
            limit = None
        elif partial:
            limit = self._targets.get(pos, None)
        else:
            limit = self._targets.pop(pos, None)
        top = self._stack.pop()
        while True:
            top = _simplify(top)
            if top is limit:
                break
            if isinstance(top, ast.comprehension):
                break
            if not self._stack:
                break

            top2 = self._stack[-1]
            if isinstance(top2, ast.comprehension):
                break
            if partial and hasattr(top2, 'endpos') and top2.endpos == pos:
                break

            if isinstance(top2, ast.BoolOp):
                if isinstance(top, ast.BoolOp) and type(top2.op) is type(top.op):
                    top2.values.extend(top.values)
                else:
                    top2.values.append(top)
            elif isinstance(top2, ast.IfExp):  # Python 2.5
                top2.orelse = top
                if hasattr(top, 'endpos'):
                    top2.endpos = top.endpos
                    if self._targets.get(top.endpos) is top:
                        self._targets[top.endpos] = top2
            else:
                raise DecompileError('Expression is too complex to decompile')

            top2.endpos = max(top2.endpos, getattr(top, 'endpos', 0))
            top = self._stack.pop()
        self._stack.append(top)

    def JUMP_FORWARD(self, endpos):
        i = self.next_pos  # next instruction
        self._process_target(i, True)
        then = self._stack.pop()
        self._process_target(i, False)
        test = self._stack.pop()
        if_exp = ast.IfExp(test=_simplify(test), body=_simplify(then), orelse=None)
        if_exp.endpos = endpos
        self._targets.setdefault(endpos, if_exp)
        if self._targets.get(endpos) is then:
            self._targets[endpos] = if_exp
        return if_exp

    def IS_OP(self, invert):
        return self.COMPARE_OP('is not' if invert else 'is')

    def LIST_APPEND(self, offset=None):
        raise InvalidQuery('Use generator expression (... for ... in ...) '
                           'instead of list comprehension [... for ... in ...] inside query')

    def LIST_EXTEND(self, offset):
        if offset != 1:
            raise NotImplementedError(offset)

        items = self._stack.pop()
        if not isinstance(items, ast.Constant):
            raise NotImplementedError(type(items))

        if not isinstance(items.value, tuple):
            raise NotImplementedError(type(items.value))

        lst = self._stack.pop()

        if not isinstance(lst, ast.List):
            raise NotImplementedError(type(lst))

        values = [_make_const(v) for v in items.value]
        lst.elts.extend(values)
        return lst

    def LOAD_ATTR(self, attr_name):
        return ast.Attribute(self._stack.pop(), attr_name, ast.Load())

    def LOAD_CLOSURE(self, freeVariable):
        self._names.add(freeVariable)
        return ast.Name(freeVariable, ast.Load())

    def LOAD_CONST(self, const_value):
        return _make_const(const_value)

    def LOAD_DEREF(self, freeVariable):
        self._names.add(freeVariable)
        return ast.Name(freeVariable, ast.Load())

    def LOAD_FAST(self, varname):
        self._names.add(varname)
        return ast.Name(varname, ast.Load())

    def LOAD_GLOBAL(self, varname):
        self._names.add(varname)
        return ast.Name(varname, ast.Load())

    def LOAD_METHOD(self, methodName):
        return self.LOAD_ATTR(methodName)

    def LOOKUP_METHOD(self, methodName):
        return self.LOAD_ATTR(methodName)  # For PyPy

    def LOAD_NAME(self, varname):
        self._names.add(varname)
        return ast.Name(varname, ast.Load())

    def MAKE_CLOSURE(self, argc):
        self._stack[-3:-2] = []  # ignore free variables
        return self.MAKE_FUNCTION(argc)

    def MAKE_FUNCTION(self, argc):
        defaults = []
        if sys.version_info >= (3, 6):
            qualifiedName = self._stack.pop()
            tos = self._stack.pop()
            if argc & 0x08:
                func_closure = self._stack.pop()
            if argc & 0x04:
                annotations = self._stack.pop()
            if argc & 0x02:
                kwonly_defaults = self._stack.pop()
                raise NotImplementedError()
            if argc & 0x01:
                defaults = self._stack.pop()
                assert isinstance(defaults, ast.Tuple)
                defaults = defaults.elts
        else:
            qualifiedName = self._stack.pop()
            tos = self._stack.pop()
            if argc:
                defaults = [self._stack.pop() for i in range(argc)]
                defaults.reverse()

        codeObject = tos.value
        func_decompiler = Decompiler()
        astTree = func_decompiler.run(codeObject)
        # decompiler.names.update(decompiler.names)  ???
        if codeObject.co_varnames[:1] == ('.0',):
            return astTree.tree  # generator

        argNames, varArg, kwarg = inspect.getargs(codeObject)
        args = ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg=v) for v in argNames],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=defaults,
            vararg=ast.arg(arg=varArg) if varArg else None,
            kwarg=ast.arg(arg=kwarg) if kwarg else None
        )
        return ast.Lambda(args, func_decompiler.ast)

    POP_JUMP_IF_FALSE = JUMP_IF_FALSE
    POP_JUMP_IF_TRUE = JUMP_IF_TRUE

    def POP_TOP(self):
        pass

    def RETURN_VALUE(self):
        if self.next_pos != self._end:
            raise DecompileError()
        expr = self._stack.pop()
        return _simplify(expr)

    def ROT_TWO(self):
        tos = self._stack.pop()
        tos1 = self._stack.pop()
        self._stack.append(tos)
        self._stack.append(tos1)

    def ROT_THREE(self):
        tos = self._stack.pop()
        tos1 = self._stack.pop()
        tos2 = self._stack.pop()
        self._stack.append(tos)
        self._stack.append(tos2)
        self._stack.append(tos1)

    def SETUP_LOOP(self, endpos):
        pass

    def STORE_ATTR(self, attrName):
        self._store(ast.Attribute(self._stack.pop(), attrName, ast.Store()))

    def STORE_DEREF(self, freeVar):
        self._assNames.add(freeVar)
        self._store(ast.Name(freeVar, ast.Store()))

    def STORE_FAST(self, varName):
        if varName.startswith('_['):
            raise InvalidQuery('Use generator expression (... for ... in ...) '
                               'instead of list comprehension [... for ... in ...] inside query')
        self._assNames.add(varName)
        self._store(ast.Name(varName, ast.Store()))

    def STORE_MAP(self):
        tos = self._stack.pop()
        tos1 = self._stack.pop()
        tos2 = self._stack[-1]
        if not isinstance(tos2, ast.Dict):
            assert False  # pragma: no cover
        if tos2.items == ():
            tos2.items = []
        tos2.items.append((tos, tos1))

    def STORE_SUBSCR(self):
        tos = self._stack.pop()
        tos1 = self._stack.pop()
        tos2 = self._stack.pop()
        if not isinstance(tos1, ast.Dict):
            assert False  # pragma: no cover
        if tos1.items == ():
            tos1.items = []
        tos1.items.append((tos, tos2))

    def UNARY_POSITIVE(self):
        return ast.UnaryOp(op=ast.UAdd(), operand=self._stack.pop())

    def UNARY_NEGATIVE(self):
        return ast.UnaryOp(op=ast.USub(), operand=self._stack.pop())

    def UNARY_NOT(self):
        return ast.UnaryOp(op=ast.Not(), operand=self._stack.pop())

    def UNARY_INVERT(self):
        return ast.Invert(self._stack.pop())

    def UNPACK_SEQUENCE(self, count):
        ass_tuple = ast.Assign(targets=ast.Tuple([], ast.Store()))
        ass_tuple.count = count
        return ass_tuple

    def YIELD_VALUE(self):
        expr = self._stack.pop()
        generators = []
        while self._stack:
            self._process_target(None)
            top = self._stack.pop()
            if not isinstance(top, ast.comprehension):
                cond = top
                top = self._stack.pop()
                assert isinstance(top, ast.comprehension)
                top.ifs.append(cond)
                generators.append(top)
            else:
                generators.append(top)
        generators.reverse()
        return ast.GeneratorExp(_simplify(expr), generators)


test_lines = """
    (a and b if c and d else e and f for i in T if (A and B if C and D else E and F))

    (a for b in T)
    (a for b, c in T)
    (a for b in T1 for c in T2)
    (a for b in T1 for c in T2 for d in T3)
    (a for b in T if f)
    (a for b in T if f and h)
    (a for b in T if f and h or t)
    (a for b in T if f == 5 and r or t)
    (a for b in T if f and r and t)

    # (a for b in T if f == 5 and +r or not t)
    # (a for b in T if -t and ~r or `f`)

    (a for b in T if x and not y and z)
    (a for b in T if not x and y)
    (a for b in T if not x and y and z)
    (a for b in T if not x and y or z) #FIXME!

    (a**2 for b in T if t * r > y / 3)
    (a + 2 for b in T if t + r > y // 3)
    (a[2,v] for b in T if t - r > y[3])
    ((a + 2) * 3 for b in T if t[r, e] > y[3, r * 4, t])
    (a<<2 for b in T if t>>e > r & (y & u))
    (a|b for c in T1 if t^e > r | (y & (u & (w % z))))

    ([a, b, c] for d in T)
    ([a, b, 4] for d in T if a[4, b] > b[1,v,3])
    ((a, b, c) for d in T)
    ({} for d in T)
    ({'a' : x, 'b' : y} for a, b in T)
    (({'a' : x, 'b' : y}, {'c' : x1, 'd' : 1}) for a, b, c, d in T)
    ([{'a' : x, 'b' : y}, {'c' : x1, 'd' : 1}] for a, b, c, d in T)

    (a[1:2] for b in T)
    (a[:2] for b in T)
    (a[2:] for b in T)
    (a[:] for b in T)
    (a[1:2:3] for b in T)
    (a[1:2, 3:4] for b in T)
    (a[2:4:6,6:8] for a, y in T)

    (a.b.c for d.e.f.g in T)
    # (a.b.c for d[g] in T)

    ((s,d,w) for t in T if (4 != x.a or a*3 > 20) and a * 2 < 5)
    ([s,d,w] for t in T if (4 != x.amount or amount * 3 > 20 or amount * 2 < 5) and amount*8 == 20)
    ([s,d,w] for t in T if (4 != x.a or a*3 > 20 or a*2 < 5 or 4 == 5) and a * 8 == 20)
    (s for s in T if s.a > 20 and (s.x.y == 123 or 'ABC' in s.p.q.r))
    (a for b in T1 if c > d for e in T2 if f < g)

    (func1(a, a.attr, x=123) for s in T)
    # (func1(a, a.attr, *args) for s in T)
    # (func1(a, a.attr, x=123, **kwargs) for s in T)
    (func1(a, b, a.attr1, a.b.c, x=123, y='foo') for s in T)
    # (func1(a, b, a.attr1, a.b.c, x=123, y='foo', **kwargs) for s in T)
    # (func(a, a.attr, keyarg=123) for a in T if a.method(x, *args, **kwargs) == 4)

    ((x or y) and (p or q) for a in T if (a or b) and (c or d))
    (x.y for x in T if (a and (b or (c and d))) or X)

    (a for a in T1 if a in (b for b in T2))
    (a for a in T1 if a in (b for b in T2 if b == a))

    (a for a in T1 if a in (b for b in T2))
    (a for a in T1 if a in select(b for b in T2))
    (a for a in T1 if a in (b for b in T2 if b in (c for c in T3 if c == a)))
    (a for a in T1 if a > x and a in (b for b in T1 if b < y) and a < z)
"""
# should throw InvalidQuery due to using [] inside of a query
##   (a for a in T1 if a in [b for b in T2 if b in [(c, d) for c in T3]])

# examples of conditional expressions
##    (a if b else c for x in T)
##    (x for x in T if (d if e else f))
##    (a if b else c for x in T if (d if e else f))
##    (a and b or c and d if x and y or p and q else r and n or m and k for i in T)
##    (i for i in T if (a and b or c and d if x and y or p and q else r and n or m and k))
##    (a and b or c and d if x and y or p and q else r and n or m and k for i in T if (A and B or C and D if X and Y or P and Q else R and N or M and K))


def test(test_line=None):
    import sys
    if sys.version[:3] > '2.4':
        outmost_iterable_name = '.0'
    else:
        outmost_iterable_name = '[outmost-iterable]'
    import dis
    for i, line in enumerate(test_lines.split('\n')):
        if test_line is not None and i != test_line:
            continue
        if not line or line.isspace():
            continue
        line = line.strip()
        if line.startswith('#'):
            continue

        code = compile(line, '<?>', 'eval').co_consts[0]
        ast1 = ast.parse(line).body[0]

        ast1.value.generators[0].iter.id = outmost_iterable_name
        ast1 = ast.dump(ast1)
        try:
            decompiler = Decompiler()
            astTree = decompiler.run(code)
            ast2 = ast.Expr(astTree.tree)
            ast2 = ast.dump(ast2)
        except Exception as e:
            print()
            print(i, line)
            print()
            print(ast1)
            print()
            dis.dis(code)
            raise
        if ast1 != ast2:
            print()
            print(i, line)
            print()
            print(ast1)
            print()
            print(ast2)
            print()
            dis.dis(code)
            # break
        else:
            print('%d OK: %s' % (i, line))
    else:
        print('Done!')


if __name__ == '__main__':
    test()

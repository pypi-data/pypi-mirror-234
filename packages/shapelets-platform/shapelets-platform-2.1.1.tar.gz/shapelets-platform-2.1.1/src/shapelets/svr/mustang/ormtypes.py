import types
from decimal import Decimal
from datetime import date, time, datetime, timedelta

NoneType = type(None)


class SetType(object):
    __slots__ = 'item_type'

    def __deepcopy__(self, memo):
        return self  # SetType instances are "immutable"

    def __init__(self, item_type):
        self.item_type = item_type

    def __eq__(self, other):
        return type(other) is SetType and self.item_type == other.item_type

    def __ne__(self, other):
        return type(other) is not SetType or self.item_type != other.item_type

    def __hash__(self):
        return hash(self.item_type) + 1


class FuncType(object):
    __slots__ = 'func'

    def __deepcopy__(self, memo):
        return self  # FuncType instances are "immutable"

    def __init__(self, func):
        self.func = func

    def __eq__(self, other):
        return type(other) is FuncType and self.func == other.func

    def __ne__(self, other):
        return type(other) is not FuncType or self.func != other.func

    def __hash__(self):
        return hash(self.func) + 1

    def __repr__(self):
        return 'FuncType(%s at %d)' % (self.func.__name__, id(self.func))


def deref_proxy(value):
    
    t = type(value)

    if t.__name__ == 'LocalProxy' and '_get_current_object' in t.__dict__:
        value = value._get_current_object()  # Flask local proxy
    elif t.__name__ == 'EntityProxy':
        value = value._get_object()  # Pony proxy
    elif t.__name__ == 'DataSet':
        value = iter(value)

    return value


def normalize(value):
    value = deref_proxy(value)
    t = type(value)
    if t is tuple:
        item_types, item_values = [], []
        for item in value:
            item_type, item_value = normalize(item)
            item_values.append(item_value)
            item_types.append(item_type)
        return tuple(item_types), tuple(item_values)

    if t.__name__ == 'EntityMeta':
        return SetType(value), value

    if t.__name__ == 'EntityIter':
        entity = value.entity
        return SetType(entity), entity

    if isinstance(value, str):
        return str, value

    if t in function_types:
        return FuncType(value), value

    if hasattr(value, '_get_type_'):
        return value._get_type_(), value

    return normalize_type(t), value


def normalize_type(t):
    tt = type(t)
    if tt is tuple:
        return tuple(normalize_type(item) for item in t)
    if not isinstance(t, type):
        return t
    assert t.__name__ != 'EntityMeta'
    if tt.__name__ == 'EntityMeta':
        return t
    if t is NoneType:
        return t
    t = type_normalization_dict.get(t, t)
    if t in primitive_types:
        return t
    if t in (slice, type(Ellipsis)):
        return t
    if issubclass(t, str):
        return str

    if issubclass(t, Array):
        return t

    return str


coercions = {
    (int, float): float,
    (int, Decimal): Decimal,
    (date, datetime): datetime,
    (bool, int): int,
    (bool, float): float,
    (bool, Decimal): Decimal
}
coercions.update(((t2, t1), t3) for ((t1, t2), t3) in list(coercions.items()))


def coerce_types(t1, t2):
    if t1 == t2:
        return t1
    is_set_type = False
    if type(t1) is SetType:
        is_set_type = True
        t1 = t1.item_type
    if type(t2) is SetType:
        is_set_type = True
        t2 = t2.item_type
    result = coercions.get((t1, t2))
    if result is not None and is_set_type:
        result = SetType(result)
    return result


def are_comparable_types(t1, t2, op='=='):
    # types must be normalized already!
    tt1 = type(t1)
    tt2 = type(t2)

    t12 = {t1, t2}

    if op in ('in', 'not in'):

        if tt2 is not SetType:
            return False
        op = '=='
        t2 = t2.item_type
        tt2 = type(t2)
    if op in ('is', 'is not'):
        return t1 is not None and t2 is NoneType
    if tt1 is tuple:
        if not tt2 is tuple:
            return False
        if len(t1) != len(t2):
            return False
        for item1, item2 in zip(t1, t2):
            if not are_comparable_types(item1, item2):
                return False
        return True

    if op in ('==', '<>', '!='):
        if t1 is NoneType and t2 is NoneType:
            return False
        if t1 is NoneType or t2 is NoneType:
            return True
        if t1 in primitive_types:
            if t1 is t2:
                return True
            if (t1, t2) in coercions:
                return True
            if tt1 is not type or tt2 is not type:
                return False
            if issubclass(t1, int) and issubclass(t2, str):
                return True
            if issubclass(t2, int) and issubclass(t1, str):
                return True
            return False
        if tt1.__name__ == tt2.__name__ == 'EntityMeta':
            return t1._root_ is t2._root_
        return False
    if t1 is t2 and t1 in comparable_types:
        return True
    return (t1, t2) in coercions


class Array(object):
    item_type = None  # Should be overridden in subclass

    @classmethod
    def default_empty_value(cls):
        return []


class IntArray(Array):
    item_type = int


class StrArray(Array):
    item_type = str


class FloatArray(Array):
    item_type = float


numeric_types = {bool, int, float, Decimal}
comparable_types = {int, float, Decimal, str, date, time, datetime,
                    timedelta, bool, IntArray, StrArray, FloatArray}
primitive_types = comparable_types | {bytes}
function_types = {type, types.FunctionType, types.BuiltinFunctionType}
type_normalization_dict = {}

array_types = {
    int: IntArray,
    float: FloatArray,
    str: StrArray
}

import sys
import types

from functools import wraps
from typing import Any, Dict, List, Union


def built_in(**meta):
    """ Decorator factory. """

    def variable_injector(func):
        """ Decorator. """
        func.__dbname__ = meta['db_name']
        func.__aggregated__ = meta['aggregated']

        @wraps(func)
        def decorator(*args, **kwargs):
            func.__dbname__ = meta['db_name']
            func.__aggregated__ = meta['aggregated']

            func_globals = func.__globals__

            # Save copy of any global values that will be replaced.
            saved_values = {
                key: func_globals[key]
                for key in meta
                if key in func_globals
            }

            func_globals.update(meta)
            try:
                result = func(*args, **kwargs)
            finally:
                func_globals.update(saved_values)  # Restore replaced globals.

            return result

        return decorator

    return variable_injector


###########################
## H3 Indexing Functions ##
###########################

# these two have the same function H3Cell in the backend

@built_in(db_name='h3cell', aggregated=False)
def h3Cell(lat: float, lng: float, res: int) -> int:
    """
    Computes the H3 cell number for a given WGS84 latitude and longitude pair
    """
    pass


@built_in(db_name='h3cell', aggregated=False)
def h3FromCellId(cellId: str) -> int:
    """
    Parses a canonical string representation of an H3 cell and returns 
    its numerical value.
    """
    pass


@built_in(db_name='h3lat', aggregated=False)
def h3Lat(cell: int) -> float:
    """
    Returns the WGS84 latitude of the point at the center of a H3 cell
    """
    pass


@built_in(db_name='h3lng', aggregated=False)
def h3Lng(cell: int) -> float:
    """
    Returns the WGS84 longitude of the point at the center of a H3 cell
    """
    pass

# these two have the same function h3_parent_cell function in the backend


@built_in(db_name='h3ParentCell', aggregated=False)
def h3Coarse(cell: int) -> int:
    """
    Returns the immediate parent of a H3 cell
    """
    pass


@built_in(db_name='h3ParentCell', aggregated=False)
def h3Parent(cell: int, res: int) -> int:
    """
    Returns the immediate parent of a H3 cell
    """
    pass


@built_in(db_name='h3Resolution', aggregated=False)
def h3Resolution(cell: int) -> int:
    """
    Returns the resolution of a H3 cell 
    """
    pass


@built_in(db_name='h3GridDistance', aggregated=False)
def h3GridDistance(from_cell: int, to_cell: int) -> int:
    """
    Returns the grid distance between two H3 cells
    """
    pass


@built_in(db_name='h3CellId', aggregated=False)
def h3CellId(cell: int) -> str:
    """
    Returns the canonical string representation of an H3 cell
    """
    pass


#############################
## Aggregated Computations ##
#############################

@built_in(db_name='avg', aggregated=True)
def avg(col: Union[int, float]) -> float:
    """
    Computes the arithmetic average of a column
    """
    pass


@built_in(db_name='count', aggregated=True)
def count() -> float:
    """
    Counts the number of elements in a group
    """
    pass


@built_in(db_name='favg', aggregated=True)
def kahanAvg(col: Union[int, float]) -> float:
    """
    Computes the arithmetic average of a column, using 
    Kahan sum for improved accuracy.
    """
    pass


@built_in(db_name='fsum', aggregated=True)
def kahanSum(col: Union[int, float]) -> float:
    """
    Computes the sum of a column, using Kahan algorithm
    for improved accuracy.
    """
    pass


@built_in(db_name='first', aggregated=True)
def first(col: Any) -> Any:
    """
    Returns the first element found whilst computing 
    a group by aggregation.
    """
    pass


@built_in(db_name='histogram', aggregated=True)
def histogram(col: Any) -> Dict[Any, int]:
    """
    Computes a basic histogram of the values stored in a column 
    """
    pass


@built_in(db_name='last', aggregated=True)
def last(col: Any) -> Any:
    """
    Returns the first element found whilst computing 
    a group by aggregation.
    """
    pass


@built_in(db_name='list', aggregated=True)
def listAgg(col: Any) -> List[Any]:
    """
    Returns a list with all values of a column
    """
    pass


@built_in(db_name='max', aggregated=True)
def max(col: Any) -> Any:
    """
    Returns the maximum value found in a column during an aggregation
    """
    pass


@built_in(db_name='min', aggregated=True)
def min(col: Any) -> Any:
    """
    Returns the minimum value found in a column during an aggregation
    """
    pass


@built_in(db_name='product', aggregated=True)
def prod(col: Union[float, int]) -> float:
    """
    Computes the product of all values stored in a column 
    """
    pass


@built_in(db_name='group_concat', aggregated=True)
def join(col: str, sep: str) -> str:
    """
    Concatenates all string values using a separator between values
    """
    pass


@built_in(db_name='sum', aggregated=True)
def sum() -> float:
    """
    Computes the sum of a column.
    """
    pass


###########################
## Statistical Functions ##
###########################


@built_in(db_name='corr', aggregated=True)
def corr(y: Union[int, float], x: Union[int, float]) -> float:
    """
    Returns the correlation coefficient between two columns.
    """
    pass


@built_in(db_name='covar_pop', aggregated=True)
def covarp(y: Union[int, float], x: Union[int, float]) -> float:
    """
    Returns the population covariance of input values
    """
    pass


@built_in(db_name='entropy', aggregated=True)
def entropy(x: Any) -> float:
    """
    Returns the log-2 entropy of count input-values.
    """
    pass


@built_in(db_name='kurtosis', aggregated=True)
def kurtosis(x: Union[int, float]) -> float:
    """
    Returns the excess kurtosis of all input values.
    """
    pass


@built_in(db_name='mad', aggregated=True)
def mad(x: Union[int, float]) -> float:
    """
    Returns the median absolute deviation for the values within x.
    """
    pass


@built_in(db_name='median', aggregated=True)
def median(x: Any) -> Any:
    """
    Returns the middle value of the set. NULL values are ignored.
    """
    pass


@built_in(db_name='mode', aggregated=True)
def mode(x: Any) -> Any:
    """
    Returns the most frequent value for the values within x.
    """
    pass


@built_in(db_name='quantile', aggregated=True)
def quantile(x: Any, q: float) -> Any:
    """
    Returns the exact quantile number between 0 and 1
    """
    pass


@built_in(db_name='skewness', aggregated=True)
def skewness(x: Union[int, float]) -> float:
    """
    Returns the skewness of all values in a group
    """
    pass


@built_in(db_name='stddev_pop', aggregated=True)
def stddevp() -> float:
    """
    Returns the population standard deviation.
    """
    pass


@built_in(db_name='stddev_samp', aggregated=True)
def stddevs() -> float:
    """
    Returns the sample standard deviation.
    """
    pass


@built_in(db_name='var_pop', aggregated=True)
def varp() -> float:
    """
    Returns the population variance.
    """
    pass


@built_in(db_name='var_samp', aggregated=True)
def vars() -> float:
    """
    Returns the sample variance of all input values.
    """
    pass

#########################
## Numerical Functions ##
#########################


@built_in(db_name='abs', aggregated=False)
def abs(col: Union[int, float]) -> Union[int, float]:
    """
    Computes the absolute value
    """
    pass


@built_in(db_name='acos', aggregated=False)
def acos(col: Union[int, float]) -> float:
    """
    Computes the arc cosine
    """
    pass


@built_in(db_name='asin', aggregated=False)
def asin(col: Union[int, float]) -> float:
    """
    Computes the arc sin
    """
    pass


@built_in(db_name='atan', aggregated=False)
def atan(col: Union[int, float]) -> float:
    """
    Computes the arc tangent
    """
    pass


@built_in(db_name='atan2', aggregated=False)
def atan2(col_x: Union[int, float], col_y: Union[int, float]) -> float:
    """
    Computes the arc tangent between two values
    """
    pass


@built_in(db_name='cbrt', aggregated=False)
def cbrt(col: Union[int, float]) -> float:
    """
    Computes the cubic root
    """
    pass


@built_in(db_name='ceil', aggregated=False)
def ceil(col: Union[int, float]) -> float:
    """
    Rounds the number up
    """
    pass


@built_in(db_name='chr', aggregated=False)
def chr(col: int) -> str:
    """
    Returns the character corresponding to an ascii code.
    """
    pass


@built_in(db_name='cos', aggregated=False)
def cos(col: Union[int, float]) -> float:
    """
    Computes the cosine 
    """
    pass


@built_in(db_name='cot', aggregated=False)
def cot(col: Union[int, float]) -> float:
    """
    Computes the cotangent
    """
    pass


@built_in(db_name='degrees', aggregated=False)
def deg(col: Union[int, float]) -> float:
    """
    Converts radians to degrees
    """
    pass


@built_in(db_name='even', aggregated=False)
def even(col: Union[int, float]) -> float:
    """
    Returns to next even number by rounding away from zero.
    """
    pass


@built_in(db_name='factorial', aggregated=False)
def factorial(col: int) -> int:
    """
    Computes the factorial.
    """
    pass


@built_in(db_name='floor', aggregated=False)
def floor(col: Union[int, float]) -> float:
    """
    Rounds a number down.
    """
    pass


@built_in(db_name='gamma', aggregated=False)
def gamma(col: Union[int, float]) -> float:
    """
    Gamma function.
    """
    pass


@built_in(db_name='isfinite', aggregated=False)
def isFinite(col: float) -> bool:
    """
    Return a boolean flag indicating if a value is finite.
    """
    pass


@built_in(db_name='isinf', aggregated=False)
def isInf(col: float) -> bool:
    """
    Return a boolean flag indicating if a value is a representation of infinite
    """
    pass


@built_in(db_name='isnan', aggregated=False)
def isNaN(col: float) -> bool:
    """
    Return a flag indicating a number should be considered as NaN
    """
    pass


@built_in(db_name='lgamma', aggregated=False)
def lgamma(col: float) -> float:
    """
    Computes the logarithm of the gamma function.
    """
    pass


@built_in(db_name='ln', aggregated=False)
def ln(col: float) -> float:
    """
    Computes the natural logarithm.
    """
    pass


@built_in(db_name='log', aggregated=False)
def log(col: float) -> float:
    """
    Computes the base 10 logarithm.
    """
    pass


@built_in(db_name='log2', aggregated=False)
def log2(col: float) -> float:
    """
    Computes the base 2 logarithm.
    """
    pass


@built_in(db_name='pi', aggregated=False)
def pi() -> float:
    """ 
    Returns the number pi
    """
    pass


@built_in(db_name='pow', aggregated=False)
def pow(col_x: Union[int, float], col_y: Union[int, float]) -> float:
    """
    Returns x to the power of y
    """
    pass


@built_in(db_name='radians', aggregated=False)
def radians(col: float) -> float:
    """
    Converts degrees to radians
    """
    pass


@built_in(db_name='round', aggregated=False)
def round(col: float, dec_places: int) -> float:
    """
    Rounds a number to a fixed number of decimal places
    """
    pass


@built_in(db_name='sin', aggregated=False)
def sin(col: Union[float, int]) -> float:
    """
    Computes the sin function
    """
    pass


@built_in(db_name='sign', aggregated=False)
def sign(col: Union[float, int]) -> int:
    """
    Returns -1 if the value is native; 0 if the value is 0 and +1 in 
    any other case
    """
    pass


@built_in(db_name='sqrt', aggregated=False)
def sqrt(col: Union[float, int]) -> float:
    """
    Computes the squared root of a number 
    """
    pass


@built_in(db_name='tab', aggregated=False)
def tan(col: Union[float, int]) -> float:
    """
    Computes the tangent
    """
    pass

######################
## String Functions ##
######################

###
#
# String Distances


@built_in(db_name='lower', aggregated=False)
def levenshtein(a: str, b: str) -> float:
    pass


@built_in(db_name='jaccard', aggregated=False)
def jaccard(a: str, b: str) -> float:
    pass


@built_in(db_name='hamming', aggregated=False)
def hamming(a: str, b: str) -> float:
    pass

###
#
# Code-Like functions


@built_in(db_name='ascii', aggregated=False)
def ascii(col: str) -> int:
    pass


@built_in(db_name='md5', aggregated=False)
def md5(col: str) -> str:
    pass


@built_in(db_name='unicode', aggregated=False)
def unicode(val: str) -> int:
    pass


@built_in(db_name='base64', aggregated=False)
def base64(val: bytes) -> str:
    pass

###
#
# Upper and Lower


@built_in(db_name='lower', aggregated=False)
def lower(col: str) -> str:
    pass


@built_in(db_name='upper', aggregated=False)
def upper(col: str) -> str:
    pass

###
#
# Pad and Trim


@built_in(db_name='rpad', aggregated=False)
def padRight(val: str, count: int, char: str) -> str:
    pass


@built_in(db_name='lpad', aggregated=False)
def padLeft(val: str, count: int, char: str) -> str:
    pass


@built_in(db_name='rtrim', aggregated=False)
def trimRight(val: str) -> str:
    pass


@built_in(db_name='ltrim', aggregated=False)
def trimLeft(val: str) -> str:
    pass


@built_in(db_name='trim', aggregated=False)
def trim(val: str) -> str:
    pass


###
#
# Sub-String like

@built_in(db_name='substr', aggregated=False)
def substr(val: str, start: int, end: int) -> str:
    pass


@built_in(db_name='suffix', aggregated=False)
def endsWith(val: str, suffix: str) -> bool:
    pass


@built_in(db_name='prefix', aggregated=False)
def startsWith(val: str, prefix: str) -> bool:
    pass


@built_in(db_name='instr', aggregated=False)
def indexOf(val: str, chars: str) -> int:
    pass

###
#
# General


@built_in(db_name='replace', aggregated=False)
def replace(val: str, what: str, new: str) -> str:
    pass


@built_in(db_name='reverse', aggregated=False)
def reverse(val: str) -> str:
    pass


@built_in(db_name='strlen', aggregated=False)
def strlen(val: str) -> int:
    pass


###########################
## Date / Time Functions ##
###########################


@built_in(db_name='day', aggregated=False)
def day() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass


@built_in(db_name='month', aggregated=False)
def month() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass


@built_in(db_name='year', aggregated=False)
def year() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass


@built_in(db_name='hour', aggregated=False)
def hour() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass


@built_in(db_name='minute', aggregated=False)
def minute() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass


@built_in(db_name='second', aggregated=False)
def second() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass


@built_in(db_name='getDate', aggregated=False)
def getDate() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass


@built_in(db_name='getTime', aggregated=False)
def getTime() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass


@built_in(db_name='hamming', aggregated=False)
def hamming() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    pass


@built_in(db_name='floor', aggregated=False)
def floor() -> int:
    """_summary_

    Returns:
        int: _description_
    """
    pass


@built_in(db_name='ceil', aggregated=False)
def ceil() -> int:
    """_summary_

    Returns:
        int: _description_
    """
    pass

###############
## J O I N S ##
###############

@built_in(db_name='left', aggregated=True)
def left() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass


@built_in(db_name='right', aggregated=True)
def right() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass

@built_in(db_name='full', aggregated=True)
def full() -> float:
    """_summary_

    Returns:
        float: _description_
    """
    pass

this_module = sys.modules[__name__]

func_list = [
    getattr(this_module, a)
    for a in dir(this_module)
    if isinstance(getattr(this_module, a), types.FunctionType)
]

allowedFunctionList = [
    item.__name__
    for item in func_list
    if (item.__name__ != 'built_in' and item.__name__ != 'wraps')
]

realFunctionList = [
    item.__dbname__
    for item in func_list
    if (item.__name__ != 'built_in' and item.__name__ != 'wraps')
]

zip_iterator = zip(allowedFunctionList, realFunctionList)
function_dictionary = dict(zip_iterator)

aggregatedFunctionList = [
    (item.__dbname__, item.__aggregated__)
    for item in func_list
    if (item.__name__ != 'built_in' and item.__name__ != 'wraps')]

aggregatedFunctionList = [f[0] for f in aggregatedFunctionList if f[1]]


def checkAggregatedFunctionProtoype(key):
    for key in function_dictionary:
        if (function_dictionary[key] in aggregatedFunctionList):
            return True
        else:
            pass
    return False


__all__ = [
    'h3Cell', 'h3FromCellId', 'h3Lat', 'h3Lng', 'h3Coarse', 'h3Parent',
    'h3Resolution', 'h3GridDistance', 'h3CellId', 'avg', 'count',
    'kahanAvg', 'kahanSum', 'first', 'histogram', 'last', 'listAgg', 'max',
    'min', 'prod', 'join', 'sum', 'corr', 'covarp', 'entropy', 'kurtosis', 'mad',
    'median', 'mode', 'quantile', 'skewness', 'stddevp', 'stddevs', 'varp',
    'vars', 'abs', 'acos', 'asin', 'atan', 'atan2', 'cbrt', 'ceil', 'chr', 'cos',
    'cot', 'deg', 'even', 'factorial', 'floor', 'gamma', 'isFinite', 'isInf',
    'isNaN', 'lgamma', 'ln', 'log', 'log2', 'pi', 'pow', 'radians', 'round', 'sin',
    'sign', 'sqrt', 'tan', 'lower', 'upper', 'day', 'month', 'year', 'hour',
    'minute', 'second', 'getDate', 'getTime', 'left', 'right', 'checkAggregatedFunctionProtoype',
    'hamming', 'floor', 'ceil','full'
]

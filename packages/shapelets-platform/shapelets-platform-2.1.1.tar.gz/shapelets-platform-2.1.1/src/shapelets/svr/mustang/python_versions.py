import platform
import sys

PYPY = platform.python_implementation() == "PyPy"
PY36 = sys.version_info >= (3, 6)
PY37 = sys.version_info[:2] >= (3, 7)
PY38 = sys.version_info[:2] >= (3, 8)
PY39 = sys.version_info[:2] >= (3, 9)
PY310 = sys.version_info[:2] >= (3, 10)


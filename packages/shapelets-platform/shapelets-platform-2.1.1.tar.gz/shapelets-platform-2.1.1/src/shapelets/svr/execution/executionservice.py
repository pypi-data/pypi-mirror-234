import base64
import dill
import pyarrow as pa
import os
import zlib

from typing import Any

from .iexecutionrepo import IExecutionRepo
from .iexecutionservice import IExecutionService

from ..model.function import FunctionProfile

SH_DIR = os.path.expanduser('~/.shapelets')
DATA_DIR = os.path.join(SH_DIR, 'data')


def _read_from_arrow_file(file_name: str, from_row: int = 0, n: int = 10) -> str:
    path = os.path.join(DATA_DIR, file_name)
    with open(path, "rb") as file:
        reader = pa.ipc.open_file(file)
        table = reader.read_all()
    return _serialize_table(table.slice(from_row, n))


def _serialize_table(table: pa.Table):
    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchFileWriter(sink, table.schema) as writer:
        writer.write(table)
    buffer = sink.getvalue()
    return base64.b64encode(buffer).decode("utf-8")


class ExecutionService(IExecutionService):
    __slots__ = ('_execution_repo',)

    def __init__(self, execution_repo: IExecutionRepo) -> None:
        self._execution_repo = execution_repo

    def execute_function(self, fn: FunctionProfile) -> Any:
        # Function is saved in .shapelets/data
        with open(os.path.join(DATA_DIR, fn.body), 'r') as f:
            lines = f.read()
        # In addition, fn body is serialized and compressed with zlib
        bytes_from_str = base64.decodebytes(bytes(lines, encoding="utf-8"))
        decompress = zlib.decompress(bytes_from_str)
        callable_fn = dill.loads(decompress)
        arg_values = []
        for arg in fn.parameters:
            if arg.get('pickled'):
                arg_values.append(dill.loads(base64.decodebytes(bytes(arg.get('value'), encoding="utf-8"))))
            else:
                # Value was not serialized
                arg_values.append(arg.get('value'))
        result = callable_fn(*arg_values)
        if hasattr(result, "parent_data_app") and result.parent_data_app._data:
            # if there are files associated with the dataApp, save them.
            current_file = fn.body
            self._execution_repo.add_files(current_file, result.parent_data_app._data)
        return result

    def table_data(self, table: str, from_row: int, n: int) -> str:
        return _read_from_arrow_file(table, from_row, n)

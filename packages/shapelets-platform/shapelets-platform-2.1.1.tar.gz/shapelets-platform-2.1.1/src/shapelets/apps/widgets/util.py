import base64
import numpy as np
import pandas as pd
import pyarrow as pa
import os

from typing import Union

from ... import DataSet

SH_DIR = os.path.expanduser('~/.shapelets')
DATA_DIR = os.path.join(SH_DIR, 'data')


def _to_utf64_arrow_buffer(data: Union[pd.DataFrame, DataSet], preserve_index: bool = True) -> str:
    """
    Transform pandas dataframe or Shapelets dataset to an arrow buffer
    """
    if isinstance(data, pd.DataFrame):
        # df = dataframe.astype(float)
        table = pa.Table.from_pandas(data, preserve_index=preserve_index)
    elif isinstance(data, DataSet):
        table = data.to_arrow_table(1024)

    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchFileWriter(sink, table.schema) as writer:
        writer.write(table)
    buffer = sink.getvalue()
    return base64.b64encode(buffer).decode("utf-8")


def _to_utf64_arrow_buffer_numpy(array: np.ndarray) -> str:
    parray = pa.array(array.flatten())
    batch = pa.record_batch([parray], names=["values"])
    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchFileWriter(sink, batch.schema) as writer:
        writer.write(batch)
    buffer = sink.getvalue()
    return base64.b64encode(buffer).decode("utf-8")


def _to_utf64_arrow_buffer_series(series: pd.Series) -> str:
    parray = pa.Array.from_pandas(series)
    batch = pa.record_batch([parray], names=["values"])
    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchFileWriter(sink, batch.schema) as writer:
        writer.write(batch)
    buffer = sink.getvalue()
    return base64.b64encode(buffer).decode("utf-8")


def _write_arrow_file(data: Union[pd.DataFrame, DataSet], uid: str, preserve_index: bool = False):
    if isinstance(data, pd.DataFrame):
        table = pa.Table.from_pandas(data, preserve_index=preserve_index)
    elif isinstance(data, DataSet):
        table = data.to_arrow_table(1024)
    elif isinstance(data, pd.Series):
        arrow_array = pa.array(data)
        table = pa.Table.from_arrays([arrow_array], names=[data.name])

    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, uid)

    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchFileWriter(sink, table.schema) as writer:
        writer.write(table)
    buffer = sink.getvalue()
    with open(path, 'wb') as sink:
        sink.write(buffer)


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

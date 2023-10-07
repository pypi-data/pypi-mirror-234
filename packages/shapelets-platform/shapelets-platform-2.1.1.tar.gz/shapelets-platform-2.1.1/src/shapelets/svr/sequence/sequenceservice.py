import base64
import dill
import pyarrow as pa
import os
import shapelets_native as sn

from typing import Dict, List, Tuple

from .isequencerepo import ISequenceRepo
from .isequenceservice import ISequenceService

from ..model.sequence import LevelsMetadata, SequenceProfile

SH_DIR = os.path.expanduser('~/.shapelets')
DATA_DIR = os.path.join(SH_DIR, 'data')

"""
TODO
- Clean up
- Attach sequence to dataApp and make sure is delete. DONE
- Check linechart title in UI
- Check how linechart data is generated to avoid taking so long. DONE
- Check behaviour with multiline-chart
- Create sequence in server, not in client DONE
"""


def _read_arrow_file_with_offsets(seq_id: str, offsets: List[int]) -> str:
    """
    Giving the offsets of the requested levels and blocks, provide with a table where each batch is the data for the giving
    offset. This table is serialized and sent as string.
    """
    try:
        if offsets is None:
            return None
        path = os.path.join(DATA_DIR, f"{seq_id}-levels")
        batches = []
        with open(path, "rb") as file:
            reader = pa.ipc.open_file(file)
            for i in offsets:
                batches.append(reader.get_batch(i))
        table = pa.Table.from_batches(batches)
        return _serialize_table(table)
    except Exception as e:
        print(e)


def _serialize_table(table: pa.Table):
    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchFileWriter(sink, table.schema) as writer:
        writer.write(table)
    buffer = sink.getvalue()
    return base64.b64encode(buffer).decode("utf-8")


def _arrow_block(levels: List[List[Tuple[int, int]]], level: int, block: int) -> int:
    """
    Giving a level and a block, calculate the arrow block, or offset, of the giving level and block.
    """
    offset = sum(len(levels[i]) for i in range(level))
    return offset + block


def _generate_levels(x: List[float], y: List[float], n_points: int = 256):
    """
    Calculate levels and blocks.
    By default, size_in_bytes is 4096, bytes_per_row are 16. 4096/16 = 256
    """
    return sn.computeLevels(x, y, n_points)


def _save_levels(seq_id: str, levels: List[List[Tuple[float, float]]]):
    """
    Save levels in Arrow file. Levels are saved as batches.
    """
    dict_data = [{'x': item[0], 'y': item[1]} for sublist in levels for item in sublist]
    writer = None
    path = os.path.join(DATA_DIR, f"{seq_id}-levels")
    if dict_data:
        for batch in dict_data:
            py_batch = pa.RecordBatch.from_pydict(batch)
            if writer is None:
                # Create the writer for the first batch
                writer = pa.RecordBatchFileWriter(path, py_batch.schema)
            writer.write_batch(py_batch)
        writer.close()
    else:
        # Create empty file to avoid errors.
        with open(path, 'w') as fp:
            pass


def _read_full_from_arrow_file(sequence_id: str) -> pa.Table:
    """
    Read arrow file as pyarrow Table
    """
    path = os.path.join(DATA_DIR, sequence_id)
    with open(path, "rb") as file:
        reader = pa.ipc.open_file(file)
        table = reader.read_all()
    return table


def levels_full_fn(sequence_id: str, starts: int, every: int) -> Tuple:
    arrow_data = _read_full_from_arrow_file(sequence_id)
    col_names = arrow_data.column_names

    # Extract y and x
    y_axis = arrow_data.to_pydict()[col_names[0]]
    # Remove those points where Nans exists.
    none_indices = [index for index, value in enumerate(y_axis) if value is None]
    y_axis = [value for index, value in enumerate(y_axis) if index not in none_indices]
    x_axis = [starts + (every * x) for x in range(0, len(y_axis))]
    # Generate levels
    levels = _generate_levels(x_axis, y_axis)
    # Save levels in Arrow batch
    _save_levels(sequence_id, levels)

    # Count items per block
    levels_count = []
    for level in levels:
        blocks = []
        for block in level:
            blocks.append(len(block[0]))
        levels_count.append(blocks)
    # Save levels count as serialized string
    levels_count_ser = base64.b64encode(dill.dumps(levels_count, recurse=True)).decode('utf-8')
    return levels, levels_count_ser


class SequenceService(ISequenceService):
    __slots__ = ('_sequence_repo',)

    def __init__(self, sequence_repo: ISequenceRepo) -> None:
        self._sequence_repo = sequence_repo

    def create_sequence(self, sequence: SequenceProfile):
        self._sequence_repo.create_sequence(sequence)

    def get_sequence(self, sequence_id: str) -> SequenceProfile:
        return self._sequence_repo.get_sequence(sequence_id)

    def get_levels_blocks(self, sequence_id: str) -> LevelsMetadata:
        return self._sequence_repo.get_levels_blocks(sequence_id)

    def get_visualization(self, sequence_id: str, level_blocks: List[Dict[str, str]]) -> str:
        """
        Giving a list of levels and blocks, return the visualization as serialized string.
        levels_blocks is a list of dicts with the structure {level: 1, block: 4}
        """
        levels_metadata = self.get_levels_blocks(sequence_id)

        offsets = []
        for item in level_blocks:
            level = item["level"]
            block = item["block"]
            offsets.append(_arrow_block(levels_metadata.levels, level, block))

        result = _read_arrow_file_with_offsets(sequence_id, offsets)
        return result

    async def generate_levels(self, sequence_id: str):
        # Get sequence information
        sequence_info = self._sequence_repo.get_sequence(sequence_id)
        levels, levels_count_ser = levels_full_fn(sequence_id, sequence_info.axisInfo.starts,
                                                  sequence_info.axisInfo.every)
        # Update sequence information
        self._sequence_repo.save_levels_info(sequence_id, len(levels), levels_count_ser)

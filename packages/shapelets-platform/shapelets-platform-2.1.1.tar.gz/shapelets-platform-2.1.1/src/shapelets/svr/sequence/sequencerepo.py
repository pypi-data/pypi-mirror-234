import base64
import dill

from .isequencerepo import ISequenceRepo

from ..model import AxisInfo, LevelsMetadata, SequenceProfile, VisualizationInfo
from ..db import Connection, transaction


def insert_sequence(sequence: SequenceProfile, conn: Connection):
    """
    Insert sequence info in database
    """
    conn.execute("""
            INSERT INTO sequences 
            (id, name, length, starts, every, ends, axis_type, number_of_levels, chunk_size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
                 [
                     sequence.id, sequence.name, sequence.length, sequence.axisInfo.starts, sequence.axisInfo.every,
                     sequence.axisInfo.ends, sequence.axisInfo.type, sequence.visualizationInfo.numberOfLevels,
                     sequence.visualizationInfo.chunkSize
                 ])


def _load_sequence(sequence_id: str, conn: Connection):
    """
    Load sequence data using sequence ID
    """

    conn.execute(""" 
        SELECT id, name, length, starts, every, ends, axis_type, number_of_levels, chunk_size
        FROM sequences
        WHERE id = ?;
    """, [sequence_id])

    record = conn.fetch_one()
    if record is None:
        return None

    return SequenceProfile(
        id=record[0],
        name=record[1],
        length=record[3],
        axisInfo=AxisInfo(starts=record[3], every=record[4], ends=record[5], type=record[6]),
        visualizationInfo=VisualizationInfo(numberOfLevels=record[7], chunkSize=record[8]))


def _load_levels_blocks(sequence_id, conn) -> LevelsMetadata:
    """
    Load Levels Metadata Message
    """
    conn.execute(""" 
        SELECT chunk_size, elements_per_block
        FROM sequences
        WHERE id = ?;
    """, [sequence_id])

    record = conn.fetch_one()
    if record is None:
        return None
    # elements_per_block are serialized.
    bytes_from_str = base64.decodebytes(bytes(record[1], encoding="utf-8"))
    levels_count = dill.loads(bytes_from_str)
    return LevelsMetadata(levels=levels_count, chunkSize=record[0])


def update_levels_info(sequence_id: str, levels_length: int, elements_per_block: str, conn: Connection):
    """
    Update sequence with its level information.
    param levels_length is the amount of level the sequence has.
    param elements_per_block is a List[List[int]] where each list represents a level and each element inside represents
    the count of that block. This list is serialized and save in database as a string.
    """

    conn.execute(""" 
        UPDATE sequences 
        SET number_of_levels = ?, elements_per_block = ?
        WHERE id = ? ;
    """, [levels_length, elements_per_block, sequence_id])


class SequenceRepo(ISequenceRepo):

    def create_sequence(self, sequence: SequenceProfile):
        with transaction() as conn:
            insert_sequence(sequence, conn)

    def get_sequence(self, sequence_id: str) -> SequenceProfile:
        with transaction() as conn:
            return _load_sequence(sequence_id, conn)

    def get_levels_blocks(self, sequence_id: str) -> LevelsMetadata:
        with transaction() as conn:
            return _load_levels_blocks(sequence_id, conn)

    def save_levels_info(self, sequence_id: str, levels_length: int, elements_per_block: str):
        with transaction() as conn:
            return update_levels_info(sequence_id, levels_length, elements_per_block, conn)

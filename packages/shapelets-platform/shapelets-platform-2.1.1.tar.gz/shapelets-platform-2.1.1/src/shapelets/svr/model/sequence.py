from pydantic import BaseModel
from typing import List, Optional, Set
from typing_extensions import Literal

SequenceField = Literal['id', 'length', 'starts', 'every', 'ends', 'axisType', 'number_of_levels', 'chunk_size',]
SequenceAllFields: Set[SequenceField] = set(
    ['id', 'length', 'starts', 'every', 'ends', 'axisType', 'number_of_levels', 'chunk_size'])


class VisualizationInfo(BaseModel):
    numberOfLevels: Optional[int] = None
    chunkSize: int


class AxisInfo(BaseModel):
    starts: int
    every: int
    ends: int
    type: str


class SequenceAttributes(BaseModel):
    name: Optional[str] = None
    length: int
    axisInfo: AxisInfo
    visualizationInfo: VisualizationInfo


class SequenceProfile(SequenceAttributes):
    id: str


class LevelsMetadata(BaseModel):
    """
    Levels Metadata.
    Param levels is a List[List[int]] where each list represents a level and each element inside represents
    the count of elements in that block. This list is serialized and save in database as a string.
    """
    levels: List[List[int]]
    chunkSize: int

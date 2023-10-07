from abc import ABC, abstractmethod
from ..model.sequence import LevelsMetadata, SequenceProfile


class ISequenceRepo(ABC):
    @abstractmethod
    def create_sequence(self, sequence: SequenceProfile):
        pass

    @abstractmethod
    def get_sequence(self, sequence_id: str) -> SequenceProfile:
        pass

    @abstractmethod
    def get_levels_blocks(self, sequence_id: str) -> LevelsMetadata:
        pass

    @abstractmethod
    def save_levels_info(self, sequence_id: str, levels_length: int, elements_per_block: str):
        """
        Once the levels have been generated, we need to update the sequence in database with the length of the levels,
        and the count of elements per block, a List[List[int]] serialized.
        """
        pass

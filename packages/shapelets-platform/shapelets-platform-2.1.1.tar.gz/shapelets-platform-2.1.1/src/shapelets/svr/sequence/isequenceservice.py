from abc import ABC, abstractmethod

from ..model.sequence import LevelsMetadata, SequenceProfile


class ISequenceService(ABC):
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
    def get_visualization(self, sequence_id: str, level_blocks) -> str:
        pass

    @abstractmethod
    async def generate_levels(self, sequence_id: str):
        pass

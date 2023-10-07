from abc import ABC, abstractmethod
from typing import Any

from ..model.function import FunctionProfile


class IExecutionService(ABC):
    @abstractmethod
    def execute_function(self, fn: FunctionProfile) -> Any:
        pass

    @abstractmethod
    def table_data(self, table: str, from_row: int, to_row: int) -> str:
        pass

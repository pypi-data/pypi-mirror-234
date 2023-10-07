# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABC, abstractmethod
from typing import List


class IExecutionRepo(ABC):
    @abstractmethod
    def execute_function(self, fn: str):
        pass

    @abstractmethod
    def add_files(self, current_fn_id: str, new_ids: List[str] ):
        pass



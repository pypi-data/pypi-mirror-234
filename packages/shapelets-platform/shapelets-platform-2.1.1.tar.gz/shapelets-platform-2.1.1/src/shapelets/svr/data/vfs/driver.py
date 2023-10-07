
from abc import ABC, abstractmethod
from pydantic import Field
from typing import TypeVar, Dict, Union, Any, Generic
# from typing_extensions import Protocol, runtime_checkable

from .dynamic_credentials import MissingUserData, RequiredToken
from .protocols import FSSpecProvider

S = TypeVar('S')


class Driver(Generic[S]):

    @abstractmethod
    def available(self) -> bool:
        pass

    @abstractmethod
    def accept(self, configuration: Any):
        pass

    @abstractmethod
    def has_full_credentials(self, cfg: S) -> bool:
        pass

    @abstractmethod
    def resolve_credentials(self, cfg: S, prefix: str, user_data: Dict[str, str]) -> Union[S, MissingUserData, RequiredToken]:
        pass

    @abstractmethod
    def create(self, cfg: S) -> FSSpecProvider:
        pass

import os

from typing import Union, Dict, Any
from typing_extensions import Literal

from pydantic import BaseModel

from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from fsspec.implementations.dirfs import DirFileSystem

from .driver import Driver
from .dynamic_credentials import MissingUserData, RequiredToken
from .protocols import FSSpecProvider


class LocalVirtualFS(BaseModel):
    mount_as: str
    root: str
    auto_mkdir: bool = True
    kind: Literal['localfs'] = 'localfs'


class LocalProvider:
    def __init__(self, cfg: LocalVirtualFS) -> None:
        self.__cfg = cfg

    @property
    def name(self) -> str:
        return self.__cfg.mount_as

    @property
    def vfs(self) -> LocalVirtualFS:
        return self.__cfg

    def create(self, cache_root: str, **kwargs) -> AbstractFileSystem:
        local_fs = LocalFileSystem(self.__cfg.auto_mkdir, **kwargs)  # , skip_instance_cache=True
        checked_root = os.path.expanduser(self.__cfg.root)
        checked_root = os.path.expandvars(checked_root)
        os.makedirs(checked_root, exist_ok=True)
        return DirFileSystem(str(checked_root), local_fs)


class LocalDriver(Driver[LocalVirtualFS]):

    def available(self) -> bool:
        return True

    def accept(self, configuration: Any):
        return isinstance(configuration, LocalVirtualFS)

    def has_full_credentials(self, cfg: LocalVirtualFS) -> bool:
        return True

    def resolve_credentials(self, cfg: LocalVirtualFS, prefix: str, user_data: Dict[str, str]) -> Union[LocalVirtualFS, MissingUserData, RequiredToken]:
        return cfg

    def create(self, cfg: LocalVirtualFS) -> FSSpecProvider:
        if not self.has_full_credentials(cfg):
            raise ValueError("Missing credentials!")

        return LocalProvider(cfg)

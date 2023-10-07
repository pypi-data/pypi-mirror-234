from __future__ import annotations

import os

from typing import Union, Dict, Optional, Any
from typing_extensions import Literal

from pydantic import BaseModel

from fsspec import AbstractFileSystem
from fsspec.implementations.ftp import FTPFileSystem
from fsspec.implementations.cached import CachingFileSystem

from .driver import Driver
from .dynamic_credentials import MissingUserData, RequiredToken, complete_settings
from .protocols import FSSpecProvider


class FtpCredentials(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    account: Optional[str] = None

    def resolve(self, prefix: str, user_data: Dict[str, str]) -> Union[FtpCredentials, MissingUserData]:
        cfg, missing_fields = complete_settings(self, prefix, user_data)
        if len(missing_fields) > 0:
            return MissingUserData(env_prefix=prefix, fields=missing_fields)
        return cfg


class FtpVirtualFS(BaseModel):
    mount_as: str
    host: str
    port: int = 21
    credentials: Optional[FtpCredentials] = None
    kind: Literal['ftp'] = 'ftp'


class FtpProvider:
    def __init__(self, cfg: FtpVirtualFS) -> None:
        self.__cfg = cfg

    @property
    def name(self) -> str:
        return self.__cfg.mount_as

    @property
    def vfs(self) -> FtpVirtualFS:
        return self.__cfg

    def create(self, cache_root: str, **kwargs) -> AbstractFileSystem:
        credentials = {} if self.__cfg.credentials is None else self.__cfg.credentials.dict()
        base = FTPFileSystem(self.__cfg.host, self.__cfg.port, **credentials, **kwargs)
        cache_storage = os.path.join(cache_root, self.__cfg.mount_as)
        os.makedirs(cache_storage, exist_ok=True)

        return CachingFileSystem(fs=base, cache_storage=cache_storage, compression=None)


class FtpDriver(Driver[FtpVirtualFS]):

    def available(self) -> bool:
        return True

    def accept(self, configuration: Any):
        return isinstance(configuration, FtpVirtualFS)

    def has_full_credentials(self, cfg: FtpVirtualFS) -> bool:
        cred = cfg.credentials
        if cred is None:
            return True

        return not (cred.username is None or cred.password is None)

    def resolve_credentials(self, cfg: FtpVirtualFS, prefix: str, user_data: Dict[str, str]) -> Union[FtpVirtualFS, MissingUserData, RequiredToken]:
        if cfg.credentials is None:
            return cfg

        new_cfg = cfg.credentials.resolve(prefix, user_data)
        if isinstance(new_cfg, (MissingUserData, RequiredToken)):
            return new_cfg
        return cfg.copy(update={'credentials': new_cfg})

    def create(self, cfg: FtpVirtualFS) -> FSSpecProvider:
        if not self.has_full_credentials(cfg):
            raise ValueError("Missing credentials!")

        return FtpProvider(cfg)

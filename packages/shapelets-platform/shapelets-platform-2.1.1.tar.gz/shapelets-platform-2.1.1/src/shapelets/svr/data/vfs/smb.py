from __future__ import annotations

import os

from typing import Union, Dict, Any, Optional
from typing_extensions import Literal
from warnings import warn

from pydantic import BaseModel
from fsspec.implementations.cached import CachingFileSystem
from fsspec import AbstractFileSystem

from .driver import Driver
from .dynamic_credentials import MissingUserData, RequiredToken, complete_settings
from .protocols import FSSpecProvider

SMBAvailable = False
try:
    from fsspec.implementations.smb import SMBFileSystem as SMBFS
    SMBAvailable = True
except:
    SMBFS = Any


class SmbCredentials(BaseModel):
    workgroup: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

    def resolve(self, prefix: str, user_data: Dict[str, str]) -> Union[SmbCredentials, MissingUserData]:
        cfg, missing_fields = complete_settings(self, prefix, user_data)
        if len(missing_fields) > 0:
            return MissingUserData(env_prefix=prefix, fields=missing_fields)
        return cfg


class SmbVirtualFS(BaseModel):
    mount_as: str
    host: str
    port: Optional[int] = None
    share_access: Optional[Literal['r', 'w', 'd']] = None
    credentials: Optional[SmbCredentials] = None
    kind: Literal['smb'] = 'smb'


class SmbProvider:
    def __init__(self, cfg: SmbVirtualFS) -> None:
        self.__cfg = cfg

    @property
    def name(self) -> str:
        return self.__cfg.mount_as

    @property
    def vfs(self) -> SmbVirtualFS:
        return self.__cfg

    def create(self, cache_root: str, **kwargs) -> AbstractFileSystem:
        credentials = {} if self.__cfg.credentials is None else self.__cfg.credentials.dict()
        base = SMBFS(self.__cfg.host, port=self.__cfg.port,
                     share_access=self.__cfg.share_access,
                     **credentials, **kwargs)
        cache_storage = os.path.join(cache_root, self.__cfg.mount_as)
        os.makedirs(cache_storage, exist_ok=True)
        return CachingFileSystem(fs=base, cache_storage=cache_storage, compression=None)


class SmbDriver(Driver[SmbVirtualFS]):

    def available(self) -> bool:
        return SMBAvailable

    def accept(self, configuration: Any):
        return isinstance(configuration, SmbVirtualFS)

    def has_full_credentials(self, cfg: SmbVirtualFS) -> bool:
        cred = cfg.credentials
        if cred is None:
            return True

        for f in cred.__fields__:
            if f in cred.__fields_set__:
                continue
            if getattr(cred, f) is None:
                return False

        return True

    def resolve_credentials(self, cfg: SmbVirtualFS, prefix: str, user_data: Dict[str, str]) -> Union[SmbVirtualFS, MissingUserData, RequiredToken]:
        if cfg.credentials is None:
            return cfg

        new_cfg = cfg.credentials.resolve(prefix, user_data)
        if isinstance(new_cfg, (MissingUserData, RequiredToken)):
            return new_cfg
        return cfg.copy(update={'credentials': new_cfg})

    def create(self, cfg: SmbVirtualFS) -> FSSpecProvider:
        if not self.available():
            warn("SMB Virtual File System is not available due to missing dependencies.", ImportWarning)
            warn("Install additional dependencies through `pip install shapelets-platform[vfs-smb]`", ImportWarning)
            raise ImportError(name='smbprotocol')

        if not self.has_full_credentials(cfg):
            raise ValueError("Missing credentials!")

        return SmbProvider(cfg)

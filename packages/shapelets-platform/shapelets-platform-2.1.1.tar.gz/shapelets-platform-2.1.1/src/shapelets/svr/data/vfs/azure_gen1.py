from __future__ import annotations

import os

from typing import Union, Dict, Any, Optional
from typing_extensions import Literal
from warnings import warn

from pydantic import BaseModel
from fsspec import AbstractFileSystem
from fsspec.implementations.cached import CachingFileSystem

from .dynamic_credentials import MissingUserData, RequiredToken, complete_settings
from .driver import Driver
from .protocols import FSSpecProvider

AzureGen1Available = False
try:
    from adlfs import AzureDatalakeFileSystem as AzureFS
    AzureGen1Available = True
except:
    AzureFS = Any


class AzureServicePrincipalGen1(BaseModel):
    """
    Azure Gen1 Credentials
    """

    tenant_id: Optional[str] = None
    """
    Tenant ID
    """

    client_id: Optional[str] = None
    """
    Client ID
    """

    client_secret: Optional[str] = None
    """
    Client secret
    """

    def resolve(self, prefix: str, user_data: Dict[str, str]) -> Union[AzureServicePrincipalGen1, MissingUserData]:
        cfg, missing_fields = complete_settings(self, prefix, user_data)
        if len(missing_fields) > 0:
            return MissingUserData(env_prefix=prefix, fields=missing_fields)
        return cfg


class AzureGen1VirtualFS(BaseModel):
    mount_as: str
    credentials: AzureServicePrincipalGen1
    kind: Literal['azgen1'] = 'azgen1'


class AzureGen1Provider:
    def __init__(self, cfg: AzureGen1VirtualFS) -> None:
        self.__cfg = cfg

    @property
    def name(self) -> str:
        return self.__cfg.mount_as

    @property
    def vfs(self) -> AzureGen1VirtualFS:
        return self.__cfg

    def create(self, cache_root: str, **kwargs) -> AbstractFileSystem:
        params = self.__cfg.credentials.dict()
        base = AzureFS(**params, **kwargs)
        cache_storage = os.path.join(cache_root, self.__cfg.mount_as)
        os.makedirs(cache_storage, exist_ok=True)
        return CachingFileSystem(fs=base, cache_storage=cache_root, compression=None)


class AzureGen1Driver(Driver[AzureGen1VirtualFS]):

    def available(self) -> bool:
        return AzureGen1Available

    def accept(self, configuration: Any):
        return isinstance(configuration, AzureGen1VirtualFS)

    def has_full_credentials(self, cfg: AzureGen1VirtualFS) -> bool:
        cred = cfg.credentials
        for f in cred.__fields__:
            if f in cred.__fields_set__:
                continue
            if getattr(cred, f) is None:
                return False
        return True

    def resolve_credentials(self, cfg: AzureGen1VirtualFS, prefix: str, user_data: Dict[str, str]) -> Union[AzureGen1VirtualFS, MissingUserData, RequiredToken]:
        new_cfg = cfg.credentials.resolve(prefix, user_data)
        if isinstance(new_cfg, (MissingUserData, RequiredToken)):
            return new_cfg

        return cfg.copy(update={'credentials': new_cfg})

    def create(self, cfg: AzureGen1VirtualFS) -> FSSpecProvider:
        if not self.available():
            warn("Azure Storage Gen1 File System is not available due to missing dependencies.", ImportWarning)
            warn("Install additional dependencies through `pip install shapelets-platform[vfs-azure]`", ImportWarning)
            raise ImportError(name='adlfs')

        if not self.has_full_credentials(cfg):
            raise ValueError("Missing credentials!")

        return AzureGen1Provider(cfg)

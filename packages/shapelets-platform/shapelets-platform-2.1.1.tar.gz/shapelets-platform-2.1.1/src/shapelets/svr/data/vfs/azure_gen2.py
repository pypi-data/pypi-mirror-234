from __future__ import annotations

import os

from typing import Union, Dict, Any, Optional
from typing_extensions import Literal, Annotated
from warnings import warn

from pydantic import BaseModel, Field
from fsspec import AbstractFileSystem
from fsspec.implementations.cached import CachingFileSystem

from .driver import Driver
from .access_token_credentials import AccessToken
from .dynamic_credentials import MissingUserData, RequiredToken, complete_settings
from .protocols import FSSpecProvider

AzureGen2Available = False
try:
    from adlfs import AzureBlobFileSystem as AzureFS
    AzureGen2Available = True
except:
    AzureFS = Any


class AzureAccountKey(BaseModel):
    """
    Authentication using an account key
    """

    account_name: Optional[str] = None
    """
    The storage account name.
    """

    account_key: Optional[str] = None
    """
    The storage account key
    """

    cred_kind: Literal['azacckey'] = 'azacckey'

    def resolve(self, prefix: str, user_data: Dict[str, str]) -> Union[AzureAccountKey, MissingUserData]:
        cfg, missing_fields = complete_settings(self, prefix, user_data)
        if len(missing_fields) > 0:
            return MissingUserData(env_prefix=prefix, fields=missing_fields)
        return cfg


class AzureServicePrincipalGen2(BaseModel):
    """
    Authentication using an AD Service Principal client/secret
    """
    account_name: Optional[str] = None
    """
    The storage account name.
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

    cred_kind: Literal['azsp'] = 'azsp'

    def resolve(self, prefix: str, user_data: Dict[str, str]) -> Union[AzureServicePrincipalGen2, MissingUserData]:
        cfg, missing_fields = complete_settings(self, prefix, user_data)
        if len(missing_fields) > 0:
            return MissingUserData(env_prefix=prefix, fields=missing_fields)
        return cfg


class AzureConnectionString(BaseModel):
    """
    Authentication through a connection string
    """
    connection_string: Optional[str] = None
    """
    See http://azure.microsoft.com/en-us/documentation/articles/storage-configure-connection-string/
    """

    cred_kind: Literal['azconn'] = 'azconn'

    def resolve(self, prefix: str, user_data: Dict[str, str]) -> Union[AzureConnectionString, MissingUserData]:
        cfg, missing_fields = complete_settings(self, prefix, user_data)
        if len(missing_fields) > 0:
            return MissingUserData(env_prefix=prefix, fields=missing_fields)
        return cfg


class AzureAnonymous(BaseModel):
    """
    Anonymous access
    """
    account_name: Optional[str] = None
    """
    The storage account name.
    """
    cred_kind: Literal['azanon'] = 'azanon'

    def resolve(self, prefix: str, user_data: Dict[str, str]) -> Union[AzureAnonymous, MissingUserData]:
        cfg, missing_fields = complete_settings(self, prefix, user_data)
        if len(missing_fields) > 0:
            return MissingUserData(env_prefix=prefix, fields=missing_fields)
        return cfg


AzureCredentialsGen2 = Annotated[
    Union[AzureConnectionString, AccessToken, AzureServicePrincipalGen2, AzureAccountKey, AzureAnonymous],
    Field(discriminator="cred_kind")
]


class AzureGen2VirtualFS(BaseModel):
    mount_as: str
    credentials: AzureCredentialsGen2
    kind: Literal['azgen2'] = 'azgen2'


class AzureGen2Provider:
    def __init__(self, cfg: AzureGen2VirtualFS) -> None:
        self.__cfg = cfg

    @property
    def name(self) -> str:
        return self.__cfg.mount_as

    @property
    def vfs(self) -> AzureGen2VirtualFS:
        return self.__cfg

    def create(self, cache_root: str, **kwargs) -> AbstractFileSystem:
        params = self.__cfg.credentials.dict()

        if isinstance(self.__cfg.credentials, AccessToken):
            params['sas_token'] = params['token']
            del params['service']
            del params['token']

        base = AzureFS(**params, **kwargs)
        cache_storage = os.path.join(cache_root, self.__cfg.mount_as)
        os.makedirs(cache_storage, exist_ok=True)
        return CachingFileSystem(fs=base, cache_storage=cache_storage, compression=None)


class AzureGen2Driver(Driver[AzureGen2VirtualFS]):

    def available(self) -> bool:
        return AzureGen2Available

    def accept(self, configuration: Any):
        return isinstance(configuration, AzureGen2VirtualFS)

    def has_full_credentials(self, cfg: AzureGen2VirtualFS) -> bool:
        cred = cfg.credentials
        for f in cred.__fields__:
            if f in cred.__fields_set__:
                continue
            if getattr(cred, f) is None:
                return False
        return True

    def resolve_credentials(self, cfg: AzureGen2VirtualFS, prefix: str, user_data: Dict[str, str]) -> Union[AzureGen2VirtualFS, MissingUserData, RequiredToken]:
        new_cfg = cfg.credentials.resolve(prefix, user_data)
        if isinstance(new_cfg, (MissingUserData, RequiredToken)):
            return new_cfg

        return cfg.copy(update={'credentials': new_cfg})

    def create(self, cfg: AzureGen2VirtualFS) -> FSSpecProvider:
        if not self.available():
            warn("Azure Storage Gen1 File System is not available due to missing dependencies.", ImportWarning)
            warn("Install additional dependencies through `pip install shapelets-platform[vfs-azure]`", ImportWarning)
            raise ImportError(name='adlfs')

        if not self.has_full_credentials(cfg):
            raise ValueError("Missing credentials!")

        return AzureGen2Provider(cfg)

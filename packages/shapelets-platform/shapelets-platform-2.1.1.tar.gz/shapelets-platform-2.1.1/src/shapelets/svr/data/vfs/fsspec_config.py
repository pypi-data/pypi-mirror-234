from __future__ import annotations

import os
import tomlkit

from typing import Union, List
from typing_extensions import Annotated
from pydantic import BaseModel, DirectoryPath, Field, parse_obj_as
from warnings import warn

from .azure_gen1 import AzureGen1VirtualFS
from .azure_gen2 import AzureGen2VirtualFS, AzureAnonymous
from .ftp import FtpVirtualFS
from .smb import SmbVirtualFS
from .local import LocalVirtualFS


VirtualFS = Annotated[
    Union[AzureGen1VirtualFS, AzureGen2VirtualFS, FtpVirtualFS, SmbVirtualFS, LocalVirtualFS],
    Field(discriminator="kind")
]


class FSSpecVFSConfig(BaseModel):
    cache_root: str
    vfs: List[VirtualFS]

    @staticmethod
    def load(file: str = '~/.shapelets/vfs.toml') -> FSSpecVFSConfig:
        checked_file = os.path.expanduser(file)
        checked_file = os.path.expandvars(checked_file)
        if not os.path.exists(checked_file):
            warn(f"No virtual file system found in {file}. Using default settings.", UserWarning)
            default_cache = os.path.expanduser("~/.shapelets/cache")
            os.makedirs(default_cache)
            default_fs = AzureGen2VirtualFS(
                mount_as='azpublic',
                credentials=AzureAnonymous(account_name='azureopendatastorage'))
            result = FSSpecVFSConfig(cache_root=default_cache, vfs=[default_fs])

            default_settings_file = os.path.expanduser('~/.shapelets/vfs.toml')

            with open(default_settings_file, "wt", encoding="utf-8") as handle:
                tomlkit.dump(result.dict(), handle)

            return result

        with open(checked_file, "rt", encoding="utf-8") as handle:
            data = tomlkit.load(handle).unwrap()

        return parse_obj_as(FSSpecVFSConfig, data)

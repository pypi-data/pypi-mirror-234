"""
# VFS Module
Provides an abstraction over the location of datasets; it doesn't provide named datasets 
but a way to access them, wherever they may be. 

There are two mayor components in this design: in one hand, we have fsspec* classes, which 
are responsible for the file system abstractions, in such way these are presented to 
the native code.  On the other hand, we have the rest of the classes, which represent
an actual file system abstraction built over fsspec.

## Actual File systems
There are 4 types of classes; if you take smb (for example), you will find SmbCredentials, 
SmbVirtualFS, SmbProvider and SmbDriver.

`*Driver` classes are responsible for validating at runtime `*VirtualFS` instances, which 
may contain `*Credentials`.  Driver classes trigger the logic for completing `*Credential` 
instances based on user provided overrides and environment variables; user overrides always 
take preference over environment variables.  Lastly, `*Driver` classes are responsible for 
creating `*Provider` instances; which are used by the virtual system to instantiate 
fsspec.AbstractFileSystem instances on a closed configuration.  `*Provider` classes are 
meant to implement a protocol, FSSpecProvider, so they can be used by FSSpecVFSFactory.

## FSSPEC* Classes
These are responsible for presenting the native layer an uniform virtual file system.  The 
URL structure will be in the form `fss://actual/path`, where `actual` is the `mount_as` 
attribute in a `*VirtualFS` instance; `path` interpretation is delegated to the actual 
file system.

FSSpecVFSFactory implements shapelets_native.VirtualFileSystemFactory; the method create 
is called by a native thread to set itself up with a thread safe copy of the virtual 
file system.  DynamicFSProvider protocol is implemented by FSSpecVFSFactory; the protocol 
is utilized to add new file systems to the virtual tree at run time (FSSpecVFS uses 
lookup method to find new instances and clients of this package may use this protocol 
to add/remove new filesystems on request).

FSSpecVFS implements shapelets_native.VirtualFileSystem; instances are created by 
`FSSpecVFSFactory::create` method.

FSSpecVFSFile implements shapelets_native.VirtualFile; instances are created by 
`FSSpecVFS::open_file` method.

FSSpecVFSConfig provides a minimal configuration from a toml file, which is 
located by default under '~/.shapelets/vfs.toml'


## Validating a file system
Credentials in a file system change completely from one system to the next.  However, 
a common protocol is introduced to resolve these settings, so administrators may 
be able to use env files, environment settings to set up confidential information or 
simply left blank for the user to provide the correct values.

The method `validate_file_system` takes care of this process.  Given a `*VirtualFS` 
configuration instance, it locates the `*Driver` class and proceeds to its 
credential validation.  This process uses environment variables and user provided 
overrides.  If the process determines there is missing information, the 
method will return either:

* MissingUserData, which documents the prefix used in the resolution of settings and 
the list of missing credentials settings the user will need to supply.
* RequiredToken.  Informs the caller that an OAuth access token is required to 
complete the operation.  This token should be obtained through Shapelets GC.

If the process returns an instance of protocol FSSpecProvider, the validation 
process is completed and the validated file system can be added to a 
FSSpecVFSFactory (through DynamicFSProvider protocol.)

"""


from typing import Dict, Union, Optional

from .azure_gen1 import AzureGen1VirtualFS, AzureServicePrincipalGen1
from .azure_gen2 import AzureAccountKey, AzureServicePrincipalGen2, AzureConnectionString, AzureAnonymous, AzureCredentialsGen2, AzureGen2VirtualFS
from .access_token_credentials import AccessToken
from .ftp import FtpVirtualFS, FtpCredentials
from .smb import SmbVirtualFS, SmbCredentials
from .local import LocalVirtualFS
from .driver import Driver
from .fsspec_config import VirtualFS, FSSpecVFSConfig
from .dynamic_credentials import MissingUserData, RequiredToken
from .protocols import FSSpecProvider
from .fsspec_vfs_factory import FSSpecVFSFactory
from .fsspec_vfs import FSSpecVFS, OpenFlags
from .fsspec_vfs_file import FSSpecVFSFile

from . import azure_gen1
from . import azure_gen2
from . import ftp
from . import smb
from . import local

from rodi import Container


def _setup_services(container: Container):
    """
    Adds drivers to container, mapping configurations with logic
    """
    container.add_singleton(Driver[AzureGen1VirtualFS], azure_gen1.AzureGen1Driver)
    container.add_singleton(Driver[AzureGen2VirtualFS], azure_gen2.AzureGen2Driver)
    container.add_singleton(Driver[FtpVirtualFS], ftp.FtpDriver)
    container.add_singleton(Driver[SmbVirtualFS], smb.SmbDriver)
    container.add_singleton(Driver[LocalVirtualFS], local.LocalDriver)
    return container.build_provider()


_services = _setup_services(Container())


def validate_file_system(cfg: VirtualFS, user_overrides: Dict[str, str] = {}, sep: str = "__") -> Optional[Union[FSSpecProvider, MissingUserData, RequiredToken]]:
    """
    Validates a file system configuration, checking for missing values that cannot either be 
    resolved through the environment variables or through the user provided data.

    Parameters
    ----------
    cfg: one of AzureGen1VirtualFS, AzureGen2VirtualFS, FtpVirtualFS, SmbVirtualFS, LocalVirtualFS
        a virtual file system configuration 

    user_overrides: dictionary of settings
        User provided settings.  These will take preference over environment settings.

    sep: str, defaults to "__"
        Utilized to construct the prefix string to locate the correct environment and user 
        provided settings.  For example, a virtual file system may be named "test_vfs" and 
        sep parameter may be "__"; in this example all missing settings will be searched as 
        "test_vsf__" in either the environment variables or the user provided data.

    Returns
    -------
    Either it returns a resolved file system provider or it returns a object (MissingData, 
    RequiredToken) documenting missing information that couldn't be resolved 

    """
    global _services
    driver = _services.get(Driver[type(cfg)])
    if driver is None or not driver.accept(cfg):
        raise ValueError(f"Unknown virtual file system configuration {cfg}")
    new_cfg = driver.resolve_credentials(cfg, cfg.mount_as + sep, user_overrides)
    if isinstance(new_cfg, (MissingUserData, RequiredToken)):
        return new_cfg
    return driver.create(new_cfg)


__all__ = [
    "VirtualFS",
    "AzureGen1VirtualFS", "AzureServicePrincipalGen1",
    "AzureAccountKey", "AzureServicePrincipalGen2", "AzureConnectionString", "AzureAnonymous", "AzureCredentialsGen2", "AzureGen2VirtualFS",
    "AccessToken",
    "FtpVirtualFS", "FtpCredentials",
    "SmbVirtualFS", "SmbCredentials",
    "LocalVirtualFS",
    "validate_file_system",
    "FSSpecVFS",
    "OpenFlags",
    "FSSpecVFSFile",
    "FSSpecVFSFactory",
    "FSSpecVFSConfig",
    "Driver"
]

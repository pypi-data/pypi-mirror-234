from fsspec import AbstractFileSystem
from typing import Optional, Any
from typing_extensions import Protocol


class FSSpecProvider(Protocol):
    """
    Represents a named configuration source for a fsspec 
    filesystem that can be instantiated through a 
    create method.
    """
    @property
    def name(self) -> str:
        """
        Identification of the filesystem; it will be used as key 
        in the virtual tree as `fss://{name}/...`
        """
        pass

    @property
    def vfs(self) -> Any:
        """
        Only used for debugging purposes as it allows to see the 
        final settings of the virtual file system.  It is set to 
        Any to ease up on cyclic dependencies.
        """
        pass

    def create(self, cache_root: str, **kwargs) -> AbstractFileSystem:
        """
        Instantiates on demand a file system.

        Parameters
        ----------
        cache_root: str
            Indicates the base directory where to create a 
            local contents cache.
        kwargs: 
            Named parameters to pass down the stack
        """
        pass


class DynamicFSProvider(Protocol):
    """
    Models a configuration point where new filesystems may be added or removed
    """

    def __contains__(self, name: str) -> bool:
        """
        Checks if a filesystem has been registered under a particular name.
        """
        pass

    def append(self, provider: FSSpecProvider):
        """
        Adds or overrides a provider
        """
        pass

    def lookup(self, name: str) -> Optional[AbstractFileSystem]:
        """
        Looks up a filesystem by name and returns a brand new instance 
        of such filesystem.
        """
        pass

    def is_valid(self, name: str) -> bool:
        """
        Checks if a particular filesystem is still valid
        """
        pass

    def remove(self, name: str):
        """
        Marks a file system as invalid (no further instances should be created.)
        """
        pass

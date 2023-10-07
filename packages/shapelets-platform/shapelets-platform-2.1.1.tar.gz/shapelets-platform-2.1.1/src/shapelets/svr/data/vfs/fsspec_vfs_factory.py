import os

from typing import List, Optional, Set

from fsspec import AbstractFileSystem
from shapelets_native import VirtualFileSystemFactory

from .fsspec_vfs import FSSpecVFS
from .protocols import FSSpecProvider


class FSSpecVFSFactory(VirtualFileSystemFactory):
    """
    Implementation of a VirtualFileSystemFactory using FSSpec

    Follows DynamicFSProvider protocol
    """

    def __init__(self, cache_root: str, fixed_sources: List[FSSpecProvider]) -> None:
        # call it this way to ensure proper initialization of the
        # native / trampoline classes.
        VirtualFileSystemFactory.__init__(self)
        # expand tildes
        checked_path = os.path.expanduser(cache_root)
        # expand env vars
        checked_path = os.path.expandvars(checked_path)
        # ensure the directory exists
        os.makedirs(checked_path, exist_ok=True)

        self.__cache_root = checked_path
        self.__fixed_sources = fixed_sources
        self.__sources = {entry.name: entry for entry in self.__fixed_sources}
        self.__removed: Set[str] = set()

    def create(self) -> FSSpecVFS:
        """
        Implements the create method expected by VirtualFileSystemFactory

        This method will be called directly by the native layer, for each 
        native thread accessing the virtual file system.
        """
        fixed_config = dict()
        for source in self.__fixed_sources:
            fixed_config[source.name] = source.create(self.__cache_root)

        return FSSpecVFS(self, fixed_config)

    def __contains__(self, name: str) -> bool:
        # Checks if name is registered
        return name in self.__sources and name not in self.__removed

    def append(self, fs: FSSpecProvider):
        # Adds / overrides a file system
        self.__sources[fs.name] = fs
        self.__removed.remove(fs.name)

    def lookup(self, name: str) -> Optional[AbstractFileSystem]:
        # Looks up and instantiates a file system
        if not name in self.__sources or name in self.__removed:
            return None

        return self.__sources[name].create(self.__cache_root)

    def is_valid(self, name: str) -> bool:
        # A wrapper around __contains__
        return name in self

    def remove(self, name: str):
        # Adds the name to the removed entries and eliminates the entry
        # in sources
        self.__removed.add(name)
        del self.__sources[name]

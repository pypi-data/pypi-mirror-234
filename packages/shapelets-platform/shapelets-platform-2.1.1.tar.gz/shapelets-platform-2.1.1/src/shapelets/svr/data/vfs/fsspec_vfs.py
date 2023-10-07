import re

from typing import Dict, Tuple, List
from fsspec import AbstractFileSystem
from shapelets_native import VirtualFileSystem, VirtualFileSystemFactory

from .fsspec_vfs_file import FSSpecVFSFile
from .protocols import DynamicFSProvider


def is_flag_set(flags: int, test: int) -> bool:
    return flags & test == test


class OpenFlags:
    READ = VirtualFileSystem.READ
    WRITE = VirtualFileSystem.WRITE
    CREATE = VirtualFileSystem.CREATE
    CREATE_NEW = VirtualFileSystem.CREATE_NEW
    APPEND = VirtualFileSystem.APPEND


class FSSpecVFS(VirtualFileSystem):
    """
    Implementation of a VirtualFileSystem using FSSpec
    """

    def __init__(self, dyn_provider: DynamicFSProvider, cfg: Dict[str, AbstractFileSystem]) -> None:
        VirtualFileSystem.__init__(self)
        self._cfg = cfg
        self._dyn_provider = dyn_provider
        self._extractor = re.compile(r"fss://(?P<fs>[^/]+)(?P<actual>.+)", re.RegexFlag.IGNORECASE)

    def _extract(self, path: str) -> Tuple[str, AbstractFileSystem, str]:
        m = self._extractor.search(path)
        fs_code = m.group('fs')
        actual = m.group('actual')
        # There are a few bugs like
        # this one in fsspec
        actual = actual.replace("//", "/")
        if fs_code not in self._cfg:
            raise RuntimeError(f"Unknown configuration [{fs_code}]")

        return (fs_code, self._cfg[fs_code], actual)

    def open_file(self, path: str, flags: int) -> FSSpecVFSFile:
        _, fs, actual = self._extract(path)
        if is_flag_set(flags, VirtualFileSystem.CREATE_NEW):
            if not fs.exists(actual):
                p = actual.rfind("/")
                if p > 0:
                    fs.makedirs(actual[0:p], exist_ok=True)
                fs.touch(actual)
                return FSSpecVFSFile(fs, actual, "wb")
            else:
                handle = FSSpecVFSFile(fs, actual)
                handle.truncate(0)
                return handle

        if is_flag_set(flags, VirtualFileSystem.CREATE):
            if not fs.exists(actual):
                p = actual.rfind("/")
                if p > 0:
                    fs.makedirs(actual[0:p], exist_ok=True)
                fs.touch(actual)
            return FSSpecVFSFile(fs, actual, "wb")

        if is_flag_set(flags, VirtualFileSystem.APPEND):
            handle = FSSpecVFSFile(fs, actual, "wb")
            handle.set_position(handle.size() - 1)
            return handle

        return FSSpecVFSFile(fs, actual)

    def directory_exists(self, directory: str) -> bool:
        _, fs, actual = self._extract(directory)
        return fs.exists(actual)

    def create_directory(self, directory: str) -> None:
        _, fs, actual = self._extract(directory)
        fs.mkdir(actual)

    def remove_directory(self, directory: str) -> None:
        _, fs, actual = self._extract(directory)
        fs.rm(actual, recursive=True)

    def list_files(self, directory: str) -> List[Tuple[str, bool]]:
        fs_code, fs, actual = self._extract(directory)
        return [(f'fss://{fs_code}/{x["name"]}', x["type"] != 'file') for x in fs.ls(actual, detail=True)]

    def move_file(self, src: str, dst: str) -> None:
        _, fs, actual_src = self._extract(src)
        _, _, actual_dst = self._extract(dst)
        fs.move(actual_src, actual_dst)

    def file_exists(self, path: str) -> bool:
        _, fs, actual = self._extract(path)
        return fs.exists(actual)

    def delete_file(self, path: str) -> None:
        _, fs, actual = self._extract(path)
        fs.rm_file(actual)

    def glob(self, path: str) -> List[str]:
        fs_code, fs, actual = self._extract(path)
        base_lst = fs.glob(actual)
        return [f'fss://{fs_code}/{x}' for x in base_lst]

    def can_handle(self, path: str) -> bool:
        m = self._extractor.search(path)
        fs_code = m.group('fs')

        if fs_code is None or fs_code not in self._dyn_provider:
            return False

        if fs_code in self._cfg:
            is_valid = self._dyn_provider.is_valid(fs_code)
            if not is_valid:
                del self._cfg[fs_code]
            return is_valid

        new_fs = self._dyn_provider.lookup(fs_code)
        self._cfg[fs_code] = new_fs
        return True

from datetime import datetime
from os import stat
from time import mktime
from stat import S_ISREG

from shapelets_native import VirtualFile


class FSSpecVFSFile(VirtualFile):
    """
    Implementation of a VirtualFile using FSSpec
    """

    def __init__(self, fs, actual: str, mode: str = "rb") -> None:
        # Use this method to init the base class
        # instead of the standard super().__init__()
        # to ensure the native base class is
        # initialized correctly
        VirtualFile.__init__(self)
        self._file = fs.open(actual, mode)

        fileno_fn = getattr(self._file, "fileno", None)
        self._has_fileno = fileno_fn is not None and callable(fileno_fn)
        if self._has_fileno:
            try:
                self._file.fileno()
            except:
                self._has_fileno = False

        info_fn = getattr(self._file, "info", None)
        self._has_info = info_fn is not None and callable(info_fn)
        if self._has_info:
            try:
                self._file.info()
            except:
                self._has_info = False

        self._has_details = getattr(self._file, "details", None) is not None
        if self._has_details:
            try:
                self._file.details
            except:
                self._has_details = False

    def read_at(self, buffer: memoryview, bytes: int, location: int) -> None:
        current = self.get_position()
        self.set_position(location)
        try:
            data = self._file.read(bytes)
            buffer[: len(data)] = data
            return len(data)
        finally:
            self.set_position(current)

    def write_at(self, buffer: memoryview, bytes: int, location: int) -> None:
        current = self.get_position()
        self.set_position(location)
        try:
            return self._file.write(buffer[0:bytes])
        finally:
            self.set_position(current)

    def read(self, buffer: memoryview, bytes: int) -> int:
        data = self._file.read(bytes)
        buffer[: len(data)] = data
        return len(data)

    def write(self, buffer: memoryview, bytes: int) -> int:
        return self._file.write(buffer[0:bytes])

    def size(self) -> int:
        if self._has_fileno:
            return stat(self._file.fileno()).st_size

        details = {}
        if self._has_info:
            details = self._file.info()
        elif self._has_details:
            details = self._file.details

        if 'size' in details:
            return int(details['size'])

        return 0

    def last_modified_time(self) -> int:
        if self._has_fileno:
            return int(stat(self._file.fileno()).st_mtime)

        details = {}
        if self._has_info:
            details = self._file.info()
        elif self._has_details:
            details = self._file.details

        if 'last_modified' in details:
            lm = details['last_modified']
            if isinstance(lm, (datetime)):
                return int(mktime(lm.timetuple()))
        return 0

    def is_file(self) -> bool:
        if self._has_fileno:
            mode = stat(self._file.fileno()).st_mode
            return S_ISREG(mode)

        details = {}
        if self._has_info:
            details = self._file.info()
        elif self._has_details:
            details = self._file.details

        if 'type' in details:
            return details['type'] == 'file'

        return False

    def truncate(self, new_size: int) -> None:
        self._file.truncate(new_size)

    def sync(self) -> None:
        self._file.flush(True)

    def set_position(self, location: int) -> None:
        self._file.seek(location)

    def get_position(self) -> int:
        return self._file.tell()

    def close(self) -> None:
        self._file.close()

from typing import Optional, Union, List
from pydantic import BaseModel, DirectoryPath, PositiveFloat


class ReloadSettings(BaseModel):
    enabled: bool = False
    """
    Should the server watch for changes and reload?
    """

    dirs: Optional[Union[List[DirectoryPath], DirectoryPath]] = None
    """
    Directory, or list of directories, to watch for changes
    """

    delay: Optional[PositiveFloat] = None
    """
    Time before reloading after detecting a change
    """

    includes: Optional[Union[List[str], str]] = None
    """
    Glob pattern(s) of files to include
    """

    excludes: Optional[Union[List[str], str]] = None
    """
    Glob pattern(s) of files to exclude
    """

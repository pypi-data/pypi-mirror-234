import os
import tomlkit

from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


class _TOMLFile:
    """
    Provides `toml` contents to `pydantic`
    """
    __slots__ = ('path', 'encoding')

    def __init__(self, file: Path, encoding: str = 'utf-8') -> None:
        self.path = file
        self.encoding = encoding

    def exists(self) -> bool:
        return self.path.exists() if self.path is not None else False

    def __call__(self, settings: Optional[BaseSettings] = None) -> Dict[str, Any]:
        with open(self.path, "rt", encoding="utf-8") as handle:
            # unwrap says it is a str, but it returns the dictionary we need!!
            # two hours chasing my own tail
            return tomlkit.load(handle).unwrap()

    def __repr__(self) -> str:
        return f'TOML: {self.path}'


def _find_configuration_file(directory: str, namePattern: str = 'settings') -> Optional[SettingsSourceCallable]:
    """
    Utility method that returns a reader compatible with `pydantic`
    capable of processing `toml` files.
    """
    d = Path(os.path.expandvars(os.path.expanduser(directory)))

    if not d.exists():
        return None

    if not d.is_dir():
        raise ValueError(f"{directory} is not a directory")

    file = d / (namePattern + '.toml')
    if not file.exists():
        return None

    return _TOMLFile(file)


def package_settings() -> Optional[SettingsSourceCallable]:
    """
    Access default values, which comes with the software distribution itself.
    """
    packageDir = os.path.dirname(__file__)
    return _find_configuration_file(packageDir)


def home_settings() -> Optional[SettingsSourceCallable]:
    """
    Access configuration settings stored in the home directory
    """
    return _find_configuration_file('~/.shapelets')


def current_settings() -> Optional[SettingsSourceCallable]:
    """
    Access configuration settings stored in the current directory
    """
    return _find_configuration_file(os.getcwd())


__all__ = ['package_settings', 'home_settings', 'current_settings']

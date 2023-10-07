import os
import tomlkit

from pathlib import Path
from typing import Union

from .global_client import global_client_defaults
from .telemetry import telemetry_defaults


def defaults(loc: Union[Path, str] = '~/.shapelets/settings.toml', **kwargs):
    """
    Create, update and reset common configuration values using a simple api.

    Parameters
    ----------
    loc: path or string, defaults to `~/.shapelets/settings.toml`
        File where the new default settings will be stored

    **kwargs: Settings to create, update or remove
        If a setting is not present, it will be left unchanged.  When set to None, the 
        setting will be removed from the configuration file, letting other configuration 
        files and environment settings to set its value.  When set to an actual value,
        it will create a new entry in the `loc` file.

        Valid keyword arguments are:

        - **signed_token**: optional, string
          Outcome of successful login is a signed token that can be (re)used as a 
          bearer token to work with Shapelets Server APIs.

        - **host**: optional, either a string, bytes, int, IPv4Address or IPv6Address
          Address of the server to connect to.

        - **port**: optional, positive int
          Port number on the host where the server can be located.

        - **enable_telemetry**: optional, boolean, defaults to None
          Enables or disables the anonymous telemetry metrics.

        - **server_mode**: optional, one of `headless`, `in-process`, `out-of-process`, defaults to None 
          Should the server component be hosted within this process or, alternatively, it is to be 
          hosted by an external (usually demonized) process.
    """

    file = Path(os.path.expandvars(os.path.expanduser(loc)))
    if not file.exists():
        file.parent.mkdir(exist_ok=True)
        file.touch()

    # load the data
    with open(file, "rt", encoding="utf-8") as handle:
        data = tomlkit.load(handle)

    global_client_defaults(data, **kwargs)
    telemetry_defaults(data, **kwargs)

    with open(file, "wt", encoding="utf-8") as handle:
        tomlkit.dump(data, handle)

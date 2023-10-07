import tomlkit
import tomlkit.items

from ipaddress import IPv4Address, IPv6Address
from pydantic import BaseModel, IPvAnyAddress, PositiveInt
from typing import Optional, Dict
from typing_extensions import Literal

from .user import UserSettings, user_defaults

ServerModeType = Literal['headless', 'in-process', 'out-of-process', 'standalone']


class ClientSettings(BaseModel):
    """
    Client settings
    """

    users: Optional[Dict[str, UserSettings]] = None
    """
    Cached identity that can be persisted to disk.
    """

    protocol: Optional[str] = 'http'
    """
    Protocol to connect with the server
    """

    host: Optional[IPvAnyAddress] = '127.0.0.1'
    """
    Bind socket to this host. Use `127.0.0.1` to make the application available 
    on your local network. IPv6 addresses are supported, `::`.
    """

    port: Optional[PositiveInt] = 4567
    """
    Bind to a socket with this port. 
    """

    default_user: Optional[str] = None
    """
    Default user using the client settings. 
    """

    @property
    def server_url(self) -> str:
        """
        Utility function that returns the url of the server
        """
        return f'{self.protocol}://{self.host}:{self.port}'


def client_defaults(**kwargs) -> tomlkit.items.Table:
    """
    Creates or updates a configuration file with default client connectivity settings

    To revert values to their configuration, set the parameter to None; if the value 
    is not included in the call, no changes will be done to such parameter.  If the 
    parameter has a value, it will override existing values and stored them in the desired 
    file.

    Parameters
    ----------
    protocol: optional, string
        Protocol to connect with the server

    host: optional, either a string, bytes, int, IPv4Address or IPv6Address
        Address of the server to connect to.

    port: optional, positive int
        Port number on the host where the server can be located.

    deafult_user: optional, str
        Default user for the client.

    users: optional, UserSettings
        List of user credentials.

    """

    section = tomlkit.table()

    if 'host' in kwargs:
        host_info = kwargs['host']

        if 'host' in host_info:

            if 'protocol' in host_info and host_info['protocol'] is not None:
                section['protocol'] = str(host_info['protocol'])

            if 'host' in host_info and host_info['host'] is not None:
                user_value = host_info['host']
                address = IPvAnyAddress.validate(user_value) if isinstance(user_value,
                                                                           (str, bytes, int)) else user_value
                if not isinstance(address, (IPv4Address, IPv6Address)):
                    raise ValueError("Invalid host.")
                section['host'] = str(address)

            if 'port' in host_info and host_info['port'] is not None:
                section['port'] = int(host_info['port'])

            if 'default_user' in host_info and host_info['default_user'] is not None:
                section['default_user'] = host_info['default_user']

            if 'users' in host_info and host_info['users'] is not None:
                users_info = tomlkit.table()
                for user in host_info['users']:
                    users_info[user] = user_defaults(user_id=user, user=host_info['users'][user])
                section['users'] = users_info

    return section

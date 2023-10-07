import os
import tomlkit

from pathlib import Path
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from typing_extensions import Literal

from .client import ClientSettings, client_defaults
from .user import user_defaults

from ..model import SignedPrincipalId

ServerModeType = Literal['headless', 'in-process', 'out-of-process', 'standalone']


class GlobalClientSettings(BaseModel):
    """
    Global Client settings. It has inside the settings of multiple clients.
    """

    default_server: Optional[str] = None
    """
    Default server. Set to localhost
    """

    clients: Optional[Dict[str, ClientSettings]] = None
    """
    List of clients
    """

    server_mode: Optional[ServerModeType] = 'out-of-process'
    """
    Determines how the server component of Shapelets is managed, from the 
    perspective of this client.
    
    When set to `out-of-process`, which is the default setting, the 
    server component of Shapelets will be expected to be found at 
    the address determined by `host` and `port`.  
    
    `in-process` and `headless` are two special modes to interact 
    and host the server component; when set to `in-process`, a server 
    component will be launched within this process and, thus, its 
    lifetime will be coupled with this process.  When `in-process` 
    mode is active, host will be set to '127.0.0.1'
    
    In `headless` mode, the lifetime of the server will also be 
    tight to the lifetime of this process, but not HTTP interface 
    will be created; therefore, HTML UI won't be hosted.
    
    In `standalone` mode, only HTTP server is launched. This is really useful 
    for testing environments with remote clients. 
    
    `in-process` and `headless` mode are useful modes when running 
    either on testing environments or when running on isolated 
    environments like computational nodes and isolated worker processes.
    """


def global_client_defaults(data: tomlkit.TOMLDocument, **kwargs):
    """
       Creates or updates a configuration file with default client connectivity settings

       To revert values to their configuration, set the parameter to None; if the value
       is not included in the call, no changes will be done to such parameter.  If the
       parameter has a value, it will override existing values and stored them in the desired
       file.

       Parameters
       ----------
       data: TOML Document
            Current settings.toml

       default_server: optional, string
           Set the alias of the server used as local.

       server_mode: optional, ServerModeType
           Should the server component be hosted within this process or, alternatively, it is to be
           hosted by an external (usually demonized) process.

       clients: optional, ClientSettings
           Client information.

       """

    if 'client' not in data:
        section = tomlkit.table()
        data['client'] = section
    else:
        section = data['client']

    if 'default_server' in kwargs:
        if kwargs['default_server'] is None:
            # Leave it as it is
            pass
        else:
            section['default_server'] = kwargs['default_server']

    if 'server_mode' in kwargs:
        if kwargs['server_mode'] is None:
            if 'server_mode' in section:
                del section['server_mode']
        else:
            section['server_mode'] = kwargs['server_mode']

    if 'clients' in kwargs:
        if kwargs['clients'] is None:
            if 'clients' in section:
                del section['clients']
        else:
            # are we replacing or is new
            if section.get("clients"):
                clients = section["clients"]
            else:
                clients = tomlkit.table()
            for client in kwargs['clients']:
                # Create new one or replace existing
                clients[client] = client_defaults(alias=client, host=kwargs['clients'][client])
            section['clients'] = clients


def list_available_clients(loc: Union[Path, str] = "~/.shapelets/settings.toml") -> List[List[str]]:
    """
    List available clients.

    Parameters
    ----------
    loc: path or string, defaults to `~/.shapelets/settings.toml`
        File where the settings are.
    """

    file = Path(os.path.expandvars(os.path.expanduser(loc)))

    # load the data
    with open(file, "rt", encoding="utf-8") as handle:
        data = tomlkit.load(handle)

    if data.get("client").get("clients"):
        default_server = data.get("client").get("default_server")
        return_clients = []
        clients = data.get("client").get("clients")
        for client in clients:
            print(f"Alias: {client}")
            print(f"Default Server: {client == default_server}")
            print(f"Host: {clients.get(client).get('host')}")
            print(f"Port: {clients.get(client).get('port')}")
            print(f"Protocol: {clients.get(client).get('protocol')}")
            print(f"Default User: {clients.get(client).get('default_user')}")
            print(f"Saved Users: {[user for user in clients.get(client).get('users')]}\n")
            return_clients.append([client, clients.get(client).get('host'), clients.get(client).get('port'),
                                   clients.get(client).get('protocol'), clients.get(client).get('default_user'),
                                   [user for user in clients.get(client).get('users')]])
        return return_clients
    else:
        print("No clients found. ")
        return []


def add_user_to_client(host: str,
                       user_name: str,
                       user_principal: SignedPrincipalId,
                       default: bool = False,
                       loc: Union[Path, str] = "~/.shapelets/settings.toml"):
    """
    When adding a new user to a client, save user information in the configuration.
    """
    data = load_config_file(loc)

    host_alias = None
    client = data.get("client")
    if client is None:
        raise ValueError("There is no server information save. Please, add server information (sh.add(server))")
    for client, info in data.get("client").get("clients").items():
        if host == info.get("host"):
            host_alias = client
            break
    if host_alias is None:
        raise ValueError(f"Alias not found for host {host}")

    try:
        user_info = {
            "signed_token": user_principal.to_token(),
            "user_id": user_principal.userId
        }

        users = data.get("client").get("clients").get(host_alias).get("users")
        if users is None:
            # First time we add a user
            data.get("client").get("clients").get(host_alias)["users"] = {}
            users = data.get("client").get("clients").get(host_alias)["users"]
        users[user_name] = user_defaults(user=user_info)
        if default:
            data.get("client").get("clients").get(host_alias)["default_user"] = user_name

        save_config_file(data, loc)

    except Exception as e:
        raise ValueError("Unable to add user to configuration. Make sure the selected host exists.")


def remove_user_from_client(host: str, user_name: str, loc: Union[Path, str] = "~/.shapelets/settings.toml"):
    """
    Remove user from configuration file.
    """
    data = load_config_file(loc)

    host_alias = None
    for client, info in data.get("client").get("clients").items():
        if host == info.get("host"):
            host_alias = client
            break
    if host_alias is None:
        raise ValueError(f"Alias not found for host {host}")

    try:
        del data.get("client").get("clients").get(host_alias).get("users")[user_name]

        default_user = data.get("client").get("clients").get(host_alias).get("default_user")
        if default_user == user_name:
            del data.get("client").get("clients").get(host_alias)["default_user"]

        save_config_file(data, loc)

    except Exception as e:
        raise ValueError("Unable to remove user to configuration. Make sure the selected host exists.")


def load_config_file(loc: Union[Path, str] = "~/.shapelets/settings.toml") -> tomlkit.TOMLDocument:
    file = Path(os.path.expandvars(os.path.expanduser(loc)))
    with open(file, "rt", encoding="utf-8") as handle:
        data = tomlkit.load(handle)

    return data


def save_config_file(data: tomlkit.TOMLDocument, loc: Union[Path, str] = "~/.shapelets/settings.toml"):
    file = Path(os.path.expandvars(os.path.expanduser(loc)))
    with open(file, "wt", encoding="utf-8") as handle:
        tomlkit.dump(data, handle)

import os
import getpass

from requests import Session
from typing import List, Optional, Union
from typing_extensions import Literal
from urllib.parse import urlparse

from .svr import (
    add_user_to_client,
    crypto,
    defaults,
    gc_flow,
    get_service,
    get_service_optional,
    GroupProfile,
    IAuthService,
    IGroupsService,
    _is_server_up,
    IUsersService,
    list_available_clients,
    PrefixedSession,
    remove_user_from_client,
    Settings,
    SignedPrincipalId,
    UserAttributes,
    UserProfile)

EnterpriseLoginType = Literal['azure', 'linkedin', 'google', 'github']


def forget_me():
    """
    Forgets credentials stored in configuration files 
    """
    defaults(signed_token=None)


def login(*,
          authn_provider: Optional[EnterpriseLoginType] = None,
          user_name: Optional[str] = None,
          password: Optional[str] = None,
          remember_me: bool = True,
          user_settings: Optional[Settings] = None, ):
    """
    Warning: This method will be deleted.

    Login to Shapelets.

    This function is quite versatile and provides multiple methods of authentication. 

    When `authn_provider` is set, it will take preference over user name / password 
    combinations, even when found in the environment variables.  When login through 
    an external authentication provider for the very first time, a user will be 
    automatically created using the information shared by the authentication
    provider.

    If `authn_provider` is left unset, the code will try to log in using an user name 
    and password combination.  This information can be set directly as parameters, 
    through environment variables or by configuration files.  The recommended 
    method is to use environment variables to avoid exposing plain passwords.  Bear 
    in mind the credentials should have been created beforehand.

    If no external authentication or no user name / password combination is found, 
    the system will try to login the user using a previous login. 

    Parameters
    ----------
    authn_provider: optional, one of `azure`, `linkedin`, `google`, `github`
        Determines which external authentication provider should be used.

    user_name: optional, string 
        User name.  The preferred method for setting this value is through 
        the environment variable `SHAPELETS_CLIENT__USERNAME`

    password: optional, string 
        Password associated with `user_name`.  The preferred method for 
        setting this value is through the environment variable 
        `SHAPELETS_CLIENT__PASSWORD`

    remember_me: optional, bool, defaults to True
        Upon a successful login, stores the credentials in the default 
        user configuration file.  

    user_settings: optional, Settings, defaults to None
        Optional user settings.

    """

    settings = user_settings or get_service(Settings)
    auth_svc = get_service(IAuthService)
    signed_token: Optional[str] = None

    if authn_provider is not None:
        if not auth_svc.available(authn_provider):
            raise RuntimeError(f"Authentication flow for {authn_provider} is not available at the moment.")

        id = settings.telemetry.id.hex
        addresses = auth_svc.compute_addresses(authn_provider, id)
        gc_principal_id, user_details = gc_flow(addresses)
        signed_principal = auth_svc.auth_token(gc_principal_id, user_details)
        signed_token = signed_principal.to_token()

    else:
        user_name: str = user_name or os.environ.get('SHAPELETS_CLIENT__USERNAME', None)
        password: str = password or os.environ.get('SHAPELETS_CLIENT__PASSWORD', None)

        if user_name is not None and password is not None:
            challenge = auth_svc.generate_challenge(user_name)
            token = crypto.sign_challenge(challenge.salt, challenge.nonce, password.encode('ascii'))
            signed_principal = auth_svc.verify_challenge(user_name, challenge.nonce, token)
            signed_token = signed_principal.to_token()
        else:
            # Try to log in with default host and user
            default_server = settings.client.default_server
            if default_server is not None:
                default_user = settings.client.clients.get(default_server).default_user
                if default_user is not None:
                    signed_token = settings.client.clients.get(default_server).users.get(default_user).signed_token
                    if signed_token is not None:
                        if auth_svc.verify(signed_token):
                            signed_principal = SignedPrincipalId.from_token(signed_token)
                        else:
                            defaults(signed_token=None)  # Remove it from file
                            raise RuntimeError("Invalid cached credentials.  Please login again.")
                else:
                    raise RuntimeError("Invalid cached credentials.  Please login again.")
            else:
                raise RuntimeError("Invalid cached credentials.  Please login again.")

    if signed_token is None:
        raise RuntimeError("No login credentials.")

    if remember_me:
        current_host = str(settings.client.clients.get(settings.client.default_server).host)
        current_port = settings.client.clients.get(settings.client.default_server).port
        user_name = user_name if user_name is not None else default_user
        client = {
            current_host: {
                "host": current_host,
                "port": current_port,
                "users": {
                    user_name: {
                        "user_id": signed_principal.userId,
                        "signed_token": signed_token
                    }
                }
            }
        }
        defaults(clients=client)

    session: PrefixedSession = get_service_optional(Session)
    if session is not None:
        session.set_authorization(signed_token)


def _find_host(server: str):
    """
    Given a server that could be an alias of the server or the actual address, return its host.
    """
    full_host = urlparse(server)
    if all([full_host.scheme, full_host.netloc]) and len(full_host.netloc.split(".")) > 1:
        # url is valid
        host = str(full_host.hostname)
    else:
        # Look for alias
        settings = get_service(Settings)
        alias_host = settings.client.clients.get(server)
        if alias_host:
            host = str(alias_host.host)
        else:
            raise ValueError(f"Server alias {server} not found.")
    return host


def register(user_name: str = None, password: str = None, user_details: Optional[UserAttributes] = None,
             also_login: bool = True, remember_me: bool = True, force: bool = False,  transfer_user: str = None,
             server: str = None, default_user: bool = False):
    """
    Registers a new user in Shapelets

    Parameters
    ----------
    user_name: str, required
        New username.  This name should be unique in the system

    password: str, required
        Password associated with the new user 

    user_details: UserAttributes, optional
        User profile

    also_login: bool, defaults to True 
        Executes a login right after the registration

    remember_me: bool, defaults to True 
        Only used if `also_login` is set

    force: bool, defaults to False 
        Set this flag to overwrite the user attributes if the user already exists. Careful, if the user has active
        dataApps, these dataApps will be removed unless the transfer_user parameter is used.

    transfer_user: str, defaults to None
        In case of overwriting the user attributes with the flag force, use this parameter to select the user who will
        become the owner of any dataApp belonging to the user being overwrite.

    server: str, optional
        Alias or full address where the user will be added. If empty, user will be added to the default server.

    default_user: bool, defaults to False
        Make user default user for the given server.
    """
    if server is not None:
        host = _find_host(server)
        auth_svc = get_service(IAuthService, host)
    else:
        auth_svc = get_service(IAuthService)
        if hasattr(auth_svc, "session"):
            # Easier to find host from session
            host = str(urlparse(auth_svc.session.prefix_url).hostname)
        else:
            # Else, try to find default host in settings.
            settings = get_service(Settings)
            if settings.client.default_server is not None:
                host = str(settings.client.clients[settings.client.default_server].host)
            else:
                raise ValueError(f"Unable to find a host where user {user_name} should be added. Please, provide a host to the register funtion or add a default server.")

    if user_name is None or password is None:
        # Use terminal to ask for info
        user_name = input("Enter user name: ")
        password = getpass.getpass("Enter user password: ")
        default_user = input("Use this user as default user for this server? Y/N ").lower().strip() == 'y'

    if auth_svc.user_name_exists(user_name):
        if force:
            result = auth_svc.remove_user(user_name, transfer_user)
            if not result:
                raise ValueError("Unable to remove user name")
        else:
            raise ValueError(
                "User name already exists. To force registration with new UserAttributes, set flag force to True.")

    salt = crypto.generate_salt()
    pk = crypto.derive_verify_key(salt, password.encode('ascii'))
    if not auth_svc.register(user_name, salt, pk, user_details):
        raise RuntimeError("Unable to register a new user")

    # extract new user information
    challenge = auth_svc.generate_challenge(user_name)
    token = crypto.sign_challenge(challenge.salt, challenge.nonce, password.encode('ascii'))
    signed_principal = auth_svc.verify_challenge(user_name, challenge.nonce, token)
    # Add user to configuration file.
    add_user_to_client(host, user_name, signed_principal, default_user)

    if also_login and hasattr(auth_svc, "session"):
        auth_svc.session.set_authorization(signed_principal.to_token())
        # This will be removed, as login will be deleted.
        # login(user_name=user_name, password=password, remember_me=remember_me)
    print(f"User {user_name} was created successfully.")


def unregister(user_name: str, server: str = None, transfer: str = None):
    """
    Unregisters an existing user in Shapelets

    Parameters
    ----------
    user_name: str, required
        Existing username.

    server: str, optional
        Alias or full address where the user will be added. If empty, user will be added to the default server.

    transfer: str, optional
        Provide a username to give ownership of all dataApps belonging to the user to be deleted that this user shared with any group.
        Note: all dataApps not shared with any group will be deleted, as the only belong to the user local space.

    """
    try:
        if server is not None:
            host = _find_host(server)
            auth_svc = get_service(IAuthService, host)
        else:
            auth_svc = get_service(IAuthService)
            if hasattr(auth_svc, "session"):
                # Easier to find host from session
                host = str(urlparse(auth_svc.session.prefix_url).hostname)
            else:
                # Else, try to find default host in settings.
                settings = get_service(Settings)
                if settings.client.default_server is not None:
                    host = str(settings.client.clients[settings.client.default_server].host)
                else:
                    raise ValueError(
                        f"Unable to find a host where user {user_name} should be added. Please, provide a host to the register funtion or add a default server.")

        if auth_svc.user_name_exists(user_name):
            result = auth_svc.remove_user(user_name, transfer)
            if not result:
                raise ValueError("Error happens while removing user name")
            remove_user_from_client(host, user_name)
        else:
            raise ValueError("User does not exist. Unable to unregister user name")
    except Exception as e:
        raise ValueError(e)


def list_current_groups() -> List[GroupProfile]:
    """
    List current groups available
    """
    groups_svc = get_service(IGroupsService)
    return groups_svc.get_all()


def list_current_users() -> List[UserProfile]:
    """
    List current users registered in Shapelets
    """
    user_svr = get_service(IUsersService)
    return user_svr.get_all()


def create_group(group_name: str, description: str = None) -> GroupProfile:
    """
    Create a new group for Shapelets

    Parameters
    ----------
    group_name: str, required
        Group name.

    description: str, optional
        Group description.
    """
    groups_svc = get_service(IGroupsService)
    return groups_svc.create(group_name, description)


def delete_group(group_name: str) -> str:
    """
    Delete a group from Shapelets

    Parameters
    ----------
    group_name: str, required
        Group name.
    """
    groups_svc = get_service(IGroupsService)
    return groups_svc.delete_group(group_name)


def add_user_to_group(user_name: str, groups: Union[List[str], str], write: bool = False):
    """
    Add a Shapelets user to an existed group

    Parameters
    ----------
    user_name: str, required
        Username.

    groups: str, optional
        List of group names where the user will be added.

    write: bool, optional
        Give user permission to modify dataApps from the group.
    """
    user_svr = get_service(IUsersService)
    user_svr.add_to_group(user_name, groups, write)


def remove_user_from_group(user_name: str, groups: Union[List[str], str]):
    """
    Remove a Shapelets user from the giving group/s

    Parameters
    ----------
    user_name: str, required
        Username.

    groups: str, optional
        List of group names where the user will be removed.
    """
    user_svr = get_service(IUsersService)
    user_svr.remove_from_group(user_name, groups)


def add_server(alias: str = "local",
               host: str = "127.0.0.1",
               port: int = 4567,
               protocol: Literal["http", "https"] = "http",
               default_server: bool = True):
    """
    Add a server instance to Shapelets. If execute empty, localhost will be registered.
    Warning: if adding an existing server, the old information will be replaced.

    Parameters
    ----------
    alias: str, required
        Alias for the server. This name will help to find the server in the future.

    host: str, optional
        Where the server is located.

    port: int, optional
        Which port does it bind to.

    protocol: int, optional
        Which protocol (http / https ) should be used to contact.

    default_server: bool, optional
        Set as default server.

    """
    url = f"{protocol}://{host}:{port}"
    # Send url to make sure we can log in before saving the server info.
    auth_svc = get_service(IAuthService, host=host, full_url=url)
    # Making sure the requested server is up
    server_up = _is_server_up(auth_svc.session)
    if not server_up:
        raise RuntimeError(f"No timely response from {url}")

    print(f"Trying to login in into {url}")
    user_name = input("Enter user name: ")
    password = getpass.getpass("Enter user password: ")
    default_user = input("Use this user as default user for this server? Y/N ").lower().strip() == 'y'

    challenge = auth_svc.generate_challenge(user_name)
    token = crypto.sign_challenge(challenge.salt, challenge.nonce, password.encode('ascii'))
    signed_principal = auth_svc.verify_challenge(user_name, challenge.nonce, token)
    signed_token = signed_principal.to_token()
    client = {
        alias: {
            "host": host,
            "port": port,
            "protocol": protocol,
            "default_user": user_name if default_user else None,
            "users": {
                user_name: {
                    "user_id": signed_principal.userId,
                    "signed_token": signed_token
                }
            }

        }
    }
    defaults(clients=client, default_server=alias if default_server else None)

    print(f"Server added successfully!")


def list_available_servers():
    """
    List available serves in the configuration.
    """
    return list_available_clients()

def get_ID():
    """
    Returns current installation ID
    """
    settings = get_service(Settings)
    return settings.telemetry.id
import os
from typing import Optional
from typing_extensions import Literal

from pathlib import Path
from pydantic import BaseModel, IPvAnyAddress, PositiveInt, FilePath, DirectoryPath, SecretStr
from uvicorn import Config

from .http import HttpSettings
from .websocket import WebSocketSettings
from .reload import ReloadSettings
from .ssl import SSLSettings
from ..utils import FlexBytes


class ServerSettings(BaseModel):
    """
    Settings for local server instantiation
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

    uds: Optional[FilePath] = None
    """
    Bind to a UNIX domain socket. Useful if you want to run behind a reverse proxy.
    """

    fd: Optional[PositiveInt] = None
    """
    Bind to socket from this file descriptor. Useful if you want to run within a process manager.
    """

    static: Optional[DirectoryPath] = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'www'))
    """
    Path to the static files
    """

    loop: Literal['auto', 'asyncio', 'uvloop'] = 'auto'
    """
    Set the event loop implementation. The uvloop implementation 
    provides greater performance, but is not compatible with 
    Windows or PyPy.
    """

    limit_concurrency: Optional[PositiveInt] = None
    """
    Maximum number of concurrent connections or tasks to allow, before issuing 
    HTTP 503 responses.
    """

    limit_max_requests: Optional[PositiveInt] = None
    """
    Maximum number of requests to service before terminating the process.
    """

    backlog: Optional[PositiveInt] = None
    """
    Maximum number of connections to hold in backlog
    """

    timeout_keep_alive: Optional[PositiveInt] = None
    """
    Close Keep-Alive connections if no new data is received within this timeout
    """

    http: Optional[HttpSettings] = None
    """
    HTTP settings
    """

    ws: Optional[WebSocketSettings] = None
    """
    WebSocket settings
    """

    reload: ReloadSettings = ReloadSettings(enabled=False)
    """
    Settings to reload on changes
    """

    ssl: Optional[SSLSettings] = None
    """
    Secure socket settings
    """

    secret: Optional[SecretStr] = None
    """
    Secret used for generating a public-private sign pair used for 
    certified sessions secure tokens
    
    If this is unset, a new random secret will be created each time 
    the server starts, resulting in all stored tokens or sessions 
    in cookies to be invalidated.
    
    Normally this variable will be set by the virtual environment 
    through an environment variable `SHAPELETS_SERVER__SECRET`
    """

    salt: Optional[FlexBytes] = None
    """
    Salt used along side secret to generate the cryptographic pair
    """

    class Config:
        json_encoders = {
            FlexBytes: lambda v: str(v)
        }


def update_uvicorn_settings(server: ServerSettings, uviCfg: Config):
    """
    Translates a configuration object to an uvicorn configuration object, 
    respecting default values set by uvicorn.
    """

    if server.host is not None:
        uviCfg.host = server.host.compressed

    if server.port is not None:
        uviCfg.port = server.port

    if server.uds is not None:
        uviCfg.uds = str(server.uds)

    if server.fd is not None:
        uviCfg.fd = server.fd

    if server.loop is not None:
        uviCfg.loop = server.loop

    if server.http is not None:
        httpSettings = server.http

        if httpSettings.protocol is not None:
            uviCfg.http = httpSettings.protocol

        if httpSettings.root_path is not None:
            uviCfg.root_path = httpSettings.root_path

        if httpSettings.server_header is not None:
            uviCfg.server_header = httpSettings.server_header

        if httpSettings.date_header is not None:
            uviCfg.date_header = httpSettings.date_header

        if httpSettings.proxy_headers is not None:
            uviCfg.proxy_headers = httpSettings.proxy_headers

        if httpSettings.forwarded_allow_ips is not None:
            if isinstance(httpSettings.forwarded_allow_ips, list):
                uviCfg.forwarded_allow_ips = ','.join([str(f) for f in httpSettings.forwarded_allow_ips])
            else:
                uviCfg.forwarded_allow_ips = "*"

        if httpSettings.headers is not None:
            uviCfg.headers = httpSettings.headers

    if server.ws is not None:
        wsSettings = server.ws
        if wsSettings.protocol is not None:
            uviCfg.ws = wsSettings.protocol

        if wsSettings.max_size is not None:
            uviCfg.ws_max_size = wsSettings.max_size

        if wsSettings.ping_interval is not None:
            uviCfg.ws_ping_interval = wsSettings.ping_interval

        if wsSettings.ping_timeout is not None:
            uviCfg.ws_ping_timeout = wsSettings.ping_timeout

        if wsSettings.per_message_deflate is not None:
            uviCfg.ws_per_message_deflate = wsSettings.per_message_deflate

    uviCfg.reload = server.reload.enabled
    if server.reload.enabled:
        if server.reload.dirs is not None:
            if isinstance(server.reload.dirs, list):
                uviCfg.reload_dirs = [Path(entry) for entry in server.reload.dirs]
            else:
                uviCfg.reload_dirs = [Path(server.reload.dirs)]

        if server.reload.delay is not None:
            uviCfg.reload_delay = server.reload.delay

        if server.reload.includes is not None:
            if isinstance(server.reload.includes, list):
                uviCfg.reload_includes = server.reload.includes
            else:
                uviCfg.reload_includes = [server.reload.includes]

        if server.reload.excludes is not None:
            if isinstance(server.reload.excludes, list):
                uviCfg.reload_excludes = server.reload.excludes
            else:
                uviCfg.reload_excludes = [server.reload.excludes]

    if server.ssl is not None:
        sslSettings = server.ssl
        uviCfg.ssl_keyfile = str(sslSettings.keyfile)
        uviCfg.ssl_certfile = str(sslSettings.certfile)
        if sslSettings.keyfile_password is not None:
            uviCfg.ssl_keyfile_password = sslSettings.keyfile_password.get_secret_value()

        if sslSettings.version is not None:
            uviCfg.ssl_version = sslSettings.version

        if sslSettings.cert_reqs is not None:
            uviCfg.ssl_cert_reqs = sslSettings.cert_reqs

        if sslSettings.ca_certs is not None:
            uviCfg.ssl_ca_certs = str(sslSettings.ca_certs)

        if sslSettings.ciphers is not None:
            uviCfg.ssl_ciphers = sslSettings.ciphers

    return uviCfg

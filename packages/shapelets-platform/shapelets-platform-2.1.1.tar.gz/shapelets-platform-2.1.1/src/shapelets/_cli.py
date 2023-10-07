from typing import Optional

import argparse
# import argcomplete
import textwrap
import os
import sys
import traceback
import uuid
import pydantic
import tomlkit
import json
import shutil
import socket
import subprocess

from ipaddress import IPv4Address, IPv6Address
from string import Template
from urllib.parse import urlparse

from .svr import Settings, crypto, FlexBytes, UserAttributes, initialize_svr
from . import _api

try:
    import pwd
    import lockfile
    import daemon

    _on_windows = False
except:
    _on_windows = True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='shapelets', description='Shapelets Platform Tools')
    subparsers = parser.add_subparsers(dest='command')

    server_parser = subparsers.add_parser('server', help='Server tools')
    server_options = server_parser.add_subparsers(dest='server_command')

    # server show

    server_cfg_show = server_options.add_parser('show', help='Shows current configuration')
    server_cfg_show.add_argument('path', type=str,
                                 help="Working folder where the settings will be loaded from")
    server_cfg_show.add_argument('--plain-passwords', action='store_true',
                                 help='Show plain passwords')

    # server config

    server_cfg_options = server_options.add_parser(
        'config',
        help='Configures server settings',
        formatter_class=argparse.RawTextHelpFormatter,
        description='Creates a configuration file for a server',
        epilog=textwrap.dedent("""
        These settings may be also loaded from the environment, using the same
        names of these settings with `shapelets_server` prefix.

        For example, if host is not provided by the configuration file,
        it will try to resolve its value by reading an environment variable
        called `shapelets_server__host` (dashes are converted to
        underscores).

        Database settings can also be set through environment settings; for
        each of the options offered, the prefix will be `shapelets_database__`,
        followed with the name of the property (without `database`).  For
        example, `--database-memory-limit` will be looked up in the environment
        as `shapelets_database__memory_limit`.

        Environment values have lower priority over settings found in
        configuration files.

        """)
    )

    server_cfg_options.add_argument('destination', type=str,
                                    help="Folder where the settings will be saved")
    server_cfg_options.add_argument('--host', type=str,
                                    help="Address to bind the server")
    server_cfg_options.add_argument('--port', type=int,
                                    help="Port number of the server")
    if sys.platform != "win32":
        server_cfg_options.add_argument('--uds', type=str,
                                        help="Unix domain socket")
        server_cfg_options.add_argument('--fd', type=int,
                                        help="Bind to socket from this file descriptor")

    server_cfg_options.add_argument('--limit-concurrency', type=int,
                                    help="Maximum number of concurrent connections or tasks to allow, before issuing  HTTP 503 responses.")
    server_cfg_options.add_argument('--backlog', type=int,
                                    help="Maximum number of connections to hold in backlog.")
    server_cfg_options.add_argument('--timeout-keep-alive', type=int,
                                    help="Close Keep-Alive connections if no new data is received within this timeout.")

    server_cfg_options.add_argument('--ssl-keyfile', type=str, help='SSL key file')
    server_cfg_options.add_argument('--ssl-certfile', type=str, help='SSL certificate file')
    server_cfg_options.add_argument('--ssl-keyfile-password', type=str, help='SSL keyfile password')
    server_cfg_options.add_argument('--ssl-version', type=int, help='SSL version to use')
    server_cfg_options.add_argument('--ssl-cert-reqs', type=int,
                                    help='Whether client certificate is required')
    server_cfg_options.add_argument('--ssl-ca-certs', type=str, help='CA certificates file')
    server_cfg_options.add_argument('--ssl-ciphers', type=str, help='Ciphers to use')

    server_cfg_options.add_argument('--database-path', type=str,
                                    help='Path to the file containing the configuration database')
    server_cfg_options.add_argument('--database-temp-directory', type=str,
                                    help='Temporal directory for result handling and buffering')
    server_cfg_options.add_argument('--database-threads', type=int,
                                    help='Maximum number of threads to use in data processing operations')
    server_cfg_options.add_argument('--database-memory-limit', type=str,
                                    help='Maximum memory to use during memory operations.')

    # server run
    server_run_options = server_options.add_parser(
        'run',
        help='Runs the server',
        description="Runs the server using the current Python interpreter.")

    # server stop
    server_options.add_parser(
        'stop',
        help='Stops the server',
        description="Stops the server.")

    # if we are running on windows, disable the tools for daemons and systemd
    if not _on_windows:
        server_run_options.add_argument('--daemon', action='store_true', help='Run as a traditional *nix daemon')
        server_run_options.add_argument('--lock', type=str,
                                        help='Only used if daemon is used, it sets the location of the lock file',
                                        default='./shapelets.lock')
        server_run_options.add_argument('--log', type=str,
                                        help='Only used if daemon is used, it sets the location of the log file',
                                        default='./shapelets.log')
        server_run_options.add_argument('--pid', type=str,
                                        help='Only used if daemon is used, it sets the location of the pid file',
                                        default='./shapelets.pid')

        daemon_options = server_options.add_parser(
            'systemd',
            help='Generates daemon configuration for systemd',
            formatter_class=argparse.RawTextHelpFormatter,
            description=textwrap.dedent("""
            Generates a service template that runs a shapelets server using systemd.
            """),
            epilog=textwrap.dedent("""
            Creating service templates may require sudo permissions, since
            it will try to write the template to /etc/systemd/system/

            You may change the template destination using argument -d, providing
            a folder where to store the template.

            To start a server
            -----------------
            If the service has been named `shapelets`:

                systemctl enable shapelets
                systemctl daemon-reload
                systemctl start shapelets

            To query a server
            -----------------
                systemctl status shapelets

            To stop a server
            ----------------
                systemctl stop shapelets

            To remove a server
            ------------------
                systemctl disable shapelets
                rm /etc/systemd/system/shapelets.service
                rm /usr/lib/systemd/system/shapelets.service
                systemctl daemon-reload
                systemctl reset-failed

            """))

        daemon_options.add_argument('-n', '--name', type=str,
                                    default='shapelets',
                                    help='Name of the service template')

        daemon_options.add_argument('-w', '--wrk', type=str,
                                    help='Working directory')

        daemon_options.add_argument('-u', '--usr', type=str,
                                    help='User running the server')

        daemon_options.add_argument('-g', '--grp', type=str,
                                    help='Group to run the server')

        daemon_options.add_argument('-d', '--dst', type=str,
                                    default='/etc/systemd/system/',
                                    help='Folder to store the service template (/etc/systemd/system/).', )

    client_parser = subparsers.add_parser('client', help='Client Defaults')
    which_server = client_parser.add_mutually_exclusive_group(required=True)
    which_server.add_argument("--local", action="store_true", help='Use Local server')
    which_server.add_argument("--url", type=str, help='URL of the server to connect to')

    client_parser.add_argument("-u", "--usr", type=str, help='User Name')
    client_parser.add_argument("-p", "--pwd", type=str, help='User Password')
    client_parser.add_argument("--create", action="store_true", help='Create user if not exists')
    client_parser.add_argument("--remember-me", action="store_true", help='Logon and remember credentials')
    # client_parser.add_argument("--enable-telemetry", action="store_true", help='Enable telemetry')
    # client_parser.add_argument("--disable-telemetry", action="store_true", help='Disable telemetry')
    return parser


def resolve_host(expression: str) -> Optional[str]:
    try:
        return str(IPv4Address(expression))
    except:
        pass

    try:
        return str(IPv6Address(expression))
    except:
        pass

    try:
        return socket.gethostbyname(expression)
    except:
        return None


def process_client(data: argparse.Namespace):
    # change the current directory to user's home
    home_dir = os.path.expanduser('~/.shapelets')
    os.makedirs(home_dir, exist_ok=True)
    os.chdir(home_dir)

    # and load from here the settings
    current_settings = Settings()

    # get the doc
    settings_file = os.path.join(home_dir, 'settings.toml')
    if os.path.exists(settings_file):
        with open(settings_file, "rt", encoding="utf-8") as handle:
            doc = tomlkit.load(handle)
    else:
        doc = tomlkit.document()

    if 'telemetry' not in doc:
        telemetry_doc = tomlkit.table()
        doc['telemetry'] = telemetry_doc
    else:
        telemetry_doc = doc['telemetry']

    if 'client' not in doc:
        client_doc = tomlkit.table()
        doc['client'] = client_doc
    else:
        client_doc = doc['client']

    # enable or disable telemetry
    # if data.enable_telemetry:
    #     telemetry_doc['enabled'] = True
    #
    # if data.disable_telemetry:
    #     telemetry_doc['enabled'] = False

    # if no url is provided, move to the home user
    # settings to load the current settings for the
    # local server
    if data.url is None:
        host = str(current_settings.server.host)
        if host == '0.0.0.0':
            host = '127.0.0.1'
        elif host == '::':
            host = '::1'
        port = current_settings.server.port
        protocol = 'http' if current_settings.server.ssl is None else 'https'
    else:
        protocol, netloc, _, _, _, _ = urlparse(data.url)
        if ':' in netloc:
            host, port = netloc.split(':')
        else:
            host = netloc
            port = 443 if protocol == 'https' else 80

    ip = resolve_host(host)
    if ip is None:
        raise ValueError(f'Unable to resolve host {host}')
    if ip != host:
        print(f"{host} resolved to {ip}")

    client_doc['server_mode'] = 'out-of-process'
    client_doc['host'] = ip
    client_doc['port'] = int(port)
    client_doc['protocol'] = protocol

    # save the new settings
    with open(settings_file, "wt", encoding="utf-8") as handle:
        tomlkit.dump(doc, handle)

    # now deal with the user
    if data.create or data.remember_me:
        # so we have the settings, now we can initialise the server
        initialize_svr('headless' if data.local else 'out-of-process')

        usr = data.usr or os.environ.get('SHAPELETS_CLIENT__USERNAME', None)
        pwd = data.pwd or os.environ.get('SHAPELETS_CLIENT__PASSWORD', None)

        if data.create:
            if usr is None or pwd is None:
                raise ValueError("No username or password found")
            user_attributes = UserAttributes(nickName=usr)
            _api.register(usr, pwd, user_attributes, data.remember_me, data.remember_me, True)

        elif data.remember_me:
            if usr is None or pwd is None:
                raise ValueError("No username or password found")
            _api.login(user_name=usr, password=pwd, remember_me=data.remember_me)


def process_server_show(data: argparse.Namespace):
    os.chdir(data.path)
    settings = Settings()
    svr = settings.server
    db = settings.database

    svr_json_str = svr.json(exclude_unset=False,
                            models_as_dict=True,
                            exclude_defaults=False,
                            exclude_none=True,
                            encoder=lambda o: o.get_secret_value() if data.plain_passwords and isinstance(o, pydantic.SecretStr) else str(o))

    db_json_str = db.json(exclude_unset=False,
                          models_as_dict=True,
                          exclude_defaults=False,
                          exclude_none=True,
                          encoder=lambda o: o.get_secret_value() if data.plain_passwords and isinstance(o, pydantic.SecretStr) else str(o))

    print(tomlkit.dumps({'server': json.loads(svr_json_str), 'database': json.loads(db_json_str)}))


def process_server_config(data: argparse.Namespace):
    dst = data.destination
    dst = os.path.expanduser(os.path.expandvars(dst))
    os.makedirs(dst, exist_ok=True)

    # keep randomized settings on
    # or create them if they do not exist
    os.chdir(dst)
    current_settings = Settings()

    salt = current_settings.server.salt or FlexBytes(crypto.generate_salt())
    secret = current_settings.server.secret or pydantic.SecretStr(crypto.generate_random_password().decode('ascii'))
    teleId = current_settings.telemetry.id or uuid.uuid4()

    # take a backup of the settings
    settings_file = os.path.join(dst, 'settings.toml')
    settings_file_backup = os.path.join(dst, 'settings.toml.back')

    if os.path.exists(settings_file):
        shutil.copy2(settings_file, settings_file_backup)

    # iterate through the properties
    dbProperties = set(['path', 'temp_directory', 'treads', 'memory_limit'])
    sslProperties = set(['keyfile', 'certfile', 'keyfile_password', 'version', 'cert_reqs', 'ca_certs', 'ciphers'])
    serverProperties = set(['host', 'port', 'limit_concurrency', 'backlog', 'timeout_keep_alive'])

    server = {k: getattr(data, k) for k in serverProperties if k in data and getattr(data, k) is not None}
    # salt and secret should be propagated
    server['salt'] = str(salt)
    server['secret'] = secret.get_secret_value()

    ssl = {k: getattr(data, ('ssl_' + k))
           for k in sslProperties
           if ('ssl_' + k) in data and getattr(data, ('ssl_' + k)) is not None}

    db = {k: getattr(data, ('database_' + k))
          for k in dbProperties
          if ('database_' + k) in data and getattr(data, ('database_' + k)) is not None}

    if len(ssl) > 0:
        server['ssl'] = ssl

    # build the new config object
    new_cfg = {'server': server, 'database': db, 'telemetry': {'id': str(teleId)}}
    # dump it

    with open(settings_file, "wt", encoding="utf-8") as handle:
        handle.truncate()
        tomlkit.dump(new_cfg, handle)


def process_server_run(data: argparse.Namespace):
    run_classic_daemon = ('daemon' in data and data.daemon) or False
    if _on_windows or not run_classic_daemon:
        initialize_svr('standalone')
    else:
        pid_path = os.path.realpath(os.path.expanduser(data.pid))
        lock_path = os.path.realpath(os.path.expanduser(data.lock))
        log_path = os.path.realpath(os.path.expanduser(data.log))

        lock = lockfile.FileLock(lock_path)
        log = open(log_path, 'wt')

        print('Running Shapelets as a daemon:')
        print(f'\tLock file: {lock_path}')
        print(f'\tLog file : {log_path}')
        print(f'\tPid file : {pid_path}')
        print()
        print('To stop it:')
        print(f'\tcat {pid_path} | xargs kill')

        with daemon.DaemonContext(pidfile=lock, stderr=log):
            initialize_svr('standalone', pid_file=pid_path)


def process_server_stop():
    pid_path = os.path.join(os.path.expanduser('~/.shapelets'), 'shapelets.pid')
    if _on_windows:
        with open(pid_path, "r") as f:
            pid = f.read()
        cmd_str = f'taskkill /F /PID {pid}'
    else:
        cmd_str = f'cat {pid_path} | xargs kill'
    result = subprocess.run(cmd_str, shell=True)
    if result.returncode == 0:
        print('Shapelets Server stopped.')


def get_current_user_and_group():
    data = pwd.getpwuid(os.getuid())
    return data[0], data[3]


def get_current_user():
    data = pwd.getpwuid(os.getuid())
    return data[0]


def process_server_systemd(data: argparse.Namespace):
    dst = data.dst or '/etc/systemd/system/'
    name = data.name or 'shapelets-server'

    user = data.usr or get_current_user()
    all_users = {x.pw_name: (x.pw_uid, x.pw_dir) for x in pwd.getpwall()}
    if user not in all_users:
        raise ValueError(f"Unknown user name {user}")

    group = data.grp or all_users[user][0]
    work_dir = data.wrk or all_users[user][1]
    work_dir = os.path.abspath(os.path.expanduser(work_dir))

    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'systemd_template.txt')

    with open(template_path) as t:
        template = t.read()

        rendered = Template(template).substitute({
            'working_dir': work_dir,
            'python_exe': sys.executable,
            'user': user,
            'group': group,
            'sys_log_id': name
        })

        output_file = os.path.join(dst, f'{name}.service')
        with open(output_file, "wt") as o:
            o.truncate()
            o.write(rendered)
    print()
    print(f'File {output_file} created.')


def process_server(data: argparse.Namespace):
    if data.server_command == 'show':
        process_server_show(data)
    elif data.server_command == 'config':
        process_server_config(data)
    elif data.server_command == 'run':
        process_server_run(data)
    elif data.server_command == 'stop':
        process_server_stop()
    else:
        process_server_systemd(data)


def cli() -> None:
    parser = build_parser()
    # argcomplete.autocomplete(parser)
    # data = parser.parse_args(['client', '--url', 'http://localhost:4567', '-u', 'admin', '-p', 'admin', '--create'])
    data = parser.parse_args()
    if data.command is None or data.command == 'server' and data.server_command is None:
        parser.print_help()
        exit(-1)

    try:
        if data.command == 'server':
            process_server(data)
        else:
            process_client(data)
    except Exception as err:
        parser.print_help()
        print(str(err))
        traceback.print_exc()
        print()
        exit(-1)

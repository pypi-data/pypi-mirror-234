from pathlib import Path
from typing import Optional
from setuptools import setup
from setuptools.command.install import install
import atexit
import os
import uuid
import sys
import datetime as dt
import json

setup_dir = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(os.path.dirname(setup_dir))
write_to = os.path.join(setup_dir, 'src/shapelets/_version.py')


def python_version() -> str:
    """
    Generates a normalized string to report Python's version
    """
    psize = {2 ** 31 - 1: '32 bit', 2 ** 63 - 1: '64 bit'}.get(sys.maxsize) or 'unknown bits'
    version = "{0}.{1}.{2}.{3}.{4}".format(*sys.version_info)
    return "{0} ({1})".format(version, psize)


def shapelets_version():
    """
    Get Shapelets version
    """
    from setuptools_scm import get_version
    return get_version(root, 'guess-next-dev', 'no-local-version', write_to)


def user_language():
    import locale
    locale.setlocale(locale.LC_ALL, "")
    language = locale.getlocale(locale.LC_MESSAGES)[0]
    return language.replace("_", "-").lower()


def load_id(settings: str) -> Optional[uuid.UUID]:
    """
    Load the client anonymous id from the settings file 
    """
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib

    data = tomllib.loads(settings)
    if 'telemetry' in data:
        tel_data = data['telemetry']
        if 'id' in tel_data:
            return uuid.UUID(tel_data['id'])

    return None


def complete_install():
    """
    Completes the installation process by generating a instrumentation 
    event recording the installation time and the version installed; 
    if it detects a new installation, it will try to open a browser 
    window to the onboarding page.
    """
    home_path = os.path.expanduser("~/.shapelets")
    settings = os.path.join(home_path, "settings.toml")
    new_install = True
    id: Optional[uuid.UUID] = None

    if os.path.exists(settings):
        settings_txt = Path(settings).read_text(encoding="utf-8")
        id = load_id(settings_txt)
        new_install = False

    installation_event = {
        'install_ts': dt.datetime.now(dt.timezone.utc).isoformat(),
        'python_version': python_version(),
        'shapelets_version': shapelets_version(),
        'new_installation': new_install
    }

    if id is not None:
        installation_event['cid'] = id

    with open(os.path.join(home_path, 'install-info.json'), "w") as f:
        json.dump(installation_event, f, indent=4, sort_keys=True, default=str)

    # Activate when the landing page is ready
    #
    # if id is not None and new_install:
    #     import webbrowser
    #     webbrowser.open(f"https://shapelets.io/enroll?cid={id}&lang={user_language()}")


def stop_local_server():
    import psutil

    shapelets_dir = os.path.expanduser('~/.shapelets')
    system_pid = os.path.join(shapelets_dir, 'shapelets.pid')

    #
    # Stop current server, if any. If the server is running,
    # its PID is storedin ~/.shapelets/shapelets.pid
    #

    if os.path.exists(system_pid):

        with open(system_pid, 'rt') as f:

            try:

                # The file could be corrupt, and this could throw
                pid = int(f.read())

                server = psutil.Process(pid)
                for child in server.children(recursive=True):
                    child.terminate()
                server.terminate()

            except:
                pass
            finally:
                f.close()
                os.remove(system_pid)


class PostInstallCommand(install):
    def run(self):
        stop_local_server()
        install.run(self)
        atexit.register(complete_install)


setup(
    cmdclass={
        'install': PostInstallCommand
    },
    use_scm_version={
        'root': root,
        'write_to': write_to,
        'version_scheme': "guess-next-dev",
        "local_scheme": "no-local-version"
    }
)

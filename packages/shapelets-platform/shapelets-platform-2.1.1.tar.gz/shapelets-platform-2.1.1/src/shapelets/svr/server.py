from typing import Callable, Optional, Union

import os
import warnings
import functools
import asyncio
import threading

from uvicorn import Config as UviConfig
from uvicorn.server import Server as UviServer

from .settings import Settings, update_uvicorn_settings


try:
    # ensure we are running with uvloop if possible
    import uvloop
    # by registering it as the engine behind asyncio
    uvloop.install()
except ModuleNotFoundError:
    if os.name != 'nt':
        warnings.warn("Running without uvloop", UserWarning)


class InProcServer:
    """
    Class handling a in-process ASGI web server based on uvicorn

    Notes
    -----
    The server runs on a separated thread, on its own event loop.
    """
    __slots__ = ['__daemon', '__server', '__loop']

    def __init__(self) -> None:
        self.__daemon: Optional[threading.Thread] = None
        self.__server: Optional[UviServer] = None
        self.__loop: Optional[asyncio.AbstractEventLoop] = None

    def __run(self, config: UviConfig):
        self.__server = UviServer(config)
        self.__loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(self.__loop)
            return self.__loop.run_until_complete(self.__server.serve())
        finally:
            self.__loop.close()
            self.__loop = None
            self.__server = None

    @staticmethod
    def __stop(server: UviServer):
        server.should_exit = True

    def start(self, config: UviConfig):
        """
        Starts a new server 

        Parameters
        ----------
        config: uvicorn configuration object
            Configuration settings
        """
        if config is None:
            raise ValueError("Configuration is required.")

        if self.__daemon is not None:
            raise RuntimeError("Daemon thread already exists.")

        self.__daemon = threading.Thread(target=self.__run, daemon=True, name="api-thread", args=(config,))
        self.__daemon.start()

    def join(self, timeout: Optional[float] = None):
        """
        Asks the server to stop and waits until termination

        Parameters
        ----------
        timeout: float, optional, defaults to None
            Time in seconds to wait for the background thread 
            to terminate.  When set to None, it waits 
            forever until termination.

        """
        loop = self.__loop
        if loop is None:
            raise RuntimeError("No event loop")

        server = self.__server
        if server is None:
            raise RuntimeError("No server")

        callback = functools.partial(InProcServer.__stop, server)
        handle = loop.call_soon_threadsafe(callback)

        if self.__daemon is None:
            raise RuntimeError("No daemon")

        self.__daemon.join(timeout)
        if self.__daemon.is_alive():
            handle.cancel()
            raise RuntimeError("Unable to stop event loop thread in a timely manner.")

        self.__daemon = None


def launch_in_process(app: Union[Callable, str], cfg: Settings) -> InProcServer:
    """
    Starts an in-process server
    """
    in_proc = InProcServer()
    in_proc.start(update_uvicorn_settings(cfg.server, UviConfig(app)))
    return in_proc


def run_dedicated(app: Union[Callable, str], cfg: Settings, pid_file: Optional[str] = None):
    """
    Runs a Uvicorn server in a dedicated manner, blocking the process.
    """
    
    svr_pid = str(os.getpid())
    
    if pid_file :
        
        with open(pid_file, 'wt') as f:
            f.truncate()
            f.write(svr_pid)
           
    #
    # Store the process PID on 'shapelets.pid', so it can be easily
    # retrieved (for instance, if the process needs to be shut down)
    #
    shapelets_dir = os.path.expanduser('~/.shapelets')
    system_pid = os.path.join(shapelets_dir, 'shapelets.pid')
    
    with open(system_pid, 'wt') as f:
        f.truncate()
        f.write(svr_pid)
        
    server = UviServer(update_uvicorn_settings(cfg.server, UviConfig(app)))
    server.run()


__all__ = ['launch_in_process', 'run_dedicated']

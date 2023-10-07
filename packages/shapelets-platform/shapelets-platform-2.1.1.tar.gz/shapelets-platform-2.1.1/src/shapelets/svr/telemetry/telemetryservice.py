import os
import json
import urllib3

from requests import Session
from urllib.parse import urljoin

from .itelemetryservice import ITelemetryService
from ..settings import Settings
from .sysinfo import system_info

urllib3.disable_warnings()


class TelemetrySession(Session):
    def __init__(self, gc_server: str, *args, **kwargs):
        self.prefix_url = f'https://{gc_server}/tel/'
        super().__init__(*args, **kwargs)

    def request(self, method, url, *args, **kwargs):
        actual_url = urljoin(self.prefix_url, url)
        return super().request(method, actual_url, verify=False, timeout=1, *args, **kwargs)


class TelemetryService(ITelemetryService):
    __slots__ = ('_session', '_id')

    def __init__(self, settings: Settings) -> None:
        self._session = TelemetrySession(settings.grand_central)
        self._id = str(settings.telemetry.id)
        super().__init__()

    def library_loaded(self):
        # check if there is an installation event
        home_path = os.path.expanduser("~/.shapelets")
        install_event_path = os.path.join(home_path, 'install-info.json')
        if os.path.exists(install_event_path):
            try:
                with open(install_event_path, "r") as f:
                    install_data = json.load(f)

                if 'cid' not in install_data:
                    install_data['cid'] = self._id

                self._session.put('identify', json=system_info(), params=install_data)
                os.remove(install_event_path)
            except:
                pass
        else:
            try:
                self._session.put('track', params={
                    'id': self._id,
                    'event': 'library_loaded'
                })
            except:
                pass

    def send_telemetry(self, event: str, info: dict = None) -> None:
        """
        Send telemetry info to Grand Central
        param event: string with the event name,
        param info: dictionary containing extra data from the event
        """
        try:
            self._session.put('track', params={'id': self._id, 'event': event}, json=info)
        except Exception:
            # It seems there is no connection with GrandCentral or user is offline.
            # Avoid raising exception and just continue.
            pass

import tomlkit

from uuid import UUID, uuid4
from typing import Optional
from pydantic import BaseModel


class TelemetrySettings(BaseModel):
    """
    Telemetry settings
    """

    enabled: bool = True
    """
    Is telemetry enabled?
    """

    id: Optional[UUID] = None
    """
    Unique and opaque code that represents this shapelets installation.
    """


def telemetry_defaults(data: tomlkit.TOMLDocument, **kwargs):
    """
    Creates or updates a configuration file with new telemetry settings.

    Parameters
    ----------
    enable_telemetry: optional, boolean, defaults to None
        New default value when set; if this parameter is set to None, the configuration 
        file won't include any overrides over the default value.
    """

    # go to the section.
    if 'telemetry' not in data:
        section = tomlkit.table()
        data['telemetry'] = section
    else:
        section = data['telemetry']

    if 'id' not in section:
        section.add('id', str(uuid4()))

    if 'enable_telemetry' in kwargs:
        section['enabled'] = bool(kwargs['enable_telemetry'])

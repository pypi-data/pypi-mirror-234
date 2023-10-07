from typing import Optional
from typing_extensions import Literal

from pydantic import BaseModel, PositiveInt, PositiveFloat


class WebSocketSettings(BaseModel):
    protocol: Literal['auto', 'none', 'websockets', 'wsproto'] = 'auto'
    """
    Web sockets protocol implementation.
    Possible values are 'auto', 'none', 'websockets' or 'wsproto'
    """

    max_size: Optional[PositiveInt] = None
    """
    WebSocket max size message in bytes.
    """

    ping_interval: Optional[PositiveFloat] = None
    """
    WebSocket ping interval
    """

    ping_timeout: Optional[PositiveFloat] = None
    """
    WebSocket ping timeout
    """

    per_message_deflate: Optional[bool] = None
    """
    WebSocket per-message-deflate compression
    """

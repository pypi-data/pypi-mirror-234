from typing import Optional, Union, List, Tuple
from typing_extensions import Literal

from pydantic import BaseModel, IPvAnyAddress


class HttpSettings(BaseModel):
    protocol: Literal['auto', 'h11', 'httptools'] = 'auto'

    root_path: Optional[str] = None
    """
    Where to mount the site
    """

    server_header: Optional[bool] = None
    """
    Enable/Disable default Server header
    """

    date_header: Optional[bool] = None
    """
    Enable/Disable default Date header
    """

    proxy_headers: Optional[bool] = None
    """
    Enable/Disable X-Forwarded-Proto, X-Forwarded-For, X-Forwarded-Port to
    populate remote address info    
    """

    forwarded_allow_ips: Optional[Union[Literal['*'], List[IPvAnyAddress]]] = None
    """
    List of IPs to trust with proxy headers.
    '*' indicates all trusted
    """

    headers: Optional[List[Tuple[str, str]]] = None
    """
    Sets custom fixed headers on HTTP responses.  The default 
    value is empty (ie, no additional headers)
    """

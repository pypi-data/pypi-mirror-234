
from __future__ import annotations

from typing import Optional, Union, Dict
from typing_extensions import Literal

from pydantic import BaseModel

from .dynamic_credentials import RequiredToken, complete_settings


class AccessToken(BaseModel):
    """
    Authentication through an OAuth token.
    """

    service: str
    """
    Shapelets GC OAuth service
    """

    token: Optional[str] = None
    """
    Token received through federated authentication
    """

    cred_kind: Literal['token'] = 'token'

    def resolve(self, prefix: str, user_data: Dict[str, str]) -> Union[AccessToken, RequiredToken]:
        cfg, missing_fields = complete_settings(self, prefix, user_data)
        if len(missing_fields) > 0:
            return RequiredToken(env_prefix=prefix, fields=missing_fields, service=self.service)
        return cfg

import tomlkit
import tomlkit.items

from typing import Optional
from pydantic import BaseModel

from ..model import SignedPrincipalId


class UserSettings(BaseModel):
    """
    User settings.
    """
    signed_token: Optional[str] = None
    """
    Cached identity that can be persisted to disk.
    """

    user_id: Optional[str] = None
    """
    Cached user ID that can be persisted to disk.
    """


def user_defaults(**kwargs) -> tomlkit.items.Table:
    """
       Creates or updates a configuration file with default client connectivity settings

       To revert values to their configuration, set the parameter to None; if the value
       is not included in the call, no changes will be done to such parameter.  If the
       parameter has a value, it will override existing values and stored them in the desired
       file.

       Parameters
       ----------
        signed_token: optional, SignedPrincipalId
            User credentials.

        user_id: optional, string
            User ID.

       """
    section = tomlkit.table()

    if 'user' in kwargs:
        if 'signed_token' in kwargs['user'] and kwargs['user']['signed_token'] is not None:
            principal = kwargs['user']['signed_token']
            if isinstance(principal, SignedPrincipalId):
                principal = principal.to_token()
            if not isinstance(principal, str):
                raise ValueError("[signed_token] argument should be a string or SignedPrincipalId")
            section['signed_token'] = principal

        if 'user_id' in kwargs['user'] and kwargs['user']['user_id'] is not None:
            section['user_id'] = str(kwargs['user']['user_id'])

    return section

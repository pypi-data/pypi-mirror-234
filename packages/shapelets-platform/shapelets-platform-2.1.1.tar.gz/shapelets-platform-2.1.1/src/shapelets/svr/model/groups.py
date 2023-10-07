from pydantic import BaseModel
from typing import Optional, Set, Union
from typing_extensions import Literal


GroupField = Literal['uid', 'name', 'description']
GroupAllFields: Set[GroupField] = set(['uid', 'name', 'description'])
GroupId = Union[int, str]


class GroupAttributes(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class GroupProfile(GroupAttributes):
    uid: int

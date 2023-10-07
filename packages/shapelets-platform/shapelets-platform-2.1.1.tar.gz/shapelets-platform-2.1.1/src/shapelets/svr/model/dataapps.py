from pydantic import BaseModel
from typing import List, Optional, Set, Union
from typing_extensions import Literal

DataAppField = Literal[
    'uid', 'name', 'major', 'minor', 'description', 'creationDate', 'updateDate', 'specId', 'tags', 'userId']
DataAppAllFields: Set[DataAppField] = set(
    ['uid', 'name', 'major', 'minor', 'description', 'creationDate', 'updateDate', 'specId', 'tags', 'userId'])


class DataAppAttributes(BaseModel):
    name: str
    major: Optional[int]
    minor: Optional[int]
    description: Optional[str] = None
    creationDate: Optional[int] = None
    updateDate: Optional[int] = None
    specId: Optional[str] = None
    tags: Optional[list] = None
    userId: Optional[int] = None
    groups: Optional[Union[List[str], str]] = None
    functions: Optional[list] = None


class DataAppFunction(BaseModel):
    uid: str
    ser_body: str


class DataAppProfile(DataAppAttributes):
    uid: int

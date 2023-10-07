from pydantic import AnyUrl, BaseModel, EmailStr
from typing import List, Optional, Set, Union
from typing_extensions import Literal

UserField = Literal[
    'uid', 'nickName', 'email', 'firstName', 'familyName', 'locale', 'picture', 'bio', 'location', 'url']
UserAllFields: Set[UserField] = set(
    ['uid', 'nickName', 'email', 'firstName', 'familyName', 'locale', 'picture', 'bio', 'location', 'url'])
UserId = Union[int, str]


class UserAttributes(BaseModel):
    nickName: Optional[str] = None
    email: Optional[EmailStr] = None
    firstName: Optional[str] = None
    familyName: Optional[str] = None
    locale: Optional[str] = None
    picture: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    url: Optional[AnyUrl] = None
    groupIds: Optional[List[int]] = None


class UserProfile(UserAttributes):
    uid: int

from abc import ABC, abstractmethod
from typing import List, Optional, Set, Tuple, Union

from ..model import (
    PrincipalId,
    ResolvedPrincipalId,
    UserAttributes,
    UserAllFields,
    UserId,
    UserField,
    UserProfile
)


class UserDoesNotBelong(Exception):
    def __init__(self, user_name: str, group_name:str, *args: object) -> None:
        self._user_name = user_name
        self._group_name = group_name
        super().__init__(*args)

    def __str__(self) -> str:
        return f"User {self._user_name} does not belong to the group {self._group_name}."


class WritePermission(Exception):
    def __init__(self, user_name: str, group_name: str, *args: object) -> None:
        self._user_name = user_name
        self._group_name = group_name
        super().__init__(*args)

    def __str__(self) -> str:
        return f"User {self._user_name} has no write permission for {self._group_name} group."


class IUsersService(ABC):
    @abstractmethod
    def get_all(self,
                attributes: Optional[Set[UserField]] = UserAllFields,
                sort_by: Optional[List[Tuple[UserField, bool]]] = None,
                skip: Optional[int] = None,
                limit: Optional[int] = None) -> List[UserProfile]:
        pass

    @abstractmethod
    def create(self, attributes: UserAttributes, principal: Optional[PrincipalId]) -> UserProfile:
        pass

    @abstractmethod
    def add_to_group(self, user_name: str, groups: Union[List[str], str], write: bool = False) -> bool:
        pass

    @abstractmethod
    def remove_from_group(self, user_name: str, groups: Union[List[str], str]) -> bool:
        pass

    @abstractmethod
    def delete_user(self, uid: UserId):
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def get_user_details(self, user_ref: Union[UserId, PrincipalId]) -> Optional[UserProfile]:
        pass

    @abstractmethod
    def save_user_details(self, uid: UserId, details: UserAttributes) -> Optional[UserProfile]:
        pass

    @abstractmethod
    def nickname_exists(self, nickname: str) -> bool:
        pass

    @abstractmethod
    def get_principals(self, uid: UserId) -> List[PrincipalId]:
        pass

    @abstractmethod
    def dissociate_principal(self, principal: PrincipalId):
        pass

    @abstractmethod
    def verify_principal(self, resolved_principal: ResolvedPrincipalId) -> bool:
        pass

    @abstractmethod
    def resolve_principal(self, scope: str, pid: str) -> Optional[ResolvedPrincipalId]:
        pass

    # @abstractmethod
    # def get_user_groups(self, uid: UserId):
    #     pass

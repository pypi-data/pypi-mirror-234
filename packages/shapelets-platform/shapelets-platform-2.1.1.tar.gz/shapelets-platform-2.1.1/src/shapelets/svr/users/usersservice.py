from typing import List, Optional, Set, Tuple, Union

from .iusersrepo import IUsersRepo
from .iusersservice import IUsersService
from ..db import transaction
from ..model import (
    PrincipalId,
    ResolvedPrincipalId,
    UserAttributes,
    UserAllFields,
    UserId,
    UserField,
    UserProfile
)


class UsersService(IUsersService):
    __slots__ = ('_users_repo',)

    def __init__(self, users_repo: IUsersRepo) -> None:
        self._users_repo = users_repo

    def get_all(self,
                attributes: Optional[Set[UserField]] = UserAllFields,
                sort_by: Optional[List[Tuple[UserField, bool]]] = None,
                skip: Optional[int] = None,
                limit: Optional[int] = None) -> List[UserProfile]:

        attributes.add('uid')
        attributes.add('nickName')
        return self._users_repo.load_all(attributes, sort_by, skip, limit)

    def create(self, attributes: UserAttributes, principal: Optional[PrincipalId]) -> UserProfile:
        if attributes.nickName is None:
            raise ValueError("Invalid user name")
        with transaction():
            profile = self._users_repo.create(attributes)
            if principal is not None:
                self._users_repo.associate_principal(profile.uid, principal)
            return profile

    def add_to_group(self, user_name: str, groups: Union[List[str], str], write: bool = False) -> bool:
        if not isinstance(groups, list):
            groups = [groups]
        return self._users_repo.add_to_group(user_name, groups, write)

    def remove_from_group(self, user_name: str, groups:  Union[List[str], str]) -> bool:

        if not isinstance(groups, list):
            groups = [groups]
        return self._users_repo.remove_from_group(user_name, groups)

    def delete_user(self, uid: UserId):
        if isinstance(uid, str):
            return self._users_repo.delete_by_name(uid)
        return self._users_repo.delete_by_id(str(uid))

    def delete_all(self):
        self._users_repo.delete_all()

    def get_user_details(self, user_ref: Union[UserId, PrincipalId]) -> Optional[UserProfile]:
        if isinstance(user_ref, str):
            return self._users_repo.load_by_name(user_ref)
        if isinstance(user_ref, PrincipalId):
            return self._users_repo.load_by_principal(user_ref.scope, user_ref.id)
        return self._users_repo.load_by_id(int(user_ref))

    def save_user_details(self, id: UserId, details: UserAttributes) -> Optional[UserProfile]:
        if isinstance(id, str):
            return self._users_repo.update_by_name(id, details)
        return self._users_repo.update_by_id(int(id), details)

    def nickname_exists(self, nickname: str) -> bool:
        return self._users_repo.nickname_exists(nickname)

    def get_principals(self, uid: UserId) -> List[PrincipalId]:
        if isinstance(uid, str):
            return self._users_repo.principals_by_name(uid)
        return self._users_repo.principals_by_id(int(uid))

    def dissociate_principal(self, principal: PrincipalId):
        self._users_repo.dissociate_principal(principal)

    def verify_principal(self, resolved_principal: ResolvedPrincipalId) -> bool:
        return self._users_repo.association_exists(resolved_principal)

    def resolve_principal(self, scope: str, pid: str) -> Optional[ResolvedPrincipalId]:
        uid = self._users_repo.find_userId_by_principal(scope, pid)
        return None if uid is None else ResolvedPrincipalId(userId=uid, scope=scope, id=pid)

    # def get_user_groups(self, uid: UserId):
    #     pass

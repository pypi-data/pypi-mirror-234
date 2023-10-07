from abc import ABC, abstractmethod
from typing import List, Optional, Set, Tuple

from ..model import PrincipalId, ResolvedPrincipalId, UserAttributes, UserField, UserId, UserProfile


class IUsersRepo(ABC):

    @abstractmethod
    def create(self, details: UserAttributes) -> Optional[UserProfile]:
        pass

    @abstractmethod
    def add_to_group(self, user_name: str, groups: List[str], write: bool = False) -> bool:
        pass

    @abstractmethod
    def remove_from_group(self, user_name: str, groups: List[str]) -> bool:
        pass

    @abstractmethod
    def load_by_id(self, uid: UserId) -> Optional[UserProfile]:
        pass

    @abstractmethod
    def load_by_name(self, name: str) -> Optional[UserProfile]:
        pass

    @abstractmethod
    def load_by_principal(self, principal: PrincipalId) -> Optional[UserProfile]:
        pass

    @abstractmethod
    def delete_by_name(self, name: str):
        pass

    @abstractmethod
    def delete_by_id(self, uid: UserId):
        pass

    @abstractmethod
    def update_by_id(self, uid: UserId, new_details: UserAttributes) -> Optional[UserProfile]:
        pass

    @abstractmethod
    def update_by_name(self, name: str, new_details: UserAttributes) -> Optional[UserProfile]:
        pass

    @abstractmethod
    def nickname_exists(self, name: str) -> bool:
        pass

    @abstractmethod
    def load_all(self,
                 attributes: Optional[Set[UserField]] = None,
                 skip: Optional[int] = None,
                 sort_by: Optional[List[Tuple[UserField, bool]]] = None,
                 limit: Optional[int] = None) -> List[UserProfile]:
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def principals_by_name(self, name: str) -> List[PrincipalId]:
        pass

    @abstractmethod
    def principals_by_id(self, uid: UserId) -> List[PrincipalId]:
        pass

    @abstractmethod
    def associate_principal(self, uid: UserId, principal: PrincipalId) -> ResolvedPrincipalId:
        pass

    @abstractmethod
    def dissociate_principal(self, principal: PrincipalId):
        pass

    @abstractmethod
    def association_exists(self, rp: ResolvedPrincipalId) -> bool:
        pass

    @abstractmethod
    def find_user_id_by_principal(self, scope: str, pid: str) -> Optional[int]:
        pass

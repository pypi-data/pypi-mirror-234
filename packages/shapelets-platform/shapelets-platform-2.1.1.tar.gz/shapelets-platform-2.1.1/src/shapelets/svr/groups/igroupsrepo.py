from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from ..model import GroupAttributes, GroupField, GroupProfile, UserProfile


class IGroupsRepo(ABC):

    @abstractmethod
    def create(self, details: GroupAttributes) -> Optional[GroupProfile]:
        """
        Creates a new group
        param details: Group Attributes with the group details.
        """
        pass

    @abstractmethod
    def get_all(self,
                sort_by: Optional[List[Tuple[GroupField, bool]]] = None,
                limit: Optional[int] = None
                ) -> List[GroupProfile]:
        """
        Returns all the groups in the system.
        param sort_by: sort by any group attribute.
        param limit: max number of groups to return.
        """
        pass

    @abstractmethod
    def get_details(self, group_name: str) -> GroupProfile:
        """
        Provides with details from the requested group.
        param group_name
        """
        pass

    @abstractmethod
    def group_name_exists(self, group_name: str) -> bool:
        """
        Check if a group name already exists in the system
        param group_name
        """
        pass

    @abstractmethod
    def delete_by_id(self, uid: int):
        """
        Delete group providing its id.
        param uid
        """
        pass

    @abstractmethod
    def delete_by_name(self, group_name: str) -> str:
        """
        Delete group providing its name.
        param group_name
        """
        pass

    @abstractmethod
    def delete_all(self):
        """
        Delete all groups in the system
        """
        pass

    @abstractmethod
    def all_users_in_group(self, group_name: str) -> List[UserProfile]:
        """
        Returns all users belonging to the group.
        param group_name
        """
        pass

    @abstractmethod
    def has_privileges(self, group_name: str) -> bool:
        pass

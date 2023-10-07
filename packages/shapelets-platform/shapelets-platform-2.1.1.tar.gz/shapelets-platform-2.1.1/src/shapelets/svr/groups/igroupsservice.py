# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from ..model import GroupAttributes, GroupField, GroupProfile, UserProfile


class InvalidGroupName(Exception):
    def __init__(self, groupName: str, *args: object) -> None:
        self._groupName = groupName
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Invalid group name {self._groupName}"


class IGroupsService(ABC):
    @abstractmethod
    def create(self, attributes: GroupAttributes) -> GroupProfile:
        """
        Creates a new group

        Parameters
        ----------
        attributes: Group Attributes with the group details.

        Returns
        -------
        Group just created
        """
        pass

    @abstractmethod
    def get_all(self,
                sort_by: Optional[List[Tuple[GroupField, bool]]] = None,
                limit: Optional[int] = None
                ) -> List[GroupProfile]:
        """
        Returns all the groups in the system.

        Parameters
        ----------
        sort_by: sort by any group attribute.
        limit: max number of groups to return.

        Returns
        -------
        List of groups
        """
        pass

    @abstractmethod
    def get_details(self, group_name: str) -> GroupProfile:
        """
        Provides with details from the requested group.

        Parameters
        ----------
        group_name

        Returns
        -------
        Group Details
        """
        pass

    @abstractmethod
    def group_name_exists(self, group_name: str) -> bool:
        """
        Check if a group name already exists in the system

        Parameters
        ----------
        group_name

        Returns
        -------
        A boolean flag; when True, the group name exists.  False otherwise.
        """
        pass

    @abstractmethod
    def delete_group(self, group_name: str) -> str:
        """
        Delete group from the system

        Parameters
        ----------
        group_name
        """
        pass

    @abstractmethod
    def delete_all(self):
        """
        Delete ALL groups from the system
        """
        pass

    @abstractmethod
    def all_users_in_group(self, group_name: str) -> List[UserProfile]:
        """
        Returns all users belonging to the group.

        Parameters
        ----------
        group_name
        """
        pass

    @abstractmethod
    def has_privileges(self, group_name: str) -> bool:
        pass

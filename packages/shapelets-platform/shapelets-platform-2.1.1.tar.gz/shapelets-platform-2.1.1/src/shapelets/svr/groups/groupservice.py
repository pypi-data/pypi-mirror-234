# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import List, Optional, Tuple

from .igroupsrepo import IGroupsRepo
from .igroupsservice import IGroupsService

from ..db import transaction
from ..model import GroupAttributes, GroupField, GroupProfile, UserProfile


class GroupsService(IGroupsService):
    __slots__ = ('_groups_repo',)

    def __init__(self, groups_repo: IGroupsRepo) -> None:
        self._groups_repo = groups_repo

    def create(self, attributes: GroupAttributes) -> GroupProfile:
        with transaction():
            profile = self._groups_repo.create(attributes)
            return profile

    def get_all(self,
                sort_by: Optional[List[Tuple[GroupField, bool]]] = None,
                limit: Optional[int] = None
                ) -> List[GroupProfile]:
        return self._groups_repo.get_all(sort_by, limit)

    def get_details(self, group_name: str) -> GroupProfile:
        return self._groups_repo.get_details(group_name)

    def group_name_exists(self, group_name: str) -> bool:
        return self._groups_repo.group_name_exists(group_name)

    def delete_group(self, group_name: str) -> str:
        return self._groups_repo.delete_by_name(group_name)

    def delete_all(self):
        self._groups_repo.delete_all()

    def all_users_in_group(self, group_name: str) -> List[UserProfile]:
        self._groups_repo.all_users_in_group(group_name)

    def has_privileges(self, group_name: str) -> bool:
        self._groups_repo.has_privileges(group_name)

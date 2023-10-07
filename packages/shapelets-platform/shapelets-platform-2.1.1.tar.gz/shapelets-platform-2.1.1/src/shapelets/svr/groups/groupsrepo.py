# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations
from typing import List, Optional, Tuple, Union

from .igroupsrepo import IGroupsRepo
from ..db import connect, Connection, transaction
from ..model import GroupAttributes, GroupField, GroupProfile, UserProfile

GroupLike = Union[int, GroupProfile]


def get_id(group_like: Union[int, GroupProfile]) -> int:
    if isinstance(group_like, GroupProfile):
        return group_like.uid
    return int(group_like)


def _next_id(conn: Connection) -> int:
    conn.execute("SELECT nextval('shapelets.id_gen')")
    return int(conn.fetch_one()[0])


def _insert_group(uid: int, details: GroupAttributes, conn: Connection):
    conn.execute("""
            INSERT INTO groups 
            (uid,
            name,
            description) 
            VALUES (?, ?, ?);
        """,
                 [uid, details.name, details.description])


def _load_all(sort_by: Optional[List[Tuple[GroupField, bool]]],
              limit: Optional[int],
              conn: Connection) -> List[GroupProfile]:
    baseQuery = f"SELECT * FROM groups"
    if sort_by is not None:
        baseQuery += "ORDER BY "
        sortExpressions = [f"{s[0]} {'ASC' if s[1] else 'DESC'}" for s in sort_by]
        baseQuery += ', '.join(sortExpressions)
    if limit is not None:
        baseQuery += f" LIMIT {limit}"
    conn.execute(baseQuery)
    result = []
    for record in conn.fetch_all():
        result.append(GroupProfile(uid=record[0], name=record[1], description=record[2]))
    return result


def _load_group_by_id(uid: int, conn: Connection) -> Optional[GroupProfile]:
    conn.execute(""" 
        SELECT name, description
        FROM groups
        WHERE uid = ?;
    """, [uid])

    record = conn.fetch_one()
    if record is None:
        return None
    return GroupProfile(uid=uid, name=record[0], description=record[1])


def _load_group_by_name(group_name: str, conn: Connection) -> Optional[GroupProfile]:
    conn.execute(""" 
        SELECT *
        FROM groups
        WHERE name = ?;
    """, [group_name])

    record = conn.fetch_one()
    if record is None:
        return None
    return GroupProfile(uid=record[0], name=record[1], description=record[2])


def _delete_group_by_id(uid: int, conn: Connection):
    conn.execute("DELETE FROM groups WHERE uid = ?;", [uid])


def _delete_group_by_name(group_name: str, conn: Connection):
    conn.execute("DELETE FROM groups WHERE name = ?;", [group_name])
    conn.execute("DELETE FROM users_groups WHERE groupId = ?", [group_name])


def _clear_all_groups(conn: Connection):
    conn.execute("DELETE FROM groups;")


def _load_users_in_group(group_name: str, conn: Connection) -> Optional[UserProfile]:
    conn.execute(""" 
        SELECT *
        FROM users
        WHERE groupName = ?;
    """, [group_name])

    result = []
    for r in conn.fetch_all():
        result.append(GroupProfile(r))
    return result


def group_has_group_name(group_name: str, conn: Connection) -> bool:
    conn.execute("SELECT 1 FROM groups where name = ?", [group_name])
    result = conn.fetch_one()
    return None if result is None else int(result[0]) == 1


def _has_privileges(group_name: str, conn: Connection) -> bool:
    return True


class GroupsRepo(IGroupsRepo):

    def __init__(self) -> None:
        pass

    def create(self, details: GroupAttributes) -> Optional[GroupProfile]:
        with transaction() as conn:
            uid = _next_id(conn)
            _insert_group(uid, details, conn)
            return _load_group_by_id(uid, conn)

    def get_details(self, group_name: str) -> GroupProfile:
        with connect() as conn:
            return _load_group_by_name(group_name, conn)

    def group_name_exists(self, group_name: str) -> bool:
        with connect() as conn:
            return group_has_group_name(group_name, conn)

    def delete_by_id(self, uid: int):
        with connect() as conn:
            _delete_group_by_id(uid, conn)

    def delete_by_name(self, group_name: str) -> str:

        if self.group_name_exists(group_name):
            with connect() as conn:
                _delete_group_by_name(group_name, conn)
                return 'Group %s has been deleted' % group_name
        else:
            return 'Group %s does not exist' % group_name

    def delete_all(self):
        with connect() as conn:
            _clear_all_groups(conn)

    def get_all(self,
                sort_by: Optional[List[Tuple[GroupField, bool]]] = None,
                limit: Optional[int] = None
                ) -> List[GroupProfile]:
        with connect() as conn:
            return _load_all(sort_by, limit, conn)

    def all_users_in_group(self, group_name: str) -> List[UserProfile]:
        with connect() as conn:
            return _load_users_in_group(group_name, conn)

    def has_privileges(self, group_name: str) -> bool:
        return _has_privileges(group_name)

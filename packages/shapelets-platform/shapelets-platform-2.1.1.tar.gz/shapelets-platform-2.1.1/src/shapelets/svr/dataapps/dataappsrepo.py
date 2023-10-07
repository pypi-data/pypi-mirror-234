import os
import uuid

from datetime import datetime
from typing import List, Optional, Set, Tuple

from .idataappsrepo import IDataAppsRepo
from ..db import connect, Connection, transaction
from ..groups import InvalidGroupName
from ..model import DataAppAllFields, DataAppField, DataAppAttributes, PrincipalId
from ..model.dataapps import DataAppFunction, DataAppProfile
from ..users import UserDoesNotBelong, WritePermission

SH_DIR = os.path.expanduser('~/.shapelets')
DATAAPP_DIR = os.path.join(SH_DIR, 'dataAppsStore')
DATA_DIR = os.path.join(SH_DIR, 'data')


def _next_id(conn: Connection) -> int:
    conn.execute("SELECT nextval('shapelets.id_gen')")
    return int(conn.fetch_one()[0])


def _insert_dataapp(uid: int, details: DataAppAttributes, conn: Connection):
    spec_id = store_spec_file(details.specId)
    conn.execute("""
            INSERT INTO dataapps 
            (uid, name, major, minor, description, creationDate, updateDate, specId, tags, userId)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
                 [
                     uid, details.name, details.major, details.minor, details.description, details.creationDate,
                     details.updateDate, spec_id, details.tags, details.userId
                 ])


def _get_user_groups(user_id: int, conn: Connection):
    base_query = f"SELECT groupIds FROM users WHERE uid = {user_id}"
    conn.execute(base_query)
    return conn.fetch_one()[0]


def _load_all(user_id: int,
              attributes: Set[DataAppField],
              skip: Optional[int],
              sort_by: Optional[List[Tuple[DataAppField, bool]]],
              limit: Optional[int],
              conn: Connection) -> List[DataAppProfile]:
    base_query = f"SELECT {', '.join(attributes)} FROM dataapps "
    if sort_by is not None:
        base_query += "ORDER BY "
        sort_expressions = [f"{s[0]} {'ASC' if s[1] else 'DESC'}" for s in sort_by]
        base_query += ', '.join(sort_expressions)
    if limit is not None:
        base_query += f" LIMIT {limit}"
    if skip is not None:
        base_query += f" OFFSET {skip}"

    conn.execute(base_query)
    result = []
    d = {}
    for r in conn.fetch_all():
        for idx, a in enumerate(attributes):
            d[a] = r[idx]
        result.append(DataAppProfile(**d))

    return result


def store_spec_file(spec: str, old_spec_id: str = None) -> str:
    os.makedirs(DATAAPP_DIR, exist_ok=True)
    if old_spec_id is not None:
        remove_spec_file(old_spec_id)

    new_spec_id = str(uuid.uuid1())
    spec_path = os.path.join(DATAAPP_DIR, f"{new_spec_id}.json")

    with open(spec_path, 'wt') as f:
        f.write(spec)
    return new_spec_id


def remove_spec_file(spec_id: str):
    spec_path = os.path.join(DATAAPP_DIR, f"{spec_id}.json")
    os.remove(spec_path)


def remove_data(uid: int, conn: Connection):
    conn.execute("SELECT dataInfo FROM dataapp_data WHERE dataappId = ?;", [uid]);
    data_info = conn.fetch_all()
    if data_info is not None:
        # delete possible duplicates
        data_info = list(set(data_info))
        for widget_id in data_info:
            spec_path = os.path.join(DATA_DIR, f"{widget_id[0]}")
            os.remove(spec_path)
        conn.execute("DELETE FROM dataapp_data WHERE dataappId = ?;", [uid]);


def _user_local_dataapp_list(user_id, conn: Connection) -> Optional[DataAppProfile]:
    conn.execute("""
        SELECT dataapps.uid, dataapps.name, dataapps.major, dataapps.minor, dataapps.description, dataapps.creationDate,
        dataapps.updateDate, dataapps.specId, dataapps.tags, dataapps.userId
        from dataapps
        LEFT JOIN dataapp_group ON dataapps.uid = dataapp_group.dataappId
        WHERE dataapps.userId = ?
        AND NOT EXISTS(
        SELECT dataapp_group.dataappId 
        FROM dataapp_group 
        WHERE dataapp_group.dataappId = dataapps.uid);
    """, [user_id])
    result = []
    for record in conn.fetch_all():
        result.append(DataAppProfile(
            uid=record[0],
            name=record[1],
            major=record[2],
            minor=record[3],
            description=record[4],
            creationDate=record[5],
            updateDate=record[6],
            specId=record[7],
            tags=record[8],
            userId=record[9]
        ))
    return result


def _user_group_dataapp_list(user_id, conn: Connection) -> Optional[DataAppProfile]:
    conn.execute(""" 
            SELECT users_groups.groupId 
            from users_groups
            WHERE users_groups.userId = ?
        """, [user_id])
    group_result = conn.fetch_all()
    if not group_result or group_result is None:
        # User does not belong to any group
        return []
    group_ids = [group[0] for group in group_result]

    base_query = "SELECT distinct(dataappId) from dataapp_group"
    if len(group_ids) > 1:
        base_query += f" WHERE dataapp_group.groupId IN {tuple(group_ids)}"
    else:
        base_query += f" WHERE dataapp_group.groupId = {group_ids[0]}"

    conn.execute(base_query)

    result = []
    for record in conn.fetch_all():
        dataapp = _load_dataapp_by_id(record[0], conn)
        conn.execute(""" 
            SELECT distinct(groups.name)
            FROM groups
            INNER JOIN dataapp_group ON dataapp_group.groupId = groups.uid
            WHERE dataapp_group.dataappId = ?;
        """, [dataapp.uid])
        groups = conn.fetch_all()
        if groups is not None:
            dataapp.groups = [group[0] for group in groups]
        result.append(dataapp)
    return result


def _load_dataapp_by_name(dataapp_name: str, conn: Connection) -> Optional[DataAppProfile]:
    conn.execute(""" 
        SELECT uid, name, major, minor, description, creationDate, updateDate, specId, tags, userId
        FROM dataapps
        WHERE name = ?
        ORDER BY major desc, minor desc;
    """, [dataapp_name])

    record = conn.fetch_one()
    if record is None:
        return None

    return DataAppProfile(
        uid=record[0],
        name=record[1],
        major=record[2],
        minor=record[3],
        description=record[4],
        creationDate=record[5],
        updateDate=record[6],
        specId=record[7],
        tags=record[8],
        userId=record[9]
    )


def _load_dataapp_by_name_and_group(dataapp_name: str, group_id: int, conn: Connection) -> Optional[DataAppProfile]:
    conn.execute(""" 
        SELECT dataapps.uid, dataapps.name, dataapps.major, dataapps.minor, dataapps.description, dataapps.creationDate, 
        dataapps.updateDate, dataapps.specId, dataapps.tags, dataapps.userId
        FROM dataapps
        INNER JOIN dataapp_group ON dataapps.uid = dataapp_group.dataappId
        WHERE dataapps.name = ? and dataapp_group.groupId = ?
        ORDER BY major desc, minor desc;
    """, [dataapp_name, group_id])

    record = conn.fetch_one()
    if record is None:
        return None

    return DataAppProfile(
        uid=record[0],
        name=record[1],
        major=record[2],
        minor=record[3],
        description=record[4],
        creationDate=record[5],
        updateDate=record[6],
        specId=record[7],
        tags=record[8],
        userId=record[9]
    )


def _load_dataapp_by_name_version_and_user(dataapp_name: str,
                                           dataapp_major: int,
                                           dataapp_minor: int,
                                           user_id: int,
                                           conn: Connection) -> Optional[DataAppProfile]:
    conn.execute(""" 
        SELECT uid, name, major, minor, description, creationDate, updateDate, specId, tags, userId
        FROM dataapps
        WHERE name = ? AND major = ? AND minor = ? AND userId = ?;
    """, [dataapp_name, dataapp_major, dataapp_minor, user_id])

    record = conn.fetch_one()
    if record is None:
        return None

    return DataAppProfile(
        uid=record[0],
        name=record[1],
        major=record[2],
        minor=record[3],
        description=record[4],
        creationDate=record[5],
        updateDate=record[6],
        specId=record[7],
        tags=record[8],
        userId=record[9],
    )


def _load_dataapp_by_name_version_and_group(dataapp_name: str,
                                            dataapp_major: int,
                                            dataapp_minor: int,
                                            group_id: int,
                                            conn: Connection) -> Optional[DataAppProfile]:
    conn.execute("""
                SELECT uid, name, major, minor, description, creationDate, updateDate, specId, tags, userId
                FROM dataapps
                INNER JOIN dataapp_group ON dataapps.uid = dataapp_group.dataappId
                WHERE name = ? AND major = ? AND minor = ? AND dataapp_group.groupId = ?;
            """, [dataapp_name, dataapp_major, dataapp_minor, group_id])

    record = conn.fetch_one()
    if record is None:
        return None

    return DataAppProfile(
        uid=record[0],
        name=record[1],
        major=record[2],
        minor=record[3],
        description=record[4],
        creationDate=record[5],
        updateDate=record[6],
        specId=record[7],
        tags=record[8],
        userId=record[9],
    )


def _load_dataapp_by_name_and_user(dataapp_name: str, user_id: int, conn: Connection) -> Optional[DataAppProfile]:
    conn.execute(""" 
        SELECT uid, name, major, minor, description, creationDate, updateDate, specId, tags, userId
        FROM dataapps
        WHERE name = ? AND userId = ?
        ORDER BY major desc, minor desc;
    """, [dataapp_name, user_id])

    record = conn.fetch_one()
    if record is None:
        return None

    return DataAppProfile(
        uid=record[0],
        name=record[1],
        major=record[2],
        minor=record[3],
        description=record[4],
        creationDate=record[5],
        updateDate=record[6],
        specId=record[7],
        tags=record[8],
        userId=record[9]
    )


def _load_dataapp_by_name_and_version(dataapp_name: str,
                                      dataapp_major: int,
                                      dataapp_minor: int,
                                      conn: Connection) -> Optional[DataAppProfile]:
    conn.execute(""" 
        SELECT uid, name, major, minor, description, creationDate, updateDate, specId, tags, userId
        FROM dataapps
        WHERE name = ? AND major = ? AND minor = ?;
    """, [dataapp_name, dataapp_major, dataapp_minor])

    record = conn.fetch_one()
    if record is None:
        return None

    return DataAppProfile(
        uid=record[0],
        name=record[1],
        major=record[2],
        minor=record[3],
        description=record[4],
        creationDate=record[5],
        updateDate=record[6],
        specId=record[7],
        tags=record[8],
        userId=record[9]
    )


def _update_dataapp(dataapp_uid: int,
                    new_spec: str,
                    update_date: int,
                    old_spec_id: str,
                    conn: Connection):
    new_spec_id = store_spec_file(new_spec, old_spec_id)
    conn.execute(""" 
        UPDATE dataapps 
        SET specId = ? , updateDate = ?
        WHERE uid = ? ;
    """, [new_spec_id, update_date, dataapp_uid])


def _delete_dataapp(uid: int, user_id: int, conn: Connection) -> bool:
    dataapp = _load_dataapp_by_id(uid, conn)
    if not dataapp:
        raise RuntimeError("DataApp does exist")
    conn.execute("SELECT groupId from dataapp_group where dataappId = ?;", [uid])
    groups = conn.fetch_all()
    if groups and groups is not None:
        # Check user has permission to delete dataApp inside a group
        for group in groups[0]:
            if not _write_permission(user_id, group, conn):
                # TODO Send error to UI
                raise RuntimeError(f"User has not group permission to delete dataApp")
    else:
        if user_id != dataapp.userId:
            raise RuntimeError("User cannot delete dataApp")
    remove_spec_file(dataapp.specId)
    conn.execute("DELETE FROM dataapps WHERE uid = ?;", [uid]);
    conn.execute("DELETE FROM dataapp_group WHERE dataappId = ?;", [uid]);
    remove_data(uid, conn)
    return True


def _clear_all_dataapps(conn: Connection):
    conn.execute("DELETE FROM dataapps;")
    conn.execute("DELETE FROM dataapp_group;")
    conn.execute("DELETE FROM dataapp_data;")
    for f in os.listdir(DATAAPP_DIR):
        os.remove(os.path.join(DATAAPP_DIR, f))
    for f in os.listdir(DATA_DIR):
        os.remove(os.path.join(DATA_DIR, f))


def _get_dataapp_principals(dataapp_id: int, conn: Connection) -> List[PrincipalId]:
    pass
    # conn.execute("SELECT scope, id FROM principals where id = ?;", [dataapp_id])
    # records = conn.fetch_all()
    # return [PrincipalId(scope=str(r[0]), id=str(r[1])) for r in records]


def _get_dataapp_versions(dataapp_name: str, conn: Connection):
    conn.execute(""" 
        SELECT major, minor
        FROM dataapps
        WHERE name = ? 
        ORDER BY major DESC and minor DESC;
    """, [dataapp_name])

    result = []
    for r in conn.fetch_all():
        version = float(f"{r[0]}.{r[1]}")
        result.append(version)
    return result


def _get_dataapp_tags(dataapp_name: str, conn: Connection):
    conn.execute(""" 
        SELECT tags
        FROM dataapps
        WHERE name = ? 
        ORDER BY major DESC and minor DESC;
    """, [dataapp_name])

    result = conn.fetch_one()
    return result


def _get_group_id(group_name: str, conn: Connection):
    """
    If group exist, return its id. Otherwise, raise error.
    """
    conn.execute("SELECT uid FROM groups WHERE name = ?;", [group_name])
    result = conn.fetch_one()
    if result is not None:
        return result[0]
    raise InvalidGroupName(group_name)


def _write_permission(user_id: int, group_id: int, conn: Connection) -> bool:
    conn.execute(
        """
            SELECT read_write 
            FROM users_groups 
            WHERE userId = ? AND groupId = ?; 
        """,
        [user_id, group_id, ])
    result = conn.fetch_one()
    if result is not None:
        return bool(result[0])
    # Get Data for the exception
    conn.execute(
        """
            SELECT nickName 
            FROM users 
            WHERE uid = ?; 
        """,
        [user_id])
    user_name = conn.fetch_one()[0]
    conn.execute(
        """
            SELECT name 
            FROM groups 
            WHERE uid = ?; 
        """,
        [group_id])
    group_name = conn.fetch_one()[0]
    raise UserDoesNotBelong(user_name, group_name)


def _insert_dataapp_group(uid, group_id, conn):
    conn.execute("""
            INSERT INTO dataapp_group 
            (dataappId, groupId)
            VALUES (?, ?);
        """, [uid, group_id])


def _add_data(uid: int, data: List[str], conn: Connection):
    for widget_id in data:
        conn.execute("""
                INSERT INTO dataapp_data 
                (dataappId, dataInfo)
                VALUES (?, ?);
            """, [uid, widget_id])

def _overwrite_data(uid: int, data: List[str], conn: Connection):
    # First remove the data from the given dataApp, as it's going to be updated.
    remove_data(uid, conn)
    for widget_id in data:
        conn.execute("""
                INSERT INTO dataapp_data 
                (dataappId, dataInfo)
                VALUES (?, ?);
            """, [uid, widget_id])

def _save_dataapp_functions(functions: List[DataAppFunction]):
    # Save serialized funtion in a file
    for fn in functions:
        with open(os.path.join(DATA_DIR, fn.uid), 'wt') as f:
            f.write(fn.ser_body)


def _load_dataapp_by_id(dataapp_uid, conn) -> Optional[DataAppProfile]:
    base_query = f"SELECT {', '.join(DataAppAllFields)} FROM dataapps WHERE uid = {dataapp_uid} "
    conn.execute(base_query)
    record = conn.fetch_one()
    if record is None:
        return None
    d = {}
    for idx, a in enumerate(DataAppAllFields):
        d[a] = record[idx]

    return DataAppProfile(**d)


class DataAppsRepo(IDataAppsRepo):

    def load_all(self,
                 user_id: int,
                 attributes: Set[DataAppField],
                 skip: Optional[int],
                 sort_by: Optional[List[Tuple[DataAppField, bool]]],
                 limit: Optional[int]) -> List[DataAppProfile]:
        with connect() as conn:
            return _load_all(user_id, attributes, sort_by, skip, limit, conn)

    def user_local_dataapp_list(self, user_id: int) -> List[DataAppProfile]:
        with connect() as conn:
            return _user_local_dataapp_list(user_id, conn)

    def user_group_dataapp_list(self, user_id: int) -> List[DataAppProfile]:
        with connect() as conn:
            return _user_group_dataapp_list(user_id, conn)

    def create(self,
               details: DataAppAttributes,
               data: List[str] = None,
               dataapp_functions: List[DataAppFunction] = None
               ) -> Optional[DataAppProfile]:
        with transaction() as conn:
            # Transform group names to group ids
            if details.groups is not None:
                # DataApp is going to a group
                group_names = details.groups
                if not isinstance(group_names, list):
                    group_names = [group_names]
                group_ids = []
                for group in group_names:
                    group_id = _get_group_id(group, conn)
                    # If there is a group, check that user has write permission to the given group.
                    if _write_permission(details.userId, group_id, conn):
                        group_ids.append(group_id)
                    else:
                        conn.execute(
                            """
                                SELECT nickName 
                                FROM users 
                                WHERE uid = ?; 
                            """,
                            [details.userId])
                        user_name = conn.fetch_one()[0]
                        raise WritePermission(user_name=user_name, group_name=group)
                details.groups = group_ids
                dataapp = self._create_for_group(details, conn)
            else:
                # DataApp is going to user space
                dataapp = self._create_for_user(details, conn)
            if data:
                _overwrite_data(dataapp.uid, data, conn)
            if dataapp_functions:
                _save_dataapp_functions(dataapp_functions)
            return dataapp

    def load_by_name(self, dataapp_name: str) -> Optional[DataAppProfile]:
        with connect() as conn:
            return _load_dataapp_by_name(dataapp_name, conn)

    def load_by_id(self, uid: int) -> Optional[DataAppProfile]:
        with connect() as conn:
            return _load_dataapp_by_id(uid, conn)

    def load_by_principal(self, principal: PrincipalId) -> Optional[DataAppAttributes]:
        pass

    def delete_dataapp(self, uid: int, user_id: int) -> bool:
        with connect() as conn:
            return _delete_dataapp(uid, user_id, conn)

    def delete_all(self):
        with transaction() as conn:
            _clear_all_dataapps(conn)

    def get_dataapp_versions(self, dataapp_name: str) -> List[float]:
        with connect() as conn:
            return _get_dataapp_versions(dataapp_name, conn)

    def get_dataapp_by_version(self, dataapp_name: str, major: int, minor: int) -> DataAppAttributes:
        with connect() as conn:
            return _load_dataapp_by_name_and_version(dataapp_name, major, minor, conn)

    def get_dataapp_last_version(self, dataapp_name: str) -> float:
        with connect() as conn:
            return _get_dataapp_versions(dataapp_name, conn)[0]

    def get_dataapp_tags(self, dataapp_name: str) -> List[str]:
        with connect() as conn:
            return _get_dataapp_tags(dataapp_name, conn)[0]

    @staticmethod
    def _create_for_user(details: DataAppAttributes, conn: Connection) -> Optional[DataAppProfile]:
        dataapp_name = details.name
        # Set Update Date
        details.updateDate = int(datetime.now().timestamp())
        if details.major is None and details.minor is None:
            # if details.version is None:
            details.creationDate = int(datetime.now().timestamp())
            # check if dataApp exists
            dataapp = _load_dataapp_by_name_and_user(dataapp_name, details.userId, conn)
            if dataapp:
                # If existed, increase minor version
                details.major = dataapp.major
                details.minor = dataapp.minor + 1
            else:
                # first time dataApp is registered
                details.major = 0
                details.minor = 1
            uid = _next_id(conn)
            _insert_dataapp(uid, details, conn)
        else:
            # user provides version
            dataapp = _load_dataapp_by_name_version_and_user(dataapp_name, details.major, details.minor,
                                                             details.userId, conn)
            if dataapp:
                uid = dataapp.uid
                _update_dataapp(uid,
                                details.specId,
                                details.updateDate,
                                dataapp.specId,
                                conn)
            else:
                # Otherwise, insert new version
                details.creationDate = int(datetime.now().timestamp())
                uid = _next_id(conn)
                _insert_dataapp(uid, details, conn)

        return _load_dataapp_by_id(uid, conn)

    @staticmethod
    def _create_for_group(details: DataAppAttributes, conn: Connection) -> Optional[DataAppProfile]:
        # User write permission already checked.
        dataapp_name = details.name
        # Set Update Date
        details.updateDate = int(datetime.now().timestamp())
        if details.major is None and details.minor is None:
            # if details.version is None:
            details.creationDate = int(datetime.now().timestamp())
            insert = False
            for group in details.groups:
                # check if dataApp exists for the group
                dataapp = _load_dataapp_by_name_and_group(dataapp_name, group, conn)
                if not dataapp:
                    # check if there is dataApp existed for the user
                    dataapp = _load_dataapp_by_name_and_user(dataapp_name, details.userId, conn)
                if dataapp:
                    # If existed, increase minor version
                    details.major = dataapp.major
                    details.minor = dataapp.minor + 1
                else:
                    # first time dataApp is registered
                    details.major = 0
                    details.minor = 1
                # Check if dataApp exists for this user
                existed_app = _load_dataapp_by_name_version_and_user(dataapp_name, details.major, details.minor,
                                                                     details.userId, conn)
                if existed_app:
                    uid = existed_app.uid
                    _update_dataapp(uid,
                                    details.specId,
                                    details.updateDate,
                                    existed_app.specId,
                                    conn)
                else:
                    # Insert when all groups are checked
                    insert = True
            if insert:
                # Wait to insert until we finish checking groups to avoid duplicates
                uid = _next_id(conn)
                _insert_dataapp(uid, details, conn)
                for group in details.groups:
                    _insert_dataapp_group(uid, group, conn)

        else:
            # user provides version
            insert = False
            for group in details.groups:
                dataapp = _load_dataapp_by_name_version_and_group(dataapp_name, details.major, details.minor,
                                                                  group, conn)
                if dataapp:
                    # If dataapp exists with same version -> Update spec
                    # Only if the user updating is the user how originally created the dataApp
                    uid = dataapp.uid
                    if dataapp.userId == details.userId:
                        _update_dataapp(uid,
                                        details.specId,
                                        details.updateDate,
                                        dataapp.specId,
                                        conn)
                    else:
                        raise Exception(f"User has not rights to overwrite dataApp {details.name}.")
                else:
                    # Check if dataApp exists for this user
                    existed_app = _load_dataapp_by_name_version_and_user(dataapp_name, details.major, details.minor,
                                                                         details.userId, conn)
                    if existed_app:
                        # Share dataApp with group by modifying dataApp group
                        uid = existed_app.uid
                        _update_dataapp(uid,
                                        details.specId,
                                        details.updateDate,
                                        existed_app.specId,
                                        conn)
                        _insert_dataapp_group(uid, group, conn)
                    else:
                        # Otherwise, insert new version, but wait until we finish checking for groups to avoid duplicates.
                        insert = True
            if insert:
                # Wait to insert until we finish checking groups to avoid duplicates
                details.creationDate = int(datetime.now().timestamp())
                uid = _next_id(conn)
                _insert_dataapp(uid, details, conn)
                _insert_dataapp_group(uid, group, conn)
                for group in details.groups:
                    _insert_dataapp_group(uid, group, conn)
        return _load_dataapp_by_id(uid, conn)

from typing import Optional, Tuple

from .iauthrepo import IAuthRepo
from ..dataapps.dataappsrepo import _user_group_dataapp_list, _user_local_dataapp_list, _delete_dataapp
from ..db import Connection, connect, transaction
from ..model import UserAttributes


def _nextId(conn: Connection) -> int:
    conn.execute("SELECT nextval('shapelets.id_gen')")
    return int(conn.fetch_one()[0])


def _users_insert(uid: int, details: UserAttributes, conn: Connection):
    conn.execute("""
            INSERT INTO users 
            (uid, nickName, email, firstName, familyName, locale, picture, bio, location, url) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
                 [
                     uid, details.nickName, details.email, details.firstName, details.familyName,
                     details.locale, details.picture, details.bio, details.location, details.url
                 ])


def _unp_users_get_salt(userName: str, conn: Connection) -> Optional[bytes]:
    conn.execute("SELECT salt FROM unp_users where userName = ?;", [userName])
    result = conn.fetch_one()
    return None if result is None else result[0]


def _unp_users_verify_key(userName: str, conn: Connection) -> Optional[bytes]:
    conn.execute("SELECT verifyKey FROM unp_users where userName = ?", [userName])
    result = conn.fetch_one()
    return None if result is None else result[0]


def _unp_users_has_userName(userName: str, conn: Connection) -> bool:
    conn.execute("SELECT 1 FROM unp_users where userName = ?", [userName])
    result = conn.fetch_one()
    return None if result is None else int(result[0]) == 1


def _unp_users_insert(userName: str, salt: bytes, verify_key: bytes, conn: Connection):
    conn.execute("INSERT INTO unp_users (userName, salt, verifyKey) VALUES (?,?,?)", [userName, salt, verify_key])


def _unp_users_update(existing_user_name: str, new_user_name: str, new_salt: bytes, new_verify_key: bytes,
                      conn: Connection):
    conn.execute("""
        UPDATE unp_users
        SET verifyKey = ?, salt = ?, userName = ?
        WHERE userName = ?
    """, [new_verify_key, new_salt, new_user_name, existing_user_name])


def _unp_users_delete(userName: str, conn: Connection):
    conn.execute("DELETE FROM unp_users WHERE userName = ?", [userName])


def _users_delete(uid: int, conn: Connection):
    conn.execute("DELETE FROM users WHERE uid = ?", [uid])


def _unp_challenges_last_nonce(userName: str, conn: Connection) -> Optional[Tuple[bytes, bool]]:
    conn.execute("SELECT nonce, expired FROM unp_challenges where userName = ?", [userName])
    result = conn.fetch_one()
    return (None, None) if result is None else (bytes(result[0]), bool(result[1]))


def _unp_challenges_insert_last_nonce(userName: str, nonce: bytes, conn: Connection):
    conn.execute("INSERT INTO unp_challenges (userName, nonce, expired) VALUES (?, ?, ?);", [userName, nonce, False])


def _unp_challenges_update_last_nonce(userName: str, nonce: bytes, conn: Connection):
    conn.execute("""
        UPDATE unp_challenges 
        SET expired = FALSE, nonce = ? 
        WHERE userName = ?;
    """, [nonce, userName])


def _unp_challenges_expire_nonce(userName: str, conn: Connection):
    conn.execute("UPDATE unp_challenges SET expired = TRUE WHERE userName = ?;", [userName])


def _unp_challenges_delete(userName: str, conn: Connection):
    conn.execute("DELETE FROM unp_challenges WHERE userName = ?", [userName])


def _principals_insert(uid: int, scope: str, pid: str, conn: Connection):
    conn.execute("INSERT INTO principals (scope, id, uid) VALUES(?,?,?);", [scope, pid, uid])


def _principals_find_userId(scope: str, pid: str, conn: Connection) -> Optional[int]:
    conn.execute("SELECT uid FROM principals where scope = ? and id = ?;", [scope, pid])
    record = conn.fetch_one()
    return None if record is None else int(record[0])


def _principals_delete(scope: str, pid: str, conn: Connection):
    conn.execute("DELETE FROM principals where scope = ? and id = ?;", [scope, pid])


def _principals_delete_by_userId(uid: int, scope: str, conn: Connection):
    conn.execute("DELETE FROM principals where scope = ? and uid = ?;", [scope, uid])


def _principals_find_userName(uid: int, conn: Connection) -> Optional[str]:
    conn.execute("SELECT id FROM principals where uid = ? and scope = ?", [uid, 'unp'])
    record = conn.fetch_one()
    return None if record is None else str(record[0])


def _transfer_data_apps(old_user_id: int, new_user_id: int, conn: Connection):
    conn.execute("""
    SELECT name 
    FROM groups 
    LEFT JOIN users_groups on users_groups.groupId = groups.uid where users_groups.userId = ?
    """, [new_user_id])
    new_user_groups = conn.fetch_all()
    if new_user_groups:
        group_names = [group[0] for group in new_user_groups]
    else:
        raise ValueError("Transfer user does not belong to any group or does not have write permissions over the group.")
    # Try transferring dataApps with group
    dataapp_with_group = _user_group_dataapp_list(old_user_id, conn)
    for app in dataapp_with_group:
        if any(x in app.groups for x in group_names):
            conn.execute(""" 
                UPDATE dataapps 
                SET userId = ?
                WHERE uid = ?;
            """, [new_user_id, app.uid])
        else:
            raise Exception("Transfer user does not have access to the group where this dataApp belong")
    # delete old user private dataApps
    private_apps = _user_local_dataapp_list(old_user_id, conn)
    if private_apps:
        for app in private_apps:
            _delete_dataapp(app.uid, old_user_id, conn)


class AuthRepo(IAuthRepo):

    def find_userId(self, scope: str, id: str) -> Optional[int]:
        with connect() as conn:
            return _principals_find_userId(scope, id, conn)

    def create_new_user_unp(self, userName: str, salt: bytes, verify_key: bytes, user_details: UserAttributes) -> int:
        with transaction() as conn:
            uid = _nextId(conn)
            _users_insert(uid, user_details, conn)
            _unp_users_insert(userName, salt, verify_key, conn)
            _principals_insert(uid, 'unp', userName, conn)
            return uid

    def create_new_user(self, scope: str, id: str, user_details: UserAttributes) -> int:
        with transaction() as conn:
            uid = _nextId(conn)
            _users_insert(uid, user_details, conn)
            _principals_insert(uid, scope, id, conn)
            return uid

    def last_nonce(self, userName: str) -> Optional[Tuple[bytes, bool]]:
        with connect() as conn:
            return _unp_challenges_last_nonce(userName, conn)

    def user_name_exists(self, userName: str) -> bool:
        with connect() as conn:
            return _unp_users_has_userName(userName, conn)

    def remove_user(self, userName: str, transfer: str) -> int:
        with transaction() as conn:
            scope = 'unp'
            uid = _principals_find_userId(scope, userName, conn)
            if uid is None:
                return None

            if transfer is not None:
                transfer_user_id = _principals_find_userId(scope, transfer, conn)
                if transfer_user_id is None:
                    return None
                _transfer_data_apps(uid, transfer_user_id, conn)
            else:
                dataapp = _user_group_dataapp_list(uid, conn)
                if dataapp:
                    message = f"User {userName} cannot be deleted because this user owns dataApp/s belonging to a group. "
                    message += "Please, use transfer to change the owner before removing user."
                    raise RuntimeError(message)

            _principals_delete_by_userId(uid, scope, conn)
            _unp_users_delete(userName, conn)
            _users_delete(uid, conn)
            return uid

    def get_salt(self, userName: str) -> Optional[bytes]:
        with connect() as conn:
            return _unp_users_get_salt(userName, conn)

    def store_nonce(self, userName: str, nonce: bytes):
        with transaction() as conn:
            last_nonce, _ = _unp_challenges_last_nonce(userName, conn)
            if last_nonce is None:
                _unp_challenges_insert_last_nonce(userName, nonce, conn)
            else:
                _unp_challenges_update_last_nonce(userName, nonce, conn)

    def get_verify_key(self, userName: str) -> Optional[bytes]:
        with connect() as conn:
            return _unp_users_verify_key(userName, conn)

    def expire_nonce(self, userName: str):
        with connect() as conn:
            _unp_challenges_expire_nonce(userName, conn)

    def update_salt_and_key(self, existing_user_name: str, new_user_name: str, new_salt: bytes, new_verify_key: bytes):
        with transaction() as conn:
            uid = _principals_find_userId('unp', existing_user_name, conn)
            assert uid is not None
            _principals_delete('unp', existing_user_name, conn)
            _unp_users_update(existing_user_name, new_user_name, new_salt, new_verify_key, conn)
            _principals_insert(uid, 'unp', new_user_name, conn)

    def find_user_name_with_principal(self, scope: str, id: str) -> Optional[str]:
        with transaction() as conn:
            uid = _principals_find_userId(scope, id, conn)
            assert uid is not None
            return _principals_find_userName(uid, conn)

    def associate(self, userId: int, scope: str, id: str):
        with connect() as conn:
            _principals_insert(userId, scope, id, conn)

    def associate_unp(self, userId: int, userName: str, salt: bytes, verify_key: bytes):
        with transaction() as conn:
            _unp_users_insert(userName, salt, verify_key, conn)
            _principals_insert(userId, 'unp', userName, conn)

    def disassociate(self, userId: int, scope: str):
        with transaction() as conn:
            _principals_delete_by_userId(scope, userId, conn)
            if scope == 'unp':
                userName = _principals_find_userName(userId, conn)
                assert userName is not None
                _unp_challenges_delete(userName, conn)
                _unp_users_delete(userName, conn)

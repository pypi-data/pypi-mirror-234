import os
import tomlkit

from pathlib import Path
from typing import Optional, Tuple

from .native import Connection, transaction
from .schema_builder import SchemaBuilder
from ..model import SignedPrincipalId
from ..settings import add_user_to_client
from ..utils import crypto


class BuilderV6(SchemaBuilder):
    """
    Database Schema Version 6
    - Creates default user admin.
    """

    @staticmethod
    def _unp_users_has_user_name(user_name: str, conn: Connection) -> bool:
        conn.execute("SELECT 1 FROM unp_users where userName = ?", [user_name])
        result = conn.fetch_one()
        return None if result is None else int(result[0]) == 1

    @staticmethod
    def _users_insert(uid: int, user_name: str, conn: Connection):
        conn.execute("""
                INSERT INTO users 
                (uid, nickName) 
                VALUES (?, ?);
            """, [uid, user_name])

    @staticmethod
    def _unp_users_insert(user_name: str, salt: bytes, verify_key: bytes, conn: Connection):
        conn.execute("INSERT INTO unp_users (userName, salt, verifyKey) VALUES (?,?,?)", [user_name, salt, verify_key])

    @staticmethod
    def _principals_insert(uid: int, scope: str, pid: str, conn: Connection):
        conn.execute("INSERT INTO principals (scope, id, uid) VALUES(?,?,?);", [scope, pid, uid])

    @staticmethod
    def _nextId(conn: Connection) -> int:
        """
        Get next available ID
        """
        conn.execute("SELECT nextval('shapelets.id_gen')")
        return int(conn.fetch_one()[0])

    @staticmethod
    def _unp_challenges_last_nonce(user_name: str, conn: Connection) -> Optional[Tuple[bytes, bool]]:
        conn.execute("SELECT nonce, expired FROM unp_challenges where userName = ?", [user_name])
        result = conn.fetch_one()
        return (None, None) if result is None else (bytes(result[0]), bool(result[1]))

    @staticmethod
    def _unp_users_verify_key(user_name: str, conn: Connection) -> Optional[bytes]:
        conn.execute("SELECT verifyKey FROM unp_users where userName = ?", [user_name])
        result = conn.fetch_one()
        return None if result is None else result[0]

    @staticmethod
    def _sh_key(settings: str = '~/.shapelets/settings.toml'):
        # load the data
        file = Path(os.path.expandvars(os.path.expanduser(settings)))
        with open(file, "rt", encoding="utf-8") as handle:
            data = tomlkit.load(handle)
        import base64
        svr_salt = base64.b64decode(data.get("server").get("salt").encode('ascii'), validate=True)
        svr_secret = data.get("server").get("secret").encode('ascii')
        return crypto.derive_signature_keys(svr_salt, svr_secret)

    @property
    def version(self) -> int:
        return 6

    def setup(self):
        pass

    def patch(self, conn: Connection):
        with transaction() as conn:
            user_name = "admin"
            password = "admin"
            if not self._unp_users_has_user_name(user_name, conn):
                # Create User
                salt = crypto.generate_salt()
                pk = crypto.derive_verify_key(salt, password.encode('ascii'))
                uid = self._nextId(conn)
                self._users_insert(uid, user_name, conn)
                self._unp_users_insert(user_name, salt, pk, conn)
                self._principals_insert(uid, 'unp', user_name, conn)
                # Generate signed principal to save signed token to settings
                previous, _ = self._unp_challenges_last_nonce(user_name, conn)
                nonce = crypto.generate_nonce(previous)
                verify_key = self._unp_users_verify_key(user_name, conn)
                token = crypto.sign_challenge(salt, nonce, password.encode('ascii'))
                _, __sk = self._sh_key()

                if not crypto.verify_challenge(token, nonce, verify_key):
                    raise Exception(f"Unable to verify signature")

                message = f'unp:{user_name}:{uid}'.encode('ascii')
                signed_principal = SignedPrincipalId(
                    scope='unp',
                    id=user_name,
                    userId=uid,
                    signature=crypto.sign(message, __sk)
                )
                add_user_to_client(host="127.0.0.1", user_name=user_name, user_principal=signed_principal, default=True)

from dataclasses import dataclass
from typing import List

from .native import Connection, transaction
from .schema_builder import SchemaBuilder


@dataclass
class OldDataAppProfile:
    name: str
    major: int
    minor: int
    description: str
    creationDate: int
    updateDate: int
    specId: str
    tags: list


@dataclass
class NewDataAppProfile:
    uid: int
    name: str
    major: int
    minor: int
    description: str
    creationDate: int
    updateDate: int
    specId: str
    tags: list
    userId: int


class BuilderV4(SchemaBuilder):
    """
    Database Schema Version 4
    - Adds unique uid and userId to dataApps table
    - Drops groupName in Users table
    - Creates dataapp_group to store relation between a dataApp and a group
    - Creates users_groups to store relation between a user and a group
    - Creates dataapp_data to keep track of tables used in the dataApp
    """

    @staticmethod
    def _create_dataapps_table(conn: Connection):
        conn.execute("""
            CREATE TABLE dataapps (
                uid INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL, 
                major INTEGER NOT NULL,
                minor INTEGER NOT NULL,
                description VARCHAR NULL,
                creationDate BIGINT NOT NULL,
                updateDate BIGINT NOT NULL,
                specId VARCHAR NOT NULL, 
                tags VARCHAR[] NULL,
                userId INTEGER NOT NULL
                );
        """)

    @staticmethod
    def _get_current_dataapps(conn) -> List[OldDataAppProfile]:
        attributes = ['name', 'major', 'minor', 'description', 'creationDate', 'updateDate', 'specId', 'tags']
        conn.execute(""" 
                    SELECT *
                    FROM dataapps;
                """)
        old_data_apps = []
        d = {}
        for r in conn.fetch_all():
            for idx, a in enumerate(attributes):
                d[a] = r[idx]
            old_data_apps.append(OldDataAppProfile(**d))
        return old_data_apps

    @staticmethod
    def _drop_dataapps_table(conn: Connection):
        conn.execute("""DROP TABLE dataapps;""")

    @staticmethod
    def _insert_dataapps(new_data_apps: List[NewDataAppProfile], conn):
        for details in new_data_apps:
            conn.execute("""
                        INSERT INTO dataapps 
                        (uid, name, major, minor, description, creationDate, updateDate, specId, tags, userId)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                         [
                             details.uid, details.name, details.major, details.minor, details.description,
                             details.creationDate, details.updateDate, details.specId, details.tags, details.userId
                         ])

    @staticmethod
    def _alter_users(conn: Connection):
        conn.execute("""
            ALTER TABLE users
            DROP COLUMN groupName;
        """)

    @staticmethod
    def _create_dataapp_groups(conn: Connection):
        conn.execute("""
            CREATE TABLE dataapp_group (
                dataappId INTEGER NOT NULL, 
                groupId INTEGER NOT NULL
                );
        """)

    @staticmethod
    def _create_users_groups(conn: Connection):
        conn.execute("""
            CREATE TABLE users_groups (
                userId INTEGER NOT NULL, 
                groupId INTEGER NOT NULL,
                read_write TINYINT NOT NULL
                );
        """)

    @staticmethod
    def _create_dataapp_data(conn: Connection):
        conn.execute("""
            CREATE TABLE dataapp_data (
                dataappId INTEGER NOT NULL, 
                dataInfo VARCHAR NOT NULL
                );
        """)

    @staticmethod
    def _transform_dataapp(old_dataapps: List[OldDataAppProfile], conn: Connection) -> List[NewDataAppProfile]:
        conn.execute("SELECT uid from users WHERE nickName = ?;", ["admin"])
        user_id = conn.fetch_one()
        if user_id is None:
            conn.execute("SELECT uid from users LIMIT 1")
            user_id = conn.fetch_one()[0]
        else:
            user_id = user_id[0]
        new_dataapps = []
        for dataapp in old_dataapps:
            conn.execute("SELECT nextval('shapelets.id_gen')")
            uid = int(conn.fetch_one()[0])
            new_dataapps.append(NewDataAppProfile(
                uid=uid,
                name=dataapp.name,
                major=dataapp.major,
                minor=dataapp.minor,
                description=dataapp.description,
                creationDate=dataapp.creationDate,
                updateDate=dataapp.updateDate,
                specId=dataapp.specId,
                tags=dataapp.tags,
                userId=user_id
            ))
        return new_dataapps

    @property
    def version(self) -> int:
        return 4

    def setup(self):
        pass

    def patch(self, conn: Connection):
        with transaction() as conn:
            self._create_users_groups(conn)
            self._create_dataapp_groups(conn)
            self._create_dataapp_data(conn)
            self._alter_users(conn)
            current_dataaps = self._get_current_dataapps(conn)
            new_dataapps = []
            if current_dataaps:
                new_dataapps = self._transform_dataapp(current_dataaps, conn)
            self._drop_dataapps_table(conn)
            self._create_dataapps_table(conn)
            if new_dataapps:
                self._insert_dataapps(new_dataapps, conn)

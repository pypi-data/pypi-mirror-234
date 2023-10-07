from dataclasses import dataclass
from typing import List

from .native import Connection, transaction
from .schema_builder import SchemaBuilder


@dataclass
class OldDataAppProfile:
    name: str
    version: float
    description: str
    creationDate: int
    updateDate: int
    spec: str
    tags: list


@dataclass
class NewDataAppProfile:
    name: str
    major: int
    minor: int
    description: str
    creationDate: int
    updateDate: int
    spec: str
    tags: list


class BuilderV2(SchemaBuilder):
    """
    Database Schema Version 2
    - Split data apps version field (float) into major (int) and minor (int).
    """

    @staticmethod
    def _create_dataapps_table(conn: Connection):
        conn.execute("""
            CREATE TABLE dataapps (
                name VARCHAR NOT NULL, 
                major INTEGER NOT NULL,
                minor INTEGER NOT NULL,
                description VARCHAR NULL,
                creationDate BIGINT NOT NULL,
                updateDate BIGINT NOT NULL,
                spec VARCHAR NOT NULL, 
                tags VARCHAR[] NULL
                );
        """)

    @staticmethod
    def _get_current_dataapps(conn) -> List[OldDataAppProfile]:
        attributes = ['name', 'version', 'description', 'creationDate', 'updateDate', 'spec', 'tags']
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
    def _transform_dataapps(current_data_apps) -> List[NewDataAppProfile]:
        new_data_apps = []
        for app in current_data_apps:
            int_version = [int(x) for x in str(round(app.version, 1)).split(".")]
            new_data_apps.append(
                NewDataAppProfile(
                    name=app.name, major=int_version[0], minor=int_version[1], description=app.description,
                    creationDate=app.creationDate, updateDate=app.updateDate, spec=app.spec, tags=app.tags)
            )
        return new_data_apps

    @staticmethod
    def _drop_dataapps_table(conn: Connection):
        conn.execute("""DROP TABLE dataapps;""")

    @staticmethod
    def _insert_dataapps(new_data_apps, conn):
        for details in new_data_apps:
            conn.execute("""
                        INSERT INTO dataapps 
                        (name, major, minor, description, creationDate, updateDate, spec, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                         [
                             details.name, details.major, details.minor, details.description,
                             details.creationDate, details.updateDate, details.spec, details.tags
                         ])

    @property
    def version(self) -> int:
        return 2

    def setup(self):
        pass

    def patch(self, conn: Connection):
        with transaction() as conn:
            current_data_apps = self._get_current_dataapps(conn)
            new_data_apps = None
            if current_data_apps:
                new_data_apps = self._transform_dataapps(current_data_apps)
            self._drop_dataapps_table(conn)
            self._create_dataapps_table(conn)
            if new_data_apps:
                self._insert_dataapps(new_data_apps, conn)

import os
import uuid

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
    specId: str
    tags: list


class BuilderV3(SchemaBuilder):
    """
    Database Schema Version 3
    - Save DataApp Spec in file
    - Replace DataApp spec field for specId
    """
    SH_DIR = os.path.expanduser('~/.shapelets')
    DATAAPP_DIR = os.path.join(SH_DIR, 'dataAppsStore')
    DATA_DIR = os.path.join(SH_DIR, 'data')

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
                specId VARCHAR NOT NULL, 
                tags VARCHAR[] NULL
                );
        """)

    @staticmethod
    def _get_current_dataapps(conn) -> List[OldDataAppProfile]:
        attributes = ['name', 'major', 'minor', 'description', 'creationDate', 'updateDate', 'spec', 'tags']
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

    def _create_spec_file(self, spec: str) -> str:
        spec_id = str(uuid.uuid1())
        spec_path = os.path.join(self.DATAAPP_DIR, f"{spec_id}.json")
        with open(spec_path, 'wt') as f:
            f.write(spec)
        return spec_id

    def _save_dataapp_spec(self, current_data_apps: List[OldDataAppProfile]) -> List[NewDataAppProfile]:
        new_data_apps = []
        for app in current_data_apps:
            new_spec_id = self._create_spec_file(app.spec)
            new_data_apps.append(
                NewDataAppProfile(
                    name=app.name, major=app.major, minor=app.minor, description=app.description,
                    creationDate=app.creationDate, updateDate=app.updateDate, specId=new_spec_id, tags=app.tags)
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
                        (name, major, minor, description, creationDate, updateDate, specId, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                         [
                             details.name, details.major, details.minor, details.description,
                             details.creationDate, details.updateDate, details.specId, details.tags
                         ])

    @property
    def version(self) -> int:
        return 3

    def setup(self):
        pass

    def patch(self, conn: Connection):
        with transaction() as conn:
            current_data_apps = self._get_current_dataapps(conn)
            os.makedirs(self.DATAAPP_DIR, exist_ok=True)
            os.makedirs(self.DATA_DIR, exist_ok=True)
            new_data_apps = None
            if current_data_apps:
                new_data_apps = self._save_dataapp_spec(current_data_apps)
            self._drop_dataapps_table(conn)
            self._create_dataapps_table(conn)
            if new_data_apps:
                self._insert_dataapps(new_data_apps, conn)

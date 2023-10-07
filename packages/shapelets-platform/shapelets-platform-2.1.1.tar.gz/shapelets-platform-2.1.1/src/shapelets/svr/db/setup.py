from typing import Optional

from .native import Connection, DatabaseSettings, initialize_db, transaction
from .schema_v1 import BuilderV1
from .schema_v2 import BuilderV2
from .schema_v3 import BuilderV3
from .schema_v4 import BuilderV4
from .schema_v5 import BuilderV5
from .schema_v6 import BuilderV6


def create_version_table(conn: Connection) -> str:
    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER NOT NULL
        );
    """)


def get_schema_version(conn: Connection) -> Optional[int]:
    conn.execute("SELECT version from schema_version LIMIT 1;")
    version = conn.fetch_one()
    return None if version is None else int(version[0])


def update_schema_version(conn: Connection, newVersion: int):
    conn.execute("UPDATE schema_version SET version=?;", [newVersion])


def insert_schema_version(conn: Connection, newVersion: int):
    conn.execute("INSERT INTO schema_version VALUES(?);", [newVersion])


def setup_database(dbSettings: DatabaseSettings):
    # initialize db
    initialize_db(dbSettings)

    # Get a list of builders and sort them 
    # using the version property
    builders = [BuilderV1(), BuilderV2(), BuilderV3(), BuilderV4(), BuilderV5(), BuilderV6()]
    builders.sort(key=lambda x: x.version)

    # ensure the schema and the version table is there 
    with transaction() as conn:
        create_version_table(conn)
        version = get_schema_version(conn)

    if version is None:
        # if there is no version
        # get the first builder
        # and execute the setup
        builder = builders[0]
        # set version to 1
        version = builder.version
        with transaction() as conn:
            builder.setup(conn)
            insert_schema_version(conn, builder.version)

    # Once we have a version in the system, start patching the rest of the versions
    for builder in builders:
        if builder.version > version:
            with transaction() as conn:
                builder.patch(conn)
                update_schema_version(conn, builder.version)


__all__ = ['setup_database']

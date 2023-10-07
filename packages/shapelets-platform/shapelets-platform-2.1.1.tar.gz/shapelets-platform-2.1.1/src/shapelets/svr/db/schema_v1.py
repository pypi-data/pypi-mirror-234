import uuid

from .native import Connection, transaction
from .schema_builder import SchemaBuilder


class BuilderV1(SchemaBuilder):

    def _create_sequence(self, conn: Connection):
        conn.execute("""
            CREATE SEQUENCE id_gen 
                MINVALUE -9223372036854775808 
                MAXVALUE 9223372036854775807 
                START 1 CYCLE;
        """)

    def _create_user_table(self, conn: Connection):
        conn.execute("""
            CREATE TABLE users (
                uid INTEGER PRIMARY KEY,
                nickName VARCHAR UNIQUE, 
                email VARCHAR NULL, 
                firstName VARCHAR NULL,
                familyName VARCHAR NULL,
                locale VARCHAR NULL,
                picture VARCHAR NULL,
                bio BLOB NULL,
                location VARCHAR NULL,
                url VARCHAR NULL,
                groupName VARCHAR NULL);
        """)

    def _create_principals_table(self, conn: Connection):
        conn.execute("""
            CREATE TABLE principals (
                id VARCHAR NOT NULL,
                scope VARCHAR NOT NULL,
                uid INTEGER NOT NULL,
                PRIMARY KEY(id, scope));
        """)

    def _create_unp_challenges(self, conn: Connection):
        conn.execute("""
            CREATE TABLE unp_challenges (
                userName VARCHAR PRIMARY KEY,
                nonce BLOB NOT NULL, 
                expired BOOL NOT NULL
            );
        """)

    def _create_unp_users(self, conn: Connection):
        conn.execute("""
            CREATE TABLE unp_users (
                userName VARCHAR PRIMARY KEY,
                salt BLOB NOT NULL,
                verifyKey BLOB NOT NULL
            );
        """)

    def _create_relations(self, conn: Connection):
        conn.execute("""
            CREATE TABLE relations (
                namespace VARCHAR NOT NULL,
                name VARCHAR NOT NULL, 
                kind VARCHAR NOT NULL,
                parameters VARCHAR,
                description VARCHAR,
                PRIMARY KEY(namespace, name),
            )
        """)

    def _create_groups_table(self, conn: Connection):
        conn.execute("""
            CREATE TABLE groups (
                uid INTEGER PRIMARY KEY,
                name VARCHAR UNIQUE NOT NULL, 
                description VARCHAR NULL
                );
        """)

    def _create_dataapps_table(self, conn: Connection):
        conn.execute("""
            CREATE TABLE dataapps (
                name VARCHAR NOT NULL, 
                version DECIMAL NOT NULL, 
                description VARCHAR NULL,
                creationDate BIGINT NOT NULL,
                updateDate BIGINT NOT NULL,
                spec VARCHAR NOT NULL, 
                tags VARCHAR[] NULL
                );
        """)

    @property
    def version(self) -> int:
        return 1

    def setup(self, conn: Connection):
        with transaction() as conn:
            self._create_sequence(conn)
            self._create_user_table(conn)
            self._create_principals_table(conn)
            self._create_unp_challenges(conn)
            self._create_unp_users(conn)
            self._create_relations(conn)
            self._create_groups_table(conn)
            self._create_dataapps_table(conn)

    def patch(self, conn: Connection):
        # Since this is the first version, no patching
        pass

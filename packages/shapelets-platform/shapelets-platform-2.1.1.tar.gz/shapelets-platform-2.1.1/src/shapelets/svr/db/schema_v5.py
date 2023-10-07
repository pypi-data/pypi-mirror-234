from .native import Connection, transaction
from .schema_builder import SchemaBuilder


class BuilderV5(SchemaBuilder):
    """
    Database Schema Version 5
    - Creates sequence table to store sequence info
        id: uuid
        name: optional name for the sequence. It is used when plot
        length: sequence total length
        starts: epoch time where the sequence begins
        every: period between each point
        ends: epoch time where the sequence finishes
        number_of_levels
        chunk_size
        elements_per_block: is a List[List[int]] where each list represents a level and each element inside represents
            the count of elements in that block. This list is serialized and save in database as a string.
    """

    @staticmethod
    def _create_sequences_table(conn: Connection):
        conn.execute("""
            CREATE TABLE sequences(
                id VARCHAR PRIMARY KEY,
                name VARCHAR,
                length INTEGER NOT NULL, 
                starts BIGINT NOT NULL, 
                every BIGINT NOT NULL,
                ends BIGINT NOT NULL, 
                axis_type VARCHAR,
                number_of_levels INTEGER, 
                chunk_size INTEGER NOT NULL, 
                elements_per_block VARCHAR
                );
        """)

    @property
    def version(self) -> int:
        return 5

    def setup(self):
        pass

    def patch(self, conn: Connection):
        with transaction() as conn:
            self._create_sequences_table(conn)

from datetime import datetime
from fastsql import conn_db
from sqlalchemy import text
from l402.server.macaroons import MacaroonService

class FastSQLMacaroonService(MacaroonService):
    def __init__(self, db_url):
        self.db = conn_db(db_url, pool_pre_ping=True)
        self.is_sqlite = db_url.startswith('sqlite://')
        self._create_table()

    def _create_table(self):
        pk_type = 'INTEGER PRIMARY KEY AUTOINCREMENT' if self.is_sqlite else 'SERIAL PRIMARY KEY'
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS macaroons (
            id {pk_type},
            token_id BLOB UNIQUE NOT NULL,
            root_key BLOB NOT NULL,
            macaroon TEXT,
            created_at TIMESTAMP NOT NULL
        )
        """ 
        
        create_index_sql = """
        CREATE INDEX IF NOT EXISTS macaroons_token_id_idx ON macaroons (token_id)
        """

        with self.db.bind.connect() as conn:
            conn.execute(text(create_table_sql))
            conn.execute(text(create_index_sql))
            conn.commit()

    async def insert_root_key(self, token_id: bytes, root_key: bytes, macaroon: str):
        insert_sql = """
        INSERT INTO macaroons (token_id, root_key, macaroon, created_at)
        VALUES (:token_id, :root_key, :macaroon, :created_at)
        """
        created_at = datetime.now()
        with self.db.bind.connect() as conn:
            conn.execute(text(insert_sql), {
                "token_id": token_id,
                "root_key": root_key,
                "macaroon": macaroon,
                "created_at": created_at
            })
            conn.commit()

    async def get_root_key(self, token_id: bytes) -> bytes:
        select_sql = "SELECT root_key FROM macaroons WHERE token_id = :token_id"
        with self.db.bind.connect() as conn:
            result = conn.execute(text(select_sql), {"token_id": token_id})
            row = result.fetchone()
            return row[0] if row else None
import psycopg2
from psycopg2.extras import RealDictCursor

from typing import List, Optional

from database import DatabaseInterface, Item

class PostgreSQLDatabase(DatabaseInterface):
    def __init__(self, **kwargs):
        self.conn = psycopg2.connect(**kwargs)
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    cover_image TEXT,
                    file_path TEXT
                )
            ''')
        self.conn.commit()

    def insert_item(self, item: Item) -> Item:
        with self.conn.cursor() as cur:
            cur.execute('''
                INSERT INTO items (title, description, price, cover_image, file_path)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', (item.title, item.description, item.price, item.cover_image, item.file_path))
            item.id = cur.fetchone()[0]
        self.conn.commit()
        return item

    def get_item(self, id: int) -> Optional[Item]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM items WHERE id = %s', (id,))
            row = cur.fetchone()
            if row:
                return Item(**row)
        return None

    def get_all_items(self) -> List[Item]:
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT * FROM items')
                rows = cur.fetchall()
                return [Item(**row) for row in rows]
        except psycopg2.Error as e:
            logging.error(f"Database error in get_all_items: {e}")
            return []
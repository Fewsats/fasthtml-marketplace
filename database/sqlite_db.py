import os
import sqlite3
from typing import List, Optional

from database import DatabaseInterface, Item

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    cover_image TEXT,
                    file_path TEXT
                )
            ''')

    def insert_item(self, item: Item) -> Item:
        with self.conn:
            cursor = self.conn.execute('''
                INSERT INTO items (title, description, price, cover_image, file_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (item.title, item.description, item.price, item.cover_image, item.file_path))
            item.id = cursor.lastrowid
        return item

    def get_item(self, id: int) -> Optional[Item]:
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM items WHERE id = ?', (id,))
            row = cursor.fetchone()
            if row:
                return Item(**row)
        return None

    def get_all_items(self) -> List[Item]:
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM items')
            return [Item(**row) for row in cursor.fetchall()]
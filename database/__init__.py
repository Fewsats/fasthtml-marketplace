import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Item:
    title: str
    description: str
    price: int
    cover_image: str
    file_path: str
    id: Optional[int] = None


class DatabaseInterface(ABC):

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def insert_item(self, item: Item) -> Item:
        pass

    @abstractmethod
    def get_item(self, id: int) -> Optional[Item]:
        pass

    @abstractmethod
    def get_all_items(self) -> List[Item]:
        pass


def get_database(db_type='sqlite') -> DatabaseInterface:
    if db_type == 'sqlite':
        from database.sqlite_db import SQLiteDatabase
        return SQLiteDatabase('data/marketplace.db')

    elif db_type == 'postgresql':
        # import here to avoid psycopg2 dependency when using sqlite
        from database.postgresql_db import PostgreSQLDatabase
        return PostgreSQLDatabase(host=os.environ.get('PGHOST'),
                                  database=os.environ.get('PGDATABASE'),
                                  user=os.environ.get('PGUSER'),
                                  password=os.environ.get('PGPASSWORD'),
                                  port=os.environ.get('PGPORT'))
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

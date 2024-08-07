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
        from database.postgresql_db import PostgreSQLDatabase
        return PostgreSQLDatabase(host=os.environ.get('DB_HOST'),
                                  database=os.environ.get('DB_NAME'),
                                  user=os.environ.get('DB_USER'),
                                  password=os.environ.get('DB_PASSWORD'))
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

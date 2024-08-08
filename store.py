from dataclasses import dataclass
from typing import List
from sqlalchemy import text
from fastcore.basics import patch
from fasthtml.common import *
from fastsql import *
from sqlalchemy import text, MetaData

@dataclass
class Item:
    id: int
    title: str
    description: str
    price: int
    cover_image: str
    file_path: str

    @classmethod
    def from_row(cls, row):
        return cls(**{k: getattr(row, k) for k in cls.__annotations__})

@patch 
def __ft__(self: Item):
    price = f'${self.price / 100:.2f}'
    cover_image = f'/files/{self.cover_image}' if self.cover_image else 'https://via.placeholder.com/250x200'
    return Div(Card(
        Img(src=cover_image, alt=self.title, cls="card-img-top"),
        Div(H3(self.title, cls="card-title"),
            P(self.description[:100] + '...' if len(self.description) > 100 else self.description, cls="card-text"),
            P(B("Price: "), price, cls="card-text"),
            A("Download Link", href=f"/download/{self.id}", cls="btn btn-primary"),
            A("Pay with Hub", href=f"https://app.paywithhub.com/purchases?l402_url=https://fast-html-l402-market.replit.app/download/{self.id}", cls="btn btn-primary"),
            cls="card-body")),
        id=f'item-{self.id}',
        cls="col-xs-12 col-sm-6 col-md-4 col-lg-3")

def get_db(connstr):
    db = conn_db(connstr, pool_pre_ping=True)
    _create_items_table(db)
    return db

def _create_items_table(db):
    is_sqlite = db.bind.url.drivername == 'sqlite'
    pk_type = 'INTEGER PRIMARY KEY AUTOINCREMENT' if is_sqlite else 'SERIAL PRIMARY KEY'
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS items (
        id {pk_type},
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL,
        cover_image TEXT,
        file_path TEXT
    )
    """
    with db.bind.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()

@patch
def get_items(self: MetaData) -> List[Item]:
    with self.bind.connect() as conn:
        result = conn.execute(text("SELECT * FROM items ORDER BY id DESC"))
        return [Item.from_row(row) for row in result]

@patch
def get_item(self: MetaData, id: int) -> Item:
    with self.bind.connect() as conn:
        result = conn.execute(text("SELECT * FROM items WHERE id = :id"), {"id": id})
        row = result.fetchone()
        return Item.from_row(row) if row else None

@patch
def create_item(self: MetaData, item_data: dict) -> Item:
    with self.bind.connect() as conn:
        insert_sql = """
        INSERT INTO items (title, description, price, cover_image, file_path)
        VALUES (:title, :description, :price, :cover_image, :file_path)
        """
        result = conn.execute(text(insert_sql), item_data)
        conn.commit()
        return self.get_items()[0]  # Get the most recently inserted item
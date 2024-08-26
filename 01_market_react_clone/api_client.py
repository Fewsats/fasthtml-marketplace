import httpx
from typing import List
from dataclasses import dataclass
from item_card import ItemCard

API_URL = "https://api.fewsats.com/v0/storage"

@dataclass
class Item:
    id: str
    title: str
    description: str
    price: int
    cover_image: str
    file_path: str
    tags: str = ""

    def __ft__(self):
        return ItemCard(self)

async def fetch_items() -> List[Item]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/search")
        response.raise_for_status()
        data = response.json()
        return [map_api_item_to_item(item) for item in data.get("files", []) if item['status'] == 'valid']

def map_api_item_to_item(api_item: dict) -> Item:
    return Item(
        id=api_item["external_id"],
        title=api_item["name"],
        description=api_item["description"],
        price=api_item["price_in_cents"],
        cover_image=api_item["cover_url"],
        file_path=api_item["l402_url"],
        tags=";".join(api_item["tags"])
    )

async def fetch_single_item(item_id: str) -> Item:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/{item_id}")
        response.raise_for_status()
        api_item = response.json()
        return map_api_item_to_item(api_item['file'])
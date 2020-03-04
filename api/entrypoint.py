from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict


api = FastAPI()


class Item(BaseModel):
    id: int
    title: str


items: Dict = {
    42: dict(id=42, title="Title")
}


@api.get("/items")
async def get_items(start_from: int = 0, limit: int = 10) -> List[Item]:
    return sorted(items.values())[start_from : start_from + limit]


@api.get("/items/{item_id}")
async def get_item(item_id: int) -> Item:
    return items[item_id]


@api.post("/items")
async def create_item(item: Item) -> None:
    if item.id not in items:
        items[item.id] = item
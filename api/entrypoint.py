from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from typing import List, Dict


api = FastAPI()


class Item(BaseModel):
    id: int = Field(..., description="Unique ID")
    title: str = Field(..., description="Title of stuff", max_length=40)


items: Dict = {
    42: dict(id=42, title="Title")
}


@api.get("/items", response_model=List[Item])
async def get_items(start_from: int = 0, limit: int = 10):
    return sorted(items.values())[start_from : start_from + limit]


@api.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    return items[item_id]


@api.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    if item.id not in items:
        items[item.id] = item
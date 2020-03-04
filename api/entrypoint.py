from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict


api = FastAPI()


class Item(BaseModel):
    id: int = Field(..., description="Unique ID")
    title: str = Field(..., description="Title of stuff", max_length=40)


items: Dict = {
    42: dict(id=42, title="Title")
}


@api.get("/items", response_model=List[Item], status_code=status.HTTP_200_OK)
async def get_items(start_from: int = 0, limit: int = 10):
    return sorted(items.values())[start_from : start_from + limit]


@api.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(404, "Item doesn't exist")
    return items[item_id]


@api.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    if item.id in items:
        raise HTTPException(409, "Item with such id already exists")
    items[item.id] = item


@api.put("/items", status_code=status.HTTP_204_NO_CONTENT)
async def put_item(item: Item):
    items[item.id] = item


@api.put("/items", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    items.pop(item_id, None)

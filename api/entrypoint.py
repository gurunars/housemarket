from fastapi import FastAPI, status, HTTPException
from typing import List

from .item import (
    Item, ItemBody, get_items, exists_item, create_item, get_item,
    put_item, delete_item
)
from .db import init_db


api = FastAPI()

init_db()


@api.get("/items", response_model=List[Item], status_code=status.HTTP_200_OK)
async def _get_items(start_from: int = 0, limit: int = 10):
    return get_items(start_from, limit)


@api.post("/items", status_code=status.HTTP_201_CREATED)
async def _create_item(item: Item):
    if exists_item(item):
        raise HTTPException(409, "Item with such id already exists")
    create_item(item)


@api.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def _get_item(item_id: int):
    item = get_item(item_id)
    if item is None:
        raise HTTPException(404, "Item doesn't exist")
    return item


@api.put("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def _put_item(item_id: int, item: ItemBody):
    put_item(item_id, item)


@api.delete("/items", status_code=status.HTTP_204_NO_CONTENT)
async def _delete_item(item_id: int):
    delete_item(item_id)

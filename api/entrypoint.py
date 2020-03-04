from fastapi import FastAPI

api = FastAPI()


items = {
    42: dict(id=42, title="Title")
}


@api.get("/items")
async def get_items(start_from: int = 0, limit: int = 10):
    return sorted(items.values())[start_from : start_from + limit]


@api.get("/items/{item_id}")
async def get_item(item_id: int):
    return items[item_id]


@api.post("/items")
async def create_item():
    return "Created"
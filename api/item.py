from typing import List, Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import exists as db_exists

from pydantic import BaseModel, Field

from .db import Base, create_session


class ItemBody(BaseModel):
    title: str = Field(..., description="Title of stuff", max_length=40)


class Item(ItemBody):
    id: int = Field(..., description="Unique ID")


class DbItem(Base):
    __tablename__ = "item"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, max_length=40)

    def to_item(self):
        return Item(id=self.id, title=self.title)

    @staticmethod
    def from_item(item: Item):
        return DbItem(id=item.id, title=item.title)


def get_items(start_from: int = 0, limit: int = 10) -> List[Item]:
    with create_session() as session:
        return [
            it.to_item()
            for it in session.query(DbItem).offset(start_from).limit(limit).all()
        ]


def create_item(item: Item):
    with create_session() as session:
        session.add(DbItem.from_item(item))


def get_item_count():
    with create_session() as session:
        return session.query(DbItem).count()


def exists_item(item: Item) -> bool:
    with create_session() as session:
        return session.query(
            db_exists().where(DbItem.id == item.id)
        ).scalar()


def get_item(item_id: int) -> Optional[Item]:
    with create_session() as session:
        return session.query(DbItem).filter(DbItem.id == item_id).first().to_item()


def delete_item(item_id: int):
    with create_session() as session:
        session.query(DbItem).filter(DbItem.id == item_id).delete()


def set_item(item: Item):
    with create_session() as session:
        session.query(DbItem).filter(DbItem.id == item.id).update({"title": item.title})


def put_item(item_id: int, item_body: ItemBody):
    item = Item(id=item_id, title=item_body.title)
    if exists_item(item):
        set_item(item)
    else:
        create_item(item)

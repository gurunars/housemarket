from .item import create_item, Item, get_item_count


def create_item_fixtures():
    if get_item_count() != 0:
        return
    for it in range(1, 20):
        create_item(Item(id=it, title="title-{}".format(it)))


def init_fixtures():
    create_item_fixtures()

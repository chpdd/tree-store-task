from pydantic import BaseModel
from typing import Iterable

class StoreItem(BaseModel):
    parent: str | int
    childrens_ids: list[int] = []
    type: str

    def __repr__(self):
        return f"StoreItem(parent: {self.parent}, childrens_ids: {self.childrens_ids})"


class TreeStore:
    def __init__(self, items):
        if not items:
            self._items = {}
        else:
            if not isinstance(items, Iterable):
                raise TypeError(f'Invalid "items" type {type(items)}, there must be a Iterable')
            root_items = []
            for item in items:
                if not isinstance(item, dict):
                    raise TypeError(f'Invalid "items" element type {type(item)}, there must be a dict')
                if item.get('parent', None) == 'root':
                        root_items.append(item)
            if not len(root_items) == 1:
                raise ValueError(f'"items" must contain 1 item with parent = "root", not {len(root_items)}')
            root_item = root_items[0]
            actual_parent_id = root_item.get("id", None)
            if not actual_parent_id:
                raise ValueError(f"Invalid item id")
            self._items[actual_parent_id] = StoreItem(parent="root", childrens_ids=[])


    def getAll(self):
        ...

    def getItem(self, id):
        ...

    def getChildren(self, id):
        ...

    def getAllParents(self, id):
        ...


from pydantic import BaseModel, TypeAdapter
from typing import Any, Optional


class Item(BaseModel):
    """
    Pydantic model for validating items passed to the TreeStore constructor
    """
    id: int
    parent: int | str
    type: str | None = None


class TreeStore:
    """
    Class for working with a tree-like data structure.
    Provides O(1) access to items and their children through 
    pre-indexing in the constructor.
    """
    def __init__(self, items: list[dict[str, Any]]):
        # Validate the entire list at once
        type_adapter = TypeAdapter(list[Item])
        type_adapter.validate_python(items)

        self._initial_items = items
        self._items_by_id: dict[int, dict[str, Any]] = {}
        self._childrens_by_parent: dict[int | str, list[dict[str, Any]]] = {}

        for item in items:
            self._items_by_id[item.get('id')] = item
            parent_id = item.get('parent')
            if parent_id not in self._childrens_by_parent:
                self._childrens_by_parent[parent_id] = []
            self._childrens_by_parent[parent_id].append(item)

    def getAll(self) -> list[dict[str, Any]]:
        """Returns the original array of items."""
        return self._initial_items

    def getItem(self, id: int) -> Optional[dict[str, Any]]:
        """Returns an item by its ID."""
        return self._items_by_id.get(id)

    def getChildren(self, id: int) -> list[dict[str, Any]]:
        """Returns an array of child items for the given ID."""
        return self._childrens_by_parent.get(id, [])

    def getAllParents(self, id: int) -> list[dict[str, Any]]:
        """Returns an array of parent items from the current item to the root."""
        result = []
        current_item = self.getItem(id)

        while current_item:
            parent_id = current_item.get('parent')

            # If parent_id is "root" or None, there's nowhere else to go
            if parent_id == "root" or parent_id is None:
                break

            parent_item = self.getItem(parent_id)
            # If the item doesn't exist, we stop
            if not parent_item:
                break

            result.append(parent_item)
            current_item = parent_item

        return result

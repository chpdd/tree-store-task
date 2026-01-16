from pydantic import BaseModel, TypeAdapter
from typing import Any, Optional


class Item(BaseModel):
    """
    Pydantic модель для валидации значений вставленных в конструктор TreeStore
    """
    id: int
    parent: int | str
    type: str | None = None


class TreeStore:
    """
    Класс для работы с древовидной структурой данных.
    Обеспечивает O(1) доступ к элементам и их дочерним узлам за счет
    предварительной индексации в конструкторе.
    """

    def __init__(self, items: list[dict[str, Any]]):
        # Валидация всего списка сразу
        adapter = TypeAdapter(list[Item])
        validated_items = adapter.validate_python(items)

        self._all_items = items
        self._items_by_id: dict[int, dict[str, Any]] = {}
        self._children_by_parent: dict[int | str, list[dict[str, Any]]] = {}

        for item in items:
            item_id = item.get('id')
            parent_id = item.get('parent')

            self._items_by_id[item_id] = item

            if parent_id not in self._children_by_parent:
                self._children_by_parent[parent_id] = []
            self._children_by_parent[parent_id].append(item)

    def getAll(self) -> list[dict[str, Any]]:
        """Возвращает изначальный массив элементов."""
        return self._all_items

    def getItem(self, id: int) -> Optional[dict[str, Any]]:
        """Возвращает элемент по его id."""
        return self._items_by_id.get(id)

    def getChildren(self, id: int) -> list[dict[str, Any]]:
        """Возвращает массив дочерних элементов для элемента с заданным id."""
        return self._children_by_parent.get(id, [])

    def getAllParents(self, id: int) -> list[dict[str, Any]]:
        """
        Возвращает массив из цепочки родительских элементов от текущего до корня.
        Порядок важен: от ближайшего родителя к корню.
        """
        result = []
        current_item = self.getItem(id)

        while current_item:
            parent_id = current_item.get("parent")

            # Если parent_id == "root" или None значит дальше идти некуда
            if parent_id == "root" or parent_id is None:
                break

            parent_item = self.getItem(parent_id)
            # Если элемента нет, значит дальше идти некуда
            if not parent_item:
                break

            result.append(parent_item)
            current_item = parent_item

        return result

import pytest

from src.tree_store import TreeStore

@pytest.fixture
def tree_store_instance():
    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None}
    ]
    tree_store = TreeStore(items)
    return tree_store

@pytest.fixture
def test_init(tree_store):
    expected = [
        {1: {"items": [2, 3], "parent": "root"}, 2: [4, 5, 6], 3: [], 4: [7, 8], 5: [], 6: [], 7: [], 8: []},
    ]
    print(tree_store._items)

@pytest.fixture
def test_get_all(tree_store):
    get_all_items = tree_store.getAll()
    expected_items = [{"id": 1, "parent": "root"}, {"id": 2, "parent": 1, "type": "test"},
                      {"id": 3, "parent": 1, "type": "test"}, {"id": 4, "parent": 2, "type": "test"},
                      {"id": 5, "parent": 2, "type": "test"}, {"id": 6, "parent": 2, "type": "test"},
                      {"id": 7, "parent": 4, "type": None}, {"id": 8, "parent": 4, "type": None}]
    assert get_all_items == expected_items


@pytest.fixture
def test_get_item(tree_store):
    expected = {"id": 7, "parent": 4, "type": None}
    assert tree_store.getItem(7) == expected


@pytest.fixture
@pytest.mark.parametrize(
    "children_id expected"
    [
        (4, [{"id": 7, "parent": 4, "type": None}, {"id": 8, "parent": 4, "type": None}]),
        (5, [])
    ]
)
def test_get_children(tree_store, children_id, expected):
    assert tree_store.getChildren(children_id) == expected


@pytest.fixture
def test_get_all_parents(tree_store):
    expected = [{"id": 4, "parent": 2, "type": "test"}, {"id": 2, "parent": 1, "type": "test"},
                {"id": 1, "parent": "root"}]
    assert tree_store.getAllParents(7) == expected

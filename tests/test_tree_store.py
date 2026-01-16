import pytest
from tree_store import TreeStore


@pytest.fixture
def initial_items():
    return [
        {'id': 1, 'parent': 'root'},
        {'id': 2, 'parent': 1, 'type': 'test'},
        {'id': 3, 'parent': 1, 'type': 'test'},
        {'id': 4, 'parent': 2, 'type': 'test'},
        {'id': 5, 'parent': 2, 'type': 'test'},
        {'id': 6, 'parent': 2, 'type': 'test'},
        {'id': 7, 'parent': 4, 'type': None},
        {'id': 8, 'parent': 4, 'type': None}
    ]


@pytest.fixture
def tree_store(initial_items):
    return TreeStore(initial_items)


def test_get_all(tree_store, initial_items):
    assert tree_store.getAll() == initial_items


@pytest.mark.parametrize(
    argnames=['item_id', 'expected'],
    argvalues=[
        (7, {'id': 7, 'parent': 4, 'type': None})
    ]
)
def test_get_item(tree_store, item_id, expected):
    assert tree_store.getItem(item_id) == expected


@pytest.mark.parametrize(
    argnames=['item_id', 'expected'],
    argvalues=[
        (4, [
            {'id': 7, 'parent': 4, 'type': None},
            {'id': 8, 'parent': 4, 'type': None}
        ]),
        (5, [])
    ]
)
def test_get_children(tree_store, item_id, expected):
    assert tree_store.getChildren(item_id) == expected


@pytest.mark.parametrize(
    argnames=['item_id', 'expected'],
    argvalues=[
        (7, [
            {'id': 4, 'parent': 2, 'type': 'test'},
            {'id': 2, 'parent': 1, 'type': 'test'},
            {'id': 1, 'parent': 'root'}
        ])
    ]
)
def test_get_all_parents(tree_store, item_id, expected):
    assert tree_store.getAllParents(item_id) == expected

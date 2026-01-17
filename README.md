# TreeStore

A Python library for efficient management and retrieval of tree-like data structures. It uses pre-indexing to provide **O(1)** access to items and their children.

## Features

- **Pydantic Validation**: Ensures data integrity using Pydantic V2.
- **Fast Lookups**: Instant access to any item by ID.
- **Relationship Mapping**: Quickly find direct children or the entire parent chain.
- **Type Safety**: Fully type-hinted for better developer experience.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
poetry install
```

## Usage

```python
from tree_store import TreeStore

items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
]

ts = TreeStore(items)

# Get all items
ts.getAll()

# Get a specific item
ts.getItem(2) # {"id": 2, "parent": 1, "type": "test"}

# Get children of an item
ts.getChildren(1) # [{"id": 2, ...}, {"id": 3, ...}]

# Get all parents in order (from closest to root)
ts.getAllParents(4) # [{"id": 2, ...}, {"id": 1, ...}]
```

## API Reference

### `TreeStore(items: list[dict])`
Initialized with a list of dictionaries. Each dictionary must have at least `id` (int) and `parent` (int or "root").

- `getAll()`: Returns the original list of items.
- `getItem(id: int)`: Returns the item dictionary or `None`.
- `getChildren(id: int)`: Returns a list of direct children.
- `getAllParents(id: int)`: Returns a list of all ancestors from the immediate parent up to the root.

## Development

### Running Tests

```bash
poetry run pytest
```

## License

MIT
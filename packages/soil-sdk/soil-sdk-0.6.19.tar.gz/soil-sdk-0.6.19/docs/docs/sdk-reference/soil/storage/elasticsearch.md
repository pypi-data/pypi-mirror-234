---
sidebar_label: elasticsearch
title: soil.storage.elasticsearch
---

Module for Elasticsearch storage

## Elasticsearch Objects

```python
@dataclass
class Elasticsearch(BaseStorage)
```

This class implements Elasticsearch storage.

**Attributes**:

- `index` - str: The index name to store the data to. It will be
  automatically prefixed with the app_id.

#### search

```python
def search(body: Dict[str, Any],
           auto_scroll: bool = True,
           **kwargs: Any) -> Any
```

Perform a search in elasticsearch in the idnex self.index.

**Attributes**:

- `body` - The body of the search
- `auto_scroll` - If an auto_scroll has to be done.
  
- `Returns` - if auto_scroll is true it will return a tuple with a generator
  with the results as first element and metadata as second element.
  Otherwise it will return everything together.

#### create\_index

```python
def create_index(schema: Optional[Dict[str, Any]] = None) -> None
```

Creates an index with the schema or an empty schema.
If the index already exists it does nothing.

#### delete\_index

```python
def delete_index() -> None
```

Deletes the index

#### bulk

```python
def bulk(actions: Iterable[Any]) -> Any
```

Performs bulk operations to the index only.


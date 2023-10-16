---
sidebar_label: compound_storage
title: soil.storage.compound_storage
---

Module for the compound storage

## CompoundStorage Objects

```python
@dataclass
class CompoundStorage(BaseStorage)
```

A meta storage composed of other storages as a dict.

**Example**:

  compound = CompoundStorage(storages={
- `&quot;db&quot;` - Elasticsearch(index=&quot;index1&quot;),
- `&quot;disk&quot;` - ObjectStorage()
  })
  compound[&quot;second_db&quot;] = ElasticSearch(index=&quot;index2&quot;)
  compound[&quot;db&quot;].search(query=myquery)

#### \_\_getitem\_\_

```python
def __getitem__(storage_name: str) -> BaseStorage
```

Return the storage with that storage_name

#### \_\_setitem\_\_

```python
def __setitem__(storage_name: str, storage: BaseStorage) -> None
```

Set storage to that storage_name

#### \_\_len\_\_

```python
def __len__() -> int
```

Returns the number of storages

#### items

```python
def items() -> List[Tuple[str, BaseStorage]]
```

Returns an iterable of sotrage_name, storage tuples


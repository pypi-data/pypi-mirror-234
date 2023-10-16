---
sidebar_label: base_storage
title: soil.storage.base_storage
---

Module for BaseStorage

## BaseStorage Objects

```python
@dataclass
class BaseStorage()
```

Abstract class that implements serialize and deserialize methods for storage classes.

#### serialize

```python
def serialize() -> Dict[str, Any]
```

Serializes the storage object. In general it shouldn&#x27;t be used from a module.

#### deserialize

```python
@classmethod
def deserialize(cls: Type[StorageClass],
                serialized_storage_object: Dict[str, Any]) -> StorageClass
```

Takes a serialized storage object and returns an instance.


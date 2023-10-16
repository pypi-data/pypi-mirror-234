---
sidebar_label: object_ds
title: data_structures.predefined.object_ds
---

## ObjectDS Objects

```python
class ObjectDS(DataStructure)
```

Basic DataStructure to Store json serializable objects

#### serialize

```python
 | serialize()
```

Serializes the data and stores them using ObjectStorage.
The data must be json serializable.

#### deserialize

```python
 | @classmethod
 | deserialize(cls, obj_storage: ObjectStorage, metadata)
```

Deserializes the data obtaining them from ObjectStorage.


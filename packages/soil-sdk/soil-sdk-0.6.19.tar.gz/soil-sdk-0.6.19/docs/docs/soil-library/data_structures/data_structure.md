---
sidebar_label: data_structure
title: data_structures.data_structure
---

## DataStructure Objects

```python
class DataStructure()
```

Base class for all the data structures.

#### \_\_init\_\_

```python
 | __init__(data, metadata=None, db_object=None, storage=None)
```

**Attributes**:

- `data` - stored in self.data
- `metadata` - a dictionary stored in self.metadata
- `db_object` - Optional database object to store the object in a
  database.

#### serialize

```python
 | serialize()
```

Method to serialize the data.

**Returns**:

- `string` - To serialize to disk normally.
- `binary` - To store a object serialized with pickle
- `None` - if the result was stored using the db_object
  

**Raises**:

  NotImplementedError

#### unserialize

```python
 | @staticmethod
 | unserialize(data, metadata=None, db_object=None)
```

DEPRECATED use deserialize() instead.
Method to deserialize the data.

**Attributes**:

- `data` - the serialized data.
- `metadata` - the metadata (sometimes is necessary to deserialize)
- `db_object` - The db_object that was used to serialize (if any).
  

**Returns**:

  An initialized object with the
  

**Raises**:

  NotImplementedError

#### get\_data

```python
 | get_data(**args)
```

Method to query the data from the api.
The arguments will change depending on the class.

**Raises**:

  NotImplementedError

#### export

```python
 | export(format='csv')
```

Method to export the data.

**Attributes**:

- `format` - The format to return the data.
  

**Returns**:

  A dictionary of generators that will be serialized and compressed in a zip file.
  Each generator will be a diferent file in the zip.
  

**Raises**:

  NotImplementedError


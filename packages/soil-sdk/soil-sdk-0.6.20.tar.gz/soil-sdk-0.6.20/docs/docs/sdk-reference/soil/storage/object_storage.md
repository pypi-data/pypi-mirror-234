---
sidebar_label: object_storage
title: soil.storage.object_storage
---

Module for Object Storage

## ObjectStorage Objects

```python
@dataclass
class ObjectStorage(BaseStorage)
```

Implements basic Object Storage using s3 api. If there are no s3 credentials
it fallsback to disk. Before storing the data they are compressed with zlib.

**Example**:

  class ObjectDS(DataStructure):
  def serialize(self):
  obj_storage = ObjectStorage()
  obj_storage.put_object(json.dumps(self.data).encode(&#x27;utf-8&#x27;))
  return obj_storage
  
  @staticmethod
  def deserialize(obj_storage: ObjectStorage, metadata):
  raw_data = obj_storage.get_object()
  data = json.loads(raw_data.decode(&#x27;utf-8&#x27;))
  return ObjectDS(data, metadata, storage=obj_storage)
  
  def get_data(self):
  return self.data
  

**Attributes**:

- `path` - str = &#x27;&#x27;: An optional folder to store the data to.
- `obj_name` - Optional[str]: The obj_name can optionally be provided. Otherwise
  a unique name will be generated. Caution! Existing data for the same app
  will be overwritten if the same name is used twice.
- `metadata` - Optional[Dict[str, Any]]: Experimental. Metadata to be stored in the s3 storage.

#### put\_object

```python
def put_object(obj: bytes) -> None
```

Compressess an object and stores it.

#### get\_object

```python
def get_object() -> bytes
```

Gets the object back and decompresses it.


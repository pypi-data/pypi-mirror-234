---
sidebar_label: data_structure
title: soil.data_structure
---

This module implements a Data Structure

## DataStructure Objects

```python
class DataStructure()
```

Data Structure class

#### get\_data

```python
def get_data(**kwargs: Dict[str, Any]) -> Dict[Union[str, int], Any]
```

Invoke the get_data() method from the data structure in the cloud.

#### export

```python
def export(path: str, **kwargs: Dict[str, Any]) -> str
```

Export a result to a file. The file will be stored in the folder
and returns the file_path.

#### get\_id

```python
def get_id() -> str
```

Invoke the get_data() method from the data structure in the cloud.

#### get\_data\_structure\_name\_and\_serialize

```python
def get_data_structure_name_and_serialize(data_object: Any) -> Tuple[str, str]
```

Get the data structure and serialize it.


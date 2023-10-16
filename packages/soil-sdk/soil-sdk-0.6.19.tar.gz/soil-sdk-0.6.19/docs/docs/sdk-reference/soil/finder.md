---
sidebar_label: finder
title: soil.finder
---

This module overrides Python&#x27;s import system
https://docs.python.org/3/library/importlib.html
https://stackoverflow.com/a/43573798/3481480

## Finder Objects

```python
class Finder(MetaPathFinder)
```

Custom finder that uploads a module or data_structure to the cloud and if
the module is not found locally it is downloaded from the cloud

#### find\_spec

```python
def find_spec(
        fullname: str,
        path: Optional[Sequence[Union[bytes, str]]],
        target: Optional[types.ModuleType] = None) -> Optional[ModuleSpec]
```

find_spec implementation

## CustomLoader Objects

```python
class CustomLoader(Loader)
```

This class runs modules and uploads them

#### create\_module

```python
def create_module(spec: ModuleSpec) -> None
```

Use default module creation semantics

#### exec\_module

```python
def exec_module(module: types.ModuleType) -> None
```

Load code if necessary, upload it and run it.

#### install

```python
def install() -> None
```

Inserts the finder into the import machinery


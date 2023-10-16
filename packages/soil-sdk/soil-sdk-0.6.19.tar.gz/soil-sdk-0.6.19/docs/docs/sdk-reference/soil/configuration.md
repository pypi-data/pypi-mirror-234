---
sidebar_label: configuration
title: soil.configuration
---

Defines the configuration for Soil

#### get\_soil\_root

```python
def get_soil_root(relpath: str) -> Optional[str]
```

Checks if the current dir is under a soil environment
and returns its root. Returns None otherwise.

## SoilConfiguration Objects

```python
class SoilConfiguration(NamedTuple)
```

Soil configuration class

#### \_\_getattribute\_\_

```python
def __getattribute__(name: str) -> str
```

Refresh the token if necessary before accessing it.


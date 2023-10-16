---
sidebar_label: modulify
title: soil.modulify
---

This module defines the @modulify decorator.

#### modulify

```python
@decorator(depth=2)
def modulify(_func: Optional[Callable[..., List[DataStructure]]] = None,
             *,
             output_types: Optional[Callable] = None,
             centralize: bool = False,
             distribute: bool = False,
             federating: bool = False,
             num_outputs: int = 1,
             _from_db: bool = False) -> Callable
```

Decorates a function to mark it as a soil module.


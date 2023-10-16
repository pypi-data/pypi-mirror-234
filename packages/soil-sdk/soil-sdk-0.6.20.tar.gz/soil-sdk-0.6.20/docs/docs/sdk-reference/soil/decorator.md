---
sidebar_label: decorator
title: soil.decorator
---

soil.decorator package.

#### decorator

```python
def decorator(depth: Optional[int] = None) -> Callable
```

This is a decorator of decorators. It allows to serialize a
decorator that is not fully executed.

If the decorated function is executed with __show_calls it will return the lists
of args and kwargs that ran until that moment.

When the function is fully executed it will run normally.

**Attributes**:

- `depth` - The number of times the decorator will return a function.


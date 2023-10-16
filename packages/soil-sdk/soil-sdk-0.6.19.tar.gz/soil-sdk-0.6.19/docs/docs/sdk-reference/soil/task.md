---
sidebar_label: task
title: soil.task
---

Package for soil.task

#### task

```python
def task(modulified_module: Callable) -> Callable
```

Decorates a modulified module in soil. This function is to call
soil modules from other soil modules.

**Example**:

  task(my_module)(data, arg1=&#x27;val1&#x27;)

#### task\_wait

```python
def task_wait(futures: Any) -> Any
```

Wait until computation completes and gather results.

Accepts a future, nested container of futures, iterator, or queue.
The return type will match the input type.

**Example**:

  result = tasks_wait([future1, future2])


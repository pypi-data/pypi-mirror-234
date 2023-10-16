---
sidebar_label: utils
title: soil.utils
---

This module defines some useful functions

#### generate\_data\_structure\_ids

```python
def generate_data_structure_ids(fn_name: str, quantity: int) -> List[str]
```

Generates an id for a datastructure

#### build\_function

```python
def build_function(function: Callable) -> Dict[str, Any]
```

Mounts the argument structure to serialize a function. It uses the reserved dict key
`__soil_arg_type` to mark a function. The function code must be inside modules or
data_structures folders.
It recognises 3 types of functions:
    * Named functions: `__soil_arg_type=&#x27;function&#x27;` functions with a module
        and a name.
    * Lambda functions: `__soil_arg_type=&#x27;lambda&#x27;` They are not actually serialized
        but kept as a placeholder for the pattern matching in the server.
        They can only be used as a decorator parameter.
    * Decorated functions: `__soil_arg_type=&#x27;decorated&#x27;` A function that has been
        decorated with one or more decorators that have been decorated with
        soil.decorator or functions returned by that decorated function.

#### build\_arguments

```python
def build_arguments(args: Any) -> Any
```

Transforms the module arguments into serializable arguments

#### generate\_transformation

```python
def generate_transformation(input_ids: List[str], output_ids: List[str],
                            fn_name: str, args: Dict[str,
                                                     Any]) -> Dict[str, Any]
```

Mounts the dictionary for a module in a plan


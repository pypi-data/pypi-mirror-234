---
sidebar_label: experiment
title: modules.experiment
---

## Experiment Objects

```python
class Experiment()
```

Abstract class for experiments

#### do

```python
 | do(*pargs)
```

Gets the inputs and returns the data for the Results

#### get\_output\_types

```python
 | @staticmethod
 | get_output_types(inputs, args)
```

Get the output types. Raises error if the experiment cannot handle
the inputs


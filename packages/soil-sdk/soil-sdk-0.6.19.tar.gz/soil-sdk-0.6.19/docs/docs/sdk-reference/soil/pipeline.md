---
sidebar_label: pipeline
title: soil.pipeline
---

This module defines a Pipeline.

## Pipeline Objects

```python
class Pipeline()
```

A Pipeline stores the transformations and dependencies to obtain certain results.

#### run

```python
def run() -> Dict[str, str]
```

Run the Pipeline (blocking call until the experiment finishes)

#### add\_transformation

```python
def add_transformation(transformation: Dict[str, str]) -> Pipeline
```

Add a new transformation to the Pipeline, returns a new Pipeline
containing the plan of the old Pipeline plus the transformation.

#### merge\_pipelines

```python
@staticmethod
def merge_pipelines(*pipelines: Pipeline) -> Pipeline
```

Merges all the Pipelines passed into a new Pipeline that is returned.


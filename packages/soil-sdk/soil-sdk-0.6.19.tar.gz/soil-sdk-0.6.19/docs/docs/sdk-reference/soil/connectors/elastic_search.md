---
sidebar_label: elastic_search
title: soil.connectors.elastic_search
---

Package for Elastic Search Connector

## ElasticSearchDBObject Objects

```python
class ElasticSearchDBObject()
```

Represents an Elastic Search Data Base Object.

#### bulk

```python
def bulk(actions: Iterable[Any]) -> Any
```

Performs actions in bulk as defined in the ES bulk API.

#### query

```python
def query(query: Any, random_sorting: bool = False) -> Any
```

Launches a query to ES. Returns the query.

#### insert

```python
def insert(document: Any, id: Optional[str] = None) -> Any
```

Inserts a document to ES.

#### update\_query

```python
def update_query(new_partial_query: Any) -> Any
```

Updates a query without executing it.

#### create\_db\_object

```python
def create_db_object(index: str, force_rewrite: bool = False) -> ElasticSearchDBObject
```

Obtains an Elastic Search DB object. Only works on cloud.


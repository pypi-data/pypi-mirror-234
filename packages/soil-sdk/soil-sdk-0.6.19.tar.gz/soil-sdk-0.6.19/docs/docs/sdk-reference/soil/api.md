---
sidebar_label: api
title: soil.api
---

This package contains calls to the SOIL&#x27;s REST API

#### upload\_data

```python
def upload_data(dtype: str, data: Any, metadata: Any) -> Result
```

Upload data to the cloud as a new dataset.

#### get\_result

```python
def get_result(result_id: str) -> Dict[str, Any]
```

Get the result data

#### get\_result\_data

```python
def get_result_data(result_id: str,
                    query: Optional[Dict[str, str]] = None) -> Dict[str, Any]
```

Get the result data

#### export\_result

```python
def export_result(result_id: str,
                  file_path: str,
                  query: Optional[Dict[str, str]] = None) -> None
```

Export result and saves it to a file

#### upload\_module

```python
def upload_module(module_name: str, code: str, is_package: bool) -> None
```

Uploads a module

#### get\_module

```python
def get_module(full_name: str) -> GetModule
```

Downloads a module

#### set\_alias

```python
def set_alias(alias: str,
              result_id: str,
              roles: Optional[List[str]] = None) -> None
```

Sets an alias for a result. Updates a previous one with the same name.

#### get\_alias

```python
def get_alias(alias: str) -> Dict[str, Any]
```

Gets an alias

#### create\_experiment

```python
def create_experiment(plan: Plan) -> Experiment
```

Runs an experiment in SOIL

#### get\_experiment

```python
def get_experiment(experiment_id: str) -> Experiment
```

Runs an experiment from SOIL

#### get\_experiment\_logs

```python
def get_experiment_logs(experiment_id: str, start_date: str) -> Any
```

Gets logs from a SOIL experiment

#### create\_event

```python
def create_event(key: str, value: Any) -> Any
```

Saves an event in soil

#### create\_alert

```python
def create_alert(alert: Dict) -> Any
```

Creates an alert

#### get\_dictionary

```python
def get_dictionary(name: str, language: str) -> Dict[str, Any]
```

Get the a dictionary

#### create\_dictionary

```python
def create_dictionary(name: str, language: str,
                      content: Dict) -> Dict[str, Any]
```

Create a dictionary or update it


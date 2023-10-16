---
sidebar_label: errors
title: soil.errors
---

Exceptions for SOIL-SDK

## SoilSDKError Objects

```python
class SoilSDKError(Exception)
```

Common soil-sdk exception

## LoginError Objects

```python
class LoginError(SoilSDKError)
```

Exception to raise when unable to login Soil

## ExperimentError Objects

```python
class ExperimentError(SoilSDKError)
```

Exception to raise when an error has occurred while executing a Soil experiment

## ObjectNotFound Objects

```python
class ObjectNotFound(SoilSDKError)
```

Exception to raise when Soil object could not be found

## DictionaryNotFound Objects

```python
class DictionaryNotFound(ObjectNotFound)
```

Exception to raise when Soil Dictionary could not be found

## DataNotFound Objects

```python
class DataNotFound(ObjectNotFound)
```

Exception to raise when Soil data could not be found

## ModuleNotFound Objects

```python
class ModuleNotFound(ObjectNotFound)
```

Exception to raise when Soil module could not be found

## ObjectNotUploaded Objects

```python
class ObjectNotUploaded(SoilSDKError)
```

Exception to raise when Soil object could not be uploaded

## DictionaryNotUploaded Objects

```python
class DictionaryNotUploaded(ObjectNotUploaded)
```

Exception to raise when Soil Dictionary could not be uploaded

## DataNotUploaded Objects

```python
class DataNotUploaded(ObjectNotUploaded)
```

Exception to raise when Soil data could not be uploaded

## ModuleNotUploaded Objects

```python
class ModuleNotUploaded(ObjectNotUploaded)
```

Exception to raise when Soil Module could not be uploaded

## AlertDataNotUploaded Objects

```python
class AlertDataNotUploaded(ObjectNotUploaded)
```

Exception to raise when Soil alert could not be uploaded

## AlertNotUploaded Objects

```python
class AlertNotUploaded(AlertDataNotUploaded)
```

Exception to raise when Soil alert condition could not be uploaded

## EventNotUploaded Objects

```python
class EventNotUploaded(AlertDataNotUploaded)
```

Exception to raise when Soil event alert could not be uploaded

## DataStructureError Objects

```python
class DataStructureError(SoilSDKError)
```

Exception to raise when Soil DataStructure has any error

## DataStructureType Objects

```python
class DataStructureType(DataStructureError)
```

Exception to raise when Soil DataStructure type is not recognised

## DataStructurePipelineNotFound Objects

```python
class DataStructurePipelineNotFound(DataStructureError)
```

Exception to raise when Soil DataStructure Pipeline is not found


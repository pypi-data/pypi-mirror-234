---
sidebar_label: patients
title: data_structures.streams.patients
---

## Patients Objects

```python
class Patients(Stream)
```

#### export

```python
 | export(format='csv', events_column='events', max_subevents_columns=10, **kwargs)
```

Exports a dataset of patients using metadata.schema to extract columns:
    When format=csv it flattens the events_column. Each line
    is an event/episode.
    When format=jsonl each line is a patient.

## Patient Objects

```python
class Patient()
```

Deprecated


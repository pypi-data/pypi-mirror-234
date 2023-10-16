---
sidebar_label: trajectories
title: modules.temporal.trajectories
---

## Trajectories Objects

```python
class Trajectories(Experiment)
```

#### \_\_init\_\_

```python
 | __init__(instances_var='events.instances.name', events_sorting_key='events.end_date', error_tolerance=14, seed=None, max_distance=0.3, max_patients=1000, min_support=50, max_memory=2000)
```

instances_var: Name of the variable to use as items
 e.g events.instances.name

events_sorting_key: Which is the attribute to sort the events with
 e.g. events.end_date

error_tolerance: size for the HLL. larger values -&gt; less error and
 more memory usage

seed: Random seed to reproduce exact results. Defaults to UnixTime

#### copy\_patient

```python
 | copy_patient(patient)
```

Patients are copied to avoid lateral efects with other experiments
when modifying them.

#### sort\_events

```python
 | sort_events(patient, sorting_key)
```

Sort events and remove repeated elements


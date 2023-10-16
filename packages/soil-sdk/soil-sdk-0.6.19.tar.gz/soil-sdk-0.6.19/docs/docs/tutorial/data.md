---
id: data
title: Data
sidebar_label: Data
---

## Referencing data

The simplest way to query your data is with `soil.data`.

```python
import soil

data_ref = soil.data('my_dataset_id')
```


## Uploading data

You can also upload data to the cloud. Non-production accounts may have limitations to the size of the uploaded data.
```python
import soil

data_ref = soil.data([for i in range(100)])
for i in data_ref.data:
  print(i)
```

Soil accepts typical python structures like dicts and lists as long as they are json serializable and numpy arrays and pandas data frames.

```py
import soil
import numpy as np

np_array = np.array([[1,2,3,4], [5,6,7,8]])
ds = soil.data(np_array)
print(ds.data)
```

You can pass metadata as a dictionary (json serializable) to the uploaded data.
```py
data = soil.data(d, metadata={'awww': 'yeah'})
```

By default soil recognises basic data types that can be passed in soil.data. These are:
* [List](/docs/soil-library/data_structures/predefined/list)
* [Dict](/docs/soil-library/data_structures/predefined/dict)
* [ndarray](/docs/soil-library/data_structures/predefined/ndarray)
* [PdDataFrame](/docs/soil-library/data_structures/predefined/pd_data_frame)


## Accessing data

To access the data you can do:
```python
some_result = data_ref.get_data()

# equivalent to get_data()
some_result = data_ref.data

# and get the metadata as well (Dict[str, any])
its_metadata = data_ref.metadata
```

The schema of the metadata can be different for every data structure type.


You can pass parameters if the data structure supports it:
```
patients_slice = patients.get_data(skip=1000, limit=50)
```


## Data Aliases

`soil.alias(name, ref, roles=None)` allows to easily reference the data. This can be useful in a continuous learining environment for example.

* **roles** is an optional list of strings that indicate which users will have permissions to read the result.
At least one role must coincide with one of the roles of the user.

```python
def do_every_hour():
  # Get the old model
  old_model = soil.data('my_model')
  # Retrieve the dataset with an alias we have set before
  dataset = soil.data('my_dataset')
  # Retrieve the data that has arrived in the last hour
  new_data = row_filter({ 'date': { 'gte': 'now-1h'} }, dataset)
  # Train the new model
  new_model = a_continuous_training_algorithm(old_model, new_data)
  # Set the alias and allow some users to read it.
  soil.alias(
      'my_model', new_model,
      roles=['emergency_department', 'admissions_department']
  )

```

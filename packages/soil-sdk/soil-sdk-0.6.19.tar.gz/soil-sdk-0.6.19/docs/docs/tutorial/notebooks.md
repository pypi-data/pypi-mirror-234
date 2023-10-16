---
id: notebooks
title: Notebooks
sidebar_label: Notebooks
---

To run soil pipelines from a Jupiter notebook you can simply import soil and run a cell:

```python
import soil
```

To run modules declared in your project you also have to run:

```python
import os
from os.path import join

package_name = 'your_package_name'

os.environ['MODULES_PATH'] = join(os.getcwd(), package_name, 'modules')
os.environ['DATA_STRUCTURES_PATH'] = join(os.getcwd(), package_name, 'data_structures')
```

where "your_package_name" is the name of your package were the folders modules and data_structures reside.

It is not possible to declare modules or data structures in a Notebook.

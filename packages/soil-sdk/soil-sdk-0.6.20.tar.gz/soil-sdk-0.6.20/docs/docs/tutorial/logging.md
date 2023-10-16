---
id: logging
title: Logging
sidebar_label: Logging
---

## Activate logging
You can activate the logs from SOIL using the [Python logger](https://docs.python.org/3.7/howto/logging.html).

```py
import logging
import soil
from soil.modules.preprocessing.filters import row_filter
from soil.modules.simple_module import simple_mean

# Activate logs up to severity = INFO
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

patients = soil.data('5eafdf99130d73515270d3cf')
women, = row_filter.RowFilter(patients, sex={'eql': '1'})
statistics, = simple_mean(women, aggregation_column='age')
print(statistics.metadata, statistics.data)
```

## Log from your modules

In a module you can import the soil logger from `soil.logger` and use it with the severity levels from Python: debug, info, warning, error, exception and critical.

```py
from soil import modulify
from soil import logger
from soil.data_structures.simple_datastructure import SimpleDataStructure

@modulify(output_types=lambda *inputs, **args: [SimpleDataStructure])
def simple_mean(patients, aggregation_column=None):
    logger.info('This is a log from simple_mean')
    logger.debug('This is another log from simple_mean')
    if aggregation_column is None:
        raise TypeError('Expected aggregation_column parameter')
    total_sum = 0
    count = 0
    for patient in patients:
        if hasattr(patient, aggregation_column):
            val = patient[aggregation_column]
            total_sum += val
            count += 1
    return [SimpleDataStructure(
      {'mean': round(total_sum / count)}, metadata={'awww': 'yeah'}
    )]
```

Running the two examples above would output something like this:
```
2020-07-10 11:35:20,861 - INFO - 2020-07-10T11:35:20.139516+02:00 - Locking experiment: 5f0836577e1433c87129d3b2
2020-07-10 11:35:20,861 - INFO - 2020-07-10T11:35:20.153957+02:00 - Executing experiment: 5f0836577e1433c87129d3b2
2020-07-10 11:35:20,862 - INFO - 2020-07-10T11:35:20.182409+02:00 - Computing: RowFilter
2020-07-10 11:35:20,862 - INFO - 2020-07-10T11:35:20.198914+02:00 - Computing: Modulified
2020-07-10 11:35:20,862 - INFO - 2020-07-10T11:35:20.211914+02:00 - This is a log from simple_mean
2020-07-10 11:35:20,862 - INFO - 2020-07-10T11:35:20.626843+02:00 - Setting experiment 5f0836577e1433c87129d3b2 result soil/modules/simple_module/simple_mean-3068-0 5f0836577e1433c87129d3b1 to done.
{'awww': 'yeah'} {'mean': 49}
```

Rembember logs are not logged because the level we have set is INFO. The second timestamp after the level name is the time in which the server recorded the log whereas the first is the time when the sdk created the log.

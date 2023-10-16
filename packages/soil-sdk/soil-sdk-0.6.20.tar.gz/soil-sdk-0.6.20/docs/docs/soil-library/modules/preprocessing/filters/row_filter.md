---
sidebar_label: row_filter
title: modules.preprocessing.filters.row_filter
---

## RowFilter Objects

```python
class RowFilter(Experiment)
```

Patients row filter

Grammar for the arguments:

    query: {
        &quot;all&quot;: [obj],
        &quot;any&quot;: [obj],
        &quot;not&quot;: obj,
        &quot;all_query&quot;: [query],
        &quot;any_query&quot;: [query],
        &quot;not_query&quot;: query,
    }
    obj: {
        var: {
            &quot;eql&quot;:val,
            &quot;lte&quot;:val,
            &quot;gte&quot;:val,
            &quot;regexp&quot;: val,
            &quot;in&quot;: val,
            &quot;all&quot;: [obj],
            &quot;any&quot;: [obj],
            &quot;not&quot;: obj,
            &quot;all_query&quot;: [query],
            &quot;any_query&quot;: [query],
            &quot;not_query&quot;: query,
            }
        }


---
sidebar_label: trajectory_clusters
title: data_structures.streams.trajectory_clusters
---

## TrajectoryClusters Objects

```python
class TrajectoryClusters(Stream)
```

A stream of hierarchical clusters:
{
    &#x27;elements&#x27;: Sorted list of elements,
    &#x27;distance&#x27;: Jaccard distance,
    &#x27;children&#x27;: [
        ...
        ]
}
For leafs:
{
    &#x27;elements&#x27;: Sorted list of elements,
    &#x27;p-value&#x27;: p-value for temporality
}


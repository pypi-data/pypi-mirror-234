---
sidebar_label: hypergraph
title: data_structures.hypergraph
---

## Hypergraph Objects

```python
class Hypergraph(DataStructure)
```

#### subgraph

```python
 | subgraph(center_node, depth, sort_by='w', merged_nodes=None, max_edges=500, filter=None, min_weight=0)
```

BFS up to nodes in distance=depth. It calculates the PMIs from
a frequent itemsets hypergraph.
TODO accept more than one merged node.

#### PMI\_subraph\_guess

```python
 | PMI_subraph_guess(center_node, merged_nodes=None)
```

Return the list of possible nodes which center_node could merge

#### filter\_edges

```python
 | filter_edges(center_node, max_edges=100, depth=2, sorting_attr='w')
```

Returns a subgraph with a maximum number of edges taking the ones
with more weight first and ensuring that the subgraph is connected


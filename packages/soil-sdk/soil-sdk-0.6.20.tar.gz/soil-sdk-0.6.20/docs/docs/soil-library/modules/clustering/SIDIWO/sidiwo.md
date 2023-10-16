---
sidebar_label: sidiwo
title: modules.clustering.SIDIWO.sidiwo
---

#### MAP\_assign\_clusters\_stm

```python
MAP_assign_clusters_stm(X, M, omega)
```

Assign documents in a corpus X to the most likely topic,
via MAP assignment
@param M: the conditional expectations matrix
@param omega: the mixing weights
@param X: a bag-of-words documents distributed
    as a Single Topic Model, with n rows an d columns;
    at position (i,j) we have the number of times the word j appeared in doc. i,

#### SIDIWO\_lowrank\_single\_topic\_model

```python
SIDIWO_lowrank_single_topic_model(X)
```

Implements SIDIWO for the single topic model using l=2
@param X: a bag-of-words documents distributed
        as a Single Topic Model, with n rows an d columns;
        at position (i,j) we have the number of times the word j appeared in doc. i,

#### asvtd

```python
asvtd(X, k)
```

Learn an approximate pair M, omega
@param X: the dataset
@param k: the number of clusters

#### create\_cluster\_graph\_single\_topic\_model

```python
create_cluster_graph_single_topic_model(X, depth, CL_input, Y=None)
```

Recursive implementation of Algorithm 2, to find a divisive binary tree by
splitting a corpus into two parts.
@param X: a bag-of-words documents distributed 
    as a Single Topic Model, with n rows an d columns;
    at position (i,j) we have the number of times the word j appeared in doc. i,
@param depth: the current depth of the tree; 
    depth =1 means that we are at a leaf
    depth &gt;1 the algorithm perform a splits and calls himself with depth=depth-1
@param CL_input: a list of lists containing the binary tree.
    Each entry is a node, containing: the depth of the node and the binary tree behind him
@param Y: the list of samples contained in the current node, to be splitted at this iteration.


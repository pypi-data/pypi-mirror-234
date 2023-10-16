---
sidebar_label: NBClustering
title: modules.clustering.NBClustering
---

## NBClustering Objects

```python
class NBClustering(Experiment)
```

This module computes Naive Bayes Clusters.
This version only works for Bernoulli variables.

This version also computes

#### \_\_init\_\_

```python
 | __init__(count_variables, num_clusters=15, epsilon=0.01, min_support=0.01, soft=False, lmbda=1.0, supplementary_variables=None, basic_statistics=None, custom_statistics=None)
```

**Attributes**:

- `count_variables` - List[str] A list with the variables to take into
  account.
- `num_clusters` - The number of clusters to compute.
- `min_support` - Variable values with lower support will be ignored.

#### do

```python
 | do(data)
```

Performs clustering of the dataset.

**Attributes**:

- `data` - Should be a Stream.

#### asvtd

```python
 | asvtd(X, k)
```

Learn an approximate pair M, omega
@param X: the dataset
@param k: the number of clusters

#### EM

```python
 | EM(X, M, omega, Eps=0.001, verbose=False)
```

Implementation of EM to learn a NBM with binary variables
@param X: the dataset
@param M: the centers of the mixture
@param omega: the mixing weights
@param Eps: the stopping criterion
@param verbose: whether to show or not the error


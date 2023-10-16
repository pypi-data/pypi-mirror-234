---
sidebar_label: NBClustering_categorical
title: modules.clustering.NBClustering_categorical
---

## NBClustering\_categorical Objects

```python
class NBClustering_categorical(Experiment)
```

#### do

```python
 | do(data)
```

Performs clustering of the dataset
@param data: the dataset

#### asvtd

```python
 | asvtd(X, k)
```

Learn an approximate pair M, omega
@param X: the dataset
@param k: the number of clusters

#### EM

```python
 | EM(X, M, omega, bernoulli_index, categorical_index, Eps=0.001, verbose=False)
```

Implementation of EM to learn a NBM with binary variables
@param X: the dataset
@param M: the centers of the mixture
@param omega: the mixing weights
@param Eps: the stopping criterion
@param verbose: whether to show or not the error

#### get\_relevance

```python
 | get_relevance(M, X, omega, CL)
```

Compute the relevance of each feature for each cluster


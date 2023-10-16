---
sidebar_label: Predictor
title: modules.higher_order.Predictor
---

## Predictor Objects

```python
class Predictor(Experiment)
```

A class providing methods for the computation of (hard or soft) cluster \
    assignments for a stream of patients from a precomputed model.
Note that we don&#x27;t require identical set of variables for the precomputed \
    model and the predicted assignments, \
    we use the intersection of the two sets for prediction.
Currently, two modes for cluster prediction are provided: \
    batch (called do as this is the default) and iterative \
    (called do_iterative).
The iterative predictor needs preprocessing in order to achieve \
    scalable prediction, i.e., one that depends only on the number of
    nonzero coordinates in the input instance.

#### do

```python
 | do(model, data)
```

Predicts (hard and soft) cluster assignments using a batch or \
    iterative (one example at time ) mode
@param cluster_model: a precomputed model containing the M and  \
    omega matrices for centers and prior cluster weight \
        distributions
@param data: a stream of patients

#### do\_iterative

```python
 | do_iterative(model, data)
```

Predicts (hard and soft) cluster assignments in an iterative mode.
It uses preprocessing for fast computation, more experments needed \
    to establish
if the approach is more officient than the batch mode

#### do\_batch

```python
 | do_batch(model, data)
```

Predicts (hard and soft) cluster assignments
@param cluster_model: a precomputed model containing the M and \
    omega matrices for centers and prior cluster weight \
    distributions
@param data: a stream of patients


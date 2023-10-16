---
id: data-structures
title: Data Structures
sidebar_label: Data Structures
---

Data Structures contain and pass the information between modules in a SOIL pipeline. They are defined in the `data_structures` package under the top level. A data structure is defined in a class that inherits from `soil.data_structures.data_structure.DataStructure` or from a class that inherits from it.

It contains three attributes **data**, **metadata** and **storage**. The schema for the data can be different for each data structure.

Additionally a data structure must implement three methods:
* **serialize**: To transform and store the data in disk or a in DB.
* **deserialize**: A class method to transform serialized data to actual data.
* **get_data**: Returns a jsonable object to send the data to the client.

The signature of the init method is: `__init__(data, metadata=None, storage=None)`

Optionally you can implement the **export(format='csv')** method that when called will generate a zip file with the data contained in the data structure.

The following example serializes and deserializes json.

```py
import json
from soil.data_structures.data_structure import DataStructure
from soil.storage.object_storage import ObjectStorage


class ObjectDS(DataStructure):
    '''
    Basic DataStructure to Store json serializable objects
    '''
    def serialize(self):
        '''
        Serializes the data and stores them using ObjectStorage.
        The data must be json serializable.
        '''
        obj_storage = ObjectStorage()
        obj_storage.put_object(json.dumps(self.data).encode('utf-8'))
        return obj_storage

    @classmethod
    def deserialize(cls, obj_storage, metadata):
        '''
        Deserializes the data obtaining them from ObjectStorage.
        '''
        raw_data = obj_storage.get_object()
        data = json.loads(raw_data.decode('utf-8'))
        return cls(data, metadata, storage=obj_storage)

    def get_data(self):
        return self.data

```

## Storage Classes
The connectors between data structures and the actual storage APIs are Storage Classes. Storage Classes implement an API layer to isolate soil applications and abstract configuration parameters that may vary between deployments.

* The serialize method of a DataStructure will return an storage class and will be called when the data is going to be stored.
* The deserialize method of a DataStructure gets a storage class and the metadata and returns the initialized DataStructure instance.

It is not mandatory to initialize the data inside deserialize. For example when we have data in a database it is possible to initialize the data structure with None and call later the `self.storage.do_query(my_query)`.

**Storage Objects may be shared between data structures.** For example we can implement a module that updates a query to be run in another module. The storage object will be passed between data structures until some module executes the query.

Some examples of storage classes are:
* [Object Storage](/docs/sdk-reference/soil/storage/object_storage)
* [Elasticsearch](/docs/sdk-reference/soil/storage/elasticsearch)

## Differences between Data Structures and Storage Classes
It may be confusing to see which are the differences between Data Structures and Storage Classes. Storage Classes are the connector with the storage API and are defined by soil developers. Data Structures are defined by Soil users and called by the modules.

For example we can define a HyperLogLog data structure that implements a  `count()` method. A module that uses the HyperLogLog doesn't care if the data is in elasticsearch, redis or a custom pickled object stored in a file. It is responsability of the Data Structure to decide which storage back-end should be used. Mind that not all storage back-ends might be available in a deployment hence having flexible data structures is a plus.

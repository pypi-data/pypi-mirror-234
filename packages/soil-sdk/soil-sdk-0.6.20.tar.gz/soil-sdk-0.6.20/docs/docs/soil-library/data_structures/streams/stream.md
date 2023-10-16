---
sidebar_label: stream
title: data_structures.streams.stream
---

## Stream Objects

```python
class Stream(DataStructure)
```

Base class for Streams.

Streams are iterable objects that can only be consumed once.

Before consuming a stream self.data will be None.

Implement the method db_unserializer(self, data_element) to process each
row.


# Construction

Graph construction start with a [Graph](../components/graph.md) object.

```python
from asyncgraphs import Graph

g = Graph()
```

This graph acts as the handle for your entire ETL operation.


## Adding a source

An ETL graph needs nodes and the first nodes that are needed are [source](../components/source.md) nodes.
More information on the operations that can be used as a source can be found on the [source](../components/source.md) page.

Adding sources to the ETL flow is done by linking it to the [Graph](../components/graph.md) object.
This can be done in a couple of ways. The following example shows them.

```python
from asyncgraphs import Graph

g = Graph()
g.link_to([1, 2, 3])
g >> [4, 5, 6]
g | [7, 8, 9]
```

In the example above there are 3 different source nodes in the graph, each emitting values from a fixed list.

## Adding a transform (or sink)

All nodes that are not a source are considered a [transform](../components/transform.md).
Transform nodes take in data and optionally emit data.

The same methods and operators can be used to attach transformations to a source.

```python
from asyncgraphs import Graph

g = Graph()
source_ref = g | [1, 2, 3]
source_ref | (lambda x: x + 1) | print
```
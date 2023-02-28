# Transform

Transformations (and data sinks) are always of type Callable.
As an argument they take 1 output value of the previous step in the graph.

The functions can be async (which is preferred if the task can be done asynchronously).
There are 2 ways of implementing the transformation:

- 1 doc in = 1 doc out: return the output document
- 1 doc in = 0 or more docs out: use the yield keyword to yield the documents that should be outputted by the transformation
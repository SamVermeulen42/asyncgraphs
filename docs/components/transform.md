# Transform

Transformations (and data sinks) are always of type Callable.
As an argument they take 1 output value of the previous step in the graph.

The functions can be async (which is preferred if the task can be done asynchronously).
There are 2 ways of implementing the transformation:

- 1 doc in = 1 doc out: return the output document
- 1 doc in = 0 or more docs out: use the yield keyword to yield the documents that should be outputted by the transformation

Example of a 1 to 1 transform:

```python
from asyncgraphs import Graph

g = Graph()

def add_one(input: int) -> int:
    return input + 1


g | [1, 2, 3] | add_one | print
```

For a 1 to any transform, use yields:

```python
from asyncgraphs import Graph

g = Graph()

def repeat_hello(input: int) -> str:
    for _ in range(input):
        yield "hello"


g | [0, 1, 2, 3] | repeat_hello | print
```
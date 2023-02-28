# Source

A source in AsyncGraphs is a Node that simply generates data.

Sources are attached directly to [Graph](graph.md) objects and take no input.

Any python Iterable or AsyncIterable can be used.

```python
from asyncgraphs import Graph

g = Graph()

g | [1, 2, 3]
```

```python
from asyncgraphs import Graph
from random import random

g = Graph()

g | (random() for _ in range(10))
```

```python
from asyncgraphs import Graph

g = Graph()

def my_source():
    for i in range(1000):
        yield {"number": i}

g | my_source()
```

```python
import asyncio
from asyncgraphs import Graph
import aiohttp

g = Graph()


async def my_source(session):
    while True:
        async with session.get('http://localhost:8000') as response:
            response.raise_for_status()
            yield await response.json()
        await asyncio.sleep(10)

async def main():
    async with aiohttp.ClientSession() as session:
        g | my_source(session)
```

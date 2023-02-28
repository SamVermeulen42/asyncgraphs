# AsyncGraphs

<img src="https://github.com/SamVermeulen42/asyncgraphs/workflows/Tests/badge.svg?event=push&branch=main" alt="Test"/>
<img src="https://codecov.io/gh/SamVermeulen42/asyncgraphs/branch/main/graph/badge.svg?token=17MW83L23M" alt="Coverage"/>
<img src="https://img.shields.io/pypi/v/asyncgraphs" alt="Package version"/>
<img src="https://img.shields.io/pypi/pyversions/asyncgraphs.svg" alt="Supported Python versions">

AsyncGraphs is a tiny ETL framework that leverages asyncio to make the execution more efficient.


## Installation

```commandline
pip install asyncgraphs
```

## Basic usage

```python
import asyncio
import datetime
from random import random

import pytz
from asyncgraphs import Graph, run


async def my_extract():
    while True:
        await asyncio.sleep(1)
        yield {"timestamp": datetime.datetime.now(tz=pytz.UTC), "value": random()}


def my_transform(in_doc):
    if in_doc["value"] < 0.5:
        in_doc["value"] = None
    return in_doc


class MyForwardFill:
    def __init__(self):
        self.last_value = None

    def __call__(self, in_doc):
        if in_doc["value"] is None:
            in_doc["value"] = self.last_value
        else:
            self.last_value = in_doc["value"]
        return in_doc


async def main():
    g = Graph()
    g | my_extract() | my_transform | MyForwardFill() | print
    await run(g)

if __name__ == '__main__':
    asyncio.run(main())
```

The example above shows some dummy extract/transform/load steps.
In the example most are synchronous, but regular applications should use async libraries as often as possible.


## Features

### Typed

This library is typed. Checking the types of chained operations is also supported.

In the following example, the source outputs strings. 
Adding a transformer that expects an integer is thus not supported

This is indicated when using a type checker.

```python
# tests/test_examples/typed.py

import asyncio
import random
import string
from typing import AsyncGenerator

from asyncgraphs import Graph, run

graph = Graph()


async def random_strings(
    value_count: int, character_count: int
) -> AsyncGenerator[str, None]:
    for i in range(value_count):
        yield "".join(
            random.choice(string.ascii_lowercase) for _ in range(character_count)
        )
        await asyncio.sleep(0)


def add_one(value: int) -> int:
    return value + 1


def prefix_hello(value: str) -> str:
    return f"Hello {value}"


async def main() -> None:
    g = Graph()
    g | random_strings(20, 5) \
      | add_one \
      | print
    await run(g)

    g = Graph()
    g | random_strings(20, 5) \
      | prefix_hello \
      | print
    await run(g)


if __name__ == "__main__":
    asyncio.run(main())
```

```commandline
$ mypy tests/test_examples/typed.py
tests/test_examples/typed.py:32: error: Unsupported operand types for | ("Source[str]" and "Callable[[int], int]")  [operator]
Found 1 error in 1 file (checked 1 source file)
```


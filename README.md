# AsyncGraphs

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

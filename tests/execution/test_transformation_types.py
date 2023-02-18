import pytest

from asyncgraphs.construction import Graph
from asyncgraphs.execution import run


@pytest.mark.asyncio
async def test_fn():
    def add_one(x):
        return x + 1

    out = []
    g = Graph()
    g | [1, 2, 3] \
      | (lambda x: x * 4) \
      | add_one \
      | out.append

    await run(g)
    assert out == [5, 9, 13]


@pytest.mark.asyncio
async def test_async_fn():
    async def add_one(x):
        return x + 1

    out = []
    g = Graph()
    g | [1, 2, 3] \
      | add_one \
      | out.append

    await run(g)
    assert out == [2, 3, 4]


@pytest.mark.asyncio
async def test_iterable():
    def powers(x):
        return [x, x ** 2, x ** 3]

    out = []
    g = Graph()
    g | [1, 2, 3] \
      | powers \
      | out.append

    await run(g)
    assert out == [[1, 1, 1], [2, 4, 8], [3, 9, 27]]


@pytest.mark.asyncio
async def test_generator():
    def powers(x):
        yield x
        yield x ** 2
        yield x ** 3

    out = []
    g = Graph()
    g | [1, 2, 3] \
      | powers \
      | out.append

    await run(g)
    assert out == [1, 1, 1, 2, 4, 8, 3, 9, 27]


@pytest.mark.asyncio
async def test_async_generator():
    async def powers(x):
        yield x
        yield x ** 2
        yield x ** 3

    out = []
    g = Graph()
    g | [1, 2, 3] \
      | powers \
      | out.append

    await run(g)
    assert out == [1, 1, 1, 2, 4, 8, 3, 9, 27]

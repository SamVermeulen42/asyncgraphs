import pytest

from asyncgraphs.construction import Graph
from asyncgraphs.execution import run


@pytest.mark.asyncio
async def test_range():
    out = []
    g = Graph()
    g | range(100) | out.append

    await run(g)
    assert out == list(range(100))


@pytest.mark.asyncio
async def test_list():
    out = []
    g = Graph()
    g | [1, 2, 3] | out.append

    await run(g)
    assert out == [1, 2, 3]


@pytest.mark.asyncio
async def test_generator():
    def gen():
        for i in range(100):
            yield i

    out = []
    g = Graph()
    g | gen() | out.append

    await run(g)
    assert out == list(range(100))


@pytest.mark.asyncio
async def test_async_generator():
    async def gen():
        for i in range(100):
            yield i

    out = []
    g = Graph()
    g | gen() | out.append

    await run(g)
    assert out == list(range(100))

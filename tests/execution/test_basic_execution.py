import asyncio

import pytest as pytest

from asyncgraphs.construction import Graph, Transform
from asyncgraphs.execution import run, run_transform, CompletedSignal


@pytest.mark.asyncio
async def test_run_node():
    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue()
    for i in range(10):
        await in_queue.put(i)
    await in_queue.put(CompletedSignal)

    await run_transform(in_queue, Transform(None, lambda x: x * 2), {out_queue})

    results = []
    while (out := await out_queue.get()) != CompletedSignal:
        results.append(out)
    assert [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] == results


@pytest.mark.asyncio
async def test_run_graph():
    out = []
    g = Graph()
    g | range(100) | Transform("add 1", lambda x: x + 1) | (
        lambda x: x * 2
    ) | out.append

    await run(g)
    assert out == list(range(2, 201, 2))

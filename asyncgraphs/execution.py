import asyncio
import types
from asyncio import Queue
from collections.abc import AsyncIterable
from typing import Any, List, Set, Tuple

import sentinel

from asyncgraphs.construction import Graph, Source, Transform, TransformOperation

CompletedSignal = sentinel.create("CompletedSignal")


async def run(graph: Graph) -> None:
    tasks = []
    for s_node in graph.entry_nodes:
        s_out_queues = set()
        for t_node in s_node.next_nodes:
            t_in_queue: Queue[Any] = Queue()
            branch_run_info = _get_transform_run_info(t_in_queue, t_node)
            s_out_queues.add(t_in_queue)
            tasks += [run_transform(i, n, o) for i, n, o in branch_run_info]
        tasks.append(run_source(s_node, s_out_queues))
    await asyncio.gather(*tasks)


def _get_transform_run_info(
    in_queue: Queue[Any], node: Transform[Any, Any]
) -> List[Tuple[Queue[Any], Transform[Any, Any], Set[Queue[Any]]]]:
    to_return = []
    node_out_queues = set()
    for n in node.next_nodes:
        q: Queue[Any] = Queue()
        to_return += _get_transform_run_info(q, n)
        node_out_queues.add(q)
    return to_return + [(in_queue, node, node_out_queues)]


async def run_source(node: Source[Any], out_queues: Set[Queue[Any]]) -> None:
    if isinstance(node.operation, AsyncIterable):
        async for data_out in node.operation:
            await asyncio.gather(*[q.put(data_out) for q in out_queues])
    else:
        for data_out in node.operation:
            await asyncio.gather(*[q.put(data_out) for q in out_queues])
    await asyncio.gather(*[q.put(CompletedSignal) for q in out_queues])


async def run_transform(
    in_queue: Queue[Any], node: Transform[Any, Any], out_queues: Set[Queue[Any]]
) -> None:
    data_in = await in_queue.get()
    while data_in != CompletedSignal:
        await apply_operation(data_in, node.operation, out_queues)
        in_queue.task_done()
        data_in = await in_queue.get()
    await asyncio.gather(*[q.put(CompletedSignal) for q in out_queues])


async def apply_operation(
    data_in: Any, operation: TransformOperation[Any, Any], out_queues: Set[Queue[Any]]
) -> None:
    r = operation(data_in)

    # multiple values
    if isinstance(r, types.AsyncGeneratorType):
        async for out in r:
            await asyncio.gather(*[q.put(out) for q in out_queues])
        return
    elif isinstance(r, types.GeneratorType):
        for out in r:
            await asyncio.gather(*[q.put(out) for q in out_queues])
        return

    # single value
    if asyncio.iscoroutine(r):
        r = await r
    else:
        await asyncio.sleep(0)  # pass prio
    await asyncio.gather(*[q.put(r) for q in out_queues])

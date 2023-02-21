import asyncio
import types
from asyncio import Queue
from enum import StrEnum, auto
from typing import Set, List, Tuple, Any

from asyncgraphs.construction import Graph, Transform, Source, TransformOperation
from asyncgraphs.exceptions import NoEntrypointException


class Signals(StrEnum):
    completed = auto()


async def run(graph: Graph) -> None:
    node_run_info = []
    entry_out_queues = set()
    if graph.entry_node is None:
        raise NoEntrypointException()
    for n in graph.entry_node.next_nodes:
        q: Queue[Any] = Queue()
        node_run_info += get_children_run_info(q, n)
        entry_out_queues.add(q)
    await asyncio.gather(
        run_source(graph.entry_node, entry_out_queues),
        *[run_transform(i, n, o) for i, n, o in node_run_info],
    )


def get_children_run_info(
    in_queue, node
) -> List[Tuple[Set[Queue], Transform, Set[Queue]]]:
    to_return = []
    node_out_queues = set()
    for n in node.next_nodes:
        q = Queue()
        to_return += get_children_run_info(q, n)
        node_out_queues.add(q)
    return to_return + [(in_queue, node, node_out_queues)]


async def run_source(node: Source, out_queues: Set[Queue]) -> None:
    if isinstance(node.operation, types.AsyncGeneratorType):
        async for data_out in node.operation:
            await asyncio.gather(*[q.put(data_out) for q in out_queues])
    else:
        for data_out in node.operation:
            await asyncio.gather(*[q.put(data_out) for q in out_queues])
    await asyncio.gather(*[q.put(Signals.completed) for q in out_queues])


async def run_transform(
    in_queue: Queue, node: Transform, out_queues: Set[Queue]
) -> None:
    data_in = await in_queue.get()
    while data_in != Signals.completed:
        await apply_operation(data_in, node.operation, out_queues)
        in_queue.task_done()
        data_in = await in_queue.get()
    await asyncio.gather(*[q.put(Signals.completed) for q in out_queues])


async def apply_operation(
    data_in: Any, operation: TransformOperation, out_queues: Set[Queue]
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

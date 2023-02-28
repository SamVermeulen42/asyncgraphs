from __future__ import annotations

from typing import (
    Any,
    AsyncGenerator,
    AsyncIterable,
    Awaitable,
    Callable,
    Generator,
    Generic,
    Iterable,
    Optional,
    Set,
    TypeAlias,
    TypeVar,
)

IN_T = TypeVar("IN_T")
OUT_T = TypeVar("OUT_T")
TransformOperation: TypeAlias = Callable[
    [IN_T],
    Generator[OUT_T, Any, Any] | AsyncGenerator[OUT_T, Any] | Awaitable[OUT_T] | OUT_T,
]


class _NodeBase(Generic[OUT_T]):
    def __init__(self, name: Optional[str]) -> None:
        self.name = name or f"Node<{id(self)}>"
        self.next_nodes: Set[Transform[OUT_T, Any]] = set()

    def link_to(
        self, other: Transform[OUT_T, Any] | TransformOperation[OUT_T, Any]
    ) -> Transform[OUT_T, Any]:
        if callable(other):
            other_node = Transform(None, other)
        else:
            other_node = other
        self.next_nodes.add(other_node)
        return other_node

    def __or__(
        self, other: Transform[OUT_T, Any] | TransformOperation[OUT_T, Any]
    ) -> Transform[OUT_T, Any]:
        return self.link_to(other)

    def __rshift__(
        self, other: Transform[OUT_T, Any] | TransformOperation[OUT_T, Any]
    ) -> Transform[OUT_T, Any]:
        return self.link_to(other)


class Source(_NodeBase[OUT_T]):
    def __init__(
        self, name: Optional[str], operation: Iterable[OUT_T] | AsyncIterable[OUT_T]
    ) -> None:
        super().__init__(name)
        self.operation = operation


class Transform(_NodeBase[OUT_T], Generic[IN_T, OUT_T]):
    def __init__(
        self, name: Optional[str], operation: TransformOperation[IN_T, OUT_T]
    ) -> None:
        super().__init__(name)
        self.operation = operation


class Graph:
    def __init__(self) -> None:
        self.entry_nodes: Set[Source[Any]] = set()

    def link_to(
        self, other: Source[OUT_T] | Iterable[OUT_T] | AsyncIterable[OUT_T]
    ) -> Source[OUT_T]:
        if isinstance(other, Source):
            other_node = other
        else:
            other_node = Source(None, other)
        self.entry_nodes.add(other_node)
        return other_node

    def __or__(
        self, other: Source[OUT_T] | Iterable[OUT_T] | AsyncIterable[OUT_T]
    ) -> Source[OUT_T]:
        return self.link_to(other)

    def __rshift__(
        self, other: Source[OUT_T] | Iterable[OUT_T] | AsyncIterable[OUT_T]
    ) -> Source[OUT_T]:
        return self.link_to(other)

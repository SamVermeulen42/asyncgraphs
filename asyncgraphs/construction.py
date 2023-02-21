import abc
from typing import (
    Optional,
    Callable,
    Iterable,
    AsyncIterable,
    Any,
    Set,
    TypeVar, TypeAlias,
)

SourceOperation: TypeAlias = Iterable[Any] | AsyncIterable[Any]
TransformOperation: TypeAlias = Callable[..., Any]
TTransform = TypeVar("TTransform", bound="Transform")


class _NodeBase(abc.ABC):
    def __init__(self, name: Optional[str]) -> None:
        self.name = name or f"Node<{id(self)}>"
        self.next_nodes: Set[Transform] = set()

    def __or__(self, other: TTransform | TransformOperation) -> "Transform":
        if callable(other):
            other_node = Transform(None, other)
        else:
            other_node = other
        self.next_nodes.add(other_node)
        return other_node


class Source(_NodeBase):
    def __init__(self, name: Optional[str], operation: SourceOperation) -> None:
        super().__init__(name)
        self.operation = operation


class Transform(_NodeBase):
    def __init__(self, name: Optional[str], operation: TransformOperation) -> None:
        super().__init__(name)
        self.operation = operation


class Graph:
    def __init__(self) -> None:
        self.entry_node: Optional[Source] = None

    def __or__(self, other: Source | SourceOperation) -> Source:
        if self.entry_node is not None:
            raise ValueError("Graph entrypoint is already set.")
        if isinstance(other, Source):
            self.entry_node = other
        else:
            self.entry_node = Source(None, other)
        return self.entry_node

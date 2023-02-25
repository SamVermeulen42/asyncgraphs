from typing import (
    Any,
    AsyncIterable,
    Callable,
    Iterable,
    Optional,
    Set,
    TypeAlias,
    TypeVar,
)

SourceOperation: TypeAlias = Iterable[Any] | AsyncIterable[Any]
TransformOperation: TypeAlias = Callable[..., Any]
TTransform = TypeVar("TTransform", bound="Transform")


class _NodeBase:
    def __init__(self, name: Optional[str]) -> None:
        self.name = name or f"Node<{id(self)}>"
        self.next_nodes: Set[Transform] = set()

    def link_to(self, other: TTransform | TransformOperation) -> "Transform":
        if callable(other):
            other_node = Transform(None, other)
        else:
            other_node = other
        self.next_nodes.add(other_node)
        return other_node

    def __or__(self, other: TTransform | TransformOperation) -> "Transform":
        return self.link_to(other)

    def __rshift__(self, other: TTransform | TransformOperation) -> "Transform":
        return self.link_to(other)


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
        self.entry_nodes: Set[Source] = set()

    def link_to(self, other: Source | SourceOperation) -> Source:
        if isinstance(other, Source):
            other_node = other
        else:
            other_node = Source(None, other)
        self.entry_nodes.add(other_node)
        return other_node

    def __or__(self, other: Source | SourceOperation) -> Source:
        return self.link_to(other)

    def __rshift__(self, other: Source | SourceOperation) -> Source:
        return self.link_to(other)

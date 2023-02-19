from typing import Optional, Self


class Node:
    def __init__(self, name: Optional[str], operation) -> None:
        self.name = name or f"Node<{id(self)}>"
        self.operation = operation
        self.next_nodes = set()

    def __or__(self, other) -> Self:
        if isinstance(other, Node):
            other_node = other
        else:
            other_node = Node(None, other)
        self.next_nodes.add(other_node)
        return other_node


class Graph:
    def __init__(self) -> None:
        self.entry_node: Optional[Node] = None

    def __or__(self, other) -> Node:
        if self.entry_node is not None:
            raise ValueError("Graph entrypoint is already set.")
        if isinstance(other, Node):
            self.entry_node = other
        else:
            self.entry_node = Node(None, other)
        return self.entry_node

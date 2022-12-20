from dataclasses import dataclass
from state import State
from typing import Optional
from item import Item
from parser_types import Symbol


@dataclass(eq=True)
class StateIndexEdge:
    symbol: Symbol
    state_index: int


@dataclass
class CanonicalCollection:
    states: list[State]
    edges: dict[int, list[StateIndexEdge]]

    def __str__(self) -> str:
        state_str = "\n\n".join(
            [f"[State {i}]\n{state}" for i, state in enumerate(self.states)]
        )

        edge_str = ""
        for start_index, edges in self.edges.items():
            for edge in edges:
                edge_str = (
                    f"{edge_str}\n{start_index} -- {edge.symbol} -> {edge.state_index}"
                )

        return f"{state_str}\n{edge_str}"

    @property
    def starting_item(self) -> Item:
        return self.states[0].items[0]

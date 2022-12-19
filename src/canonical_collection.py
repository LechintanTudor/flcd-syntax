from dataclasses import dataclass
from state import State
from parser_types import Symbol


@dataclass
class StateIndexEdge:
    symbol: Symbol
    state_index: int


@dataclass
class CanonicalCollection:
    states: list[State]
    edges: dict[int, StateIndexEdge]

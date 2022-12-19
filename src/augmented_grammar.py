from dataclasses import dataclass
from functools import reduce
import json
from parser_types import Nonterminal, Terminal, Symbol
from item import Item
from production import Production


@dataclass
class AugmentedGrammar:
    nonterminals: set[Nonterminal]
    terminals: set[Terminal]
    productions: list[Production]
    items: list[Item]
    start_nonterminal: Nonterminal

    def __str__(self) -> str:
        production_str = reduce(lambda p1, p2: f"{p1}\n{p2}", self.productions)
        item_str = reduce(lambda i1, i2: f"{i1}\n{i2}", self.items)

        return (
            f"Nonterminals: {self.nonterminals}\n\n"
            f"Terminals: {self.terminals}\n\n"
            f"Productions:\n{production_str}\n\n"
            f"Items:\n{item_str}\n\n"
            f"Start nonterminal: {self.start_nonterminal}"
        )

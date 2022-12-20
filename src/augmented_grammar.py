from dataclasses import dataclass
import json
from parser_types import Nonterminal, Terminal, Symbol
from item import Item
from production import Production
from typing import Iterator


@dataclass
class AugmentedGrammar:
    nonterminals: set[Nonterminal]
    terminals: set[Terminal]
    productions: list[Production]
    items: list[Item]
    start_nonterminal: Nonterminal

    def __str__(self) -> str:
        production_str = "\n".join([str(p) for p in self.productions])
        item_str = "\n".join([str(i) for i in self.items])

        return (
            f"Nonterminals: {self.nonterminals}\n\n"
            f"Terminals: {self.terminals}\n\n"
            f"Productions:\n{production_str}\n\n"
            f"Items:\n{item_str}\n\n"
            f"Start nonterminal: {self.start_nonterminal}"
        )

    def productions_for(self, nonterminal: Nonterminal) -> Iterator[Production]:
        for production in self.productions:
            if production.lhp == nonterminal:
                yield production

    def items_for(self, nonterminal: Nonterminal) -> Iterator[Item]:
        for item in self.items:
            if item.lhp == nonterminal:
                yield item

    def symbols(self) -> Iterator[Symbol]:
        for terminal in self.terminals:
            yield terminal

        for nonterminal in self.nonterminals:
            yield nonterminal

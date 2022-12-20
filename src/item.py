from dataclasses import dataclass
from parser_types import Nonterminal, ItemSymbol


@dataclass(eq=True)
class Item:
    lhp: Nonterminal
    rhp: list[ItemSymbol]

    def __str__(self) -> str:
        return f"{self.lhp} -> {self.rhp}"

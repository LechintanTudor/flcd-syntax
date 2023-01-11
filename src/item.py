from dataclasses import dataclass
from parser_types import Nonterminal, ItemSymbol


@dataclass(eq=True)
class Item:
    """Mapping from a nonterminal to a list of symbols in the context of an augmented grammar."""

    lhp: Nonterminal
    rhp: list[ItemSymbol]

    def __str__(self) -> str:
        return f"{self.lhp} -> {self.rhp}"

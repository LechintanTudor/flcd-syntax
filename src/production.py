from dataclasses import dataclass
from parser_types import Nonterminal, Symbol


@dataclass
class Production:
    lhp: Nonterminal
    rhp: list[Symbol]

    def __str__(self) -> str:
        return f"{self.lhp} -> {self.rhp}"

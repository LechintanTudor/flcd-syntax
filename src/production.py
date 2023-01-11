from dataclasses import dataclass
from parser_types import Nonterminal, Symbol


@dataclass(eq=True)
class Production:
    """Mapping from a nonterminal to a list of symbols in the context of a regular grammar."""

    lhp: Nonterminal
    rhp: list[Symbol]

    def __str__(self) -> str:
        return f"{self.lhp} -> {self.rhp}"

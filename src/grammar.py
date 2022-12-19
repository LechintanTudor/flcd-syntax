from augmented_grammar import AugmentedGrammar
from dataclasses import dataclass
from dot import Dot
from item import Item
import json
from parser_types import Nonterminal, Terminal, Symbol
from production import Production


@dataclass
class Grammar:
    nonterminals: set[Nonterminal]
    terminals: set[Terminal]
    productions: list[Production]
    start_nonterminal: Nonterminal

    def augment(self) -> AugmentedGrammar:
        aug_start_nonterminal = f"{self.start_nonterminal}'"
        aug_nonterminals = self.nonterminals.union({aug_start_nonterminal})

        aug_items = []
        aug_items.append(Item(aug_start_nonterminal, [Dot, self.start_nonterminal]))
        for production in self.productions:
            aug_items.append(Item(production.lhp, [Dot] + production.rhp))

        return AugmentedGrammar(
            aug_nonterminals,
            self.terminals,
            self.productions,
            aug_items,
            aug_start_nonterminal,
        )

    def __str__(self) -> str:
        production_str = "\n".join(self.productions)

        return (
            f"Nonterminals: {self.nonterminals}\n\n"
            f"Terminals: {self.terminals}\n\n"
            f"Productions:\n{production_str}\n\n"
            f"Start nonterminal: {self.start_nonterminal}"
        )

    @staticmethod
    def load_from_json(path: str) -> "Grammar":
        with open(path, "rt") as file:
            json_data = json.load(file)
            nonterminals = set(json_data["nonterminals"].keys())
            terminals = set(json_data["terminals"])

            productions = []
            for lhp, rhp_list in json_data["nonterminals"].items():
                for rhp in rhp_list:
                    productions.append(Production(lhp, rhp))
            productions.sort(key=lambda production: production.lhp)

            start_nonterminal = json_data["start_nonterminal"]

            if start_nonterminal not in nonterminals:
                raise ValueError("Start nonterminal not found in nonterminals")

            return Grammar(nonterminals, terminals, productions, start_nonterminal)

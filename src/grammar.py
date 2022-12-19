from dataclasses import dataclass
from functools import reduce
import json
from parser_types import Nonterminal, Terminal, Symbol
from production import Production


@dataclass
class Grammar:
    nonterminals: set[Nonterminal]
    terminals: set[Terminal]
    productions: list[Production]
    start_nonterminal: Nonterminal

    def __str__(self) -> str:
        production_str = reduce(lambda p1, p2: f"{p1}\n{p2}", self.productions)

        return (
            f"Nonterminals: {self.nonterminals}\n"
            f"Terminals: {self.terminals}\n"
            f"Productions: {production_str}\n"
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

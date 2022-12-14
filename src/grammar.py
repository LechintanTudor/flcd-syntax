from copy import deepcopy
import json


class Dot:
    def __str__(self):
        return "<DOT/>"

    def __repr__(self):
        return "<DOT/>"

    def __eq__(self, other):
        return isinstance(other, Dot)


class Grammar:
    def __init__(self):
        self._non_terminals = []
        self._terminals = []
        self._productions = {}

    def load_from_file(self, filename):
        with open(filename, "rt") as f:
            json_data = json.load(f)
            self._terminals = json_data["terminals"]
            self._non_terminals = list(json_data["nonterminals"].keys())

            for non_terminal in self._non_terminals:
                if non_terminal not in self._productions:
                    self._productions[non_terminal] = []

                self._productions[non_terminal] = json_data["nonterminals"][
                    non_terminal
                ]

    def get_terminals(self):
        return self._terminals

    def get_non_terminals(self):
        return self._non_terminals

    def get_productions(self, non_terminal=None):
        if non_terminal:
            return self._productions[non_terminal]

        return self._productions


class AugmentedGrammar(Grammar):
    def __init__(self, grammar: Grammar, start_non_terminal: str):
        super().__init__()

        assert start_non_terminal in grammar.get_non_terminals()
        root_non_terminal = f"{start_non_terminal}'"

        self._terminals = grammar.get_terminals()
        self._non_terminals = grammar.get_non_terminals() + [root_non_terminal]
        self._productions = {root_non_terminal: [[Dot(), start_non_terminal]]}
        self._root_non_terminal = root_non_terminal

        for non_terminal in self._non_terminals:
            if non_terminal in grammar.get_productions():
                self._productions[non_terminal] = []

                for prod in grammar.get_productions()[non_terminal]:
                    self._productions[non_terminal].append([Dot()] + prod)

    @property
    def productions(self):
        return self._productions

    @property
    def non_terminals(self):
        return self._non_terminals

    @property
    def root_non_terminal(self):
        return self._root_non_terminal

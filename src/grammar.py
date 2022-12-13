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

    def closure(self):
        # List of states where each state is a dictionary that maps a starting nonterminal to a list
        # where each element is a list of terminals and nonterminals
        states = [self._productions]

        productions = deepcopy(self._productions)

        while True:
            added_production = False

            # Iterate all starting nonterminals and their lists of productions
            for src, dst_list in productions.items():
                # Iterate all productions in a nonterminal's production list
                for dst in dst_list:
                    # Find the index of the dot, if any
                    dot_index = None

                    for i, dst_item in enumerate(dst):
                        if isinstance(dst_item, Dot):
                            dot_index = i
                            break

                    # Skip the iteration if the production doesn't contain a dot
                    if dot_index is None:
                        continue

                    # Skip the iteration if the dot is at the end of the production
                    next_index = dot_index + 1
                    if next_index >= len(dst):
                        continue

                    # Generate a production where the dot and the next item are swapped
                    swapped_production = (
                        dst[:dot_index]
                        + [dst[next_index], Dot()]
                        + dst[(dot_index + 2) :]
                    )

                    # Skip the iteration if the production already exists
                    if swapped_production in productions[src]:
                        continue

                    # Add the production and set the flag to continue iterations
                    productions[src].append(swapped_production)
                    added_production = True

                    # Create a new state to add to the result
                    state = {}
                    state[src] = [swapped_production]

                    non_terminal_index = next_index + 1

                    # If the item right after the dot is a nonterminal, add its productions to the
                    # state
                    if (
                        non_terminal_index < len(swapped_production)
                        and swapped_production[non_terminal_index]
                        in self._non_terminals
                    ):
                        non_terminal = swapped_production[non_terminal_index]
                        state[non_terminal] = []

                        for dst in self._productions[non_terminal]:
                            if dst != swapped_production:
                                state[non_terminal].append(dst)

                    states.append(state)

            if not added_production:
                break

        return states


g = Grammar()
g.load_from_file("../docs/simple-syntax.json")
ag = AugmentedGrammar(g, "S")
result = ag.closure()

for i, state in enumerate(result):
    print(f"[STATE {i}]")

    for src, dst_list in state.items():
        for dst in dst_list:
            print(f"{src} -> {dst}")

    print()

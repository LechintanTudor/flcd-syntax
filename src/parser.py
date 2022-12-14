from copy import deepcopy

from grammar import Grammar, AugmentedGrammar, Dot


class Parser:
    def __init__(self, grammar: Grammar, program: str):
        self.closures = []
        self.grammar = grammar
        self.program = program
        self.aug_grammar = AugmentedGrammar(self.grammar, program)

    def get_symbol_after_dot(self, production):
        element_iter = iter(production[1])
        found_dot = False

        while True:
            try:
                element = next(element_iter)

                if not found_dot:
                    if isinstance(element, Dot):
                        found_dot = True
                else:
                    if (
                        element
                        in self.grammar.get_non_terminals()
                        + self.grammar.get_terminals()
                    ):
                        return element
                    else:
                        return None
            except StopIteration:
                return None

    def closure(self, productions):
        result = deepcopy(productions)
        while True:
            new_entry = False
            for production in result:
                el_after_dot = self.get_symbol_after_dot(production)
                if el_after_dot in self.aug_grammar.get_non_terminals():
                    possible_productions = self.aug_grammar.get_productions(
                        non_terminal=el_after_dot
                    )
                    for possible_production in possible_productions:
                        if (el_after_dot, possible_production) not in result:
                            result.append((el_after_dot, possible_production))
                            new_entry = True
            if not new_entry:
                break
        return result

    def dot_index(self, production):
        dot_index = None

        for i, dst_item in enumerate(production[1]):
            if isinstance(dst_item, Dot):
                dot_index = i
                break
        return dot_index

    def goto(self, item_set, symbol):
        result = []
        for item in item_set:
            el_after_dot = self.get_symbol_after_dot(item)
            if el_after_dot != symbol:
                continue
            dot_index = self.dot_index(item)
            swapped_production = (
                item[0],
                item[1][:dot_index]
                + [item[1][dot_index + 1], Dot()]
                + item[1][(dot_index + 2) :],
            )
            result += self.closure([swapped_production])
        return result

    def colcan(self):
        can = self.closure(
            [
                (self.aug_grammar.root_non_terminal, prod)
                for prod in self.aug_grammar.get_productions(
                    self.aug_grammar.root_non_terminal
                )
            ]
        )
        while True:
            new_entry = False
            for s in can:
                for symbol in (
                    self.aug_grammar.get_non_terminals()
                    + self.aug_grammar.get_terminals()
                ):
                    new_states = self.goto([s], symbol)
                    if len(new_states) > 0:
                        for new_state in new_states:
                            if new_state not in can:
                                can.append(new_state)
                                new_entry = True
            if not new_entry:
                break
        return can

    def lr0(self):
        # List of states where each state is a dictionary that maps a starting nonterminal to a list
        # where each element is a list of terminals and nonterminals
        states = [self.aug_grammar.productions]

        productions = deepcopy(self.aug_grammar.get_productions())

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
                        in self.aug_grammar.non_terminals
                    ):
                        non_terminal = swapped_production[non_terminal_index]
                        state[non_terminal] = []

                        for dst in self.aug_grammar.get_productions(
                            non_terminal=non_terminal
                        ):
                            if dst != swapped_production:
                                state[non_terminal].append(dst)

                    states.append(state)

            if not added_production:
                break

        return states


# g = Grammar()
# g.load_from_file("docs/simple.json")
# ag = AugmentedGrammar(g, "S")
# ag.get_productions()
# p = Parser(g, "S")
# closure = p.closure([("S'", [Dot(), "S"])])
# goto = p.goto([("S'", [Dot(), "S"])], 'S')

# for s in p.colcan():
#     print(s)
#     print()

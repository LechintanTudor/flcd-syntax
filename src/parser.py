from grammar import Grammar, AugmentedGrammar, Dot


class Parser:
    def __init__(self, grammar: Grammar, program: str):
        self.closures = []
        self.grammar = grammar
        self.program = program
        self.aug_grammar = AugmentedGrammar(self.grammar)

    def create_closures(self):
        self.closures = self.aug_grammar.get_productions(non_terminal=self.program)
        while True:
            old_closures = self.closures
            for closure in self.closures:
                pass
            break

    def get_non_term_after_dot(self, closure):
        element_iter = iter(closure)
        found_dot = False

        while True:
            try:
                element = next(element_iter)

                if not found_dot:
                    if isinstance(element, Dot):
                        found_dot = True
                else:
                    if element in self.grammar.get_non_terminals():
                        return element
                    else:
                        return None
            except StopIteration:
                return None


g = Grammar()
g.load_from_file("docs/simple.json")
ag = AugmentedGrammar(g)
ag.get_productions()
p = Parser(g, "S")
p.create_closures()

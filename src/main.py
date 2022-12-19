from grammar import Grammar

if __name__ == "__main__":
    grammar = Grammar.load_from_json("docs/simple.json")
    augmented_grammar = grammar.augment()
    print(augmented_grammar)

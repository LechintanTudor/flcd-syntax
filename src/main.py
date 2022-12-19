from grammar import Grammar

if __name__ == "__main__":
    grammar = Grammar.load_from_json("docs/simple.json")
    print(grammar)

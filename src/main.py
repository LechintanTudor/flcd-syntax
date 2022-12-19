from grammar import Grammar
from parser import Parser
from item import Item
from dot import Dot


if __name__ == "__main__":
    grammar = Grammar.load_from_json("docs/simple.json")
    parser = Parser(grammar)

    initial_state = parser.closure(Item("S'", [Dot, "S"]))
    print(initial_state)

    print()

    next_state = parser.goto(initial_state, "b")
    print(next_state)
